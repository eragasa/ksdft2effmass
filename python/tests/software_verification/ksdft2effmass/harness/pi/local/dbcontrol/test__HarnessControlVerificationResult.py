r"""Software verification of ``HarnessControlVerificationResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the complete intrinsic source-aware verification result.

Intrinsic and cross-object scope

Represented agreement, structured finding consistency, value semantics, and
immutability are intrinsic; filesystem comparison belongs to the verifier Action.

VVUQ and scientific exclusions

This is structural software verification only; scientific validation and UQ are
excluded.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessControlVerificationFinding,
    HarnessControlVerificationResult,
)

SUT = HarnessControlVerificationResult
pytestmark = pytest.mark.software_verification


def agreement(*, raw_candidate: str = "raw") -> HarnessControlVerificationResult:
    """Evidence ID: Owns no identifier; supports verification-result evidence.

    Requirement: Result tests need one complete represented-agreement value.

    Method: Construct exact literal agreement fields with one selectable diagnostic
    candidate hash.

    Oracle: The public result contract fixes represented agreement independently of
    raw hash equality.

    Acceptance: Return one immutable successful result.

    Interpretation: Failure indicates fixture construction drift.

    Limitations: This helper establishes no independent verification claim.
    """  # noqa: E501
    return SUT("ok", 0, "semantic", "semantic", "raw", raw_candidate, True)


def test_constructor__reconstruction_fields__preserve_exact_values() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-result.reconstruction-fields-preserve-exact-values

    Requirement: Verification results preserve every agreement field while raw SQLite
    hashes remain diagnostic and may differ under semantic agreement.

    Method: Construct two equal successful results whose raw hashes differ.

    Oracle: Literal semantic identities and agreement booleans define success; no raw
    hash equality is required.

    Acceptance: All represented agreement fields are true, findings are empty, raw
    hashes differ, and equal constructions compare exactly.

    Interpretation: Failure conflates SQLite bytes with represented semantics or loses
    public state.

    Limitations: No SQLite file is opened.
    """  # noqa: E501
    result = agreement(raw_candidate="different-raw")
    assert result == agreement(raw_candidate="different-raw")
    assert result.raw_database_sha256 != result.reconstructed_database_sha256
    assert (
        result.schema_version_agrees,
        result.sql_identical,
        result.manifest_identical,
        result.projections_identical,
        result.findings,
    ) == (True, True, True, True, ())


@pytest.mark.parametrize(
    "field",
    (
        pytest.param("projections_identical", id="projection_boolean"),
        pytest.param("schema_version_agrees", id="schema_boolean"),
        pytest.param("sql_identical", id="sql_boolean"),
        pytest.param("manifest_identical", id="manifest_boolean"),
    ),
)
def test_constructor__agreement_flags__require_strict_booleans(field: str) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-result.strict-booleans

    Requirement: Every represented agreement flag accepts exactly built-in Boolean
    values.

    Method: Replace one flag at a time with integer one.

    Oracle: Python distinguishes ``bool`` from semantically invalid integer flags.

    Acceptance: Every partition raises ``TypeError``.

    Interpretation: Failure admits ambiguous JSON Boolean state.

    Limitations: Valid flag combinations are covered separately.
    """  # noqa: E501
    values = {
        "projections_identical": True,
        "schema_version_agrees": True,
        "sql_identical": True,
        "manifest_identical": True,
    }
    values[field] = 1  # type: ignore[assignment]
    with pytest.raises(TypeError):
        SUT(
            "ok",
            0,
            "a",
            "a",
            "b",
            "b",
            values["projections_identical"],
            values["schema_version_agrees"],
            values["sql_identical"],
            values["manifest_identical"],
        )


def test_constructor__structured_findings__require_sorted_unique_consistency() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-result.finding-consistency

    Requirement: Drift requires sorted unique structured findings and semantic digest
    disagreement is represented independently of raw hashes.

    Method: Construct one valid semantic disagreement, then reverse and duplicate two
    findings and omit findings from disagreement.

    Oracle: Literal finding keys and represented semantic equality define consistency.

    Acceptance: Valid drift is preserved; reversed, duplicate, and missing findings
    raise ``ValueError``.

    Interpretation: Failure admits nondeterministic or unreported drift.

    Limitations: Finding code field invariants have their own class owner.
    """  # noqa: E501
    changed = HarnessControlVerificationFinding(
        "changed_artifact", "harness/state/harness-control.sql", "changed"
    )
    semantic = HarnessControlVerificationFinding(
        "semantic_disagreement", "harness/state/harness-control.sqlite3", "different"
    )
    findings = (changed, semantic)
    result = SUT("ok", 0, "a", "b", "raw", "raw", True, True, True, True, findings)
    assert result.findings == findings
    with pytest.raises(ValueError, match="sorted"):
        SUT(
            "ok",
            0,
            "a",
            "b",
            "raw",
            "raw",
            True,
            True,
            True,
            True,
            tuple(reversed(findings)),
        )
    with pytest.raises(ValueError, match="sorted"):
        SUT("ok", 0, "a", "b", "raw", "raw", True, True, True, True, (changed, changed))
    with pytest.raises(ValueError, match="agree"):
        SUT("ok", 0, "a", "b", "raw", "raw", True)
    with pytest.raises(ValueError, match="agree"):
        SUT("ok", 0, "a", "a", "raw", "raw", True, findings=(changed,))


def test_constructor__immutability__rejects_field_assignment() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-result.immutable

    Requirement: Verification results reject public mutation.

    Method: Assign a new digest to a successful frozen result.

    Oracle: Frozen dataclass semantics define rejection.

    Acceptance: Assignment raises ``FrozenInstanceError``.

    Interpretation: Failure permits verification evidence to change after execution.

    Limitations: Nested findings are independently immutable.
    """  # noqa: E501
    result = agreement()
    with pytest.raises(FrozenInstanceError):
        result.semantic_digest = "changed"  # type: ignore[misc]
