r"""Software verification of ``ArtifactIdentity``.

Facet and represented meaning
-----------------------------
This module verifies the immutable byte-identity DataObject and its exact represented
fields through the public constructor.

Intrinsic and cross-object scope
--------------------------------
``ArtifactIdentity`` is the sole SUT; only its owner-local identifier, digest, size,
immutability, and value-semantics invariants are exercised.

VVUQ and scientific exclusions
------------------------------
Pass/fail concerns represented metadata only, not numerical verification, scientific
validation, UQ, physical correctness, hashing of real bytes, or cross-language
conformance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.provenance import ArtifactIdentity

SUT = ArtifactIdentity
pytestmark = pytest.mark.software_verification


def test_constructor__fields_and_u64_range__maps_exact_values() -> None:
    """Evidence ID
    SV-PROV-001
    Requirement
    Identity fields map exactly and byte_size accepts the complete unsigned 64-bit
    boundary.
    Method
    Construct public records at zero and 2**64-1 with fixed lowercase digests.
    Oracle
    The accepted P2 unsigned-64 contract and dataclass field vocabulary are fixed
    independently.
    Acceptance
    Each field equals its input exactly for both inclusive boundaries.
    Interpretation
    Failure indicates a constructor, public-contract, or test-data defect.
    Limitations
    No hashing computation, file I/O, scientific validation, UQ, or cross-language claim
    is made.
    """
    for size in (0, 2**64 - 1):
        value = SUT("artifact-1", "a" * 64, size)
        assert (value.artifact_id, value.sha256, value.byte_size) == (
            "artifact-1",
            "a" * 64,
            size,
        )


def test_constructor__types_digest_and_size__rejects_invalid_values() -> None:
    """Evidence ID
    SV-PROV-002
    Requirement
    Digests are lowercase SHA-256 text and sizes are built-in integers excluding bool in
    u64 range.
    Method
    Construct with boolean, string, overflow, negative, short, and uppercase
    alternatives.
    Oracle
    The public type and digest invariants define TypeError versus ValueError exactly.
    Acceptance
    Wrong semantic types raise TypeError and invalid values raise ValueError.
    Interpretation
    Failure identifies weakened runtime validation or stale evidence.
    Limitations
    The digest is synthetic and is not recomputed from bytes.
    """
    with pytest.raises(TypeError):
        SUT("artifact-1", "a" * 64, True)
    with pytest.raises(TypeError):
        SUT("artifact-1", "a" * 64, "1")  # type: ignore[arg-type]
    for size in (-1, 2**64):
        with pytest.raises(ValueError):
            SUT("artifact-1", "a" * 64, size)
    for digest in ("a" * 63, "A" * 64):
        with pytest.raises(ValueError):
            SUT("artifact-1", digest, 1)


def test_field__immutable_value_semantics__is_frozen_and_exact() -> None:
    """Evidence ID
    SV-PROV-003
    Requirement
    ArtifactIdentity has frozen exact value semantics.
    Method
    Compare equal public constructions and attempt ordinary field reassignment.
    Oracle
    Frozen dataclass semantics and exact represented fields are the accepted contract.
    Acceptance
    Equal values compare equal and reassignment raises FrozenInstanceError.
    Interpretation
    Failure indicates mutable state or non-exact equality.
    Limitations
    Deliberate low-level memory attacks are excluded.
    """
    value = SUT("artifact-1", "a" * 64, 3)
    assert value == SUT("artifact-1", "a" * 64, 3)
    assert value != SUT("artifact-1", "a" * 64, 4)
    with pytest.raises(FrozenInstanceError):
        value.byte_size = 4  # type: ignore[misc]


@pytest.mark.parametrize("field", ["artifact_id", "sha256"])
def test_field__text_semantic_type__rejects_non_builtin_strings(field: str) -> None:
    """Evidence ID
    SV-PROV-080
    Requirement
    Text fields require built-in strings and do not coerce bytes or other values.
    Method
    Replace each text field independently with bytes through the public constructor.
    Oracle
    The documented semantic type boundary requires TypeError before value validation.
    Acceptance
    Every replacement raises TypeError.
    Interpretation
    Failure indicates unintended coercion or incomplete owner-local validation.
    Limitations
    Representative wrong types stand for the semantic non-string partition.
    """
    values: dict[str, object] = {
        "artifact_id": "artifact-1",
        "sha256": "a" * 64,
        "byte_size": 1,
    }
    values[field] = b"bytes"
    with pytest.raises(TypeError):
        SUT(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize("artifact_id", ["", "bad id", "e\u0301", "\ud800", "a" * 129])
def test_field__artifact_identifier__rejects_nonportable_text(artifact_id: str) -> None:
    """Evidence ID
    SV-PROV-081
    Requirement
    artifact_id is nonempty NFC scalar Unicode matching the bounded identifier grammar.
    Method
    Supply empty, spaced, decomposed, surrogate, and overlength representatives.
    Oracle
    The public identifier grammar and Unicode NFC definition classify every case.
    Acceptance
    Every prohibited identifier raises ValueError.
    Interpretation
    Failure admits a nonportable durable artifact identity.
    Limitations
    Cross-record identifier uniqueness is outside this DataObject.
    """
    with pytest.raises(ValueError):
        SUT(artifact_id, "a" * 64, 1)


def test_field__digest_semantic_type__rejects_empty_and_non_string_values() -> None:
    """Evidence ID
    SV-PROV-082
    Requirement
    sha256 is a nonempty built-in string before its lowercase digest grammar is applied.
    Method
    Supply an empty string and bytes digest to the public constructor.
    Oracle
    Empty text violates the value invariant; bytes violate the semantic type invariant.
    Acceptance
    Empty text raises ValueError and bytes raise TypeError.
    Interpretation
    Failure indicates an incomplete digest validation partition.
    Limitations
    Digest computation from artifact bytes is excluded.
    """
    with pytest.raises(ValueError):
        SUT("artifact-1", "", 1)
    with pytest.raises(TypeError):
        SUT("artifact-1", b"a" * 64, 1)  # type: ignore[arg-type]
