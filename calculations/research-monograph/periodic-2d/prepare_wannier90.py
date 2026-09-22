#!/usr/bin/env python3
"""Prepare the frozen periodic-2D rank-three Wannier90 interface."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, replace
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
    """Frozen parent, rank, mesh, and trial-orbital interface controls."""

    lambda_x: float
    lambda_y: float
    lambda_xy: float
    cutoff: int
    mesh_size: int
    rank: int
    center: tuple[float, float]
    momentum_width: float
    transverse_lattice_length: float = 1.0


class InterfaceInputDeserializer:
    """Deserialize the owned subset of the composite input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> InterfaceSpecification:
        root = self._mapping(cast(JsonValue, json.loads(payload.decode())))
        potential = self._mapping(root["potential"])
        trials = self._mapping(root["trial_orbitals"])
        retained = self._integers(root["retained_band_indices"])
        center = self._reals(trials["center_fractional"])
        if retained != tuple(range(len(retained))) or len(retained) != 3:
            raise ValueError("Wannier90 interface requires the lowest rank-three group")
        if len(center) != 2:
            raise ValueError("trial center must have two coordinates")
        return InterfaceSpecification(
            lambda_x=self._real(potential["lambda_x"]),
            lambda_y=self._real(potential["lambda_y"]),
            lambda_xy=self._real(potential["lambda_xy"]),
            cutoff=self._integer(root["plane_wave_cutoff"]),
            mesh_size=self._integer(root["reciprocal_mesh_size"]),
            rank=len(retained),
            center=(center[0], center[1]),
            momentum_width=self._real(trials["momentum_width"]),
        )

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("value must be an object")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be numeric")
        return float(value)

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be an integer")
        return value

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._real(item) for item in value)

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._integer(item) for item in value)


class Wannier90InterfacePreparer:
    """Write initial and post-preprocessing Wannier90 interface files."""

    __slots__ = ()

    seed = "low_triple"

    def write_initial(self, source: InterfaceSpecification, workdir: Path) -> None:
        seed_dir = workdir / self.seed
        seed_dir.mkdir(parents=True, exist_ok=True)
        kpoints, energies, vectors, projections = self._parent(source)
        (seed_dir / f"{self.seed}.win").write_text(
            self._win(source, kpoints), encoding="utf-8"
        )
        (seed_dir / f"{self.seed}.eig").write_text(
            self._eig(energies), encoding="utf-8"
        )
        (seed_dir / f"{self.seed}.amn").write_text(
            self._amn(projections), encoding="utf-8"
        )
        _ = vectors
        self._manifest(source, workdir, "initial_inputs_ready")

    def write_interface(self, source: InterfaceSpecification, workdir: Path) -> None:
        seed_dir = workdir / self.seed
        nnkp = seed_dir / f"{self.seed}.nnkp"
        if not nnkp.is_file():
            raise FileNotFoundError(f"missing preprocessing output {nnkp}")
        neighbors = self._neighbors(nnkp.read_text(encoding="utf-8"))
        _, _, vectors, _ = self._parent(source)
        (seed_dir / f"{self.seed}.mmn").write_text(
            self._mmn(vectors, neighbors, source.cutoff), encoding="utf-8"
        )
        self._manifest(source, workdir, "interface_ready")

    @staticmethod
    def _win(source: InterfaceSpecification, kpoints: npt.NDArray[np.float64]) -> str:
        lines = [
            f"num_bands = {source.rank}",
            f"num_wann = {source.rank}",
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
            (
                "0.0 0.0 1.0"
                if source.transverse_lattice_length == 1.0
                else f"0.0 0.0 {source.transverse_lattice_length:.16f}"
            ),
            "end unit_cell_cart",
            "",
            "begin atoms_frac",
            "H 0.5 0.5 0.0",
            "end atoms_frac",
            "",
            "begin projections",
            "random",
            "end projections",
            "",
            f"mp_grid = {source.mesh_size} {source.mesh_size} 1",
            "",
            "begin kpoints",
        ]
        lines.extend(f"{kx:.16f} {ky:.16f} 0.0" for kx, ky in kpoints)
        lines.extend(["end kpoints", ""])
        return "\n".join(lines)

    @staticmethod
    def _eig(energies: npt.NDArray[np.float64]) -> str:
        lines: list[str] = []
        for k_index in range(energies.shape[0]):
            for band in range(energies.shape[1]):
                lines.append(
                    f"{band + 1:5d} {k_index + 1:5d} {energies[k_index, band]:.16e}"
                )
        return "\n".join(lines) + "\n"

    @staticmethod
    def _amn(projections: npt.NDArray[np.complex128]) -> str:
        rank = projections.shape[1]
        lines = [
            "Synthetic s/px/py projections for periodic-2D retained triple",
            f"{rank:12d}{projections.shape[0]:12d}{rank:12d}",
        ]
        for k_index in range(projections.shape[0]):
            for projection in range(rank):
                for band in range(rank):
                    value = projections[k_index, band, projection]
                    lines.append(
                        f"{band + 1:5d}{projection + 1:5d}{k_index + 1:5d} "
                        f"{value.real:22.14e} {value.imag:22.14e}"
                    )
        return "\n".join(lines) + "\n"

    @staticmethod
    def _mmn(
        frames: npt.NDArray[np.complex128],
        neighbors: tuple[tuple[int, int, int, int, int], ...],
        cutoff: int,
    ) -> str:
        rank = frames.shape[-1]
        neighbor_count = len(neighbors) // frames.shape[0]
        lines = [
            "Synthetic overlaps for periodic-2D retained triple",
            f"{rank:12d}{frames.shape[0]:12d}{neighbor_count:12d}",
        ]
        for first, second, gx, gy, gz in neighbors:
            shifted = Wannier90InterfacePreparer._shift(
                frames[second - 1], cutoff, gx, gy
            )
            overlap = frames[first - 1].conj().T @ shifted
            _ = gz
            lines.append(f"{first:5d}{second:5d}{gx:5d}{gy:5d}{gz:5d}")
            for column in range(rank):
                for row in range(rank):
                    value = overlap[row, column]
                    lines.append(f"{value.real:22.14e} {value.imag:22.14e}")
        return "\n".join(lines) + "\n"

    def _parent(
        self, source: InterfaceSpecification
    ) -> tuple[
        npt.NDArray[np.float64],
        npt.NDArray[np.float64],
        npt.NDArray[np.complex128],
        npt.NDArray[np.complex128],
    ]:
        fractions = np.arange(source.mesh_size, dtype=float) / source.mesh_size
        kpoints = np.asarray([(kx, ky) for kx in fractions for ky in fractions])
        dimension = (2 * source.cutoff + 1) ** 2
        energies = np.empty((kpoints.shape[0], source.rank), float)
        vectors = np.empty((kpoints.shape[0], dimension, source.rank), complex)
        projections = np.empty((kpoints.shape[0], source.rank, source.rank), complex)
        for index, (kx, ky) in enumerate(kpoints):
            operator = self._operator(source, float(kx), float(ky))
            spectrum, states = np.linalg.eigh(operator)
            retained = states[:, : source.rank]
            trial = self._trials(source, float(kx), float(ky))
            energies[index] = spectrum[: source.rank]
            vectors[index] = retained
            projections[index] = retained.conj().T @ trial
        return kpoints, energies, vectors, projections

    @staticmethod
    def _operator(
        source: InterfaceSpecification, kx: float, ky: float
    ) -> ComplexMatrix:
        indices = np.arange(-source.cutoff, source.cutoff + 1)
        p, q = np.meshgrid(indices, indices, indexing="ij")
        flat_p = p.ravel()
        flat_q = q.ravel()
        dp = flat_p[:, None] - flat_p[None, :]
        dq = flat_q[:, None] - flat_q[None, :]
        matrix = np.diag((kx + flat_p) ** 2 + (ky + flat_q) ** 2).astype(complex)
        matrix += (source.lambda_x / 2.0) * ((np.abs(dp) == 1) & (dq == 0))
        matrix += (source.lambda_y / 2.0) * ((dp == 0) & (np.abs(dq) == 1))
        matrix += (source.lambda_xy / 4.0) * ((np.abs(dp) == 1) & (np.abs(dq) == 1))
        return matrix

    @staticmethod
    def _trials(source: InterfaceSpecification, kx: float, ky: float) -> ComplexMatrix:
        columns: list[npt.NDArray[np.complex128]] = []
        for character in range(source.rank):
            values: list[complex] = []
            for p in range(-source.cutoff, source.cutoff + 1):
                for q in range(-source.cutoff, source.cutoff + 1):
                    x = kx + p
                    y = ky + q
                    base = np.exp(-0.5 * source.momentum_width**2 * (x * x + y * y))
                    phase = np.exp(
                        -2j * np.pi * (source.center[0] * x + source.center[1] * y)
                    )
                    factor = (
                        1.0 if character == 0 else 1j * (x if character == 1 else y)
                    )
                    values.append(complex(factor * base * phase))
            vector = np.asarray(values)
            vector /= np.linalg.norm(vector)
            columns.append(vector)
        return np.linalg.qr(np.column_stack(columns))[0]

    @staticmethod
    def _shift(frame: ComplexMatrix, cutoff: int, gx: int, gy: int) -> ComplexMatrix:
        side = 2 * cutoff + 1
        source = frame.reshape(side, side, frame.shape[1])
        result = np.zeros_like(source)
        x_source = slice(max(gx, 0), min(side + gx, side))
        x_target = slice(max(-gx, 0), min(side - gx, side))
        y_source = slice(max(gy, 0), min(side + gy, side))
        y_target = slice(max(-gy, 0), min(side - gy, side))
        result[x_target, y_target] = source[x_source, y_source]
        return result.reshape(frame.shape)

    @staticmethod
    def _neighbors(text: str) -> tuple[tuple[int, int, int, int, int], ...]:
        lines = [line.strip() for line in text.splitlines()]
        try:
            begin = lines.index("begin nnkpts")
            end = lines.index("end nnkpts")
        except ValueError as exc:
            raise ValueError("nnkp lacks an nnkpts block") from exc
        block = [line for line in lines[begin + 1 : end] if line]
        if not block:
            raise ValueError("nnkpts block is empty")
        neighbor_count = int(block[0])
        records: list[tuple[int, int, int, int, int]] = []
        for line in block[1:]:
            fields = line.split()
            if len(fields) != 5:
                raise ValueError("nnkpts entry must contain five integers")
            records.append(tuple(int(value) for value in fields))  # type: ignore[arg-type]
        if len(records) % neighbor_count != 0:
            raise ValueError("nnkpts count disagrees with neighbor count")
        return tuple(records)

    @staticmethod
    def _manifest(source: InterfaceSpecification, workdir: Path, status: str) -> None:
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
                "lambda_x": source.lambda_x,
                "lambda_y": source.lambda_y,
                "lambda_xy": source.lambda_xy,
                "plane_wave_cutoff": source.cutoff,
                "mesh": [source.mesh_size, source.mesh_size, 1],
                "rank": source.rank,
                "transverse_lattice_length": source.transverse_lattice_length,
            },
            "embedding": (
                "two active dimensions and one inactive unit transverse factor"
            ),
            "energy_interface_convention": "one numerical E_G is written as one eV",
            "files": files,
        }
        (workdir / "interface-manifest.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n"
        )


class CommandAdapter:
    """Adapt explicit paths and stage choice to the interface preparer."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=Path, required=True)
        parser.add_argument("--workdir", type=Path, required=True)
        parser.add_argument("--stage", choices=("initial", "interface"), required=True)
        parser.add_argument("--embedding", choices=("unit", "balanced"), default="unit")
        parser.add_argument("--transverse-length", type=float)
        arguments = parser.parse_args(argv)
        source = InterfaceInputDeserializer().execute(
            cast(Path, arguments.input).resolve().read_bytes()
        )
        transverse_length = cast(float | None, arguments.transverse_length)
        if transverse_length is not None:
            if not np.isfinite(transverse_length) or transverse_length <= 0.0:
                raise ValueError("transverse length must be finite and positive")
            source = replace(source, transverse_lattice_length=transverse_length)
        elif arguments.embedding == "balanced":
            source = replace(source, transverse_lattice_length=float(source.mesh_size))
        preparer = Wannier90InterfacePreparer()
        workdir = cast(Path, arguments.workdir).resolve()
        if arguments.stage == "initial":
            preparer.write_initial(source, workdir)
        else:
            preparer.write_interface(source, workdir)
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
