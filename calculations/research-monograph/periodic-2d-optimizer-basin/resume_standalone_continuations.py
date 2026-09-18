#!/usr/bin/env python3
"""Resume only pending standalone-study continuations with live progress."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from execute_study import JsonValue


class StandaloneContinuationResumer:
    """Resume retained nonconverged starts without rerunning completed stages."""

    __slots__ = ()

    _maximum_seconds_per_stage = 600
    _maximum_total_seconds = 28_800
    _maximum_resident_bytes_per_stage = 1_073_741_824
    _maximum_bytes_per_continuation = 33_554_432
    _maximum_external_output_bytes_total = 3_221_225_472

    def execute(
        self,
        proposal_path: Path,
        starts_path: Path,
        execution_path: Path,
    ) -> dict[str, JsonValue]:
        started = time.monotonic()
        starts = self._load(starts_path)
        result = self._load(execution_path)
        root = execution_path.parent
        self._verify_inputs(proposal_path, starts_path, starts, result)
        initial = [
            self._mapping(value) for value in self._array(result["localizations"])
        ]
        continuations = [
            self._mapping(value) for value in self._array(result["continuations"])
        ]
        if len(initial) != 256:
            raise AssertionError("resume requires all 256 initial localizations")
        if any(record["process_completed"] is not True for record in initial):
            raise AssertionError("resume requires successful initial processes")
        completed_keys = {
            (
                self._string(record["configuration_id"]),
                self._string(record["source_arm"]),
                self._string(record["start_id"]),
            )
            for record in continuations
        }
        candidates = [
            record
            for record in initial
            if record["native_convergence_criterion_satisfied"] is False
            and self._record_key(record) not in completed_keys
        ]
        if len(candidates) != 115:
            raise AssertionError(
                f"expected 115 pending continuations, found {len(candidates)}"
            )
        snapshot_path = root / "execution-result-before-resume.json"
        if snapshot_path.exists():
            raise FileExistsError(f"pre-resume snapshot exists: {snapshot_path}")
        shutil.copy2(execution_path, snapshot_path)
        snapshot_sha256 = self._sha256(snapshot_path)
        executable = Path(
            self._string(self._mapping(result["provenance"])["executable_path"])
        )
        executable_sha256 = self._string(
            self._mapping(result["provenance"])["executable_sha256"]
        )
        self._identity(executable, executable_sha256, "Wannier90 executable")
        resume_record: dict[str, JsonValue] = {
            "authorization_checkpoint": (
                "RM-PERIODIC-2D-STANDALONE-CONTINUATION-RESUME-HC10"
            ),
            "started_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "driver_path": str(Path(__file__).resolve()),
            "driver_sha256": self._sha256(Path(__file__).resolve()),
            "pre_resume_snapshot_path": str(snapshot_path),
            "pre_resume_snapshot_sha256": snapshot_sha256,
            "initial_localizations_reexecuted": 0,
            "pending_continuations_at_start": len(candidates),
            "limits": {
                "maximum_seconds_per_stage": self._maximum_seconds_per_stage,
                "maximum_total_cumulative_seconds": self._maximum_total_seconds,
                "maximum_resident_bytes_per_stage": (
                    self._maximum_resident_bytes_per_stage
                ),
                "maximum_external_output_bytes_per_continuation": (
                    self._maximum_bytes_per_continuation
                ),
                "maximum_external_output_bytes_total": (
                    self._maximum_external_output_bytes_total
                ),
            },
            "completed": 0,
            "stopped_early": False,
            "stop_reason": None,
        }
        resume_events = self._array(result.setdefault("resume_events", []))
        resume_events.append(resume_record)
        result["stopped_early"] = False
        result["stop_reason"] = None
        self._persist(result, execution_path)
        initial_elapsed = self._real(result["elapsed_seconds"])
        total = len(candidates)
        print(
            "resume_start "
            f"pending={total} existing_continuations={len(continuations)} "
            f"tree_bytes={self._tree_bytes(root)}",
            flush=True,
        )
        for index, record in enumerate(candidates, start=1):
            key = self._record_key(record)
            elapsed_total = initial_elapsed + (time.monotonic() - started)
            if elapsed_total > self._maximum_total_seconds:
                self._stop(
                    result,
                    resume_record,
                    "maximum cumulative execution time exceeded",
                )
                break
            tree_bytes = self._tree_bytes(root)
            if tree_bytes > self._maximum_external_output_bytes_total:
                self._stop(result, resume_record, "maximum total output exceeded")
                break
            print(
                f"[{index}/{total}] start "
                f"configuration={key[0]} arm={key[1]} start={key[2]} "
                f"cumulative_seconds={elapsed_total:.2f} tree_bytes={tree_bytes}",
                flush=True,
            )
            continuation = self._continue(record, executable)
            self._array(result["continuations"]).append(continuation)
            completed = self._integer(resume_record["completed"]) + 1
            resume_record["completed"] = completed
            result["continuation_count"] = len(self._array(result["continuations"]))
            result["localization_stage_count"] = self._integer(
                result["initial_localization_count"]
            ) + self._integer(result["continuation_count"])
            result["external_output_bytes"] = self._tree_bytes(root)
            result["elapsed_seconds"] = initial_elapsed + (time.monotonic() - started)
            self._persist(result, execution_path)
            stage = self._mapping(continuation["stage"])
            print(
                f"[{index}/{total}] done "
                f"exit={stage['exit_code']} "
                "converged="
                f"{continuation['native_convergence_criterion_satisfied']} "
                f"stage_seconds={self._real(stage['elapsed_seconds']):.2f} "
                f"continuation_bytes={continuation['external_output_bytes']} "
                f"tree_bytes={result['external_output_bytes']}",
                flush=True,
            )
            if continuation["resource_limit_exceeded"] is True:
                self._stop(
                    result,
                    resume_record,
                    f"revised resource limit exceeded by {key[0]}/{key[1]}/{key[2]}",
                )
                break
            if continuation["process_completed"] is not True:
                self._stop(
                    result,
                    resume_record,
                    f"continuation process failed for {key[0]}/{key[1]}/{key[2]}",
                )
                break
        resume_record["finished_at_utc"] = (
            datetime.now(UTC).replace(microsecond=0).isoformat()
        )
        resume_record["elapsed_seconds"] = time.monotonic() - started
        result["external_output_bytes"] = self._tree_bytes(root)
        result["elapsed_seconds"] = initial_elapsed + (time.monotonic() - started)
        result["continuation_count"] = len(self._array(result["continuations"]))
        result["localization_stage_count"] = self._integer(
            result["initial_localization_count"]
        ) + self._integer(result["continuation_count"])
        if self._integer(resume_record["completed"]) == total:
            result["stopped_early"] = False
            result["stop_reason"] = None
            resume_record["stopped_early"] = False
            resume_record["stop_reason"] = None
        self._persist(result, execution_path)
        print(
            "resume_finish "
            f"completed={resume_record['completed']}/{total} "
            f"stopped_early={resume_record['stopped_early']} "
            f"elapsed_seconds={resume_record['elapsed_seconds']:.2f} "
            f"tree_bytes={result['external_output_bytes']}",
            flush=True,
        )
        return result

    def _continue(
        self, source_record: dict[str, JsonValue], executable: Path
    ) -> dict[str, JsonValue]:
        configuration = self._string(source_record["configuration_id"])
        arm = self._string(source_record["arm"])
        start = self._string(source_record["start_id"])
        initial_root = Path(self._string(source_record["run_root"]))
        source_seed = initial_root / "low_triple"
        run_root = initial_root / "continuation"
        if run_root.exists():
            raise FileExistsError(f"unexpected continuation directory: {run_root}")
        seed_root = run_root / "low_triple"
        seed_root.mkdir(parents=True)
        for name in (
            "low_triple.eig",
            "low_triple.mmn",
            "low_triple.nnkp",
            "low_triple.amn",
        ):
            self._relative_symlink(source_seed / name, seed_root / name)
        source_checkpoint = source_seed / "low_triple.chk"
        if not source_checkpoint.is_file():
            raise FileNotFoundError(f"missing checkpoint: {source_checkpoint}")
        shutil.copy2(source_checkpoint, seed_root / "low_triple.chk")
        source_checkpoint_sha256 = self._sha256(source_checkpoint)
        copied_checkpoint_sha256 = self._sha256(seed_root / "low_triple.chk")
        if source_checkpoint_sha256 != copied_checkpoint_sha256:
            raise AssertionError("continuation checkpoint copy changed identity")
        win_text = (source_seed / "low_triple.win").read_text(encoding="utf-8")
        if "num_iter = 5000" not in win_text:
            raise AssertionError(
                "source WIN does not have frozen initial iteration cap"
            )
        win_text = win_text.replace("num_iter = 5000", "num_iter = 15000")
        win_text = win_text.replace(
            "write_hr = true", "restart = wannierise\nwrite_hr = true"
        )
        (seed_root / "low_triple.win").write_text(win_text, encoding="utf-8")
        stage = self._run_timed(executable, seed_root)
        convergence, iterations = self._convergence(seed_root / "low_triple.wout")
        output_bytes = self._tree_bytes(run_root)
        exceeded = (
            self._stage_exceeds(stage)
            or output_bytes > self._maximum_bytes_per_continuation
        )
        return {
            "configuration_id": configuration,
            "source_arm": arm,
            "start_id": start,
            "source_run_root": str(initial_root),
            "source_checkpoint_sha256": source_checkpoint_sha256,
            "continuation_checkpoint_initial_sha256": copied_checkpoint_sha256,
            "stage": stage,
            "process_completed": self._passed(stage),
            "native_convergence_criterion_satisfied": convergence,
            "continuation_iterations": iterations,
            "resource_limit_exceeded": exceeded,
            "external_output_bytes": output_bytes,
            "run_root": str(run_root),
            "file_manifest": self._files(run_root),
            "execution_authorization_checkpoint": (
                "RM-PERIODIC-2D-STANDALONE-CONTINUATION-RESUME-HC10"
            ),
        }

    def _run_timed(self, executable: Path, seed_root: Path) -> dict[str, JsonValue]:
        stdout_path = seed_root / "continuation.stdout"
        stderr_path = seed_root / "continuation.stderr"
        time_path = seed_root / "continuation.time"
        command = (str(executable), "low_triple")
        wrapped = ("/usr/bin/time", "-l", "-o", str(time_path), *command)
        started = time.monotonic()
        try:
            with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
                completed = subprocess.run(
                    wrapped,
                    cwd=seed_root,
                    stdout=stdout,
                    stderr=stderr,
                    check=False,
                    timeout=self._maximum_seconds_per_stage,
                )
            exit_code = completed.returncode
            timed_out = False
        except subprocess.TimeoutExpired:
            exit_code = 124
            timed_out = True
        stage: dict[str, JsonValue] = {
            "stage": "continuation",
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
                stage["maximum_resident_bytes"] = int(memory.group(1))
            if elapsed is not None:
                stage["elapsed_seconds"] = float(elapsed.group(1))
        return stage

    def _stage_exceeds(self, stage: dict[str, JsonValue]) -> bool:
        memory = stage["maximum_resident_bytes"]
        return self._real(
            stage["elapsed_seconds"]
        ) > self._maximum_seconds_per_stage or (
            memory is not None
            and self._integer(memory) > self._maximum_resident_bytes_per_stage
        )

    @staticmethod
    def _passed(stage: dict[str, JsonValue]) -> bool:
        code = stage["exit_code"]
        return isinstance(code, int) and not isinstance(code, bool) and code == 0

    @staticmethod
    def _convergence(path: Path) -> tuple[bool, int | None]:
        if not path.is_file():
            return False, None
        text = path.read_text(encoding="utf-8")
        iterations = re.findall(r"^\s+(\d+)\s+.*<-- CONV$", text, re.MULTILINE)
        return (
            "Wannierisation convergence criteria satisfied" in text,
            int(iterations[-1]) if iterations else None,
        )

    def _verify_inputs(
        self,
        proposal_path: Path,
        starts_path: Path,
        starts: dict[str, JsonValue],
        result: dict[str, JsonValue],
    ) -> None:
        expected_proposal = self._string(
            self._mapping(result["provenance"])["proposal_sha256"]
        )
        expected_starts = self._string(
            self._mapping(result["provenance"])["starts_sha256"]
        )
        self._identity(proposal_path, expected_proposal, "proposal")
        self._identity(starts_path, expected_starts, "start table")
        self._identity(
            proposal_path,
            self._string(starts["proposal_sha256"]),
            "proposal referenced by start table",
        )
        if result["stopped_early"] is not True:
            raise AssertionError("resume input is not a retained stopped execution")

    def _record_key(self, record: dict[str, JsonValue]) -> tuple[str, str, str]:
        return (
            self._string(record["configuration_id"]),
            self._string(record["arm"]),
            self._string(record["start_id"]),
        )

    @staticmethod
    def _stop(
        result: dict[str, JsonValue],
        resume_record: dict[str, JsonValue],
        reason: str,
    ) -> None:
        result["stopped_early"] = True
        result["stop_reason"] = reason
        resume_record["stopped_early"] = True
        resume_record["stop_reason"] = reason

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

    @staticmethod
    def _persist(result: dict[str, JsonValue], path: Path) -> None:
        path.write_text(
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


class CommandAdapter:
    """Adapt retained execution paths to the bounded continuation resumer."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--proposal", type=Path, required=True)
        parser.add_argument("--starts", type=Path, required=True)
        parser.add_argument("--execution-result", type=Path, required=True)
        arguments = parser.parse_args(argv)
        result = StandaloneContinuationResumer().execute(
            cast(Path, arguments.proposal).resolve(),
            cast(Path, arguments.starts).resolve(),
            cast(Path, arguments.execution_result).resolve(),
        )
        print(
            json.dumps(
                {
                    "continuation_count": result["continuation_count"],
                    "localization_stage_count": result["localization_stage_count"],
                    "elapsed_seconds": result["elapsed_seconds"],
                    "external_output_bytes": result["external_output_bytes"],
                    "stopped_early": result["stopped_early"],
                    "stop_reason": result["stop_reason"],
                },
                indent=2,
                sort_keys=True,
            ),
            flush=True,
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
