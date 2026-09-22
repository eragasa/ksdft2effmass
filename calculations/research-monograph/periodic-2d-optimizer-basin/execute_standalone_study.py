#!/usr/bin/env python3
"""Execute the exact bounded standalone optimizer-convergence study."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from execute_study import InitialGaugeAction, JsonValue


class StandaloneStudyExecutor:
    """Prepare every interface, then run baseline, control, and continuations."""

    __slots__ = ("_started",)

    def __init__(self) -> None:
        self._started = 0.0

    def execute(
        self,
        proposal_path: Path,
        starts_path: Path,
        preparer_path: Path,
        output_root: Path,
    ) -> dict[str, JsonValue]:
        proposal = self._load(proposal_path)
        starts_payload = self._load(starts_path)
        if proposal["evidence_status"] != "proposed work; not authorized for execution":
            raise ValueError("unexpected proposal status")
        self._identity(
            proposal_path,
            self._string(starts_payload["proposal_sha256"]),
            "proposal",
        )
        starts = [
            self._mapping(value) for value in self._array(starts_payload["starts"])
        ]
        configurations = [
            self._mapping(value)
            for value in self._array(proposal["baseline_configurations"])
        ]
        limits = self._mapping(proposal["execution_limits_proposed"])
        counts = self._mapping(proposal["maximum_execution_counts"])
        control_ids = set(
            self._strings(
                self._mapping(proposal["optimizer_protocol"])["control_configurations"]
            )
        )
        self._validate_counts(configurations, starts, control_ids, counts)
        executable_record = self._mapping(proposal["executable"])
        executable = Path(self._string(executable_record["path"])).resolve()
        self._identity(
            executable,
            self._string(executable_record["sha256"]),
            "Wannier90 executable",
        )
        repository_root = proposal_path.parents[3]
        parent_input_path = repository_root / self._string(proposal["parent_contract"])
        gauge_transform_path = Path(__file__).resolve().with_name("execute_study.py")
        output_root.mkdir(parents=True, exist_ok=False)
        self._started = time.monotonic()
        result: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": self._string(proposal["proposal_id"]),
            "evidence_status": "calculated bounded synthetic non-DFT execution",
            "authorization_checkpoint": ("RM-PERIODIC-2D-STANDALONE-EXECUTION-HC09"),
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "provenance": {
                "proposal_path": str(proposal_path),
                "proposal_sha256": self._sha256(proposal_path),
                "starts_path": str(starts_path),
                "starts_sha256": self._sha256(starts_path),
                "parent_input_path": str(parent_input_path),
                "parent_input_sha256": self._sha256(parent_input_path),
                "preparer_path": str(preparer_path),
                "preparer_sha256": self._sha256(preparer_path),
                "driver_path": str(Path(__file__).resolve()),
                "driver_sha256": self._sha256(Path(__file__).resolve()),
                "gauge_transform_path": str(gauge_transform_path),
                "gauge_transform_sha256": self._sha256(gauge_transform_path),
                "executable_path": str(executable),
                "executable_sha256": self._sha256(executable),
                "python_version": platform.python_version(),
                "external_output_root": str(output_root),
            },
            "limits": limits,
            "configuration_interfaces": [],
            "localizations": [],
            "continuations": [],
            "stopped_early": False,
            "stop_reason": None,
        }
        timeout = self._integer(limits["maximum_seconds_per_stage"])
        interface_records: dict[str, dict[str, JsonValue]] = {}
        for configuration in configurations:
            if self._limit_reached(output_root, limits, result):
                break
            interface = self._prepare_interface(
                configuration,
                parent_input_path,
                preparer_path,
                executable,
                output_root,
                timeout,
                limits,
            )
            self._array(result["configuration_interfaces"]).append(interface)
            identifier = self._string(configuration["configuration_id"])
            interface_records[identifier] = interface
            self._persist(result, output_root)
            if interface["completed"] is not True:
                result["stopped_early"] = True
                result["stop_reason"] = (
                    f"interface preparation failed for {identifier}; "
                    "no localization started"
                )
                break
        if result["stopped_early"] is False:
            continuation_candidates: list[
                tuple[
                    dict[str, JsonValue],
                    str,
                    dict[str, JsonValue],
                    Path,
                ]
            ] = []
            for configuration in configurations:
                if self._limit_reached(output_root, limits, result):
                    break
                identifier = self._string(configuration["configuration_id"])
                interface = interface_records[identifier]
                for start in starts:
                    if self._limit_reached(output_root, limits, result):
                        break
                    record, run_root = self._localize(
                        configuration,
                        start,
                        "baseline_preconditioned",
                        True,
                        interface,
                        executable,
                        output_root,
                        timeout,
                        limits,
                    )
                    self._array(result["localizations"]).append(record)
                    if self._continuation_required(record, run_root):
                        continuation_candidates.append(
                            (configuration, "baseline_preconditioned", start, run_root)
                        )
                    self._persist(result, output_root)
            for configuration in configurations:
                identifier = self._string(configuration["configuration_id"])
                if identifier not in control_ids:
                    continue
                interface = interface_records[identifier]
                for start in starts:
                    if self._limit_reached(output_root, limits, result):
                        break
                    record, run_root = self._localize(
                        configuration,
                        start,
                        "control_preconditioner_off",
                        False,
                        interface,
                        executable,
                        output_root,
                        timeout,
                        limits,
                    )
                    self._array(result["localizations"]).append(record)
                    if self._continuation_required(record, run_root):
                        continuation_candidates.append(
                            (
                                configuration,
                                "control_preconditioner_off",
                                start,
                                run_root,
                            )
                        )
                    self._persist(result, output_root)
            for configuration, arm, start, run_root in continuation_candidates:
                if self._limit_reached(output_root, limits, result):
                    break
                continuation = self._continue(
                    configuration,
                    arm,
                    start,
                    run_root,
                    executable,
                    output_root,
                    timeout,
                    limits,
                )
                self._array(result["continuations"]).append(continuation)
                self._persist(result, output_root)
        self._limit_reached(output_root, limits, result)
        result["elapsed_seconds"] = time.monotonic() - self._started
        result["external_output_bytes"] = self._tree_bytes(output_root)
        result["interface_count"] = len(self._array(result["configuration_interfaces"]))
        result["initial_localization_count"] = len(self._array(result["localizations"]))
        result["continuation_count"] = len(self._array(result["continuations"]))
        result["localization_stage_count"] = self._integer(
            result["initial_localization_count"]
        ) + self._integer(result["continuation_count"])
        self._persist(result, output_root)
        return result

    def _prepare_interface(
        self,
        configuration: dict[str, JsonValue],
        parent_input_path: Path,
        preparer_path: Path,
        executable: Path,
        output_root: Path,
        timeout: int,
        limits: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        identifier = self._string(configuration["configuration_id"])
        root = output_root / identifier
        interface_root = root / "interface"
        interface_root.mkdir(parents=True)
        parent = self._load(parent_input_path)
        parent["plane_wave_cutoff"] = self._integer(configuration["plane_wave_cutoff"])
        parent["reciprocal_mesh_size"] = self._integer(
            configuration["reciprocal_mesh_size"]
        )
        input_path = root / "composite-input.json"
        input_path.write_text(
            json.dumps(parent, indent=2, sort_keys=True) + "\n", encoding="utf-8"
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
                    str(interface_root),
                    "--stage",
                    "initial",
                    "--transverse-length",
                    f"{transverse:.16g}",
                ),
                interface_root,
                "prepare-initial",
                timeout,
            )
        )
        seed_root = interface_root / "low_triple"
        if self._passed(stages[-1]):
            stages.append(
                self._run_timed(
                    (str(executable), "-pp", "low_triple"),
                    seed_root,
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
                        str(interface_root),
                        "--stage",
                        "interface",
                        "--transverse-length",
                        f"{transverse:.16g}",
                    ),
                    interface_root,
                    "prepare-interface",
                    timeout,
                )
            )
        completed = all(self._passed(value) for value in stages)
        exceeded = self._stages_exceed(stages, limits)
        return {
            "configuration_id": identifier,
            "axes": configuration["axes"],
            "plane_wave_cutoff": configuration["plane_wave_cutoff"],
            "reciprocal_mesh_size": configuration["reciprocal_mesh_size"],
            "transverse_lattice_length": transverse,
            "input_path": str(input_path),
            "input_sha256": self._sha256(input_path),
            "interface_root": str(interface_root),
            "stages": stages,
            "completed": completed and not exceeded,
            "resource_limit_exceeded": exceeded,
            "file_manifest": self._files(interface_root),
        }

    def _localize(
        self,
        configuration: dict[str, JsonValue],
        start: dict[str, JsonValue],
        arm: str,
        preconditioner: bool,
        interface: dict[str, JsonValue],
        executable: Path,
        output_root: Path,
        timeout: int,
        limits: dict[str, JsonValue],
    ) -> tuple[dict[str, JsonValue], Path]:
        identifier = self._string(configuration["configuration_id"])
        start_id = self._string(start["start_id"])
        run_root = output_root / identifier / arm / start_id
        seed_root = run_root / "low_triple"
        seed_root.mkdir(parents=True)
        interface_seed = Path(self._string(interface["interface_root"])) / "low_triple"
        for name in ("low_triple.eig", "low_triple.mmn", "low_triple.nnkp"):
            self._relative_symlink(interface_seed / name, seed_root / name)
        win_text = (interface_seed / "low_triple.win").read_text(encoding="utf-8")
        win_text = win_text.replace(
            "precond = true", f"precond = {'true' if preconditioner else 'false'}"
        )
        (seed_root / "low_triple.win").write_text(win_text, encoding="utf-8")
        gauge = {
            "gauge_id": start_id,
            "ordered_generator_terms": start["ordered_terms"],
        }
        invariant = InitialGaugeAction().execute(
            interface_seed / "low_triple.amn",
            seed_root / "low_triple.amn",
            self._integer(configuration["reciprocal_mesh_size"]),
            gauge,
        )
        stage = self._run_timed(
            (str(executable), "low_triple"),
            seed_root,
            "localization",
            timeout,
        )
        output_bytes = self._tree_bytes(run_root)
        exceeded = self._stage_exceeds(stage, limits) or output_bytes > self._integer(
            limits["maximum_external_output_bytes_per_localization"]
        )
        convergence = self._convergence(seed_root / "low_triple.wout")
        record: dict[str, JsonValue] = {
            "configuration_id": identifier,
            "arm": arm,
            "preconditioner": preconditioner,
            "start_id": start_id,
            "gauge_invariants": invariant,
            "stage": stage,
            "process_completed": self._passed(stage),
            "native_convergence_criterion_satisfied": convergence[0],
            "iterations": convergence[1],
            "resource_limit_exceeded": exceeded,
            "external_output_bytes": output_bytes,
            "run_root": str(run_root),
            "file_manifest": self._files(run_root),
        }
        if exceeded:
            record["stop_required"] = True
        return record, run_root

    def _continue(
        self,
        configuration: dict[str, JsonValue],
        arm: str,
        start: dict[str, JsonValue],
        initial_root: Path,
        executable: Path,
        output_root: Path,
        timeout: int,
        limits: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        identifier = self._string(configuration["configuration_id"])
        start_id = self._string(start["start_id"])
        source_seed = initial_root / "low_triple"
        run_root = initial_root / "continuation"
        seed_root = run_root / "low_triple"
        seed_root.mkdir(parents=True)
        for name in (
            "low_triple.eig",
            "low_triple.mmn",
            "low_triple.nnkp",
            "low_triple.amn",
        ):
            self._relative_symlink(source_seed / name, seed_root / name)
        shutil.copy2(source_seed / "low_triple.chk", seed_root / "low_triple.chk")
        win_text = (source_seed / "low_triple.win").read_text(encoding="utf-8")
        win_text = win_text.replace("num_iter = 5000", "num_iter = 15000")
        win_text = win_text.replace(
            "write_hr = true", "restart = wannierise\nwrite_hr = true"
        )
        (seed_root / "low_triple.win").write_text(win_text, encoding="utf-8")
        source_checkpoint_sha256 = self._sha256(source_seed / "low_triple.chk")
        copied_checkpoint_sha256 = self._sha256(seed_root / "low_triple.chk")
        if source_checkpoint_sha256 != copied_checkpoint_sha256:
            raise AssertionError("continuation checkpoint copy changed identity")
        stage = self._run_timed(
            (str(executable), "low_triple"),
            seed_root,
            "continuation",
            timeout,
        )
        output_bytes = self._tree_bytes(run_root)
        exceeded = self._stage_exceeds(stage, limits) or output_bytes > self._integer(
            limits["maximum_external_output_bytes_per_localization"]
        )
        convergence = self._convergence(seed_root / "low_triple.wout")
        return {
            "configuration_id": identifier,
            "source_arm": arm,
            "start_id": start_id,
            "source_run_root": str(initial_root),
            "source_checkpoint_sha256": source_checkpoint_sha256,
            "continuation_checkpoint_initial_sha256": copied_checkpoint_sha256,
            "stage": stage,
            "process_completed": self._passed(stage),
            "native_convergence_criterion_satisfied": convergence[0],
            "continuation_iterations": convergence[1],
            "resource_limit_exceeded": exceeded,
            "external_output_bytes": output_bytes,
            "run_root": str(run_root),
            "file_manifest": self._files(run_root),
        }

    def _continuation_required(
        self, record: dict[str, JsonValue], run_root: Path
    ) -> bool:
        return (
            record["process_completed"] is True
            and record["native_convergence_criterion_satisfied"] is False
            and (run_root / "low_triple" / "low_triple.chk").is_file()
        )

    def _convergence(self, path: Path) -> tuple[bool, int | None]:
        if not path.is_file():
            return False, None
        text = path.read_text(encoding="utf-8")
        iterations = re.findall(r"^\s+(\d+)\s+.*<-- CONV$", text, re.MULTILINE)
        return (
            "Wannierisation convergence criteria satisfied" in text,
            int(iterations[-1]) if iterations else None,
        )

    def _limit_reached(
        self,
        output_root: Path,
        limits: dict[str, JsonValue],
        result: dict[str, JsonValue],
    ) -> bool:
        if result["stopped_early"] is True:
            return True
        if time.monotonic() - self._started > self._integer(
            limits["maximum_total_seconds"]
        ):
            result["stopped_early"] = True
            result["stop_reason"] = "maximum total execution time exceeded"
            return True
        if self._tree_bytes(output_root) > self._integer(
            limits["maximum_external_output_bytes_total"]
        ):
            result["stopped_early"] = True
            result["stop_reason"] = "maximum total external output exceeded"
            return True
        for record_value in self._array(result["localizations"]) + self._array(
            result["continuations"]
        ):
            record = self._mapping(record_value)
            if record["resource_limit_exceeded"] is True:
                result["stopped_early"] = True
                result["stop_reason"] = (
                    "per-localization resource limit exceeded by "
                    f"{record['configuration_id']}/{record['start_id']}"
                )
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

    def _stages_exceed(
        self, stages: list[JsonValue], limits: dict[str, JsonValue]
    ) -> bool:
        return any(
            self._stage_exceeds(self._mapping(value), limits) for value in stages
        )

    def _stage_exceeds(
        self, stage: dict[str, JsonValue], limits: dict[str, JsonValue]
    ) -> bool:
        memory = stage["maximum_resident_bytes"]
        return self._real(stage["elapsed_seconds"]) > self._integer(
            limits["maximum_seconds_per_stage"]
        ) or (
            memory is not None
            and self._integer(memory)
            > self._integer(limits["maximum_resident_bytes_per_stage"])
        )

    @staticmethod
    def _passed(value: JsonValue) -> bool:
        if not isinstance(value, dict):
            raise TypeError("stage must be an object")
        code = value["exit_code"]
        return isinstance(code, int) and not isinstance(code, bool) and code == 0

    def _validate_counts(
        self,
        configurations: list[dict[str, JsonValue]],
        starts: list[dict[str, JsonValue]],
        control_ids: set[str],
        counts: dict[str, JsonValue],
    ) -> None:
        if len(configurations) != self._integer(counts["unique_interfaces"]):
            raise ValueError("interface count disagrees with proposal")
        if len(starts) != 16:
            raise ValueError("start count must equal 16")
        baseline = len(configurations) * len(starts)
        controls = len(control_ids) * len(starts)
        identifiers = {
            self._string(configuration["configuration_id"])
            for configuration in configurations
        }
        if not control_ids <= identifiers:
            raise ValueError("optimizer-control identity is not an interface")
        if baseline != self._integer(counts["baseline_localizations"]):
            raise ValueError("baseline localization count disagrees")
        if controls != self._integer(counts["optimizer_control_localizations"]):
            raise ValueError("optimizer-control count disagrees")
        if baseline + controls != self._integer(
            counts["maximum_conditional_continuations"]
        ):
            raise ValueError("maximum continuation count disagrees")
        if 2 * (baseline + controls) != self._integer(
            counts["maximum_localization_stages"]
        ):
            raise ValueError("maximum localization-stage count disagrees")

    @staticmethod
    def _relative_symlink(source: Path, target: Path) -> None:
        target.symlink_to(os.path.relpath(source, target.parent))

    def _files(self, root: Path) -> list[JsonValue]:
        records: list[JsonValue] = []
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                resolved = path.resolve(strict=True)
                records.append(
                    {
                        "path": path.relative_to(root).as_posix(),
                        "kind": "symlink",
                        "link_target": os.readlink(path),
                        "target_bytes": resolved.stat().st_size,
                        "target_sha256": self._sha256(resolved),
                    }
                )
            elif path.is_file():
                records.append(
                    {
                        "path": path.relative_to(root).as_posix(),
                        "kind": "file",
                        "bytes": path.stat().st_size,
                        "sha256": self._sha256(path),
                    }
                )
        return records

    @staticmethod
    def _tree_bytes(root: Path) -> int:
        total = 0
        for path in root.rglob("*"):
            if path.is_symlink():
                total += path.lstat().st_size
            elif path.is_file():
                total += path.stat().st_size
        return total

    def _persist(self, result: dict[str, JsonValue], output_root: Path) -> None:
        (output_root / "execution-result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

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

    def _strings(self, value: JsonValue) -> tuple[str, ...]:
        return tuple(self._string(item) for item in self._array(value))


class CommandAdapter:
    """Adapt exact proposal and output paths to the bounded executor."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--proposal", type=Path, required=True)
        parser.add_argument("--starts", type=Path, required=True)
        parser.add_argument("--preparer", type=Path, required=True)
        parser.add_argument("--output-root", type=Path, required=True)
        arguments = parser.parse_args(argv)
        result = StandaloneStudyExecutor().execute(
            cast(Path, arguments.proposal).resolve(),
            cast(Path, arguments.starts).resolve(),
            cast(Path, arguments.preparer).resolve(),
            cast(Path, arguments.output_root).resolve(),
        )
        print(
            json.dumps(
                {
                    "interface_count": result["interface_count"],
                    "initial_localization_count": result["initial_localization_count"],
                    "continuation_count": result["continuation_count"],
                    "localization_stage_count": result["localization_stage_count"],
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
