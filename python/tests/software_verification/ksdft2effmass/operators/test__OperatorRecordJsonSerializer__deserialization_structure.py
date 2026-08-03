"""OperatorRecordJsonSerializer structural decoding software verification.

Object: serializer JSON parser and version-1 object/matrix structure boundary.
Evidence class: software verification. Requirement: strict JSON text, unique keys,
standard constants, exact object fields, exact integer version, and rectangular
square complex-pair matrices. Strategy: mutate one independently valid payload at
a time. Oracle: approved grammar and field tables, independent of private methods.
Acceptance requires documented TypeError/ValueError categories. Passing is not
scientific validation, UQ, or Rust conformance; failure indicates runtime,
specification, documentation, or evidence drift.
"""

import json
from typing import Any

import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification


def valid_payload() -> dict[str, Any]:
    """Support SV-ORJS-007 through SV-ORJS-011 with fresh valid JSON state.

    Evidence ID: supporting helper (no executable owner). Requirement: mutations
    begin from valid version-1 text. Method: public serialization followed by the
    independent standard parser. Oracle: successful public construction.
    Interpretation: isolates one mutation per case. Limitations: the helper is not
    evidence itself and performs no scientific validation, UQ, or Rust conformance.
    """
    return json.loads(OperatorRecordJsonSerializer().serialize(make_record()))


def test_malformed_nonobject_duplicate_and_constant_rejection() -> None:
    """Evidence ID: SV-ORJS-007.

    Requirement: reject malformed JSON, nonobject roots, duplicate keys, and
    nonstandard constants. Method: submit literal boundary texts with readable IDs.
    Oracle: standard JSON object grammar plus approved duplicate/constant policy.
    Acceptance is ValueError for malformed/duplicate/constants and TypeError for
    valid nonobject roots. Interpretation: failure is parser-boundary drift.
    Limitations: dependency parser internals, scientific validation, UQ, and Rust
    conformance are not validated.
    """
    serializer = OperatorRecordJsonSerializer()
    for text in ("{",):
        with pytest.raises(ValueError):
            serializer.deserialize(text)
    for text in ("[]", "null", '"record"', "1"):
        with pytest.raises(TypeError, match="top-level object"):
            serializer.deserialize(text)
    with pytest.raises(ValueError, match="duplicate"):
        serializer.deserialize('{"schema_version":1,"schema_version":1}')
    for constant in ("NaN", "Infinity", "-Infinity"):
        with pytest.raises(ValueError, match="nonstandard"):
            serializer.deserialize('{"schema_version":' + constant + "}")


@pytest.mark.parametrize(
    ("path", "remove", "extra"),
    [
        ((), "basis", None),
        ((), None, "extra"),
        (("state_space",), "kind", None),
        (("state_space",), None, "extra"),
        (("basis",), "kind", None),
        (("basis",), None, "extra"),
        (("geometry",), "system", None),
        (("geometry",), None, "extra"),
        (("energy_reference",), "unit", None),
        (("energy_reference",), None, "value"),
    ],
    ids=[
        "top-missing",
        "top-unknown",
        "state-space-missing",
        "state-space-unknown",
        "basis-missing",
        "basis-unknown",
        "geometry-missing",
        "geometry-unknown",
        "energy-reference-missing",
        "energy-reference-unknown-value",
    ],
)
def test_exact_fields_at_every_structured_object_level(
    path: tuple[str, ...], remove: str | None, extra: str | None
) -> None:
    """Evidence ID: SV-ORJS-008.

    Requirement: fixed fields are required and unknown fields rejected at every
    declared record object level. Method: delete or add one field in fresh valid
    state. Oracle: approved exact version-1 field table. Acceptance is ValueError.
    Interpretation: failure permits ambiguous or incomplete wire objects.
    Limitations: arbitrary provenance names are intentionally excluded; no
    scientific validation, UQ, or Rust conformance is performed.
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
    [True, False, 1.0, "1", None, [], {}, 0, 2, -1],
    ids=[
        "true",
        "false",
        "float-one",
        "numeric-string",
        "null",
        "array",
        "object",
        "zero",
        "two",
        "negative",
    ],
)
def test_schema_version_is_exact_integer_one(version: Any) -> None:
    """Evidence ID: SV-ORJS-009.

    Requirement: schema_version is the exact JSON integer 1. Method: replace only
    that field with wrong semantic types or unsupported integers. Oracle: approved
    version constant and JSON scalar semantics. Acceptance is TypeError for non-int
    and ValueError for other ints. Interpretation: failure broadens compatibility.
    Limitations: no migration policy, scientific validation, UQ, or Rust conformance
    is established.
    """
    payload = valid_payload()
    payload["schema_version"] = version
    expected = ValueError if type(version) is int else TypeError
    with pytest.raises(expected):
        OperatorRecordJsonSerializer().deserialize(json.dumps(payload))


@pytest.mark.parametrize(
    ("matrix", "expected", "message"),
    [
        (1, TypeError, "array"),
        ([1], TypeError, "rows"),
        ([[1.0]], ValueError, "pairs"),
        ([[[1.0]]], ValueError, "pairs"),
        ([[[1.0, 0.0, 2.0]]], ValueError, "pairs"),
        ([[[1.0, 0.0]], [[1.0, 0.0], [2.0, 0.0]]], ValueError, "ragged"),
        ([[[1.0, 0.0], [2.0, 0.0]]], ValueError, "square"),
        ([], ValueError, "empty"),
        ([[]], ValueError, "empty"),
    ],
    ids=[
        "scalar",
        "row-scalar",
        "rank-two",
        "short-pair",
        "long-pair",
        "ragged",
        "nonsquare",
        "no-rows",
        "empty-row",
    ],
)
def test_matrix_container_pair_rank_and_shape_rules(
    matrix: Any, expected: type[Exception], message: str
) -> None:
    """Evidence ID: SV-ORJS-010.

    Requirement: matrix is nonempty square rows of exact two-number pairs. Method:
    replace matrix with one malformed structural family. Oracle: N-by-N-by-2 wire
    shape. Acceptance is the documented TypeError/ValueError and diagnostic class.
    Interpretation: failure means malformed structure escaped or taxonomy drifted.
    Limitations: numeric value semantics are separate; no scientific validation,
    UQ, or Rust conformance is performed.
    """
    payload = valid_payload()
    payload["matrix"] = matrix
    with pytest.raises(expected, match=message):
        OperatorRecordJsonSerializer().deserialize(json.dumps(payload))


def test_nested_records_require_json_object_containers() -> None:
    """Evidence ID: SV-ORJS-011.

    Requirement: each nested structured record and provenance is a JSON object.
    Method: replace each with an array. Oracle: approved container field table.
    Acceptance is field-boundary TypeError. Interpretation: failure indicates JSON
    container coercion. Limitations: nested values are tested elsewhere; no
    scientific validation, UQ, or Rust conformance is established.
    """
    for field in ("state_space", "basis", "geometry", "energy_reference", "provenance"):
        payload = valid_payload()
        payload[field] = []
        with pytest.raises(TypeError, match="JSON object"):
            OperatorRecordJsonSerializer().deserialize(json.dumps(payload))
