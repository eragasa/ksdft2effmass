r"""Software verification of ``OperatorRecordJsonSerializer``.

Facet and represented meaning
-----------------------------
This class-owned module owns the round trip facet. Object: exact
record-to-text-to-record behavior. Evidence class: software
verification. Requirement: deterministic version-1 round trips preserve all eight
fields, general non-Hermitian state, empty provenance, complex/extreme finite
values, and defensive immutable ownership. Strategy: construct synthetic public
records and compare exact DataObject equality and ownership properties. Oracle:
independently supplied source records and approved exact equality. Acceptance is
exact, never approximate. Passing is not scientific validation, uncertainty
quantification, or Rust conformance; failure indicates lossy mapping or ownership
drift.

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

from collections.abc import Mapping

import numpy as np
import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordJsonSerializer


@pytest.mark.parametrize(
    ("matrix", "provenance"),
    [
        pytest.param(
            np.array([[0.0 + 0j]], dtype=np.complex128), {}, id="empty_provenance_zero"
        ),
        pytest.param(
            np.array([[1 + 2j, 3 - 4j], [-5 + 6j, 7 + 8j]], dtype=np.complex128),
            {"source": "non-Hermitian"},
            id="complex_nonhermitian",
        ),
        pytest.param(
            np.array(
                [
                    [np.finfo(np.float64).max + 1j * np.finfo(np.float64).tiny, 0j],
                    [0j, -np.finfo(np.float64).max - 1j * np.finfo(np.float64).tiny],
                ],
                dtype=np.complex128,
            ),
            {},
            id="extreme_finite",
        ),
    ],
)
def test_method__serialize__exact_deterministic_round_trips(
    matrix: np.ndarray, provenance: dict[str, str]
) -> None:
    r"""Evidence ID
    SV-ORJS-017
    Requirement
    OperatorRecordJsonSerializer enforces this version-1 JSON boundary partition:
    serialize: exact deterministic round trips.
    Method
    Invoke serialize() or deserialize() on the explicit schema-version-1 partition
    (serialize: exact deterministic round trips); warnings and coercive fallback
    behavior are not accepted.
    Oracle
    The public version-1 schema, fixed wire-field vocabulary, literal JSON grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.
    Acceptance
    All literal values, arrays, field names, ordering relations, object identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    dimension = matrix.shape[0]
    ordering = tuple(f"b{i}" for i in range(dimension))
    from operator_record_fixtures import make_basis, make_state_space

    record = make_record(
        matrix,
        state_space=make_state_space(dimension=dimension),
        basis=make_basis(ordering=ordering),
        provenance=provenance,
    )
    serializer = OperatorRecordJsonSerializer()
    text = serializer.serialize(record)
    restored = serializer.deserialize(text)
    assert restored == record
    assert serializer.serialize(restored) == text


def test_method__deserialize__deserialized_state_is_defensively_owned_and() -> None:
    r"""Evidence ID
    SV-ORJS-018
    Requirement
    OperatorRecordJsonSerializer enforces this version-1 JSON boundary partition:
    deserialize: deserialized state is defensively owned and.
    Method
    Invoke serialize() or deserialize() on the explicit schema-version-1 partition
    (deserialize: deserialized state is defensively owned and); warnings and coercive
    fallback behavior are not accepted.
    Oracle
    The public version-1 schema, fixed wire-field vocabulary, literal JSON grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.
    Acceptance
    The named partition raises exactly ValueError or TypeError with the asserted public
    message, code, or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    source = make_record(provenance={"source": "round trip"})
    restored = OperatorRecordJsonSerializer().deserialize(
        OperatorRecordJsonSerializer().serialize(source)
    )
    assert not np.shares_memory(restored.matrix, source.matrix)
    assert not restored.matrix.flags.writeable
    assert isinstance(restored.provenance, Mapping)
    with pytest.raises(ValueError):
        restored.matrix[0, 0] = 9
    with pytest.raises(ValueError):
        restored.matrix.setflags(write=True)
    with pytest.raises(TypeError):
        restored.provenance["new"] = "value"  # type: ignore[index]
