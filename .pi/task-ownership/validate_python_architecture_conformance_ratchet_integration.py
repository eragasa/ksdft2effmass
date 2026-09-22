#!/usr/bin/env python3
"""Validate the bounded production-conformance ratchet integration slice.

The retained validator checks exact activation, ownership, implementation evidence,
accepted Phase 2 compatibility, documentation, and deterministic projections. It does
not classify supported routes, repair source, approve inherited findings, close a
Task, establish scientific validity, or activate a successor.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PythonArchitectureRatchetIntegrationCompletionValidator:
    """Validate the operation-scoped Phase 2d implementation boundary."""

    repository_root: Path

    _TASK = "python.architecture-refactor.architecture-conformance.ratchet-integration"
    _CLI_TEST = (
        "python/tests/software_verification/ksdft2effmass/harness/test__harness_cli.py"
    )
    _TEST = (
        "python/tests/software_verification/ksdft2effmass/harness/"
        "test__production_conformance_ratchet.py"
    )
    _TEST_OWNERSHIP = (
        "python/tests/software_verification/ksdft2effmass/harness/resources/"
        "production-conformance-ratchet-test-ownership.json"
    )
    _PROFILE = "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
    _MANUSCRIPT = (
        "docs/publications/research-monograph/appendices/"
        "J-two-dimensional-defect-extraction.tex"
    )
    _OWNED_PATHS = frozenset(
        {
            ".pi/evidence/python-conformance/module-inventory.json",
            ".pi/task-ownership/python.architecture-refactor.architecture-conformance.ratchet-integration.json",
            ".pi/task-ownership/validate_python_architecture_conformance_ratchet_integration.py",
            "docs/architecture/v2/ksdft2effmass/harness/conformance.md",
            "harness/intake/python-architecture-review-refactor.md",
            "harness/state/harness-control.sql",
            "harness/state/harness-control.sqlite3",
            "harness/state/projection-manifest.json",
            "harness/task-graph.json",
            "harness/task-selection.json",
            "python/src/ksdft2effmass/harness/cli/main.py",
            "python/src/ksdft2effmass/harness/cli/validate_production_conformance.py",
            "python/src/ksdft2effmass/harness/pi/conformance/python/ratchet.py",
            "python/tests/software_verification/ksdft2effmass/harness/resources/production-conformance-ratchet-test-ownership.json",
            "python/tests/software_verification/ksdft2effmass/harness/resources/production_conformance_ratchet/baseline-v1.txt",
            "python/tests/software_verification/ksdft2effmass/harness/resources/production_conformance_ratchet/configuration-v1.txt",
            "python/tests/software_verification/ksdft2effmass/harness/resources/production_conformance_ratchet/inherited.py.txt",
            "python/tests/software_verification/ksdft2effmass/harness/resources/production_conformance_ratchet/new.py.txt",
            _CLI_TEST,
            _TEST,
            "tasks/software/python.architecture-refactor.architecture-conformance.json",
            f"tasks/software/{_TASK}.json",
        }
    )

    def execute(self) -> int:
        """Return zero only when every retained bounded check passes."""
        missing = tuple(
            path
            for path in sorted(self._OWNED_PATHS)
            if not (self.repository_root / path).exists()
        )
        if missing:
            print(f"missing required owned paths: {missing}")
            return 1
        if not self._activation_state_is_exact() or not self._changed_scope_is_exact():
            return 1
        interpreter = self.repository_root / "python/.venv/bin/python"
        source = "python/src/ksdft2effmass/harness/pi/conformance/python/ratchet.py"
        cli = "python/src/ksdft2effmass/harness/cli/validate_production_conformance.py"
        validator = (
            ".pi/task-ownership/"
            "validate_python_architecture_conformance_ratchet_integration.py"
        )
        prerequisite_tests = (
            "python/tests/software_verification/ksdft2effmass/harness/test__production_source_facts.py",
            "python/tests/software_verification/ksdft2effmass/harness/test__callable_private_rules.py",
            "python/tests/software_verification/ksdft2effmass/harness/test__dependency_graph_views.py",
            "python/tests/software_verification/ksdft2effmass/harness/test__CodingStandardsConformanceValidator.py",
            "python/tests/software_verification/ksdft2effmass/harness/test__PythonCodingStandardsAdapter.py",
        )
        commands: tuple[tuple[str | Path, ...], ...] = (
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-task-ownership",
                "--repository-root",
                self.repository_root,
                "--task",
                self._TASK,
                "--task-record",
                f"tasks/software/{self._TASK}.json",
                "--ownership-manifest",
                ".pi/task-ownership/python.architecture-refactor.architecture-conformance.ratchet-integration.json",
            ),
            (interpreter, "-m", "pytest", "-q", self._TEST, self._CLI_TEST),
            (interpreter, "-m", "pytest", "-q", *prerequisite_tests),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-python-conformance",
                "--ownership",
                self._TEST_OWNERSHIP,
                "--profile-matrix",
                self._PROFILE,
                self._TEST,
            ),
            (
                interpreter,
                "-m",
                "ruff",
                "format",
                "--check",
                source,
                cli,
                self._TEST,
                self._CLI_TEST,
                validator,
            ),
            (
                interpreter,
                "-m",
                "ruff",
                "check",
                source,
                cli,
                self._TEST,
                self._CLI_TEST,
                validator,
            ),
            (
                interpreter,
                "-m",
                "mypy",
                source,
                cli,
                self._TEST,
                self._CLI_TEST,
                validator,
            ),
        )
        for command in commands:
            if self._run(command) != 0:
                return 1
        with tempfile.TemporaryDirectory(prefix="ratchet-integration-sphinx-") as build:
            if (
                self._run(
                    (
                        interpreter,
                        "-m",
                        "sphinx",
                        "-b",
                        "dummy",
                        "-W",
                        "--keep-going",
                        "docs",
                        build,
                    )
                )
                != 0
            ):
                return 1
        for command in (
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
            ("git", "diff", "--check"),
        ):
            if self._run(command) != 0:
                return 1
        print(
            "PASS: bounded Phase 2d structural software verification is consistent; "
            "inherited findings remain visible and are not approvals or waivers, and "
            "this result establishes no route disposition, repair, Task acceptance, "
            "scientific claim, or successor authority."
        )
        return 0

    def _activation_state_is_exact(self) -> bool:
        """Check selected child, deferred parent, prerequisites, and successors."""
        required: dict[str, tuple[str, ...]] = {
            "harness/task-selection.json": (
                '"active_task_id": null',
                '"explicit_activation_receipt_ids": []',
                '"automatic_successor_activation": false',
            ),
            f"tasks/software/{self._TASK}.json": (
                '"status": "closed_human_accepted_pass"',
                "accept and closeout authorized",
                "human acceptance of the bounded Phase 2d",
            ),
            (
                "tasks/software/"
                "python.architecture-refactor.architecture-conformance.json"
            ): (
                '"status": "deferred_between_children"',
                "all four children are closed",
                "Phases 3-6 remain inactive",
            ),
        }
        for prerequisite in (
            "production-facts",
            "callable-private-rules",
            "dependency-graph-views",
        ):
            required[
                "tasks/software/python.architecture-refactor.architecture-conformance."
                f"{prerequisite}.json"
            ] = ('"status": "closed_human_accepted_pass"',)
        for successor in (
            "python.architecture-refactor.public-import-boundaries",
            "python.architecture-refactor.module-decomposition",
            "python.architecture-refactor.abstraction-design",
            "python.architecture-refactor.aggregate-verification",
        ):
            required[f"tasks/software/{successor}.json"] = ('"status": "inactive"',)
        for path, fragments in required.items():
            text = (self.repository_root / path).read_text(encoding="utf-8")
            for fragment in fragments:
                if fragment not in text:
                    print(f"activation-state mismatch in {path}: {fragment}")
                    return False
        return True

    def _changed_scope_is_exact(self) -> bool:
        """Reject worktree changes outside ownership and the excluded manuscript."""
        completed = subprocess.run(
            ("git", "status", "--porcelain=v1", "-z", "--untracked-files=all"),
            cwd=self.repository_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            return False
        changed: set[str] = set()
        for record in completed.stdout.split("\0"):
            if not record:
                continue
            path = record[3:]
            if " -> " in path:
                path = path.split(" -> ", maxsplit=1)[1]
            changed.add(path)
        unexpected = changed - self._OWNED_PATHS - {self._MANUSCRIPT}
        if unexpected:
            print(
                f"changed paths outside bounded ownership: {tuple(sorted(unexpected))}"
            )
            return False
        return True

    def _run(self, command: tuple[str | Path, ...]) -> int:
        """Execute one declared nonrepairing check."""
        rendered = tuple(str(part) for part in command)
        print("RUN", " ".join(rendered))
        return subprocess.run(
            rendered, cwd=self.repository_root, check=False
        ).returncode


def main() -> int:
    """Adapt script execution to the explicit completion-validator owner."""
    root = Path(__file__).resolve().parents[2]
    return PythonArchitectureRatchetIntegrationCompletionValidator(root).execute()


if __name__ == "__main__":
    sys.exit(main())
