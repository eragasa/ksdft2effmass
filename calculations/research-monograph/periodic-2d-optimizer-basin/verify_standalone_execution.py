#!/usr/bin/env python3
"""Verify the completed standalone-study external execution evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import cast

from execute_study import JsonValue


class StandaloneExecutionVerifier:
    """Verify identities, stage coverage, resources, and retained file manifests."""

    __slots__ = ()

    def execute(
        self,
        proposal_path: Path,
        starts_path: Path,
        execution_path: Path,
    ) -> None:
        proposal = self._load(proposal_path)
        starts = self._load(starts_path)
        result = self._load(execution_path)
        provenance = self._mapping(result["provenance"])
        self._identity(
            proposal_path, self._string(provenance["proposal_sha256"]), "proposal"
        )
        self._identity(starts_path, self._string(provenance["starts_sha256"]), "starts")
        self._identity(
            proposal_path,
            self._string(starts["proposal_sha256"]),
            "proposal referenced by starts",
        )
        executable = Path(self._string(provenance["executable_path"]))
        self._identity(
            executable,
            self._string(provenance["executable_sha256"]),
            "Wannier90 executable",
        )
        interfaces = [
            self._mapping(value)
            for value in self._array(result["configuration_interfaces"])
        ]
        initial = [
            self._mapping(value) for value in self._array(result["localizations"])
        ]
        continuations = [
            self._mapping(value) for value in self._array(result["continuations"])
        ]
        self._equal(len(interfaces), 14, "interface count")
        self._equal(len(initial), 256, "initial-localization count")
        self._equal(len(continuations), 120, "continuation count")
        self._equal(
            self._integer(result["localization_stage_count"]), 376, "stage count"
        )
        if result["stopped_early"] is not False or result["stop_reason"] is not None:
            raise AssertionError("completed execution retains a stop")
        if any(interface["completed"] is not True for interface in interfaces):
            raise AssertionError("an interface did not complete")
        if any(record["process_completed"] is not True for record in initial):
            raise AssertionError("an initial process did not complete")
        if any(record["process_completed"] is not True for record in continuations):
            raise AssertionError("a continuation process did not complete")
        nonconverged_keys = {
            self._initial_key(record)
            for record in initial
            if record["native_convergence_criterion_satisfied"] is False
        }
        continuation_keys = {self._continuation_key(record) for record in continuations}
        self._equal(len(nonconverged_keys), 120, "initial nonconverged count")
        if continuation_keys != nonconverged_keys:
            raise AssertionError("continuation coverage differs from nonconverged set")
        self._equal(
            sum(
                record["native_convergence_criterion_satisfied"] is True
                for record in initial
            ),
            136,
            "initial converged count",
        )
        self._equal(
            sum(
                record["native_convergence_criterion_satisfied"] is True
                for record in continuations
            ),
            60,
            "continuation converged count",
        )
        old_exceedances = [
            record
            for record in continuations
            if record["resource_limit_exceeded"] is True
        ]
        self._equal(len(old_exceedances), 1, "retained original-limit exceedance")
        if self._continuation_key(old_exceedances[0]) != (
            "fixed_c31_p4_n15",
            "baseline_preconditioned",
            "halton_15",
        ):
            raise AssertionError("unexpected original-limit exceedance identity")
        resume_events = [
            self._mapping(value) for value in self._array(result["resume_events"])
        ]
        self._equal(len(resume_events), 1, "resume-event count")
        resume = resume_events[0]
        self._equal(
            self._integer(resume["pending_continuations_at_start"]),
            115,
            "pending resume count",
        )
        self._equal(self._integer(resume["completed"]), 115, "resumed count")
        if resume["stopped_early"] is not False:
            raise AssertionError("resume did not complete")
        snapshot = Path(self._string(resume["pre_resume_snapshot_path"]))
        self._identity(
            snapshot,
            self._string(resume["pre_resume_snapshot_sha256"]),
            "pre-resume snapshot",
        )
        limits = self._mapping(resume["limits"])
        revised = [
            record
            for record in continuations
            if record.get("execution_authorization_checkpoint")
            == "RM-PERIODIC-2D-STANDALONE-CONTINUATION-RESUME-HC10"
        ]
        self._equal(len(revised), 115, "revised-limit continuation count")
        for record in revised:
            if record["resource_limit_exceeded"] is not False:
                raise AssertionError("a resumed continuation exceeded revised limits")
            stage = self._mapping(record["stage"])
            if self._real(stage["elapsed_seconds"]) > self._integer(
                limits["maximum_seconds_per_stage"]
            ):
                raise AssertionError("continuation exceeded stage time")
            memory = stage["maximum_resident_bytes"]
            if memory is not None and self._integer(memory) > self._integer(
                limits["maximum_resident_bytes_per_stage"]
            ):
                raise AssertionError("continuation exceeded memory")
            if self._integer(record["external_output_bytes"]) > self._integer(
                limits["maximum_external_output_bytes_per_continuation"]
            ):
                raise AssertionError("continuation exceeded output size")
        if self._tree_bytes(execution_path.parent) > self._integer(
            limits["maximum_external_output_bytes_total"]
        ):
            raise AssertionError("external tree exceeds revised total limit")
        for record in interfaces + initial + continuations:
            self._verify_manifest(record)
        expected_interfaces = {
            self._string(self._mapping(value)["configuration_id"])
            for value in self._array(proposal["baseline_configurations"])
        }
        actual_interfaces = {
            self._string(record["configuration_id"]) for record in interfaces
        }
        if actual_interfaces != expected_interfaces:
            raise AssertionError("executed interface set differs from proposal")

    def _verify_manifest(self, record: dict[str, JsonValue]) -> None:
        if "interface_root" in record:
            root = Path(self._string(record["interface_root"]))
        else:
            root = Path(self._string(record["run_root"]))
        for value in self._array(record["file_manifest"]):
            file_record = self._mapping(value)
            path = root / self._string(file_record["path"])
            kind = self._string(file_record["kind"])
            if kind == "symlink":
                if not path.is_symlink():
                    raise AssertionError(f"missing retained symlink {path}")
                if os.readlink(path) != self._string(file_record["link_target"]):
                    raise AssertionError(f"symlink target changed: {path}")
                target = path.resolve(strict=True)
                self._identity(
                    target,
                    self._string(file_record["target_sha256"]),
                    str(target),
                )
            elif kind == "file":
                self._identity(path, self._string(file_record["sha256"]), str(path))
            else:
                raise AssertionError(f"unsupported manifest kind {kind}")

    def _initial_key(self, record: dict[str, JsonValue]) -> tuple[str, str, str]:
        return (
            self._string(record["configuration_id"]),
            self._string(record["arm"]),
            self._string(record["start_id"]),
        )

    def _continuation_key(self, record: dict[str, JsonValue]) -> tuple[str, str, str]:
        return (
            self._string(record["configuration_id"]),
            self._string(record["source_arm"]),
            self._string(record["start_id"]),
        )

    @staticmethod
    def _tree_bytes(root: Path) -> int:
        total = 0
        for path in root.rglob("*"):
            if path.is_symlink():
                total += path.lstat().st_size
            elif path.is_file():
                total += path.stat().st_size
        return total

    @staticmethod
    def _identity(path: Path, expected: str, label: str) -> None:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
            )

    @staticmethod
    def _equal(actual: int, expected: int, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label}: actual={actual}, expected={expected}")

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
    """Adapt retained proposal, starts, and execution paths to verification."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--proposal", type=Path, required=True)
        parser.add_argument("--starts", type=Path, required=True)
        parser.add_argument("--execution-result", type=Path, required=True)
        arguments = parser.parse_args(argv)
        StandaloneExecutionVerifier().execute(
            cast(Path, arguments.proposal).resolve(),
            cast(Path, arguments.starts).resolve(),
            cast(Path, arguments.execution_result).resolve(),
        )
        print("periodic_2d_standalone_external_execution_verification=PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
