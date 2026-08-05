"""Evidence class and represented meaning
Software verification of the stateless exact artifact identity ActionObject.
Owned contract, oracle, and scope
ArtifactIdentityVerifier is the SUT; hand-compared digest and byte-size equality is the
independent oracle.
VVUQ and scientific exclusions
Evidence performs no file I/O and excludes numerical verification, scientific
validation, UQ, format correctness, and cross-language conformance.
"""

import pytest

from ksdft2effmass.provenance import (
    ArtifactIdentity,
    ArtifactIdentityVerificationStatus,
    ArtifactIdentityVerifier,
    ArtifactReference,
    ArtifactSpecification,
)

SUT = ArtifactIdentityVerifier
pytestmark = pytest.mark.software_verification


def _reference() -> ArtifactReference:
    """Evidence ID
    Supports SV-PROV-049 and SV-PROV-050 and owns no separate identifier.
    Requirement
    Provide one explicit sealed-reference input.
    Method
    Construct public nested records with a fixed digest and size.
    Oracle
    Values are independently chosen and visible to each assertion.
    Acceptance
    A valid ArtifactReference is returned.
    Interpretation
    Failure is setup failure only.
    Limitations
    The digest is synthetic.
    """
    return ArtifactReference(
        ArtifactIdentity("artifact-1", "a" * 64, 10),
        ArtifactSpecification("out/a", "bin", "result", "retain"),
        "manifest-1",
    )


def test_method__execute_exact_identity__returns_verified_or_mismatch_without_io() -> (
    None
):
    """Evidence ID
    SV-PROV-049
    Requirement
    execute returns VERIFIED only when both observed digest and size equal the reference
    exactly.
    Method
    Exercise matching, digest-different, and size-different public inputs.
    Oracle
    Direct equality of visible literal digest and integer pairs is independent of the
    action implementation.
    Acceptance
    Matching input is VERIFIED; each single-field difference is MISMATCH with exact
    expected/observed fields.
    Interpretation
    Failure indicates comparison or result mapping drift.
    Limitations
    The action accepts already observed values and does not validate observation
    acquisition.
    """
    action = SUT()
    verified = action.execute(_reference(), "a" * 64, 10)
    digest_mismatch = action.execute(_reference(), "b" * 64, 10)
    size_mismatch = action.execute(_reference(), "a" * 64, 11)
    assert verified.status is ArtifactIdentityVerificationStatus.VERIFIED
    assert digest_mismatch.status is ArtifactIdentityVerificationStatus.MISMATCH
    assert size_mismatch.status is ArtifactIdentityVerificationStatus.MISMATCH
    assert (size_mismatch.expected_byte_size, size_mismatch.observed_byte_size) == (
        10,
        11,
    )


def test_method__execute_input_boundary__rejects_wrong_types_and_invalid_u64() -> None:
    """Evidence ID
    SV-PROV-050
    Requirement
    execute accepts only ArtifactReference, lowercase SHA-256, and built-in u64 size
    excluding bool.
    Method
    Pass mapping reference, uppercase digest, bool size, and overflow size.
    Oracle
    The public action signature and P2 digest/u64 contract fix exception classes.
    Acceptance
    Wrong reference/bool raise TypeError and invalid digest/overflow raise ValueError.
    Interpretation
    Failure indicates coercion or boundary-validation drift.
    Limitations
    Representative invalid values are used rather than every malformed digest.
    """
    action = SUT()
    with pytest.raises(TypeError):
        action.execute({}, "a" * 64, 1)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        action.execute(_reference(), "A" * 64, 1)
    with pytest.raises(TypeError):
        action.execute(_reference(), "a" * 64, True)
    with pytest.raises(ValueError):
        action.execute(_reference(), "a" * 64, 2**64)
