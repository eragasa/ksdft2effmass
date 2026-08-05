"""Evidence class and represented meaning
Software verification of capability-verification observations.
Owned contract, oracle, and scope
VerificationObservation is the SUT; lifecycle separation, canonical evidence IDs, safe
fields, and status vocabulary are the oracle.
VVUQ and scientific exclusions
Evidence excludes capability execution, numerical acceptance, scientific validation, UQ,
and cross-language conformance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.provenance import VerificationObservation, VerificationStatus

SUT = VerificationObservation
pytestmark = pytest.mark.software_verification


def test_constructor__verification_fields__maps_safe_evidence_and_provenance() -> None:
    """Evidence ID
    SV-PROV-034
    Requirement
    Verification correlates installation, capability, status, evidence artifacts, and
    provenance without raw detail.
    Method
    Construct a rejected observation and inspect all six fields and the field inventory.
    Oracle
    The corrected verification vocabulary independently fixes the mapping.
    Acceptance
    Every value maps exactly and no detail/message field exists.
    Interpretation
    Failure indicates lifecycle mapping or raw diagnostic leakage.
    Limitations
    Synthetic status does not prove a real tool was tested.
    """
    value = SUT(
        "verify-1",
        "install-1",
        "cap-1",
        VerificationStatus.REJECTED,
        ("evidence-a",),
        "prov-1",
    )
    assert (
        value.verification_id,
        value.installation_id,
        value.capability_id,
        value.status,
        value.evidence_artifact_ids,
        value.provenance_id,
    ) == (
        "verify-1",
        "install-1",
        "cap-1",
        VerificationStatus.REJECTED,
        ("evidence-a",),
        "prov-1",
    )
    assert tuple(field.name for field in fields(SUT)) == (
        "verification_id",
        "installation_id",
        "capability_id",
        "status",
        "evidence_artifact_ids",
        "provenance_id",
    )


def test_constructor__evidence_identifiers__requires_canonical_tuple() -> None:
    """Evidence ID
    SV-PROV-035
    Requirement
    Evidence identities are a built-in lexically sorted duplicate-free tuple.
    Method
    Pass list, unsorted tuple, and duplicate tuple alternatives.
    Oracle
    The canonical identifier invariant defines rejection.
    Acceptance
    List raises TypeError and noncanonical tuples raise ValueError.
    Interpretation
    Failure indicates unstable verification representation.
    Limitations
    Artifact existence and evidentiary adequacy are excluded.
    """
    with pytest.raises(TypeError):
        SUT("v", "i", "c", VerificationStatus.VERIFIED, ["a"], "p")  # type: ignore[arg-type]
    for identifiers in (("b", "a"), ("a", "a")):
        with pytest.raises(ValueError):
            SUT("v", "i", "c", VerificationStatus.VERIFIED, identifiers, "p")


def test_field__status_values__remain_non_scientific_states() -> None:
    """Evidence ID
    SV-PROV-036
    Requirement
    Status values are exactly verified, rejected, unavailable and remain distinct from
    installation state.
    Method
    Enumerate the complete public enum vocabulary.
    Oracle
    The accepted version-1 VerificationStatus fixes exact values.
    Acceptance
    The enum tuple matches exactly.
    Interpretation
    Failure indicates lifecycle vocabulary drift.
    Limitations
    VERIFIED is not numerical or scientific acceptance.
    """
    assert tuple(item.value for item in VerificationStatus) == (
        "verified",
        "rejected",
        "unavailable",
    )
