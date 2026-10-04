"""Scientific adoption of retained periodic-1D composite operator forms.

This module constructs finite-parent retained-operator identities from already
correlated Appendix G input and result records. It performs no historical calculation,
frame reconstruction, gauge selection, external execution, or payload rewriting.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.operators import Basis, EnergyReference, ScalarQuantity, Unitless
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
from ksdft2effmass.periodic1d import (
    Periodic1DFourierHamiltonianToyModel,
    Periodic1DPlaneWaveParentRepresentation,
    Periodic1DPlaneWaveParentRepresentationConstructor,
    Periodic1DRetainedBandGroupDefinition,
    Periodic1DRetainedOperatorHoppingRepresentation,
    Periodic1DRetainedOperatorReciprocalRepresentation,
    Periodic1DSelectedBandRetentionDefinition,
)
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
)

from .composite_results import Periodic1DCompositeBandGroupResult
from .wilson_workflows import Periodic1DCompositeCampaignWorkflowResult


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeOperatorGroupAdoption:
    """Retain one gauge-independent operator and its three represented forms.

    Parameters
    ----------
    source_result
        Exact historical group result owning diagnostics and artifact identities.
    selected_bands
        Finite-parent selected-band retention definition.
    retained_subspace
        Gauge-independent retained mathematical space. The historical smooth-projector
        digest remains evidence owned by ``source_result`` because no projector
        coordinates are retained.
    retained_operator
        Exact invariant restriction of the finite plane-wave parent operator.
    smooth_reciprocal_operator
        Smooth-gauge reciprocal-matrix family.
    smooth_hopping_operator
        Complete smooth-gauge hopping family.
    rough_hopping_operator
        Complete rough-gauge hopping family.

    Raises
    ------
    TypeError
        If a member has the wrong exact semantic type.
    ValueError
        If ownership, selection, gauge, represented data, or artifact identities do
        not remain correlated.

    Notes
    -----
    The historical result retains no rough-gauge reciprocal matrices, frame array
    bytes, or projector coordinates. This record does not reconstruct any of them. The
    retained space and exact operator remain gauge-independent while the three available
    represented forms are explicitly gauge-qualified. ``source_result`` remains the
    campaign owner of all diagnostics, route outcomes, and its authenticated
    smooth-projector digest. That digest is not copied into retained-space identity or
    promoted to a represented projector binding.
    """

    source_result: Periodic1DCompositeBandGroupResult
    selected_bands: Periodic1DSelectedBandRetentionDefinition
    retained_subspace: PeriodicRetainedSubspace
    retained_operator: PeriodicRetainedOperator
    smooth_reciprocal_operator: Periodic1DRetainedOperatorReciprocalRepresentation
    smooth_hopping_operator: Periodic1DRetainedOperatorHoppingRepresentation
    rough_hopping_operator: Periodic1DRetainedOperatorHoppingRepresentation

    def __post_init__(self) -> None:
        """Check exact member types and the complete group ownership graph."""
        self._check_args_member_types()
        self._check_args_retention_graph()
        self._check_args_representations()
        self._check_args_artifact_identities()

    def _check_args_member_types(self) -> None:
        """Require every public member to use its exact domain type."""
        expected = (
            ("source_result", self.source_result, Periodic1DCompositeBandGroupResult),
            (
                "selected_bands",
                self.selected_bands,
                Periodic1DSelectedBandRetentionDefinition,
            ),
            ("retained_subspace", self.retained_subspace, PeriodicRetainedSubspace),
            ("retained_operator", self.retained_operator, PeriodicRetainedOperator),
            (
                "smooth_reciprocal_operator",
                self.smooth_reciprocal_operator,
                Periodic1DRetainedOperatorReciprocalRepresentation,
            ),
            (
                "smooth_hopping_operator",
                self.smooth_hopping_operator,
                Periodic1DRetainedOperatorHoppingRepresentation,
            ),
            (
                "rough_hopping_operator",
                self.rough_hopping_operator,
                Periodic1DRetainedOperatorHoppingRepresentation,
            ),
        )
        for name, value, expected_type in expected:
            if type(value) is not expected_type:
                raise TypeError(f"{name} has the wrong exact type")

    def _check_args_retention_graph(self) -> None:
        """Require the selected bands, retained space, and exact operator to agree."""
        if self.selected_bands.retention is not self.retained_subspace.definition:
            raise ValueError("selected bands must define the retained subspace")
        if self.retained_operator.retained_subspace is not self.retained_subspace:
            raise ValueError("retained operator must act on the retained subspace")
        if self.selected_bands.band_indices != self.source_result.band_indices:
            raise ValueError("selected bands must match the historical group")

    def _check_args_representations(self) -> None:
        """Keep every represented form on one operator with explicit gauges."""
        represented = (
            self.smooth_reciprocal_operator,
            self.smooth_hopping_operator,
            self.rough_hopping_operator,
        )
        if any(
            value.retained_operator is not self.retained_operator
            for value in represented
        ):
            raise ValueError("every represented form must bind the retained operator")
        if self.smooth_reciprocal_operator.samples is not (
            self.source_result.hopping_representation.smooth_reciprocal_hamiltonians
        ):
            raise ValueError("smooth reciprocal form must preserve the source samples")
        if self.smooth_hopping_operator.hopping_model is not (
            self.source_result.hopping_representation.smooth_hopping_model
        ):
            raise ValueError("smooth hopping form must preserve the source blocks")
        if self.rough_hopping_operator.hopping_model is not (
            self.source_result.hopping_representation.rough_hopping_model
        ):
            raise ValueError("rough hopping form must preserve the source blocks")
        if self.smooth_reciprocal_operator.gauge_id != (
            self.smooth_hopping_operator.gauge_id
        ):
            raise ValueError("smooth represented forms must share one gauge identity")
        if self.smooth_reciprocal_operator.basis != (
            self.smooth_hopping_operator.basis
        ):
            raise ValueError(
                "smooth represented forms must share complete basis metadata"
            )
        smooth_basis_id = self.source_result.identities.smooth_frame_sha256
        if self.smooth_reciprocal_operator.basis.identifier != smooth_basis_id:
            raise ValueError("smooth forms must identify the retained smooth frame")
        if (
            self.rough_hopping_operator.gauge_id
            == self.smooth_hopping_operator.gauge_id
        ):
            raise ValueError("rough and smooth gauge identities must differ")

    def _check_args_artifact_identities(self) -> None:
        """Preserve historical content identities on their represented arrays."""
        identities = self.source_result.identities
        if self.smooth_reciprocal_operator.content_sha256 != (
            identities.smooth_reciprocal_hamiltonian_sha256
        ):
            raise ValueError("smooth reciprocal content identity must be preserved")
        if (
            self.smooth_hopping_operator.content_sha256
            != identities.smooth_hopping_sha256
        ):
            raise ValueError("smooth hopping content identity must be preserved")
        if (
            self.rough_hopping_operator.content_sha256
            != identities.rough_hopping_sha256
        ):
            raise ValueError("rough hopping content identity must be preserved")

    @property
    def group_id(self) -> str:
        """Return the stable historical band-group identity."""
        return self.source_result.group_id


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeScientificAdoptionRequest:
    """Provide one already correlated composite campaign for scientific adoption.

    Parameters
    ----------
    correlated_campaign
        Typed input/result correlation retaining the exact source objects and their
        SHA-256 identities.
    """

    correlated_campaign: Periodic1DCompositeCampaignWorkflowResult

    def __post_init__(self) -> None:
        """Require the exact correlated campaign result type."""
        if (
            type(self.correlated_campaign)
            is not Periodic1DCompositeCampaignWorkflowResult
        ):
            raise TypeError(
                "correlated_campaign must be Periodic1DCompositeCampaignWorkflowResult"
            )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeScientificAdoptionResult:
    """Retain the finite parent and all adopted composite operator groups.

    Parameters
    ----------
    correlated_campaign
        Exact correlated input and historical result records used by the adoption.
    parent_model
        Untruncated Fourier toy parent from the correlated definition.
    parent_representation
        Cutoff-qualified finite plane-wave parent operator on the historical mesh.
    groups
        Ordered retained groups with gauge-independent operators and explicit
        represented forms.

    Notes
    -----
    Exact restriction is asserted only relative to ``parent_representation``. This
    result records no untruncated-parent error bound, frame reconstruction, scientific
    validation, or uncertainty quantification.
    """

    correlated_campaign: Periodic1DCompositeCampaignWorkflowResult
    parent_model: Periodic1DFourierHamiltonianToyModel
    parent_representation: Periodic1DPlaneWaveParentRepresentation
    groups: tuple[Periodic1DCompositeOperatorGroupAdoption, ...]

    def __post_init__(self) -> None:
        """Check exact source ownership, finite parentage, and ordered groups."""
        self._check_args_member_types()
        self._check_args_parent_graph()
        self._check_args_groups()
        self._check_args_represented_graph()

    def _check_args_member_types(self) -> None:
        """Require exact campaign, parent-model, and representation types."""
        if (
            type(self.correlated_campaign)
            is not Periodic1DCompositeCampaignWorkflowResult
        ):
            raise TypeError("correlated_campaign has the wrong exact type")
        if type(self.parent_model) is not Periodic1DFourierHamiltonianToyModel:
            raise TypeError("parent_model has the wrong exact type")
        if (
            type(self.parent_representation)
            is not Periodic1DPlaneWaveParentRepresentation
        ):
            raise TypeError("parent_representation has the wrong exact type")

    def _check_args_parent_graph(self) -> None:
        """Correlate the finite parent with the exact campaign controls."""
        if self.parent_model is not self.correlated_campaign.definition.parent_model:
            raise ValueError("parent model must be the correlated definition object")
        if self.parent_representation.parent_model is not self.parent_model:
            raise ValueError("parent representation must compose the parent model")
        definition = self.correlated_campaign.definition
        if self.parent_representation.cutoff != definition.plane_wave_cutoff:
            raise ValueError("parent representation cutoff must match the campaign")
        if (
            self.parent_representation.reciprocal_mesh.point_count
            != definition.reciprocal_mesh_size
        ):
            raise ValueError("parent representation mesh must match the campaign")

    def _check_args_groups(self) -> None:
        """Require the exact nonempty source-group inventory and order."""
        if (
            not isinstance(self.groups, tuple)
            or not self.groups
            or any(
                type(group) is not Periodic1DCompositeOperatorGroupAdoption
                for group in self.groups
            )
        ):
            raise TypeError("groups must be a nonempty typed tuple")
        source_groups = self.correlated_campaign.campaign_result.groups
        if len(self.groups) != len(source_groups) or any(
            group.source_result is not source
            for group, source in zip(self.groups, source_groups, strict=True)
        ):
            raise ValueError("adopted groups must preserve source objects and order")

    def _check_args_represented_graph(self) -> None:
        """Bind every group and represented mesh to the finite parent."""
        parent = self.parent_representation.represented_operator
        if any(
            group.retained_operator.parent_operator is not parent
            for group in self.groups
        ):
            raise ValueError("every retained operator must restrict the finite parent")
        for group in self.groups:
            if group.retained_subspace.ambient_dimension != (
                self.parent_representation.ambient_dimension
            ):
                raise ValueError("retained ambient dimension must match finite parent")
            represented_forms = (
                group.smooth_reciprocal_operator,
                group.smooth_hopping_operator,
                group.rough_hopping_operator,
            )
            if any(
                form.reciprocal_mesh is not self.parent_representation.reciprocal_mesh
                for form in represented_forms
            ):
                raise ValueError("represented meshes must be the finite parent mesh")


class Periodic1DCompositeScientificAdoption:
    """Construct finite-parent retained operators and gauge-qualified forms."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DCompositeScientificAdoptionRequest
    ) -> Periodic1DCompositeScientificAdoptionResult:
        """Adopt correlated composite records without rerunning the calculation."""
        if type(request) is not Periodic1DCompositeScientificAdoptionRequest:
            raise TypeError(
                "request must be Periodic1DCompositeScientificAdoptionRequest"
            )
        correlated = request.correlated_campaign
        definition = correlated.definition
        parent = definition.parent_model
        identity = definition.experiment_id
        reciprocal_period = ScalarQuantity(
            parent.potential.reciprocal_period_in(ScalarQuantity(1.0, Unitless())),
            Unitless(),
        )
        mesh = CenteredUniformReciprocalMesh1D(
            reciprocal_period,
            definition.reciprocal_mesh_size,
        )
        basis = PlaneWaveBasis1D(reciprocal_period, definition.plane_wave_cutoff)
        parent_reference = PeriodicOperatorReference(
            model_id=parent.model_id,
            operator_id=(
                f"{identity}.plane-wave-cutoff-{definition.plane_wave_cutoff}-"
                "hamiltonian"
            ),
            state_space_id=(
                f"{identity}.plane-wave-cutoff-{definition.plane_wave_cutoff}-"
                "bloch-space"
            ),
            spatial_dimension=1,
        )
        parent_representation = (
            Periodic1DPlaneWaveParentRepresentationConstructor().execute(
                representation_id=(
                    f"{identity}.plane-wave-cutoff-{definition.plane_wave_cutoff}-"
                    "representation"
                ),
                parent_model=parent,
                basis=basis,
                reciprocal_mesh=mesh,
                represented_operator=parent_reference,
                representation_map_id=(
                    f"{identity}.plane-wave-galerkin-cutoff-"
                    f"{definition.plane_wave_cutoff}"
                ),
                provenance_id=correlated.input_sha256,
            )
        )
        adopted_groups = tuple(
            self._adopt_group(
                identity=identity,
                definition_group=definition_group,
                source_group=source_group,
                parent_reference=parent_reference,
                parent_representation=parent_representation,
                provenance_id=correlated.result_sha256,
            )
            for definition_group, source_group in zip(
                definition.retained_band_groups,
                correlated.campaign_result.groups,
                strict=True,
            )
        )
        return Periodic1DCompositeScientificAdoptionResult(
            correlated_campaign=correlated,
            parent_model=parent,
            parent_representation=parent_representation,
            groups=adopted_groups,
        )

    @staticmethod
    def _adopt_group(
        *,
        identity: str,
        definition_group: Periodic1DRetainedBandGroupDefinition,
        source_group: Periodic1DCompositeBandGroupResult,
        parent_reference: PeriodicOperatorReference,
        parent_representation: Periodic1DPlaneWaveParentRepresentation,
        provenance_id: str,
    ) -> Periodic1DCompositeOperatorGroupAdoption:
        """Construct one finite-parent retained group and its available forms."""
        # The correlated Workflow has already established exact group order and band
        # inventories. Keep the private construction boundary exact as well.
        if type(definition_group) is not Periodic1DRetainedBandGroupDefinition:
            raise TypeError("definition_group has the wrong exact type")
        group_id = definition_group.identifier
        if source_group.group_id != group_id:
            raise ValueError("definition and source group identities must agree")
        representation = source_group.hopping_representation
        represented_units = (
            representation.smooth_reciprocal_hamiltonians.matrices[0].unit,
            representation.smooth_hopping_model.hopping_blocks[0].unit,
            representation.rough_hopping_model.hopping_blocks[0].unit,
        )
        if any(not isinstance(unit, Unitless) for unit in represented_units):
            raise ValueError("composite represented energies must be unitless")
        prefix = (
            f"{identity}.plane-wave-cutoff-{parent_representation.cutoff}.{group_id}"
        )
        selection = ContiguousBandSelection(
            definition_group.lower_index,
            definition_group.upper_index,
        )
        retention = PeriodicRetentionDefinition(
            retention_id=f"{prefix}.retention",
            parent_operator=parent_reference,
            retained_space_id=f"{prefix}.retained-space",
            kind=PeriodicRetentionKind.SELECTED_BANDS,
            rank=selection.band_count,
            ordered_state_labels=tuple(
                f"band-{index}" for index in source_group.band_indices
            ),
            reciprocal_domain_id=parent_representation.parent_model.reciprocal_domain_id,
            construction_record_id=f"{prefix}.contiguous-band-selection",
            assumption_ids=(),
            provenance_id=provenance_id,
        )
        selected = Periodic1DSelectedBandRetentionDefinition(retention, selection)
        subspace = PeriodicRetainedSubspaceConstructor().execute(
            definition=retention,
            ambient_state_space_id=parent_reference.state_space_id,
            ambient_dimension=parent_representation.ambient_dimension,
            spin_convention="spinless scalar toy model",
            internal_degree_convention=(
                "ordered retained parent-band indices "
                + ",".join(str(index) for index in source_group.band_indices)
            ),
            reciprocal_boundary_convention=(
                "half-open centered mesh with finite-cutoff reciprocal sewing"
            ),
            provenance_id=provenance_id,
        )
        retained_operator = PeriodicRetainedOperatorConstructor().execute(
            operator_id=f"{prefix}.retained-hamiltonian",
            parent_operator=parent_reference,
            retained_subspace=subspace,
            construction_kind=(
                PeriodicRetainedOperatorConstructionKind.INVARIANT_RESTRICTION
            ),
            energy_reference=EnergyReference(
                zero="unshifted parent Hamiltonian zero in E_G-scaled coordinates",
                unit="dimensionless",
            ),
            hermiticity_status=PeriodicHermiticityStatus.DECLARED_HERMITIAN,
            provenance_id=provenance_id,
        )
        smooth_gauge_id = f"{prefix}.closed-polar-smooth-gauge"
        rough_gauge_id = f"{prefix}.rough-gauge"
        smooth_basis = Basis(
            identifier=source_group.identities.smooth_frame_sha256,
            kind="closed-polar smooth retained-band frame",
            ordering=retention.ordered_state_labels,
            orthonormal=True,
        )
        rough_basis = Basis(
            identifier=f"{prefix}.rough-gauge-basis-convention",
            kind="rough unitary transform of the smooth retained-band frame",
            ordering=retention.ordered_state_labels,
            orthonormal=True,
        )
        reciprocal = Periodic1DRetainedOperatorReciprocalRepresentation(
            representation_id=f"{prefix}.smooth-reciprocal-representation",
            retained_operator=retained_operator,
            reciprocal_mesh=parent_representation.reciprocal_mesh,
            samples=representation.smooth_reciprocal_hamiltonians,
            basis=smooth_basis,
            energy_reference=retained_operator.energy_reference,
            representation_map_id=f"{prefix}.smooth-frame-reciprocal-map",
            gauge_id=smooth_gauge_id,
            content_sha256=(
                source_group.identities.smooth_reciprocal_hamiltonian_sha256
            ),
            provenance_id=provenance_id,
        )
        smooth_hopping = Periodic1DRetainedOperatorHoppingRepresentation(
            representation_id=f"{prefix}.smooth-complete-hopping-representation",
            retained_operator=retained_operator,
            reciprocal_mesh=parent_representation.reciprocal_mesh,
            hopping_model=representation.smooth_hopping_model,
            basis=smooth_basis,
            energy_reference=retained_operator.energy_reference,
            representation_map_id=f"{prefix}.smooth-complete-fourier-map",
            gauge_id=smooth_gauge_id,
            content_sha256=source_group.identities.smooth_hopping_sha256,
            provenance_id=provenance_id,
        )
        rough_hopping = Periodic1DRetainedOperatorHoppingRepresentation(
            representation_id=f"{prefix}.rough-complete-hopping-representation",
            retained_operator=retained_operator,
            reciprocal_mesh=parent_representation.reciprocal_mesh,
            hopping_model=representation.rough_hopping_model,
            basis=rough_basis,
            energy_reference=retained_operator.energy_reference,
            representation_map_id=f"{prefix}.rough-complete-fourier-map",
            gauge_id=rough_gauge_id,
            content_sha256=source_group.identities.rough_hopping_sha256,
            provenance_id=provenance_id,
        )
        return Periodic1DCompositeOperatorGroupAdoption(
            source_result=source_group,
            selected_bands=selected,
            retained_subspace=subspace,
            retained_operator=retained_operator,
            smooth_reciprocal_operator=reciprocal,
            smooth_hopping_operator=smooth_hopping,
            rough_hopping_operator=rough_hopping,
        )


__all__ = [
    "Periodic1DCompositeOperatorGroupAdoption",
    "Periodic1DCompositeScientificAdoption",
    "Periodic1DCompositeScientificAdoptionRequest",
    "Periodic1DCompositeScientificAdoptionResult",
]
