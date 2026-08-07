r"""Software verification of ``OperatorRecordJsonSerializer``.

Facet and represented meaning
-----------------------------
This class-owned module owns the deserialization structure facet. Object: serializer
JSON parser and version-1 object/matrix structure boundary.
Evidence class: software verification. Requirement: strict JSON text, unique keys,
standard constants, exact object fields, exact integer version, and rectangular
square complex-pair matrices. Strategy: mutate one independently valid payload at
a time. Oracle: approved grammar and field tables, independent of private methods.
Acceptance requires documented TypeError/ValueError categories. Passing is not
scientific validation, UQ, or Rust conformance; failure indicates runtime,
specification, documentation, or evidence drift.

Intrinsic and cross-object scope
--------------------------------
The primary owner is ``OperatorRecordJsonSerializer``; collaborators only construct
inputs or expose public outcomes. Accepted public contracts, literal expected
values, Python language semantics, and assigned schema or fixture artifacts provide
the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

import json
from typing import Any

import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordJsonSerializer


def valid_payload() -> dict[str, Any]:
    r"""Evidence ID
    Owns no identifier; supports evidence in this module.
    Requirement
    Structural deserialization cases require one complete schema-version-1 payload
    before changing a single structural partition.
    Method
    Construct or inspect only the named synthetic fixture operation (valid payload); the
    helper owns no assertion result and introduces no hidden oracle.
    Oracle
    The public version-1 schema, fixed wire-field vocabulary, literal JSON grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.
    Acceptance
    The helper returns exactly the requested fixture value or applies only the
    documented comparison; all pass/fail assertions remain in the owning test.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    return json.loads(OperatorRecordJsonSerializer().serialize(make_record()))


@pytest.mark.parametrize("text", [pytest.param("{", id="truncated_object")])
def test_method__deserialize__malformed_json__raises_value_error(text: str) -> None:
    r"""Evidence ID
    SV-ORJS-007
    Requirement
    Syntactically malformed JSON is rejected before payload interpretation.
    Method
    Deserialize a fixed truncated object text.
    Oracle
    JSON grammar requires a closing brace.
    Acceptance
    Exactly ``ValueError`` is raised.
    Interpretation
    A pass confirms syntax translation; failure indicates parser-boundary drift.
    Limitations
    Semantic payload types, validation, UQ, and Rust are excluded.
    """
    with pytest.raises(ValueError):
        OperatorRecordJsonSerializer().deserialize(text)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("[]", id="array_top_level"),
        pytest.param("null", id="null_top_level"),
        pytest.param('"record"', id="string_top_level"),
        pytest.param("1", id="number_top_level"),
    ],
)
def test_method__deserialize__nonobject_top_level__raises_type_error(text: str) -> None:
    r"""Evidence ID
    SV-ORJS-019
    Requirement
    Valid JSON values of the wrong top-level semantic type are rejected.
    Method
    Deserialize array, null, string, and number JSON values independently.
    Oracle
    Schema-version-1 records require one top-level JSON object.
    Acceptance
    Exactly ``TypeError`` names the top-level object role.
    Interpretation
    A pass confirms wrong-type taxonomy; failure indicates runtime layering drift.
    Limitations
    Object field invariants, validation, UQ, and Rust are excluded.
    """
    with pytest.raises(TypeError, match="top-level object"):
        OperatorRecordJsonSerializer().deserialize(text)


def test_method__deserialize__duplicate_object_key__raises_value_error() -> None:
    r"""Evidence ID
    SV-ORJS-020
    Requirement
    Duplicate JSON object keys are rejected rather than resolved by ordering.
    Method
    Deserialize text containing two ``schema_version`` keys.
    Oracle
    The strict wire contract forbids duplicate keys.
    Acceptance
    Exactly ``ValueError`` identifies duplication.
    Interpretation
    A pass confirms strict object parsing; failure indicates parser policy drift.
    Limitations
    Other malformed JSON, validation, UQ, and Rust are excluded.
    """
    with pytest.raises(ValueError, match="duplicate"):
        OperatorRecordJsonSerializer().deserialize(
            '{"schema_version":1,"schema_version":1}'
        )


@pytest.mark.parametrize(
    "constant",
    [
        pytest.param("NaN", id="nan_constant"),
        pytest.param("Infinity", id="positive_infinity_constant"),
        pytest.param("-Infinity", id="negative_infinity_constant"),
    ],
)
def test_method__deserialize__nonstandard_numeric_constant__raises_value_error(
    constant: str,
) -> None:
    r"""Evidence ID
    SV-ORJS-021
    Requirement
    Nonstandard nonfinite JSON numeric constants are rejected at parse time.
    Method
    Place each fixed token in the schema-version field of an object.
    Oracle
    RFC-compatible JSON numbers exclude NaN and infinities.
    Acceptance
    Exactly ``ValueError`` identifies a nonstandard constant.
    Interpretation
    A pass confirms strict numeric parsing; failure indicates parser drift.
    Limitations
    Finite semantic values, validation, UQ, and Rust are excluded.
    """
    with pytest.raises(ValueError, match="nonstandard"):
        OperatorRecordJsonSerializer().deserialize(
            '{"schema_version":' + constant + "}"
        )


@pytest.mark.parametrize(
    ("path", "remove", "extra"),
    [
        pytest.param((), "basis", None, id="top_missing"),
        pytest.param((), None, "extra", id="top_unknown"),
        pytest.param(("state_space",), "kind", None, id="state_space_missing"),
        pytest.param(("state_space",), None, "extra", id="state_space_unknown"),
        pytest.param(("basis",), "kind", None, id="basis_missing"),
        pytest.param(("basis",), None, "extra", id="basis_unknown"),
        pytest.param(("geometry",), "system", None, id="geometry_missing"),
        pytest.param(("geometry",), None, "extra", id="geometry_unknown"),
        pytest.param(
            ("energy_reference",), "unit", None, id="energy_reference_missing"
        ),
        pytest.param(
            ("energy_reference",), None, "value", id="energy_reference_unknown_value"
        ),
    ],
)
def test_field__exact_fields_at_every_structured_object_level__is_exact(
    path: tuple[str, ...], remove: str | None, extra: str | None
) -> None:
    r"""Evidence ID
    SV-ORJS-008
    Requirement
    OperatorRecordJsonSerializer enforces this version-1 JSON boundary partition: exact
    fields at every structured object level: is exact.
    Method
    Invoke serialize() or deserialize() on the explicit schema-version-1 partition
    (exact fields at every structured object level: is exact); warnings and coercive
    fallback behavior are not accepted.
    Oracle
    The public version-1 schema, fixed wire-field vocabulary, literal JSON grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.
    Acceptance
    The named partition raises exactly ValueError with the asserted public message,
    code, or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    payload: dict[str, Any] = valid_payload()
    target = payload if not path else payload[path[0]]
    if remove is not None:
        del target[remove]
    else:
        assert extra is not None
        target[extra] = 0
    with pytest.raises(ValueError, match="missing|unknown"):
        OperatorRecordJsonSerializer().deserialize(json.dumps(payload))


@pytest.mark.parametrize(
    "version",
    [
        pytest.param(True, id="true"),
        pytest.param(False, id="false"),
        pytest.param(1.0, id="float_one"),
        pytest.param("1", id="numeric_string"),
        pytest.param(None, id="null"),
        pytest.param([], id="array"),
        pytest.param({}, id="object"),
        pytest.param(0, id="zero"),
        pytest.param(2, id="two"),
        pytest.param(-1, id="negative"),
    ],
)
def test_method__deserialize__schema_version_is_exact_integer_one(version: Any) -> None:
    r"""Evidence ID
    SV-ORJS-009
    Requirement
    OperatorRecordJsonSerializer enforces this version-1 JSON boundary partition:
    deserialize: schema version is exact integer one.
    Method
    Invoke serialize() or deserialize() on the explicit schema-version-1 partition
    (deserialize: schema version is exact integer one); warnings and coercive fallback
    behavior are not accepted.
    Oracle
    The public version-1 schema, fixed wire-field vocabulary, literal JSON grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.
    Acceptance
    The named partition raises exactly expected with the asserted public message, code,
    or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    payload = valid_payload()
    payload["schema_version"] = version
    expected = ValueError if type(version) is int else TypeError
    with pytest.raises(expected):
        OperatorRecordJsonSerializer().deserialize(json.dumps(payload))


@pytest.mark.parametrize(
    ("matrix", "expected", "message"),
    [
        pytest.param(1, TypeError, "array", id="scalar"),
        pytest.param([1], TypeError, "rows", id="row_scalar"),
        pytest.param([[1.0]], ValueError, "pairs", id="rank_two"),
        pytest.param([[[1.0]]], ValueError, "pairs", id="short_pair"),
        pytest.param([[[1.0, 0.0, 2.0]]], ValueError, "pairs", id="long_pair"),
        pytest.param(
            [[[1.0, 0.0]], [[1.0, 0.0], [2.0, 0.0]]], ValueError, "ragged", id="ragged"
        ),
        pytest.param([[[1.0, 0.0], [2.0, 0.0]]], ValueError, "square", id="nonsquare"),
        pytest.param([], ValueError, "empty", id="no_rows"),
        pytest.param([[]], ValueError, "empty", id="empty_row"),
    ],
)
def test_field__matrix_container_pair_rank_and_shape_rules__is_exact(
    matrix: Any, expected: type[Exception], message: str
) -> None:
    r"""Evidence ID
    SV-ORJS-010
    Requirement
    OperatorRecordJsonSerializer enforces this version-1 JSON boundary partition: matrix
    container pair rank and shape rules: is exact.
    Method
    Invoke serialize() or deserialize() on the explicit schema-version-1 partition
    (matrix container pair rank and shape rules: is exact); warnings and coercive
    fallback behavior are not accepted.
    Oracle
    The public version-1 schema, fixed wire-field vocabulary, literal JSON grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.
    Acceptance
    The named partition raises exactly expected with the asserted public message, code,
    or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    payload = valid_payload()
    payload["matrix"] = matrix
    with pytest.raises(expected, match=message):
        OperatorRecordJsonSerializer().deserialize(json.dumps(payload))


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("state_space", id="state_space_object"),
        pytest.param("basis", id="basis_object"),
        pytest.param("geometry", id="geometry_object"),
        pytest.param("energy_reference", id="energy_reference_object"),
        pytest.param("provenance", id="provenance_object"),
    ],
)
def test_method__deserialize__nested_records_require_json_object_containers(
    field: str,
) -> None:
    r"""Evidence ID
    SV-ORJS-011
    Requirement
    OperatorRecordJsonSerializer enforces this version-1 JSON boundary partition:
    deserialize: nested records require json object containers.
    Method
    Invoke serialize() or deserialize() on the explicit schema-version-1 partition
    (deserialize: nested records require json object containers); warnings and coercive
    fallback behavior are not accepted.
    Oracle
    The public version-1 schema, fixed wire-field vocabulary, literal JSON grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.
    Acceptance
    The named partition raises exactly TypeError with the asserted public message, code,
    or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    payload = valid_payload()
    payload[field] = []
    with pytest.raises(TypeError, match="JSON object"):
        OperatorRecordJsonSerializer().deserialize(json.dumps(payload))
