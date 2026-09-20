"""Exclusive retained-artifact and attempt-journal operations for Stage C."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import cast

from .authorization import StageCOperationPaths, ValidatedStageCExecution
from .model import JsonValue

STAGE_DIRECTORY = Path(__file__).resolve(strict=True).parent.parent
VERIFIER_PATH = STAGE_DIRECTORY / "verify_stage_c_parent.py"
PLOTTER_PATH = STAGE_DIRECTORY / "plot_stage_c_parent.py"


class AcceptedParentStageCResultSerializer:
    """Serialize one bounded result deterministically and without overwrite."""

    __slots__ = ()

    @staticmethod
    def execute(
        result: dict[str, JsonValue], output: Path, maximum_bytes: int | None = None
    ) -> None:
        provenance = cast(dict[str, JsonValue], result["provenance"])
        observation = cast(dict[str, JsonValue], provenance["execution_observation"])
        encoded = b""
        for _ in range(4):
            encoded = (
                json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
            ).encode("utf-8")
            if observation["output_bytes"] == len(encoded):
                break
            observation["output_bytes"] = len(encoded)
        if observation["output_bytes"] != len(encoded):
            raise RuntimeError("serialized output-byte identity did not stabilize")
        if maximum_bytes is not None and len(encoded) > maximum_bytes:
            raise ValueError("serialized result exceeds the authorized output bound")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())


class ExclusiveRetainedArtifactWriter:
    """Create one retained artifact exclusively and durably."""

    __slots__ = ()

    @staticmethod
    def execute(path: Path, content: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())


class StageCAttemptJournal:
    """Consume one attempt atomically and append its terminal identity."""

    __slots__ = ()

    @staticmethod
    def start(
        path: Path,
        authorization_id: str,
        authorization_sha256: str,
        operation_inventory: tuple[str, ...],
        evidence_status: str,
    ) -> str:
        event: dict[str, JsonValue] = {
            "schema_version": 1,
            "event": "STARTED",
            "authorization_id": authorization_id,
            "authorization_sha256": authorization_sha256,
            "operation_inventory": list(operation_inventory),
            "evidence_status": evidence_status,
        }
        encoded = StageCAttemptJournal._encode(event)
        ExclusiveRetainedArtifactWriter.execute(path, encoded)
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def succeed(
        path: Path,
        started_sha256: str,
        outputs: tuple[tuple[str, Path], ...],
    ) -> None:
        identities: list[JsonValue] = [
            {
                "role": role,
                "path": output.name,
                "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                "bytes": output.stat().st_size,
            }
            for role, output in outputs
        ]
        StageCAttemptJournal._append(
            path,
            {
                "schema_version": 1,
                "event": "TERMINAL",
                "status": "SUCCESS",
                "started_event_sha256": started_sha256,
                "output_identities": identities,
                "error": None,
            },
        )

    @staticmethod
    def fail(path: Path, started_sha256: str, error: BaseException) -> None:
        description = f"{type(error).__name__}: {error}"
        StageCAttemptJournal._append(
            path,
            {
                "schema_version": 1,
                "event": "TERMINAL",
                "status": "FAILURE",
                "started_event_sha256": started_sha256,
                "output_identities": [],
                "error": {
                    "type": type(error).__name__,
                    "message": str(error)[:4096],
                    "sha256": hashlib.sha256(description.encode("utf-8")).hexdigest(),
                },
            },
        )

    @staticmethod
    def _append(path: Path, event: dict[str, JsonValue]) -> None:
        with path.open("ab") as stream:
            stream.write(StageCAttemptJournal._encode(event))
            stream.flush()
            os.fsync(stream.fileno())

    @staticmethod
    def _encode(event: dict[str, JsonValue]) -> bytes:
        return (
            json.dumps(event, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n"
        ).encode("utf-8")


class StageCProtectedOperationFinalizer:
    """Produce verification, visualization, report, manifest, and checksums."""

    __slots__ = ()

    @staticmethod
    def verify_accepted(
        execution: ValidatedStageCExecution, repository_root: Path
    ) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(VERIFIER_PATH),
                "--execution-authorization",
                str(execution.authorization_path),
                "--repository-root",
                str(repository_root),
                "--result",
                str(execution.outputs.result),
            ],
            cwd=repository_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            raise RuntimeError(f"independent verification failed: {process.stderr}")
        ExclusiveRetainedArtifactWriter.execute(
            execution.outputs.verification_log, process.stdout.encode("utf-8")
        )

    @staticmethod
    def verify_authored(
        design: Path, fixture: Path, result: Path, output: Path, root: Path
    ) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(VERIFIER_PATH),
                "--accepted-parent-design",
                str(design),
                "--authored-adapter-fixture",
                str(fixture),
                "--result",
                str(result),
            ],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            raise RuntimeError(
                f"independent authored verification failed: {process.stderr}"
            )
        ExclusiveRetainedArtifactWriter.execute(output, process.stdout.encode("utf-8"))

    @staticmethod
    def plot(result: Path, output: Path, root: Path) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(PLOTTER_PATH),
                "--result",
                str(result),
                "--output",
                str(output),
            ],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            raise RuntimeError(f"summary plotting failed: {process.stderr}")

    @staticmethod
    def report(result: Path, verification: Path, output: Path) -> None:
        payload = cast(JsonValue, json.loads(result.read_text(encoding="utf-8")))
        if not isinstance(payload, dict):
            raise TypeError("retained Stage C result must be an object")
        verification_payload = cast(
            JsonValue, json.loads(verification.read_text(encoding="utf-8"))
        )
        if not isinstance(verification_payload, dict):
            raise TypeError("verification report must be an object")
        accepted = payload.get("accepted_parent_read") is True
        evidence = payload.get("evidence_status")
        summary = payload.get("summary")
        criteria_passed = (
            isinstance(summary, dict) and summary.get("all_criteria_passed") is True
        )
        content = (
            "# Stage C accepted-parent operation report\n\n"
            f"- Accepted-parent read: `{str(accepted).lower()}`\n"
            f"- Evidence status: `{evidence}`\n"
            f"- Runner criteria passed: `{str(criteria_passed).lower()}`\n"
            "- Independent verification: "
            f"`{verification_payload.get('verification')}`\n\n"
            "This compact report does not establish material validation, scientific "
            "validation, uncertainty quantification, publication readiness, or "
            "authority for Stage D.\n"
        )
        ExclusiveRetainedArtifactWriter.execute(output, content.encode("utf-8"))

    @staticmethod
    def manifest(
        result: Path,
        verification: Path,
        svg: Path,
        report: Path,
        output: Path,
        evidence_status: str,
    ) -> None:
        records: list[JsonValue] = [
            {
                "role": role,
                "path": path.name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
            for role, path in (
                ("result", result),
                ("verification_log", verification),
                ("summary_svg", svg),
                ("report", report),
            )
        ]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "manifest_kind": "stage-c-accepted-parent-native-evidence",
            "evidence_status": evidence_status,
            "artifacts": records,
            "dense_matrices_retained": False,
        }
        ExclusiveRetainedArtifactWriter.execute(
            output,
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )

    @staticmethod
    def validate_total_size(outputs: StageCOperationPaths, maximum_bytes: int) -> None:
        retained = tuple(path for _, path in outputs.produced_outputs()) + (
            outputs.checksum_catalog,
            outputs.attempt_record,
        )
        terminal_event_reserve = 64 * 1024
        if (
            sum(path.stat().st_size for path in retained) + terminal_event_reserve
            > maximum_bytes
        ):
            raise ValueError("retained operation package exceeds authorized size")

    @staticmethod
    def checksums(outputs: StageCOperationPaths) -> None:
        lines = [
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
            for _, path in outputs.produced_outputs()
        ]
        ExclusiveRetainedArtifactWriter.execute(
            outputs.checksum_catalog, ("\n".join(lines) + "\n").encode("utf-8")
        )
