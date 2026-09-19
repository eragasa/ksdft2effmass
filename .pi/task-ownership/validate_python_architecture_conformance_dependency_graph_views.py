#!/usr/bin/env python3
"""Validate the bounded dependency-graph-view implementation slice.

This command checks declared state, ownership, source and maintained evidence,
documentation, deterministic projections, and changed-path scope. It never repairs
source and establishes no universal dependency meaning, runtime-cycle conclusion,
numerical verification, scientific validation, uncertainty quantification, human
acceptance, successor authority, or preservation of an excluded pre-existing
manuscript modification.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PythonArchitectureDependencyGraphViewsCompletionValidator:
    """Validate bounded activation, implementation evidence, and projections."""

    repository_root: Path

    _TASK = (
        "python.architecture-refactor.architecture-conformance.dependency-graph-views"
    )
    _TEST = (
        "python/tests/software_verification/ksdft2effmass/harness/"
        "test__dependency_graph_views.py"
    )
    _OWNERSHIP = (
        "python/tests/software_verification/ksdft2effmass/harness/resources/"
        "dependency-graph-views-test-ownership.json"
    )
    _PROFILE = "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
    _MANUSCRIPT = (
        "docs/publications/research-monograph/appendices/"
        "J-two-dimensional-defect-extraction.tex"
    )
    _OWNED_PATHS = frozenset(
        {
            ".pi/evidence/python-conformance/module-inventory.json",
            ".pi/task-ownership/python.architecture-refactor.architecture-conformance.dependency-graph-views.json",
            ".pi/task-ownership/validate_python_architecture_conformance_dependency_graph_views.py",
            "docs/architecture/v2/ksdft2effmass/harness/conformance.md",
            "harness/intake/python-architecture-review-refactor.md",
            "harness/state/harness-control.sql",
            "harness/state/harness-control.sqlite3",
            "harness/state/projection-manifest.json",
            "harness/task-graph.json",
            "harness/task-selection.json",
            "python/src/ksdft2effmass/harness/pi/conformance/python/dependency_graph.py",
            "python/tests/software_verification/ksdft2effmass/harness/resources/dependency-graph-views-test-ownership.json",
            "python/tests/software_verification/ksdft2effmass/harness/resources/dependency_graph_views/pkg/__init__.py.txt",
            "python/tests/software_verification/ksdft2effmass/harness/resources/dependency_graph_views/pkg/alpha.py.txt",
            "python/tests/software_verification/ksdft2effmass/harness/resources/dependency_graph_views/pkg/beta.py.txt",
            "python/tests/software_verification/ksdft2effmass/harness/resources/dependency_graph_views/pkg/conditional.py.txt",
            "python/tests/software_verification/ksdft2effmass/harness/resources/dependency_graph_views/pkg/local.py.txt",
            _TEST,
            f"tasks/software/{_TASK}.json",
            "tasks/software/python.architecture-refactor.architecture-conformance.json",
        }
    )

    def execute(self) -> int:
        """Return zero only when every bounded deterministic check passes."""
        missing = tuple(
            path
            for path in sorted(self._OWNED_PATHS)
            if not (self.repository_root / path).exists()
        )
        if missing:
            print(f"missing required owned paths: {missing}")
            return 1
        if not self._activation_state_is_exact():
            return 1
        if not self._changed_path_scope_is_exact():
            return 1

        interpreter = self.repository_root / "python/.venv/bin/python"
        source = (
            "python/src/ksdft2effmass/harness/pi/conformance/python/dependency_graph.py"
        )
        production_source = (
            "python/src/ksdft2effmass/harness/pi/conformance/python/production.py"
        )
        completion_validator = (
            ".pi/task-ownership/"
            "validate_python_architecture_conformance_dependency_graph_views.py"
        )
        accepted_tests = (
            (
                "python/tests/software_verification/ksdft2effmass/harness/"
                "test__production_source_facts.py"
            ),
            (
                "python/tests/software_verification/ksdft2effmass/harness/"
                "test__callable_private_rules.py"
            ),
            (
                "python/tests/software_verification/ksdft2effmass/harness/"
                "test__CodingStandardsConformanceValidator.py"
            ),
            (
                "python/tests/software_verification/ksdft2effmass/harness/"
                "test__PythonCodingStandardsAdapter.py"
            ),
            (
                "python/tests/software_verification/ksdft2effmass/harness/"
                "test__conformance_records.py"
            ),
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
                (
                    ".pi/task-ownership/"
                    "python.architecture-refactor.architecture-conformance."
                    "dependency-graph-views.json"
                ),
            ),
            (interpreter, "-m", "pytest", "-q", self._TEST),
            (interpreter, "-m", "pytest", "-q", *accepted_tests),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-python-conformance",
                "--ownership",
                self._OWNERSHIP,
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
                self._TEST,
                completion_validator,
            ),
            (
                interpreter,
                "-m",
                "ruff",
                "check",
                source,
                self._TEST,
                completion_validator,
            ),
            (
                interpreter,
                "-m",
                "mypy",
                source,
                production_source,
                self._TEST,
                completion_validator,
            ),
        )
        for command in commands:
            if self._run(command) != 0:
                return 1

        with tempfile.TemporaryDirectory(
            prefix="dependency-graph-views-sphinx-"
        ) as build:
            for builder in ("dummy", "html"):
                command = (
                    interpreter,
                    "-m",
                    "sphinx",
                    "-b",
                    builder,
                    "-W",
                    "--keep-going",
                    "docs",
                    str(Path(build) / builder),
                )
                if self._run(command) != 0:
                    return 1

        final_commands: tuple[tuple[str | Path, ...], ...] = (
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
        )
        for command in final_commands:
            if self._run(command) != 0:
                return 1
        print(
            "PASS: bounded dependency-graph-view structural software-verification "
            "state is consistent; every view remains identified, opposing exact-edge "
            "contracts fail closed, observed check results retain exact edge "
            "provenance, and this validator establishes no "
            "universal graph, runtime-cycle, repair, acceptance, or successor claim."
        )
        return 0

    def _activation_state_is_exact(self) -> bool:
        """Check bounded selected-child and parent/sibling phase state."""
        required = {
            "harness/task-selection.json": (
                '"active_task_id": null',
                '"explicit_activation_receipt_ids": []',
                '"automatic_successor_activation": false',
            ),
            f"tasks/software/{self._TASK}.json": (
                '"status": "closed_human_accepted_pass"',
                "accepted and closeout authorized",
                "human acceptance of the bounded dependency-graph-views",
            ),
            (
                "tasks/software/"
                "python.architecture-refactor.architecture-conformance.json"
            ): (
                '"status": "deferred_between_children"',
                "dependency-graph-views remain closed",
                "ratchet-integration and Phases 3-6 remain inactive",
            ),
            (
                "tasks/software/python.architecture-refactor."
                "architecture-conformance.production-facts.json"
            ): ('"status": "closed_human_accepted_pass"',),
            (
                "tasks/software/python.architecture-refactor."
                "architecture-conformance.callable-private-rules.json"
            ): ('"status": "closed_human_accepted_pass"',),
        }
        inactive = (
            "python.architecture-refactor.architecture-conformance.ratchet-integration",
            "python.architecture-refactor.public-import-boundaries",
            "python.architecture-refactor.module-decomposition",
            "python.architecture-refactor.abstraction-design",
            "python.architecture-refactor.aggregate-verification",
        )
        required.update(
            {
                f"tasks/software/{task}.json": ('"status": "inactive"',)
                for task in inactive
            }
        )
        for path, fragments in required.items():
            text = (self.repository_root / path).read_text(encoding="utf-8")
            for fragment in fragments:
                if fragment not in text:
                    print(f"activation-state mismatch in {path}: {fragment}")
                    return False
        return True

    def _changed_path_scope_is_exact(self) -> bool:
        """Reject paths outside ownership except the excluded manuscript path.

        The manuscript exemption prevents an unrelated pre-existing worktree change
        from blocking this slice. No pre-slice content identity is available here, so
        this scope check deliberately makes no manuscript-preservation claim.
        """
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
        """Execute one declared check without mutating or repairing source."""
        rendered = tuple(str(part) for part in command)
        print("RUN", " ".join(rendered))
        completed = subprocess.run(rendered, cwd=self.repository_root, check=False)
        return completed.returncode


def main() -> int:
    """Adapt the command entry point to its explicit validator owner."""
    repository_root = Path(__file__).resolve().parents[2]
    return PythonArchitectureDependencyGraphViewsCompletionValidator(
        repository_root
    ).execute()


if __name__ == "__main__":
    sys.exit(main())
