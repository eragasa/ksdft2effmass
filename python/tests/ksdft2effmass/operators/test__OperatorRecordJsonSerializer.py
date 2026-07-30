"""Software-verification tests for the public operator-record API.

These tests exercise object construction, invariants, numerical policies, and
serialization or comparison contracts for maintained first-party Python code.
They are software verification checks and do not constitute scientific
validation of a represented Hamiltonian or reduced model.
"""

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    OperatorRecord,
    OperatorRecordJsonSerializer,
    StateSpace,
)

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0))
SPEC_DIR = (
    Path(__file__).resolve().parents[4] / "specification" / "operator-record" / "v1"
)


def make_record() -> OperatorRecord:
    return OperatorRecord(
        "synthetic-two-level",
        "finite_test_hamiltonian",
        np.array([[1.0, 0.25j], [-0.25j, 2.0]]),
        StateSpace("H_test", "finite synthetic", 2),
        Basis("canonical", "test basis", ("a", "b"), True),
        Geometry(
            "synthetic",
            VALID_CELL,
            "finite synthetic",
            "cartesian row lattice vectors",
            "angstrom",
        ),
        EnergyReference("explicit zero", "eV"),
        {"z_source": "unit test", "a_code": "pytest"},
    )


def fixture_text(kind: str, name: str) -> str:
    return (SPEC_DIR / kind / name).read_text()


def canonicalize(text: str) -> str:
    return json.dumps(json.loads(text), sort_keys=True, separators=(",", ":"))


def mutated_text(field_path: tuple[str | int, ...], value: Any) -> str:
    payload = json.loads(OperatorRecordJsonSerializer().serialize(make_record()))
    target: Any = payload
    for key in field_path[:-1]:
        target = target[key]
    target[field_path[-1]] = value
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def test_public_import_constructs_serializer() -> None:
    serializer = OperatorRecordJsonSerializer()

    assert serializer.SCHEMA_VERSION == 1


def test_obsolete_codec_import_is_absent() -> None:
    import ksdft2effmass.operators as operators

    assert not hasattr(operators, "OperatorRecordJsonCodec")


def test_serialize_emits_deterministic_json_text() -> None:
    text = OperatorRecordJsonSerializer().serialize(make_record())

    assert isinstance(text, str)
    assert text == OperatorRecordJsonSerializer().serialize(make_record())
    assert text == canonicalize(text)
    payload = json.loads(text)
    assert payload["schema_version"] == 1
    assert payload["matrix"] == [
        [[1.0, 0.0], [0.0, 0.25]],
        [[0.0, -0.25], [2.0, 0.0]],
    ]
    assert payload["provenance"] == {"a_code": "pytest", "z_source": "unit test"}


def test_serialize_requires_operator_record() -> None:
    with pytest.raises(TypeError, match="OperatorRecord"):
        OperatorRecordJsonSerializer().serialize({})  # type: ignore[arg-type]


def test_deserialize_requires_json_text() -> None:
    with pytest.raises(TypeError, match="JSON text"):
        OperatorRecordJsonSerializer().deserialize({})  # type: ignore[arg-type]


def test_serialize_deserialize_round_trip_preserves_exact_record() -> None:
    serializer = OperatorRecordJsonSerializer()
    record = make_record()

    restored = serializer.deserialize(serializer.serialize(record))

    assert restored == record
    assert not restored.matrix.flags.writeable
    assert isinstance(restored.provenance, Mapping)


@pytest.mark.parametrize(
    "name, expected_error",
    [
        ("missing-field.json", ValueError),
        ("unknown-field.json", ValueError),
        ("unsupported-version.json", ValueError),
        ("numeric-string.json", TypeError),
        ("boolean-as-number.json", TypeError),
        ("duplicate-basis-label.json", ValueError),
        ("nonorthogonal-basis.json", ValueError),
        ("ragged-matrix.json", ValueError),
        ("nonsquare-matrix.json", ValueError),
        ("dimension-mismatch.json", ValueError),
        ("empty-string.json", ValueError),
        ("singular-cell.json", ValueError),
        ("energy-reference-value.json", ValueError),
    ],
)
def test_invalid_fixtures_are_rejected(
    name: str, expected_error: type[TypeError] | type[ValueError]
) -> None:
    with pytest.raises(expected_error):
        OperatorRecordJsonSerializer().deserialize(fixture_text("invalid", name))


@pytest.mark.parametrize(
    "text, expected_error", [("{", ValueError), ("[]", TypeError), ("null", TypeError)]
)
def test_deserialize_rejects_malformed_or_nontop_object_json(
    text: str, expected_error: type[TypeError] | type[ValueError]
) -> None:
    with pytest.raises(expected_error):
        OperatorRecordJsonSerializer().deserialize(text)


def test_deserialize_rejects_duplicate_object_keys() -> None:
    text = '{"schema_version":1,"schema_version":1}'

    with pytest.raises(ValueError, match="duplicate"):
        OperatorRecordJsonSerializer().deserialize(text)


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_deserialize_rejects_nonstandard_json_constants(constant: str) -> None:
    text = mutated_text(("matrix", 0, 0, 0), 0.0).replace("0.0", constant, 1)

    with pytest.raises(ValueError, match="nonstandard"):
        OperatorRecordJsonSerializer().deserialize(text)


@pytest.mark.parametrize(
    "field_path, value",
    [
        (("schema_version",), True),
        (("state_space", "dimension"), False),
        (("matrix", 0, 0, 0), True),
        (("geometry", "cell", 0, 0), False),
    ],
)
def test_deserialize_rejects_booleans_where_numbers_are_required(
    field_path: tuple[str | int, ...], value: Any
) -> None:
    with pytest.raises(TypeError, match="real number|integer"):
        OperatorRecordJsonSerializer().deserialize(mutated_text(field_path, value))


@pytest.mark.parametrize(
    "field_path, value",
    [
        (("geometry", "cell", 0, 0), "1.0"),
        (("matrix", 0, 0, 0), "1.0"),
        (("matrix", 0, 0, 1), "0.0"),
        (("state_space", "dimension"), "2"),
        (("schema_version",), "1"),
    ],
)
def test_deserialize_rejects_numeric_strings(
    field_path: tuple[str | int, ...], value: str
) -> None:
    with pytest.raises(TypeError, match="real number|integer"):
        OperatorRecordJsonSerializer().deserialize(mutated_text(field_path, value))


def test_deserialize_rejects_missing_and_unknown_fields() -> None:
    payload = json.loads(OperatorRecordJsonSerializer().serialize(make_record()))
    del payload["basis"]
    with pytest.raises(ValueError, match="missing"):
        OperatorRecordJsonSerializer().deserialize(json.dumps(payload))

    payload = json.loads(OperatorRecordJsonSerializer().serialize(make_record()))
    payload["energy_reference"]["value"] = 0.0
    with pytest.raises(ValueError, match="unknown"):
        OperatorRecordJsonSerializer().deserialize(json.dumps(payload))


@pytest.mark.parametrize(
    "matrix, message",
    [
        ([[[1.0, 0.0, 2.0]]], "pairs"),
        ([[[1.0, 0.0]], [[1.0, 0.0], [2.0, 0.0]]], "ragged"),
        ([[1.0]], "pairs"),
        ([[[1.0, 0.0], [2.0, 0.0]]], "square"),
    ],
)
def test_deserialize_rejects_complex_pair_ragged_and_nonsquare_matrices(
    matrix: Any, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        OperatorRecordJsonSerializer().deserialize(mutated_text(("matrix",), matrix))


def test_specific_invalid_semantics_are_rejected() -> None:
    serializer = OperatorRecordJsonSerializer()
    cases = [
        (("state_space", "dimension"), 3, "dimension"),
        (("basis", "ordering"), ["a", "a"], "unique"),
        (("basis", "orthonormal"), False, "orthonormal"),
        (("geometry", "cell"), [[1, 0, 0], [2, 0, 0], [3, 0, 0]], "independent"),
    ]
    for path, value, message in cases:
        with pytest.raises(ValueError, match=message):
            serializer.deserialize(mutated_text(path, value))
