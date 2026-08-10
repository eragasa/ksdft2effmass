r"""Software verification of authoritative SQLite harness control.

Facet and represented meaning

The module covers immutable request/result records and the maintained migration
and verification ActionObject call boundaries.

Intrinsic and cross-object scope

Intrinsic record invariants and exact ActionObject request typing are covered.
Repository migration, SQL reconstruction, and projection equality are exercised
by the bounded repository validation command rather than repeated in unit tests.

VVUQ and scientific exclusions

These tests are software verification only. They do not validate scientific
models, numerical algorithms, telemetry, protected execution, or human intent.
"""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessControlMigrationRequest,
    HarnessControlMigrationResult,
    HarnessControlMigrator,
    HarnessControlVerificationResult,
    HarnessControlVerifier,
)

pytestmark = pytest.mark.software_verification


def test_artifact__migration_request__relative_root__raises_value_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-request.relative-root-raises-value-error

    Requirement: The migration request accepts only an explicit absolute repository root.

    Method: Construct the public request with a relative ``Path``.

    Oracle: ``Path('repository')`` is relative by Python path semantics.

    Acceptance: Construction raises exactly ``ValueError``.

    Interpretation: Failure indicates an ambient-root persistence boundary regression.

    Limitations: Filesystem existence and migration behavior are not exercised.
    """  # noqa: E501
    with pytest.raises(ValueError):
        HarnessControlMigrationRequest(Path("repository"))


def test_artifact__migration_result__nested_state__is_immutable() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-result.nested-state-is-immutable

    Requirement: Migration results expose immutable tuples for counts, issues, and paths.

    Method: Construct the public result and attempt field reassignment.

    Oracle: A frozen dataclass rejects public field reassignment.

    Acceptance: Exact tuple state is retained and reassignment raises ``FrozenInstanceError``.

    Interpretation: Failure indicates mutable migration evidence or an incorrect record boundary.

    Limitations: The test does not establish that represented counts came from a migration.
    """  # noqa: E501
    result = HarnessControlMigrationResult(1, "a" * 64, (("tasks", 1),), (), ("x",))
    assert result.counts == (("tasks", 1),)
    with pytest.raises(FrozenInstanceError):
        result.schema_version = 2  # type: ignore[misc]


def test_artifact__migration_action__wrong_request_type__raises_type_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-action.wrong-request-type-raises-type-error

    Requirement: The migration ActionObject rejects values outside its request contract.

    Method: Call public ``execute`` with a plain object.

    Oracle: The public signature requires ``HarnessControlMigrationRequest`` exactly.

    Acceptance: The call raises exactly ``TypeError`` before filesystem mutation.

    Interpretation: Failure indicates a weakened structured-write boundary.

    Limitations: Valid migration behavior is covered by repository-level verification.
    """  # noqa: E501
    with pytest.raises(TypeError):
        HarnessControlMigrator().execute(object())  # type: ignore[arg-type]


def test_artifact__verification_result__reconstruction_fields__preserve_exact_values() -> (  # noqa: E501
    None
):
    """Evidence ID: software-verification.harness.sqlite-control.verification-result.reconstruction-fields-preserve-exact-values

    Requirement: Verification results distinguish source and reconstructed identities.

    Method: Construct the public ResultObject with distinct exact digest values.

    Oracle: Dataclass field order and supplied values are explicit public state.

    Acceptance: Both semantic and raw source/reconstruction identities remain distinct and exact.

    Interpretation: Failure indicates loss of reconstruction evidence in the ResultObject.

    Limitations: No SQLite file is opened by this constructor test.
    """  # noqa: E501
    result = HarnessControlVerificationResult("ok", 0, "a", "b", "c", "d", True)
    assert (result.semantic_digest, result.reconstructed_semantic_digest) == ("a", "b")
    assert (result.raw_database_sha256, result.reconstructed_database_sha256) == (
        "c",
        "d",
    )
    assert result.projections_identical is True


def test_artifact__verification_action__relative_root__raises_value_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-action.relative-root-raises-value-error

    Requirement: Verification uses an explicit absolute repository boundary.

    Method: Call the public verifier with a relative path.

    Oracle: ``Path('.')`` is not absolute.

    Acceptance: The call raises exactly ``ValueError`` before opening SQLite.

    Interpretation: Failure indicates ambient-root verification behavior.

    Limitations: Valid reconstruction is exercised by the maintained CLI validation.
    """  # noqa: E501
    with pytest.raises(ValueError):
        HarnessControlVerifier().execute(Path("."))
