"""Typed results for the prospective isolated-band calculation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityResult1D,
    HoppingParsevalResult1D,
    ScalarHoppingBandShapeResult1D,
)
from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitResult1D,
    BlockHoppingModelComparisonResult1D,
)
from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorResult1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.operators import ScalarQuantity
from ksdft2effmass.solid_state import (
    BlockHoppingTruncationResult1D,
    ReciprocalOperatorFourierTransformResult1D,
)

from .definition import Periodic1DIsolatedBandCalculationDefinition


@dataclass(frozen=True, slots=True)
class Periodic1DPlaneWaveConvergenceObservation:
    """Retain one cutoff and its maximum error against the declared reference."""

    cutoff: int
    maximum_absolute_error: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate the cutoff and nonnegative energy error."""
        if type(self.cutoff) is not int:
            raise TypeError("cutoff must be a built-in int")
        if self.cutoff <= 0:
            raise ValueError("cutoff must be positive")
        if type(self.maximum_absolute_error) is not ScalarQuantity:
            raise TypeError("maximum_absolute_error must be ScalarQuantity")
        if self.maximum_absolute_error.magnitude < 0.0:
            raise ValueError("maximum_absolute_error must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DFiniteDifferenceConvergenceObservation:
    """Retain one grid extent and its maximum error against the same parent."""

    point_count: int
    maximum_absolute_error: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate the grid extent and nonnegative energy error."""
        if type(self.point_count) is not int:
            raise TypeError("point_count must be a built-in int")
        if self.point_count < 3:
            raise ValueError("point_count must be at least three")
        if type(self.maximum_absolute_error) is not ScalarQuantity:
            raise TypeError("maximum_absolute_error must be ScalarQuantity")
        if self.maximum_absolute_error.magnitude < 0.0:
            raise ValueError("maximum_absolute_error must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandRangeResult:
    """Retain diagnostics for one prospectively declared hopping range."""

    truncation: BlockHoppingTruncationResult1D
    training_error: BandApproximationErrorResult1D
    withheld_error: BandApproximationErrorResult1D
    parseval: HoppingParsevalResult1D
    direct_fit: BlockHoppingLeastSquaresFitResult1D
    direct_mediated_comparison: BlockHoppingModelComparisonResult1D
    band_shape: ScalarHoppingBandShapeResult1D

    def __post_init__(self) -> None:
        """Require exact diagnostic types and one common finite-range model."""
        if type(self.truncation) is not BlockHoppingTruncationResult1D:
            raise TypeError("truncation must be BlockHoppingTruncationResult1D")
        if type(self.training_error) is not BandApproximationErrorResult1D:
            raise TypeError("training_error must be BandApproximationErrorResult1D")
        if type(self.withheld_error) is not BandApproximationErrorResult1D:
            raise TypeError("withheld_error must be BandApproximationErrorResult1D")
        if type(self.parseval) is not HoppingParsevalResult1D:
            raise TypeError("parseval must be HoppingParsevalResult1D")
        if type(self.direct_fit) is not BlockHoppingLeastSquaresFitResult1D:
            raise TypeError("direct_fit must be BlockHoppingLeastSquaresFitResult1D")
        if (
            type(self.direct_mediated_comparison)
            is not BlockHoppingModelComparisonResult1D
        ):
            raise TypeError(
                "direct_mediated_comparison must be BlockHoppingModelComparisonResult1D"
            )
        if type(self.band_shape) is not ScalarHoppingBandShapeResult1D:
            raise TypeError("band_shape must be ScalarHoppingBandShapeResult1D")
        mediated = self.truncation.truncated
        if self.direct_mediated_comparison.reference is not mediated:
            raise ValueError(
                "route comparison must use the truncated model as reference"
            )
        if self.band_shape.model is not mediated:
            raise ValueError("band-shape diagnostics must use the truncated model")
        if self.parseval.truncation is not self.truncation:
            raise ValueError("Parseval diagnostics must use the same truncation")
        if self.direct_fit.representatives != mediated.representatives:
            raise ValueError("direct fit must use the truncated representatives")
        if (
            self.direct_mediated_comparison.candidate
            is not self.direct_fit.fitted_model
        ):
            raise ValueError("route comparison must use the direct-fit model")

    @property
    def maximum_range(self) -> int:
        """Return the represented cell range of this result."""
        return self.truncation.maximum_range


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCalculationResult:
    """Retain M1 software/numerical channels without localization claims."""

    definition: Periodic1DIsolatedBandCalculationDefinition
    parent_reference: BandSpectrumSamples1D
    plane_wave_convergence: tuple[Periodic1DPlaneWaveConvergenceObservation, ...]
    finite_difference_convergence: tuple[
        Periodic1DFiniteDifferenceConvergenceObservation, ...
    ]
    training_target: BandSpectrumSamples1D
    withheld_target: BandSpectrumSamples1D
    complete_transform: ReciprocalOperatorFourierTransformResult1D
    hopping_hermiticity: BlockHoppingHermiticityResult1D
    range_study: tuple[Periodic1DIsolatedBandRangeResult, ...]

    def __post_init__(self) -> None:
        """Validate typed channels, declared inventories, and sample-role separation."""
        if type(self.definition) is not Periodic1DIsolatedBandCalculationDefinition:
            raise TypeError(
                "definition must be Periodic1DIsolatedBandCalculationDefinition"
            )
        if type(self.parent_reference) is not BandSpectrumSamples1D:
            raise TypeError("parent_reference must be BandSpectrumSamples1D")
        if not isinstance(self.plane_wave_convergence, tuple) or any(
            type(item) is not Periodic1DPlaneWaveConvergenceObservation
            for item in self.plane_wave_convergence
        ):
            raise TypeError("plane_wave_convergence must be a typed tuple")
        if not isinstance(self.finite_difference_convergence, tuple) or any(
            type(item) is not Periodic1DFiniteDifferenceConvergenceObservation
            for item in self.finite_difference_convergence
        ):
            raise TypeError("finite_difference_convergence must be a typed tuple")
        if tuple(item.cutoff for item in self.plane_wave_convergence) != (
            self.definition.plane_wave_cutoffs
        ):
            raise ValueError("plane-wave observations must match declared cutoffs")
        if tuple(item.point_count for item in self.finite_difference_convergence) != (
            self.definition.finite_difference_points
        ):
            raise ValueError("finite-difference observations must match declared grids")
        expected_parent_coordinates = (
            self.definition.parent_model.reciprocal_vector.magnitude
            * np.asarray(
                self.definition.parent_sample_reduced_momenta, dtype=np.float64
            )
        )
        if not np.array_equal(
            self.parent_reference.coordinates.magnitude, expected_parent_coordinates
        ):
            raise ValueError("parent reference must use declared parent momenta")
        if self.parent_reference.band_count != self.definition.compared_band_count:
            raise ValueError("parent reference must use the declared band count")
        if type(self.training_target) is not BandSpectrumSamples1D:
            raise TypeError("training_target must be BandSpectrumSamples1D")
        if type(self.withheld_target) is not BandSpectrumSamples1D:
            raise TypeError("withheld_target must be BandSpectrumSamples1D")
        if self.training_target.band_count != 1 or self.withheld_target.band_count != 1:
            raise ValueError("isolated-band targets must contain exactly one band")
        if self.training_target.sample_count != self.definition.reciprocal_mesh_size:
            raise ValueError("training target must use the declared reciprocal mesh")
        if self.withheld_target.sample_count != self.definition.withheld_mesh_size:
            raise ValueError("withheld target must use the declared withheld mesh")
        expected_withheld_coordinates = (
            self.definition.parent_model.reciprocal_vector.magnitude
            * np.asarray(self.definition.withheld_reduced_momenta, dtype=np.float64)
        )
        if not np.array_equal(
            self.withheld_target.coordinates.magnitude,
            expected_withheld_coordinates,
        ):
            raise ValueError("withheld target must use the frozen staggered mesh")
        if (
            type(self.complete_transform)
            is not ReciprocalOperatorFourierTransformResult1D
        ):
            raise TypeError(
                "complete_transform must be ReciprocalOperatorFourierTransformResult1D"
            )
        if type(self.hopping_hermiticity) is not BlockHoppingHermiticityResult1D:
            raise TypeError(
                "hopping_hermiticity must be BlockHoppingHermiticityResult1D"
            )
        if self.hopping_hermiticity.model is not (
            self.complete_transform.hopping_model
        ):
            raise ValueError("Hermiticity must analyze the complete hopping model")
        if not isinstance(self.range_study, tuple) or any(
            type(item) is not Periodic1DIsolatedBandRangeResult
            for item in self.range_study
        ):
            raise TypeError("range_study must be a typed tuple")
        if tuple(item.maximum_range for item in self.range_study) != (
            self.definition.hopping_ranges
        ):
            raise ValueError("range results must match declared hopping ranges")
        if (
            self.complete_transform.mesh.point_count
            != self.definition.reciprocal_mesh_size
        ):
            raise ValueError("complete transform must use the declared training mesh")
        source = self.complete_transform.source
        if not np.array_equal(
            source.coordinates.magnitude, self.training_target.coordinates.magnitude
        ):
            raise ValueError("complete transform must use the training coordinates")
        source_complex_values = np.asarray(
            [matrix.magnitude[0, 0] for matrix in source.matrices],
            dtype=np.complex128,
        )
        if np.any(source_complex_values.imag != 0.0):
            raise ValueError("isolated-band source samples must remain real")
        if not np.array_equal(
            source_complex_values.real,
            self.training_target.eigenvalues.magnitude[:, 0],
        ):
            raise ValueError("complete transform must use the training spectrum")
        for item in self.range_study:
            if item.truncation.source is not self.complete_transform.hopping_model:
                raise ValueError("every truncation must use the complete hopping model")
            if item.parseval.transform is not self.complete_transform:
                raise ValueError(
                    "every Parseval diagnostic must use the complete transform"
                )
            if item.direct_fit.source is not source:
                raise ValueError(
                    "every direct fit must use the transform source samples"
                )
            if item.training_error.target is not self.training_target:
                raise ValueError("training diagnostics must use the training target")
            if item.withheld_error.target is not self.withheld_target:
                raise ValueError("withheld diagnostics must use the withheld target")
            if (
                item.direct_mediated_comparison.comparison_coordinates
                is not self.training_target.coordinates
            ):
                raise ValueError("route comparison must use the training coordinates")
            if item.band_shape.comparison_coordinates is not (
                self.withheld_target.coordinates
            ):
                raise ValueError("band shape must use the withheld coordinates")
        training_coordinates = self.training_target.coordinates.magnitude
        withheld_coordinates = self.withheld_target.coordinates.magnitude
        if (
            training_coordinates.shape == withheld_coordinates.shape
            and (training_coordinates == withheld_coordinates).all()
        ):
            raise ValueError("training and withheld coordinates must remain distinct")


__all__ = [
    "Periodic1DFiniteDifferenceConvergenceObservation",
    "Periodic1DIsolatedBandCalculationResult",
    "Periodic1DIsolatedBandRangeResult",
    "Periodic1DPlaneWaveConvergenceObservation",
]
