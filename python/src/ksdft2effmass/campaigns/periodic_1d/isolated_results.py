"""Typed retained results for the Appendix G isolated-band campaign."""

from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.solid_state import BlockHoppingModel1D, ReciprocalOperatorSamples1D

from .result_documents import (
    Periodic1DJsonObject,
    Periodic1DRetainedResultDocument,
    Periodic1DRetainedResultJsonSerializer,
    Periodic1DRetainedResultKind,
)


@dataclass(frozen=True, slots=True)
class Periodic1DPlaneWaveCutoffObservation:
    """Retain one dimensionless plane-wave cutoff error observation."""

    cutoff: int
    maximum_first_bands_absolute_error: float

    def __post_init__(self) -> None:
        """Require a positive cutoff and finite nonnegative error."""
        if type(self.cutoff) is not int or self.cutoff <= 0:
            raise ValueError("cutoff must be a positive built-in int")
        if (
            type(self.maximum_first_bands_absolute_error) is not float
            or not np.isfinite(self.maximum_first_bands_absolute_error)
            or self.maximum_first_bands_absolute_error < 0.0
        ):
            raise ValueError("maximum error must be a finite nonnegative float")


@dataclass(frozen=True, slots=True)
class Periodic1DFiniteDifferenceGridObservation:
    """Retain one dimensionless periodic finite-difference error observation."""

    interior_cell_points: int
    grid_spacing_over_period: float
    maximum_first_bands_absolute_error: float

    def __post_init__(self) -> None:
        """Require a useful grid and finite positive spacing and error."""
        if type(self.interior_cell_points) is not int or self.interior_cell_points < 3:
            raise ValueError(
                "interior_cell_points must be an integer of at least three"
            )
        for name, value in (
            ("grid_spacing_over_period", self.grid_spacing_over_period),
            (
                "maximum_first_bands_absolute_error",
                self.maximum_first_bands_absolute_error,
            ),
        ):
            if type(value) is not float or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative float")
        if self.grid_spacing_over_period == 0.0:
            raise ValueError("grid_spacing_over_period must be positive")


@dataclass(frozen=True, slots=True)
class Periodic1DLowModeOperatorObservation:
    """Retain one common-subspace operator comparison observation."""

    interior_cell_points: int
    low_mode_cutoff: int
    maximum_low_mode_operator_frobenius_error: float

    def __post_init__(self) -> None:
        """Validate represented dimensions and dimensionless error."""
        if type(self.interior_cell_points) is not int or self.interior_cell_points < 3:
            raise ValueError(
                "interior_cell_points must be an integer of at least three"
            )
        if type(self.low_mode_cutoff) is not int or self.low_mode_cutoff < 0:
            raise ValueError("low_mode_cutoff must be a nonnegative built-in int")
        if (
            type(self.maximum_low_mode_operator_frobenius_error) is not float
            or not np.isfinite(self.maximum_low_mode_operator_frobenius_error)
            or self.maximum_low_mode_operator_frobenius_error < 0.0
        ):
            raise ValueError("operator error must be a finite nonnegative float")


@dataclass(frozen=True, slots=True)
class Periodic1DWeakPotentialGapObservation:
    """Retain one dimensionless weak-potential gap comparison."""

    potential_strength: float
    zone_boundary_gap: float
    leading_perturbative_gap: float
    relative_deviation_from_leading_gap: float

    def __post_init__(self) -> None:
        """Require finite nonnegative dimensionless gap diagnostics."""
        for name, value in (
            ("potential_strength", self.potential_strength),
            ("zone_boundary_gap", self.zone_boundary_gap),
            ("leading_perturbative_gap", self.leading_perturbative_gap),
            (
                "relative_deviation_from_leading_gap",
                self.relative_deviation_from_leading_gap,
            ),
        ):
            if type(value) is not float or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative float")


@dataclass(frozen=True, slots=True)
class Periodic1DParentRepresentationVerificationResult:
    """Retain all typed parent-representation verification channels."""

    plane_wave_cutoff_study: tuple[Periodic1DPlaneWaveCutoffObservation, ...]
    finite_difference_grid_study: tuple[Periodic1DFiniteDifferenceGridObservation, ...]
    common_low_mode_operator_study: tuple[Periodic1DLowModeOperatorObservation, ...]
    weak_potential_gap_study: tuple[Periodic1DWeakPotentialGapObservation, ...]
    mathieu_zone_center_lowest: float
    mathieu_zone_boundary_lowest_two: tuple[float, float]
    mathieu_plane_wave_zone_center_absolute_error: float
    mathieu_plane_wave_zone_boundary_maximum_absolute_error: float
    mathieu_q_convention: str
    inversion_maximum_absolute_energy: float
    potential_sign_translation_maximum_absolute_energy: float

    def __post_init__(self) -> None:
        """Require nonempty typed channels and finite scalar diagnostics."""
        typed_channels = (
            (self.plane_wave_cutoff_study, Periodic1DPlaneWaveCutoffObservation),
            (
                self.finite_difference_grid_study,
                Periodic1DFiniteDifferenceGridObservation,
            ),
            (
                self.common_low_mode_operator_study,
                Periodic1DLowModeOperatorObservation,
            ),
            (self.weak_potential_gap_study, Periodic1DWeakPotentialGapObservation),
        )
        if any(
            not isinstance(channel, tuple)
            or not channel
            or any(type(item) is not kind for item in channel)
            for channel, kind in typed_channels
        ):
            raise TypeError("every verification channel must be a nonempty typed tuple")
        if (
            not isinstance(self.mathieu_zone_boundary_lowest_two, tuple)
            or len(self.mathieu_zone_boundary_lowest_two) != 2
        ):
            raise TypeError("Mathieu zone-boundary values must be a pair")
        scalar_values = (
            self.mathieu_zone_center_lowest,
            *self.mathieu_zone_boundary_lowest_two,
            self.mathieu_plane_wave_zone_center_absolute_error,
            self.mathieu_plane_wave_zone_boundary_maximum_absolute_error,
            self.inversion_maximum_absolute_energy,
            self.potential_sign_translation_maximum_absolute_energy,
        )
        if any(
            type(value) is not float or not np.isfinite(value)
            for value in scalar_values
        ):
            raise ValueError(
                "parent verification scalars must be finite built-in floats"
            )
        if type(self.mathieu_q_convention) is not str or not self.mathieu_q_convention:
            raise ValueError("mathieu_q_convention must be a nonempty built-in str")


@dataclass(frozen=True, slots=True)
class Periodic1DHoppingRangeDiagnostic:
    """Retain one finite-range scalar hopping approximation outcome."""

    hopping_range_cells: int
    retained_coefficient_count: int
    omitted_hopping_l2_norm: float
    training_maximum_absolute_error: float
    training_root_mean_square_error: float
    withheld_maximum_absolute_error: float
    withheld_root_mean_square_error: float
    bandwidth_error: float
    zone_center_curvature: float
    direct_mediated_coefficient_l2_defect: float
    direct_mediated_training_l2_defect: float
    parseval_absolute_residual: float

    def __post_init__(self) -> None:
        """Require nonnegative dimensions and finite dimensionless diagnostics."""
        if type(self.hopping_range_cells) is not int or self.hopping_range_cells < 0:
            raise ValueError("hopping_range_cells must be a nonnegative built-in int")
        if (
            type(self.retained_coefficient_count) is not int
            or self.retained_coefficient_count <= 0
        ):
            raise ValueError(
                "retained_coefficient_count must be a positive built-in int"
            )
        values = (
            self.omitted_hopping_l2_norm,
            self.training_maximum_absolute_error,
            self.training_root_mean_square_error,
            self.withheld_maximum_absolute_error,
            self.withheld_root_mean_square_error,
            self.bandwidth_error,
            self.zone_center_curvature,
            self.direct_mediated_coefficient_l2_defect,
            self.direct_mediated_training_l2_defect,
            self.parseval_absolute_residual,
        )
        if any(type(value) is not float or not np.isfinite(value) for value in values):
            raise ValueError("hopping diagnostics must be finite built-in floats")
        nonnegative_values = (
            self.omitted_hopping_l2_norm,
            self.training_maximum_absolute_error,
            self.training_root_mean_square_error,
            self.withheld_maximum_absolute_error,
            self.withheld_root_mean_square_error,
            self.bandwidth_error,
            self.direct_mediated_coefficient_l2_defect,
            self.direct_mediated_training_l2_defect,
            self.parseval_absolute_residual,
        )
        if any(value < 0.0 for value in nonnegative_values):
            raise ValueError("hopping errors and defects must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DParentBandObservables:
    """Retain dimensionless bandwidth, gap, and curvature observables."""

    bandwidth: float
    zone_boundary_gap: float
    zone_center_curvature: float

    def __post_init__(self) -> None:
        """Require finite values and nonnegative bandwidth and gap."""
        if any(
            type(value) is not float or not np.isfinite(value)
            for value in (
                self.bandwidth,
                self.zone_boundary_gap,
                self.zone_center_curvature,
            )
        ):
            raise ValueError("parent observables must be finite built-in floats")
        if self.bandwidth < 0.0 or self.zone_boundary_gap < 0.0:
            raise ValueError("bandwidth and zone-boundary gap must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DRetainedLocalizationResult:
    """Retain localization moments and the authenticated density identity."""

    quadrature_norm: float
    center_over_period: float
    spread_over_period_squared: float
    profile_sample_count: int
    profile_definition: str
    profile_density_content_encoding: str
    profile_density_content_sha256: str

    def __post_init__(self) -> None:
        """Validate finite moments, sample count, and SHA-256 identity syntax."""
        for moment_name, moment_value in (
            ("quadrature_norm", self.quadrature_norm),
            ("center_over_period", self.center_over_period),
            ("spread_over_period_squared", self.spread_over_period_squared),
        ):
            if type(moment_value) is not float or not np.isfinite(moment_value):
                raise ValueError(f"{moment_name} must be a finite built-in float")
        if self.quadrature_norm <= 0.0 or self.spread_over_period_squared < 0.0:
            raise ValueError(
                "localization norm must be positive and spread nonnegative"
            )
        if type(self.profile_sample_count) is not int or self.profile_sample_count <= 0:
            raise ValueError("profile_sample_count must be a positive built-in int")
        for text_name, text_value in (
            ("profile_definition", self.profile_definition),
            ("profile_density_content_encoding", self.profile_density_content_encoding),
        ):
            if type(text_value) is not str or not text_value:
                raise ValueError(f"{text_name} must be a nonempty built-in str")
        if (
            type(self.profile_density_content_sha256) is not str
            or len(self.profile_density_content_sha256) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.profile_density_content_sha256
            )
        ):
            raise ValueError("profile density identity must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandReductionResult:
    """Retain the typed complete isolated-band and scalar hopping reduction."""

    reciprocal_samples: ReciprocalOperatorSamples1D
    hopping_model: BlockHoppingModel1D
    hopping_range_study: tuple[Periodic1DHoppingRangeDiagnostic, ...]
    parent_observables: Periodic1DParentBandObservables
    localization: Periodic1DRetainedLocalizationResult
    closure_holonomy_phase: float
    neighbor_overlap_minimum_magnitude: float
    neighbor_overlap_maximum_magnitude: float
    full_mesh_reconstruction_maximum_absolute_error: float
    full_mesh_reconstruction_maximum_imaginary: float
    hopping_maximum_imaginary: float

    def __post_init__(self) -> None:
        """Validate typed models, channel size, and finite scalar diagnostics."""
        if type(self.reciprocal_samples) is not ReciprocalOperatorSamples1D:
            raise TypeError("reciprocal_samples must be ReciprocalOperatorSamples1D")
        if self.reciprocal_samples.matrix_dimension != 1:
            raise ValueError("isolated-band reciprocal samples must be scalar")
        if type(self.hopping_model) is not BlockHoppingModel1D:
            raise TypeError("hopping_model must be BlockHoppingModel1D")
        if self.hopping_model.matrix_dimension != 1:
            raise ValueError("isolated-band hopping model must be scalar")
        if (
            not isinstance(self.hopping_range_study, tuple)
            or not self.hopping_range_study
        ):
            raise TypeError("hopping_range_study must be a nonempty tuple")
        if any(
            type(item) is not Periodic1DHoppingRangeDiagnostic
            for item in self.hopping_range_study
        ):
            raise TypeError("every hopping range outcome must use the typed record")
        if type(self.parent_observables) is not Periodic1DParentBandObservables:
            raise TypeError(
                "parent_observables must be Periodic1DParentBandObservables"
            )
        if type(self.localization) is not Periodic1DRetainedLocalizationResult:
            raise TypeError("localization must be Periodic1DRetainedLocalizationResult")
        values = (
            self.closure_holonomy_phase,
            self.neighbor_overlap_minimum_magnitude,
            self.neighbor_overlap_maximum_magnitude,
            self.full_mesh_reconstruction_maximum_absolute_error,
            self.full_mesh_reconstruction_maximum_imaginary,
            self.hopping_maximum_imaginary,
        )
        if any(type(value) is not float or not np.isfinite(value) for value in values):
            raise ValueError("isolated-band diagnostics must be finite built-in floats")
        if (
            self.neighbor_overlap_minimum_magnitude
            > self.neighbor_overlap_maximum_magnitude
        ):
            raise ValueError("neighbor-overlap extrema must be ordered")


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaignResult:
    """Retain typed isolated-band outcomes and their complete source document."""

    source_document: Periodic1DRetainedResultDocument
    parent_verification: Periodic1DParentRepresentationVerificationResult
    reduction: Periodic1DIsolatedBandReductionResult

    def __post_init__(self) -> None:
        """Validate exact result types and isolated-band source kind."""
        if type(self.source_document) is not Periodic1DRetainedResultDocument:
            raise TypeError("source_document must be Periodic1DRetainedResultDocument")
        if self.source_document.kind is not Periodic1DRetainedResultKind.ISOLATED_BAND:
            raise ValueError("source_document must be an isolated-band result")
        if (
            type(self.parent_verification)
            is not Periodic1DParentRepresentationVerificationResult
        ):
            raise TypeError("parent_verification uses the wrong result type")
        if type(self.reduction) is not Periodic1DIsolatedBandReductionResult:
            raise TypeError("reduction uses the wrong result type")


class Periodic1DIsolatedBandResultJsonSerializer(
    JsonCodec[Periodic1DIsolatedBandCampaignResult, bytes]
):
    """Adapt retained isolated-band result bytes to typed domain results."""

    __slots__ = ()

    retained = Periodic1DRetainedResultJsonSerializer(
        Periodic1DRetainedResultKind.ISOLATED_BAND
    )

    def deserialize(self, payload: bytes) -> Periodic1DIsolatedBandCampaignResult:
        """Decode complete retained bytes and extract typed scientific outcomes."""
        document = self.retained.deserialize(payload)
        parent = self.retained.object(
            document.root.field("parent_representation_verification"),
            "parent_representation_verification",
        )
        reduction = self.retained.object(
            document.root.field("isolated_band_reduction"), "isolated_band_reduction"
        )
        convention = self.retained.object(
            document.root.field("dimensionless_convention"), "dimensionless_convention"
        )
        reciprocal_period = ScalarQuantity(
            self.retained.real_field(convention, "reciprocal_vector"), Unitless()
        )
        coordinates = self.retained.real_vector_field(reduction, "reciprocal_mesh")
        energies = self.retained.real_vector_field(reduction, "lowest_band_energies")
        reciprocal_samples = ReciprocalOperatorSamples1D(
            VectorQuantity(coordinates, Unitless()),
            reciprocal_period,
            tuple(
                ComplexMatrixQuantity(
                    np.asarray([[energy]], dtype=np.complex128), Unitless()
                )
                for energy in energies
            ),
        )
        representatives = self.retained.integer_tuple_field(
            reduction, "hopping_representatives_cells"
        )
        coefficients = self.retained.complex_vector_field(
            reduction, "hopping_coefficients"
        )
        hopping_model = BlockHoppingModel1D(
            reciprocal_period,
            representatives,
            tuple(
                ComplexMatrixQuantity(
                    np.asarray([[coefficient]], dtype=np.complex128), Unitless()
                )
                for coefficient in coefficients
            ),
        )
        return Periodic1DIsolatedBandCampaignResult(
            document,
            self.decode_parent_verification(parent),
            self.decode_reduction(reduction, reciprocal_samples, hopping_model),
        )

    def serialize(self, value: Periodic1DIsolatedBandCampaignResult) -> bytes:
        """Encode the complete correlated source document canonically."""
        if type(value) is not Periodic1DIsolatedBandCampaignResult:
            raise TypeError("value must be Periodic1DIsolatedBandCampaignResult")
        return self.retained.serialize(value.source_document)

    def decode(self, payload: bytes) -> Periodic1DIsolatedBandCampaignResult:
        """Deprecated compatibility alias for :meth:`deserialize`."""
        warnings.warn(
            "decode() is deprecated; use deserialize()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.deserialize(payload)

    def encode(self, value: Periodic1DIsolatedBandCampaignResult) -> bytes:
        """Deprecated compatibility alias for :meth:`serialize`."""
        warnings.warn(
            "encode() is deprecated; use serialize()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.serialize(value)

    def decode_parent_verification(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DParentRepresentationVerificationResult:
        """Extract all typed parent-representation verification channels."""
        mathieu = self.retained.object_field(value, "mathieu_references")
        symmetry = self.retained.object_field(value, "symmetry_residuals")
        boundary = self.retained.real_vector_field(mathieu, "zone_boundary_lowest_two")
        if boundary.shape != (2,):
            raise ValueError("Mathieu zone-boundary values must contain two entries")
        return Periodic1DParentRepresentationVerificationResult(
            tuple(
                self.decode_plane_wave_observation(item)
                for item in self.retained.object_array_field(
                    value, "plane_wave_cutoff_study"
                )
            ),
            tuple(
                self.decode_finite_difference_observation(item)
                for item in self.retained.object_array_field(
                    value, "finite_difference_grid_study"
                )
            ),
            tuple(
                self.decode_low_mode_observation(item)
                for item in self.retained.object_array_field(
                    value, "common_low_mode_operator_study"
                )
            ),
            tuple(
                self.decode_weak_gap_observation(item)
                for item in self.retained.object_array_field(
                    value, "weak_potential_gap_study"
                )
            ),
            self.retained.real_field(mathieu, "zone_center_lowest"),
            (float(boundary[0]), float(boundary[1])),
            self.retained.real_field(mathieu, "plane_wave_zone_center_absolute_error"),
            self.retained.real_field(
                mathieu, "plane_wave_zone_boundary_maximum_absolute_error"
            ),
            self.retained.string_field(mathieu, "q_convention"),
            self.retained.real_field(symmetry, "inversion_maximum_absolute_energy"),
            self.retained.real_field(
                symmetry, "potential_sign_translation_maximum_absolute_energy"
            ),
        )

    def decode_reduction(
        self,
        value: Periodic1DJsonObject,
        samples: ReciprocalOperatorSamples1D,
        hopping_model: BlockHoppingModel1D,
    ) -> Periodic1DIsolatedBandReductionResult:
        """Extract typed isolated-band reduction outcomes."""
        observables = self.retained.object_field(value, "parent_observables")
        localization = self.retained.object_field(value, "wannier_localization")
        return Periodic1DIsolatedBandReductionResult(
            samples,
            hopping_model,
            tuple(
                self.decode_hopping_range_diagnostic(item)
                for item in self.retained.object_array_field(
                    value, "hopping_range_study"
                )
            ),
            Periodic1DParentBandObservables(
                self.retained.real_field(observables, "bandwidth"),
                self.retained.real_field(observables, "zone_boundary_gap"),
                self.retained.real_field(observables, "zone_center_curvature"),
            ),
            self.decode_localization(localization),
            self.retained.real_field(value, "closure_holonomy_phase"),
            self.retained.real_field(value, "neighbor_overlap_minimum_magnitude"),
            self.retained.real_field(value, "neighbor_overlap_maximum_magnitude"),
            self.retained.real_field(
                value, "full_mesh_reconstruction_maximum_absolute_error"
            ),
            self.retained.real_field(
                value, "full_mesh_reconstruction_maximum_imaginary"
            ),
            self.retained.real_field(value, "hopping_maximum_imaginary"),
        )

    def decode_plane_wave_observation(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DPlaneWaveCutoffObservation:
        """Decode one plane-wave cutoff observation."""
        return Periodic1DPlaneWaveCutoffObservation(
            self.retained.integer_field(value, "cutoff"),
            self.retained.real_field(value, "maximum_first_bands_absolute_error"),
        )

    def decode_finite_difference_observation(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DFiniteDifferenceGridObservation:
        """Decode one finite-difference grid observation."""
        return Periodic1DFiniteDifferenceGridObservation(
            self.retained.integer_field(value, "interior_cell_points"),
            self.retained.real_field(value, "grid_spacing_over_period"),
            self.retained.real_field(value, "maximum_first_bands_absolute_error"),
        )

    def decode_low_mode_observation(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DLowModeOperatorObservation:
        """Decode one common-low-mode operator observation."""
        return Periodic1DLowModeOperatorObservation(
            self.retained.integer_field(value, "interior_cell_points"),
            self.retained.integer_field(value, "low_mode_cutoff"),
            self.retained.real_field(
                value, "maximum_low_mode_operator_frobenius_error"
            ),
        )

    def decode_weak_gap_observation(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DWeakPotentialGapObservation:
        """Decode one weak-potential gap observation."""
        return Periodic1DWeakPotentialGapObservation(
            self.retained.real_field(value, "potential_strength"),
            self.retained.real_field(value, "zone_boundary_gap"),
            self.retained.real_field(value, "leading_perturbative_gap"),
            self.retained.real_field(value, "relative_deviation_from_leading_gap"),
        )

    def decode_hopping_range_diagnostic(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DHoppingRangeDiagnostic:
        """Decode one finite-range hopping diagnostic."""
        return Periodic1DHoppingRangeDiagnostic(
            self.retained.integer_field(value, "hopping_range_cells"),
            self.retained.integer_field(value, "retained_coefficient_count"),
            self.retained.real_field(value, "omitted_hopping_l2_norm"),
            self.retained.real_field(value, "training_maximum_absolute_error"),
            self.retained.real_field(value, "training_root_mean_square_error"),
            self.retained.real_field(value, "withheld_maximum_absolute_error"),
            self.retained.real_field(value, "withheld_root_mean_square_error"),
            self.retained.real_field(value, "bandwidth_error"),
            self.retained.real_field(value, "zone_center_curvature"),
            self.retained.real_field(value, "direct_mediated_coefficient_l2_defect"),
            self.retained.real_field(value, "direct_mediated_training_l2_defect"),
            self.retained.real_field(value, "parseval_absolute_residual"),
        )

    def decode_localization(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DRetainedLocalizationResult:
        """Decode one retained localization summary and density identity."""
        return Periodic1DRetainedLocalizationResult(
            self.retained.real_field(value, "quadrature_norm"),
            self.retained.real_field(value, "center_over_period"),
            self.retained.real_field(value, "spread_over_period_squared"),
            self.retained.integer_field(value, "profile_sample_count"),
            self.retained.string_field(value, "profile_definition"),
            self.retained.string_field(value, "profile_density_content_encoding"),
            self.retained.string_field(value, "profile_density_content_sha256"),
        )
