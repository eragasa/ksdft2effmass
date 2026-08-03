"""OperatorRecordJsonSerializer encoding software verification.

Object: serializer ``serialize`` behavior. Evidence class: software verification.
Requirement: deterministic sorted compact JSON with nine exact top-level fields,
all eight record fields, and row-major ``[real, imaginary]`` complex entries.
Strategy: serialize an independently constructed synthetic record and compare with
an independently assembled JSON object/text oracle. Acceptance is exact text and
value equality. Passing is wire-encoding conformance, not scientific validation,
uncertainty quantification, or Rust conformance; failure requires contract/source/
evidence investigation.
"""

import json

import numpy as np
import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification


def test_serialization_is_sorted_compact_and_deterministic() -> None:
    """Evidence ID: SV-ORJS-004.

    Requirement: equal records emit identical sorted compact JSON text. Method:
    serialize twice and compare with independent ``json.dumps`` canonicalization.
    Oracle: Python's standard JSON parser/dumper configured by the public contract.
    Acceptance is exact string equality and absence of formatting whitespace.
    Interpretation: failure indicates nondeterminism or formatting drift.
    Limitations: parser correctness, scientific validation, UQ, and Rust conformance
    are not established.
    """
    serializer = OperatorRecordJsonSerializer()
    text = serializer.serialize(make_record(provenance={"z": "last", "a": "first"}))
    assert text == serializer.serialize(
        make_record(provenance={"a": "first", "z": "last"})
    )
    assert text == json.dumps(json.loads(text), sort_keys=True, separators=(",", ":"))
    assert "\n" not in text and ": " not in text and ", " not in text


def test_serialization_emits_exact_nested_fields_and_values() -> None:
    """Evidence ID: SV-ORJS-005.

    Requirement: version one encodes every record field under fixed exact names.
    Method: decode emitted text with the independent standard JSON parser and
    compare every object to literal expected values. Oracle: approved field table.
    Acceptance is exact key sets and metadata values. Interpretation: failure is a
    schema mapping regression. Limitations: schema-validator behavior, scientific
    validation, UQ, and Rust conformance are not tested.
    """
    payload = json.loads(OperatorRecordJsonSerializer().serialize(make_record()))
    assert set(payload) == {
        "schema_version",
        "identifier",
        "operator_kind",
        "matrix",
        "state_space",
        "basis",
        "geometry",
        "energy_reference",
        "provenance",
    }
    assert payload["schema_version"] == 1
    assert payload["identifier"] == "synthetic-two-level"
    assert payload["operator_kind"] == "finite_test_hamiltonian"
    assert payload["state_space"] == {
        "identifier": "H_test",
        "kind": "finite synthetic",
        "dimension": 2,
    }
    assert payload["basis"] == {
        "identifier": "canonical",
        "kind": "test basis",
        "ordering": ["a", "b"],
        "orthonormal": True,
    }
    assert payload["geometry"] == {
        "system": "synthetic",
        "cell": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        "boundary_conditions": "finite synthetic",
        "coordinate_convention": "cartesian row lattice vectors",
        "length_unit": "angstrom",
    }
    assert payload["energy_reference"] == {"zero": "explicit zero", "unit": "eV"}
    assert payload["provenance"] == {"source": "unit test"}


def test_complex_matrix_encoding_is_row_major_pairs() -> None:
    """Evidence ID: SV-ORJS-006.

    Requirement: an N-by-N complex128 matrix maps by row to real/imaginary pairs.
    Method: serialize a 2-by-2 synthetic non-Hermitian matrix with distinct entries.
    Oracle: manually decomposed binary64 components in source row order. Acceptance
    is exact nested-list equality. Interpretation: failure indicates ordering or
    component-sign corruption. Limitations: no physical matrix meaning, scientific
    validation, UQ, or Rust conformance is established.
    """
    matrix = np.array([[1 + 2j, -3 + 4j], [5 - 6j, -7 - 8j]], dtype=np.complex128)
    payload = json.loads(OperatorRecordJsonSerializer().serialize(make_record(matrix)))
    assert payload["matrix"] == [[[1.0, 2.0], [-3.0, 4.0]], [[5.0, -6.0], [-7.0, -8.0]]]
