"""Reusable complete-transform and finite-range single-band reduction Workflow."""

from __future__ import annotations

import numpy as np

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityAnalyzer1D,
    HoppingParsevalAnalyzer1D,
    ScalarHoppingBandShapeAnalyzer1D,
)
from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitter1D,
    BlockHoppingModelComparator1D,
)
from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorAnalyzer1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.solid_state import (
    BlockHoppingInterpolator1D,
    BlockHoppingTruncator1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformResult1D,
    ReciprocalOperatorSamples1D,
)

from .definition import SingleBandHoppingReductionRequest1D
from .results import (
    SingleBandHoppingRangeReductionResult1D,
    SingleBandHoppingReductionResult1D,
)


class SingleBandHoppingReductionWorkflow1D:
    """Reduce supplied single-band samples without owning an experiment.

    The Workflow applies one complete finite Fourier transform, symmetric finite-range
    truncations, weighted direct fits in the same representative classes, and separate
    training/evaluation diagnostics. It performs no parent calculation, band selection,
    filesystem access, evidence retention, acceptance decision, or interpretation.

    Notes
    -----
    ``BlockHoppingLeastSquaresFitter1D`` is the KSD domain adapter for the direct
    route. The reusable unit-free complex positive-weight multiple-right-hand-side
    least-squares kernel is supplied by an exact version-bound
    ``projectkoios-optimization`` dependency. This Workflow deliberately introduces no
    second solver, generic solver protocol, or owner-neutral least-squares result.
    """

    __slots__ = ()

    def execute(
        self, request: SingleBandHoppingReductionRequest1D
    ) -> SingleBandHoppingReductionResult1D:
        """Return the complete transform and every requested range result."""
        if type(request) is not SingleBandHoppingReductionRequest1D:
            raise TypeError("request must be SingleBandHoppingReductionRequest1D")
        converter = MODEL_SYSTEM_UNIT_CONVERTER
        energy_unit = request.training_target.eigenvalues.unit
        reciprocal_unit = request.training_target.reciprocal_period.unit
        squared_energy_unit = (
            Unitless()
            if isinstance(energy_unit, Unitless)
            else PhysicalUnit(f"({energy_unit.expression}) ** 2")
        )
        coordinate_tolerance = converter.convert_scalar(
            request.tolerances.coordinate_absolute, reciprocal_unit
        ).magnitude
        reconstruction_tolerance = converter.convert_scalar(
            request.tolerances.reconstruction_absolute, energy_unit
        ).magnitude
        hermiticity_tolerance = converter.convert_scalar(
            request.tolerances.hermiticity_absolute, energy_unit
        )
        parseval_tolerance = converter.convert_scalar(
            request.tolerances.parseval_absolute, squared_energy_unit
        )
        imaginary_tolerance = converter.convert_scalar(
            request.tolerances.imaginary_absolute, energy_unit
        )

        source = self._operator_samples(request.training_target)
        transform = ReciprocalOperatorFourierTransformer1D().execute(
            source,
            request.transform_mesh,
            coordinate_tolerance,
            reconstruction_tolerance,
        )
        hermiticity = BlockHoppingHermiticityAnalyzer1D().execute(
            transform.hopping_model,
            hermiticity_tolerance,
            request.transform_mesh.point_count,
        )
        ranges = tuple(
            self._reduce_range(
                request,
                source,
                transform,
                maximum_range,
                coordinate_tolerance,
                parseval_tolerance,
                imaginary_tolerance,
            )
            for maximum_range in request.hopping_ranges
        )
        return SingleBandHoppingReductionResult1D(
            request,
            source,
            transform,
            hermiticity,
            ranges,
        )

    @staticmethod
    def _operator_samples(
        target: BandSpectrumSamples1D,
    ) -> ReciprocalOperatorSamples1D:
        """Embed one real band as identified scalar reciprocal operators."""
        if type(target) is not BandSpectrumSamples1D:
            raise TypeError("target must be BandSpectrumSamples1D")
        if target.band_count != 1:
            raise ValueError("target must contain exactly one band")
        return ReciprocalOperatorSamples1D(
            target.coordinates,
            target.reciprocal_period,
            tuple(
                ComplexMatrixQuantity(
                    np.asarray([[value]], dtype=np.complex128),
                    target.eigenvalues.unit,
                )
                for value in target.eigenvalues.magnitude[:, 0]
            ),
        )

    @staticmethod
    def _reduce_range(
        request: SingleBandHoppingReductionRequest1D,
        source: ReciprocalOperatorSamples1D,
        transform: ReciprocalOperatorFourierTransformResult1D,
        maximum_range: int,
        coordinate_tolerance: float,
        parseval_tolerance: ScalarQuantity,
        imaginary_tolerance: ScalarQuantity,
    ) -> SingleBandHoppingRangeReductionResult1D:
        """Construct mediated/direct routes and diagnostics for one range."""
        if type(transform) is not ReciprocalOperatorFourierTransformResult1D:
            raise TypeError(
                "transform must be ReciprocalOperatorFourierTransformResult1D"
            )
        truncation = BlockHoppingTruncator1D().execute(
            transform.hopping_model, maximum_range
        )
        interpolator = BlockHoppingInterpolator1D()
        training_candidate = interpolator.execute(
            truncation.truncated, request.training_target.coordinates
        )
        evaluation_candidate = interpolator.execute(
            truncation.truncated, request.evaluation_target.coordinates
        )
        error_analyzer = BandApproximationErrorAnalyzer1D()
        training_error = error_analyzer.execute(
            request.training_target,
            training_candidate,
            coordinate_tolerance,
        )
        evaluation_error = error_analyzer.execute(
            request.evaluation_target,
            evaluation_candidate,
            coordinate_tolerance,
        )
        parseval = HoppingParsevalAnalyzer1D().execute(
            transform,
            truncation,
            parseval_tolerance,
        )
        direct_fit = BlockHoppingLeastSquaresFitter1D().execute(
            source,
            truncation.truncated.representatives,
            request.fitting_weights,
        )
        route_comparison = BlockHoppingModelComparator1D().execute(
            truncation.truncated,
            direct_fit.fitted_model,
            request.training_target.coordinates,
        )
        band_shape = ScalarHoppingBandShapeAnalyzer1D().execute(
            truncation.truncated,
            request.evaluation_target.coordinates,
            imaginary_tolerance,
        )
        return SingleBandHoppingRangeReductionResult1D(
            truncation,
            training_error,
            evaluation_error,
            parseval,
            direct_fit,
            route_comparison,
            band_shape,
        )


__all__ = ["SingleBandHoppingReductionWorkflow1D"]
