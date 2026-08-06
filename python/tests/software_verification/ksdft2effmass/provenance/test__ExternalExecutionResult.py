r"""Software verification of ``ExternalExecutionResult``.

Facet and represented meaning
-----------------------------
This class-owned software evidence verifies exact eight-field result
construction, identifier invariants, exact status typing, canonical
output-artifact tuples, frozen state, equality, durable result boundaries, and
completion lifecycle limitations.

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``ExternalExecutionResult``. Public constructor inputs,
dataclass field semantics, and fixed valid or invalid literals provide the
oracles. ``COMPLETED`` records only completion at the external boundary; it does
not establish output parsing, output adaptation, artifact identity verification,
solver convergence, numerical acceptance, scientific validation, UQ, or
provenance truth.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the stated result-record software behavior; failure
identifies a production, test-input, oracle, or accepted-contract mismatch.
Field absence establishes only the current stored-state boundary. This evidence
does not establish physical correctness, portability, cross-language agreement,
scientific validation, or uncertainty quantification.
"""

from dataclasses import FrozenInstanceError, astuple, fields
from typing import Any

import pytest

from ksdft2effmass.provenance import (
    ExternalExecutionResult,
    ExternalExecutionStatus,
)

SUT = ExternalExecutionResult
pytestmark = pytest.mark.software_verification

IDENTIFIER_FIELDS = (
    "result_id",
    "request_id",
    "correlation_id",
    "attempt_id",
    "manifest_id",
    "provenance_id",
)
PUBLIC_FIELDS = (
    "result_id",
    "request_id",
    "correlation_id",
    "attempt_id",
    "status",
    "output_artifact_ids",
    "manifest_id",
    "provenance_id",
)


def make_external_execution_result(**overrides: Any) -> ExternalExecutionResult:
    """Evidence ID
    Owns no identifier; supports all class-owned evidence in this module.
    Requirement
    Result tests need valid baseline state with explicit one-field overrides.
    Method
    Merge named overrides into fixed synthetic values and call the public constructor.
    Oracle
    The accepted constructor signature and independently valid literals define setup.
    Acceptance
    Return the constructor result without assertions, normalization, or I/O.
    Interpretation
    The helper isolates one field while every unselected result field remains valid.
    Limitations
    This helper owns no evidence result and contains no hidden oracle.
    """
    values: dict[str, Any] = {
        "result_id": "result-1",
        "request_id": "request-1",
        "correlation_id": "correlation-1",
        "attempt_id": "attempt-1",
        "status": ExternalExecutionStatus.COMPLETED,
        "output_artifact_ids": ("output-1", "output-2"),
        "manifest_id": "manifest-1",
        "provenance_id": "provenance-1",
    }
    values.update(overrides)
    return ExternalExecutionResult(**values)


def test_constructor__field_mapping__stores_exact_values_types_and_order() -> None:
    """Evidence ID
    SV-PROV-040
    Requirement
    Construction stores the exact eight-field result state without coercion.
    Method
    Construct baseline state and inspect public order, values, and exact stored types.
    Oracle
    The accepted public inventory and fixed literals define expected represented state.
    Acceptance
    Order and values match exactly; types are str, ExternalExecutionStatus, and
    tuple in the declared positions.
    Interpretation
    Passing establishes exact result constructor mapping and stored-type preservation.
    Limitations
    Synthetic metadata only; construction does not parse, adapt, or verify artifacts.
    """
    record = make_external_execution_result()
    assert tuple(field.name for field in fields(record)) == PUBLIC_FIELDS
    assert astuple(record) == (
        "result-1",
        "request-1",
        "correlation-1",
        "attempt-1",
        ExternalExecutionStatus.COMPLETED,
        ("output-1", "output-2"),
        "manifest-1",
        "provenance-1",
    )
    assert tuple(type(value) for value in astuple(record)) == (
        str,
        str,
        str,
        str,
        ExternalExecutionStatus,
        tuple,
        str,
        str,
    )
    assert type(record.status) is ExternalExecutionStatus
    assert type(record.output_artifact_ids) is tuple


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "result_id", "result-ordinary", id="result_id_ordinary_valid_identifier"
        ),
        pytest.param("result_id", "a", id="result_id_minimum_length_1"),
        pytest.param("result_id", "a" * 128, id="result_id_maximum_length_128"),
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
            "manifest_id",
            "manifest-ordinary",
            id="manifest_id_ordinary_valid_identifier",
        ),
        pytest.param("manifest_id", "a", id="manifest_id_minimum_length_1"),
        pytest.param("manifest_id", "a" * 128, id="manifest_id_maximum_length_128"),
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
    """Evidence ID
    SV-PROV-314
    Requirement
    Every identifier accepts ordinary portable text and lengths 1 and 128.
    Method
    Override one field for each explicit field-and-length partition.
    Oracle
    The accepted grammar permits 1 through 128 portable ASCII characters.
    Acceptance
    Construction succeeds and stores the selected value unchanged.
    Interpretation
    Passing establishes accepted lexical-length partitions for all six identifiers.
    Limitations
    This lexical evidence does not establish identity uniqueness or provenance truth.
    """
    assert (
        getattr(make_external_execution_result(**{field_name: value}), field_name)
        == value
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("result_id", b"identifier", id="result_id_bytes_wrong_type"),
        pytest.param("request_id", b"identifier", id="request_id_bytes_wrong_type"),
        pytest.param(
            "correlation_id", b"identifier", id="correlation_id_bytes_wrong_type"
        ),
        pytest.param("attempt_id", b"identifier", id="attempt_id_bytes_wrong_type"),
        pytest.param("manifest_id", b"identifier", id="manifest_id_bytes_wrong_type"),
        pytest.param(
            "provenance_id", b"identifier", id="provenance_id_bytes_wrong_type"
        ),
    ],
)
def test_constructor__identifier_type__rejects_bytes_wrong_type(
    field_name: str, value: object
) -> None:
    """Evidence ID
    SV-PROV-224
    Requirement
    Every identifier rejects a wrong semantic type.
    Method
    Override each identifier independently with bytes.
    Oracle
    The accepted identifier type contract assigns TypeError to bytes.
    Acceptance
    Every field raises exactly TypeError.
    Interpretation
    Passing establishes bytes wrong type rejection for all six identifiers.
    Limitations
    Every other field remains valid; no identity relation or provenance truth is tested.
    """
    with pytest.raises(TypeError):
        make_external_execution_result(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("result_id", "", id="result_id_empty_text"),
        pytest.param("request_id", "", id="request_id_empty_text"),
        pytest.param("correlation_id", "", id="correlation_id_empty_text"),
        pytest.param("attempt_id", "", id="attempt_id_empty_text"),
        pytest.param("manifest_id", "", id="manifest_id_empty_text"),
        pytest.param("provenance_id", "", id="provenance_id_empty_text"),
    ],
)
def test_constructor__identifier_empty__rejects_empty_text(
    field_name: str, value: object
) -> None:
    """Evidence ID
    SV-PROV-315
    Requirement
    Every identifier rejects empty text.
    Method
    Override each identifier independently with an empty string.
    Oracle
    The accepted nonempty invariant assigns ValueError to empty text.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes empty text rejection for all six identifiers.
    Limitations
    Every other field remains valid; no identity relation or provenance truth is tested.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("result_id", "bad id", id="result_id_embedded_space"),
        pytest.param("request_id", "bad id", id="request_id_embedded_space"),
        pytest.param("correlation_id", "bad id", id="correlation_id_embedded_space"),
        pytest.param("attempt_id", "bad id", id="attempt_id_embedded_space"),
        pytest.param("manifest_id", "bad id", id="manifest_id_embedded_space"),
        pytest.param("provenance_id", "bad id", id="provenance_id_embedded_space"),
    ],
)
def test_constructor__identifier_grammar__rejects_embedded_space(
    field_name: str, value: object
) -> None:
    """Evidence ID
    SV-PROV-316
    Requirement
    Every identifier rejects embedded-space grammar.
    Method
    Override each identifier independently with malformed text.
    Oracle
    The portable grammar excludes embedded spaces and assigns ValueError.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes embedded space rejection for all six identifiers.
    Limitations
    Every other field remains valid; no identity relation or provenance truth is tested.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("result_id", "-leading", id="result_id_invalid_leading_hyphen"),
        pytest.param("request_id", "-leading", id="request_id_invalid_leading_hyphen"),
        pytest.param(
            "correlation_id", "-leading", id="correlation_id_invalid_leading_hyphen"
        ),
        pytest.param("attempt_id", "-leading", id="attempt_id_invalid_leading_hyphen"),
        pytest.param(
            "manifest_id", "-leading", id="manifest_id_invalid_leading_hyphen"
        ),
        pytest.param(
            "provenance_id", "-leading", id="provenance_id_invalid_leading_hyphen"
        ),
    ],
)
def test_constructor__identifier_leading__rejects_invalid_leading_hyphen(
    field_name: str, value: object
) -> None:
    """Evidence ID
    SV-PROV-317
    Requirement
    Every identifier rejects an invalid leading character.
    Method
    Override each identifier independently with a leading hyphen.
    Oracle
    The portable grammar requires an ASCII alphanumeric leading character.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes invalid leading hyphen rejection for all six identifiers.
    Limitations
    Every other field remains valid; no identity relation or provenance truth is tested.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("result_id", "\ud800", id="result_id_unicode_surrogate"),
        pytest.param("request_id", "\ud800", id="request_id_unicode_surrogate"),
        pytest.param("correlation_id", "\ud800", id="correlation_id_unicode_surrogate"),
        pytest.param("attempt_id", "\ud800", id="attempt_id_unicode_surrogate"),
        pytest.param("manifest_id", "\ud800", id="manifest_id_unicode_surrogate"),
        pytest.param("provenance_id", "\ud800", id="provenance_id_unicode_surrogate"),
    ],
)
def test_constructor__identifier_surrogate__rejects_unicode_surrogate(
    field_name: str, value: object
) -> None:
    """Evidence ID
    SV-PROV-318
    Requirement
    Every identifier rejects Unicode surrogate text.
    Method
    Override each identifier independently with one surrogate code point.
    Oracle
    The accepted Unicode contract excludes surrogate code points.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes unicode surrogate rejection for all six identifiers.
    Limitations
    Every other field remains valid; no identity relation or provenance truth is tested.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("result_id", "e\u0301", id="result_id_non_nfc"),
        pytest.param("request_id", "e\u0301", id="request_id_non_nfc"),
        pytest.param("correlation_id", "e\u0301", id="correlation_id_non_nfc"),
        pytest.param("attempt_id", "e\u0301", id="attempt_id_non_nfc"),
        pytest.param("manifest_id", "e\u0301", id="manifest_id_non_nfc"),
        pytest.param("provenance_id", "e\u0301", id="provenance_id_non_nfc"),
    ],
)
def test_constructor__identifier_nfc__rejects_non_nfc(
    field_name: str, value: object
) -> None:
    """Evidence ID
    SV-PROV-319
    Requirement
    Every identifier rejects non-NFC text.
    Method
    Override each identifier independently with decomposed accented text.
    Oracle
    The accepted Unicode contract requires text equal to its NFC normalization.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes non nfc rejection for all six identifiers.
    Limitations
    Every other field remains valid; no identity relation or provenance truth is tested.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(**{field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("result_id", "a" * 129, id="result_id_overlength_129"),
        pytest.param("request_id", "a" * 129, id="request_id_overlength_129"),
        pytest.param("correlation_id", "a" * 129, id="correlation_id_overlength_129"),
        pytest.param("attempt_id", "a" * 129, id="attempt_id_overlength_129"),
        pytest.param("manifest_id", "a" * 129, id="manifest_id_overlength_129"),
        pytest.param("provenance_id", "a" * 129, id="provenance_id_overlength_129"),
    ],
)
def test_constructor__identifier_length__rejects_overlength_129(
    field_name: str, value: object
) -> None:
    """Evidence ID
    SV-PROV-320
    Requirement
    Every identifier rejects text longer than 128 characters.
    Method
    Override each identifier independently with 129 portable characters.
    Oracle
    The accepted identifier maximum is exactly 128 characters.
    Acceptance
    Every field raises exactly ValueError.
    Interpretation
    Passing establishes overlength 129 rejection for all six identifiers.
    Limitations
    Every other field remains valid; no identity relation or provenance truth is tested.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(**{field_name: value})


def test_constructor__status_exact_type__accepts_completed_member() -> None:
    """Evidence ID
    SV-PROV-321
    Requirement
    Status accepts the exact version-1 COMPLETED enum state.
    Method
    Construct with ExternalExecutionStatus.COMPLETED and inspect identity and exact
    type.
    Oracle
    The accepted version-1 status vocabulary contains this exact member.
    Acceptance
    The member is stored unchanged and type(record.status) is ExternalExecutionStatus.
    Interpretation
    Passing establishes accepted exact status construction and storage.
    Limitations
    Version 1 provides no second valid result status and no lifecycle conclusion
    beyond boundary completion.
    """
    status = ExternalExecutionStatus.COMPLETED
    record = make_external_execution_result(status=status)
    assert record.status is status
    assert type(record.status) is ExternalExecutionStatus


def test_constructor__status_type__rejects_string_lookalike() -> None:
    """Evidence ID
    SV-PROV-223
    Requirement
    Status rejects the completed wire string in place of the enum member.
    Method
    Override status with the string lookalike completed.
    Oracle
    The semantic enum contract excludes raw strings despite equal wire spelling.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing distinguishes the enum member from its string representation.
    Limitations
    This test does not assess serialization or another valid status state.
    """
    with pytest.raises(TypeError):
        make_external_execution_result(status="completed")


def test_constructor__status_type__rejects_unrelated_integer() -> None:
    """Evidence ID
    SV-PROV-322
    Requirement
    Status rejects an unrelated integer semantic type.
    Method
    Override status independently with integer 1.
    Oracle
    The semantic enum contract accepts only ExternalExecutionStatus members.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing establishes rejection of an unrelated wrong semantic type.
    Limitations
    This test does not assess serialization or status equality variation.
    """
    with pytest.raises(TypeError):
        make_external_execution_result(status=1)


@pytest.mark.parametrize(
    "outputs",
    [
        pytest.param((), id="empty_builtin_tuple"),
        pytest.param(("output-1",), id="singleton_builtin_tuple"),
        pytest.param(
            ("output-1", "output-2"), id="unique_lexically_sorted_builtin_tuple"
        ),
    ],
)
def test_constructor__output_artifact_ids__accepts_canonical_states(
    outputs: tuple[str, ...],
) -> None:
    """Evidence ID
    SV-PROV-041
    Requirement
    Output artifact IDs accept canonical built-in tuple states.
    Method
    Construct empty, singleton, and unique lexically sorted tuple partitions.
    Oracle
    The accepted tuple contract declares each fixed tuple canonical.
    Acceptance
    Each tuple value is stored exactly with built-in tuple type.
    Interpretation
    Passing establishes all accepted tuple cardinality and ordering states.
    Limitations
    This does not verify that referenced artifacts exist or match their identities.
    """
    record = make_external_execution_result(output_artifact_ids=outputs)
    assert record.output_artifact_ids == outputs
    assert type(record.output_artifact_ids) is tuple


def test_constructor__output_artifact_ids_container_type__rejects_invalid_state() -> (
    None
):
    """Evidence ID
    SV-PROV-222
    Requirement
    Output artifact IDs require an exact built-in tuple.
    Method
    Pass a list containing an otherwise valid identifier.
    Oracle
    The accepted container contract excludes list and assigns TypeError.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing isolates wrong container type rejection.
    Limitations
    All other result state remains valid; artifact existence and content are not
    inspected.
    """
    with pytest.raises(TypeError):
        make_external_execution_result(output_artifact_ids=["output-1"])


def test_constructor__output_artifact_ids_member_type__rejects_invalid_state() -> None:
    """Evidence ID
    SV-PROV-323
    Requirement
    Every output tuple member requires exact built-in string type.
    Method
    Pass a built-in tuple containing one integer.
    Oracle
    The accepted member contract excludes integers and assigns TypeError.
    Acceptance
    Construction raises exactly TypeError.
    Interpretation
    Passing isolates wrong member type rejection.
    Limitations
    All other result state remains valid; artifact existence and content are not
    inspected.
    """
    with pytest.raises(TypeError):
        make_external_execution_result(output_artifact_ids=(1,))


def test_constructor__output_artifact_ids_member_nonempty__rejects_invalid_state() -> (
    None
):
    """Evidence ID
    SV-PROV-324
    Requirement
    Every output tuple member must be nonempty.
    Method
    Pass a tuple containing one empty string.
    Oracle
    The accepted member invariant assigns ValueError to empty text.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates empty member rejection.
    Limitations
    All other result state remains valid; artifact existence and content are not
    inspected.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(output_artifact_ids=("",))


def test_constructor__output_artifact_ids_member_grammar__rejects_invalid_state() -> (
    None
):
    """Evidence ID
    SV-PROV-325
    Requirement
    Every output tuple member must satisfy portable grammar.
    Method
    Pass a tuple containing one embedded-space identifier.
    Oracle
    The accepted portable grammar excludes embedded spaces.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates malformed member grammar rejection.
    Limitations
    All other result state remains valid; artifact existence and content are not
    inspected.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(output_artifact_ids=("bad id",))


def test_constructor__output_artifact_ids_member_leading__rejects_invalid_state() -> (
    None
):
    """Evidence ID
    SV-PROV-326
    Requirement
    Every output tuple member requires an alphanumeric leading character.
    Method
    Pass a tuple containing one leading-hyphen identifier.
    Oracle
    The accepted portable grammar excludes that leading character.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates invalid member-leading-character rejection.
    Limitations
    All other result state remains valid; artifact existence and content are not
    inspected.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(output_artifact_ids=("-leading",))


@pytest.mark.parametrize(
    "outputs",
    [
        pytest.param(("\ud800",), id="member_unicode_surrogate"),
        pytest.param(("e\u0301",), id="member_non_nfc"),
    ],
)
def test_constructor__output_artifact_ids_member_unicode__rejects_invalid_state(
    outputs: tuple[str, ...],
) -> None:
    """Evidence ID
    SV-PROV-327
    Requirement
    Every output tuple member must be surrogate-free NFC text.
    Method
    Pass independent surrogate and decomposed non-NFC member partitions.
    Oracle
    The accepted Unicode contract rejects both partitions with ValueError.
    Acceptance
    Each partition raises exactly ValueError.
    Interpretation
    Passing establishes the two owned Unicode member invariants.
    Limitations
    Portable grammar, length, artifact existence, and content are outside this owner.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(output_artifact_ids=outputs)


def test_constructor__output_artifact_ids_member_length__rejects_invalid_state() -> (
    None
):
    """Evidence ID
    SV-PROV-328
    Requirement
    Every output tuple member has maximum length 128.
    Method
    Pass one 129-character portable member.
    Oracle
    The accepted identifier maximum is exactly 128 characters.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates overlength member rejection.
    Limitations
    All other result state remains valid; artifact existence and content are not
    inspected.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(output_artifact_ids=("a" * 129,))


def test_constructor__output_artifact_ids_ordering__rejects_invalid_state() -> None:
    """Evidence ID
    SV-PROV-329
    Requirement
    Output artifact IDs must be in lexical order.
    Method
    Pass two valid unique members in reverse lexical order.
    Oracle
    The canonical relation requires tuple order equal sorted tuple order.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates reverse-order rejection.
    Limitations
    All other result state remains valid; artifact existence and content are not
    inspected.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(output_artifact_ids=("output-2", "output-1"))


def test_constructor__output_artifact_ids_uniqueness__rejects_invalid_state() -> None:
    """Evidence ID
    SV-PROV-330
    Requirement
    Output artifact IDs must be unique.
    Method
    Pass a sorted tuple containing a duplicate member.
    Oracle
    The canonical relation requires member cardinality equal set cardinality.
    Acceptance
    Construction raises exactly ValueError.
    Interpretation
    Passing isolates duplicate-member rejection.
    Limitations
    All other result state remains valid; artifact existence and content are not
    inspected.
    """
    with pytest.raises(ValueError):
        make_external_execution_result(output_artifact_ids=("output-1", "output-1"))


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("result_id", id="result_id_frozen_reassignment"),
        pytest.param("request_id", id="request_id_frozen_reassignment"),
        pytest.param("correlation_id", id="correlation_id_frozen_reassignment"),
        pytest.param("attempt_id", id="attempt_id_frozen_reassignment"),
        pytest.param("status", id="status_frozen_reassignment"),
        pytest.param(
            "output_artifact_ids", id="output_artifact_ids_frozen_reassignment"
        ),
        pytest.param("manifest_id", id="manifest_id_frozen_reassignment"),
        pytest.param("provenance_id", id="provenance_id_frozen_reassignment"),
    ],
)
def test_field__frozen_state__rejects_every_public_field_reassignment(
    field_name: str,
) -> None:
    """Evidence ID
    SV-PROV-227
    Requirement
    Every public result field is frozen after construction.
    Method
    Attempt setattr independently for each semantic public field ID.
    Oracle
    Frozen dataclass assignment has the exact FrozenInstanceError oracle.
    Acceptance
    Every field reassignment raises exactly FrozenInstanceError.
    Interpretation
    Passing establishes uniform frozen assignment behavior over all eight fields.
    Limitations
    Nested referents and external artifact mutability are outside this record-state
    test.
    """
    record = make_external_execution_result()
    with pytest.raises(FrozenInstanceError):
        setattr(record, field_name, getattr(record, field_name))


def test_method__eq__identical_state__compares_equal() -> None:
    """Evidence ID
    SV-PROV-331
    Requirement
    Two independently constructed records with identical complete valid state
    compare equal.
    Method
    Construct two baseline records and apply the public equality operation.
    Oracle
    Accepted dataclass value semantics make identical eight-field state equal.
    Acceptance
    The two records compare equal.
    Interpretation
    Passing establishes equality for identical complete represented state.
    Limitations
    Version 1 status variation and equality against subclasses are not assessed.
    """
    assert make_external_execution_result() == make_external_execution_result()


@pytest.mark.parametrize(
    ("field_name", "distinct_value"),
    [
        pytest.param(
            "result_id", "result-2", id="result_id_valid_state_affects_equality"
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
            "output_artifact_ids",
            ("output-3",),
            id="output_artifact_ids_valid_state_affects_equality",
        ),
        pytest.param(
            "manifest_id", "manifest-2", id="manifest_id_valid_state_affects_equality"
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
    """Evidence ID
    SV-PROV-228
    Requirement
    Every result field having two valid version-1 states independently affects equality.
    Method
    Compare baseline state with one valid override for each variable field,
    including a distinct valid output tuple.
    Oracle
    Dataclass equality compares represented field values; each fixed override is
    valid and distinct.
    Acceptance
    Every one-field variant compares unequal to baseline.
    Interpretation
    Passing establishes equality sensitivity for all fields with two valid public
    states.
    Limitations
    Version 1 admits only COMPLETED; status validity belongs to constructor/type
    evidence and is not fabricated for equality variation.
    """
    assert make_external_execution_result() != make_external_execution_result(
        **{field_name: distinct_value}
    )


def test_method__eq__unrelated_object__compares_unequal() -> None:
    """Evidence ID
    SV-PROV-332
    Requirement
    A result record compares unequal to an unrelated object.
    Method
    Compare a valid record with a fresh built-in object.
    Oracle
    Accepted dataclass equality returns unequal for an unrelated class.
    Acceptance
    The comparison evaluates to unequal.
    Interpretation
    Passing establishes the unrelated-object equality boundary.
    Limitations
    This does not assess ordering, hashing, subclasses, or cross-language equality.
    """
    assert make_external_execution_result() != object()


def test_field__completion_lifecycle__excludes_later_decisions() -> None:
    """Evidence ID
    SV-PROV-225
    Requirement
    COMPLETED records only completion at the external boundary.
    Method
    Inspect the exact public field inventory for parsing, adaptation, identity,
    convergence, acceptance, validation, and UQ conclusion fields.
    Oracle
    The accepted lifecycle boundary excludes all listed later-state names.
    Acceptance
    The exact public inventory equals PUBLIC_FIELDS and is disjoint from every
    excluded name.
    Interpretation
    Passing establishes only the current stored-state boundary.
    Limitations
    Field absence does not prove outputs were parsed or adapted, identity verified,
    convergence reached, numerical acceptance granted, scientific validation
    performed, UQ performed, or provenance true.
    """
    public_fields = tuple(field.name for field in fields(SUT))
    assert public_fields == PUBLIC_FIELDS
    assert set(public_fields).isdisjoint(
        {
            "parsed",
            "adapted",
            "artifact_verified",
            "converged",
            "numerically_accepted",
            "scientifically_validated",
            "uncertainty_quantified",
        }
    )


def test_field__durable_boundary__excludes_runtime_state() -> None:
    """Evidence ID
    SV-PROV-229
    Requirement
    Durable result records exclude commands, secrets, handles, and mutable runtime
    services.
    Method
    Inspect the exact public field inventory against the complete prohibited-name
    inventory.
    Oracle
    The accepted durable boundary excludes each listed runtime or credential field.
    Acceptance
    The exact public inventory equals PUBLIC_FIELDS and is disjoint from all
    prohibited names.
    Interpretation
    Passing establishes only absence of those fields from current stored result state.
    Limitations
    Name absence does not inspect referenced artifacts, prove secret-free identifier
    text, or establish provenance truth.
    """
    public_fields = tuple(field.name for field in fields(SUT))
    assert public_fields == PUBLIC_FIELDS
    assert set(public_fields).isdisjoint(
        {
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
