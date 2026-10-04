r"""Software verification of periodic-1D composite-operator adoption.

Evidence profile: claim_bearing

Bounded artifact scope: correlated Appendix G composite input/result records and their
retained reciprocal and complete hopping arrays.

Scientific exclusions: passing establishes source correlation, content authentication,
and typed software ownership only. It does not reconstruct unavailable frame arrays,
rerun the campaign, establish parent-model accuracy, validate a gauge, or perform
uncertainty quantification.
"""

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.periodic_1d import (
    Periodic1DCompositeCampaignWorkflow,
    Periodic1DCompositeCampaignWorkflowRequest,
    Periodic1DCompositeScientificAdoption,
    Periodic1DCompositeScientificAdoptionRequest,
    Periodic1DCompositeScientificAdoptionResult,
)
from ksdft2effmass.operators import (
    Basis,
    ComplexMatrixQuantity,
    EnergyReference,
    PhysicalUnit,
)
from ksdft2effmass.periodic import PeriodicRetentionKind
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
)

pytestmark = pytest.mark.software_verification


class TestPeriodic1DCompositeScientificAdoption:
    """Own finite-parent and gauge-qualified composite adoption evidence."""

    @staticmethod
    def adopt() -> Periodic1DCompositeScientificAdoptionResult:
        """Correlate immutable historical bytes and execute scientific adoption."""
        repository_root = Path(__file__).resolve().parents[6]
        calculation_root = repository_root / (
            "calculations/research-monograph/periodic-1d"
        )
        correlated = Periodic1DCompositeCampaignWorkflow().execute(
            Periodic1DCompositeCampaignWorkflowRequest(
                calculation_root.joinpath("composite-input.json").read_bytes(),
                calculation_root.joinpath("composite-result.json").read_bytes(),
            )
        )
        return Periodic1DCompositeScientificAdoption().execute(
            Periodic1DCompositeScientificAdoptionRequest(correlated)
        )

    def test_method__execute__constructs_finite_parent_retained_operators(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-ADOPTION-001.

        Requirement: Composite band retention must descend from the cutoff-qualified
        finite parent rather than conflate that representation with the untruncated
        Fourier model.

        Acceptance: The cutoff-15, dimension-31, 128-point parent is distinct from the
        untruncated parent state space, and both rank-two groups define invariant
        restrictions of that exact finite parent.
        """
        adoption = self.adopt()
        represented_parent = adoption.parent_representation.represented_operator

        assert adoption.parent_representation.parent_model is adoption.parent_model
        assert adoption.parent_representation.cutoff == 15
        assert adoption.parent_representation.ambient_dimension == 31
        assert adoption.parent_representation.reciprocal_mesh.point_count == 128
        assert represented_parent.state_space_id != adoption.parent_model.state_space_id
        assert tuple(group.group_id for group in adoption.groups) == (
            "low_pair",
            "higher_pair",
        )
        assert all(
            group.selected_bands.retention.kind is PeriodicRetentionKind.SELECTED_BANDS
            and group.selected_bands.retention.parent_operator is represented_parent
            and group.retained_subspace.ambient_dimension == 31
            and group.retained_operator.parent_operator is represented_parent
            for group in adoption.groups
        )

    def test_method__execute__separates_exact_operator_from_gauge_forms(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-ADOPTION-002.

        Requirement: One gauge-independent retained operator must own separate smooth
        reciprocal, smooth hopping, and rough hopping representations.

        Acceptance: All three forms bind the same exact operator and exact historical
        data objects; smooth forms share a gauge while the rough form has a distinct
        gauge and no unavailable rough reciprocal form is fabricated.
        """
        adoption = self.adopt()

        for group in adoption.groups:
            source = group.source_result
            exact = group.retained_operator
            assert group.smooth_reciprocal_operator.retained_operator is exact
            assert group.smooth_hopping_operator.retained_operator is exact
            assert group.rough_hopping_operator.retained_operator is exact
            assert group.smooth_reciprocal_operator.samples is (
                source.hopping_representation.smooth_reciprocal_hamiltonians
            )
            assert group.smooth_hopping_operator.hopping_model is (
                source.hopping_representation.smooth_hopping_model
            )
            assert group.rough_hopping_operator.hopping_model is (
                source.hopping_representation.rough_hopping_model
            )
            assert group.smooth_reciprocal_operator.gauge_id == (
                group.smooth_hopping_operator.gauge_id
            )
            assert group.rough_hopping_operator.gauge_id != (
                group.smooth_hopping_operator.gauge_id
            )

    def test_method__execute__authenticates_preserved_array_identities(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-ADOPTION-003.

        Requirement: Adopted represented forms must preserve and authenticate the
        historical reciprocal and hopping artifact identities.

        Acceptance: Each wrapper retains its matching source SHA-256; replacing any
        digest or substituting the smooth form for the rough form is rejected.
        """
        adoption = self.adopt()
        group = adoption.groups[0]
        identities = group.source_result.identities

        assert tuple(
            value.source_result.identities.smooth_projector_sha256
            for value in adoption.groups
        ) == (
            "89271831ecf21f69a89cd85425e52ed8a039ec18c583d0986e6f35ba0678275a",
            "f25c9f1c913cc6b5a016164fdc821ba33989a8e3b114da4a721cdc45be56e6cf",
        )
        assert group.smooth_reciprocal_operator.basis.identifier == (
            identities.smooth_frame_sha256
        )
        assert group.smooth_reciprocal_operator.content_sha256 == (
            identities.smooth_reciprocal_hamiltonian_sha256
        )
        assert group.smooth_hopping_operator.content_sha256 == (
            identities.smooth_hopping_sha256
        )
        assert group.rough_hopping_operator.content_sha256 == (
            identities.rough_hopping_sha256
        )

        with pytest.raises(ValueError, match="authenticate reciprocal matrices"):
            replace(group.smooth_reciprocal_operator, content_sha256="0" * 64)
        with pytest.raises(ValueError, match="authenticate hopping blocks"):
            replace(group.rough_hopping_operator, content_sha256="0" * 64)
        with pytest.raises(ValueError, match="rough hopping form"):
            replace(group, rough_hopping_operator=group.smooth_hopping_operator)

    def test_init__rejects_incomplete_or_ambiguous_representation_metadata(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-ADOPTION-004.

        Requirement: Public represented-family records must reject incomplete mesh and
        ambiguous gauge metadata rather than infer meaning from matrix shape.

        Acceptance: Empty gauge metadata, incomplete hopping representatives, and
        wrong-type or malformed content identities are rejected.
        """
        group = self.adopt().groups[0]
        complete = group.smooth_hopping_operator
        model = complete.hopping_model

        with pytest.raises(ValueError, match="gauge_id must be nonempty"):
            replace(group.smooth_reciprocal_operator, gauge_id="")
        with pytest.raises(ValueError, match="complete mesh"):
            replace(
                complete,
                hopping_model=replace(
                    model,
                    representatives=model.representatives[1:],
                    hopping_blocks=model.hopping_blocks[1:],
                ),
            )
        for represented in (group.smooth_reciprocal_operator, complete):
            with pytest.raises(TypeError, match="built-in str"):
                replace(represented, content_sha256=1)  # type: ignore[arg-type]
            with pytest.raises(ValueError, match="lowercase SHA-256"):
                replace(represented, content_sha256="not-a-digest")

    def test_init__rejects_basis_and_energy_metadata_contradictions(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-ADOPTION-005.

        Requirement: A represented operator family must bind the retained basis
        ordering and exact energy reference, not only matrix rank and content bytes.

        Acceptance: Reordered labels, a changed energy zero, changed matrix units, and
        substitution of another smooth-basis identity each raise ``ValueError``.
        """
        group = self.adopt().groups[0]
        reciprocal = group.smooth_reciprocal_operator
        reordered = Basis(
            identifier=reciprocal.basis.identifier,
            kind=reciprocal.basis.kind,
            ordering=tuple(reversed(reciprocal.basis.ordering)),
            orthonormal=True,
        )

        with pytest.raises(ValueError, match="basis ordering"):
            replace(reciprocal, basis=reordered)
        with pytest.raises(ValueError, match="energy reference"):
            replace(
                reciprocal,
                energy_reference=EnergyReference("different zero", "dimensionless"),
            )

        physical_unit = PhysicalUnit("electron_volt")
        physical_samples = replace(
            reciprocal.samples,
            matrices=tuple(
                ComplexMatrixQuantity(matrix.magnitude, physical_unit)
                for matrix in reciprocal.samples.matrices
            ),
        )
        with pytest.raises(ValueError, match="sample units"):
            replace(reciprocal, samples=physical_samples)

        alternate_basis = replace(
            group.smooth_hopping_operator.basis,
            kind="contradictory smooth basis description",
        )
        alternate_hopping = replace(
            group.smooth_hopping_operator,
            basis=alternate_basis,
        )
        with pytest.raises(ValueError, match="complete basis metadata"):
            replace(group, smooth_hopping_operator=alternate_hopping)

    def test_init__does_not_infer_subspace_from_rank_or_wilson_data(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-ADOPTION-007.

        Requirement: Composite projector identity remains digest-only campaign
        evidence and must not be copied into, or inferred as, retained-space identity.
        Aggregate adoption must preserve the exact correlated source object.

        Acceptance: A standalone group can retain a different source digest without
        changing its mathematical retained space, but substitution into the correlated
        aggregate is rejected because the source object is no longer exact.
        """
        adoption = self.adopt()
        group = adoption.groups[0]
        source = group.source_result
        assert source is adoption.correlated_campaign.campaign_result.groups[0]
        changed_identity_source = replace(
            source,
            identities=replace(
                source.identities,
                smooth_projector_sha256="0" * 64,
            ),
        )

        assert changed_identity_source.wilson is source.wilson
        assert (
            changed_identity_source.hopping_representation
            is source.hopping_representation
        )
        changed_group = replace(group, source_result=changed_identity_source)
        assert changed_group.retained_subspace is group.retained_subspace
        assert changed_group.source_result.identities.smooth_projector_sha256 == (
            "0" * 64
        )
        with pytest.raises(ValueError, match="preserve source objects and order"):
            replace(adoption, groups=(changed_group, adoption.groups[1]))

    def test_init__rejects_finite_parent_graph_contradictions(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-ADOPTION-006.

        Requirement: The public adoption result must intrinsically correlate the
        finite parent's cutoff, mesh, and ambient dimension with the campaign and all
        adopted groups.

        Acceptance: A cutoff-14 parent, a 64-point parent mesh, and a rank-compatible
        but wrong retained ambient dimension each raise ``ValueError``.
        """
        adoption = self.adopt()
        parent = adoption.parent_representation

        wrong_cutoff_parent = replace(
            parent,
            basis=PlaneWaveBasis1D(parent.basis.reciprocal_vector, 14),
        )
        with pytest.raises(ValueError, match="cutoff must match"):
            replace(adoption, parent_representation=wrong_cutoff_parent)

        wrong_mesh_parent = replace(
            parent,
            reciprocal_mesh=CenteredUniformReciprocalMesh1D(
                parent.reciprocal_mesh.reciprocal_period,
                64,
            ),
        )
        with pytest.raises(ValueError, match="mesh must match"):
            replace(adoption, parent_representation=wrong_mesh_parent)

        group = adoption.groups[0]
        wrong_subspace = replace(group.retained_subspace, ambient_dimension=30)
        wrong_operator = replace(
            group.retained_operator,
            retained_subspace=wrong_subspace,
        )
        wrong_group = replace(
            group,
            retained_subspace=wrong_subspace,
            retained_operator=wrong_operator,
            smooth_reciprocal_operator=replace(
                group.smooth_reciprocal_operator,
                retained_operator=wrong_operator,
            ),
            smooth_hopping_operator=replace(
                group.smooth_hopping_operator,
                retained_operator=wrong_operator,
            ),
            rough_hopping_operator=replace(
                group.rough_hopping_operator,
                retained_operator=wrong_operator,
            ),
        )
        with pytest.raises(ValueError, match="ambient dimension"):
            replace(adoption, groups=(wrong_group, adoption.groups[1]))
