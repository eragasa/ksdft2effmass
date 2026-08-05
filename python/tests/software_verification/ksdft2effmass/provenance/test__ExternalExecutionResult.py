"""Evidence class and represented meaning
Software verification of immutable successful external-boundary outcomes.
Owned contract, oracle, and scope
ExternalExecutionResult is the SUT; exact request/correlation/attempt fields, canonical
outputs, and completed status are the oracle.
VVUQ and scientific exclusions
Evidence excludes solver convergence, numerical verification, scientific validation, UQ,
and cross-language conformance.
"""

import pytest

from ksdft2effmass.provenance import ExternalExecutionResult, ExternalExecutionStatus

SUT = ExternalExecutionResult
pytestmark = pytest.mark.software_verification


def test_constructor__result_correlation_and_provenance__maps_attempt_fields() -> None:
    """Evidence ID
    SV-PROV-040
    Requirement
    Result identity, request/correlation/attempt identities, status, outputs, manifest,
    and provenance map exactly.
    Method
    Construct a completed synthetic outcome and inspect every field.
    Oracle
    The corrected eight-field result vocabulary independently fixes expected values.
    Acceptance
    The complete field tuple equals the supplied values.
    Interpretation
    Failure indicates attempt correlation or provenance mapping drift.
    Limitations
    COMPLETED means boundary completion only.
    """
    value = SUT(
        "result-1",
        "request-1",
        "correlation-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        ("output-a",),
        "manifest-1",
        "prov-1",
    )
    assert (
        value.result_id,
        value.request_id,
        value.correlation_id,
        value.attempt_id,
        value.status,
        value.output_artifact_ids,
        value.manifest_id,
        value.provenance_id,
    ) == (
        "result-1",
        "request-1",
        "correlation-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        ("output-a",),
        "manifest-1",
        "prov-1",
    )


def test_constructor__status_and_outputs__rejects_wrong_or_noncanonical_values() -> (
    None
):
    """Evidence ID
    SV-PROV-041
    Requirement
    Attempt is a portable identifier, status is the exact enum, and outputs are a
    canonical tuple.
    Method
    Pass empty attempt, string status, list outputs, and unsorted outputs.
    Oracle
    Public typing and canonical tuple invariants define rejection.
    Acceptance
    Wrong types raise TypeError and invalid values/order raise ValueError.
    Interpretation
    Failure indicates coercion or nondeterministic result state.
    Limitations
    Artifact existence is excluded.
    """
    with pytest.raises(ValueError):
        SUT("x", "r", "c", "", ExternalExecutionStatus.COMPLETED, (), "m", "p")
    with pytest.raises(TypeError):
        SUT("x", "r", "c", "a", "completed", (), "m", "p")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("x", "r", "c", "a", ExternalExecutionStatus.COMPLETED, ["a"], "m", "p")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("x", "r", "c", "a", ExternalExecutionStatus.COMPLETED, ("b", "a"), "m", "p")


def test_field__completed_enum_value__is_boundary_status_only() -> None:
    """Evidence ID
    SV-PROV-042
    Requirement
    Successful-boundary status contains exactly completed.
    Method
    Enumerate public ExternalExecutionStatus values.
    Oracle
    The accepted version-1 enum fixes one exact string.
    Acceptance
    The tuple is exactly ('completed',).
    Interpretation
    Failure indicates lifecycle vocabulary drift.
    Limitations
    Completion is not convergence or acceptance.
    """
    assert tuple(item.value for item in ExternalExecutionStatus) == ("completed",)
