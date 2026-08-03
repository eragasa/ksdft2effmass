"""OperatorRecordJsonSerializer decoded-value software verification.

Object: serializer scalar/container value admission and DataObject propagation.
Evidence class: software verification. Requirement: JSON meanings remain strict,
numeric booleans/strings and nonfinite/overflow values are rejected, provenance
is string-to-string, and intrinsic/cross-field DataObject invariants propagate.
Strategy: change one value in valid serialized state. Oracle: approved serializer
and public DataObject contracts, not private decoder methods. Acceptance uses exact
TypeError/ValueError categories. Passing does not constitute scientific validation,
uncertainty quantification, or Rust conformance; failure requires investigation.
"""

import json
from typing import Any

import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification


def mutated(path: tuple[str | int, ...], value: Any) -> str:
    """Support SV-ORJS-012 through SV-ORJS-016 with one public payload mutation.

    Evidence ID: supporting helper (no executable owner). Requirement: cases differ
    from valid state at one explicit path. Method: public serialization, independent
    parsing, direct assignment, and standard dumping. Oracle: unchanged valid base.
    Interpretation: isolates the named rejected value. Limitations: not independent
    evidence; no scientific validation, UQ, or Rust conformance is performed.
    """
    payload: Any = json.loads(OperatorRecordJsonSerializer().serialize(make_record()))
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def raw_number(path: tuple[str | int, ...], token: str) -> str:
    """Support SV-ORJS-014 controlled interpreter-overflow boundary evidence.

    Evidence ID: supporting helper (no executable owner). Requirement: exercise a
    JSON numeric token too large for finite binary64 without converting it first.
    Method: insert a sentinel then replace its quoted spelling with the token.
    Oracle: approved finite-number taxonomy. Interpretation: controls only input
    text; it does not validate Python's parser. Limitations: no scientific
    validation, UQ, or Rust conformance is performed.
    """
    return mutated(path, "__RAW__").replace('"__RAW__"', token)


@pytest.mark.parametrize(
    "path",
    [
        ("schema_version",),
        ("state_space", "dimension"),
        ("matrix", 0, 0, 0),
        ("matrix", 0, 0, 1),
        ("geometry", "cell", 0, 0),
    ],
    ids=[
        "schema-version",
        "dimension",
        "matrix-real",
        "matrix-imaginary",
        "cell-component",
    ],
)
def test_booleans_are_not_numeric_values(path: tuple[str | int, ...]) -> None:
    """Evidence ID: SV-ORJS-012.

    Requirement: JSON booleans are never integers/reals. Method: inject true at
    each numeric role. Oracle: JSON scalar semantics and approved no-bool policy.
    Acceptance is TypeError. Interpretation: failure indicates Python bool/int
    leakage. Limitations: orthonormal intentionally accepts Boolean; no scientific
    validation, UQ, or Rust conformance is performed.
    """
    with pytest.raises(TypeError, match="integer|real number"):
        OperatorRecordJsonSerializer().deserialize(mutated(path, True))


@pytest.mark.parametrize(
    "path",
    [
        ("schema_version",),
        ("state_space", "dimension"),
        ("matrix", 0, 0, 0),
        ("matrix", 0, 0, 1),
        ("geometry", "cell", 0, 0),
    ],
    ids=[
        "schema-version",
        "dimension",
        "matrix-real",
        "matrix-imaginary",
        "cell-component",
    ],
)
def test_numeric_strings_are_not_numbers(path: tuple[str | int, ...]) -> None:
    """Evidence ID: SV-ORJS-013.

    Requirement: numeric-looking strings are not converted. Method: inject ``"1"``
    at each numeric role. Oracle: JSON type semantics. Acceptance is TypeError.
    Interpretation: failure broadens wire meaning through coercion. Limitations:
    strings remain valid in textual roles; no scientific validation, UQ, or Rust
    conformance is performed.
    """
    with pytest.raises(TypeError, match="integer|real number"):
        OperatorRecordJsonSerializer().deserialize(mutated(path, "1"))


@pytest.mark.parametrize(
    "path",
    [("matrix", 0, 0, 0), ("matrix", 0, 0, 1), ("geometry", "cell", 0, 0)],
    ids=["matrix-real", "matrix-imaginary", "cell-component"],
)
@pytest.mark.parametrize("sign", ["positive", "negative"], ids=["positive", "negative"])
def test_numeric_overflow_maps_to_finite_value_error(
    path: tuple[str | int, ...], sign: str
) -> None:
    """Evidence ID: SV-ORJS-014.

    Requirement: huge standard JSON integers in real roles map to finite ValueError.
    Method: inject a signed 10,001-digit token, which valid constructed records
    cannot contain because DataObjects already reject it. Oracle: approved public
    overflow taxonomy. Acceptance is ValueError mentioning finite. Interpretation:
    failure leaks interpreter behavior or admits nonfinite state. Limitations: this
    controlled parser boundary does not validate Python integer parsing, scientific
    validation, UQ, or Rust conformance.
    """
    token = "1" + "0" * 10000
    if sign == "negative":
        token = "-" + token
    with pytest.raises(ValueError, match="finite"):
        OperatorRecordJsonSerializer().deserialize(raw_number(path, token))


@pytest.mark.parametrize(
    ("path", "value", "expected"),
    [
        (("identifier",), 1, TypeError),
        (("operator_kind",), "", ValueError),
        (("state_space", "identifier"), "", ValueError),
        (("basis", "ordering"), "a", TypeError),
        (("basis", "ordering"), ["a", 2], TypeError),
        (("basis", "orthonormal"), 1, TypeError),
        (("provenance",), {"source": 1}, TypeError),
        (("provenance",), {"": "value"}, ValueError),
    ],
    ids=[
        "identifier-type",
        "operator-kind-empty",
        "state-id-empty",
        "ordering-container",
        "ordering-label",
        "orthonormal-type",
        "provenance-value",
        "provenance-key-empty",
    ],
)
def test_json_scalar_and_container_semantics(
    path: tuple[str | int, ...], value: Any, expected: type[Exception]
) -> None:
    """Evidence ID: SV-ORJS-015.

    Requirement: textual, array, Boolean, and provenance roles retain exact JSON
    meanings. Method: inject one wrong value family. Oracle: version-1 field types
    and nonempty-string rules. Acceptance is stated exact exception category.
    Interpretation: failure indicates coercion or taxonomy drift. Limitations: no
    physical metadata interpretation, scientific validation, UQ, or Rust
    conformance is performed.
    """
    with pytest.raises(expected):
        OperatorRecordJsonSerializer().deserialize(mutated(path, value))


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("state_space", "dimension"), 3, "dimension"),
        (("basis", "ordering"), ["a", "a"], "unique"),
        (("basis", "orthonormal"), False, "orthonormal"),
        (("geometry", "cell"), [[1, 0, 0], [2, 0, 0], [3, 0, 0]], "independent"),
        (("geometry", "cell"), [[1, 0, 0], [0, 1, 0]], "three"),
    ],
    ids=[
        "dimension-mismatch",
        "duplicate-label",
        "nonorthogonal-record",
        "singular-cell",
        "cell-row-count",
    ],
)
def test_public_dataobject_invariants_propagate(
    path: tuple[str | int, ...], value: Any, message: str
) -> None:
    """Evidence ID: SV-ORJS-016.

    Requirement: deserialization constructs public DataObjects and propagates their
    intrinsic/cross-field invariants. Method: inject independently meaningful valid-
    JSON values violating one public invariant. Oracle: approved DataObject contract.
    Acceptance is ValueError with relevant diagnostic. Interpretation: failure means
    invalid record state escaped. Limitations: this does not duplicate full owner
    facet coverage or establish scientific validation, UQ, or Rust conformance.
    """
    with pytest.raises(ValueError, match=message):
        OperatorRecordJsonSerializer().deserialize(mutated(path, value))
