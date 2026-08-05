"""Evidence class and represented meaning
Software verification of the immutable byte-identity DataObject.
Owned contract, oracle, and scope
ArtifactIdentity is the SUT; the public P2 contract is the exact oracle.
VVUQ and scientific exclusions
Pass/fail concerns represented metadata only, not numerical verification, scientific
validation, UQ, physical correctness, or cross-language conformance.
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
    with pytest.raises(FrozenInstanceError):
        value.byte_size = 4  # type: ignore[misc]
