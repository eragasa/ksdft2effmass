r"""Software verification of ``HarnessControlVerifier``.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``HarnessControlVerifier``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import sqlite3
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import HarnessControlVerifier
from ksdft2effmass.harness.pi.local.dbcontrol.database import _ControlDatabase
from ksdft2effmass.harness.pi.local.dbcontrol.schema import _SCHEMA

SUT = HarnessControlVerifier

pytestmark = pytest.mark.software_verification


def test_method__execute_relative_root__raises_value_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-action.relative-root-raises-value-error

    Requirement: Verification uses an explicit absolute repository boundary.

    Method: Call the public verifier with a relative path.

    Oracle: ``Path('.')`` is not absolute.

    Acceptance: The call raises exactly ``ValueError`` before opening SQLite.

    Interpretation: Failure indicates ambient-root verification behavior.

    Limitations: Valid reconstruction is covered separately.
    """  # noqa: E501
    with pytest.raises(ValueError):
        HarnessControlVerifier().execute(Path("."))


def test_method__execute_valid_reconstruction__reports_exact_agreement(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-action.valid-reconstruction

    Requirement: Verification reports SQLite integrity, zero foreign-key issues, semantic reconstruction equality, and projection equality for valid authority.

    Method: Build authority and deterministic SQL from one immutable literal metadata row, then execute the public verifier.

    Oracle: A schema-valid database reconstructed from its deterministic SQL has identical ordered logical rows; raw hashes remain report-only.

    Acceptance: Integrity is ``ok``, issue count zero, semantic digests equal, both digests are 64 characters, and projections are identical.

    Interpretation: Failure indicates verifier reconstruction or comparison drift.

    Limitations: Raw SQLite byte equality is not required and full repository ingestion is excluded.
    """  # noqa: E501
    state = tmp_path / "harness/state"
    state.mkdir(parents=True)
    database_path = state / "harness-control.sqlite3"
    _ControlDatabase.reconstruct(database_path, (_SCHEMA + "\n").encode())
    with sqlite3.connect(database_path) as connection:
        connection.execute("INSERT INTO harness_metadata VALUES ('literal','value')")
        connection.commit()
        sql = _ControlDatabase(connection).deterministic_sql_export()
    (state / "harness-control.sql").write_bytes(sql)
    result = HarnessControlVerifier().execute(tmp_path.resolve())
    assert (result.integrity_check, result.foreign_key_issue_count) == ("ok", 0)
    assert result.semantic_digest == result.reconstructed_semantic_digest
    assert len(result.semantic_digest) == 64
    assert result.projections_identical is True
