#!/usr/bin/env python3
"""Validate the bounded Phase 3 public-import-boundaries planning operation.

This command checks durable planning state and deterministic Harness agreement only.
It does not classify an import route, establish implementation behavior, provide human
acceptance, or authorize activation, commit, or push.
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
        """Return a deterministic diagnostic when required content is absent."""
        artifact = repository_root / self.path
        if not artifact.is_file():
            return f"missing planning artifact: {self.path}"
        text = artifact.read_text(encoding="utf-8")
        for fragment in self.fragments:
            if fragment not in text:
                return f"missing required planning text in {self.path}: {fragment}"
        return None


@dataclass(frozen=True, slots=True)
class PythonPublicImportBoundariesPlanningValidator:
    """Validate Phase 3 planning identities, boundaries, and projections."""

    repository_root: Path

    def execute(self) -> int:
        """Return the first failing deterministic check status, otherwise zero."""
        requirements = self._requirements()
        for requirement in requirements:
            diagnostic = requirement.validate(self.repository_root)
            if diagnostic is not None:
                print(diagnostic)
                return 1

        interpreter = self.repository_root / "python/.venv/bin/python"
        json_paths = tuple(
            requirement.path
            for requirement in requirements
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
        parent = "python.architecture-refactor.public-import-boundaries"
        foundation = f"{parent}.current-fact-foundation"
        return (
            RequiredPlanningText(
                "harness/task-selection.json",
                (
                    f'"active_task_id": "{foundation}"',
                    f'"human-selection.{foundation}"',
                    '"automatic_successor_activation": false',
                ),
            ),
            RequiredPlanningText(
                f"tasks/software/{parent}.json",
                (
                    f'"task_id": "{parent}"',
                    '"status": "deferred_between_children"',
                    "recommendation authorized under an adverserial planning",
                    "34351631-3be1-45b3-9c9b-be6f7db1a369",
                    "independent assumption challenge",
                    "independent integration challenge",
                    "NO_BLOCKING_FINDINGS",
                    "21 route-disposition units",
                    "Only the inactive current-fact-foundation child is recorded now",
                    "does not classify a route",
                    "Automatic successor activation remains false",
                    "responded exactly `recommendation authorized`",
                    "acceptance of the corrected bounded Phase 3 adversarial plan",
                    "implementation activation of only",
                    "F0 is selected with status `planning`",
                    "harness/reports/python-public-import-boundaries-plan.md",
                ),
            ),
            RequiredPlanningText(
                f"tasks/software/{foundation}.json",
                (
                    f'"task_id": "{foundation}"',
                    '"status": "planning"',
                    f'"parent_task_id": "{parent}"',
                    '"python.architecture-refactor.architecture-conformance"',
                    '"explicit_activation_required": true',
                    "exactly 985 unique predecessor route keys",
                    "all 35 package initializers",
                    "all ten zero-route surfaces",
                    "Represent missing or ambiguous support authority as neutral data",
                    "responded exactly `recommendation authorized`",
                    "explicit implementation activation of only this neutral",
                    "F0 is selected with status `planning`",
                    "No disposition-unit recording or activation",
                ),
            ),
            RequiredPlanningText(
                "harness/reports/python-public-import-boundaries-plan.md",
                (
                    "# Phase 3 public-import boundaries: corrected bounded recommendation",
                    "The accepted Phase 1 inventory contains 985 distinct `export_routes`",
                    "### F0 — Current fact foundation",
                    "### D1–D21 — Disposition units",
                    "The 20 nonzero units are disjoint and sum to exactly **985**",
                    "### M1 — File-level mutation partition",
                    "### I* — Conditional implementation children",
                    "### V1 — Aggregate verification",
                    "Support:** `supported`, `unsupported`, or `unresolved`",
                    "Compatibility:** `preserve`, `deprecate`, `alias`, `retire`, or `unresolved`",
                    "**ReviewOutcome: NO_BLOCKING_FINDINGS**",
                    "**OperatorRequest: NONE**",
                ),
            ),
            RequiredPlanningText(
                "harness/reports/python-architecture-inventory.json",
                (
                    '"individual_export_route_decision_input_count": 985',
                    '"package_exports": [',
                    '"support_status": "unknown_no_exact_accepted_support_evidence"',
                    '"compatibility_disposition": "unclassified_pending_bounded_option_b_application"',
                ),
            ),
            RequiredPlanningText(
                "harness/intake/python-architecture-review-refactor.md",
                (
                    "### Phase 3 adversarial planning selection",
                    "> recommendation authorized under an adverserial planning",
                    "#### Phase 3 adversarial planning result",
                    "34351631-3be1-45b3-9c9b-be6f7db1a369",
                    "Both initial\nreviews reported `CHANGES_REQUIRED`",
                    "corrected every evidence-backed\n`MUST_FIX`",
                    "python-public-import-boundaries-plan.md",
                    foundation,
                    "#### Phase 3 plan acceptance and F0 activation",
                    "> recommendation authorized",
                    "acceptance of the corrected bounded Phase 3\nadversarial plan",
                    "F0 is selected with status\n`planning`",
                    "automatic\nsuccessor activation remain inactive",
                    "The Phase 3 response additionally activates only F0",
                    "None authorizes D1–D21",
                ),
            ),
            RequiredPlanningText(
                "tasks/software/python.architecture-refactor.architecture-conformance.json",
                ('"status": "closed_human_accepted_pass"',),
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
        )


def main() -> int:
    """Adapt the command entry point to its explicit validator owner."""
    repository_root = Path(__file__).resolve().parents[2]
    return PythonPublicImportBoundariesPlanningValidator(repository_root).execute()


if __name__ == "__main__":
    sys.exit(main())
