"""Shared synthetic constructor for retained HarnessTask verification.

This helper module owns no evidence identifier or independent acceptance claim.
"""

from __future__ import annotations

from ksdft2effmass.harness import HarnessTask


def make_task(**changes: object) -> HarnessTask:
    """Construct one valid synthetic Task with explicit overrides."""
    values: dict[str, object] = {
        "schema_version": 3,
        "task_id": "example.task",
        "title": "Example Task",
        "status": "proposed",
        "status_detail": None,
        "parent_task_id": None,
        "task_prerequisite_ids": (),
        "external_prerequisite_ids": (),
        "superseded_by_task_ids": (),
        "explicit_activation_required": True,
        "objective": "Verify the accepted software contract.",
        "authority_reference_paths": ("records/decision.md",),
        "authorized_scope": ("Use synthetic test data.",),
        "completion_criteria": ("Exact checks pass.",),
        "exclusions": ("No migration is authorized.",),
        "intake_path": "records/example.intake.md",
        "documentation_path": "docs/example.md",
    }
    values.update(changes)
    return HarnessTask(**values)  # type: ignore[arg-type]
