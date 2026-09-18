#!/usr/bin/env python3
"""Execute the authorized bounded periodic-2D optimizer-basin study."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import re
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexTensor = npt.NDArray[np.complex128]


class InitialGaugeAction:
    """Apply one declared smooth periodic unitary to baseline AMN matrices."""

    __slots__ = ()

    def execute(
        self,
        source_path: Path,
        target_path: Path,
        mesh_size: int,
        gauge: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        header, matrices = self._read(source_path)
        if matrices.shape != (mesh_size * mesh_size, 3, 3):
            raise ValueError("baseline AMN dimensions disagree with declared mesh")
        transformed = np.empty_like(matrices)
        maximum_unitarity_defect = 0.0
        maximum_subspace_gram_defect = 0.0
        terms = self._array(gauge["ordered_generator_terms"])
        for index in range(matrices.shape[0]):
            kx = (index // mesh_size) / mesh_size
            ky = (index % mesh_size) / mesh_size
            unitary = self._unitary(terms, kx, ky)
            transformed[index] = matrices[index] @ unitary
            maximum_unitarity_defect = max(
                maximum_unitarity_defect,
                float(np.linalg.norm(unitary.conj().T @ unitary - np.eye(3))),
            )
            maximum_subspace_gram_defect = max(
                maximum_subspace_gram_defect,
                float(
                    np.linalg.norm(
                        transformed[index] @ transformed[index].conj().T
                        - matrices[index] @ matrices[index].conj().T
                    )
                ),
            )
        if maximum_unitarity_defect > 1.0e-12:
            raise AssertionError("seed unitary failed its numerical invariant")
        if maximum_subspace_gram_defect > 1.0e-12:
            raise AssertionError("seed transformation changed the retained Gram matrix")
        self._write(target_path, header, transformed)
        return {
            "gauge_id": self._string(gauge["gauge_id"]),
            "source_amn_sha256": self._sha256(source_path),
            "seeded_amn_sha256": self._sha256(target_path),
            "maximum_unitarity_frobenius_defect": maximum_unitarity_defect,
            "maximum_subspace_gram_frobenius_defect": (maximum_subspace_gram_defect),
        }

    def _unitary(self, terms: list[JsonValue], kx: float, ky: float) -> ComplexMatrix:
        result = np.eye(3, dtype=complex)
        for value in terms:
            term = self._mapping(value)
            harmonic = self._integers(term["harmonic"])
            if len(harmonic) != 2:
                raise ValueError("gauge harmonic must contain two integers")
            angle = self._real(term["amplitude"]) * math.sin(
                2.0 * math.pi * (harmonic[0] * kx + harmonic[1] * ky)
                + self._real(term["phase_radians"])
            )
            generator = self._generator(self._string(term["generator"]))
            eigenvalues, eigenvectors = np.linalg.eigh(generator)
            exponential = (
                eigenvectors * np.exp(1j * angle * eigenvalues)[None, :]
            ) @ eigenvectors.conj().T
            result = result @ exponential
        return result

    @staticmethod
    def _generator(name: str) -> ComplexMatrix:
        matrix = np.zeros((3, 3), dtype=complex)
        if name.startswith("x") or name.startswith("y"):
            if name not in {"x01", "y01", "x02", "y02", "x12", "y12"}:
                raise ValueError(f"unsupported generator {name}")
            first = int(name[1])
            second = int(name[2])
            if name[0] == "x":
                matrix[first, second] = 1.0
                matrix[second, first] = 1.0
            else:
                matrix[first, second] = -1j
                matrix[second, first] = 1j
            return matrix
        if name == "diag01":
            return np.diag([1.0, -1.0, 0.0]).astype(complex) / math.sqrt(2.0)
        if name == "diag012":
            return np.diag([1.0, 1.0, -2.0]).astype(complex) / math.sqrt(6.0)
        raise ValueError(f"unsupported generator {name}")

    def _read(self, path: Path) -> tuple[str, ComplexTensor]:
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) < 2:
            raise ValueError("AMN file is incomplete")
        dimensions = [int(value) for value in lines[1].split()]
        if len(dimensions) != 3:
            raise ValueError("AMN dimension record must contain three integers")
        bands, kpoints, projections = dimensions
        matrices = np.empty((kpoints, bands, projections), dtype=complex)
        expected = bands * kpoints * projections
        if len(lines[2:]) != expected:
            raise ValueError("AMN payload size disagrees with dimensions")
        for line in lines[2:]:
            fields = line.split()
            if len(fields) != 5:
                raise ValueError("AMN entry must contain five values")
            band, projection, kpoint = (int(value) for value in fields[:3])
            matrices[kpoint - 1, band - 1, projection - 1] = complex(
                float(fields[3]), float(fields[4])
            )
        return lines[0], matrices

    @staticmethod
    def _write(path: Path, header: str, matrices: ComplexTensor) -> None:
        kpoints, bands, projections = matrices.shape
        lines = [header, f"{bands:12d}{kpoints:12d}{projections:12d}"]
        for kpoint in range(kpoints):
            for projection in range(projections):
                for band in range(bands):
                    value = matrices[kpoint, band, projection]
                    lines.append(
                        f"{band + 1:5d}{projection + 1:5d}{kpoint + 1:5d} "
                        f"{value.real:22.14e} {value.imag:22.14e}"
                    )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected an object")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        result: list[int] = []
        for item in self._array(value):
            if isinstance(item, bool) or not isinstance(item, int):
                raise TypeError("expected integer array entries")
            result.append(item)
        return tuple(result)


class BoundedOptimizerBasinStudy:
    """Prepare shared interfaces and execute every authorized localization once."""

    __slots__ = ("_started",)

    def __init__(self) -> None:
        self._started = 0.0

    def execute(
        self,
        study_path: Path,
        preparer_path: Path,
    ) -> dict[str, JsonValue]:
        study = self._load(study_path)
        if self._integer(study["schema_version"]) != 1:
            raise ValueError("unsupported study schema")
        configurations = [
            self._mapping(value) for value in self._array(study["configurations"])
        ]
        gauges = [
            self._mapping(value) for value in self._array(study["initial_gauges"])
        ]
        limits = self._mapping(study["execution_limits"])
        self._validate_counts(configurations, gauges, limits)
        executable_record = self._mapping(study["executable"])
        executable = Path(self._string(executable_record["path"])).resolve()
        self._identity(
            executable,
            self._string(executable_record["sha256"]),
            "Wannier90 executable",
        )
        repository_root = study_path.parents[3]
        parent_input = repository_root / self._string(study["parent_input_path"])
        output_root = Path(self._string(study["external_output_root"])).resolve()
        output_root.mkdir(parents=True, exist_ok=False)
        timeout = self._integer(limits["maximum_seconds_per_stage"])
        self._started = time.monotonic()
        result: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": self._string(study["experiment_id"]),
            "evidence_status": "calculated bounded synthetic non-DFT execution",
            "authorization_checkpoint": self._string(study["authorization_checkpoint"]),
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "provenance": {
                "study_input_path": str(study_path),
                "study_input_sha256": self._sha256(study_path),
                "parent_input_path": str(parent_input),
                "parent_input_sha256": self._sha256(parent_input),
                "preparer_path": str(preparer_path),
                "preparer_sha256": self._sha256(preparer_path),
                "driver_path": str(Path(__file__).resolve()),
                "driver_sha256": self._sha256(Path(__file__).resolve()),
                "executable_path": str(executable),
                "executable_sha256": self._sha256(executable),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "external_output_root": str(output_root),
            },
            "limits": limits,
            "configurations": [],
            "stopped_early": False,
            "stop_reason": None,
        }
        for configuration in configurations:
            if self._limit_reached(output_root, limits, result):
                break
            record = self._execute_configuration(
                configuration,
                gauges,
                parent_input,
                preparer_path,
                executable,
                output_root,
                timeout,
                limits,
                result,
            )
            self._array(result["configurations"]).append(record)
            self._persist(result, output_root)
        result["elapsed_seconds"] = time.monotonic() - self._started
        result["external_output_bytes"] = self._tree_bytes(output_root)
        result["completed_localizations"] = sum(
            len(self._array(self._mapping(value)["localizations"]))
            for value in self._array(result["configurations"])
        )
        result["all_declared_localizations_attempted"] = self._integer(
            result["completed_localizations"]
        ) == len(configurations) * len(gauges)
        self._persist(result, output_root)
        return result

    def _execute_configuration(
        self,
        configuration: dict[str, JsonValue],
        gauges: list[dict[str, JsonValue]],
        parent_input: Path,
        preparer_path: Path,
        executable: Path,
        output_root: Path,
        timeout: int,
        limits: dict[str, JsonValue],
        result: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        identifier = self._string(configuration["configuration_id"])
        root = output_root / identifier
        base_root = root / "base"
        base_root.mkdir(parents=True)
        base = self._load(parent_input)
        base["plane_wave_cutoff"] = self._integer(configuration["plane_wave_cutoff"])
        base["reciprocal_mesh_size"] = self._integer(
            configuration["reciprocal_mesh_size"]
        )
        input_path = root / "composite-input.json"
        input_path.write_text(
            json.dumps(base, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        transverse = self._real(configuration["transverse_lattice_length"])
        stages: list[JsonValue] = []
        stages.append(
            self._run_timed(
                (
                    sys.executable,
                    str(preparer_path),
                    "--input",
                    str(input_path),
                    "--workdir",
                    str(base_root),
                    "--stage",
                    "initial",
                    "--transverse-length",
                    f"{transverse:.16g}",
                ),
                base_root,
                "prepare-initial",
                timeout,
            )
        )
        seed_dir = base_root / "low_triple"
        if self._passed(stages[-1]):
            stages.append(
                self._run_timed(
                    (str(executable), "-pp", "low_triple"),
                    seed_dir,
                    "preprocessing",
                    timeout,
                )
            )
        if self._passed(stages[-1]):
            stages.append(
                self._run_timed(
                    (
                        sys.executable,
                        str(preparer_path),
                        "--input",
                        str(input_path),
                        "--workdir",
                        str(base_root),
                        "--stage",
                        "interface",
                        "--transverse-length",
                        f"{transverse:.16g}",
                    ),
                    base_root,
                    "prepare-interface",
                    timeout,
                )
            )
        record: dict[str, JsonValue] = {
            "configuration_id": identifier,
            "study_axes": configuration["study_axes"],
            "plane_wave_cutoff": self._integer(configuration["plane_wave_cutoff"]),
            "reciprocal_mesh_size": self._integer(
                configuration["reciprocal_mesh_size"]
            ),
            "transverse_lattice_length": transverse,
            "input_sha256": self._sha256(input_path),
            "interface_stages": stages,
            "interface_completed": all(self._passed(value) for value in stages),
            "localizations": [],
        }
        if record["interface_completed"] is not True:
            return record
        gauge_action = InitialGaugeAction()
        required = [
            "low_triple.win",
            "low_triple.eig",
            "low_triple.nnkp",
            "low_triple.mmn",
        ]
        for gauge in gauges:
            if self._limit_reached(output_root, limits, result):
                break
            gauge_id = self._string(gauge["gauge_id"])
            gauge_root = root / gauge_id
            gauge_seed = gauge_root / "low_triple"
            gauge_seed.mkdir(parents=True)
            for name in required:
                shutil.copy2(seed_dir / name, gauge_seed / name)
            invariant = gauge_action.execute(
                seed_dir / "low_triple.amn",
                gauge_seed / "low_triple.amn",
                self._integer(configuration["reciprocal_mesh_size"]),
                gauge,
            )
            localization = self._run_timed(
                (str(executable), "low_triple"),
                gauge_seed,
                "localization",
                timeout,
            )
            output_bytes = self._tree_bytes(gauge_root)
            memory = localization["maximum_resident_bytes"]
            exceeded = output_bytes > self._integer(
                limits["maximum_external_output_bytes_per_localization"]
            ) or (
                memory is not None
                and self._integer(memory)
                > self._integer(limits["maximum_resident_bytes_per_stage"])
            )
            localization_record: dict[str, JsonValue] = {
                "gauge_id": gauge_id,
                "gauge": gauge,
                "gauge_invariants": invariant,
                "stage": localization,
                "completed": self._passed(localization),
                "resource_limit_exceeded": exceeded,
                "external_output_bytes": output_bytes,
                "file_manifest": self._files(gauge_root),
            }
            self._array(record["localizations"]).append(localization_record)
            if exceeded:
                result["stopped_early"] = True
                result["stop_reason"] = (
                    f"resource limit exceeded by {identifier}/{gauge_id}"
                )
                break
        return record

    def _limit_reached(
        self,
        output_root: Path,
        limits: dict[str, JsonValue],
        result: dict[str, JsonValue],
    ) -> bool:
        if result["stopped_early"] is True:
            return True
        elapsed = time.monotonic() - self._started
        if elapsed > self._integer(limits["maximum_total_seconds"]):
            result["stopped_early"] = True
            result["stop_reason"] = "maximum total execution time exceeded"
            return True
        if self._tree_bytes(output_root) > self._integer(
            limits["maximum_external_output_bytes_total"]
        ):
            result["stopped_early"] = True
            result["stop_reason"] = "maximum total external output exceeded"
            return True
        return False

    def _run_timed(
        self,
        command: tuple[str, ...],
        cwd: Path,
        label: str,
        timeout: int,
    ) -> dict[str, JsonValue]:
        stdout_path = cwd / f"{label}.stdout"
        stderr_path = cwd / f"{label}.stderr"
        time_path = cwd / f"{label}.time"
        wrapped = ("/usr/bin/time", "-l", "-o", str(time_path), *command)
        started = time.monotonic()
        try:
            with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
                completed = subprocess.run(
                    wrapped,
                    cwd=cwd,
                    stdout=stdout,
                    stderr=stderr,
                    check=False,
                    timeout=timeout,
                )
            exit_code = completed.returncode
            timed_out = False
        except subprocess.TimeoutExpired:
            exit_code = 124
            timed_out = True
        record: dict[str, JsonValue] = {
            "stage": label,
            "command": list(command),
            "exit_code": exit_code,
            "timed_out": timed_out,
            "elapsed_seconds": time.monotonic() - started,
            "maximum_resident_bytes": None,
        }
        if time_path.is_file():
            text = time_path.read_text(encoding="utf-8")
            memory = re.search(r"(\d+)\s+maximum resident set size", text)
            elapsed = re.search(r"\s*([0-9.]+)\s+real", text)
            if memory is not None:
                record["maximum_resident_bytes"] = int(memory.group(1))
            if elapsed is not None:
                record["elapsed_seconds"] = float(elapsed.group(1))
        return record

    @staticmethod
    def _passed(value: JsonValue) -> bool:
        if not isinstance(value, dict):
            raise TypeError("stage must be an object")
        code = value["exit_code"]
        return isinstance(code, int) and not isinstance(code, bool) and code == 0

    def _validate_counts(
        self,
        configurations: list[dict[str, JsonValue]],
        gauges: list[dict[str, JsonValue]],
        limits: dict[str, JsonValue],
    ) -> None:
        if len(configurations) != self._integer(limits["maximum_configurations"]):
            raise ValueError("configuration count must equal the authorized count")
        if len(gauges) != self._integer(
            limits["maximum_initial_gauges_per_configuration"]
        ):
            raise ValueError("gauge count must equal the authorized count")
        if len(configurations) * len(gauges) != self._integer(
            limits["maximum_localizations"]
        ):
            raise ValueError("localization count must equal the authorized count")
        if limits["serial_execution_only"] is not True:
            raise ValueError("study must require serial execution")
        if limits["automatic_retry"] is not False:
            raise ValueError("automatic retry must be disabled")

    def _persist(self, result: dict[str, JsonValue], output_root: Path) -> None:
        (output_root / "execution-result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    def _files(self, root: Path) -> list[JsonValue]:
        return [
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": self._sha256(path),
            }
            for path in sorted(root.rglob("*"))
            if path.is_file()
        ]

    @staticmethod
    def _tree_bytes(root: Path) -> int:
        return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())

    @staticmethod
    def _identity(path: Path, expected: str, label: str) -> None:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
            )

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _load(self, path: Path) -> dict[str, JsonValue]:
        return self._mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        )

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected an object")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)


class CommandAdapter:
    """Adapt CLI paths to the bounded study action."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--study", type=Path, required=True)
        parser.add_argument("--preparer", type=Path, required=True)
        arguments = parser.parse_args(argv)
        result = BoundedOptimizerBasinStudy().execute(
            cast(Path, arguments.study).resolve(),
            cast(Path, arguments.preparer).resolve(),
        )
        print(
            json.dumps(
                {
                    "completed_localizations": result["completed_localizations"],
                    "elapsed_seconds": result["elapsed_seconds"],
                    "external_output_bytes": result["external_output_bytes"],
                    "stopped_early": result["stopped_early"],
                    "stop_reason": result["stop_reason"],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
