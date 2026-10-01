"""Typed retained outcomes for the Appendix G periodic-1D stress campaign."""

from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np

from ksdft2effmass.serialization import JsonCodec

from .result_documents import (
    Periodic1DJsonObject,
    Periodic1DRetainedResultDocument,
    Periodic1DRetainedResultJsonSerializer,
    Periodic1DRetainedResultKind,
)


@dataclass(frozen=True, slots=True)
class Periodic1DStressDiscretizationObservation:
    """Retain one plane-wave or finite-difference stress error observation."""

    resolution: int
    maximum_low_band_error: float

    def __post_init__(self) -> None:
        """Require positive resolution and finite nonnegative error."""
        if type(self.resolution) is not int or self.resolution <= 0:
            raise ValueError("resolution must be a positive built-in int")
        if (
            type(self.maximum_low_band_error) is not float
            or not np.isfinite(self.maximum_low_band_error)
            or self.maximum_low_band_error < 0.0
        ):
            raise ValueError("maximum_low_band_error must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DPotentialAmplitudeStressResult:
    """Retain one potential-amplitude stress outcome and convergence channels."""

    potential_strength: float
    zone_boundary_gap: float
    isolated_band_status: str
    potential_sign_invariance_maximum_error: float
    plane_wave_cutoff_study: tuple[Periodic1DStressDiscretizationObservation, ...]
    finite_difference_grid_study: tuple[Periodic1DStressDiscretizationObservation, ...]

    def __post_init__(self) -> None:
        """Validate finite scalars, status, and nonempty typed studies."""
        values = (
            self.potential_strength,
            self.zone_boundary_gap,
            self.potential_sign_invariance_maximum_error,
        )
        if any(
            type(value) is not float or not np.isfinite(value) or value < 0.0
            for value in values
        ):
            raise ValueError("amplitude stress scalars must be finite and nonnegative")
        if type(self.isolated_band_status) is not str or not self.isolated_band_status:
            raise ValueError("isolated_band_status must be a nonempty built-in str")
        for study in (self.plane_wave_cutoff_study, self.finite_difference_grid_study):
            if (
                not isinstance(study, tuple)
                or not study
                or any(
                    type(item) is not Periodic1DStressDiscretizationObservation
                    for item in study
                )
            ):
                raise TypeError("discretization studies must be nonempty typed tuples")


@dataclass(frozen=True, slots=True)
class Periodic1DMeshBandIsolationStressResult:
    """Retain one mesh, band, amplitude, and isolation stress outcome."""

    potential_strength: float
    mesh_size: int
    band_index: int
    isolation_applicable: bool
    minimum_adjacent_gap: float
    minimum_sewn_neighbor_overlap: float
    full_reconstruction_maximum_error: float
    fixed_range_withheld_maximum_error: float

    def __post_init__(self) -> None:
        """Validate exact discrete controls and finite nonnegative diagnostics."""
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        if type(self.band_index) is not int or self.band_index < 0:
            raise ValueError("band_index must be a nonnegative built-in int")
        if type(self.isolation_applicable) is not bool:
            raise TypeError("isolation_applicable must be a built-in bool")
        values = (
            self.potential_strength,
            self.minimum_adjacent_gap,
            self.minimum_sewn_neighbor_overlap,
            self.full_reconstruction_maximum_error,
            self.fixed_range_withheld_maximum_error,
        )
        if any(
            type(value) is not float or not np.isfinite(value) or value < 0.0
            for value in values
        ):
            raise ValueError("mesh stress diagnostics must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DPotentialShapeStressCase:
    """Retain one named Fourier-potential shape stress outcome."""

    identifier: str
    finest_grid_maximum_band_error: float
    minimum_adjacent_gaps: tuple[float, ...]
    time_reversal_energy_residual: float

    def __post_init__(self) -> None:
        """Validate identity, gap inventory, and residuals."""
        if type(self.identifier) is not str or not self.identifier:
            raise ValueError("identifier must be a nonempty built-in str")
        if (
            not isinstance(self.minimum_adjacent_gaps, tuple)
            or not self.minimum_adjacent_gaps
        ):
            raise TypeError("minimum_adjacent_gaps must be a nonempty tuple")
        values = (
            self.finest_grid_maximum_band_error,
            *self.minimum_adjacent_gaps,
            self.time_reversal_energy_residual,
        )
        if any(
            type(value) is not float or not np.isfinite(value) or value < 0.0
            for value in values
        ):
            raise ValueError("shape stress diagnostics must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DPotentialShapeStressResult:
    """Retain shape cases and translation/constant-shift covariance defects."""

    cases: tuple[Periodic1DPotentialShapeStressCase, ...]
    constant_shift_covariance_maximum_error: float
    translation_isospectral_maximum_error: float

    def __post_init__(self) -> None:
        """Validate typed unique cases and finite covariance defects."""
        if (
            not isinstance(self.cases, tuple)
            or not self.cases
            or any(
                type(case) is not Periodic1DPotentialShapeStressCase
                for case in self.cases
            )
        ):
            raise TypeError("cases must be a nonempty typed tuple")
        identifiers = tuple(case.identifier for case in self.cases)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("shape identifiers must be unique")
        values = (
            self.constant_shift_covariance_maximum_error,
            self.translation_isospectral_maximum_error,
        )
        if any(
            type(value) is not float or not np.isfinite(value) or value < 0.0
            for value in values
        ):
            raise ValueError("shape covariance defects must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DGaugeCovarianceStressResult:
    """Retain random-gauge, transport, and closure covariance diagnostics."""

    potential_strength: float
    mesh_size: int
    random_phase_projector_maximum_frobenius_defect: float
    parallel_transport_frame_maximum_aligned_defect: float
    closure_holonomy_difference_modulo_2pi: float

    def __post_init__(self) -> None:
        """Validate mesh and finite nonnegative covariance defects."""
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        values = (
            self.potential_strength,
            self.random_phase_projector_maximum_frobenius_defect,
            self.parallel_transport_frame_maximum_aligned_defect,
            self.closure_holonomy_difference_modulo_2pi,
        )
        if any(
            type(value) is not float or not np.isfinite(value) or value < 0.0
            for value in values
        ):
            raise ValueError("gauge stress diagnostics must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DRouteAssumptionStressResult:
    """Retain complete, incomplete, and nonuniform fitting-route defects."""

    potential_strength: float
    mesh_size: int
    hopping_range_cells: int
    uniform_complete_coefficient_defect: float
    incomplete_training_coefficient_defect: float
    incomplete_training_comparison_l2_defect: float
    nonuniform_weight_coefficient_defect: float
    nonuniform_weight_comparison_l2_defect: float

    def __post_init__(self) -> None:
        """Validate route controls and finite nonnegative defects."""
        if type(self.mesh_size) is not int or self.mesh_size <= 0:
            raise ValueError("mesh_size must be a positive built-in int")
        if type(self.hopping_range_cells) is not int or self.hopping_range_cells < 0:
            raise ValueError("hopping_range_cells must be nonnegative")
        values = (
            self.potential_strength,
            self.uniform_complete_coefficient_defect,
            self.incomplete_training_coefficient_defect,
            self.incomplete_training_comparison_l2_defect,
            self.nonuniform_weight_coefficient_defect,
            self.nonuniform_weight_comparison_l2_defect,
        )
        if any(
            type(value) is not float or not np.isfinite(value) or value < 0.0
            for value in values
        ):
            raise ValueError("route stress diagnostics must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaignResult:
    """Retain all typed stress channels and the complete source document."""

    source_document: Periodic1DRetainedResultDocument
    potential_amplitude_stress: tuple[Periodic1DPotentialAmplitudeStressResult, ...]
    mesh_band_and_isolation_stress: tuple[Periodic1DMeshBandIsolationStressResult, ...]
    potential_shape_stress: Periodic1DPotentialShapeStressResult
    gauge_covariance_stress: Periodic1DGaugeCovarianceStressResult
    route_assumption_stress: Periodic1DRouteAssumptionStressResult

    def __post_init__(self) -> None:
        """Validate the stress source kind and exact typed channel ownership."""
        if type(self.source_document) is not Periodic1DRetainedResultDocument:
            raise TypeError("source_document must be Periodic1DRetainedResultDocument")
        if self.source_document.kind is not Periodic1DRetainedResultKind.STRESS:
            raise ValueError("source_document must be a stress result")
        if (
            not isinstance(self.potential_amplitude_stress, tuple)
            or not self.potential_amplitude_stress
        ):
            raise TypeError("potential_amplitude_stress must be a nonempty tuple")
        if any(
            type(item) is not Periodic1DPotentialAmplitudeStressResult
            for item in self.potential_amplitude_stress
        ):
            raise TypeError("potential amplitude outcomes use the wrong type")
        if (
            not isinstance(self.mesh_band_and_isolation_stress, tuple)
            or not self.mesh_band_and_isolation_stress
        ):
            raise TypeError("mesh_band_and_isolation_stress must be a nonempty tuple")
        if any(
            type(item) is not Periodic1DMeshBandIsolationStressResult
            for item in self.mesh_band_and_isolation_stress
        ):
            raise TypeError("mesh/band outcomes use the wrong type")
        if (
            type(self.potential_shape_stress)
            is not Periodic1DPotentialShapeStressResult
        ):
            raise TypeError("potential_shape_stress uses the wrong type")
        if (
            type(self.gauge_covariance_stress)
            is not Periodic1DGaugeCovarianceStressResult
        ):
            raise TypeError("gauge_covariance_stress uses the wrong type")
        if (
            type(self.route_assumption_stress)
            is not Periodic1DRouteAssumptionStressResult
        ):
            raise TypeError("route_assumption_stress uses the wrong type")


class Periodic1DStressResultJsonSerializer(
    JsonCodec[Periodic1DStressCampaignResult, bytes]
):
    """Adapt retained stress-result bytes to typed channel ResultObjects."""

    __slots__ = ()

    retained = Periodic1DRetainedResultJsonSerializer(
        Periodic1DRetainedResultKind.STRESS
    )

    def deserialize(self, payload: bytes) -> Periodic1DStressCampaignResult:
        """Decode complete retained bytes and extract every typed stress channel."""
        document = self.retained.deserialize(payload)
        root = document.root
        return Periodic1DStressCampaignResult(
            document,
            tuple(
                self.deserialize_amplitude(item)
                for item in self.retained.object_array_field(
                    root, "potential_amplitude_stress"
                )
            ),
            tuple(
                self.deserialize_mesh_band(item)
                for item in self.retained.object_array_field(
                    root, "mesh_band_and_isolation_stress"
                )
            ),
            self.deserialize_shape_stress(
                self.retained.object_field(root, "potential_shape_stress")
            ),
            self.deserialize_gauge_stress(
                self.retained.object_field(root, "gauge_covariance_stress")
            ),
            self.deserialize_route_stress(
                self.retained.object_field(root, "route_assumption_stress")
            ),
        )

    def serialize(self, value: Periodic1DStressCampaignResult) -> bytes:
        """Encode the complete correlated source document canonically."""
        if type(value) is not Periodic1DStressCampaignResult:
            raise TypeError("value must be Periodic1DStressCampaignResult")
        return self.retained.serialize(value.source_document)

    def decode(self, payload: bytes) -> Periodic1DStressCampaignResult:
        """Deprecated compatibility alias for :meth:`deserialize`."""
        warnings.warn(
            "decode() is deprecated; use deserialize()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.deserialize(payload)

    def encode(self, value: Periodic1DStressCampaignResult) -> bytes:
        """Deprecated compatibility alias for :meth:`serialize`."""
        warnings.warn(
            "encode() is deprecated; use serialize()", DeprecationWarning, stacklevel=2
        )
        return self.serialize(value)

    def deserialize_amplitude(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DPotentialAmplitudeStressResult:
        """Decode one amplitude-stress record."""
        return Periodic1DPotentialAmplitudeStressResult(
            self.retained.real_field(value, "potential_strength"),
            self.retained.real_field(value, "zone_boundary_gap"),
            self.retained.string_field(value, "isolated_band_status"),
            self.retained.real_field(value, "potential_sign_invariance_maximum_error"),
            tuple(
                self.deserialize_discretization(item, "cutoff")
                for item in self.retained.object_array_field(
                    value, "plane_wave_cutoff_study"
                )
            ),
            tuple(
                self.deserialize_discretization(item, "points")
                for item in self.retained.object_array_field(
                    value, "finite_difference_grid_study"
                )
            ),
        )

    def deserialize_discretization(
        self, value: Periodic1DJsonObject, resolution_field: str
    ) -> Periodic1DStressDiscretizationObservation:
        """Decode one plane-wave or finite-difference stress observation."""
        return Periodic1DStressDiscretizationObservation(
            self.retained.integer_field(value, resolution_field),
            self.retained.real_field(value, "maximum_low_band_error"),
        )

    def deserialize_mesh_band(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DMeshBandIsolationStressResult:
        """Decode one mesh/band/isolation stress record."""
        return Periodic1DMeshBandIsolationStressResult(
            self.retained.real_field(value, "potential_strength"),
            self.retained.integer_field(value, "mesh_size"),
            self.retained.integer_field(value, "band_index"),
            self.retained.boolean_field(value, "isolation_applicable"),
            self.retained.real_field(value, "minimum_adjacent_gap"),
            self.retained.real_field(value, "minimum_sewn_neighbor_overlap"),
            self.retained.real_field(value, "full_reconstruction_maximum_error"),
            self.retained.real_field(value, "fixed_range_withheld_maximum_error"),
        )

    def deserialize_shape_stress(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DPotentialShapeStressResult:
        """Decode all named potential-shape stress records."""
        return Periodic1DPotentialShapeStressResult(
            tuple(
                self.deserialize_shape_case(item)
                for item in self.retained.object_array_field(value, "cases")
            ),
            self.retained.real_field(value, "constant_shift_covariance_maximum_error"),
            self.retained.real_field(value, "translation_isospectral_maximum_error"),
        )

    def deserialize_shape_case(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DPotentialShapeStressCase:
        """Decode one named potential-shape stress case."""
        gaps = self.retained.real_vector_field(value, "minimum_adjacent_gaps")
        return Periodic1DPotentialShapeStressCase(
            self.retained.string_field(value, "id"),
            self.retained.real_field(value, "finest_grid_maximum_band_error"),
            tuple(float(item) for item in gaps),
            self.retained.real_field(value, "time_reversal_energy_residual"),
        )

    def deserialize_gauge_stress(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DGaugeCovarianceStressResult:
        """Decode gauge covariance stress diagnostics."""
        return Periodic1DGaugeCovarianceStressResult(
            self.retained.real_field(value, "potential_strength"),
            self.retained.integer_field(value, "mesh_size"),
            self.retained.real_field(
                value, "random_phase_projector_maximum_frobenius_defect"
            ),
            self.retained.real_field(
                value, "parallel_transport_frame_maximum_aligned_defect"
            ),
            self.retained.real_field(value, "closure_holonomy_difference_modulo_2pi"),
        )

    def deserialize_route_stress(
        self, value: Periodic1DJsonObject
    ) -> Periodic1DRouteAssumptionStressResult:
        """Decode complete, incomplete, and nonuniform fitting-route diagnostics."""
        return Periodic1DRouteAssumptionStressResult(
            self.retained.real_field(value, "potential_strength"),
            self.retained.integer_field(value, "mesh_size"),
            self.retained.integer_field(value, "hopping_range_cells"),
            self.retained.real_field(value, "uniform_complete_coefficient_defect"),
            self.retained.real_field(value, "incomplete_training_coefficient_defect"),
            self.retained.real_field(value, "incomplete_training_comparison_l2_defect"),
            self.retained.real_field(value, "nonuniform_weight_coefficient_defect"),
            self.retained.real_field(value, "nonuniform_weight_comparison_l2_defect"),
        )
