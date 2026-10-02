"""Software verification for represented retained-operator binding.

Evidence profile: routine

Bounded artifact scope: ``PeriodicRepresentedRetainedOperatorConstructor`` exact
state-space, dimension, ordering, energy-reference, and metadata binding contract.

Facet and represented meaning
-----------------------------
The module verifies the public binding between one exact retained mathematical
operator and one finite ``OperatorRecord`` representation.

Intrinsic and cross-object scope
--------------------------------
State-space identity, dimension, basis ordering, energy reference, gauge identity, and
representation-map identity are checked against exact synthetic records.

VVUQ and scientific exclusions
------------------------------
These tests establish software compatibility checks only. They do not assess
Hermiticity, gauge equivalence, numerical accuracy, material realism, scientific
validation, or uncertainty.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    OperatorRecord,
    StateSpace,
)
from ksdft2effmass.periodic import (
    PeriodicHermiticityStatus,
    PeriodicOperatorReference,
    PeriodicRepresentedRetainedOperator,
    PeriodicRepresentedRetainedOperatorConstructor,
    PeriodicRetainedOperator,
    PeriodicRetainedOperatorConstructionKind,
    PeriodicRetainedOperatorConstructor,
    PeriodicRetainedSubspaceConstructor,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)

pytestmark = pytest.mark.software_verification


class TestPeriodicRepresentedRetainedOperatorConstructor:
    """Verify exact finite-representation binding and incompatibility rejection."""

    @staticmethod
    def make_parent() -> PeriodicOperatorReference:
        """Return one synthetic periodic parent reference."""
        return PeriodicOperatorReference(
            model_id="test.parent",
            operator_id="test.parent.hamiltonian",
            state_space_id="test.parent.space",
            spatial_dimension=1,
        )

    @classmethod
    def make_retained_operator(cls) -> PeriodicRetainedOperator:
        """Return one exact synthetic rank-two retained operator."""
        definition = PeriodicRetentionDefinition(
            retention_id="test.retention",
            parent_operator=cls.make_parent(),
            retained_space_id="test.retained.space",
            kind=PeriodicRetentionKind.SELECTED_BANDS,
            rank=2,
            ordered_state_labels=("band-0", "band-1"),
            reciprocal_domain_id="test.mesh",
            construction_record_id="test.selection",
            assumption_ids=(),
            provenance_id="test.provenance.definition",
        )
        subspace = PeriodicRetainedSubspaceConstructor().execute(
            definition=definition,
            ambient_state_space_id="test.parent.space",
            ambient_dimension=4,
            projector_or_frame_record_id="test.frame",
            spin_convention="spinless",
            internal_degree_convention="ordered bands",
            reciprocal_boundary_convention="periodic sewing",
            provenance_id="test.provenance.space",
        )
        return PeriodicRetainedOperatorConstructor().execute(
            operator_id="test.retained.hamiltonian",
            parent_operator=cls.make_parent(),
            retained_subspace=subspace,
            construction_kind=(
                PeriodicRetainedOperatorConstructionKind.ORTHOGONAL_COMPRESSION
            ),
            energy_reference=EnergyReference("parent zero", "eV"),
            hermiticity_status=PeriodicHermiticityStatus.DECLARED_HERMITIAN,
            provenance_id="test.provenance.operator",
        )

    @staticmethod
    def make_record(
        *,
        state_space_id: str = "test.retained.space",
        dimension: int = 2,
        ordering: tuple[str, ...] = ("band-0", "band-1"),
        energy_zero: str = "parent zero",
        energy_unit: str = "eV",
    ) -> OperatorRecord:
        """Return one finite synthetic represented operator with selected metadata."""
        matrix = (
            ((1.0, 0.0), (0.0, 2.0))
            if dimension == 2
            else tuple(
                tuple(1.0 if row == column else 0.0 for column in range(dimension))
                for row in range(dimension)
            )
        )
        return OperatorRecord(
            identifier="test.operator-record",
            operator_kind="retained Hamiltonian",
            matrix=matrix,
            state_space=StateSpace(
                identifier=state_space_id,
                kind="retained periodic space",
                dimension=dimension,
            ),
            basis=Basis(
                identifier="test.basis",
                kind="retained frame",
                ordering=ordering,
                orthonormal=True,
            ),
            geometry=Geometry(
                system="synthetic periodic system",
                cell=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
                boundary_conditions="periodic",
                coordinate_convention="row lattice vectors",
                length_unit="angstrom",
            ),
            energy_reference=EnergyReference(energy_zero, energy_unit),
            provenance={"source": "synthetic software-verification record"},
        )

    @classmethod
    def construct(cls) -> PeriodicRepresentedRetainedOperator:
        """Construct one valid representation binding through its ActionObject."""
        return PeriodicRepresentedRetainedOperatorConstructor().execute(
            representation_id="test.representation",
            retained_operator=cls.make_retained_operator(),
            operator_record=cls.make_record(),
            representation_map_id="test.retained-frame-synthesis",
            gauge_id="test.periodic-gauge",
            provenance_id="test.provenance.binding",
        )

    def test_method__execute__preserves_exact_representation_metadata(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-REPRESENTATION-001

        Requirement: A compatible finite record binds without changing its represented
        state or the declared representation metadata.

        Acceptance: Identity, shape, ordering, matrix entry, and gauge remain exact.
        """
        represented = self.construct()

        assert represented.representation_id == "test.representation"
        assert (
            represented.operator_record.state_space.identifier == "test.retained.space"
        )
        assert represented.operator_record.shape == (2, 2)
        assert represented.operator_record.basis.ordering == ("band-0", "band-1")
        assert represented.operator_record.matrix[0, 0] == 1.0 + 0.0j
        assert represented.gauge_id == "test.periodic-gauge"

    def test_method__execute__rejects_state_space_identity_mismatch(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-REPRESENTATION-002

        Requirement: Represented and exact retained-space identities agree exactly.

        Acceptance: A different state-space identity raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="identity must match retained space"):
            PeriodicRepresentedRetainedOperatorConstructor().execute(
                representation_id="test.representation",
                retained_operator=self.make_retained_operator(),
                operator_record=self.make_record(state_space_id="test.other.space"),
                representation_map_id="test.map",
                gauge_id="test.gauge",
                provenance_id="test.provenance.binding",
            )

    def test_method__execute__rejects_dimension_mismatch(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-REPRESENTATION-003

        Requirement: Represented state-space dimension equals exact retained rank.

        Acceptance: A different represented dimension raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="dimension must match retained rank"):
            PeriodicRepresentedRetainedOperatorConstructor().execute(
                representation_id="test.representation",
                retained_operator=self.make_retained_operator(),
                operator_record=self.make_record(
                    dimension=1,
                    ordering=("band-0",),
                ),
                representation_map_id="test.map",
                gauge_id="test.gauge",
                provenance_id="test.provenance.binding",
            )

    def test_method__execute__rejects_basis_ordering_mismatch(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-REPRESENTATION-004

        Requirement: Represented basis ordering equals retained-state ordering.

        Acceptance: Reversed labels raise ``ValueError`` rather than implicit reorder.
        """
        with pytest.raises(ValueError, match="basis ordering must match"):
            PeriodicRepresentedRetainedOperatorConstructor().execute(
                representation_id="test.representation",
                retained_operator=self.make_retained_operator(),
                operator_record=self.make_record(ordering=("band-1", "band-0")),
                representation_map_id="test.map",
                gauge_id="test.gauge",
                provenance_id="test.provenance.binding",
            )

    @pytest.mark.parametrize(
        ("energy_zero", "energy_unit"),
        (
            pytest.param("different zero", "eV", id="different_energy_zero"),
            pytest.param("parent zero", "hartree", id="different_energy_unit"),
        ),
    )
    def test_method__execute__rejects_energy_reference_mismatch(
        self,
        energy_zero: str,
        energy_unit: str,
    ) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-REPRESENTATION-005

        Requirement: Exact retained and represented energy references agree without
        inferred unit conversion or scalar energy alignment.

        Acceptance: Each explicit zero or unit mismatch raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="energy reference must match"):
            PeriodicRepresentedRetainedOperatorConstructor().execute(
                representation_id="test.representation",
                retained_operator=self.make_retained_operator(),
                operator_record=self.make_record(
                    energy_zero=energy_zero,
                    energy_unit=energy_unit,
                ),
                representation_map_id="test.map",
                gauge_id="test.gauge",
                provenance_id="test.provenance.binding",
            )
