#!/usr/bin/env python3
"""Validate the bounded Phase 2 architecture-conformance planning operation.

This command checks durable planning state and deterministic Harness agreement only.
It verifies the recorded human response but does not independently establish
implementation, test, numerical, scientific, or acceptance evidence.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RequiredPlanningText:
    """Exact text fragments required in one bounded planning artifact."""

    path: str
    fragments: tuple[str, ...]

    def validate(self, repository_root: Path) -> str | None:
        """Return a deterministic diagnostic when the artifact is missing content."""
        artifact = repository_root / self.path
        if not artifact.is_file():
            return f"missing planning artifact: {self.path}"
        text = artifact.read_text(encoding="utf-8")
        for fragment in self.fragments:
            if fragment not in text:
                return f"missing required planning text in {self.path}: {fragment}"
        return None


@dataclass(frozen=True, slots=True)
class PythonArchitectureConformancePlanningValidator:
    """Validate identities, state, boundaries, projections, and whitespace."""

    repository_root: Path

    def execute(self) -> int:
        """Return the first failing deterministic check status, otherwise zero."""
        for requirement in self._requirements():
            diagnostic = requirement.validate(self.repository_root)
            if diagnostic is not None:
                print(diagnostic)
                return 1

        interpreter = self.repository_root / "python/.venv/bin/python"
        json_paths = tuple(
            requirement.path
            for requirement in self._requirements()
            if requirement.path.endswith(".json")
        )
        commands: tuple[tuple[str | Path, ...], ...] = tuple(
            (interpreter, "-m", "json.tool", self.repository_root / path)
            for path in json_paths
        ) + (
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
        for command in commands:
            completed = subprocess.run(command, cwd=self.repository_root, check=False)
            if completed.returncode != 0:
                return completed.returncode
        return 0

    @staticmethod
    def _requirements() -> tuple[RequiredPlanningText, ...]:
        """Return closed planning expectations without ambient task discovery."""
        parent = "python.architecture-refactor.architecture-conformance"
        return (
            RequiredPlanningText(
                "harness/task-selection.json",
                (
                    f'"active_task_id": "{parent}"',
                    f'"human-selection.{parent}"',
                    '"automatic_successor_activation": false',
                ),
            ),
            RequiredPlanningText(
                f"tasks/software/{parent}.json",
                (
                    f'"task_id": "{parent}"',
                    '"status": "planning"',
                    "recommendation authorized",
                    "subsequent exact human response `yes`",
                    (
                        "Do you accept the Phase 2 planning/decomposition result? "
                        "Acceptance will not activate an implementation slice."
                    ),
                    (
                        "normalized as acceptance of this bounded "
                        "planning/decomposition result"
                    ),
                    "Phase 2 remains selected with status `planning`",
                    "does not activate implementation",
                    "authorize staging, commit, or push",
                    (
                        "establish software verification, numerical verification, "
                        "scientific validation, or uncertainty quantification"
                    ),
                    "neutral syntactic export facts",
                    "explicitly supplied accepted route contract",
                    "985 support dispositions remain Phase 3-owned and unclassified",
                    "deterministic enforcement",
                    "deterministic structural observation",
                    "review-only signal",
                    (
                        "semantic ownership of public, scientific, numerical, "
                        "comparison, compatibility, or validation policy is "
                        "review-only absent explicit semantic metadata"
                    ),
                    "python.test-evidence",
                    "sibling subject/profile",
                    "No production implementation is authorized",
                ),
            ),
            *PythonArchitectureConformancePlanningValidator._child_requirements(parent),
            RequiredPlanningText(
                "tasks/software/python.architecture-refactor.json",
                ('"status": "inactive"',),
            ),
            RequiredPlanningText(
                "tasks/software/python.architecture-refactor.inventory-and-policy.json",
                ('"status": "closed_human_accepted_pass"',),
            ),
            RequiredPlanningText(
                "tasks/software/python.architecture-refactor.public-import-boundaries.json",
                ('"status": "inactive"',),
            ),
            RequiredPlanningText(
                "tasks/software/python.architecture-refactor.module-decomposition.json",
                ('"status": "inactive"',),
            ),
            RequiredPlanningText(
                "tasks/software/python.architecture-refactor.abstraction-design.json",
                ('"status": "inactive"',),
            ),
            RequiredPlanningText(
                "tasks/software/python.architecture-refactor.aggregate-verification.json",
                ('"status": "inactive"',),
            ),
            RequiredPlanningText(
                "harness/intake/python-architecture-review-refactor.md",
                (
                    "## Phase 2 planning and decomposition",
                    "> recommendation authorized",
                    "### Phase 2 planning acceptance",
                    (
                        "> Do you accept the Phase 2 planning/decomposition result? "
                        "Acceptance will not activate an implementation slice."
                    ),
                    "> yes",
                    (
                        "normalized as acceptance of the bounded Phase 2\n"
                        "planning/decomposition result"
                    ),
                    "A\nnext child-activation decision remains separate",
                    "production-facts",
                    "callable-private-rules",
                    "dependency-graph-views",
                    "ratchet-integration",
                    (
                        "production source, tests, exports, dependencies, wire "
                        "contracts, or public contracts"
                    ),
                ),
            ),
        )

    @staticmethod
    def _child_requirements(parent: str) -> tuple[RequiredPlanningText, ...]:
        """Return exact inactive child identity and prerequisite expectations."""
        phase_one = "python.architecture-refactor.inventory-and-policy"
        children = (
            ("production-facts", phase_one),
            ("callable-private-rules", f"{parent}.production-facts"),
            ("dependency-graph-views", f"{parent}.production-facts"),
            ("ratchet-integration", f"{parent}.callable-private-rules"),
        )
        requirements: list[RequiredPlanningText] = []
        for suffix, prerequisite in children:
            child = f"{parent}.{suffix}"
            fragments = [
                '"schema_version": 3',
                f'"task_id": "{child}"',
                '"status": "inactive"',
                f'"parent_task_id": "{parent}"',
                f'"{prerequisite}"',
                '"explicit_activation_required": true',
                (
                    "No source, test, export, dependency, wire, or public-contract "
                    "mutation is authorized while this Task is inactive"
                ),
            ]
            if suffix == "ratchet-integration":
                fragments.append(f'"{parent}.dependency-graph-views"')
            requirements.append(
                RequiredPlanningText(f"tasks/software/{child}.json", tuple(fragments))
            )
        return tuple(requirements)


def main() -> int:
    """Adapt the command entry point to its explicit validator owner."""
    repository_root = Path(__file__).resolve().parents[2]
    return PythonArchitectureConformancePlanningValidator(repository_root).execute()


if __name__ == "__main__":
    sys.exit(main())
