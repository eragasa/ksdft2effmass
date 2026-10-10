"""Calculation Action for a controlled one-dimensional isolated-band study."""

from __future__ import annotations

import numpy as np
from scipy.sparse.linalg import eigsh  # type: ignore[import-untyped]

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityAnalyzer1D,
    HoppingParsevalAnalyzer1D,
    ScalarHoppingBandShapeAnalyzer1D,
)
from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitter1D,
    BlockHoppingModelComparator1D,
)
from ksdft2effmass.analysis.model_systems import (
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicUniformGrid1D,
    PlaneWaveFiberHamiltonian1DConstructor,
)
from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorAnalyzer1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import (
    BlockHoppingInterpolator1D,
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformResult1D,
    ReciprocalOperatorSamples1D,
)

from .definition import Periodic1DIsolatedBandCalculationDefinition
from .results import (
    Periodic1DFiniteDifferenceConvergenceObservation,
    Periodic1DIsolatedBandCalculationResult,
    Periodic1DIsolatedBandRangeResult,
    Periodic1DPlaneWaveConvergenceObservation,
)


class Periodic1DIsolatedBandCalculator:
    """Compose maintained model, transform, fit, and diagnostic Actions.

    The calculator performs deterministic in-process numerical work.  It does not read
    or write retained artifacts, execute an external calculator, choose acceptance
    thresholds, calculate a Wannier gauge, or claim material validity.
    """

    __slots__ = ()

    def execute(
        self, definition: Periodic1DIsolatedBandCalculationDefinition
    ) -> Periodic1DIsolatedBandCalculationResult:
        """Calculate parent refinement and scalar hopping-reduction channels."""
        if type(definition) is not Periodic1DIsolatedBandCalculationDefinition:
            raise TypeError(
                "definition must be Periodic1DIsolatedBandCalculationDefinition"
            )
        model = definition.parent_model
        parent_reduced = np.asarray(
            definition.parent_sample_reduced_momenta, dtype=np.float64
        )
        parent_coordinates = self._physical_coordinates(definition, parent_reduced)
        parent_reference = self._plane_wave_spectrum(
            definition,
            definition.plane_wave_reference_cutoff,
            parent_coordinates,
            definition.compared_band_count,
        )
        plane_wave_convergence = tuple(
            Periodic1DPlaneWaveConvergenceObservation(
                cutoff,
                self._maximum_spectrum_error(
                    self._plane_wave_spectrum(
                        definition,
                        cutoff,
                        parent_coordinates,
                        definition.compared_band_count,
                    ),
                    parent_reference,
                ),
            )
            for cutoff in definition.plane_wave_cutoffs
        )
        finite_difference_convergence = tuple(
            Periodic1DFiniteDifferenceConvergenceObservation(
                points,
                self._maximum_spectrum_error(
                    self._finite_difference_spectrum(
                        definition,
                        points,
                        parent_coordinates,
                        definition.compared_band_count,
                    ),
                    parent_reference,
                ),
            )
            for points in definition.finite_difference_points
        )

        training_mesh = CenteredUniformReciprocalMesh1D(
            model.reciprocal_vector, definition.reciprocal_mesh_size
        )
        training_target = self._plane_wave_spectrum(
            definition,
            definition.production_plane_wave_cutoff,
            training_mesh.coordinates,
            1,
        )
        source = self._scalar_operator_samples(training_target)
        transform = ReciprocalOperatorFourierTransformer1D().execute(
            source,
            training_mesh,
            definition.coordinate_absolute_tolerance,
            definition.reconstruction_absolute_tolerance,
        )
        hermiticity = BlockHoppingHermiticityAnalyzer1D().execute(
            transform.hopping_model,
            definition.hermiticity_absolute_tolerance,
            definition.reciprocal_mesh_size,
        )

        withheld_reduced = np.asarray(
            definition.withheld_reduced_momenta, dtype=np.float64
        )
        withheld_coordinates = self._physical_coordinates(definition, withheld_reduced)
        withheld_target = self._plane_wave_spectrum(
            definition,
            definition.production_plane_wave_cutoff,
            withheld_coordinates,
            1,
        )
        range_study = tuple(
            self._calculate_range(
                definition,
                training_target,
                withheld_target,
                transform,
                maximum_range,
            )
            for maximum_range in definition.hopping_ranges
        )
        return Periodic1DIsolatedBandCalculationResult(
            definition,
            parent_reference,
            plane_wave_convergence,
            finite_difference_convergence,
            training_target,
            withheld_target,
            transform,
            hermiticity,
            range_study,
        )

    def _calculate_range(
        self,
        definition: Periodic1DIsolatedBandCalculationDefinition,
        training_target: BandSpectrumSamples1D,
        withheld_target: BandSpectrumSamples1D,
        transform: ReciprocalOperatorFourierTransformResult1D,
        maximum_range: int,
    ) -> Periodic1DIsolatedBandRangeResult:
        if type(transform) is not ReciprocalOperatorFourierTransformResult1D:
            raise TypeError(
                "transform must be ReciprocalOperatorFourierTransformResult1D"
            )
        truncation = BlockHoppingTruncator1D().execute(
            transform.hopping_model, maximum_range
        )
        interpolator = BlockHoppingInterpolator1D()
        training_candidate = interpolator.execute(
            truncation.truncated, training_target.coordinates
        )
        withheld_candidate = interpolator.execute(
            truncation.truncated, withheld_target.coordinates
        )
        error_analyzer = BandApproximationErrorAnalyzer1D()
        training_error = error_analyzer.execute(
            training_target,
            training_candidate,
            definition.coordinate_absolute_tolerance,
        )
        withheld_error = error_analyzer.execute(
            withheld_target,
            withheld_candidate,
            definition.coordinate_absolute_tolerance,
        )
        parseval = HoppingParsevalAnalyzer1D().execute(
            transform,
            truncation,
            definition.parseval_absolute_tolerance,
        )
        weights = VectorQuantity(
            np.ones(training_target.sample_count, dtype=np.float64), Unitless()
        )
        direct_fit = BlockHoppingLeastSquaresFitter1D().execute(
            transform.source,
            truncation.truncated.representatives,
            weights,
        )
        route_comparison = BlockHoppingModelComparator1D().execute(
            truncation.truncated,
            direct_fit.fitted_model,
            training_target.coordinates,
        )
        band_shape = ScalarHoppingBandShapeAnalyzer1D().execute(
            truncation.truncated,
            withheld_target.coordinates,
            definition.imaginary_absolute_tolerance,
        )
        return Periodic1DIsolatedBandRangeResult(
            truncation,
            training_error,
            withheld_error,
            parseval,
            direct_fit,
            route_comparison,
            band_shape,
        )

    def _plane_wave_spectrum(
        self,
        definition: Periodic1DIsolatedBandCalculationDefinition,
        cutoff: int,
        coordinates: VectorQuantity,
        band_count: int,
    ) -> BandSpectrumSamples1D:
        model = definition.parent_model
        reduced = coordinates.magnitude / model.reciprocal_vector.magnitude
        basis = PlaneWaveBasis1D(model.reciprocal_vector, cutoff)
        constructor = PlaneWaveFiberHamiltonian1DConstructor()
        values = np.asarray(
            [
                np.linalg.eigvalsh(
                    constructor.execute(
                        float(momentum),
                        basis,
                        model.potential,
                        model.recoil_energy,
                        model.duality_absolute_tolerance,
                    ).represented_matrix.magnitude
                )[:band_count]
                for momentum in reduced
            ],
            dtype=np.float64,
        )
        return BandSpectrumSamples1D(
            coordinates,
            model.reciprocal_vector,
            MatrixQuantity(values, model.recoil_energy.unit),
        )

    def _finite_difference_spectrum(
        self,
        definition: Periodic1DIsolatedBandCalculationDefinition,
        point_count: int,
        coordinates: VectorQuantity,
        band_count: int,
    ) -> BandSpectrumSamples1D:
        model = definition.parent_model
        grid = PeriodicUniformGrid1D(
            ScalarQuantity(0.0, model.potential.period.unit),
            model.potential.period,
            point_count,
        )
        reduced = coordinates.magnitude / model.reciprocal_vector.magnitude
        constructor = PeriodicFiniteDifferenceFiberHamiltonian1DConstructor()
        values: list[np.ndarray] = []
        for momentum in reduced:
            represented = constructor.execute(
                float(momentum),
                grid,
                model.potential,
                model.recoil_energy,
                model.duality_absolute_tolerance,
            ).represented_matrix.to_csr()
            eigenvalues = eigsh(
                represented,
                k=band_count,
                which="SA",
                return_eigenvectors=False,
                v0=np.full(
                    point_count,
                    1.0 / np.sqrt(float(point_count)),
                    dtype=np.float64,
                ),
            )
            values.append(np.sort(np.asarray(eigenvalues, dtype=np.float64)))
        return BandSpectrumSamples1D(
            coordinates,
            model.reciprocal_vector,
            MatrixQuantity(np.asarray(values), model.recoil_energy.unit),
        )

    def _physical_coordinates(
        self,
        definition: Periodic1DIsolatedBandCalculationDefinition,
        reduced: np.ndarray,
    ) -> VectorQuantity:
        if type(reduced) is not np.ndarray or reduced.dtype != np.float64:
            raise TypeError("reduced momenta must be a float64 numpy.ndarray")
        model = definition.parent_model
        return VectorQuantity(
            model.reciprocal_vector.magnitude * reduced,
            model.reciprocal_vector.unit,
        )

    def _maximum_spectrum_error(
        self,
        candidate: BandSpectrumSamples1D,
        reference: BandSpectrumSamples1D,
    ) -> ScalarQuantity:
        if candidate.eigenvalues.unit != reference.eigenvalues.unit:
            raise ValueError("candidate and reference spectra must use one energy unit")
        error = float(
            np.max(
                np.abs(
                    candidate.eigenvalues.magnitude - reference.eigenvalues.magnitude
                )
            )
        )
        return ScalarQuantity(error, reference.eigenvalues.unit)

    def _scalar_operator_samples(
        self, spectrum: BandSpectrumSamples1D
    ) -> ReciprocalOperatorSamples1D:
        if spectrum.band_count != 1:
            raise ValueError("scalar operator samples require exactly one band")
        return ReciprocalOperatorSamples1D(
            spectrum.coordinates,
            spectrum.reciprocal_period,
            tuple(
                ComplexMatrixQuantity(
                    np.asarray([[value]], dtype=np.complex128),
                    spectrum.eigenvalues.unit,
                )
                for value in spectrum.eigenvalues.magnitude[:, 0]
            ),
        )


__all__ = ["Periodic1DIsolatedBandCalculator"]
