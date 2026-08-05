"""Evidence class and represented meaning
Software verification of immutable structured external-operation failures.
Owned contract, oracle, and scope
ExternalExecutionFailure is the SUT; attempt correlation, stage/code, safe diagnostic
paths, and provenance are the oracle.
VVUQ and scientific exclusions
Evidence performs no external fault injection and excludes numerical verification,
scientific validation, UQ, and cross-language conformance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.provenance import (
    ExternalExecutionFailure,
    ExternalFailureCode,
    ExternalFailureStage,
)

SUT = ExternalExecutionFailure
pytestmark = pytest.mark.software_verification


def test_constructor__structured_failure_fields__maps_attempt_without_raw_message() -> (
    None
):
    """Evidence ID
    SV-PROV-043
    Requirement
    Failure identity, request/correlation/attempt, structured stage/code, diagnostic
    paths, and provenance map exactly with no raw message.
    Method
    Construct one result-capture failure and inspect every field plus field inventory.
    Oracle
    The corrected eight-field safe failure contract fixes exact values.
    Acceptance
    Values match and the dataclass has no message/detail field.
    Interpretation
    Failure indicates structured failure, attempt correlation, or raw-text leakage.
    Limitations
    The synthetic failure validates no dependency.
    """
    value = SUT(
        "failure-1",
        "request-1",
        "correlation-1",
        "attempt-1",
        ExternalFailureStage.RESULT_CAPTURE,
        ExternalFailureCode.MALFORMED_RESULT,
        ("logs/stderr.txt",),
        "prov-1",
    )
    assert (
        value.failure_id,
        value.request_id,
        value.correlation_id,
        value.attempt_id,
        value.stage,
        value.code,
        value.diagnostic_paths,
        value.provenance_id,
    ) == (
        "failure-1",
        "request-1",
        "correlation-1",
        "attempt-1",
        ExternalFailureStage.RESULT_CAPTURE,
        ExternalFailureCode.MALFORMED_RESULT,
        ("logs/stderr.txt",),
        "prov-1",
    )
    assert "message" not in {field.name for field in fields(SUT)}


def test_constructor__stage_code_and_paths__rejects_invalid_forms() -> None:
    """Evidence ID
    SV-PROV-044
    Requirement
    Stage/code are exact enums and diagnostic paths are sorted unique root-relative
    POSIX tuples.
    Method
    Pass string enum, list paths, unsorted paths, and absolute paths.
    Oracle
    Public typing and lexical path/tuple contracts define rejection.
    Acceptance
    String/list cases raise TypeError and invalid paths/order raise ValueError.
    Interpretation
    Failure indicates unstructured or nonportable durable failure state.
    Limitations
    Diagnostic contents and existence are excluded.
    """
    with pytest.raises(TypeError):
        SUT("f", "r", "c", "a", "execution", ExternalFailureCode.REJECTED, (), "p")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(
            "f",
            "r",
            "c",
            "a",
            ExternalFailureStage.EXECUTION,
            ExternalFailureCode.REJECTED,
            [],  # type: ignore[arg-type]
            "p",
        )
    for paths in (("z/log", "a/log"), ("/absolute",), ("diag\\stderr.txt",)):
        with pytest.raises(ValueError):
            SUT(
                "f",
                "r",
                "c",
                "a",
                ExternalFailureStage.EXECUTION,
                ExternalFailureCode.REJECTED,
                paths,
                "p",
            )


def test_field__failure_enum_values__match_version_one_taxonomy() -> None:
    """Evidence ID
    SV-PROV-045
    Requirement
    Stage and code enums expose the complete exact version-1 failure taxonomy.
    Method
    Enumerate both public enum artifacts.
    Oracle
    The accepted schema vocabulary fixes strings and order.
    Acceptance
    Both tuples match exactly.
    Interpretation
    Failure indicates structured vocabulary drift.
    Limitations
    Adapter classification quality is excluded.
    """
    assert tuple(item.value for item in ExternalFailureStage) == (
        "request_acceptance",
        "execution",
        "result_capture",
    )
    assert tuple(item.value for item in ExternalFailureCode) == (
        "unavailable",
        "not_authorized",
        "rejected",
        "interrupted",
        "malformed_result",
        "internal_error",
    )
