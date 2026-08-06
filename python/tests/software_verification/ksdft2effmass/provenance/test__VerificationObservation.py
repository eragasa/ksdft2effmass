r"""Software verification of ``VerificationObservation``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies verification field mapping, lifecycle meaning, enum typing, canonical evidence tuples, rejection, immutability, and equality..

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``VerificationObservation``; collaborators only supply public constructor
inputs or expose declared Python value semantics. Oracles are the accepted
field, enum, dataclass, tuple, and exception contracts. Values are synthetic,
dimensionless metadata at ordinary lexical scales; no warnings are expected.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the stated software contract. Failure indicates a
production, test-input, or accepted-contract mismatch. This evidence does not
establish numerical verification, physical correctness, scientific validation,
uncertainty quantification, portability, or cross-language agreement.
"""

# ruff: noqa: E501

from dataclasses import FrozenInstanceError, astuple, fields
from typing import Any, cast

import pytest

from ksdft2effmass.provenance import VerificationObservation, VerificationStatus

SUT = VerificationObservation
pytestmark = pytest.mark.software_verification


def test_constructor__field_mapping__stores_exact_verification_metadata() -> None:
    """Evidence ID
    SV-PROV-034
    Requirement
    Verification observation stores exact correlation, status, evidence, and provenance fields.
    Method
    Construct fixed synthetic already-observed metadata.
    Oracle
    The public signature and literal tuple define exact state.
    Acceptance
    Field names and values match exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "verify-1",
        "install-1",
        "cap-1",
        VerificationStatus.VERIFIED,
        ("evidence-1", "evidence-2"),
        "prov-1",
    )
    assert tuple(f.name for f in fields(record)) == (
        "verification_id",
        "installation_id",
        "capability_id",
        "status",
        "evidence_artifact_ids",
        "provenance_id",
    )
    assert astuple(record) == (
        "verify-1",
        "install-1",
        "cap-1",
        VerificationStatus.VERIFIED,
        ("evidence-1", "evidence-2"),
        "prov-1",
    )
    assert type(record.status) is VerificationStatus
    assert type(record.evidence_artifact_ids) is tuple


@pytest.mark.parametrize(
    "evidence_ids",
    [
        pytest.param((), id="empty_evidence_tuple"),
        pytest.param(("evidence-1",), id="singleton_evidence_tuple"),
        pytest.param(("evidence-1", "evidence-2"), id="sorted_pair_evidence_tuple"),
    ],
)
def test_constructor__evidence_identifiers__accepts_canonical_tuples(
    evidence_ids: tuple[str, ...],
) -> None:
    """Evidence ID
    SV-PROV-035
    Requirement
    Evidence identifiers accept empty and unique lexically sorted built-in tuples.
    Method
    Construct each explicit canonical cardinality partition.
    Oracle
    The accepted tuple invariant supplies exact accepted states.
    Acceptance
    Each tuple is retained exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    assert (
        SUT(
            "verify-1",
            "install-1",
            "cap-1",
            VerificationStatus.VERIFIED,
            evidence_ids,
            "prov-1",
        ).evidence_artifact_ids
        == evidence_ids
    )


@pytest.mark.parametrize(
    "evidence_ids",
    [
        pytest.param(["evidence-1"], id="list_container"),
        pytest.param((1,), id="integer_member"),
        pytest.param(("evidence-2", "evidence-1"), id="reverse_order"),
        pytest.param(("evidence-1", "evidence-1"), id="duplicate_member"),
    ],
)
def test_constructor__evidence_identifiers__rejects_noncanonical_state(
    evidence_ids: object,
) -> None:
    """Evidence ID
    SV-PROV-211
    Requirement
    Evidence identifiers require a built-in tuple of valid unique lexically sorted strings.
    Method
    Construct explicit container, member, order, and duplicate rejection partitions.
    Oracle
    The accepted semantic types and canonical tuple relation determine errors.
    Acceptance
    Container/member type cases raise TypeError; relational cases raise ValueError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    error = (
        TypeError
        if type(evidence_ids) is not tuple
        or any(type(x) is not str for x in evidence_ids)
        else ValueError
    )
    with pytest.raises(error):
        SUT(
            "verify-1",
            "install-1",
            "cap-1",
            VerificationStatus.VERIFIED,
            cast(Any, evidence_ids),
            "prov-1",
        )


def test_constructor__status_semantic_type__rejects_string_lookalike() -> None:
    """Evidence ID
    SV-PROV-212
    Requirement
    Verification status requires a VerificationStatus member.
    Method
    Pass the wire string lookalike.
    Oracle
    The accepted semantic type is the public enum.
    Acceptance
    Construction raises TypeError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(TypeError):
        SUT("verify-1", "install-1", "cap-1", cast(Any, "verified"), (), "prov-1")


def test_constructor__identifier_type_and_value__reject_invalid_state() -> None:
    """Evidence ID
    SV-PROV-213
    Requirement
    Verification identifiers require exact built-in portable strings.
    Method
    Exercise a bytes wrong-type partition and embedded-space malformed partition.
    Oracle
    The public type and identifier grammar determine exceptions.
    Acceptance
    Bytes raises TypeError and malformed text raises ValueError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(TypeError):
        SUT(
            cast(Any, b"verify"),
            "install-1",
            "cap-1",
            VerificationStatus.VERIFIED,
            (),
            "prov-1",
        )
    with pytest.raises(ValueError):
        SUT("bad id", "install-1", "cap-1", VerificationStatus.VERIFIED, (), "prov-1")


def test_field__lifecycle_status__remains_capability_observation_only() -> None:
    """Evidence ID
    SV-PROV-214
    Requirement
    VERIFIED denotes observed software capability, not execution completion or scientific acceptance.
    Method
    Inspect the record field inventory for execution and scientific acceptance state.
    Oracle
    The lifecycle contract contains only verification status and evidence references.
    Acceptance
    Execution result, convergence, and acceptance fields are absent.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    assert {f.name for f in fields(SUT)}.isdisjoint(
        {"result_id", "failure_id", "converged", "scientifically_accepted"}
    )


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID
    SV-PROV-215
    Requirement
    Verification observations are frozen.
    Method
    Assign status after construction.
    Oracle
    Frozen dataclass semantics require FrozenInstanceError.
    Acceptance
    Assignment raises FrozenInstanceError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "verify-1",
        "install-1",
        "cap-1",
        VerificationStatus.VERIFIED,
        ("evidence-1", "evidence-2"),
        "prov-1",
    )
    with pytest.raises(FrozenInstanceError):
        field_name = "status"
        setattr(record, field_name, VerificationStatus.REJECTED)


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID
    SV-PROV-216
    Requirement
    Equality covers complete verification state.
    Method
    Compare identical records and one status-different record.
    Oracle
    Dataclass full-state equality is the oracle.
    Acceptance
    Identical state is equal and one-field-different state is unequal.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "verify-1",
        "install-1",
        "cap-1",
        VerificationStatus.VERIFIED,
        ("evidence-1", "evidence-2"),
        "prov-1",
    )
    assert record == SUT(
        "verify-1",
        "install-1",
        "cap-1",
        VerificationStatus.VERIFIED,
        ("evidence-1", "evidence-2"),
        "prov-1",
    )
    assert record != SUT(
        "verify-1",
        "install-1",
        "cap-1",
        VerificationStatus.REJECTED,
        ("evidence-1", "evidence-2"),
        "prov-1",
    )
