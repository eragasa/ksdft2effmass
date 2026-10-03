"""Software verification of ``Periodic1DPlaneWaveParentRepresentation``.

Evidence profile: routine

Facet and represented meaning
-----------------------------
The class identifies one finite plane-wave Galerkin representation of a distinct
untruncated one-dimensional Fourier parent.

Intrinsic and cross-object scope
--------------------------------
Exact parent identity, represented operator and state-space identity, finite cutoff,
reciprocal mesh, representation map, and provenance are covered using public records.

VVUQ and scientific exclusions
------------------------------
Inputs are synthetic. Passing establishes software behavior only; it does not establish
cutoff convergence, scientific validation, or uncertainty quantification.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.periodic import PeriodicOperatorReference
from ksdft2effmass.periodic1d import (
    Periodic1DFourierHamiltonianToyModel,
    Periodic1DPlaneWaveParentRepresentation,
    Periodic1DPlaneWaveParentRepresentationConstructor,
)
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
)

pytestmark = pytest.mark.software_verification

SYNTHETIC_LATTICE_PERIOD = 2.0 * np.pi
SYNTHETIC_RECIPROCAL_VECTOR_MAGNITUDE = 1.0
SYNTHETIC_POTENTIAL_STRENGTH = 0.2
SYNTHETIC_PLANE_WAVE_CUTOFF = 3
SYNTHETIC_RECIPROCAL_MESH_POINT_COUNT = 8
MISMATCHED_RECIPROCAL_VECTOR_MAGNITUDE = 2.0


class TestPeriodic1DPlaneWaveParentRepresentation:
    """Own finite-parent-representation identity and separation evidence."""

    @staticmethod
    def parent() -> Periodic1DFourierHamiltonianToyModel:
        """Return one synthetic untruncated Fourier parent."""
        return Periodic1DFourierHamiltonianToyModel(
            model_id="test.periodic1d.parent",
            state_space_id="test.periodic1d.untruncated-bloch-space",
            reciprocal_domain_id="test.periodic1d.primitive-zone",
            potential=PeriodicFourierPotential1D(
                period=ScalarQuantity(SYNTHETIC_LATTICE_PERIOD, Unitless()),
                constant_coefficient=ScalarQuantity(0.0, Unitless()),
                cosine_coefficients=VectorQuantity(
                    np.asarray([SYNTHETIC_POTENTIAL_STRENGTH], dtype=np.float64),
                    Unitless(),
                ),
                sine_coefficients=VectorQuantity(
                    np.zeros(1, dtype=np.float64), Unitless()
                ),
            ),
            recoil_energy=ScalarQuantity(1.0, Unitless()),
        )

    @classmethod
    def representation(cls) -> Periodic1DPlaneWaveParentRepresentation:
        """Return one finite cutoff-three, eight-point representation."""
        parent = cls.parent()
        reciprocal_vector = ScalarQuantity(
            SYNTHETIC_RECIPROCAL_VECTOR_MAGNITUDE, Unitless()
        )
        return Periodic1DPlaneWaveParentRepresentationConstructor().execute(
            representation_id="test.periodic1d.plane-wave-p3-k8",
            parent_model=parent,
            basis=PlaneWaveBasis1D(reciprocal_vector, SYNTHETIC_PLANE_WAVE_CUTOFF),
            reciprocal_mesh=CenteredUniformReciprocalMesh1D(
                reciprocal_vector, SYNTHETIC_RECIPROCAL_MESH_POINT_COUNT
            ),
            represented_operator=PeriodicOperatorReference(
                model_id=parent.model_id,
                operator_id="test.periodic1d.plane-wave-p3-hamiltonian",
                state_space_id="test.periodic1d.plane-wave-p3-bloch-space",
                spatial_dimension=1,
            ),
            representation_map_id="test.periodic1d.plane-wave-galerkin-p3",
            provenance_id="test.periodic1d.synthetic-provenance",
        )

    def test_construction__finite_representation__preserves_cutoff_identity(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-PLANE-WAVE-PARENT-001.

        Requirement: A finite parent representation identifies its untruncated parent,
        cutoff basis, reciprocal mesh, finite operator, finite state space, map, and
        provenance without becoming a second scientific parent model.

        Acceptance: Public fields retain the authored identities and report the
        cutoff-derived finite ambient dimension.
        """
        representation = self.representation()

        assert representation.parent_model.state_space_id == (
            "test.periodic1d.untruncated-bloch-space"
        )
        assert representation.represented_operator.state_space_id == (
            "test.periodic1d.plane-wave-p3-bloch-space"
        )
        assert representation.parent_model.state_space_id != (
            representation.represented_operator.state_space_id
        )
        assert representation.cutoff == SYNTHETIC_PLANE_WAVE_CUTOFF
        assert representation.ambient_dimension == (2 * SYNTHETIC_PLANE_WAVE_CUTOFF + 1)
        assert representation.reciprocal_mesh.point_count == (
            SYNTHETIC_RECIPROCAL_MESH_POINT_COUNT
        )
        assert representation.representation_map_id == (
            "test.periodic1d.plane-wave-galerkin-p3"
        )

    def test_construction__state_space__rejects_untruncated_identity_reuse(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-PLANE-WAVE-PARENT-002.

        Requirement: A finite Galerkin state space must not be identified as the
        untruncated parent state space.

        Acceptance: Reusing the untruncated identity raises ``ValueError``.
        """
        representation = self.representation()
        parent = representation.parent_model

        with pytest.raises(ValueError, match="state spaces must remain distinct"):
            Periodic1DPlaneWaveParentRepresentation(
                representation_id=representation.representation_id,
                parent_model=parent,
                basis=representation.basis,
                reciprocal_mesh=representation.reciprocal_mesh,
                represented_operator=PeriodicOperatorReference(
                    model_id=parent.model_id,
                    operator_id=representation.represented_operator.operator_id,
                    state_space_id=parent.state_space_id,
                    spatial_dimension=1,
                ),
                representation_map_id=representation.representation_map_id,
                provenance_id=representation.provenance_id,
            )

    def test_construction__reciprocal_mesh__rejects_basis_period_mismatch(self) -> None:
        """Evidence ID: SV-PERIODIC1D-PLANE-WAVE-PARENT-003.

        Requirement: The finite basis and sampled reciprocal mesh identify the same
        reciprocal period.

        Acceptance: A mismatched mesh period raises ``ValueError``.
        """
        representation = self.representation()

        with pytest.raises(ValueError, match="basis and reciprocal mesh must agree"):
            Periodic1DPlaneWaveParentRepresentation(
                representation_id=representation.representation_id,
                parent_model=representation.parent_model,
                basis=representation.basis,
                reciprocal_mesh=CenteredUniformReciprocalMesh1D(
                    ScalarQuantity(MISMATCHED_RECIPROCAL_VECTOR_MAGNITUDE, Unitless()),
                    SYNTHETIC_RECIPROCAL_MESH_POINT_COUNT,
                ),
                represented_operator=representation.represented_operator,
                representation_map_id=representation.representation_map_id,
                provenance_id=representation.provenance_id,
            )
