r"""Software verification of ``ArtifactIdentityVerificationResult``.

Facet and represented meaning

-----------------------------
This module verifies immutable represented expected/observed artifact identity and its
derived exact-match status.

Intrinsic and cross-object scope

--------------------------------
``ArtifactIdentityVerificationResult`` is the sole SUT. Literal identifiers, lowercase
SHA-256 text, unsigned 64-bit sizes, dataclass fields, and Python equality are oracles.

VVUQ and scientific exclusions

------------------------------
Passing establishes ResultObject mapping and invariants only. It excludes file I/O,
cryptographic correctness, numerical verification, scientific validation, UQ, format
truth, portability, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.provenance import (
    ArtifactIdentityVerificationResult,
    ArtifactIdentityVerificationStatus,
)

SUT = ArtifactIdentityVerificationResult
pytestmark = pytest.mark.software_verification

EQUALITY_FIELDS = (
    "artifact_id",
    "expected_sha256",
    "observed_sha256",
    "expected_size_bytes",
    "observed_size_bytes",
)


def test_constructor__verification_fields__maps_exact_values() -> None:
    """Evidence ID: SV-PROV-174

    Requirement: Construction maps all five represented identity fields without
    coercion.

    Method: Construct one result using distinct literal expected and observed values.

    Oracle: Constructor argument order and the independently chosen literals fix stored
    state.

    Acceptance: The five public fields equal their inputs exactly.

    Interpretation: Failure indicates constructor mapping or represented-state drift.

    Limitations: The digest text and sizes are synthetic and no bytes are observed.
    """
    value = SUT("artifact-1", "a" * 64, "b" * 64, 10, 11)
    assert (
        value.artifact_id,
        value.expected_sha256,
        value.observed_sha256,
        value.expected_byte_size,
        value.observed_byte_size,
    ) == ("artifact-1", "a" * 64, "b" * 64, 10, 11)


@pytest.mark.parametrize(
    ("expected_sha256", "observed_sha256", "expected_size", "observed_size", "status"),
    [
        pytest.param(
            "a" * 64,
            "a" * 64,
            10,
            10,
            ArtifactIdentityVerificationStatus.VERIFIED,
            id="verified",
        ),
        pytest.param(
            "a" * 64,
            "b" * 64,
            10,
            10,
            ArtifactIdentityVerificationStatus.MISMATCH,
            id="digest_mismatch",
        ),
        pytest.param(
            "a" * 64,
            "a" * 64,
            10,
            11,
            ArtifactIdentityVerificationStatus.MISMATCH,
            id="size_mismatch",
        ),
        pytest.param(
            "a" * 64,
            "b" * 64,
            10,
            11,
            ArtifactIdentityVerificationStatus.MISMATCH,
            id="digest_and_size_mismatch",
        ),
    ],
)
def test_property__status__derives_exact_identity_outcome(
    expected_sha256: str,
    observed_sha256: str,
    expected_size: int,
    observed_size: int,
    status: ArtifactIdentityVerificationStatus,
) -> None:
    """Evidence ID: SV-PROV-046

    Requirement: Status is VERIFIED only when both digest and size match, otherwise
    MISMATCH.

    Method: Partition exact match, each single mismatch, and simultaneous digest/size
    mismatch.

    Oracle: Direct equality of the four visible literal identity components predicts
    status.

    Acceptance: Each case returns the exact independently listed enum member.

    Interpretation: Failure indicates incorrect conjunction or status derivation.

    Limitations: This does not validate how observed values were acquired.
    """
    assert (
        SUT(
            "artifact-1", expected_sha256, observed_sha256, expected_size, observed_size
        ).status
        is status
    )


def test_field__status_storage__excludes_derived_property() -> None:
    """Evidence ID: SV-PROV-144

    Requirement: Derived status is not independently stored in represented result state.

    Method: Inspect the public dataclass field inventory.

    Oracle: The public ResultObject contract declares exactly five represented fields.

    Acceptance: Field names equal the literal five-name tuple and exclude status.

    Interpretation: Failure indicates duplicated or mutable derived state.

    Limitations: Reflection does not assess hostile runtime mutation.
    """
    assert tuple(field.name for field in fields(SUT)) == (
        "artifact_id",
        "expected_sha256",
        "observed_sha256",
        "expected_byte_size",
        "observed_byte_size",
    )


def test_field__artifact_identifier_semantic_type__rejects_non_builtin_string() -> None:
    """Evidence ID: SV-PROV-145

    Requirement: artifact_id accepts only a built-in string.

    Method: Construct with bytes while all other fields remain valid.

    Oracle: The documented semantic type boundary requires TypeError without coercion.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates coercion or weakened identifier typing.

    Limitations: User-defined string subclasses are not separately partitioned.
    """
    with pytest.raises(TypeError):
        SUT(b"artifact-1", "a" * 64, "a" * 64, 1, 1)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "artifact_id",
    [
        pytest.param("", id="empty_identifier"),
        pytest.param("bad id", id="embedded_space"),
        pytest.param("e\u0301", id="non_nfc_identifier"),
        pytest.param("\ud800", id="unicode_surrogate"),
        pytest.param("a" * 129, id="overlength_identifier"),
    ],
)
def test_field__artifact_identifier_value__rejects_nonportable_text(
    artifact_id: str,
) -> None:
    """Evidence ID: SV-PROV-146

    Requirement: artifact_id obeys the nonempty portable identifier grammar and length
    limit.

    Method: Partition empty, embedded-space, non-NFC, surrogate, and overlength strings.

    Oracle: The public portable-identifier grammar rejects each literal.

    Acceptance: Every case raises ValueError.

    Interpretation: Failure indicates malformed identifier acceptance.

    Limitations: The cases cover the declared grammar boundaries, not every Unicode
    string.
    """
    with pytest.raises(ValueError):
        SUT(artifact_id, "a" * 64, "a" * 64, 1, 1)


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("expected_sha256", id="expected_digest"),
        pytest.param("observed_sha256", id="observed_digest"),
    ],
)
def test_field__digest_semantic_type__rejects_non_string(field_name: str) -> None:
    """Evidence ID: SV-PROV-147

    Requirement: Both digest fields accept only built-in strings.

    Method: Replace one digest at a time with bytes through keyword construction.

    Oracle: The documented digest semantic type requires TypeError without coercion.

    Acceptance: Each partition raises TypeError.

    Interpretation: Failure indicates a weakened digest type boundary.

    Limitations: Cryptographic computation and collision resistance are excluded.
    """
    values: dict[str, object] = {
        "artifact_id": "artifact-1",
        "expected_sha256": "a" * 64,
        "observed_sha256": "a" * 64,
        "expected_byte_size": 1,
        "observed_byte_size": 1,
    }
    values[field_name] = b"a" * 64
    with pytest.raises(TypeError):
        SUT(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field_name", "digest"),
    [
        pytest.param("expected_sha256", "", id="expected_empty_digest"),
        pytest.param("expected_sha256", "A" * 64, id="expected_uppercase_digest"),
        pytest.param("expected_sha256", "g" * 64, id="expected_nonhex_digest"),
        pytest.param("expected_sha256", "a" * 63, id="expected_short_digest"),
        pytest.param("observed_sha256", "", id="observed_empty_digest"),
        pytest.param("observed_sha256", "A" * 64, id="observed_uppercase_digest"),
        pytest.param("observed_sha256", "g" * 64, id="observed_nonhex_digest"),
        pytest.param("observed_sha256", "a" * 63, id="observed_short_digest"),
    ],
)
def test_field__digest_value__rejects_malformed_sha256(
    field_name: str, digest: str
) -> None:
    """Evidence ID: SV-PROV-148

    Requirement: Both digest fields require exactly 64 lowercase hexadecimal characters.

    Method: Partition empty, uppercase, nonhex, and short text for both digest fields.

    Oracle: The public lowercase SHA-256 grammar rejects each literal.

    Acceptance: Every case raises ValueError.

    Interpretation: Failure indicates malformed digest acceptance.

    Limitations: Valid syntax does not prove a digest was computed from content.
    """
    values = {
        "artifact_id": "artifact-1",
        "expected_sha256": "a" * 64,
        "observed_sha256": "a" * 64,
        "expected_byte_size": 1,
        "observed_byte_size": 1,
    }
    values[field_name] = digest
    with pytest.raises(ValueError):
        SUT(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("expected_byte_size", id="expected_size"),
        pytest.param("observed_byte_size", id="observed_size"),
    ],
)
def test_field__byte_size_semantic_type__rejects_non_integer(field_name: str) -> None:
    """Evidence ID: SV-PROV-149

    Requirement: Both byte-size fields accept only built-in integers.

    Method: Replace one size at a time with the numeric string ``"1"``.

    Oracle: The documented semantic type boundary requires TypeError without coercion.

    Acceptance: Each partition raises TypeError.

    Interpretation: Failure indicates numeric-string coercion or weakened typing.

    Limitations: Boolean rejection is independently partitioned.
    """
    values: dict[str, object] = {
        "artifact_id": "artifact-1",
        "expected_sha256": "a" * 64,
        "observed_sha256": "a" * 64,
        "expected_byte_size": 1,
        "observed_byte_size": 1,
    }
    values[field_name] = "1"
    with pytest.raises(TypeError):
        SUT(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("expected_byte_size", id="expected_size_boolean"),
        pytest.param("observed_byte_size", id="observed_size_boolean"),
    ],
)
def test_field__byte_size_boolean__rejects_bool(field_name: str) -> None:
    """Evidence ID: SV-PROV-047

    Requirement: Boolean values are rejected as byte sizes despite being integer
    subclasses.

    Method: Replace each byte-size field independently with True.

    Oracle: The explicit built-in-int-excluding-bool contract requires TypeError.

    Acceptance: Each partition raises TypeError.

    Interpretation: Failure indicates accidental Boolean acceptance.

    Limitations: Other wrong semantic types are covered separately.
    """
    values: dict[str, object] = {
        "artifact_id": "artifact-1",
        "expected_sha256": "a" * 64,
        "observed_sha256": "a" * 64,
        "expected_byte_size": 1,
        "observed_byte_size": 1,
    }
    values[field_name] = True
    with pytest.raises(TypeError):
        SUT(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("expected_size", "observed_size"),
    [
        pytest.param(0, 0, id="minimum_u64"),
        pytest.param(2**64 - 1, 2**64 - 1, id="maximum_u64"),
    ],
)
def test_field__byte_size_bounds__accepts_inclusive_u64(
    expected_size: int, observed_size: int
) -> None:
    """Evidence ID: SV-PROV-150

    Requirement: Both byte sizes accept the inclusive unsigned 64-bit endpoints.

    Method: Construct values at zero and 2**64 minus one.

    Oracle: The mathematical u64 interval independently fixes both valid endpoints.

    Acceptance: Stored sizes equal the endpoint inputs exactly.

    Interpretation: Failure indicates an off-by-one range defect.

    Limitations: Python integer behavior outside the interval is covered separately.
    """
    value = SUT("artifact-1", "a" * 64, "a" * 64, expected_size, observed_size)
    assert (value.expected_byte_size, value.observed_byte_size) == (
        expected_size,
        observed_size,
    )


@pytest.mark.parametrize(
    ("field_name", "size"),
    [
        pytest.param("expected_byte_size", -1, id="expected_negative_one"),
        pytest.param("expected_byte_size", 2**64, id="expected_u64_overflow"),
        pytest.param("observed_byte_size", -1, id="observed_negative_one"),
        pytest.param("observed_byte_size", 2**64, id="observed_u64_overflow"),
    ],
)
def test_field__byte_size_value__rejects_outside_u64(
    field_name: str, size: int
) -> None:
    """Evidence ID: SV-PROV-151

    Requirement: Both byte sizes reject integers outside the unsigned 64-bit interval.

    Method: Partition the immediate lower and upper out-of-range values for each field.

    Oracle: The mathematical u64 interval excludes -1 and 2**64.

    Acceptance: Every case raises ValueError.

    Interpretation: Failure indicates an off-by-one or missing range check.

    Limitations: No storage allocation is performed.
    """
    values = {
        "artifact_id": "artifact-1",
        "expected_sha256": "a" * 64,
        "observed_sha256": "a" * 64,
        "expected_byte_size": 1,
        "observed_byte_size": 1,
    }
    values[field_name] = size
    with pytest.raises(ValueError):
        SUT(**values)  # type: ignore[arg-type]


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-152

    Requirement: Verification results are operationally immutable through ordinary
    assignment.

    Method: Assign another valid artifact identifier to a constructed result.

    Oracle: The public frozen ResultObject contract requires FrozenInstanceError.

    Acceptance: Reassignment raises FrozenInstanceError.

    Interpretation: Failure indicates mutable durable result state.

    Limitations: Hostile reflection is excluded.
    """
    value = SUT("artifact-1", "a" * 64, "a" * 64, 1, 1)
    with pytest.raises(FrozenInstanceError):
        value.artifact_id = "artifact-2"  # type: ignore[misc]


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID: SV-PROV-153

    Requirement: Equality compares all represented fields exactly.

    Method: Compare equal constructions and five variants, each changing exactly one
    field.

    Oracle: Dataclass value semantics and each independent literal field difference
    predict
    inequality.

    Acceptance: Equal state compares equal; every single-field variant compares unequal.

    Interpretation: Failure indicates incomplete or nonexact value semantics.

    Limitations: Equality does not establish scientific or content identity.
    """
    baseline = SUT("artifact-1", "a" * 64, "a" * 64, 1, 1)
    assert baseline == SUT("artifact-1", "a" * 64, "a" * 64, 1, 1)
    assert baseline != SUT("artifact-2", "a" * 64, "a" * 64, 1, 1)
    assert baseline != SUT("artifact-1", "b" * 64, "a" * 64, 1, 1)
    assert baseline != SUT("artifact-1", "a" * 64, "b" * 64, 1, 1)
    assert baseline != SUT("artifact-1", "a" * 64, "a" * 64, 2, 1)
    assert baseline != SUT("artifact-1", "a" * 64, "a" * 64, 1, 2)
