r"""Software verification of ``QexsdDocument``.

Evidence profile: routine

Bounded artifact scope: immutable mechanically parsed native QEXSD state.

Facet and represented meaning

The DataObject owns native dimensions, references, finiteness, and cardinalities.

Intrinsic and cross-object scope

Only document-owned invariants and deep tuple immutability are covered.

VVUQ and scientific exclusions

The controlled document establishes no numerical or scientific validity.
"""

from dataclasses import FrozenInstanceError, replace

import pytest
from qexsd_fixtures import CONTROLLED_QEXSD, controlled_source_bytes

from ksdft2effmass.io.quantum_espresso.qexsd import (
    ParseQexsdDocument,
    QexsdDocument,
    QexsdSource,
)

SUT = QexsdDocument
pytestmark = pytest.mark.software_verification


def make_document() -> QexsdDocument:
    """Parse the controlled fixture into the class-owned SUT.

    Evidence ID: Helper owns no identifier.

    Requirement: Support the named tests without owning evidence.

    Acceptance: Return deterministic controlled support data.
    """
    digest, count = controlled_source_bytes()
    return ParseQexsdDocument().execute(
        QexsdSource("/controlled/source.xml", digest, count, CONTROLLED_QEXSD)
    )


def test_constructor__immutable_state__retains_nested_tuples() -> None:
    """Evidence ID: SV-PERIODIC-007

    Requirement: Retained native collections are deeply immutable ordered tuples.

    Acceptance: Nested state is tuple-backed and field reassignment raises
    FrozenInstanceError.
    """
    document = make_document()
    assert type(document.atoms) is tuple and type(document.atoms[0][2]) is tuple
    assert (
        type(document.eigenvalues) is tuple and type(document.eigenvalues[0]) is tuple
    )
    with pytest.raises(FrozenInstanceError):
        document.exit_status = 1  # type: ignore[misc]


@pytest.mark.parametrize(
    "changes",
    [
        pytest.param({"source_sha256": "bad"}, id="source_digest"),
        pytest.param({"direct_lattice_vectors": ((1.0, 0.0),)}, id="lattice_shape"),
        pytest.param({"declared_atom_count": 3}, id="atom_cardinality"),
        pytest.param({"atoms": ((1, "Ge", (0.0, 0.0, 0.0)),)}, id="species_resolution"),
        pytest.param({"k_point_weights": (1.0,)}, id="kpoint_weight_cardinality"),
        pytest.param({"eigenvalues": ((1.0, 2.0),)}, id="spectrum_cardinality"),
        pytest.param({"occupations": ((1.0,), (1.0, 0.0))}, id="occupation_shape"),
        pytest.param({"fft_grid": (4, 0, 6)}, id="fft_shape"),
        pytest.param({"exit_status": 256}, id="exit_status"),
    ],
)
def test_constructor__intrinsic_relationships__rejects_invalid_state(
    changes: dict[str, object],
) -> None:
    """Evidence ID: SV-PERIODIC-008

    Requirement: Native vector, reference, count, spectrum, grid, and status
    invariants hold.

    Acceptance: Every named invalid replacement raises TypeError or ValueError.
    """
    with pytest.raises((TypeError, ValueError)):
        replace(make_document(), **changes)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "changes",
    [
        pytest.param({"source_byte_count": True}, id="boolean_byte_count"),
        pytest.param({"producing_application_version": 7}, id="numeric_version"),
        pytest.param({"declared_atom_count": True}, id="boolean_atom_count"),
        pytest.param({"species": (["Si", 28.0, "Si.upf"],)}, id="list_species"),
        pytest.param({"sampled_k_point_count": True}, id="boolean_kpoint_count"),
        pytest.param({"k_point_weights": (True, True)}, id="boolean_weights"),
        pytest.param({"band_count": True}, id="boolean_band_count"),
        pytest.param({"total_energy": "-1.0"}, id="string_energy"),
        pytest.param({"fft_grid": (4, True, 6)}, id="boolean_fft_value"),
        pytest.param({"exit_status": True}, id="boolean_exit_status"),
    ],
)
def test_constructor__semantic_types__raise_type_error(
    changes: dict[str, object],
) -> None:
    """Evidence ID: SV-QEXSD-004

    Requirement: Wrong semantic scalar, container, and member types are rejected
    without implicit conversion.

    Acceptance: Every named wrong-type partition raises ``TypeError`` exactly.
    """
    with pytest.raises(TypeError):
        replace(make_document(), **changes)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "changes",
    [
        pytest.param({"source_byte_count": -1}, id="negative_byte_count"),
        pytest.param({"producing_application_version": ""}, id="empty_version"),
        pytest.param({"atomic_structure_alat": float("nan")}, id="nonfinite_alat"),
        pytest.param({"declared_atom_count": 0}, id="zero_atom_count"),
        pytest.param({"sampled_k_point_count": 0}, id="zero_kpoint_count"),
        pytest.param({"band_count": 0}, id="zero_band_count"),
        pytest.param({"total_energy": float("inf")}, id="nonfinite_energy"),
        pytest.param({"fft_grid": (4, 0, 6)}, id="nonpositive_fft_value"),
        pytest.param({"exit_status": 256}, id="out_of_range_exit_status"),
    ],
)
def test_constructor__typed_invariants__raise_value_error(
    changes: dict[str, object],
) -> None:
    """Evidence ID: SV-QEXSD-005

    Requirement: Correctly typed values violating native record invariants are
    rejected without changing represented semantics.

    Acceptance: Every named invalid-value partition raises ``ValueError`` exactly.
    """
    with pytest.raises(ValueError):
        replace(make_document(), **changes)  # type: ignore[arg-type]
