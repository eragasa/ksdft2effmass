#!/usr/bin/env python3
"""Prepare exact Wannier90 inputs for the frozen periodic-1D comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class InterfaceSpecification:
    """Represent the exact synthetic parent and retained groups."""

    period: float
    strength: float
    cutoff: int
    mesh_size: int
    groups: tuple[tuple[str, int, int], ...]


class InterfaceInputDeserializer:
    """Deserialize the owned subset of the composite input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> InterfaceSpecification:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self._mapping(value)
        if root["schema_version"] != 1:
            raise ValueError("unsupported composite input schema version")
        groups: list[tuple[str, int, int]] = []
        for value_group in self._array(root["retained_band_groups"]):
            group = self._mapping(value_group)
            indices = self._array(group["band_indices"])
            if len(indices) != 2:
                raise ValueError("Wannier90 interface requires two-band groups")
            lower = self._integer(indices[0])
            upper = self._integer(indices[1])
            if upper != lower + 1:
                raise ValueError("retained groups must be contiguous")
            groups.append((self._string(group["id"]), lower, upper))
        return InterfaceSpecification(
            period=self._real(root["period"]),
            strength=self._real(root["potential_strength_over_recoil"]),
            cutoff=self._integer(root["plane_wave_cutoff"]),
            mesh_size=self._integer(root["reciprocal_mesh_size"]),
            groups=tuple(groups),
        )

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("value must be a JSON object")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("value must be a JSON array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        return value

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be an integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be a number")
        return float(value)


class Wannier90InterfacePreparer:
    """Write preprocessing inputs and post-preprocessing overlap matrices."""

    __slots__ = ()

    def write_initial(
        self, specification: InterfaceSpecification, workdir: Path
    ) -> None:
        workdir.mkdir(parents=True, exist_ok=True)
        for seed, lower, upper in specification.groups:
            seed_dir = workdir / seed
            seed_dir.mkdir(parents=True, exist_ok=True)
            momenta, values, _ = self._parent_states(specification, upper + 1)
            (seed_dir / f"{seed}.win").write_text(
                self._win_text(specification, momenta), encoding="utf-8"
            )
            (seed_dir / f"{seed}.eig").write_text(
                self._eig_text(values[:, lower : upper + 1]), encoding="utf-8"
            )
            (seed_dir / f"{seed}.amn").write_text(
                self._amn_text(specification.mesh_size), encoding="utf-8"
            )
        self._write_manifest(specification, workdir, "initial_inputs_ready")

    def write_interface(
        self, specification: InterfaceSpecification, workdir: Path
    ) -> None:
        for seed, lower, upper in specification.groups:
            seed_dir = workdir / seed
            nnkp_path = seed_dir / f"{seed}.nnkp"
            if not nnkp_path.is_file():
                raise FileNotFoundError(f"missing preprocessing output {nnkp_path}")
            neighbors = self._nnkp_neighbors(nnkp_path.read_text(encoding="utf-8"))
            _, _, vectors = self._parent_states(specification, upper + 1)
            retained = vectors[:, :, lower : upper + 1]
            (seed_dir / f"{seed}.mmn").write_text(
                self._mmn_text(retained, neighbors), encoding="utf-8"
            )
        self._write_manifest(specification, workdir, "interface_ready")

    @staticmethod
    def _win_text(
        specification: InterfaceSpecification, momenta: npt.NDArray[np.float64]
    ) -> str:
        lines = [
            "num_bands = 2",
            "num_wann = 2",
            "num_iter = 5000",
            "conv_tol = 1.0d-12",
            "conv_window = 5",
            "precond = true",
            "search_shells = 130",
            "write_hr = true",
            "write_u_matrices = true",
            "translate_home_cell = true",
            "",
            "begin unit_cell_cart",
            "ang",
            "1.0 0.0 0.0",
            "0.0 1.0 0.0",
            "0.0 0.0 1.0",
            "end unit_cell_cart",
            "",
            "begin atoms_frac",
            "H 0.0 0.0 0.0",
            "end atoms_frac",
            "",
            "begin projections",
            "random",
            "end projections",
            "",
            f"mp_grid = {specification.mesh_size} 1 1",
            "",
            "begin kpoints",
        ]
        lines.extend(f"{momentum:.16f} 0.0 0.0" for momentum in momenta)
        lines.extend(["end kpoints", ""])
        return "\n".join(lines)

    @staticmethod
    def _eig_text(values: npt.NDArray[np.float64]) -> str:
        lines: list[str] = []
        for k_index in range(values.shape[0]):
            for band_index in range(values.shape[1]):
                lines.append(
                    f"{band_index + 1:5d} {k_index + 1:5d} "
                    f"{values[k_index, band_index]:.16e}"
                )
        return "\n".join(lines) + "\n"

    @staticmethod
    def _amn_text(mesh_size: int) -> str:
        lines = [
            "Synthetic identity projections for periodic-1D retained pair",
            f"{2:12d}{mesh_size:12d}{2:12d}",
        ]
        for k_index in range(mesh_size):
            for projection in range(2):
                for band in range(2):
                    value = 1.0 if band == projection else 0.0
                    lines.append(
                        f"{band + 1:5d}{projection + 1:5d}{k_index + 1:5d} "
                        f"{value:22.14e} {0.0:22.14e}"
                    )
        return "\n".join(lines) + "\n"

    def _mmn_text(
        self,
        frames: npt.NDArray[np.complex128],
        neighbors: tuple[tuple[int, int, int, int, int], ...],
    ) -> str:
        neighbor_count = len(neighbors) // frames.shape[0]
        lines = [
            "Synthetic overlaps for periodic-1D retained pair",
            f"{2:12d}{frames.shape[0]:12d}{neighbor_count:12d}",
        ]
        for first, second, gx, gy, gz in neighbors:
            first_frame = frames[first - 1]
            second_frame = frames[second - 1]
            shifted = self._shift_reciprocal_coefficients(second_frame, gx)
            overlap = first_frame.conj().T @ shifted
            # The synthetic inactive-direction embedding has unit transverse
            # form factor, so y/z reciprocal shifts do not alter the x overlap.
            _ = (gy, gz)
            lines.append(f"{first:5d}{second:5d}{gx:5d}{gy:5d}{gz:5d}")
            for column in range(2):
                for row in range(2):
                    value = overlap[row, column]
                    lines.append(f"{value.real:22.14e} {value.imag:22.14e}")
        return "\n".join(lines) + "\n"

    @staticmethod
    def _shift_reciprocal_coefficients(
        frame: ComplexMatrix, reciprocal_shift: int
    ) -> ComplexMatrix:
        result = np.zeros_like(frame)
        if reciprocal_shift == 0:
            result[:] = frame
        elif reciprocal_shift > 0:
            result[:-reciprocal_shift] = frame[reciprocal_shift:]
        else:
            amount = -reciprocal_shift
            result[amount:] = frame[:-amount]
        return result

    @staticmethod
    def _nnkp_neighbors(
        text: str,
    ) -> tuple[tuple[int, int, int, int, int], ...]:
        lines = [line.strip() for line in text.splitlines()]
        try:
            begin = lines.index("begin nnkpts")
            end = lines.index("end nnkpts")
        except ValueError as exc:
            raise ValueError("nnkp file lacks an nnkpts block") from exc
        block_lines = [line for line in lines[begin + 1 : end] if line]
        if not block_lines:
            raise ValueError("nnkpts block is empty")
        neighbor_count = int(block_lines[0])
        records: list[tuple[int, int, int, int, int]] = []
        for line in block_lines[1:]:
            fields = line.split()
            if len(fields) != 5:
                raise ValueError("nnkpts entry must contain five integers")
            records.append(
                (
                    int(fields[0]),
                    int(fields[1]),
                    int(fields[2]),
                    int(fields[3]),
                    int(fields[4]),
                )
            )
        if len(records) % neighbor_count != 0:
            raise ValueError("nnkpts entry count disagrees with neighbor count")
        return tuple(records)

    @staticmethod
    def _parent_states(
        specification: InterfaceSpecification, band_count: int
    ) -> tuple[
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        npt.NDArray[np.complex128],
    ]:
        momenta = np.arange(specification.mesh_size, dtype=np.float64)
        momenta /= specification.mesh_size
        dimension = 2 * specification.cutoff + 1
        values = np.empty((specification.mesh_size, band_count), dtype=np.float64)
        vectors = np.empty(
            (specification.mesh_size, dimension, band_count), dtype=np.complex128
        )
        indices = np.arange(-specification.cutoff, specification.cutoff + 1)
        for k_index, momentum in enumerate(momenta):
            matrix = np.diag(np.square(momentum + indices)).astype(np.complex128)
            coupling = 0.5 * specification.strength
            matrix += np.diag(np.full(dimension - 1, coupling), 1)
            matrix += np.diag(np.full(dimension - 1, coupling), -1)
            eigenvalues, eigenvectors = np.linalg.eigh(matrix)
            values[k_index] = eigenvalues[:band_count]
            vectors[k_index] = eigenvectors[:, :band_count]
        return momenta, values, vectors

    @staticmethod
    def _write_manifest(
        specification: InterfaceSpecification, workdir: Path, status: str
    ) -> None:
        files: list[JsonValue] = []
        for path in sorted(workdir.glob("*/*")):
            if path.is_file() and path.name != "interface-manifest.json":
                files.append(
                    {
                        "path": path.relative_to(workdir).as_posix(),
                        "bytes": path.stat().st_size,
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    }
                )
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "status": status,
            "parent": {
                "period": specification.period,
                "potential_strength_over_recoil": specification.strength,
                "plane_wave_cutoff": specification.cutoff,
                "reciprocal_mesh_size": specification.mesh_size,
            },
            "inactive_direction_overlap_convention": (
                "unit transverse form factor for all y/z reciprocal shifts"
            ),
            "energy_interface_convention": "one numerical E_G is written as one eV",
            "files": files,
        }
        (workdir / "interface-manifest.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


class CommandAdapter:
    """Adapt paths and stage selection to the interface preparer."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=Path, required=True)
        parser.add_argument("--workdir", type=Path, required=True)
        parser.add_argument("--stage", choices=("initial", "interface"), required=True)
        args = parser.parse_args(argv)
        specification = InterfaceInputDeserializer().execute(
            cast(Path, args.input).resolve().read_bytes()
        )
        preparer = Wannier90InterfacePreparer()
        workdir = cast(Path, args.workdir).resolve()
        if args.stage == "initial":
            preparer.write_initial(specification, workdir)
        else:
            preparer.write_interface(specification, workdir)
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
