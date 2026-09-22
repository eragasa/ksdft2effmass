#!/usr/bin/env python3
"""Fail-closed completion validator for the current-fact supplement."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from public_import_current_fact_supplement.command import (
    CurrentFactSupplementParser,
)
from public_import_current_fact_supplement.delta_acquisition import (
    AcquisitionManifestSerializer,
)
from public_import_current_fact_supplement.f0_adapter import AcceptedF0Adapter
from python_public_import_current_fact_supplement_model import (
    AcquisitionManifest,
    CurrentFactSupplementCrossViewValidator,
    SelectionSerializer,
    SupplementJsonCodec,
)
from python_public_import_foundation_model import (
    JsonRecord,
    JsonValue,
    PublicImportFoundation,
)


@dataclass(frozen=True, slots=True)
class CurrentFactSupplementCompletionValidator:
    """Own deterministic reproduction and repository completion gates."""

    repository_root: Path

    def execute(self) -> int:
        """Run every no-argument completion gate and fail closed."""
        interpreter = self.repository_root / "python/.venv/bin/python"
        tool = (
            self.repository_root
            / ".pi/task-ownership/generate_python_public_import_current_fact_supplement.py"
        )
        selection = (
            self.repository_root
            / "harness/reports/public-import-boundaries/phase3/current-fact-supplement-selection.tsv"
        )
        manifest = (
            self.repository_root
            / "harness/reports/public-import-boundaries/phase3/current-fact-supplement-inputs.json"
        )
        report = (
            self.repository_root
            / "harness/reports/public-import-boundaries/phase3/current-fact-supplement.json"
        )
        f0 = {
            "harness/reports/public-import-boundaries/phase3/foundation-selection.tsv": "cfefc7338d34bda173350bdc834716b6d48c6eb8306c09c302a7f0645d66f0f1",
            "harness/reports/public-import-boundaries/phase3/foundation-inputs.json": "e2db856169f2224b66fe7728c04765625bd72ecc8ea07a400f7eb062d6e29c01",
            "harness/reports/public-import-boundaries/phase3/foundation.json": "3da51677747741fc0088d2f31f1359e6e8280bd1555ef514409ccfb5879f9e61",
        }
        before = {path: self._sha(self.repository_root / path) for path in f0}
        if before != f0:
            return self._fail("accepted F0 identity mismatch")
        diagnostic = self._validate_permitted_delta()
        if diagnostic is not None:
            return self._fail(diagnostic)
        diagnostic = self._validate_control_state()
        if diagnostic is not None:
            return self._fail(diagnostic)
        try:
            selected = SelectionSerializer().decode(selection.read_bytes())
            if SelectionSerializer().encode(selected) != selection.read_bytes():
                return self._fail("selection TSV is not canonical")
            retained_manifest = AcquisitionManifestSerializer().decode(
                manifest.read_bytes()
            )
            if len(retained_manifest.inputs) != len(selected):
                return self._fail("selection and manifest cardinalities disagree")
            report_payload = report.read_bytes()
            decoded = SupplementJsonCodec().decode(report_payload)
            parsed_report = CurrentFactSupplementParser().decode(report_payload)
            foundation = AcceptedF0Adapter().execute(
                self.repository_root
                / "harness/reports/public-import-boundaries/phase3/foundation.json"
            )
            CurrentFactSupplementCrossViewValidator().execute(
                parsed_report,
                retained_manifest,
                hashlib.sha256(manifest.read_bytes()).hexdigest(),
                foundation,
            )
            if type(decoded) is not dict or decoded.get("summary") != {
                "accepted_zero_lineage_count": 10,
                "added_path_count": 419,
                "current_empty_surface_count": 9,
                "current_route_count": 1456,
                "deleted_path_count": 1,
                "delta_path_count": 565,
                "modified_path_count": 145,
                "package_surface_count": 47,
                "predecessor_route_count": 985,
                "production_module_count": 320,
                "supplemental_candidate_count": 471,
                "zero_boundary_transition_count": 1,
            }:
                return self._fail(
                    "supplement summary disagrees with required derived facts"
                )
            foundation_value = self._record(
                SupplementJsonCodec().decode(
                    (
                        self.repository_root
                        / "harness/reports/public-import-boundaries/phase3/foundation.json"
                    ).read_bytes()
                ),
                "foundation",
            )
            if decoded.get("predecessor_routes") != foundation_value.get(
                "predecessor_routes"
            ):
                return self._fail("encoded predecessor routes differ from accepted F0")
            if decoded.get("predecessor_package_observations") != foundation_value.get(
                "package_surfaces"
            ):
                return self._fail(
                    "encoded predecessor packages differ from accepted F0"
                )
            if decoded.get("accepted_zero_boundary_lineages") != foundation_value.get(
                "zero_route_surfaces"
            ):
                return self._fail("encoded zero lineages differ from accepted F0")
            self._malformed_probes(
                manifest.read_bytes(),
                selection.read_bytes(),
                report_payload,
                retained_manifest,
                foundation,
            )
            self._no_syntax_adjudication_probe(decoded)
        except (OSError, TypeError, ValueError) as exc:
            return self._fail(f"closed artifact validation failed: {exc}")
        with TemporaryDirectory(prefix="current-fact-validation-") as raw:
            temporary = Path(raw)
            outputs: list[bytes] = []
            manifests: list[bytes] = []
            for index in range(2):
                snapshot = temporary / f"snapshot-{index}"
                candidate_manifest = temporary / f"manifest-{index}.json"
                candidate_report = temporary / f"report-{index}.json"
                commands = (
                    (
                        interpreter,
                        tool,
                        "acquire",
                        "--repository-root",
                        self.repository_root,
                        "--selection",
                        selection,
                        "--snapshot-root",
                        snapshot,
                        "--manifest",
                        candidate_manifest,
                    ),
                    (
                        interpreter,
                        tool,
                        "generate",
                        "--repository-root",
                        self.repository_root,
                        "--snapshot-root",
                        snapshot,
                        "--manifest",
                        candidate_manifest,
                        "--output",
                        candidate_report,
                        "--python-executable",
                        interpreter,
                    ),
                )
                for reproduction_command in commands:
                    if self._run(reproduction_command) != 0:
                        return 1
                manifests.append(candidate_manifest.read_bytes())
                candidate_payload = candidate_report.read_bytes()
                candidate_parsed = CurrentFactSupplementParser().decode(
                    candidate_payload
                )
                candidate_manifest_record = AcquisitionManifestSerializer().decode(
                    candidate_manifest.read_bytes()
                )
                CurrentFactSupplementCrossViewValidator().execute(
                    candidate_parsed,
                    candidate_manifest_record,
                    hashlib.sha256(candidate_manifest.read_bytes()).hexdigest(),
                    foundation,
                )
                outputs.append(candidate_payload)
            if manifests[0] != manifests[1] or manifests[0] != manifest.read_bytes():
                return self._fail("isolated acquisition is not byte-identical")
            if outputs[0] != outputs[1] or outputs[0] != report.read_bytes():
                return self._fail("isolated generation is not byte-identical")
            if self._alias_probes(interpreter, tool, selection, temporary) is not None:
                return self._fail("alias probe failed or mutated an input")
        completion_commands: tuple[tuple[str | Path, ...], ...] = (
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-task-ownership",
                "--repository-root",
                self.repository_root,
                "--task",
                "python.architecture-refactor.public-import-boundaries.current-fact-supplement",
                "--task-record",
                self.repository_root
                / "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-supplement.json",
                "--ownership-manifest",
                self.repository_root
                / ".pi/task-ownership/python.architecture-refactor.public-import-boundaries.current-fact-supplement.json",
            ),
            (
                interpreter,
                "-m",
                "ruff",
                "check",
                ".pi/task-ownership/generate_python_public_import_current_fact_supplement.py",
                ".pi/task-ownership/python_public_import_current_fact_supplement_model.py",
                ".pi/task-ownership/public_import_current_fact_supplement",
                ".pi/task-ownership/validate_python_public_import_current_fact_supplement.py",
            ),
            (
                interpreter,
                "-m",
                "ruff",
                "format",
                "--check",
                ".pi/task-ownership/generate_python_public_import_current_fact_supplement.py",
                ".pi/task-ownership/python_public_import_current_fact_supplement_model.py",
                ".pi/task-ownership/public_import_current_fact_supplement",
                ".pi/task-ownership/validate_python_public_import_current_fact_supplement.py",
            ),
            (
                interpreter,
                "-m",
                "mypy",
                "--strict",
                ".pi/task-ownership/generate_python_public_import_current_fact_supplement.py",
                ".pi/task-ownership/python_public_import_current_fact_supplement_model.py",
                ".pi/task-ownership/public_import_current_fact_supplement",
                ".pi/task-ownership/validate_python_public_import_current_fact_supplement.py",
            ),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "harness-projection",
                "--repository-root",
                self.repository_root,
                "check",
            ),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-harness",
                "--repository-root",
                self.repository_root,
            ),
            ("git", "-C", self.repository_root, "diff", "--check"),
        )
        environment = {
            **os.environ,
            "MYPYPATH": f"{self.repository_root / '.pi/task-ownership'}:{self.repository_root / 'python/src'}",
        }
        for command in completion_commands:
            if self._run(command, environment) != 0:
                return 1
        if {path: self._sha(self.repository_root / path) for path in f0} != before:
            return self._fail("validation mutated accepted F0 bytes")
        print("current-fact supplement completion validation passed")
        return 0

    def _validate_permitted_delta(self) -> str | None:
        permitted = {
            ".pi/task-ownership/generate_python_public_import_current_fact_supplement.py",
            ".pi/task-ownership/public_import_current_fact_supplement/__init__.py",
            ".pi/task-ownership/public_import_current_fact_supplement/command.py",
            ".pi/task-ownership/public_import_current_fact_supplement/delta_acquisition.py",
            ".pi/task-ownership/public_import_current_fact_supplement/f0_adapter.py",
            ".pi/task-ownership/public_import_current_fact_supplement/supplement_assembly.py",
            ".pi/task-ownership/python.architecture-refactor.public-import-boundaries.current-fact-supplement.json",
            ".pi/task-ownership/python_public_import_current_fact_supplement_model.py",
            ".pi/task-ownership/validate_python_public_import_current_fact_supplement.py",
            "harness/reports/public-import-boundaries/phase3/current-fact-supplement-inputs.json",
            "harness/reports/public-import-boundaries/phase3/current-fact-supplement-selection.tsv",
            "harness/reports/public-import-boundaries/phase3/current-fact-supplement.json",
            "harness/state/harness-control.sql",
            "harness/state/harness-control.sqlite3",
            "harness/state/projection-manifest.json",
            "harness/task-graph.json",
            "harness/task-selection.json",
            "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-supplement.json",
            "tasks/software/python.architecture-refactor.public-import-boundaries.json",
        }
        completed = subprocess.run(
            (
                "git",
                "-C",
                str(self.repository_root),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ),
            check=False,
            capture_output=True,
            env={"LANG": "C", "LC_ALL": "C", "PATH": os.defpath},
        )
        if completed.returncode != 0:
            return "cannot inspect the permitted working-tree delta"
        try:
            lines = completed.stdout.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            return "working-tree status is not UTF-8"
        observed: set[str] = set()
        for line in lines:
            if len(line) < 4 or line[2] != " ":
                return "working-tree status has an unsupported record"
            status, path = line[:2], line[3:]
            if status[0] not in {" ", "?"}:
                return f"staged path is prohibited: {path}"
            if " -> " in path:
                return f"renamed working-tree path is prohibited: {path}"
            observed.add(path)
        unexpected = sorted(observed - permitted)
        if unexpected:
            return (
                f"working-tree path is outside the ownership manifest: {unexpected[0]}"
            )
        return None

    def _validate_control_state(self) -> str | None:
        try:
            selection = self._record(
                SupplementJsonCodec().decode(
                    (self.repository_root / "harness/task-selection.json").read_bytes()
                ),
                "task selection",
            )
            task = self._record(
                SupplementJsonCodec().decode(
                    (
                        self.repository_root
                        / "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-supplement.json"
                    ).read_bytes()
                ),
                "selected task",
            )
            parent = self._record(
                SupplementJsonCodec().decode(
                    (
                        self.repository_root
                        / "tasks/software/python.architecture-refactor.public-import-boundaries.json"
                    ).read_bytes()
                ),
                "parent task",
            )
        except (OSError, TypeError, ValueError) as exc:
            return f"cannot validate control state: {exc}"
        task_id = (
            "python.architecture-refactor.public-import-boundaries."
            "current-fact-supplement"
        )
        active_task_id = selection.get("active_task_id")
        receipt_ids = selection.get("explicit_activation_receipt_ids")
        task_status = task.get("status")
        if active_task_id == task_id:
            if receipt_ids != [f"human-selection.{task_id}"]:
                return "selected supplement activation receipt is not exact"
            if task_status != "planning":
                return "selected supplement must remain planning"
        elif active_task_id is None:
            if receipt_ids != []:
                return "closed supplement selection receipts must be empty"
            if task_status != "closed_human_accepted_pass":
                return "unselected supplement must be human-accepted and closed"
        else:
            return "task selection names an unsupported task"
        if selection.get("automatic_successor_activation") is not False:
            return "automatic successor activation must remain false"
        if parent.get("status") != "deferred_between_children":
            return "parent must remain deferred between children"
        return None

    @staticmethod
    def _record(value: JsonValue, label: str) -> JsonRecord:
        if type(value) is not dict:
            raise ValueError(f"{label} must be an object")
        return value

    @classmethod
    def _malformed_probes(
        cls,
        manifest: bytes,
        selection: bytes,
        report: bytes,
        retained_manifest: AcquisitionManifest,
        foundation: PublicImportFoundation,
    ) -> None:
        for payload in (
            b'{"x":1,"x":2}\n',
            manifest.replace(b'"Added"', b'"Renamed"', 1),
            manifest.replace(b'"status":"Added"', b'"status":"Deleted"', 1),
            manifest.replace(b'"status":"Deleted"', b'"status":"Modified"', 1),
            manifest + b" ",
        ):
            try:
                AcquisitionManifestSerializer().decode(payload)
            except ValueError:
                pass
            else:
                raise ValueError("malformed manifest probe was accepted")
        try:
            SelectionSerializer().decode(
                selection + selection.splitlines(keepends=True)[1]
            )
        except ValueError:
            pass
        else:
            raise ValueError("duplicate selection path was accepted")
        root = cls._record(SupplementJsonCodec().decode(report), "supplement")
        mutations: list[tuple[str, str | None, JsonRecord]] = []
        unknown: JsonRecord = dict(root)
        unknown["conformance_debt"] = [
            "object.__setattr__",
            "object() negative test",
            "pytest.fixture",
        ]
        mutations.append(("unknown closed field", None, unknown))
        duplicate_route: JsonRecord = dict(root)
        routes = cls._array(root.get("current_routes"), "current_routes")
        duplicate_route["current_routes"] = [*routes, routes[0]]
        mutations.append(("duplicate current route", None, duplicate_route))
        wrong_empty: JsonRecord = dict(root)
        wrong_empty["current_empty_surfaces"] = []
        mutations.append(("inconsistent empty surfaces", None, wrong_empty))
        wrong_manifest: JsonRecord = dict(root)
        wrong_manifest["manifest_sha256"] = "0" * 64
        mutations.append(("wrong manifest identity", None, wrong_manifest))
        mutations.extend(
            (
                (
                    "candidate-route-record mismatch",
                    "supplemental candidate route differs from current route",
                    cls._candidate_route_mismatch(root),
                ),
                (
                    "package-initializer identity mismatch",
                    "package initializer identity differs from selected input",
                    cls._package_initializer_identity_mismatch(root),
                ),
                (
                    "target-source runtime identity mismatch",
                    "runtime target-source identity differs from selected input",
                    cls._runtime_target_identity_mismatch(root),
                ),
            )
        )
        focused_rejections: list[str] = []
        for label, expected_error, mutation in mutations:
            try:
                parsed = CurrentFactSupplementParser().decode(
                    SupplementJsonCodec().encode(mutation)
                )
                CurrentFactSupplementCrossViewValidator().execute(
                    parsed,
                    retained_manifest,
                    hashlib.sha256(manifest).hexdigest(),
                    foundation,
                )
            except ValueError as exc:
                if expected_error is not None:
                    if expected_error not in str(exc):
                        raise ValueError(
                            f"{label} was rejected for the wrong relation: {exc}"
                        ) from exc
                    focused_rejections.append(label)
            else:
                raise ValueError(f"malformed supplement probe was accepted: {label}")
        if len(focused_rejections) != 3:
            raise ValueError("three focused malformed-report probes must be rejected")
        print(
            "focused malformed-report probes rejected: " + "; ".join(focused_rejections)
        )

    @classmethod
    def _candidate_route_mismatch(cls, root: JsonRecord) -> JsonRecord:
        candidates = list(
            cls._array(root.get("supplemental_candidates"), "supplemental_candidates")
        )
        candidate = dict(cls._record(candidates[0], "supplemental_candidate"))
        route = dict(cls._record(candidate.get("route"), "candidate.route"))
        route["direct_origin"] = "synthetic.inconsistent.origin"
        candidate["route"] = route
        candidates[0] = candidate
        mutation: JsonRecord = dict(root)
        mutation["supplemental_candidates"] = candidates
        return mutation

    @classmethod
    def _package_initializer_identity_mismatch(cls, root: JsonRecord) -> JsonRecord:
        surfaces = list(
            cls._array(root.get("current_package_surfaces"), "current_package_surfaces")
        )
        surface = dict(cls._record(surfaces[0], "current_package_surface"))
        surface["initializer_sha256"] = "0" * 64
        surfaces[0] = surface
        mutation: JsonRecord = dict(root)
        mutation["current_package_surfaces"] = surfaces
        return mutation

    @classmethod
    def _runtime_target_identity_mismatch(cls, root: JsonRecord) -> JsonRecord:
        runtimes = list(
            cls._array(root.get("runtime_observations"), "runtime_observations")
        )
        for runtime_index, runtime_value in enumerate(runtimes):
            runtime = dict(cls._record(runtime_value, "runtime_observation"))
            observation = dict(
                cls._record(runtime.get("observation"), "runtime.observation")
            )
            loaded_files = list(
                cls._array(observation.get("loaded_files"), "runtime.loaded_files")
            )
            for loaded_index, loaded_value in enumerate(loaded_files):
                loaded = dict(cls._record(loaded_value, "runtime.loaded_file"))
                path = loaded.get("path")
                if type(path) is str and path.startswith("target-source:"):
                    loaded["sha256"] = "0" * 64
                    loaded_files[loaded_index] = loaded
                    observation["loaded_files"] = loaded_files
                    runtime["observation"] = observation
                    runtimes[runtime_index] = runtime
                    mutation: JsonRecord = dict(root)
                    mutation["runtime_observations"] = runtimes
                    return mutation
        raise ValueError("retained report lacks target-source runtime evidence")

    @staticmethod
    def _no_syntax_adjudication_probe(report: JsonRecord) -> None:
        if "conformance_debt" in report or "syntax_candidates" in report:
            raise ValueError("report must not adjudicate changed syntax")

    def _alias_probes(
        self, interpreter: Path, tool: Path, selection: Path, temporary: Path
    ) -> str | None:
        selection_before = selection.read_bytes()
        tool_before = tool.read_bytes()
        probes = (
            (temporary / "alias-selection", selection),
            (temporary / "alias-tool", tool),
            (
                temporary / "alias-destination",
                temporary / "alias-destination/target/AGENTS.md",
            ),
        )
        for snapshot, output in probes:
            acquisition_alias_command = (
                interpreter,
                tool,
                "acquire",
                "--repository-root",
                self.repository_root,
                "--selection",
                selection,
                "--snapshot-root",
                snapshot,
                "--manifest",
                output,
            )
            if self._run_expect_failure(acquisition_alias_command) is False:
                return "acquire alias was accepted"
        if (
            selection.read_bytes() != selection_before
            or tool.read_bytes() != tool_before
        ):
            return "acquire alias probe mutated a source"
        snapshot = temporary / "alias-generation-snapshot"
        candidate_manifest = temporary / "alias-generation-manifest.json"
        if (
            self._run(
                (
                    interpreter,
                    tool,
                    "acquire",
                    "--repository-root",
                    self.repository_root,
                    "--selection",
                    selection,
                    "--snapshot-root",
                    snapshot,
                    "--manifest",
                    candidate_manifest,
                )
            )
            != 0
        ):
            return "cannot prepare generation alias probe"
        decoded = AcquisitionManifestSerializer().decode(
            candidate_manifest.read_bytes()
        )
        snapshot_paths = tuple(
            item.snapshot_path
            for item in decoded.inputs
            if item.snapshot_path is not None
        )
        if not snapshot_paths:
            return "generation alias probe has no snapshot input"
        snapshot_input = snapshot / snapshot_paths[0].as_posix()
        before = snapshot_input.read_bytes()
        manifest_before = candidate_manifest.read_bytes()
        interpreter_before = interpreter.read_bytes()
        for output in (
            snapshot_input,
            candidate_manifest,
            interpreter,
            selection,
            tool,
        ):
            generation_alias_command = (
                interpreter,
                tool,
                "generate",
                "--repository-root",
                self.repository_root,
                "--snapshot-root",
                snapshot,
                "--manifest",
                candidate_manifest,
                "--output",
                output,
                "--python-executable",
                interpreter,
            )
            if self._run_expect_failure(generation_alias_command) is False:
                return "generation alias was accepted"
        if (
            snapshot_input.read_bytes() != before
            or candidate_manifest.read_bytes() != manifest_before
            or interpreter.read_bytes() != interpreter_before
            or selection.read_bytes() != selection_before
            or tool.read_bytes() != tool_before
        ):
            return "generation alias probe mutated an input"
        return None

    def _run_expect_failure(self, command: tuple[str | Path, ...]) -> bool:
        completed = subprocess.run(
            tuple(str(value) for value in command),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
        )
        return completed.returncode != 0

    @staticmethod
    def _array(value: JsonValue | None, label: str) -> list[JsonValue]:
        if type(value) is not list:
            raise ValueError(f"{label} must be an array")
        return value

    def _run(
        self, command: tuple[str | Path, ...], environment: dict[str, str] | None = None
    ) -> int:
        completed = subprocess.run(
            tuple(str(value) for value in command),
            cwd=self.repository_root,
            env=environment,
            check=False,
        )
        if completed.returncode != 0:
            print(
                f"completion command failed: {' '.join(str(value) for value in command)}",
                file=sys.stderr,
            )
        return completed.returncode

    @staticmethod
    def _sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def _fail(message: str) -> int:
        print(message, file=sys.stderr)
        return 1


def main() -> int:
    """Adapt the no-argument process entry point."""
    if len(sys.argv) != 1:
        print("completion validator takes no arguments", file=sys.stderr)
        return 1
    return CurrentFactSupplementCompletionValidator(
        Path(__file__).resolve().parents[2]
    ).execute()


if __name__ == "__main__":
    raise SystemExit(main())
