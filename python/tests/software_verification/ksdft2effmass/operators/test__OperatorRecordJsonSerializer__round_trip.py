"""OperatorRecordJsonSerializer round-trip software verification.

Object: exact record-to-text-to-record behavior. Evidence class: software
verification. Requirement: deterministic version-1 round trips preserve all eight
fields, general non-Hermitian state, empty provenance, complex/extreme finite
values, and defensive immutable ownership. Strategy: construct synthetic public
records and compare exact DataObject equality and ownership properties. Oracle:
independently supplied source records and approved exact equality. Acceptance is
exact, never approximate. Passing is not scientific validation, uncertainty
quantification, or Rust conformance; failure indicates lossy mapping or ownership
drift.
"""

from collections.abc import Mapping

import numpy as np
import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification


@pytest.mark.parametrize(
    ("matrix", "provenance"),
    [
        (np.array([[0.0 + 0.0j]], dtype=np.complex128), {}),
        (
            np.array([[1 + 2j, 3 - 4j], [-5 + 6j, 7 + 8j]], dtype=np.complex128),
            {"source": "non-Hermitian"},
        ),
        (
            np.array(
                [
                    [np.finfo(np.float64).max + 1j * np.finfo(np.float64).tiny, 0j],
                    [0j, -np.finfo(np.float64).max - 1j * np.finfo(np.float64).tiny],
                ],
                dtype=np.complex128,
            ),
            {},
        ),
    ],
    ids=["empty-provenance-zero", "complex-nonhermitian", "extreme-finite"],
)
def test_exact_deterministic_round_trips(
    matrix: np.ndarray, provenance: dict[str, str]
) -> None:
    """Evidence ID: SV-ORJS-017.

    Requirement: empty provenance, non-Hermitian complex, and extreme finite state
    round-trip exactly. Method: serialize, deserialize, reserialize, and compare
    source/restored records and text. Oracle: exact source DataObject equality and
    IEEE binary64 values, with no tolerance. Acceptance requires equality and
    byte-for-byte text stability. Interpretation: failure indicates loss or
    nondeterminism. Limitations: synthetic matrices have explicit 1x1 or 2x2 shape,
    complex128 dtype, eV metadata, no numerical tolerance/warnings, and no physical
    meaning; scientific validation, UQ, and Rust conformance are not performed.
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


def test_deserialized_state_is_defensively_owned_and_immutable() -> None:
    """Evidence ID: SV-ORJS-018.

    Requirement: restored matrix/provenance are fresh operationally immutable
    DataObject state. Method: deserialize and exercise ordinary public mutation
    boundaries. Oracle: OperatorRecord ownership contract applied by construction.
    Acceptance requires no shared matrix memory, read-only matrix, immutable
    provenance mapping, and rejected item/setflags mutation. Interpretation: failure
    permits post-decode state mutation. Limitations: adversarial memory access,
    scientific validation, UQ, and Rust conformance are not assessed.
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
