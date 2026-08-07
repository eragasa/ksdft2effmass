r"""Software verification of ``ExternalExecutionFailure``.

Facet and represented meaning
-----------------------------
This class-owned software evidence verifies exact eight-field construction,
correlated identifiers, exact stage and code typing, canonical diagnostic-path
tuples, diagnostic-path lexical safety, frozen state, equality, result/failure
lifecycle separation, and durable structured-failure boundaries.

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``ExternalExecutionFailure``. The record stores an
already-observed external operational failure. Public constructor inputs,
dataclass semantics, and fixed valid or invalid literals provide the oracles.
It does not execute a request, expose raw diagnostics, authorize retry, or
establish that retry is safe.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the stated structured-failure software behavior;
failure identifies a production, test-input, oracle, or accepted-contract
mismatch. The record does not classify numerical discretization error or model
inadequacy and does not establish scientific invalidity, UQ, provenance truth,
physical correctness, portability, or cross-language agreement.
"""

from dataclasses import FrozenInstanceError, astuple, fields
from typing import Any

import pytest

from ksdft2effmass.provenance import (
    ExternalExecutionFailure,
    ExternalFailureCode,
    ExternalFailureStage,
)

SUT = ExternalExecutionFailure
pytestmark = pytest.mark.software_verification

IDENTIFIER_FIELDS = (
    "failure_id",
    "request_id",
    "correlation_id",
    "attempt_id",
    "provenance_id",
)
PUBLIC_FIELDS = (
    "failure_id",
    "request_id",
    "correlation_id",
    "attempt_id",
    "stage",
    "code",
    "diagnostic_paths",
    "provenance_id",
)
FROZEN_FIELDS = (
    "failure_id",
    "request_id",
    "correlation_id",
    "attempt_id",
    "stage",
    "code",
    "diagnostic_paths",
    "provenance_id",
)
EQUALITY_FIELDS = (
    "failure_id",
    "request_id",
    "correlation_id",
    "attempt_id",
    "stage",
    "code",
    "diagnostic_paths",
    "provenance_id",
)


def make_external_execution_failure(**overrides: Any) -> ExternalExecutionFailure:
    """Evidence ID
    Owns no identifier; supports all evidence in this module.
    Requirement
    Failure tests need valid baseline state with explicit one-field overrides.
    Method
    Merge named overrides into fixed synthetic values and call the public constructor.
    Oracle
    The accepted constructor signature and independently valid literals define setup.
    Acceptance
    Return the constructor result without assertions, normalization, or I/O.
    Interpretation
    The helper isolates one field while every unselected failure field remains valid.
    Limitations
    This helper owns no evidence result and contains no hidden oracle.
    """
    values: dict[str, Any] = {
        "failure_id": "failure-1",
        "request_id": "request-1",
        "correlation_id": "correlation-1",
        "attempt_id": "attempt-1",
        "stage": ExternalFailureStage.EXECUTION,
        "code": ExternalFailureCode.INTERRUPTED,
        "diagnostic_paths": (
            "diagnostics/stderr.txt",
            "diagnostics/stdout.txt",
        ),
        "provenance_id": "provenance-1",
    }
    values.update(overrides)
    return ExternalExecutionFailure(**values)


def test_constructor__field_mapping__stores_exact_values_types_and_order() -> None:
    """
    Evidence ID
    SV-PROV-043
    Requirement
    Construction stores exact eight-field structured-failure state without coercion.
    Method
    Construct baseline state and inspect public order, values, exact types, and
    raw-field absence.
    Oracle
    The accepted public inventory and fixed literals define expected represented
    state.
    Acceptance
    Order and values match exactly; stored types match the declared eight positions;
    message and traceback are absent.
    Interpretation
    Passing establishes exact constructor mapping, stored types, and the
    structured-reference boundary.
    Limitations
    Construction neither reads diagnostics nor establishes provenance truth.
    """
    record = make_external_execution_failure()
    assert tuple(field.name for field in fields(record)) == PUBLIC_FIELDS
    assert astuple(record) == (
        "failure-1",
        "request-1",
        "correlation-1",
        "attempt-1",
        ExternalFailureStage.EXECUTION,
        ExternalFailureCode.INTERRUPTED,
        ("diagnostics/stderr.txt", "diagnostics/stdout.txt"),
        "provenance-1",
    )
    assert tuple(type(value) for value in astuple(record)) == (
        str,
        str,
        str,
        str,
        ExternalFailureStage,
        ExternalFailureCode,
        tuple,
        str,
    )
    assert type(record.stage) is ExternalFailureStage
    assert type(record.code) is ExternalFailureCode
    assert type(record.diagnostic_paths) is tuple
    assert {"message", "traceback"}.isdisjoint(PUBLIC_FIELDS)


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "failure_id", "failure-ordinary", id="failure_id_ordinary_valid_identifier"
        ),
        pytest.param("failure_id", "a", id="failure_id_minimum_length_1"),
        pytest.param("failure_id", "a" * 128, id="failure_id_maximum_length_128"),
        pytest.param(
            "request_id", "request-ordinary", id="request_id_ordinary_valid_identifier"
        ),
        pytest.param("request_id", "a", id="request_id_minimum_length_1"),
        pytest.param("request_id", "a" * 128, id="request_id_maximum_length_128"),
        pytest.param(
            "correlation_id",
            "correlation-ordinary",
            id="correlation_id_ordinary_valid_identifier",
        ),
        pytest.param("correlation_id", "a", id="correlation_id_minimum_length_1"),
        pytest.param(
            "correlation_id", "a" * 128, id="correlation_id_maximum_length_128"
        ),
        pytest.param(
            "attempt_id", "attempt-ordinary", id="attempt_id_ordinary_valid_identifier"
        ),
        pytest.param("attempt_id", "a", id="attempt_id_minimum_length_1"),
        pytest.param("attempt_id", "a" * 128, id="attempt_id_maximum_length_128"),
        pytest.param(
            "provenance_id",
            "provenance-ordinary",
            id="provenance_id_ordinary_valid_identifier",
        ),
        pytest.param("provenance_id", "a", id="provenance_id_minimum_length_1"),
        pytest.param("provenance_id", "a" * 128, id="provenance_id_maximum_length_128"),
    ],
)
def test_constructor__identifiers__accept_valid_length_partitions(
    field_name: str, value: str
) -> None:
    """
    Evidence ID
    SV-PROV-333
    Requirement
    Every correlated identifier accepts ordinary portable text and lengths 1 and
    128.
    Method
    Override one field for each explicit field-and-length partition.
    Oracle
    The accepted grammar permits 1 through 128 portable ASCII characters.
    Acceptance
    Construction succeeds and stores the selected value unchanged.
    Interpretation
    Passing establishes accepted lexical-length partitions for all five identifiers.
    Limitations
    This lexical evidence does not establish correlation validity or provenance
    truth.
    """
    assert (
        getattr(make_external_execution_failure(**{field_name: value}), field_name)
        == value
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("failure_id", b"identifier", id="failure_id_bytes_wrong_type"),
        pytest.param("request_id", b"identifier", id="request_id_bytes_wrong_type"),
        pytest.param(
            "correlation_id", b"identifier", id="correlation_id_bytes_wrong_type"
        ),
        pytest.param("attempt_id", b"identifier", id="attempt_id_bytes_wrong_type"),
        pytest.param(
            "provenance_id", b"identifier", id="provenance_id_bytes_wrong_type"
        ),
    ],
)
def test_constructor__identifier_type__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """
    Evidence ID
    SV-PROV-232
    Requirement
    Every correlated identifier rejects a wrong semantic type.
    Method
    Override each identifier independently with the bytes wrong type partition.
    Oracle
    The accepted identifier type contract assigns TypeError to bytes.
    Acceptance
    Every field raises exactly TypeError.
    Interpretation
    Passing establishes bytes wrong type rejection for all five identifiers.
    Limitations
    Every other field remains valid; correlation meaning is outside this owner.
    """
    with pytest.raises(TypeError):
        make_external_execution_failure(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("failure_id", "", id="failure_id_empty_text"),
        pytest.param("request_id", "", id="request_id_empty_text"),
        pytest.param("correlation_id", "", id="correlation_id_empty_text"),
        pytest.param("attempt_id", "", id="attempt_id_empty_text"),
        pytest.param("provenance_id", "", id="provenance_id_empty_text"),
    ],
)
def test_constructor__identifier_empty__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """
    Evidence ID
    SV-PROV-334
    Requirement
    Every correlated identifier rejects empty text.
    Method
    Override each identifier independently with the empty text partition.
    Oracle
    The accepted nonempty invariant assigns ValueError to empty text.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes empty text rejection for all five identifiers.
    Limitations
    Every other field remains valid; correlation meaning is outside this owner.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("failure_id", "bad id", id="failure_id_embedded_space"),
        pytest.param("request_id", "bad id", id="request_id_embedded_space"),
        pytest.param("correlation_id", "bad id", id="correlation_id_embedded_space"),
        pytest.param("attempt_id", "bad id", id="attempt_id_embedded_space"),
        pytest.param("provenance_id", "bad id", id="provenance_id_embedded_space"),
    ],
)
def test_constructor__identifier_grammar__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """
    Evidence ID
    SV-PROV-335
    Requirement
    Every correlated identifier rejects embedded-space grammar.
    Method
    Override each identifier independently with the embedded space partition.
    Oracle
    The portable grammar excludes embedded spaces.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes embedded space rejection for all five identifiers.
    Limitations
    Every other field remains valid; correlation meaning is outside this owner.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("failure_id", "-leading", id="failure_id_invalid_leading_hyphen"),
        pytest.param("request_id", "-leading", id="request_id_invalid_leading_hyphen"),
        pytest.param(
            "correlation_id", "-leading", id="correlation_id_invalid_leading_hyphen"
        ),
        pytest.param("attempt_id", "-leading", id="attempt_id_invalid_leading_hyphen"),
        pytest.param(
            "provenance_id", "-leading", id="provenance_id_invalid_leading_hyphen"
        ),
    ],
)
def test_constructor__identifier_leading__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """
    Evidence ID
    SV-PROV-336
    Requirement
    Every correlated identifier rejects an invalid leading character.
    Method
    Override each identifier independently with the invalid leading hyphen
    partition.
    Oracle
    The grammar requires an ASCII alphanumeric leading character.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes invalid leading hyphen rejection for all five identifiers.
    Limitations
    Every other field remains valid; correlation meaning is outside this owner.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("failure_id", "\ud800", id="failure_id_unicode_surrogate"),
        pytest.param("request_id", "\ud800", id="request_id_unicode_surrogate"),
        pytest.param("correlation_id", "\ud800", id="correlation_id_unicode_surrogate"),
        pytest.param("attempt_id", "\ud800", id="attempt_id_unicode_surrogate"),
        pytest.param("provenance_id", "\ud800", id="provenance_id_unicode_surrogate"),
    ],
)
def test_constructor__identifier_surrogate__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """
    Evidence ID
    SV-PROV-337
    Requirement
    Every correlated identifier rejects Unicode surrogate text.
    Method
    Override each identifier independently with the unicode surrogate partition.
    Oracle
    The accepted Unicode contract excludes surrogate code points.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes unicode surrogate rejection for all five identifiers.
    Limitations
    Every other field remains valid; correlation meaning is outside this owner.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("failure_id", "e\u0301", id="failure_id_non_nfc"),
        pytest.param("request_id", "e\u0301", id="request_id_non_nfc"),
        pytest.param("correlation_id", "e\u0301", id="correlation_id_non_nfc"),
        pytest.param("attempt_id", "e\u0301", id="attempt_id_non_nfc"),
        pytest.param("provenance_id", "e\u0301", id="provenance_id_non_nfc"),
    ],
)
def test_constructor__identifier_nfc__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """
    Evidence ID
    SV-PROV-338
    Requirement
    Every correlated identifier rejects non-NFC text.
    Method
    Override each identifier independently with the non nfc partition.
    Oracle
    The accepted Unicode contract requires NFC normalization.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes non nfc rejection for all five identifiers.
    Limitations
    Every other field remains valid; correlation meaning is outside this owner.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("failure_id", "a" * 129, id="failure_id_overlength_129"),
        pytest.param("request_id", "a" * 129, id="request_id_overlength_129"),
        pytest.param("correlation_id", "a" * 129, id="correlation_id_overlength_129"),
        pytest.param("attempt_id", "a" * 129, id="attempt_id_overlength_129"),
        pytest.param("provenance_id", "a" * 129, id="provenance_id_overlength_129"),
    ],
)
def test_constructor__identifier_length__rejects_invalid_state(
    field_name: str, value: object
) -> None:
    """
    Evidence ID
    SV-PROV-339
    Requirement
    Every correlated identifier rejects text longer than 128 characters.
    Method
    Override each identifier independently with the overlength 129 partition.
    Oracle
    The accepted identifier maximum is exactly 128 characters.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes overlength 129 rejection for all five identifiers.
    Limitations
    Every other field remains valid; correlation meaning is outside this owner.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(**{field_name: value})


@pytest.mark.parametrize(
    "stage",
    [
        pytest.param(
            ExternalFailureStage.REQUEST_ACCEPTANCE,
            id="request_acceptance_exact_member",
        ),
        pytest.param(ExternalFailureStage.EXECUTION, id="execution_exact_member"),
        pytest.param(
            ExternalFailureStage.RESULT_CAPTURE, id="result_capture_exact_member"
        ),
    ],
)
def test_constructor__stage_exact_type__accepts_every_member(
    stage: ExternalFailureStage,
) -> None:
    """
    Evidence ID
    SV-PROV-340
    Requirement
    Stage accepts every exact ExternalFailureStage member.
    Method
    Vary only stage while retaining one valid baseline code.
    Oracle
    The accepted closed vocabulary declares the three exact members.
    Acceptance
    Each member is stored by identity with exact ExternalFailureStage type.
    Interpretation
    Passing establishes accepted construction for every stage member.
    Limitations
    Stage records observation location only; it does not authorize retry.
    """
    record = make_external_execution_failure(stage=stage)
    assert record.stage is stage
    assert type(record.stage) is ExternalFailureStage


@pytest.mark.parametrize(
    "stage",
    [
        pytest.param("request_acceptance", id="request_acceptance_string_lookalike"),
        pytest.param("execution", id="execution_string_lookalike"),
        pytest.param("result_capture", id="result_capture_string_lookalike"),
    ],
)
def test_constructor__stage_type__rejects_wire_string_lookalikes(stage: str) -> None:
    """
    Evidence ID
    SV-PROV-231
    Requirement
    Stage rejects every corresponding wire-string lookalike.
    Method
    Override only stage with each declared wire spelling.
    Oracle
    The semantic enum contract excludes raw strings.
    Acceptance
    Every string partition raises exactly TypeError.
    Interpretation
    Passing distinguishes all stage members from their wire spellings.
    Limitations
    This does not assess serialization or retry eligibility.
    """
    with pytest.raises(TypeError):
        make_external_execution_failure(stage=stage)


def test_constructor__stage_type__rejects_unrelated_integer() -> None:
    """
    Evidence ID
    SV-PROV-341
    Requirement
    Stage rejects an unrelated integer semantic type.
    Method
    Override only stage with integer 1.
    Oracle
    The semantic contract accepts only ExternalFailureStage members.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing isolates unrelated wrong-type rejection for stage.
    Limitations
    No stage meaning or retry decision is inferred.
    """
    with pytest.raises(TypeError):
        make_external_execution_failure(stage=1)


def test_constructor__stage_type__rejects_failure_code_member() -> None:
    """
    Evidence ID
    SV-PROV-342
    Requirement
    Stage rejects cross-enum contamination by ExternalFailureCode.
    Method
    Override only stage with ExternalFailureCode.INTERRUPTED.
    Oracle
    Distinct enum classes remain distinct despite both being StrEnum families.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing isolates cross-enum rejection at the stage field.
    Limitations
    This does not classify operational equivalence.
    """
    with pytest.raises(TypeError):
        make_external_execution_failure(stage=ExternalFailureCode.INTERRUPTED)


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(ExternalFailureCode.UNAVAILABLE, id="unavailable_exact_member"),
        pytest.param(
            ExternalFailureCode.NOT_AUTHORIZED, id="not_authorized_exact_member"
        ),
        pytest.param(ExternalFailureCode.REJECTED, id="rejected_exact_member"),
        pytest.param(ExternalFailureCode.INTERRUPTED, id="interrupted_exact_member"),
        pytest.param(
            ExternalFailureCode.MALFORMED_RESULT, id="malformed_result_exact_member"
        ),
        pytest.param(
            ExternalFailureCode.INTERNAL_ERROR, id="internal_error_exact_member"
        ),
    ],
)
def test_constructor__code_exact_type__accepts_every_member(
    code: ExternalFailureCode,
) -> None:
    """
    Evidence ID
    SV-PROV-343
    Requirement
    Code accepts every exact ExternalFailureCode member.
    Method
    Vary only code while retaining one valid baseline stage.
    Oracle
    The accepted closed vocabulary declares the six exact members.
    Acceptance
    Each member is stored by identity with exact ExternalFailureCode type.
    Interpretation
    Passing establishes accepted construction for every code member.
    Limitations
    Code classification does not establish retry safety or scientific invalidity.
    """
    record = make_external_execution_failure(code=code)
    assert record.code is code
    assert type(record.code) is ExternalFailureCode


@pytest.mark.parametrize(
    "code",
    [
        pytest.param("unavailable", id="unavailable_string_lookalike"),
        pytest.param("not_authorized", id="not_authorized_string_lookalike"),
        pytest.param("rejected", id="rejected_string_lookalike"),
        pytest.param("interrupted", id="interrupted_string_lookalike"),
        pytest.param("malformed_result", id="malformed_result_string_lookalike"),
        pytest.param("internal_error", id="internal_error_string_lookalike"),
    ],
)
def test_constructor__code_type__rejects_wire_string_lookalikes(code: str) -> None:
    """
    Evidence ID
    SV-PROV-344
    Requirement
    Code rejects every corresponding wire-string lookalike.
    Method
    Override only code with each declared wire spelling.
    Oracle
    The semantic enum contract excludes raw strings.
    Acceptance
    Every string partition raises exactly TypeError.
    Interpretation
    Passing distinguishes all code members from their wire spellings.
    Limitations
    This does not assess serialization or operational equivalence.
    """
    with pytest.raises(TypeError):
        make_external_execution_failure(code=code)


def test_constructor__code_type__rejects_unrelated_integer() -> None:
    """
    Evidence ID
    SV-PROV-345
    Requirement
    Code rejects an unrelated integer semantic type.
    Method
    Override only code with integer 1.
    Oracle
    The semantic contract accepts only ExternalFailureCode members.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing isolates unrelated wrong-type rejection for code.
    Limitations
    No retry or scientific decision is inferred.
    """
    with pytest.raises(TypeError):
        make_external_execution_failure(code=1)


def test_constructor__code_type__rejects_failure_stage_member() -> None:
    """
    Evidence ID
    SV-PROV-346
    Requirement
    Code rejects cross-enum contamination by ExternalFailureStage.
    Method
    Override only code with ExternalFailureStage.EXECUTION.
    Oracle
    Distinct enum classes remain distinct despite both being StrEnum families.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing isolates cross-enum rejection at the code field.
    Limitations
    This does not classify operational equivalence.
    """
    with pytest.raises(TypeError):
        make_external_execution_failure(code=ExternalFailureStage.EXECUTION)


@pytest.mark.parametrize(
    "paths",
    [
        pytest.param((), id="empty_builtin_tuple"),
        pytest.param(("diagnostics/stderr.txt",), id="singleton_builtin_tuple"),
        pytest.param(("diagnostics/a.txt", "diagnostics/b.txt"), id="sorted_path_pair"),
        pytest.param(("logs/run/stderr.txt",), id="ordinary_nested_path"),
        pytest.param(("diagnostics/café.txt",), id="nfc_unicode_path"),
        pytest.param(("Logs/Mixed.Case",), id="exact_case_preserved"),
        pytest.param(("diagnostics/report.final.txt",), id="exact_spelling_preserved"),
    ],
)
def test_constructor__diagnostic_paths__accepts_lexically_safe_states(
    paths: tuple[str, ...],
) -> None:
    """
    Evidence ID
    SV-PROV-044
    Requirement
    Diagnostic paths accept canonical built-in tuples and safe lexical partitions.
    Method
    Construct empty, singleton, sorted, nested, NFC Unicode, case, and spelling
    partitions.
    Oracle
    Each fixed tuple is unique, sorted, root-relative, NFC, and POSIX lexical.
    Acceptance
    Each tuple value and member spelling is stored exactly with built-in tuple type.
    Interpretation
    Passing establishes accepted path and tuple partitions without hidden spelling
    or case coercion.
    Limitations
    No general path-length limit, filesystem access, or diagnostic-content claim is
    made.
    """
    record = make_external_execution_failure(diagnostic_paths=paths)
    assert record.diagnostic_paths == paths
    assert type(record.diagnostic_paths) is tuple


def test_constructor__diagnostic_paths_container_type__rejects_invalid_state() -> None:
    """
    Evidence ID
    SV-PROV-230
    Requirement
    Diagnostic paths require an exact built-in tuple.
    Method
    Pass a list containing an otherwise valid path.
    Oracle
    The accepted container contract excludes list and assigns TypeError.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing isolates wrong container type rejection.
    Limitations
    Other state remains valid; no filesystem or diagnostic-content access occurs.
    """
    with pytest.raises(TypeError):
        make_external_execution_failure(diagnostic_paths=["diagnostics/a"])


def test_constructor__diagnostic_paths_member_type__rejects_invalid_state() -> None:
    """
    Evidence ID
    SV-PROV-347
    Requirement
    Every diagnostic-path member requires exact built-in string type.
    Method
    Pass a tuple containing one integer.
    Oracle
    The accepted member contract excludes integers.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing isolates wrong member type rejection.
    Limitations
    Other state remains valid; no filesystem or diagnostic-content access occurs.
    """
    with pytest.raises(TypeError):
        make_external_execution_failure(diagnostic_paths=(1,))


def test_constructor__diagnostic_paths_member_nonempty__rejects_invalid_state() -> None:
    """
    Evidence ID
    SV-PROV-348
    Requirement
    Every diagnostic path must be nonempty.
    Method
    Pass a tuple containing one empty string.
    Oracle
    The accepted path invariant excludes empty text.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates empty-path rejection.
    Limitations
    Other state remains valid; no filesystem or diagnostic-content access occurs.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(diagnostic_paths=("",))


def test_constructor__diagnostic_paths_member_surrogate__rejects_invalid_state() -> (
    None
):
    """
    Evidence ID
    SV-PROV-349
    Requirement
    Every diagnostic path must be free of Unicode surrogates.
    Method
    Pass one path containing a surrogate code point.
    Oracle
    The accepted Unicode contract excludes surrogates.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates surrogate rejection.
    Limitations
    Other state remains valid; no filesystem or diagnostic-content access occurs.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(diagnostic_paths=("diagnostics/\ud800",))


def test_constructor__diagnostic_paths_member_nfc__rejects_invalid_state() -> None:
    """
    Evidence ID
    SV-PROV-350
    Requirement
    Every diagnostic path must be NFC text.
    Method
    Pass one decomposed non-NFC path.
    Oracle
    The accepted Unicode contract requires NFC normalization.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates non-NFC rejection.
    Limitations
    Other state remains valid; no filesystem or diagnostic-content access occurs.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(diagnostic_paths=("diagnostics/e\u0301.txt",))


def test_constructor__diagnostic_paths_absolute_posix__rejects_invalid_state() -> None:
    """
    Evidence ID
    SV-PROV-351
    Requirement
    Diagnostic paths must be root-relative rather than absolute POSIX paths.
    Method
    Pass one leading-slash path.
    Oracle
    The accepted lexical contract excludes absolute POSIX syntax.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates absolute POSIX rejection.
    Limitations
    Other state remains valid; no filesystem or diagnostic-content access occurs.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(diagnostic_paths=("/absolute",))


def test_constructor__diagnostic_paths_windows_drive__rejects_invalid_state() -> None:
    """
    Evidence ID
    SV-PROV-352
    Requirement
    Diagnostic paths must not use Windows drive syntax.
    Method
    Pass one drive-prefixed path.
    Oracle
    The accepted lexical contract excludes drive syntax.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates Windows-drive rejection.
    Limitations
    Other state remains valid; no filesystem or diagnostic-content access occurs.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(diagnostic_paths=("C:/diagnostics",))


@pytest.mark.parametrize(
    "paths",
    [
        pytest.param(("diagnostics\\stderr.txt",), id="backslash_separator"),
        pytest.param(("diagnostics/",), id="trailing_separator"),
        pytest.param(("diagnostics//stderr.txt",), id="repeated_separator"),
        pytest.param(("diagnostics//stderr.txt",), id="empty_path_component"),
    ],
)
def test_constructor__diagnostic_paths_separator_syntax__rejects_invalid_state(
    paths: tuple[str, ...],
) -> None:
    """
    Evidence ID
    SV-PROV-353
    Requirement
    Diagnostic paths reject backslash, trailing, repeated, and empty-component
    separator syntax.
    Method
    Pass explicit lexical examples; repeated separators necessarily create an empty
    component.
    Oracle
    The accepted root-relative POSIX lexical contract rejects each syntax with
    ValueError.
    Acceptance
    Every semantic partition raises exactly ValueError.
    Interpretation
    Passing establishes the separator-syntax boundary and its empty-component
    consequence.
    Limitations
    The examples may share an implementation branch; no filesystem normalization is
    attempted.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(diagnostic_paths=paths)


@pytest.mark.parametrize(
    "paths",
    [
        pytest.param(("diagnostics/./stderr.txt",), id="dot_component"),
        pytest.param(("diagnostics/../stderr.txt",), id="parent_component"),
    ],
)
def test_constructor__diagnostic_paths_relative_components__rejects_invalid_state(
    paths: tuple[str, ...],
) -> None:
    """
    Evidence ID
    SV-PROV-354
    Requirement
    Diagnostic paths reject dot and parent components.
    Method
    Pass one path for each prohibited relative component.
    Oracle
    The accepted lexical contract excludes both exact component spellings.
    Acceptance
    Each partition raises exactly ValueError.
    Interpretation
    Passing establishes component-level dot-segment rejection.
    Limitations
    No path resolution or filesystem traversal occurs.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(diagnostic_paths=paths)


@pytest.mark.parametrize(
    "paths",
    [
        pytest.param(("CON",), id="windows_device_name"),
        pytest.param(("logs/NUL",), id="nested_windows_device_name"),
        pytest.param(("aux.txt",), id="windows_device_name_with_extension"),
    ],
)
def test_constructor__diagnostic_paths_windows_devices__rejects_invalid_state(
    paths: tuple[str, ...],
) -> None:
    """
    Evidence ID
    SV-PROV-355
    Requirement
    Diagnostic paths reject Windows device-name components at any depth and with
    extensions.
    Method
    Pass root, nested, and extension-bearing reserved device stems.
    Oracle
    The accepted lexical contract compares each component stem against reserved
    device names.
    Acceptance
    Each partition raises exactly ValueError.
    Interpretation
    Passing establishes reserved device-component rejection.
    Limitations
    This lexical rule does not probe an operating system or filesystem.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(diagnostic_paths=paths)


@pytest.mark.parametrize(
    "paths",
    [
        pytest.param(("diagnostics/a\x1f.txt",), id="c0_control_character"),
        pytest.param(("diagnostics/a\x7f.txt",), id="del_control_character"),
        pytest.param(("diagnostics/a\x80.txt",), id="c1_control_character"),
        pytest.param(("diagnostics/a\u2028.txt",), id="unicode_line_separator"),
        pytest.param(("diagnostics/a\u2029.txt",), id="unicode_paragraph_separator"),
    ],
)
def test_constructor__diagnostic_paths_control_characters__rejects_invalid_state(
    paths: tuple[str, ...],
) -> None:
    """
    Evidence ID
    SV-PROV-356
    Requirement
    Diagnostic paths reject C0, DEL, C1, Unicode line, and Unicode paragraph
    controls.
    Method
    Pass one explicit path for every prohibited control partition.
    Oracle
    The accepted lexical safety contract excludes each code-point range or value.
    Acceptance
    Each partition raises exactly ValueError.
    Interpretation
    Passing establishes the declared control-character safety boundary.
    Limitations
    No terminal, file, or diagnostic rendering is exercised.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(diagnostic_paths=paths)


def test_constructor__diagnostic_paths_ordering__rejects_invalid_state() -> None:
    """
    Evidence ID
    SV-PROV-357
    Requirement
    Diagnostic path tuples must be in lexical order.
    Method
    Pass two valid unique paths in reverse order.
    Oracle
    The canonical relation requires tuple order equal sorted tuple order.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates reverse-order rejection.
    Limitations
    Other state remains valid; no filesystem or diagnostic-content access occurs.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(
            diagnostic_paths=("diagnostics/b", "diagnostics/a")
        )


def test_constructor__diagnostic_paths_uniqueness__rejects_invalid_state() -> None:
    """
    Evidence ID
    SV-PROV-358
    Requirement
    Diagnostic path tuples must contain unique paths.
    Method
    Pass a sorted tuple containing a duplicate path.
    Oracle
    The canonical relation requires tuple cardinality equal set cardinality.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates duplicate-path rejection.
    Limitations
    Other state remains valid; no filesystem or diagnostic-content access occurs.
    """
    with pytest.raises(ValueError):
        make_external_execution_failure(
            diagnostic_paths=("diagnostics/a", "diagnostics/a")
        )


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("failure_id", id="failure_id_frozen_reassignment"),
        pytest.param("request_id", id="request_id_frozen_reassignment"),
        pytest.param("correlation_id", id="correlation_id_frozen_reassignment"),
        pytest.param("attempt_id", id="attempt_id_frozen_reassignment"),
        pytest.param("stage", id="stage_frozen_reassignment"),
        pytest.param("code", id="code_frozen_reassignment"),
        pytest.param("diagnostic_paths", id="diagnostic_paths_frozen_reassignment"),
        pytest.param("provenance_id", id="provenance_id_frozen_reassignment"),
    ],
)
def test_field__frozen_state__rejects_every_public_field_reassignment(
    field_name: str,
) -> None:
    """
    Evidence ID
    SV-PROV-234
    Requirement
    Every public failure field is frozen after construction.
    Method
    Attempt setattr independently for each semantic public field ID.
    Oracle
    Frozen dataclass assignment has the exact FrozenInstanceError oracle.
    Acceptance
    Every field reassignment raises exactly FrozenInstanceError.
    Interpretation
    Passing establishes uniform frozen assignment behavior over all eight fields.
    Limitations
    Referenced diagnostic artifacts and external state are outside this test.
    """
    record = make_external_execution_failure()
    with pytest.raises(FrozenInstanceError):
        setattr(record, field_name, getattr(record, field_name))


def test_method__eq__identical_state__compares_equal() -> None:
    """
    Evidence ID
    SV-PROV-359
    Requirement
    Two independently constructed failures with identical complete valid state
    compare equal.
    Method
    Construct two baseline records and apply public equality.
    Oracle
    Accepted dataclass value semantics make identical eight-field state equal.
    Acceptance
    The records compare equal.
    Interpretation
    Passing establishes equality for identical represented failure state.
    Limitations
    Equality does not imply operational equivalence, retry eligibility, or
    scientific meaning.
    """
    assert make_external_execution_failure() == make_external_execution_failure()


@pytest.mark.parametrize(
    ("field_name", "distinct_value"),
    [
        pytest.param(
            "failure_id", "failure-2", id="failure_id_valid_state_affects_equality"
        ),
        pytest.param(
            "request_id", "request-2", id="request_id_valid_state_affects_equality"
        ),
        pytest.param(
            "correlation_id",
            "correlation-2",
            id="correlation_id_valid_state_affects_equality",
        ),
        pytest.param(
            "attempt_id", "attempt-2", id="attempt_id_valid_state_affects_equality"
        ),
        pytest.param(
            "stage",
            ExternalFailureStage.RESULT_CAPTURE,
            id="stage_valid_state_affects_equality",
        ),
        pytest.param(
            "code",
            ExternalFailureCode.INTERNAL_ERROR,
            id="code_valid_state_affects_equality",
        ),
        pytest.param(
            "diagnostic_paths",
            ("diagnostics/other.txt",),
            id="diagnostic_paths_valid_state_affects_equality",
        ),
        pytest.param(
            "provenance_id",
            "provenance-2",
            id="provenance_id_valid_state_affects_equality",
        ),
    ],
)
def test_method__eq__valid_field_states__affect_equality(
    field_name: str, distinct_value: object
) -> None:
    """
    Evidence ID
    SV-PROV-235
    Requirement
    Every public failure field independently participates in equality.
    Method
    Compare baseline state with one valid override for each public field.
    Oracle
    Dataclass equality compares represented field values; every fixed override is
    valid and distinct.
    Acceptance
    Every one-field variant compares unequal to baseline.
    Interpretation
    Passing establishes equality sensitivity for all eight public fields.
    Limitations
    Equality does not establish retry eligibility or operational or scientific
    equivalence.
    """
    assert make_external_execution_failure() != make_external_execution_failure(
        **{field_name: distinct_value}
    )


@pytest.mark.parametrize(
    "distinct_stage",
    [
        pytest.param(
            ExternalFailureStage.REQUEST_ACCEPTANCE,
            id="request_acceptance_distinguishable",
        ),
        pytest.param(
            ExternalFailureStage.RESULT_CAPTURE, id="result_capture_distinguishable"
        ),
    ],
)
def test_method__eq__failure_stages__remain_distinguishable(
    distinct_stage: ExternalFailureStage,
) -> None:
    """
    Evidence ID
    SV-PROV-361
    Requirement
    Every failure stage remains distinguishable through valid failure records.
    Method
    Compare baseline EXECUTION with each other valid stage using one-field
    variation.
    Oracle
    Distinct enum members are distinct represented values under dataclass equality.
    Acceptance
    Each valid stage variant compares unequal to the EXECUTION baseline.
    Interpretation
    Passing establishes stage-member distinguishability without all-pairs expansion.
    Limitations
    No operational ordering, retry decision, or equivalence is inferred.
    """
    assert make_external_execution_failure() != make_external_execution_failure(
        stage=distinct_stage
    )


@pytest.mark.parametrize(
    "distinct_code",
    [
        pytest.param(ExternalFailureCode.UNAVAILABLE, id="unavailable_distinguishable"),
        pytest.param(
            ExternalFailureCode.NOT_AUTHORIZED, id="not_authorized_distinguishable"
        ),
        pytest.param(ExternalFailureCode.REJECTED, id="rejected_distinguishable"),
        pytest.param(
            ExternalFailureCode.MALFORMED_RESULT, id="malformed_result_distinguishable"
        ),
        pytest.param(
            ExternalFailureCode.INTERNAL_ERROR, id="internal_error_distinguishable"
        ),
    ],
)
def test_method__eq__failure_codes__remain_distinguishable(
    distinct_code: ExternalFailureCode,
) -> None:
    """
    Evidence ID
    SV-PROV-362
    Requirement
    Every failure code remains distinguishable through valid failure records.
    Method
    Compare baseline INTERRUPTED with each other valid code using one-field
    variation.
    Oracle
    Distinct enum members are distinct represented values under dataclass equality.
    Acceptance
    Each valid code variant compares unequal to the INTERRUPTED baseline.
    Interpretation
    Passing establishes code-member distinguishability without all-pairs expansion.
    Limitations
    No severity, retry decision, or scientific meaning is inferred.
    """
    assert make_external_execution_failure() != make_external_execution_failure(
        code=distinct_code
    )


def test_method__eq__unrelated_object__compares_unequal() -> None:
    """
    Evidence ID
    SV-PROV-360
    Requirement
    A failure record compares unequal to an unrelated object.
    Method
    Compare one valid failure with a fresh built-in object.
    Oracle
    Accepted dataclass equality returns unequal for an unrelated class.
    Acceptance
    The comparison evaluates to unequal.
    Interpretation
    Passing establishes the unrelated-object equality boundary.
    Limitations
    Ordering, hashing, subclasses, and cross-language equality are outside scope.
    """
    assert make_external_execution_failure() != object()


def test_field__failure_lifecycle__separates_result_and_later_decisions() -> None:
    """
    Evidence ID
    SV-PROV-233
    Requirement
    Structured failure owns stage, code, and diagnostic references but no success or
    later-decision state.
    Method
    Inspect the exact public field inventory against owned and excluded lifecycle
    names.
    Oracle
    The accepted failure family owns the three failure fields and excludes all
    listed result, retry, parsing, adaptation, numerical, scientific, and UQ fields.
    Acceptance
    The exact inventory equals PUBLIC_FIELDS, contains the three failure fields, and
    is disjoint from every excluded name.
    Interpretation
    Passing establishes only the current stored-state lifecycle boundary.
    Limitations
    Field absence does not prove retry safety, numerical or model classification,
    scientific invalidity, UQ, or provenance truth.
    """
    public_fields = tuple(field.name for field in fields(SUT))
    assert public_fields == PUBLIC_FIELDS
    assert {"stage", "code", "diagnostic_paths"} <= set(public_fields)
    assert set(public_fields).isdisjoint(
        {
            "status",
            "output_artifact_ids",
            "manifest_id",
            "retry_authorization",
            "parsed_result",
            "adapted_result",
            "converged",
            "numerically_accepted",
            "scientifically_validated",
            "uncertainty_quantified",
        }
    )


def test_field__durable_boundary__excludes_raw_runtime_and_secret_state() -> None:
    """
    Evidence ID
    SV-PROV-236
    Requirement
    Structured failure stores diagnostic references but no raw runtime or secret
    state.
    Method
    Inspect the exact public field inventory against the complete prohibited-name
    inventory.
    Oracle
    The accepted durable boundary excludes raw diagnostics, streams, commands,
    secrets, clients, processes, handles, files, and services.
    Acceptance
    The exact public inventory equals PUBLIC_FIELDS and is disjoint from all
    prohibited names.
    Interpretation
    Passing establishes only absence of those fields from current stored failure
    state.
    Limitations
    Name absence does not inspect referenced diagnostics, identifier text content,
    or provenance truth.
    """
    public_fields = tuple(field.name for field in fields(SUT))
    assert public_fields == PUBLIC_FIELDS
    assert set(public_fields).isdisjoint(
        {
            "message",
            "traceback",
            "stdout",
            "stderr",
            "command",
            "credential",
            "password",
            "secret",
            "client",
            "process",
            "scheduler_handle",
            "open_file",
            "mutable_runtime_service",
        }
    )
