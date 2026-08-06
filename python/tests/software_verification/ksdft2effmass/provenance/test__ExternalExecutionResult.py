r"""Software verification of ``ExternalExecutionResult``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies successful outcome mapping, canonical outputs,
enum typing, lifecycle distinctions, the explicitly approved internal outcome-alias
decomposition, immutability, and equality.

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT and evidence owner is ``ExternalExecutionResult``. The
``ExternalExecutionOutcome`` typing alias is an internal defining-module
collaborator used only to expose the approved result/failure decomposition; it is
not a package export or separate public owner. ``ExternalExecutionFailure`` is
the other represented-family collaborator. Oracles are the accepted field,
enum, dataclass, tuple, and internal decomposition contracts. Values are
synthetic, dimensionless metadata at ordinary lexical scales; no warnings are
expected.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the stated software contract. Failure indicates a
production, test-input, or accepted-contract mismatch. This evidence does not
establish numerical verification, physical correctness, scientific validation,
uncertainty quantification, portability, or cross-language agreement.
"""

# ruff: noqa: E501

from dataclasses import FrozenInstanceError, astuple, fields
from typing import Any, cast, get_args

import pytest

from ksdft2effmass.provenance import (
    ExternalExecutionFailure,
    ExternalExecutionResult,
    ExternalExecutionStatus,
)
from ksdft2effmass.provenance.external_execution import ExternalExecutionOutcome

SUT = ExternalExecutionResult
pytestmark = pytest.mark.software_verification


def test_constructor__field_mapping__stores_exact_completed_outcome() -> None:
    """Evidence ID
    SV-PROV-040
    Requirement
    Successful outcome stores eight exact correlated fields.
    Method
    Construct fixed already-observed boundary completion metadata.
    Oracle
    The accepted signature and literals define field state.
    Acceptance
    Names and values match exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "result-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        ("output-1", "output-2"),
        "manifest-1",
        "prov-1",
    )
    assert tuple(f.name for f in fields(record)) == (
        "result_id",
        "request_id",
        "correlation_id",
        "attempt_id",
        "status",
        "output_artifact_ids",
        "manifest_id",
        "provenance_id",
    )
    assert astuple(record) == (
        "result-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        ("output-1", "output-2"),
        "manifest-1",
        "prov-1",
    )
    assert type(record.status) is ExternalExecutionStatus
    assert type(record.output_artifact_ids) is tuple


@pytest.mark.parametrize(
    "outputs",
    [
        pytest.param((), id="empty_outputs"),
        pytest.param(("output-1",), id="singleton_outputs"),
        pytest.param(("output-1", "output-2"), id="sorted_output_pair"),
    ],
)
def test_constructor__output_artifact_ids__accepts_canonical_tuples(
    outputs: tuple[str, ...],
) -> None:
    """Evidence ID
    SV-PROV-041
    Requirement
    Output identifiers accept empty and unique sorted built-in tuples.
    Method
    Construct explicit canonical cardinality partitions.
    Oracle
    The accepted tuple invariant defines exact states.
    Acceptance
    Each tuple is preserved exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    assert (
        SUT(
            "result-1",
            "request-1",
            "corr-1",
            "attempt-1",
            ExternalExecutionStatus.COMPLETED,
            outputs,
            "manifest-1",
            "prov-1",
        ).output_artifact_ids
        == outputs
    )


@pytest.mark.parametrize(
    ("outputs", "error"),
    [
        pytest.param(["output-1"], TypeError, id="list_container"),
        pytest.param((1,), TypeError, id="integer_member"),
        pytest.param(("output-2", "output-1"), ValueError, id="reverse_order"),
        pytest.param(("output-1", "output-1"), ValueError, id="duplicate_output"),
    ],
)
def test_constructor__output_artifact_ids__rejects_noncanonical_state(
    outputs: object, error: type[Exception]
) -> None:
    """Evidence ID
    SV-PROV-222
    Requirement
    Output identifiers require a built-in tuple of valid unique sorted strings.
    Method
    Exercise explicit container, member, order, and duplicate partitions.
    Oracle
    The accepted type and canonical relation contracts determine exceptions.
    Acceptance
    Every partition raises its declared exception.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(error):
        SUT(
            "result-1",
            "request-1",
            "corr-1",
            "attempt-1",
            ExternalExecutionStatus.COMPLETED,
            cast(Any, outputs),
            "manifest-1",
            "prov-1",
        )


def test_constructor__status_semantic_type__rejects_string_lookalike() -> None:
    """Evidence ID
    SV-PROV-223
    Requirement
    Result status requires an ExternalExecutionStatus member.
    Method
    Pass the completed wire string lookalike.
    Oracle
    The accepted semantic enum type excludes raw strings.
    Acceptance
    Construction raises TypeError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(TypeError):
        SUT(
            "result-1",
            "request-1",
            "corr-1",
            "attempt-1",
            cast(Any, "completed"),
            (),
            "manifest-1",
            "prov-1",
        )


def test_constructor__identifier_type_and_value__reject_invalid_state() -> None:
    """Evidence ID
    SV-PROV-224
    Requirement
    Result identifiers require exact built-in portable strings.
    Method
    Exercise bytes and embedded-space result identifiers.
    Oracle
    The accepted type and lexical contracts determine exceptions.
    Acceptance
    Bytes raises TypeError and malformed text raises ValueError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(TypeError):
        SUT(
            cast(Any, b"result"),
            "request-1",
            "corr-1",
            "attempt-1",
            ExternalExecutionStatus.COMPLETED,
            (),
            "manifest-1",
            "prov-1",
        )
    with pytest.raises(ValueError):
        SUT(
            "bad id",
            "request-1",
            "corr-1",
            "attempt-1",
            ExternalExecutionStatus.COMPLETED,
            (),
            "manifest-1",
            "prov-1",
        )


def test_field__completion_lifecycle__excludes_convergence_and_acceptance() -> None:
    """Evidence ID
    SV-PROV-225
    Requirement
    COMPLETED records boundary completion only, not solver convergence or scientific acceptance.
    Method
    Inspect public field inventory for scientific conclusion fields.
    Oracle
    The accepted lifecycle distinction excludes converged and scientifically_accepted.
    Acceptance
    Those fields are absent.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    assert {f.name for f in fields(SUT)}.isdisjoint(
        {"converged", "numerically_accepted", "scientifically_accepted"}
    )


def test_field__external_execution_outcome_alias__accepts_result_and_failure_families() -> (
    None
):
    """Evidence ID
    SV-PROV-226
    Requirement
    The explicitly approved internal defining-module ExternalExecutionOutcome typing alias admits exactly result and structured-failure record families.
    Method
    Inspect the internal typing-alias union arguments as collaborator evidence while retaining ExternalExecutionResult as the sole SUT and owner.
    Oracle
    The approved internal decomposition names ExternalExecutionResult and ExternalExecutionFailure and does not make the alias a package export.
    Acceptance
    Union arguments equal those two classes in declaration order.
    Interpretation
    A pass confirms the approved internal decomposition under the ExternalExecutionResult owner; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    The alias is not a package export or separate public owner; this synthetic evidence makes no external-execution, numerical-verification, scientific-validation, UQ, portability, or cross-language claim.
    """
    assert get_args(ExternalExecutionOutcome) == (
        ExternalExecutionResult,
        ExternalExecutionFailure,
    )


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID
    SV-PROV-227
    Requirement
    Execution results are frozen.
    Method
    Attempt status assignment.
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
        "result-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        ("output-1", "output-2"),
        "manifest-1",
        "prov-1",
    )
    with pytest.raises(FrozenInstanceError):
        field_name = "status"
        setattr(record, field_name, ExternalExecutionStatus.COMPLETED)


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID
    SV-PROV-228
    Requirement
    Equality covers complete result state.
    Method
    Compare identical records and one differing in manifest identity.
    Oracle
    Dataclass full-state equality defines exact behavior.
    Acceptance
    Identical records compare equal and one-field difference compares unequal.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "result-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        ("output-1", "output-2"),
        "manifest-1",
        "prov-1",
    )
    assert record == SUT(
        "result-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        ("output-1", "output-2"),
        "manifest-1",
        "prov-1",
    )
    assert record != SUT(
        "result-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        ("output-1", "output-2"),
        "manifest-2",
        "prov-1",
    )


def test_field__durable_surface__excludes_runtime_credentials_and_handles() -> None:
    """Evidence ID
    SV-PROV-229
    Requirement
    Result records contain no runtime credentials or handles.
    Method
    Inspect field names against prohibited runtime state.
    Oracle
    The accepted durable boundary excludes command, credential, client, process, scheduler, and handle.
    Acceptance
    The sets are disjoint.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    assert {f.name for f in fields(SUT)}.isdisjoint(
        {"command", "credential", "client", "process", "scheduler", "handle"}
    )
