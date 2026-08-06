r"""Software verification of ``ExternalExecutionFailure``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies structured failure mapping, semantic enums, canonical diagnostic paths, lifecycle separation, strict rejection, immutability, and equality..

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``ExternalExecutionFailure``; collaborators only supply public constructor
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

from ksdft2effmass.provenance import (
    ExternalExecutionFailure,
    ExternalFailureCode,
    ExternalFailureStage,
)

SUT = ExternalExecutionFailure
pytestmark = pytest.mark.software_verification


def test_constructor__field_mapping__stores_exact_structured_failure() -> None:
    """Evidence ID
    SV-PROV-043
    Requirement
    Failure construction stores eight exact structured fields without a raw message.
    Method
    Construct fixed already-observed structured failure metadata.
    Oracle
    The accepted signature and literals define exact field state.
    Acceptance
    Names and values match exactly and message is absent.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "failure-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalFailureStage.EXECUTION,
        ExternalFailureCode.INTERRUPTED,
        ("diagnostics/stderr.txt", "diagnostics/stdout.txt"),
        "prov-1",
    )
    assert tuple(f.name for f in fields(record)) == (
        "failure_id",
        "request_id",
        "correlation_id",
        "attempt_id",
        "stage",
        "code",
        "diagnostic_paths",
        "provenance_id",
    )
    assert astuple(record) == (
        "failure-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalFailureStage.EXECUTION,
        ExternalFailureCode.INTERRUPTED,
        ("diagnostics/stderr.txt", "diagnostics/stdout.txt"),
        "prov-1",
    )
    assert type(record.stage) is ExternalFailureStage
    assert type(record.code) is ExternalFailureCode
    assert type(record.diagnostic_paths) is tuple
    assert "message" not in {f.name for f in fields(record)}


@pytest.mark.parametrize(
    "paths",
    [
        pytest.param((), id="empty_paths"),
        pytest.param(("diagnostics/stderr.txt",), id="singleton_path"),
        pytest.param(
            ("diagnostics/stderr.txt", "diagnostics/stdout.txt"), id="sorted_path_pair"
        ),
    ],
)
def test_constructor__diagnostic_paths__accepts_canonical_root_relative_tuples(
    paths: tuple[str, ...],
) -> None:
    """Evidence ID
    SV-PROV-044
    Requirement
    Diagnostic paths accept empty and unique sorted root-relative POSIX tuples.
    Method
    Construct explicit canonical cardinality partitions.
    Oracle
    The accepted root-relative lexical path and tuple invariants define states.
    Acceptance
    Each path tuple is preserved exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    assert (
        SUT(
            "failure-1",
            "request-1",
            "corr-1",
            "attempt-1",
            ExternalFailureStage.EXECUTION,
            ExternalFailureCode.INTERRUPTED,
            paths,
            "prov-1",
        ).diagnostic_paths
        == paths
    )


@pytest.mark.parametrize(
    ("paths", "error"),
    [
        pytest.param(["diagnostics/a"], TypeError, id="list_container"),
        pytest.param((1,), TypeError, id="integer_member"),
        pytest.param(("/absolute",), ValueError, id="absolute_path"),
        pytest.param(("a/../b",), ValueError, id="parent_component"),
        pytest.param(("b", "a"), ValueError, id="reverse_order"),
        pytest.param(("a", "a"), ValueError, id="duplicate_path"),
    ],
)
def test_constructor__diagnostic_paths__rejects_noncanonical_state(
    paths: object, error: type[Exception]
) -> None:
    """Evidence ID
    SV-PROV-230
    Requirement
    Diagnostic paths require a built-in tuple of valid unique sorted root-relative POSIX strings.
    Method
    Exercise container, member, absolute, parent-component, order, and duplicate partitions.
    Oracle
    The accepted type, path grammar, and canonical relation determine errors.
    Acceptance
    Every partition raises its exact declared exception.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(error):
        SUT(
            "failure-1",
            "request-1",
            "corr-1",
            "attempt-1",
            ExternalFailureStage.EXECUTION,
            ExternalFailureCode.INTERRUPTED,
            cast(Any, paths),
            "prov-1",
        )


@pytest.mark.parametrize(
    ("stage", "code"),
    [
        pytest.param(
            "execution", ExternalFailureCode.INTERRUPTED, id="stage_string_lookalike"
        ),
        pytest.param(
            ExternalFailureStage.EXECUTION, "interrupted", id="code_string_lookalike"
        ),
    ],
)
def test_constructor__failure_enums__rejects_string_lookalikes(
    stage: object, code: object
) -> None:
    """Evidence ID
    SV-PROV-231
    Requirement
    Failure stage and code require their exact semantic enum classes.
    Method
    Replace each enum member with its wire string under explicit IDs.
    Oracle
    The public semantic type contract excludes raw strings.
    Acceptance
    Every partition raises TypeError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(TypeError):
        SUT(
            "failure-1",
            "request-1",
            "corr-1",
            "attempt-1",
            cast(Any, stage),
            cast(Any, code),
            (),
            "prov-1",
        )


def test_constructor__identifier_type_and_value__reject_invalid_state() -> None:
    """Evidence ID
    SV-PROV-232
    Requirement
    Failure identifiers require exact built-in portable strings.
    Method
    Exercise bytes and embedded-space failure identifiers.
    Oracle
    The accepted type and lexical contracts determine errors.
    Acceptance
    Bytes raises TypeError and malformed text raises ValueError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(TypeError):
        SUT(
            cast(Any, b"failure"),
            "request-1",
            "corr-1",
            "attempt-1",
            ExternalFailureStage.EXECUTION,
            ExternalFailureCode.INTERRUPTED,
            (),
            "prov-1",
        )
    with pytest.raises(ValueError):
        SUT(
            "bad id",
            "request-1",
            "corr-1",
            "attempt-1",
            ExternalFailureStage.EXECUTION,
            ExternalFailureCode.INTERRUPTED,
            (),
            "prov-1",
        )


def test_field__failure_lifecycle__remains_distinct_from_completed_result() -> None:
    """Evidence ID
    SV-PROV-233
    Requirement
    A structured failure has stage and code but no completed status, outputs, or manifest.
    Method
    Inspect the public field inventory.
    Oracle
    The accepted outcome families have disjoint success/failure-specific fields.
    Acceptance
    Failure fields are present and result-only fields absent.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    names = {f.name for f in fields(SUT)}
    assert {"stage", "code", "diagnostic_paths"} <= names
    assert names.isdisjoint({"status", "output_artifact_ids", "manifest_id"})


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID
    SV-PROV-234
    Requirement
    Execution failures are frozen.
    Method
    Attempt stage assignment after construction.
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
        "failure-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalFailureStage.EXECUTION,
        ExternalFailureCode.INTERRUPTED,
        ("diagnostics/stderr.txt", "diagnostics/stdout.txt"),
        "prov-1",
    )
    with pytest.raises(FrozenInstanceError):
        field_name = "stage"
        setattr(record, field_name, ExternalFailureStage.RESULT_CAPTURE)


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID
    SV-PROV-235
    Requirement
    Equality covers complete failure state.
    Method
    Compare identical records and one differing in code.
    Oracle
    Dataclass full-state equality defines exact behavior.
    Acceptance
    Identical state is equal and one-field difference is unequal.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "failure-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalFailureStage.EXECUTION,
        ExternalFailureCode.INTERRUPTED,
        ("diagnostics/stderr.txt", "diagnostics/stdout.txt"),
        "prov-1",
    )
    assert record == SUT(
        "failure-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalFailureStage.EXECUTION,
        ExternalFailureCode.INTERRUPTED,
        ("diagnostics/stderr.txt", "diagnostics/stdout.txt"),
        "prov-1",
    )
    assert record != SUT(
        "failure-1",
        "request-1",
        "corr-1",
        "attempt-1",
        ExternalFailureStage.EXECUTION,
        ExternalFailureCode.INTERNAL_ERROR,
        ("diagnostics/stderr.txt", "diagnostics/stdout.txt"),
        "prov-1",
    )


def test_field__durable_surface__excludes_raw_runtime_and_credentials() -> None:
    """Evidence ID
    SV-PROV-236
    Requirement
    Structured failure stores diagnostic references but no raw runtime, credential, or handle state.
    Method
    Inspect field names against prohibited runtime vocabulary.
    Oracle
    The accepted durable boundary excludes message, traceback, command, credential, client, process, scheduler, and handle.
    Acceptance
    The sets are disjoint.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    assert {f.name for f in fields(SUT)}.isdisjoint(
        {
            "message",
            "traceback",
            "command",
            "credential",
            "client",
            "process",
            "scheduler",
            "handle",
        }
    )
