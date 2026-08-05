"""Evidence class and represented meaning
Software verification of exact artifact byte-identity verification results.
Owned contract, oracle, and scope
ArtifactIdentityVerificationResult is the SUT; represented fields, derived status, and
u64 rules are the oracle.
VVUQ and scientific exclusions
Evidence excludes file I/O, numerical verification, scientific validation, UQ, format
truth, and cross-language conformance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.provenance import (
    ArtifactIdentityVerificationResult,
    ArtifactIdentityVerificationStatus,
)

SUT = ArtifactIdentityVerificationResult
pytestmark = pytest.mark.software_verification


def test_constructor__verification_fields__maps_values_and_derives_status() -> None:
    """Evidence ID
    SV-PROV-046
    Requirement
    Results store only expected/observed identity fields and derive VERIFIED exactly
    when digest and size both match.
    Method
    Construct matching, digest-mismatching, and size-mismatching public results.
    Oracle
    Direct equality of visible strings and integers independently determines each
    status.
    Acceptance
    Matching values derive VERIFIED; either single difference derives MISMATCH; status
    is not a dataclass field.
    Interpretation
    Failure indicates field mapping or derived-status drift.
    Limitations
    Digests are synthetic and represented bytes are not observed.
    """
    verified = SUT("a", "a" * 64, "a" * 64, 2**64 - 1, 2**64 - 1)
    digest_mismatch = SUT("a", "a" * 64, "b" * 64, 1, 1)
    size_mismatch = SUT("a", "a" * 64, "a" * 64, 1, 2)
    assert verified.status is ArtifactIdentityVerificationStatus.VERIFIED
    assert digest_mismatch.status is ArtifactIdentityVerificationStatus.MISMATCH
    assert size_mismatch.status is ArtifactIdentityVerificationStatus.MISMATCH
    assert "status" not in {field.name for field in fields(SUT)}


def test_constructor__digest_and_size_types__rejects_invalid_values() -> None:
    """Evidence ID
    SV-PROV-047
    Requirement
    Digest fields are lowercase SHA-256 and sizes are built-in u64 integers excluding
    bool.
    Method
    Construct with boolean, overflow, and uppercase digest alternatives.
    Oracle
    The public digest grammar and inclusive unsigned-64 range define error classes.
    Acceptance
    Boolean raises TypeError; overflow and uppercase digest raise ValueError.
    Interpretation
    Failure indicates weakened ResultObject validation.
    Limitations
    Cryptographic computation and collision resistance are excluded.
    """
    with pytest.raises(TypeError):
        SUT("a", "a" * 64, "a" * 64, 1, True)
    with pytest.raises(ValueError):
        SUT("a", "a" * 64, "a" * 64, 1, 2**64)
    with pytest.raises(ValueError):
        SUT("a", "A" * 64, "a" * 64, 1, 1)


def test_field__verification_status_values__are_exact() -> None:
    """Evidence ID
    SV-PROV-048
    Requirement
    Derived identity status values are exactly verified and mismatch.
    Method
    Enumerate the public string enum artifact.
    Oracle
    The accepted version-1 vocabulary fixes both exact values.
    Acceptance
    The value tuple matches exactly.
    Interpretation
    Failure indicates public derived-status vocabulary drift.
    Limitations
    VERIFIED establishes represented identity only.
    """
    assert tuple(item.value for item in ArtifactIdentityVerificationStatus) == (
        "verified",
        "mismatch",
    )
