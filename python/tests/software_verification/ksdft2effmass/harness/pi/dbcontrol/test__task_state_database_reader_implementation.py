r"""Software verification of generic dbcontrol task-state-database-reader implementation artifact.

Evidence profile: routine

Bounded artifact scope: generic dbcontrol private task-state-database-reader implementation behavior.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_TaskStateDatabaseReader``.

Intrinsic and cross-object scope

Only the object's bounded contract is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""  # noqa: E501

import sqlite3
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.dbcontrol.database import _TaskStateDatabaseReader

SUT = _TaskStateDatabaseReader

pytestmark = pytest.mark.software_verification


def test_method__read_existing_row__returns_exact_lifecycle(tmp_path: Path) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.task-state-schema.generic-reader-agrees

    Requirement: The generic reader returns the exact lifecycle status and Boolean activation represented by its SQLite row.

    Method: Create a literal minimal SQLite table and row, then read its exact Task identity.

    Oracle: The independently supplied row is ``("active", 1)``.

    Acceptance: Reading returns exactly ``("active", True)``.

    Interpretation: Failure indicates drift in the project-neutral read contract.

    Limitations: Schema migration and repository projections are excluded.
    """  # noqa: E501
    path = tmp_path / "control.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute(
            "CREATE TABLE task_state("
            "task_id TEXT, lifecycle_status TEXT, is_active INTEGER)"
        )
        connection.execute("INSERT INTO task_state VALUES ('task.test','active',1)")
    assert _TaskStateDatabaseReader(path).read("task.test") == ("active", True)
