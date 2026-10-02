"""Software verification for exact retained-operator construction.

Evidence profile: routine

Bounded artifact scope: ``PeriodicRetainedOperatorConstructor`` parent, domain,
codomain, energy-reference, and declaration contract.

Facet and represented meaning
-----------------------------
The module verifies the public binding of a parent operator to an exact operator whose
domain and codomain are one identified retained space.

Intrinsic and cross-object scope
--------------------------------
Parent identity, restriction classification, energy reference, Hermiticity declaration,
and retained domain/codomain are checked exactly.

VVUQ and scientific exclusions
------------------------------
These synthetic tests perform no numerical compression or Hermiticity analysis and do
not establish mathematical correctness, physical adequacy, or scientific validation.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.operators import EnergyReference
from ksdft2effmass.periodic import (
    PeriodicHermiticityStatus,
    PeriodicOperatorReference,
    PeriodicRetainedOperator,
    PeriodicRetainedOperatorConstructionKind,
    PeriodicRetainedOperatorConstructor,
    PeriodicRetainedSubspace,
    PeriodicRetainedSubspaceConstructor,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)

pytestmark = pytest.mark.software_verification


class TestPeriodicRetainedOperatorConstructor:
    """Verify exact retained-operator parent and space ownership."""

    @staticmethod
    def make_parent(
        operator_id: str = "test.parent.hamiltonian",
    ) -> PeriodicOperatorReference:
        """Return one synthetic parent reference with a selectable operator identity."""
        return PeriodicOperatorReference(
            model_id="test.parent",
            operator_id=operator_id,
            state_space_id="test.parent.space",
            spatial_dimension=1,
        )

    @classmethod
    def make_subspace(cls) -> PeriodicRetainedSubspace:
        """Return one valid synthetic rank-two retained space."""
        definition = PeriodicRetentionDefinition(
            retention_id="test.retention",
            parent_operator=cls.make_parent(),
            retained_space_id="test.retained.space",
            kind=PeriodicRetentionKind.SPECTRAL_RESTRICTION,
            rank=2,
            ordered_state_labels=("state-0", "state-1"),
            reciprocal_domain_id="test.reciprocal.domain",
            construction_record_id="test.spectral-selection",
            assumption_ids=(),
            provenance_id="test.provenance.definition",
        )
        return PeriodicRetainedSubspaceConstructor().execute(
            definition=definition,
            ambient_state_space_id="test.parent.space",
            ambient_dimension=4,
            projector_or_frame_record_id="test.projector",
            spin_convention="spinless",
            internal_degree_convention="spectral ordering",
            reciprocal_boundary_convention="not applicable",
            provenance_id="test.provenance.subspace",
        )

    @classmethod
    def construct(cls) -> PeriodicRetainedOperator:
        """Construct the valid exact retained operator through its ActionObject."""
        return PeriodicRetainedOperatorConstructor().execute(
            operator_id="test.retained.hamiltonian",
            parent_operator=cls.make_parent(),
            retained_subspace=cls.make_subspace(),
            construction_kind=(
                PeriodicRetainedOperatorConstructionKind.INVARIANT_RESTRICTION
            ),
            energy_reference=EnergyReference("parent zero", "eV"),
            hermiticity_status=PeriodicHermiticityStatus.DECLARED_HERMITIAN,
            provenance_id="test.provenance.retained-operator",
        )

    def test_method__execute__sets_common_retained_domain_and_codomain(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-OPERATOR-001

        Requirement: The exact operator has one retained domain and codomain and
        preserves its declared parent and energy metadata.

        Acceptance: Public fields equal the independently declared exact identities.
        """
        operator = self.construct()

        assert operator.domain_id == "test.retained.space"
        assert operator.codomain_id == "test.retained.space"
        assert operator.parent_operator == self.make_parent()
        assert operator.energy_reference == EnergyReference("parent zero", "eV")
        assert (
            operator.hermiticity_status is PeriodicHermiticityStatus.DECLARED_HERMITIAN
        )

    def test_method__execute__rejects_different_parent_operator(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-OPERATOR-002

        Requirement: An exact retained operator and its subspace share one parent.

        Acceptance: A different parent-operator identity raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="must match retained-subspace parent"):
            PeriodicRetainedOperatorConstructor().execute(
                operator_id="test.retained.hamiltonian",
                parent_operator=self.make_parent("test.other.hamiltonian"),
                retained_subspace=self.make_subspace(),
                construction_kind=(
                    PeriodicRetainedOperatorConstructionKind.ORTHOGONAL_COMPRESSION
                ),
                energy_reference=EnergyReference("parent zero", "eV"),
                hermiticity_status=PeriodicHermiticityStatus.NOT_ASSESSED,
                provenance_id="test.provenance.retained-operator",
            )

    def test_construction__kind__rejects_untyped_string(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-OPERATOR-003

        Requirement: Construction kind uses the exact closed enum.

        Acceptance: A raw string substitute raises ``TypeError``.
        """
        with pytest.raises(TypeError, match="construction_kind must be"):
            PeriodicRetainedOperatorConstructor().execute(
                operator_id="test.retained.hamiltonian",
                parent_operator=self.make_parent(),
                retained_subspace=self.make_subspace(),
                construction_kind="invariant_restriction",  # type: ignore[arg-type]
                energy_reference=EnergyReference("parent zero", "eV"),
                hermiticity_status=PeriodicHermiticityStatus.NOT_ASSESSED,
                provenance_id="test.provenance.retained-operator",
            )

    def test_construction__hermiticity__rejects_boolean_substitute(self) -> None:
        """Evidence ID: SV-PERIODIC-RETENTION-OPERATOR-004

        Requirement: Hermiticity declaration uses the exact closed enum.

        Acceptance: A Boolean substitute raises ``TypeError``.
        """
        with pytest.raises(TypeError, match="hermiticity_status must be"):
            PeriodicRetainedOperatorConstructor().execute(
                operator_id="test.retained.hamiltonian",
                parent_operator=self.make_parent(),
                retained_subspace=self.make_subspace(),
                construction_kind=(
                    PeriodicRetainedOperatorConstructionKind.INVARIANT_RESTRICTION
                ),
                energy_reference=EnergyReference("parent zero", "eV"),
                hermiticity_status=True,  # type: ignore[arg-type]
                provenance_id="test.provenance.retained-operator",
            )
