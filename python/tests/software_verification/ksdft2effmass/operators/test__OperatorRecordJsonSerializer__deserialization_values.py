r"""Software verification of ``OperatorRecordJsonSerializer``.

Facet and represented meaning

-----------------------------
This class-owned module owns the deserialization values facet. Object: serializer
scalar/container value admission and DataObject propagation.
Evidence class: software verification. Requirement: JSON meanings remain strict,
numeric booleans/strings and nonfinite/overflow values are rejected, provenance
is string-to-string, and intrinsic/cross-field DataObject invariants propagate.
Strategy: change one value in valid serialized state. Oracle: approved serializer
and public DataObject contracts, not private decoder methods. Acceptance uses exact
TypeError/ValueError categories. Passing does not constitute scientific validation,
uncertainty quantification, or Rust conformance; failure requires investigation.

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
from functools import reduce
from typing import Any

import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordJsonSerializer


def mutated(path: tuple[str | int, ...], value: Any) -> str:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Value-deserialization cases require deterministic replacement of one
    declared JSON
    path while all other payload values remain valid.

    Method: Construct or inspect only the named synthetic fixture operation (mutated);
    the
    helper owns no assertion result and introduces no hidden oracle.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: The helper returns exactly the requested fixture value or applies only
    the
    documented comparison; all pass/fail assertions remain in the owning test.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    payload: Any = json.loads(OperatorRecordJsonSerializer().serialize(make_record()))
    target = reduce(lambda current, key: current[key], path[:-1], payload)
    target[path[-1]] = value
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def raw_number(path: tuple[str | int, ...], token: str) -> str:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Overflow evidence requires inserting one raw JSON numeric token without
    accidental
    string coercion by the test fixture.

    Method: Construct or inspect only the named synthetic fixture operation (raw
    number); the
    helper owns no assertion result and introduces no hidden oracle.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: The helper returns exactly the requested fixture value or applies only
    the
    documented comparison; all pass/fail assertions remain in the owning test.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    return mutated(path, "__RAW__").replace('"__RAW__"', token)


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(("schema_version",), id="schema_version"),
        pytest.param(("state_space", "dimension"), id="dimension"),
        pytest.param(("matrix", 0, 0, 0), id="matrix_real"),
        pytest.param(("matrix", 0, 0, 1), id="matrix_imaginary"),
        pytest.param(("geometry", "cell", 0, 0), id="cell_component"),
    ],
)
def test_method__deserialize__booleans_are_not_numeric_values(
    path: tuple[str | int, ...],
) -> None:
    r"""Evidence ID: SV-ORJS-012

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    deserialize: booleans are not numeric values.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (deserialize: booleans are not numeric values); warnings and coercive fallback
    behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: The named partition raises exactly TypeError with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    with pytest.raises(TypeError, match="integer|real number"):
        OperatorRecordJsonSerializer().deserialize(mutated(path, True))


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(("schema_version",), id="schema_version"),
        pytest.param(("state_space", "dimension"), id="dimension"),
        pytest.param(("matrix", 0, 0, 0), id="matrix_real"),
        pytest.param(("matrix", 0, 0, 1), id="matrix_imaginary"),
        pytest.param(("geometry", "cell", 0, 0), id="cell_component"),
    ],
)
def test_method__deserialize__numeric_strings_are_not_numbers(
    path: tuple[str | int, ...],
) -> None:
    r"""Evidence ID: SV-ORJS-013

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    deserialize: numeric strings are not numbers.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (deserialize: numeric strings are not numbers); warnings and coercive fallback
    behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: The named partition raises exactly TypeError with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    with pytest.raises(TypeError, match="integer|real number"):
        OperatorRecordJsonSerializer().deserialize(mutated(path, "1"))


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(("matrix", 0, 0, 0), id="matrix_real"),
        pytest.param(("matrix", 0, 0, 1), id="matrix_imaginary"),
        pytest.param(("geometry", "cell", 0, 0), id="cell_component"),
    ],
)
@pytest.mark.parametrize(
    "sign",
    [
        pytest.param("positive", id="positive"),
        pytest.param("negative", id="negative"),
    ],
)
def test_constructor__numeric_overflow_maps_to_finite_value_error__is_enforced(
    path: tuple[str | int, ...], sign: str
) -> None:
    r"""Evidence ID: SV-ORJS-014

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    numeric overflow maps to finite value error: is enforced.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (numeric overflow maps to finite value error: is enforced); warnings and coercive
    fallback behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: The named partition raises exactly ValueError with the asserted public
    message,
    code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    token = "1" + "0" * 10000
    if sign == "negative":
        token = "-" + token
    with pytest.raises(ValueError, match="finite"):
        OperatorRecordJsonSerializer().deserialize(raw_number(path, token))


@pytest.mark.parametrize(
    ("path", "value", "expected"),
    [
        pytest.param(("identifier",), 1, TypeError, id="identifier_type"),
        pytest.param(("operator_kind",), "", ValueError, id="operator_kind_empty"),
        pytest.param(
            ("state_space", "identifier"), "", ValueError, id="state_id_empty"
        ),
        pytest.param(("basis", "ordering"), "a", TypeError, id="ordering_container"),
        pytest.param(("basis", "ordering"), ["a", 2], TypeError, id="ordering_label"),
        pytest.param(("basis", "orthonormal"), 1, TypeError, id="orthonormal_type"),
        pytest.param(("provenance",), {"source": 1}, TypeError, id="provenance_value"),
        pytest.param(
            ("provenance",), {"": "value"}, ValueError, id="provenance_key_empty"
        ),
    ],
)
def test_method__deserialize__json_scalar_and_container_semantics(
    path: tuple[str | int, ...], value: Any, expected: type[Exception]
) -> None:
    r"""Evidence ID: SV-ORJS-015

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    deserialize: json scalar and container semantics.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (deserialize: json scalar and container semantics); warnings and coercive fallback
    behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: The named partition raises exactly expected with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    with pytest.raises(expected):
        OperatorRecordJsonSerializer().deserialize(mutated(path, value))


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        pytest.param(
            ("state_space", "dimension"), 3, "dimension", id="dimension_mismatch"
        ),
        pytest.param(("basis", "ordering"), ["a", "a"], "unique", id="duplicate_label"),
        pytest.param(
            ("basis", "orthonormal"), False, "orthonormal", id="nonorthogonal_record"
        ),
        pytest.param(
            ("geometry", "cell"),
            [[1, 0, 0], [2, 0, 0], [3, 0, 0]],
            "independent",
            id="singular_cell",
        ),
        pytest.param(
            ("geometry", "cell"), [[1, 0, 0], [0, 1, 0]], "three", id="cell_row_count"
        ),
    ],
)
def test_method__deserialize__public_dataobject_invariants_propagate(
    path: tuple[str | int, ...], value: Any, message: str
) -> None:
    r"""Evidence ID: SV-ORJS-016

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    deserialize: public dataobject invariants propagate.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (deserialize: public dataobject invariants propagate); warnings and coercive
    fallback behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: The named partition raises exactly ValueError with the asserted public
    message,
    code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    with pytest.raises(ValueError, match=message):
        OperatorRecordJsonSerializer().deserialize(mutated(path, value))
