"""Typed adoption of retained periodic-1D isolated-band replay artifacts."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitter1D,
    BlockHoppingModelComparator1D,
    BlockHoppingModelComparisonResult1D,
)
from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.campaigns.serialization import CampaignJsonDecoder, JsonValue
from ksdft2effmass.operators import (
    Basis,
    ComplexMatrixQuantity,
    EnergyReference,
    Geometry,
    OperatorRecord,
    ScalarQuantity,
    StateSpace,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.periodic import (
    PeriodicHermiticityStatus,
    PeriodicOperatorReference,
    PeriodicRepresentedRetainedOperator,
    PeriodicRepresentedRetainedOperatorConstructor,
    PeriodicRetainedOperator,
    PeriodicRetainedOperatorConstructionKind,
    PeriodicRetainedOperatorConstructor,
    PeriodicRetainedSubspace,
    PeriodicRetainedSubspaceConstructor,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)
from ksdft2effmass.periodic1d import (
    Periodic1DBandFrameRetainedSubspace,
    Periodic1DCompleteHoppingRepresentationResult,
    Periodic1DFittedHoppingEffectiveModelResult,
    Periodic1DFourierHamiltonianToyModel,
    Periodic1DPlaneWaveParentRepresentation,
    Periodic1DPlaneWaveParentRepresentationConstructor,
    Periodic1DSelectedBandRetentionDefinition,
    Periodic1DTruncatedHoppingEffectiveModelResult,
)
from ksdft2effmass.solid_state import (
    BlockHoppingModel1D,
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
    PlaneWaveReciprocalSewingConstructor,
    ReciprocalBandFramePath1D,
    ReciprocalOperatorFourierTransformer1D,
)

from .isolated import (
    Periodic1DIsolatedBandCampaignDefinition,
    Periodic1DIsolatedBandCampaignJsonSerializer,
)
from .isolated_results import (
    Periodic1DIsolatedBandCampaignResult,
    Periodic1DPlaneWaveCutoffObservation,
)

type ComplexArray = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic1DReplaySourceCorrelation:
    """Retain SHA-256 identities proving correlation to immutable replay sources."""

    input_sha256: str
    reference_result_sha256: str
    producer_script_sha256: str
    replay_script_sha256: str
    replayed_result_sha256: str
    exact_result_bytes_match: bool

    def __post_init__(self) -> None:
        """Check authenticated source identities and exact replay correlation."""
        self._check_args_digest_syntax()
        self._check_args_exact_result_correlation()

    def _check_args_digest_syntax(self) -> None:
        """Require every source identity to use canonical lowercase SHA-256 syntax."""
        # These digests identify immutable source bytes; none is a path or locator.
        digests = (
            ("input_sha256", self.input_sha256),
            ("reference_result_sha256", self.reference_result_sha256),
            ("producer_script_sha256", self.producer_script_sha256),
            ("replay_script_sha256", self.replay_script_sha256),
            ("replayed_result_sha256", self.replayed_result_sha256),
        )
        for name, value in digests:
            if type(value) is not str or len(value) != 64:
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
            if any(character not in "0123456789abcdef" for character in value):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")

    def _check_args_exact_result_correlation(self) -> None:
        """Require the replayed and historical result payloads to be identical."""
        if type(self.exact_result_bytes_match) is not bool:
            raise TypeError("exact_result_bytes_match must be a built-in bool")
        if not self.exact_result_bytes_match:
            raise ValueError("replay artifacts require exact retained-result agreement")
        # Exact byte agreement also requires one shared content identity.
        if self.replayed_result_sha256 != self.reference_result_sha256:
            raise ValueError("replayed and retained result identities must agree")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRangeEffectiveModelArtifacts:
    """Retain separate truncated and fitted coefficient models for one range."""

    hopping_range_cells: int
    truncated_model: BlockHoppingModel1D
    fitted_model: BlockHoppingModel1D
    truncated_coefficients_content_sha256: str
    fitted_coefficients_content_sha256: str

    def __post_init__(self) -> None:
        """Validate range, scalar model dimensions, representatives, and digests."""
        if type(self.hopping_range_cells) is not int or self.hopping_range_cells < 0:
            raise ValueError("hopping_range_cells must be a nonnegative built-in int")
        if type(self.truncated_model) is not BlockHoppingModel1D:
            raise TypeError("truncated_model must be BlockHoppingModel1D")
        if type(self.fitted_model) is not BlockHoppingModel1D:
            raise TypeError("fitted_model must be BlockHoppingModel1D")
        expected = tuple(range(-self.hopping_range_cells, self.hopping_range_cells + 1))
        if self.truncated_model.representatives != expected:
            raise ValueError("truncated representatives must match the declared range")
        if self.fitted_model.representatives != expected:
            raise ValueError("fitted representatives must match the declared range")
        if (
            self.truncated_model.matrix_dimension != 1
            or self.fitted_model.matrix_dimension != 1
        ):
            raise ValueError("isolated-band effective models must be scalar")
        for name, value in (
            (
                "truncated_coefficients_content_sha256",
                self.truncated_coefficients_content_sha256,
            ),
            (
                "fitted_coefficients_content_sha256",
                self.fitted_coefficients_content_sha256,
            ),
        ):
            if type(value) is not str or len(value) != 64:
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
            if any(character not in "0123456789abcdef" for character in value):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DIsolatedBandReplayArtifacts:
    """Retain authenticated sources, frame, and effective-model replay data.

    ``definition`` and ``result`` are the exact immutable objects supplied to the
    authenticating decoder. Scientific adoption must reuse those objects rather than
    substitute same-identifier campaign records after source authentication.
    """

    experiment_id: str
    definition: Periodic1DIsolatedBandCampaignDefinition
    result: Periodic1DIsolatedBandCampaignResult
    source_payload: bytes
    source_payload_sha256: str
    source_correlation: Periodic1DReplaySourceCorrelation
    frame_path: ReciprocalBandFramePath1D
    frame_content_sha256: str
    projector_path_content_sha256: str
    complete_hopping_model: BlockHoppingModel1D
    complete_coefficients_content_sha256: str
    range_artifacts: tuple[Periodic1DRangeEffectiveModelArtifacts, ...]

    def __post_init__(self) -> None:
        """Check authenticated sources and the typed replay-artifact inventory."""
        self._check_args_correlated_sources()
        self._check_args_payload_identity()
        self._check_args_represented_artifacts()
        self._check_args_content_digests()

    def _check_args_correlated_sources(self) -> None:
        """Require the exact definition and result authenticated by the decoder."""
        if type(self.experiment_id) is not str or not self.experiment_id:
            raise ValueError("experiment_id must be a nonempty built-in str")
        if type(self.definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("definition has the wrong exact type")
        if type(self.result) is not Periodic1DIsolatedBandCampaignResult:
            raise TypeError("result has the wrong exact type")
        if self.definition.experiment_id != self.experiment_id:
            raise ValueError("definition and replay experiment identities differ")
        if self.result.source_document.record_id != self.experiment_id:
            raise ValueError("result and replay experiment identities differ")
        if type(self.source_correlation) is not Periodic1DReplaySourceCorrelation:
            raise TypeError("source_correlation has the wrong exact type")
        if self.result.source_document.source_sha256 != (
            self.source_correlation.reference_result_sha256
        ):
            raise ValueError("result differs from the authenticated result source")

    def _check_args_payload_identity(self) -> None:
        """Require the retained sidecar bytes to match their content identity."""
        if type(self.source_payload) is not bytes:
            raise TypeError("source_payload must be bytes")
        if (
            hashlib.sha256(self.source_payload).hexdigest()
            != self.source_payload_sha256
        ):
            raise ValueError("source_payload_sha256 must authenticate source_payload")

    def _check_args_represented_artifacts(self) -> None:
        """Require one scalar frame, complete model, and ordered range inventory."""
        if type(self.frame_path) is not ReciprocalBandFramePath1D:
            raise TypeError("frame_path must be ReciprocalBandFramePath1D")
        if self.frame_path.rank != 1:
            raise ValueError("isolated-band replay frame must have rank one")
        if type(self.complete_hopping_model) is not BlockHoppingModel1D:
            raise TypeError("complete_hopping_model must be BlockHoppingModel1D")
        if self.complete_hopping_model.matrix_dimension != 1:
            raise ValueError("isolated-band complete hopping model must be scalar")
        if not isinstance(self.range_artifacts, tuple) or not self.range_artifacts:
            raise TypeError("range_artifacts must be a nonempty tuple")
        if any(
            type(value) is not Periodic1DRangeEffectiveModelArtifacts
            for value in self.range_artifacts
        ):
            raise TypeError("range_artifacts members have the wrong exact type")
        ranges = tuple(value.hopping_range_cells for value in self.range_artifacts)
        if ranges != tuple(sorted(set(ranges))):
            raise ValueError("effective-model ranges must be unique and increasing")

    def _check_args_content_digests(self) -> None:
        """Require canonical identities for retained numerical arrays."""
        for name, value in (
            ("frame_content_sha256", self.frame_content_sha256),
            ("projector_path_content_sha256", self.projector_path_content_sha256),
            (
                "complete_coefficients_content_sha256",
                self.complete_coefficients_content_sha256,
            ),
        ):
            if type(value) is not str or len(value) != 64:
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
            if any(character not in "0123456789abcdef" for character in value):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DIsolatedBandParentDiscretization:
    """Retain a finite parent representation and cutoff-comparison evidence.

    Parameters
    ----------
    representation
        Finite plane-wave representation used to construct the retained band.
    reference_basis
        Separately identified higher-cutoff finite basis used by the historical
        comparison; it is not the untruncated parent state space.
    comparison_momenta
        Retained reduced momenta at which the finite-cutoff comparison was evaluated.
    compared_band_count
        Positive number of lowest represented bands included in the comparison.
    cutoff_observation
        Historical maximum absolute energy difference for ``representation.cutoff``
        relative to ``reference_basis`` over the declared comparison set.
    provenance_id
        Nonempty identity of the retained comparison provenance.

    Notes
    -----
    The observation is numerical/discretization evidence between two finite Galerkin
    representations. It is not an error estimate for the untruncated model, a
    convergence proof, scientific validation, or uncertainty quantification.
    """

    representation: Periodic1DPlaneWaveParentRepresentation
    reference_basis: PlaneWaveBasis1D
    comparison_momenta: VectorQuantity
    compared_band_count: int
    cutoff_observation: Periodic1DPlaneWaveCutoffObservation
    provenance_id: str

    def __post_init__(self) -> None:
        """Check finite-representation and cutoff-comparison evidence."""
        self._check_args_types()
        self._check_args_comparison_definition()
        self._check_args_cutoff_correlation()
        self._check_args_provenance()

    def _check_args_types(self) -> None:
        """Require exact finite-representation evidence component types."""
        if type(self.representation) is not Periodic1DPlaneWaveParentRepresentation:
            raise TypeError(
                "representation must be Periodic1DPlaneWaveParentRepresentation"
            )
        if type(self.reference_basis) is not PlaneWaveBasis1D:
            raise TypeError("reference_basis must be PlaneWaveBasis1D")
        if type(self.comparison_momenta) is not VectorQuantity:
            raise TypeError("comparison_momenta must be VectorQuantity")
        if type(self.compared_band_count) is not int:
            raise TypeError("compared_band_count must be a built-in int")
        if type(self.cutoff_observation) is not Periodic1DPlaneWaveCutoffObservation:
            raise TypeError(
                "cutoff_observation must be Periodic1DPlaneWaveCutoffObservation"
            )

    def _check_args_comparison_definition(self) -> None:
        """Require a nonempty comparison set that fits the finite basis."""
        if self.comparison_momenta.magnitude.size == 0:
            raise ValueError("comparison_momenta must be nonempty")
        if self.compared_band_count <= 0:
            raise ValueError("compared_band_count must be positive")
        if self.compared_band_count > self.representation.ambient_dimension:
            raise ValueError("compared bands must fit the represented basis")

    def _check_args_cutoff_correlation(self) -> None:
        """Correlate represented cutoff, finite reference, and retained observation."""
        if self.cutoff_observation.cutoff != self.representation.cutoff:
            raise ValueError("cutoff observation must match represented cutoff")
        if self.reference_basis.cutoff <= self.representation.cutoff:
            raise ValueError("reference cutoff must exceed represented cutoff")
        if (
            self.reference_basis.reciprocal_vector
            != self.representation.basis.reciprocal_vector
        ):
            raise ValueError("represented and reference reciprocal vectors must agree")

    def _check_args_provenance(self) -> None:
        """Require one explicit nonempty provenance identity."""
        if type(self.provenance_id) is not str:
            raise TypeError("provenance_id must be a built-in str")
        if self.provenance_id == "":
            raise ValueError("provenance_id must be nonempty")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRangeEffectiveModelAdoption:
    """Bind retained coefficients to explicit truncation and fitting routes.

    Parameters
    ----------
    hopping_range_cells
        Nonnegative symmetric real-space range in lattice cells.
    truncated
        Effective model constructed by truncating the complete hopping representation.
    truncation_replay_comparison
        Coefficient comparison against the authenticated replay truncation route.
    truncation_coefficient_absolute_tolerance
        Resolved nonnegative absolute energy allowance for that comparison.
    fitted
        Effective model constructed by direct reciprocal-space least squares.
    fitting_replay_comparison
        Coefficient comparison against the authenticated replay fitting route.
    fitting_coefficient_absolute_tolerance
        Resolved nonnegative absolute energy allowance for that comparison.

    Notes
    -----
    Route agreement establishes reproducibility of the represented coefficient
    constructions. It does not establish effective-model adequacy, scientific
    validation, parent-model accuracy, or uncertainty quantification.
    """

    hopping_range_cells: int
    truncated: Periodic1DTruncatedHoppingEffectiveModelResult
    truncation_replay_comparison: BlockHoppingModelComparisonResult1D
    truncation_coefficient_absolute_tolerance: float
    fitted: Periodic1DFittedHoppingEffectiveModelResult
    fitting_replay_comparison: BlockHoppingModelComparisonResult1D
    fitting_coefficient_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Check one exact range, route pair, and resolved tolerances."""
        self._check_args_routes()
        self._check_args_comparison(
            "truncation",
            self.truncation_replay_comparison,
            self.truncation_coefficient_absolute_tolerance,
            self.truncated.model,
        )
        self._check_args_comparison(
            "fitting",
            self.fitting_replay_comparison,
            self.fitting_coefficient_absolute_tolerance,
            self.fitted.model,
        )

    def _check_args_routes(self) -> None:
        """Require both route results to implement the declared symmetric range."""
        if type(self.hopping_range_cells) is not int or self.hopping_range_cells < 0:
            raise ValueError("hopping_range_cells must be a nonnegative built-in int")
        if type(self.truncated) is not Periodic1DTruncatedHoppingEffectiveModelResult:
            raise TypeError("truncated has the wrong exact result type")
        if type(self.fitted) is not Periodic1DFittedHoppingEffectiveModelResult:
            raise TypeError("fitted has the wrong exact result type")
        expected = tuple(range(-self.hopping_range_cells, self.hopping_range_cells + 1))
        if self.truncated.truncation.maximum_range != self.hopping_range_cells:
            raise ValueError("truncation maximum_range must match hopping_range_cells")
        if self.truncated.model.representatives != expected:
            raise ValueError("truncated representatives must match hopping_range_cells")
        if self.fitted.fit.representatives != expected:
            raise ValueError("fitted representatives must match hopping_range_cells")

    @staticmethod
    def _check_args_comparison(
        name: str,
        comparison: BlockHoppingModelComparisonResult1D,
        tolerance: float,
        candidate: BlockHoppingModel1D,
    ) -> None:
        """Require one route comparison to own and accept its candidate model."""
        if type(comparison) is not BlockHoppingModelComparisonResult1D:
            raise TypeError(f"{name}_replay_comparison has the wrong exact type")
        if type(tolerance) is not float:
            raise TypeError(
                f"{name}_coefficient_absolute_tolerance must be a built-in float"
            )
        if not np.isfinite(tolerance) or tolerance < 0.0:
            raise ValueError(
                f"{name}_coefficient_absolute_tolerance must be finite and nonnegative"
            )
        if comparison.candidate is not candidate:
            raise ValueError(f"{name} comparison must own the adopted candidate")
        if comparison.coefficient_l2_frobenius_defect.magnitude > tolerance:
            raise ValueError(f"{name} coefficient comparison exceeds tolerance")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DIsolatedBandScientificAdoptionRequest:
    """Declare correlated replay sources and an optional energy tolerance.

    Parameters
    ----------
    definition
        Exact campaign definition correlated to the replay sources.
    result
        Historical campaign result correlated to the replay sources.
    replay
        Authenticated replay artifacts.
    absolute_tolerance
        Optional built-in ``float`` in dimensionless reciprocal-energy units. A
        supplied value is the common absolute allowance for Fourier reconstruction
        and coefficient-route comparisons. ``None`` calculates a separate allowance
        for each energy-valued comparison as binary64 machine epsilon times the
        comparison dimension times the greater of one and the reference norm.
        Reciprocal-coordinate agreement always uses its own independently calculated
        coordinate-scale allowance.

    Notes
    -----
    The coordinate rule uses coordinate count and the maximum of one, reciprocal-period
    magnitude, and maximum coordinate magnitude. The reconstruction rule uses source
    sample count and maximum source-matrix Frobenius norm. Each coefficient rule uses
    block count and the L2 aggregation of reference-block Frobenius norms. Calculated
    allowances describe scale- and dimension-adjusted binary64 comparison policy. They
    are not rigorous forward-error bounds, physical uncertainty, model-adequacy
    thresholds, or scientific acceptance criteria. Automatic calculation raises
    ``OverflowError`` rather than returning a nonfinite allowance.
    """

    definition: Periodic1DIsolatedBandCampaignDefinition
    result: Periodic1DIsolatedBandCampaignResult
    replay: Periodic1DIsolatedBandReplayArtifacts
    absolute_tolerance: float | None = None

    def __post_init__(self) -> None:
        """Check exact correlated sources and the optional energy tolerance."""
        self._check_args_types()
        self._check_args_correlated_replay()
        self._check_args_absolute_tolerance()

    def _check_args_types(self) -> None:
        """Require exact campaign and replay object types."""
        if type(self.definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("definition has the wrong exact type")
        if type(self.result) is not Periodic1DIsolatedBandCampaignResult:
            raise TypeError("result has the wrong exact type")
        if type(self.replay) is not Periodic1DIsolatedBandReplayArtifacts:
            raise TypeError("replay has the wrong exact type")

    def _check_args_correlated_replay(self) -> None:
        """Prevent same-identifier source substitution after authentication."""
        if self.replay.definition is not self.definition:
            raise ValueError("definition must be the replay-authenticated object")
        if self.replay.result is not self.result:
            raise ValueError("result must be the replay-authenticated object")

    def _check_args_absolute_tolerance(self) -> None:
        """Require an optional finite nonnegative built-in float."""
        if self.absolute_tolerance is not None:
            if type(self.absolute_tolerance) is not float:
                raise TypeError("absolute_tolerance must be a built-in float or None")
            if (
                not np.isfinite(self.absolute_tolerance)
                or self.absolute_tolerance < 0.0
            ):
                raise ValueError("absolute_tolerance must be finite and nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DIsolatedBandScientificAdoptionResult:
    """Retain parent, finite-discretization, and reduction layers separately.

    Parameters
    ----------
    parent_model
        Untruncated periodic Fourier toy Hamiltonian.
    parent_representation
        Finite plane-wave Galerkin operator family used by the retained construction.
    parent_discretization
        Explicit finite-cutoff comparison evidence for that representation.
    selected_bands
        Rank-one selected-band retention definition on the finite parent operator.
    retained_subspace
        Gauge-independent retained mathematical space.
    represented_subspace
        Gauge-dependent finite frame path representing the retained space.
    retained_operator
        Exact invariant restriction of the finite parent operator to the retained
        space; it is not an exact restriction of the untruncated parent.
    represented_zone_center_operator
        Dense finite representation of the retained operator at reduced momentum zero.
    complete_hopping
        Complete finite-mesh Fourier representation of the retained operator samples.
    complete_replay_comparison
        Coefficient comparison against the authenticated complete replay inventory.
    complete_coefficient_absolute_tolerance
        Resolved nonnegative absolute energy allowance for that comparison.
    effective_models
        Distinct truncation- and fit-derived finite-range effective-model results.

    Notes
    -----
    Exactness is local to the declared finite Galerkin parent and retained invariant
    restriction. Discretization evidence, represented-coordinate reconstruction, and
    model-reduction comparisons remain separate and imply neither scientific
    validation nor uncertainty quantification.
    """

    parent_model: Periodic1DFourierHamiltonianToyModel
    parent_representation: Periodic1DPlaneWaveParentRepresentation
    parent_discretization: Periodic1DIsolatedBandParentDiscretization
    selected_bands: Periodic1DSelectedBandRetentionDefinition
    retained_subspace: PeriodicRetainedSubspace
    represented_subspace: Periodic1DBandFrameRetainedSubspace
    retained_operator: PeriodicRetainedOperator
    represented_zone_center_operator: PeriodicRepresentedRetainedOperator
    complete_hopping: Periodic1DCompleteHoppingRepresentationResult
    complete_replay_comparison: BlockHoppingModelComparisonResult1D
    complete_coefficient_absolute_tolerance: float
    effective_models: tuple[Periodic1DRangeEffectiveModelAdoption, ...]

    def __post_init__(self) -> None:
        """Validate the exact parent-to-effective-model ownership graph."""
        self._check_args_member_types()
        self._check_args_parent_and_retention_graph()
        self._check_args_complete_route()
        self._check_args_effective_routes()

    def _check_args_member_types(self) -> None:
        """Require each public member to use its exact domain type."""
        if type(self.parent_model) is not Periodic1DFourierHamiltonianToyModel:
            raise TypeError("parent_model has the wrong exact type")
        if type(self.parent_representation) is not (
            Periodic1DPlaneWaveParentRepresentation
        ):
            raise TypeError("parent_representation has the wrong exact type")
        if type(self.parent_discretization) is not (
            Periodic1DIsolatedBandParentDiscretization
        ):
            raise TypeError("parent_discretization has the wrong exact type")
        if type(self.selected_bands) is not Periodic1DSelectedBandRetentionDefinition:
            raise TypeError("selected_bands has the wrong exact type")
        if type(self.retained_subspace) is not PeriodicRetainedSubspace:
            raise TypeError("retained_subspace has the wrong exact type")
        if type(self.represented_subspace) is not Periodic1DBandFrameRetainedSubspace:
            raise TypeError("represented_subspace has the wrong exact type")
        if type(self.retained_operator) is not PeriodicRetainedOperator:
            raise TypeError("retained_operator has the wrong exact type")
        if type(self.represented_zone_center_operator) is not (
            PeriodicRepresentedRetainedOperator
        ):
            raise TypeError("represented_zone_center_operator has the wrong exact type")
        if type(self.complete_hopping) is not (
            Periodic1DCompleteHoppingRepresentationResult
        ):
            raise TypeError("complete_hopping has the wrong exact type")

    def _check_args_parent_and_retention_graph(self) -> None:
        """Require retention to descend from the finite represented parent."""
        if self.parent_representation.parent_model is not self.parent_model:
            raise ValueError("parent representation must compose the exact parent")
        if self.parent_discretization.representation is not self.parent_representation:
            raise ValueError(
                "discretization evidence must own the parent representation"
            )
        if self.selected_bands.retention is not self.retained_subspace.definition:
            raise ValueError("selected bands must define the retained space")
        if self.represented_subspace.retained_subspace is not self.retained_subspace:
            raise ValueError("frame representation must own the retained space")
        if self.retained_operator.retained_subspace is not self.retained_subspace:
            raise ValueError("retained operator must act on the retained space")

        represented_parent = self.parent_representation.represented_operator
        if self.retained_subspace.definition.parent_operator is not represented_parent:
            raise ValueError("retention must select from the finite parent operator")
        if self.retained_operator.parent_operator is not represented_parent:
            raise ValueError("retained operator must restrict the finite parent")
        if self.retained_subspace.ambient_state_space_id != (
            represented_parent.state_space_id
        ):
            raise ValueError("retained ambient space must be the finite parent space")
        if self.retained_subspace.ambient_dimension != (
            self.parent_representation.ambient_dimension
        ):
            raise ValueError("retained ambient dimension must match the finite basis")
        if self.represented_subspace.frame_path.mesh is not (
            self.parent_representation.reciprocal_mesh
        ):
            raise ValueError("retained frame mesh must match the finite parent mesh")

    def _check_args_complete_route(self) -> None:
        """Require complete representations and replay comparison to stay correlated."""
        if self.represented_zone_center_operator.retained_operator is not (
            self.retained_operator
        ):
            raise ValueError("zone-center representation has the wrong operator")
        if self.complete_hopping.retained_operator is not self.retained_operator:
            raise ValueError("complete hopping representation has the wrong operator")
        if type(self.complete_replay_comparison) is not (
            BlockHoppingModelComparisonResult1D
        ):
            raise TypeError("complete_replay_comparison has the wrong exact type")
        if self.complete_replay_comparison.candidate is not (
            self.complete_hopping.transform.hopping_model
        ):
            raise ValueError("complete comparison must own the adopted candidate")
        tolerance = self.complete_coefficient_absolute_tolerance
        if type(tolerance) is not float:
            raise TypeError(
                "complete_coefficient_absolute_tolerance must be a built-in float"
            )
        if not np.isfinite(tolerance) or tolerance < 0.0:
            raise ValueError(
                "complete_coefficient_absolute_tolerance must be finite and nonnegative"
            )
        defect = (
            self.complete_replay_comparison.coefficient_l2_frobenius_defect.magnitude
        )
        if defect > tolerance:
            raise ValueError("complete coefficient comparison exceeds tolerance")

    def _check_args_effective_routes(self) -> None:
        """Require ordered unique ranges on one retained operator."""
        if not isinstance(self.effective_models, tuple) or not self.effective_models:
            raise TypeError("effective_models must be a nonempty tuple")
        if any(
            type(route) is not Periodic1DRangeEffectiveModelAdoption
            for route in self.effective_models
        ):
            raise TypeError("effective_models members have the wrong exact type")
        ranges = tuple(route.hopping_range_cells for route in self.effective_models)
        if ranges != tuple(sorted(set(ranges))):
            raise ValueError("effective-model ranges must be unique and increasing")
        for route in self.effective_models:
            if route.truncated.retained_operator is not self.retained_operator:
                raise ValueError("truncated model has the wrong retained operator")
            if route.fitted.retained_operator is not self.retained_operator:
                raise ValueError("fitted model has the wrong retained operator")


class Periodic1DIsolatedBandReplayArtifactDecoder(CampaignJsonDecoder):
    """Decode and authenticate one closed replay-artifact JSON document."""

    __slots__ = ()

    def execute(
        self,
        payload: bytes,
        *,
        definition: Periodic1DIsolatedBandCampaignDefinition,
        result: Periodic1DIsolatedBandCampaignResult,
        input_payload: bytes,
        reference_result_payload: bytes,
        producer_script_payload: bytes,
        replay_script_payload: bytes,
    ) -> Periodic1DIsolatedBandReplayArtifacts:
        """Return typed artifacts after source, frame, projector, and model checks."""
        for name, value in (
            ("payload", payload),
            ("input_payload", input_payload),
            ("reference_result_payload", reference_result_payload),
            ("producer_script_payload", producer_script_payload),
            ("replay_script_payload", replay_script_payload),
        ):
            if type(value) is not bytes:
                raise TypeError(f"{name} must be bytes")
        if type(definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("definition has the wrong exact type")
        if type(result) is not Periodic1DIsolatedBandCampaignResult:
            raise TypeError("result has the wrong exact type")
        root = self.document(payload)
        expected = {
            "artifact_kind",
            "effective_model_artifacts",
            "evidence_status",
            "experiment_id",
            "limitations",
            "retained_space_representation",
            "runtime",
            "schema_version",
            "source_correlation",
        }
        if set(root) != expected:
            raise ValueError("replay-artifact fields must match schema version one")
        if self.integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported replay-artifact schema version")
        if self.nonempty_string(root["artifact_kind"], "artifact_kind") != (
            "periodic-1d-isolated-band-replay-artifacts"
        ):
            raise ValueError("unsupported replay-artifact kind")
        experiment_id = self.nonempty_string(root["experiment_id"], "experiment_id")
        if experiment_id != definition.experiment_id:
            raise ValueError(
                "replay artifact and campaign experiment identities differ"
            )
        if result.source_document.record_id != experiment_id:
            raise ValueError("replay artifact and retained result identities differ")
        source = self.mapping(root["source_correlation"], "source_correlation")
        decoded_definition = Periodic1DIsolatedBandCampaignJsonSerializer().deserialize(
            input_payload
        )
        definition_serializer = Periodic1DIsolatedBandCampaignJsonSerializer()
        if definition_serializer.serialize(decoded_definition) != (
            definition_serializer.serialize(definition)
        ):
            raise ValueError("definition differs from the authenticated input source")
        correlation = Periodic1DReplaySourceCorrelation(
            input_sha256=self._correlated_hash(source, "input_sha256", input_payload),
            reference_result_sha256=self._correlated_hash(
                source, "reference_result_sha256", reference_result_payload
            ),
            producer_script_sha256=self._correlated_hash(
                source, "producer_script_sha256", producer_script_payload
            ),
            replay_script_sha256=self._correlated_hash(
                source, "replay_script_sha256", replay_script_payload
            ),
            replayed_result_sha256=self.sha256(
                source["replayed_result_sha256"], "replayed_result_sha256"
            ),
            exact_result_bytes_match=self.boolean(
                source["exact_result_bytes_match"], "exact_result_bytes_match"
            ),
        )
        if result.source_document.source_sha256 != correlation.reference_result_sha256:
            raise ValueError("result differs from the authenticated result source")
        retained = self.mapping(
            root["retained_space_representation"],
            "retained_space_representation",
        )
        frame_path, frame_hash, projector_hash = self._frame_path(retained, definition)
        effective = self.mapping(
            root["effective_model_artifacts"], "effective_model_artifacts"
        )
        complete, complete_hash, range_artifacts = self._effective_models(
            effective, definition
        )
        if complete.representatives != result.reduction.hopping_model.representatives:
            raise ValueError(
                "replay complete representatives differ from retained result"
            )
        if any(
            not np.array_equal(replay_block.magnitude, result_block.magnitude)
            for replay_block, result_block in zip(
                complete.hopping_blocks,
                result.reduction.hopping_model.hopping_blocks,
                strict=True,
            )
        ):
            raise ValueError("replay complete hopping differs from retained result")
        return Periodic1DIsolatedBandReplayArtifacts(
            experiment_id=experiment_id,
            definition=definition,
            result=result,
            source_payload=payload,
            source_payload_sha256=hashlib.sha256(payload).hexdigest(),
            source_correlation=correlation,
            frame_path=frame_path,
            frame_content_sha256=frame_hash,
            projector_path_content_sha256=projector_hash,
            complete_hopping_model=complete,
            complete_coefficients_content_sha256=complete_hash,
            range_artifacts=range_artifacts,
        )

    def _frame_path(
        self,
        value: dict[str, JsonValue],
        definition: Periodic1DIsolatedBandCampaignDefinition,
    ) -> tuple[ReciprocalBandFramePath1D, str, str]:
        mesh = CenteredUniformReciprocalMesh1D(
            definition.reciprocal_vector, definition.reciprocal_mesh_size
        )
        retained_mesh = np.asarray(
            self.reals(value["reciprocal_mesh"], "reciprocal_mesh"),
            dtype=np.float64,
        )
        if not np.array_equal(retained_mesh, mesh.coordinates.magnitude):
            raise ValueError(
                "retained reciprocal mesh differs from campaign definition"
            )
        indices = self.integers(
            value["ambient_plane_wave_indices"], "ambient_plane_wave_indices"
        )
        if len(indices) % 2 != 1:
            raise ValueError("ambient plane-wave inventory must have odd dimension")
        basis = PlaneWaveBasis1D(definition.reciprocal_vector, len(indices) // 2)
        if indices != basis.reciprocal_indices:
            raise ValueError("ambient plane-wave indices are not cutoff ordered")
        shape = self.integers(value["frame_shape"], "frame_shape")
        if shape != (mesh.point_count, basis.dimension, 1):
            raise ValueError("frame_shape differs from mesh and basis dimensions")
        frame_rows = self.array(value["parallel_transport_frame"], "frame")
        frame = np.asarray(
            [self._complex_vector(row, "frame row") for row in frame_rows],
            dtype=np.complex128,
        )
        if frame.shape != (mesh.point_count, basis.dimension):
            raise ValueError("frame values differ from declared frame shape")
        frame_hash = self.sha256(value["frame_content_sha256"], "frame hash")
        self._require_array_hash(frame, frame_hash, "frame")
        projectors = np.einsum("ki,kj->kij", frame, frame.conj(), optimize=True)
        projector_hash = self.sha256(
            value["projector_path_content_sha256"], "projector hash"
        )
        self._require_array_hash(projectors, projector_hash, "projector path")
        sewing = PlaneWaveReciprocalSewingConstructor().execute(basis)
        orthonormality_absolute_tolerance = float(
            np.finfo(np.float64).eps * basis.dimension
        )
        path = ReciprocalBandFramePath1D(
            mesh=mesh,
            frames=tuple(
                ComplexMatrixQuantity(row[:, None], Unitless()) for row in frame
            ),
            sewing_map=sewing.coefficient_map,
            orthonormality_absolute_tolerance=orthonormality_absolute_tolerance,
        )
        return path, frame_hash, projector_hash

    def _effective_models(
        self,
        value: dict[str, JsonValue],
        definition: Periodic1DIsolatedBandCampaignDefinition,
    ) -> tuple[
        BlockHoppingModel1D,
        str,
        tuple[Periodic1DRangeEffectiveModelArtifacts, ...],
    ]:
        representatives = self.integers(
            value["complete_representatives_cells"],
            "complete_representatives_cells",
        )
        coefficients = self._complex_vector(
            value["complete_coefficients"], "complete_coefficients"
        )
        complete_hash = self.sha256(
            value["complete_coefficients_content_sha256"], "complete hash"
        )
        self._require_array_hash(coefficients, complete_hash, "complete coefficients")
        complete = self._hopping_model(
            definition.reciprocal_vector, representatives, coefficients
        )
        ranges = tuple(
            self._range_artifact(item, definition.reciprocal_vector)
            for item in self._objects(value["range_artifacts"], "range_artifacts")
        )
        if tuple(item.hopping_range_cells for item in ranges) != (
            definition.hopping_ranges
        ):
            raise ValueError("replay ranges differ from campaign definition")
        return complete, complete_hash, ranges

    def _range_artifact(
        self, value: dict[str, JsonValue], reciprocal_period: ScalarQuantity
    ) -> Periodic1DRangeEffectiveModelArtifacts:
        hopping_range = self.integer(
            value["hopping_range_cells"], "hopping_range_cells"
        )
        representatives = self.integers(
            value["representatives_cells"], "representatives_cells"
        )
        truncated = self._complex_vector(
            value["truncated_coefficients"], "truncated_coefficients"
        )
        fitted = self._complex_vector(
            value["fitted_coefficients"], "fitted_coefficients"
        )
        truncated_hash = self.sha256(
            value["truncated_coefficients_content_sha256"], "truncated hash"
        )
        fitted_hash = self.sha256(
            value["fitted_coefficients_content_sha256"], "fitted hash"
        )
        self._require_array_hash(truncated, truncated_hash, "truncated coefficients")
        self._require_array_hash(fitted, fitted_hash, "fitted coefficients")
        return Periodic1DRangeEffectiveModelArtifacts(
            hopping_range_cells=hopping_range,
            truncated_model=self._hopping_model(
                reciprocal_period, representatives, truncated
            ),
            fitted_model=self._hopping_model(
                reciprocal_period, representatives, fitted
            ),
            truncated_coefficients_content_sha256=truncated_hash,
            fitted_coefficients_content_sha256=fitted_hash,
        )

    @staticmethod
    def _hopping_model(
        reciprocal_period: ScalarQuantity,
        representatives: tuple[int, ...],
        coefficients: ComplexArray,
    ) -> BlockHoppingModel1D:
        if coefficients.shape != (len(representatives),):
            raise ValueError("coefficient count must equal representative count")
        return BlockHoppingModel1D(
            reciprocal_period=reciprocal_period,
            representatives=representatives,
            hopping_blocks=tuple(
                ComplexMatrixQuantity(
                    np.asarray([[coefficient]], dtype=np.complex128), Unitless()
                )
                for coefficient in coefficients
            ),
        )

    def _objects(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        """Return one tuple of strict JSON object representations."""
        return tuple(self.mapping(item, name) for item in self.array(value, name))

    def _complex_vector(self, value: JsonValue, name: str) -> ComplexArray:
        """Decode one vector of real/imaginary JSON pairs."""
        pairs = tuple(self.reals(item, name) for item in self.array(value, name))
        if any(len(pair) != 2 for pair in pairs):
            raise ValueError(f"{name} must contain real/imaginary pairs")
        return np.asarray(
            [complex(pair[0], pair[1]) for pair in pairs], dtype=np.complex128
        )

    def _correlated_hash(
        self, source: dict[str, JsonValue], field: str, payload: bytes
    ) -> str:
        digest = self.sha256(source[field], field)
        if hashlib.sha256(payload).hexdigest() != digest:
            raise ValueError(f"{field} does not authenticate its supplied source")
        return digest

    @staticmethod
    def _require_array_hash(values: ComplexArray, digest: str, name: str) -> None:
        canonical = np.asarray(values, dtype="<c16", order="C")
        if hashlib.sha256(canonical.tobytes(order="C")).hexdigest() != digest:
            raise ValueError(f"{name} content digest differs")


class Periodic1DIsolatedBandScientificAdoption:
    """Adopt replay evidence through explicit retention and reduction actions."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DIsolatedBandScientificAdoptionRequest
    ) -> Periodic1DIsolatedBandScientificAdoptionResult:
        """Construct the parent, retained space/operator, and reduction routes."""
        if type(request) is not Periodic1DIsolatedBandScientificAdoptionRequest:
            raise TypeError("request has the wrong exact type")
        definition = request.definition
        result = request.result
        replay = request.replay
        if definition.experiment_id != replay.experiment_id:
            raise ValueError("definition and replay experiment identities differ")
        if result.source_document.record_id != replay.experiment_id:
            raise ValueError("result and replay experiment identities differ")

        identity = definition.experiment_id
        parent = Periodic1DFourierHamiltonianToyModel(
            model_id=f"{identity}.parent-model",
            state_space_id=f"{identity}.parent-bloch-state-space",
            reciprocal_domain_id=f"{identity}.primitive-reciprocal-domain",
            potential=PeriodicFourierPotential1D(
                period=definition.lattice_period,
                constant_coefficient=ScalarQuantity(0.0, Unitless()),
                cosine_coefficients=VectorQuantity(
                    np.asarray([definition.potential_strength.magnitude]), Unitless()
                ),
                sine_coefficients=VectorQuantity(np.asarray([0.0]), Unitless()),
            ),
            recoil_energy=definition.reciprocal_energy,
        )
        frame = replay.frame_path
        represented_cutoff = definition.plane_wave_cutoffs[-1]
        represented_basis = PlaneWaveBasis1D(
            definition.reciprocal_vector,
            represented_cutoff,
        )
        if represented_basis.dimension != frame.ambient_dimension:
            raise ValueError("replay frame dimension differs from represented cutoff")
        parent_reference = PeriodicOperatorReference(
            model_id=parent.model_id,
            operator_id=(
                f"{identity}.plane-wave-cutoff-{represented_cutoff}-hamiltonian"
            ),
            state_space_id=(
                f"{identity}.plane-wave-cutoff-{represented_cutoff}-bloch-space"
            ),
            spatial_dimension=1,
        )
        parent_representation = (
            Periodic1DPlaneWaveParentRepresentationConstructor().execute(
                representation_id=(
                    f"{identity}.plane-wave-cutoff-{represented_cutoff}-representation"
                ),
                parent_model=parent,
                basis=represented_basis,
                reciprocal_mesh=frame.mesh,
                represented_operator=parent_reference,
                representation_map_id=(
                    f"{identity}.plane-wave-galerkin-cutoff-{represented_cutoff}"
                ),
                provenance_id=replay.source_payload_sha256,
            )
        )
        cutoff_observation = next(
            (
                value
                for value in result.parent_verification.plane_wave_cutoff_study
                if value.cutoff == represented_cutoff
            ),
            None,
        )
        if cutoff_observation is None:
            raise ValueError("represented cutoff has no retained comparison evidence")
        parent_discretization = Periodic1DIsolatedBandParentDiscretization(
            representation=parent_representation,
            reference_basis=PlaneWaveBasis1D(
                definition.reciprocal_vector,
                definition.plane_wave_reference_cutoff,
            ),
            comparison_momenta=definition.parent_sample_momenta,
            compared_band_count=definition.compared_band_count,
            cutoff_observation=cutoff_observation,
            provenance_id=result.source_document.source_sha256,
        )
        retention = PeriodicRetentionDefinition(
            retention_id=(
                f"{identity}.plane-wave-cutoff-{represented_cutoff}-lowest-band-"
                "retention"
            ),
            parent_operator=parent_reference,
            retained_space_id=(
                f"{identity}.plane-wave-cutoff-{represented_cutoff}-lowest-band-space"
            ),
            kind=PeriodicRetentionKind.SELECTED_BANDS,
            rank=1,
            ordered_state_labels=("band-0",),
            reciprocal_domain_id=parent.reciprocal_domain_id,
            construction_record_id=(
                f"{identity}.plane-wave-cutoff-{represented_cutoff}-selected-band-0"
            ),
            assumption_ids=(
                f"{identity}.plane-wave-cutoff-{represented_cutoff}-isolated-band-"
                "assumption",
            ),
            provenance_id=replay.source_payload_sha256,
        )
        selected = Periodic1DSelectedBandRetentionDefinition(
            retention=retention,
            selection=ContiguousBandSelection(lower_index=0, upper_index=0),
        )
        subspace = PeriodicRetainedSubspaceConstructor().execute(
            definition=retention,
            ambient_state_space_id=parent_reference.state_space_id,
            ambient_dimension=frame.ambient_dimension,
            spin_convention="spinless scalar toy model",
            internal_degree_convention="one retained band",
            reciprocal_boundary_convention=(
                "finite-cutoff upper reciprocal-index sewing"
            ),
            provenance_id=replay.source_payload_sha256,
        )
        represented_subspace = Periodic1DBandFrameRetainedSubspace(
            retained_subspace=subspace,
            frame_path=frame,
            frame_content_sha256=replay.frame_content_sha256,
        )
        energy_reference = EnergyReference(
            zero="unshifted parent Hamiltonian zero",
            unit="dimensionless reciprocal-energy unit",
        )
        retained_operator = PeriodicRetainedOperatorConstructor().execute(
            operator_id=(
                f"{identity}.plane-wave-cutoff-{represented_cutoff}-lowest-band-"
                "hamiltonian"
            ),
            parent_operator=parent_reference,
            retained_subspace=subspace,
            construction_kind=(
                PeriodicRetainedOperatorConstructionKind.INVARIANT_RESTRICTION
            ),
            energy_reference=energy_reference,
            hermiticity_status=PeriodicHermiticityStatus.DECLARED_HERMITIAN,
            provenance_id=replay.source_payload_sha256,
        )
        represented_zone_center = self._zone_center_representation(
            retained_operator=retained_operator,
            result=result,
            lattice_period=definition.lattice_period,
            energy_reference=energy_reference,
            provenance_id=replay.source_payload_sha256,
        )

        coordinate_absolute_tolerance = self._coordinate_absolute_tolerance(result)
        reconstruction_absolute_tolerance = self._reconstruction_absolute_tolerance(
            request.absolute_tolerance,
            result,
        )
        transform = ReciprocalOperatorFourierTransformer1D().execute(
            source=result.reduction.reciprocal_samples,
            mesh=replay.frame_path.mesh,
            coordinate_absolute_tolerance=coordinate_absolute_tolerance,
            reconstruction_absolute_tolerance=reconstruction_absolute_tolerance,
        )
        complete = Periodic1DCompleteHoppingRepresentationResult(
            retained_operator=retained_operator,
            transform=transform,
        )
        complete_comparison = BlockHoppingModelComparator1D().execute(
            reference=replay.complete_hopping_model,
            candidate=transform.hopping_model,
            comparison_coordinates=result.reduction.reciprocal_samples.coordinates,
        )
        complete_coefficient_absolute_tolerance = self._coefficient_absolute_tolerance(
            request.absolute_tolerance,
            replay.complete_hopping_model,
        )
        if (
            complete_comparison.coefficient_l2_frobenius_defect.magnitude
            > complete_coefficient_absolute_tolerance
        ):
            raise ValueError("complete action route differs from replay coefficients")
        effective_models = tuple(
            self._effective_model_routes(
                retained_operator=retained_operator,
                result=result,
                complete=replay.complete_hopping_model,
                artifacts=value,
                identity=identity,
                absolute_tolerance=request.absolute_tolerance,
            )
            for value in replay.range_artifacts
        )
        return Periodic1DIsolatedBandScientificAdoptionResult(
            parent_model=parent,
            parent_representation=parent_representation,
            parent_discretization=parent_discretization,
            selected_bands=selected,
            retained_subspace=subspace,
            represented_subspace=represented_subspace,
            retained_operator=retained_operator,
            represented_zone_center_operator=represented_zone_center,
            complete_hopping=complete,
            complete_replay_comparison=complete_comparison,
            complete_coefficient_absolute_tolerance=(
                complete_coefficient_absolute_tolerance
            ),
            effective_models=effective_models,
        )

    @staticmethod
    def _dimension_scaled_binary64_tolerance(
        *, reference_scale: float, comparison_dimension: int
    ) -> float:
        """Return one finite dimension-scaled binary64 comparison allowance."""
        if np.isnan(reference_scale) or reference_scale < 0.0:
            raise ValueError("reference_scale must be nonnegative and not NaN")
        if np.isinf(reference_scale):
            raise OverflowError("calculated reference scale is not finite")
        if type(comparison_dimension) is not int or comparison_dimension <= 0:
            raise ValueError("comparison_dimension must be a positive built-in int")
        unit_scale = max(1.0, reference_scale)
        dimension_factor = float(np.finfo(np.float64).eps * comparison_dimension)
        if dimension_factor > np.finfo(np.float64).max / unit_scale:
            raise OverflowError("calculated absolute tolerance is not finite")
        return float(dimension_factor * unit_scale)

    @classmethod
    def _coordinate_absolute_tolerance(
        cls, result: Periodic1DIsolatedBandCampaignResult
    ) -> float:
        """Calculate a coordinate-scale allowance independent of energy policy."""
        samples = result.reduction.reciprocal_samples
        scale = max(
            1.0,
            abs(samples.reciprocal_period.magnitude),
            float(np.max(np.abs(samples.coordinates.magnitude))),
        )
        return cls._dimension_scaled_binary64_tolerance(
            reference_scale=scale,
            comparison_dimension=samples.coordinates.magnitude.size,
        )

    @classmethod
    def _reconstruction_absolute_tolerance(
        cls,
        requested: float | None,
        result: Periodic1DIsolatedBandCampaignResult,
    ) -> float:
        """Resolve the energy-valued complete reconstruction allowance."""
        if requested is not None:
            return requested
        samples = result.reduction.reciprocal_samples
        scale = max(
            float(np.linalg.norm(value.magnitude)) for value in samples.matrices
        )
        return cls._dimension_scaled_binary64_tolerance(
            reference_scale=scale,
            comparison_dimension=len(samples.matrices),
        )

    @classmethod
    def _coefficient_absolute_tolerance(
        cls,
        requested: float | None,
        reference: BlockHoppingModel1D,
    ) -> float:
        """Resolve one energy-valued coefficient-route comparison allowance."""
        if requested is not None:
            return requested
        scale = float(
            np.sqrt(
                sum(
                    np.linalg.norm(block.magnitude) ** 2
                    for block in reference.hopping_blocks
                )
            )
        )
        return cls._dimension_scaled_binary64_tolerance(
            reference_scale=scale,
            comparison_dimension=len(reference.hopping_blocks),
        )

    @staticmethod
    def _zone_center_representation(
        retained_operator: PeriodicRetainedOperator,
        result: Periodic1DIsolatedBandCampaignResult,
        lattice_period: ScalarQuantity,
        energy_reference: EnergyReference,
        provenance_id: str,
    ) -> PeriodicRepresentedRetainedOperator:
        coordinates = result.reduction.reciprocal_samples.coordinates.magnitude
        zone_center_index = int(np.flatnonzero(coordinates == 0.0)[0])
        matrix = result.reduction.reciprocal_samples.matrices[
            zone_center_index
        ].magnitude
        identity = result.source_document.record_id
        record = OperatorRecord(
            identifier=f"{identity}.zone-center-represented-operator",
            operator_kind="lowest-band Hamiltonian at reduced momentum zero",
            matrix=matrix,
            state_space=StateSpace(
                identifier=retained_operator.retained_subspace.retained_space_id,
                kind="one-dimensional selected-band fiber",
                dimension=1,
            ),
            basis=Basis(
                identifier=f"{identity}.parallel-transport-zone-center-frame",
                kind="retained band frame",
                ordering=("band-0",),
                orthonormal=True,
            ),
            geometry=Geometry(
                system="dimensionless one-dimensional periodic toy system",
                cell=(
                    (lattice_period.magnitude, 0.0, 0.0),
                    (0.0, 1.0, 0.0),
                    (0.0, 0.0, 1.0),
                ),
                boundary_conditions="periodic",
                coordinate_convention=(
                    "row lattice vectors; first row is the physical toy period"
                ),
                length_unit="dimensionless",
            ),
            energy_reference=energy_reference,
            provenance={"replay_artifact_sha256": provenance_id},
        )
        return PeriodicRepresentedRetainedOperatorConstructor().execute(
            representation_id=f"{identity}.zone-center-representation",
            retained_operator=retained_operator,
            operator_record=record,
            representation_map_id=f"{identity}.zone-center-frame-map",
            gauge_id=f"{identity}.parallel-transport-gauge",
            provenance_id=provenance_id,
        )

    @staticmethod
    def _effective_model_routes(
        retained_operator: PeriodicRetainedOperator,
        result: Periodic1DIsolatedBandCampaignResult,
        complete: BlockHoppingModel1D,
        artifacts: Periodic1DRangeEffectiveModelArtifacts,
        identity: str,
        absolute_tolerance: float | None,
    ) -> Periodic1DRangeEffectiveModelAdoption:
        hopping_range = artifacts.hopping_range_cells
        truncation = BlockHoppingTruncator1D().execute(
            source=complete,
            maximum_range=hopping_range,
        )
        truncation_comparison = BlockHoppingModelComparator1D().execute(
            reference=artifacts.truncated_model,
            candidate=truncation.truncated,
            comparison_coordinates=result.reduction.reciprocal_samples.coordinates,
        )
        truncation_coefficient_absolute_tolerance = (
            Periodic1DIsolatedBandScientificAdoption._coefficient_absolute_tolerance(
                absolute_tolerance,
                artifacts.truncated_model,
            )
        )
        if (
            truncation_comparison.coefficient_l2_frobenius_defect.magnitude
            > truncation_coefficient_absolute_tolerance
        ):
            raise ValueError("truncation action route differs from replay coefficients")
        representatives = tuple(range(-hopping_range, hopping_range + 1))
        weights = VectorQuantity(
            np.ones(len(result.reduction.reciprocal_samples.matrices)), Unitless()
        )
        fit = BlockHoppingLeastSquaresFitter1D().execute(
            source=result.reduction.reciprocal_samples,
            representatives=representatives,
            weights=weights,
        )
        fit_comparison = BlockHoppingModelComparator1D().execute(
            reference=artifacts.fitted_model,
            candidate=fit.fitted_model,
            comparison_coordinates=result.reduction.reciprocal_samples.coordinates,
        )
        fitting_coefficient_absolute_tolerance = (
            Periodic1DIsolatedBandScientificAdoption._coefficient_absolute_tolerance(
                absolute_tolerance,
                artifacts.fitted_model,
            )
        )
        if (
            fit_comparison.coefficient_l2_frobenius_defect.magnitude
            > fitting_coefficient_absolute_tolerance
        ):
            raise ValueError("fitting action route differs from replay coefficients")
        return Periodic1DRangeEffectiveModelAdoption(
            hopping_range_cells=hopping_range,
            truncated=Periodic1DTruncatedHoppingEffectiveModelResult(
                effective_model_id=f"{identity}.truncated-range-{hopping_range}",
                retained_operator=retained_operator,
                truncation=truncation,
            ),
            truncation_replay_comparison=truncation_comparison,
            truncation_coefficient_absolute_tolerance=(
                truncation_coefficient_absolute_tolerance
            ),
            fitted=Periodic1DFittedHoppingEffectiveModelResult(
                effective_model_id=f"{identity}.fitted-range-{hopping_range}",
                retained_operator=retained_operator,
                fit=fit,
            ),
            fitting_replay_comparison=fit_comparison,
            fitting_coefficient_absolute_tolerance=(
                fitting_coefficient_absolute_tolerance
            ),
        )


__all__ = [
    "Periodic1DIsolatedBandParentDiscretization",
    "Periodic1DIsolatedBandReplayArtifactDecoder",
    "Periodic1DIsolatedBandReplayArtifacts",
    "Periodic1DIsolatedBandScientificAdoption",
    "Periodic1DIsolatedBandScientificAdoptionRequest",
    "Periodic1DIsolatedBandScientificAdoptionResult",
    "Periodic1DRangeEffectiveModelAdoption",
    "Periodic1DRangeEffectiveModelArtifacts",
    "Periodic1DReplaySourceCorrelation",
]
