r"""Software verification of ``OperatorRecordJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the serialization facet. Object: serializer
``serialize`` behavior. Evidence class: software verification.

Requirement: deterministic sorted compact JSON with nine exact top-level fields,
all eight record fields, and row-major ``[real, imaginary]`` complex entries.
Strategy: serialize an independently constructed synthetic record and compare with
an independently assembled JSON object/text oracle. Acceptance is exact text and
value equality. Passing is wire-encoding conformance, not scientific validation,
uncertainty quantification, or Rust conformance; failure requires contract/source/
evidence investigation.

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

import numpy as np
import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordJsonSerializer


def test_method__serialize__serialization_is_sorted_compact_and_deterministic() -> None:
    r"""Evidence ID: SV-ORJS-004

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    serialize: serialization is sorted compact and deterministic.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (serialize: serialization is sorted compact and deterministic); warnings and
    coercive fallback behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    serializer = OperatorRecordJsonSerializer()
    text = serializer.serialize(make_record(provenance={"z": "last", "a": "first"}))
    assert text == serializer.serialize(
        make_record(provenance={"a": "first", "z": "last"})
    )
    assert text == json.dumps(json.loads(text), sort_keys=True, separators=(",", ":"))
    assert "\n" not in text and ": " not in text and ", " not in text


def test_method__serialize__serialization_emits_exact_nested_fields_and_values() -> (
    None
):
    r"""Evidence ID: SV-ORJS-005

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    serialize: serialization emits exact nested fields and values.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (serialize: serialization emits exact nested fields and values); warnings and
    coercive fallback behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
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


def test_field__complex_matrix_encoding_is_row_major_pairs__is_exact() -> None:
    r"""Evidence ID: SV-ORJS-006

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    complex matrix encoding is row major pairs: is exact.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (complex matrix encoding is row major pairs: is exact); warnings and coercive
    fallback behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    matrix = np.array([[1 + 2j, -3 + 4j], [5 - 6j, -7 - 8j]], dtype=np.complex128)
    payload = json.loads(OperatorRecordJsonSerializer().serialize(make_record(matrix)))
    assert payload["matrix"] == [[[1.0, 2.0], [-3.0, 4.0]], [[5.0, -6.0], [-7.0, -8.0]]]
