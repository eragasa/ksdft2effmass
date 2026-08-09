r"""Software verification of ``ArtifactIdentity``.

Facet and represented meaning

-----------------------------
This module verifies construction, unsigned-64 boundaries, immutable fields, and exact
value semantics of the public byte-identity DataObject.

Intrinsic and cross-object scope

--------------------------------
``ArtifactIdentity`` is the sole SUT. Oracles are the published identifier, lowercase
SHA-256, built-in integer, u64, frozen-assignment, and dataclass equality contracts.

VVUQ and scientific exclusions

------------------------------
Pass/failure concerns synthetic represented metadata only. It excludes hashing real
bytes, numerical verification, scientific validation, UQ, physical correctness,
portability beyond the stated Python contract, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.provenance import ArtifactIdentity

SUT = ArtifactIdentity
pytestmark = pytest.mark.software_verification


@pytest.mark.parametrize(
    "size",
    [pytest.param(0, id="minimum_u64"), pytest.param(2**64 - 1, id="maximum_u64")],
)
def test_constructor__fields_and_u64_range__maps_exact_values(size: int) -> None:
    """Evidence ID: SV-PROV-001

    Requirement: Identity fields map exactly and byte_size accepts both inclusive u64
    boundaries.

    Method: Construct through the public import at the named zero and maximum boundary;
    no
    warning is expected or suppressed.

    Oracle: The published field vocabulary and mathematical interval [0, 2**64-1] fix
    the
    expected values independently of production validation.

    Acceptance: Each stored field equals its input exactly for the selected boundary.

    Interpretation: Failure indicates constructor mapping, range-boundary, contract, or
    test-data drift.

    Limitations: The digest and identity are synthetic; no hashing, numerical
    verification,
    scientific validation, UQ, or cross-language claim is made.
    """
    value = SUT("artifact-1", "a" * 64, size)
    assert (value.artifact_id, value.sha256, value.byte_size) == (
        "artifact-1",
        "a" * 64,
        size,
    )


@pytest.mark.parametrize(
    "byte_size",
    [
        pytest.param(True, id="boolean_wrong_type"),
        pytest.param("1", id="numeric_string_wrong_type"),
    ],
)
def test_constructor__byte_size_semantic_type__rejects_non_builtin_int(
    byte_size: object,
) -> None:
    """Evidence ID: SV-PROV-002

    Requirement: byte_size requires a built-in integer and rejects booleans and numeric
    strings.

    Method: Construct with one explicitly named member of each documented wrong-type
    partition;
    no warning is expected or suppressed.

    Oracle: Python exact-type semantics and the public no-coercion contract classify
    both
    values.

    Acceptance: Construction raises TypeError for every case.

    Interpretation: Failure indicates unintended coercion, weakened semantic typing, or
    stale evidence.

    Limitations: Other wrong Python types are represented by the authorized
    boolean/string cases;
    scientific validation, UQ, and cross-language behavior are excluded.
    """
    with pytest.raises(TypeError):
        SUT("artifact-1", "a" * 64, byte_size)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("sha256", "byte_size"),
    [
        pytest.param("a" * 64, -1, id="negative_byte_size"),
        pytest.param("a" * 64, 2**64, id="u64_overflow"),
        pytest.param("a" * 63, 1, id="short_digest"),
        pytest.param("A" * 64, 1, id="uppercase_digest"),
    ],
)
def test_constructor__digest_and_size_values__rejects_out_of_contract_values(
    sha256: str, byte_size: int
) -> None:
    """Evidence ID: SV-PROV-105

    Requirement: byte_size stays in the inclusive u64 range and sha256 is exactly 64
    lowercase hex
    characters.

    Method: Construct with named underflow, overflow, short-digest, and uppercase
    partitions;
    no warning is expected or suppressed.

    Oracle: The public interval and lowercase SHA-256 lexical grammar classify all
    literals.

    Acceptance: Construction raises ValueError for every case.

    Interpretation: Failure indicates range or digest validation drift, or a stale
    contract fixture.

    Limitations: Digest computation and all scientific, UQ, portability, and
    cross-language claims
    are excluded.
    """
    with pytest.raises(ValueError):
        SUT("artifact-1", sha256, byte_size)


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-003

    Requirement: ArtifactIdentity is operationally immutable through ordinary field
    assignment.

    Method: Construct a valid public value and assign another valid integer to
    byte_size; no
    warning is expected or suppressed.

    Oracle: The public frozen DataObject contract requires Python FrozenInstanceError.

    Acceptance: Reassignment raises FrozenInstanceError and cannot update the field.

    Interpretation: Failure indicates operational mutability or changed frozen-record
    semantics.

    Limitations: Hostile reflection and low-level memory mutation are excluded, as are
    numerical
    verification, scientific validation, UQ, and cross-language behavior.
    """
    value = SUT("artifact-1", "a" * 64, 3)
    with pytest.raises(FrozenInstanceError):
        value.byte_size = 4  # type: ignore[misc]


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID: SV-PROV-104

    Requirement: Equality is exact over artifact_id, sha256, and byte_size.

    Method: Compare separately constructed equal values and a value differing only in
    size; no
    warning is expected or suppressed.

    Oracle: The three published dataclass fields independently define complete
    represented
    state.

    Acceptance: Identical state compares equal and the one-field variant compares
    unequal.

    Interpretation: Failure indicates identity-based, transformed, or incomplete
    equality semantics.

    Limitations: Equality does not establish byte existence, digest truth, scientific
    validity, UQ,
    portability beyond Python, or cross-language conformance.
    """
    value = SUT("artifact-1", "a" * 64, 3)
    assert value == SUT("artifact-1", "a" * 64, 3)
    assert value != SUT("artifact-1", "a" * 64, 4)


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("artifact_id", id="artifact_identifier"),
        pytest.param("sha256", id="digest_text"),
    ],
)
def test_field__text_semantic_type__rejects_non_builtin_strings(field: str) -> None:
    """Evidence ID: SV-PROV-080

    Requirement: Text fields require built-in strings and do not coerce bytes.

    Method: Replace the named text field with bytes through the public constructor; no
    warning
    is expected or suppressed.

    Oracle: The documented exact semantic-type boundary requires TypeError before value
    checks.

    Acceptance: The replacement raises TypeError.

    Interpretation: Failure indicates unintended coercion or incomplete owner-local
    validation.

    Limitations: Bytes represent the non-string partition; physical meaning, validation,
    UQ,
    portability beyond Python, and cross-language behavior are excluded.
    """
    values: dict[str, object] = {
        "artifact_id": "artifact-1",
        "sha256": "a" * 64,
        "byte_size": 1,
    }
    values[field] = b"bytes"
    with pytest.raises(TypeError):
        SUT(**values)  # type: ignore[arg-type]


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
def test_field__artifact_identifier__rejects_nonportable_text(artifact_id: str) -> None:
    """Evidence ID: SV-PROV-081

    Requirement: artifact_id is nonempty NFC scalar Unicode matching the bounded
    identifier grammar.

    Method: Supply the named invalid grammar or Unicode representative; no warning is
    expected
    or suppressed.

    Oracle: The public identifier grammar and Unicode NFC definition classify each
    literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits a nonportable durable identity or indicates stale
    evidence.

    Limitations: Cross-record uniqueness, scientific validation, UQ, and cross-language
    conformance
    are excluded.
    """
    with pytest.raises(ValueError):
        SUT(artifact_id, "a" * 64, 1)


def test_field__digest_value__rejects_empty_text() -> None:
    """Evidence ID: SV-PROV-082

    Requirement: sha256 must not be empty.

    Method: Construct with an empty built-in string digest.

    Oracle: The public nonempty digest invariant classifies the literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure indicates weakened digest value validation or stale
    evidence.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        SUT("artifact-1", "", 1)


def test_field__digest_semantic_type__rejects_bytes() -> None:
    """Evidence ID: SV-PROV-114

    Requirement: sha256 requires a built-in string without bytes coercion.

    Method: Construct with a 64-byte value as sha256.

    Oracle: The exact public semantic-type boundary classifies bytes.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended digest coercion or missing type
    validation.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        SUT("artifact-1", b"a" * 64, 1)  # type: ignore[arg-type]
