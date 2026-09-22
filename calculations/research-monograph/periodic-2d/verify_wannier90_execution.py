#!/usr/bin/env python3
"""Verify the retained periodic-2D Wannier90 preprocessing failure."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class Wannier90FailureVerifier:
    """Check external identities, failure disposition, and stage exclusion."""

    __slots__ = ()

    def execute(self, record_path: Path) -> None:
        root = self._mapping(
            cast(JsonValue, json.loads(record_path.read_text(encoding="utf-8")))
        )
        if self._integer(root["schema_version"]) != 1:
            raise ValueError("unsupported execution record schema")
        if root["evidence_status"] != "failed protected scientific execution":
            raise ValueError("unexpected evidence status")
        if root["status"] != "failed_preprocessing_retained_no_retry":
            raise ValueError("unexpected execution disposition")
        if self._boolean(root["interface_stage_started"]):
            raise ValueError("interface stage must not have started")
        if self._boolean(root["localization_stage_started"]):
            raise ValueError("localization stage must not have started")
        executable = self._mapping(root["executable"])
        executable_path = Path(self._string(executable["path"]))
        self._identity(
            executable_path,
            self._string(executable["sha256"]),
            "Wannier90 executable",
        )
        run_root = Path(self._string(root["external_run_root"]))
        seed_dir = run_root / "low_triple"
        identities = self._mapping(root["input_identity"])
        for suffix in ("win", "eig", "amn"):
            self._identity(
                seed_dir / f"low_triple.{suffix}",
                self._string(identities[f"{suffix}_sha256"]),
                f"{suffix} input",
            )
        preprocessing = self._mapping(root["preprocessing"])
        self._equal(self._integer(preprocessing["exit_code"]), 1, "exit code")
        self._identity(
            seed_dir / "low_triple.wout",
            self._string(preprocessing["wout_sha256"]),
            "preprocessing wout",
        )
        self._identity(
            seed_dir / "low_triple.pp.stderr",
            self._string(preprocessing["stderr_sha256"]),
            "preprocessing stderr",
        )
        wout = (seed_dir / "low_triple.wout").read_text(encoding="utf-8")
        failure = self._string(preprocessing["failure"])
        if failure not in wout:
            raise AssertionError("retained wout does not contain the failure")
        if wout.count("| b-vector") != 1430:
            raise AssertionError("unexpected candidate b-vector count")
        if self._boolean(preprocessing["nnkp_created"]):
            raise ValueError("execution record incorrectly claims nnkp output")
        forbidden = (
            "low_triple.nnkp",
            "low_triple.mmn",
            "low_triple.chk",
            "low_triple_u.mat",
            "low_triple_hr.dat",
        )
        present = [name for name in forbidden if (seed_dir / name).exists()]
        if present:
            raise AssertionError(
                f"post-preprocessing outputs unexpectedly exist: {present}"
            )
        exit_code = int((seed_dir / "low_triple.pp.exitcode").read_text().strip())
        self._equal(exit_code, 1, "retained exit code")
        time_text = (seed_dir / "low_triple.pp.time").read_text(encoding="utf-8")
        if "maximum resident set size" not in time_text:
            raise AssertionError("resource record lacks maximum resident memory")
        total_bytes = sum(
            path.stat().st_size for path in run_root.rglob("*") if path.is_file()
        )
        self._equal(
            total_bytes,
            self._integer(preprocessing["external_output_bytes_after_stage"]),
            "external output size",
        )
        if not self._boolean(root["resource_limits_respected"]):
            raise AssertionError("resource limit disposition is false")

    def _identity(self, path: Path, expected: str, label: str) -> None:
        if not path.is_file():
            raise FileNotFoundError(f"{label} is absent: {path}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
            )

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
        return value

    def _string(self, value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    def _integer(self, value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    def _boolean(self, value: JsonValue) -> bool:
        if not isinstance(value, bool):
            raise TypeError("expected a boolean")
        return value

    def _equal(self, actual: int, expected: int, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label}: actual={actual}, expected={expected}")


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    arguments = parser.parse_args()
    Wannier90FailureVerifier().execute(arguments.record)
    print("periodic_2d_wannier90_failure_verification=PASS")


if __name__ == "__main__":
    main()
