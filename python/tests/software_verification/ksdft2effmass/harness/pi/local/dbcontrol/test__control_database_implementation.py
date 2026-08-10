r"""Software verification of project-local dbcontrol control-database implementation artifact.

Evidence profile: routine

Bounded artifact scope: project-local dbcontrol private control-database implementation behavior.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_ControlDatabase``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""  # noqa: E501

import sqlite3
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local.dbcontrol.database import _ControlDatabase
from ksdft2effmass.harness.pi.local.dbcontrol.schema import _SCHEMA

SUT = _ControlDatabase

pytestmark = pytest.mark.software_verification


def test_method__deterministic_sql_export__reconstructs_semantic_digest(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.dbcontrol.control-database.method.deterministic-sql-reconstruction

    Requirement: Deterministic SQL reconstructs the same logical control tables and semantic digest.

    Method: Initialize the declared schema, add one literal metadata row, export twice, reconstruct, and compare ordered semantics.

    Oracle: The immutable row ``("literal", "O'Reilly")`` and SQL escaping ``O''Reilly`` are independent inputs.

    Acceptance: Export bytes repeat exactly, contain the escaped literal, and reconstructed semantic digests equal.

    Interpretation: Failure indicates nondeterministic recovery bytes or semantic loss.

    Limitations: Repository corpus ingestion is excluded.
    """  # noqa: E501
    source_path = tmp_path / "source.sqlite3"
    _ControlDatabase.reconstruct(source_path, (_SCHEMA + "\n").encode())
    with sqlite3.connect(source_path) as connection:
        connection.execute(
            "INSERT INTO harness_metadata VALUES (?,?)", ("literal", "O'Reilly")
        )
        connection.commit()
        database = _ControlDatabase(connection)
        expected_digest = database.normalized_semantic_digest()
        first = database.deterministic_sql_export()
        second = database.deterministic_sql_export()
    assert first == second
    assert b"O''Reilly" in first
    target_path = tmp_path / "target.sqlite3"
    _ControlDatabase.reconstruct(target_path, first)
    with sqlite3.connect(target_path) as target:
        assert _ControlDatabase(target).normalized_semantic_digest() == expected_digest
