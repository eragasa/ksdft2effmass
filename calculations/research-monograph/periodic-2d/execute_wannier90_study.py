#!/usr/bin/env python3
"""Execute the authorized bounded periodic-2D Wannier90 study."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class BoundedWannier90Study:
    """Generate and execute the exact declared non-DFT study cases."""

    __slots__ = ()

    def execute(
        self,
        study_path: Path,
        base_input_path: Path,
        preparer_path: Path,
        executable: Path,
        output_root: Path,
    ) -> dict[str, JsonValue]:
        study = self._mapping(
            cast(JsonValue, json.loads(study_path.read_text(encoding="utf-8")))
        )
        if self._integer(study["schema_version"]) != 1:
            raise ValueError("unsupported study schema")
        limits = self._mapping(study["execution_limits"])
        cases = self._array(study["new_cases"])
        if len(cases) > self._integer(limits["maximum_new_cases"]):
            raise ValueError("case count exceeds the authorized maximum")
        timeout = self._integer(limits["maximum_seconds_per_stage"])
        maximum_memory = self._integer(limits["maximum_resident_bytes_per_stage"])
        maximum_output = self._integer(limits["maximum_external_output_bytes_per_case"])
        base = self._mapping(
            cast(JsonValue, json.loads(base_input_path.read_text(encoding="utf-8")))
        )
        output_root.mkdir(parents=True, exist_ok=False)
        records: list[JsonValue] = []
        for case_value in cases:
            case = self._mapping(case_value)
            record = self._execute_case(
                case,
                base,
                preparer_path,
                executable,
                output_root,
                timeout,
                maximum_memory,
                maximum_output,
            )
            records.append(record)
            if self._boolean(self._mapping(record)["resource_limit_exceeded"]):
                break
        result: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": self._string(study["experiment_id"]),
            "evidence_status": "calculated bounded synthetic execution",
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "authorization_checkpoint": "RM-PERIODIC-2D-NONDFT-STUDY-HC06",
            "provenance": {
                "study_input_sha256": self._sha256(study_path),
                "base_input_sha256": self._sha256(base_input_path),
                "preparer_sha256": self._sha256(preparer_path),
                "driver_sha256": self._sha256(Path(__file__).resolve()),
                "executable_path": str(executable),
                "executable_sha256": self._sha256(executable),
                "python_version": platform.python_version(),
                "output_root": str(output_root),
            },
            "limits": limits,
            "cases": records,
        }
        (output_root / "execution-result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return result

    def _execute_case(
        self,
        case: dict[str, JsonValue],
        base: dict[str, JsonValue],
        preparer_path: Path,
        executable: Path,
        output_root: Path,
        timeout: int,
        maximum_memory: int,
        maximum_output: int,
    ) -> dict[str, JsonValue]:
        case_id = self._string(case["case_id"])
        case_root = output_root / case_id
        case_root.mkdir()
        variant = dict(base)
        variant["plane_wave_cutoff"] = self._integer(case["plane_wave_cutoff"])
        variant["reciprocal_mesh_size"] = self._integer(case["reciprocal_mesh_size"])
        input_path = case_root / "composite-input.json"
        input_path.write_text(
            json.dumps(variant, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        transverse_length = self._real(case["transverse_lattice_length"])
        stages: list[JsonValue] = []
        initial = self._run(
            (
                sys.executable,
                str(preparer_path),
                "--input",
                str(input_path),
                "--workdir",
                str(case_root),
                "--stage",
                "initial",
                "--transverse-length",
                f"{transverse_length:.16g}",
            ),
            case_root,
            "prepare-initial",
            timeout,
        )
        stages.append(initial)
        if self._integer(self._mapping(initial)["exit_code"]) == 0:
            preprocessing = self._run_timed(
                (str(executable), "-pp", "low_triple"),
                case_root / "low_triple",
                "preprocessing",
                timeout,
            )
            stages.append(preprocessing)
        if self._stage_passed(stages, "preprocessing"):
            interface = self._run(
                (
                    sys.executable,
                    str(preparer_path),
                    "--input",
                    str(input_path),
                    "--workdir",
                    str(case_root),
                    "--stage",
                    "interface",
                    "--transverse-length",
                    f"{transverse_length:.16g}",
                ),
                case_root,
                "prepare-interface",
                timeout,
            )
            stages.append(interface)
        if self._stage_passed(stages, "prepare-interface"):
            localization = self._run_timed(
                (str(executable), "low_triple"),
                case_root / "low_triple",
                "localization",
                timeout,
            )
            stages.append(localization)
        output_bytes = sum(
            path.stat().st_size for path in case_root.rglob("*") if path.is_file()
        )
        maximum_observed_memory = max(
            (
                self._integer(self._mapping(value)["maximum_resident_bytes"])
                for value in stages
                if self._mapping(value)["maximum_resident_bytes"] is not None
            ),
            default=0,
        )
        resource_limit_exceeded = (
            maximum_observed_memory > maximum_memory or output_bytes > maximum_output
        )
        completed = self._stage_passed(stages, "localization")
        return {
            "case_id": case_id,
            "study_axis": self._string(case["study_axis"]),
            "plane_wave_cutoff": self._integer(case["plane_wave_cutoff"]),
            "reciprocal_mesh_size": self._integer(case["reciprocal_mesh_size"]),
            "transverse_lattice_length": transverse_length,
            "input_sha256": self._sha256(input_path),
            "stages": stages,
            "completed": completed,
            "resource_limit_exceeded": resource_limit_exceeded,
            "external_output_bytes": output_bytes,
            "file_manifest": self._files(case_root),
        }

    def _run(
        self,
        command: tuple[str, ...],
        cwd: Path,
        label: str,
        timeout: int,
    ) -> dict[str, JsonValue]:
        stdout_path = cwd / f"{label}.stdout"
        stderr_path = cwd / f"{label}.stderr"
        try:
            with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
                completed = subprocess.run(
                    command,
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
        return {
            "stage": label,
            "command": list(command),
            "exit_code": exit_code,
            "timed_out": timed_out,
            "maximum_resident_bytes": None,
        }

    def _run_timed(
        self,
        command: tuple[str, ...],
        cwd: Path,
        label: str,
        timeout: int,
    ) -> dict[str, JsonValue]:
        time_path = cwd / f"{label}.time"
        wrapped = ("/usr/bin/time", "-l", "-o", str(time_path), *command)
        record = self._run(wrapped, cwd, label, timeout)
        if time_path.is_file():
            text = time_path.read_text(encoding="utf-8")
            match = re.search(r"(\d+)\s+maximum resident set size", text)
            if match is None:
                raise ValueError(f"{label} resource record lacks resident memory")
            record["maximum_resident_bytes"] = int(match.group(1))
            elapsed = re.search(r"\s*([0-9.]+)\s+real", text)
            if elapsed is None:
                raise ValueError(f"{label} resource record lacks elapsed time")
            record["elapsed_seconds"] = float(elapsed.group(1))
        return record

    def _stage_passed(self, stages: list[JsonValue], name: str) -> bool:
        return any(
            self._mapping(value)["stage"] == name
            and self._integer(self._mapping(value)["exit_code"]) == 0
            for value in stages
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

    def _sha256(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
        return value

    def _array(self, value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    def _string(self, value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    def _integer(self, value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    def _real(self, value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _boolean(self, value: JsonValue) -> bool:
        if not isinstance(value, bool):
            raise TypeError("expected a boolean")
        return value


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", type=Path, required=True)
    parser.add_argument("--base-input", type=Path, required=True)
    parser.add_argument("--preparer", type=Path, required=True)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    arguments = parser.parse_args()
    result = BoundedWannier90Study().execute(
        cast(Path, arguments.study).resolve(),
        cast(Path, arguments.base_input).resolve(),
        cast(Path, arguments.preparer).resolve(),
        cast(Path, arguments.executable).resolve(),
        cast(Path, arguments.output_root).resolve(),
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
