"""Direct production analysis for the finite Mathieu1D reduction."""

from __future__ import annotations

import numpy as np
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexVectorQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
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
from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorAnalyzer1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.model_systems.periodic_1d import (
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicFourierPotential1D,
    PeriodicUniformGrid1D,
    PlaneWaveFiberHamiltonian1DConstructor,
)
from ksdft2effmass.solidstate import (
    BlockHoppingInterpolator1D,
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformResult1D,
    ReciprocalOperatorSamples1D,
)

from .configuration import Mathieu1dConfiguration
from .result import (
    Mathieu1dBandSamplesResult,
    Mathieu1dCalculationResult,
    Mathieu1dRangeResult,
    Mathieu1dRefinementResult,
    Mathieu1dTransformResult,
)


class Mathieu1dAnalyzer:
    """Calculate one direct finite Mathieu1D reduction.

    The analyzer calls canonical representation, Fourier, truncation, fitting, and
    diagnostic owners directly. It does not call a Workflow, read retained artifacts,
    perform filesystem effects, choose an adequate range, or claim continuum
    isolation.
    """

    __slots__ = ()

    def calculate(
        self,
        configuration: Mathieu1dConfiguration,
        *,
        calculation_family: str,
        execution_id: str,
        evidence_status: str,
        claim_boundary: str,
    ) -> Mathieu1dCalculationResult:
        """Return one typed finite-reduction result.

        Parameters
        ----------
        configuration
            Validated unitless finite calculation controls.
        calculation_family
            Stable ``"mathieu1d-finite-reduction"`` family identifier.
        execution_id
            Concrete execution identifier attached to the result bytes.
        evidence_status
            Explicit classification of the finite numerical result.
        claim_boundary
            Human-readable limit on claims supported by the calculation.

        Returns
        -------
        Mathieu1dCalculationResult
            Complete metadata, parent refinement, band samples, transform, and range
            result.

        Raises
        ------
        TypeError
            Configuration or metadata has the wrong domain type.
        ValueError
            Metadata is empty or the calculation family is unsupported.
        """
        if not isinstance(configuration, Mathieu1dConfiguration):
            raise TypeError("configuration must be Mathieu1dConfiguration")
        for name, value in (
            ("calculation_family", calculation_family),
            ("execution_id", execution_id),
            ("evidence_status", evidence_status),
            ("claim_boundary", claim_boundary),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if calculation_family != "mathieu1d-finite-reduction":
            raise ValueError("calculation_family does not identify Mathieu1D reduction")
        # Materialize the one-harmonic parent once so both represented routes consume
        # identical model coefficients and direct/reciprocal conventions.
        unit = Unitless()
        potential = PeriodicFourierPotential1D(
            period=ScalarQuantity(configuration.period, unit),
            constant_coefficient=ScalarQuantity(
                configuration.constant_coefficient, unit
            ),
            cosine_coefficients=VectorQuantity(
                np.asarray([configuration.cosine_amplitude], dtype=np.float64), unit
            ),
            sine_coefficients=VectorQuantity(np.asarray([0.0], dtype=np.float64), unit),
        )
        reciprocal = ScalarQuantity(configuration.reciprocal_vector, unit)
        recoil = ScalarQuantity(configuration.recoil_energy, unit)
        parent_reduced = np.asarray(
            configuration.parent_reduced_momenta, dtype=np.float64
        )
        # The largest plane-wave cutoff is an explicitly finite comparison reference;
        # no value in this block is labeled as a continuum spectrum.
        parent_reference = self._plane_wave_spectrum(
            configuration,
            potential,
            reciprocal,
            recoil,
            configuration.plane_wave_reference_cutoff,
            parent_reduced,
            configuration.compared_band_count,
        )
        plane_wave_errors = np.asarray(
            [
                self._maximum_error(
                    self._plane_wave_spectrum(
                        configuration,
                        potential,
                        reciprocal,
                        recoil,
                        cutoff,
                        parent_reduced,
                        configuration.compared_band_count,
                    ),
                    parent_reference,
                )
                for cutoff in configuration.plane_wave_cutoffs
            ],
            dtype=np.float64,
        )
        finite_difference_errors = np.asarray(
            [
                self._maximum_error(
                    self._finite_difference_spectrum(
                        configuration,
                        potential,
                        recoil,
                        point_count,
                        parent_reduced,
                        configuration.compared_band_count,
                    ),
                    parent_reference,
                )
                for point_count in configuration.finite_difference_points
            ],
            dtype=np.float64,
        )
        refinement = Mathieu1dRefinementResult(
            parent_reduced_momenta=VectorQuantity(parent_reduced, unit),
            parent_reference_energies=MatrixQuantity(parent_reference, unit),
            plane_wave_cutoffs=configuration.plane_wave_cutoffs,
            plane_wave_maximum_errors=VectorQuantity(plane_wave_errors, unit),
            finite_difference_points=configuration.finite_difference_points,
            finite_difference_maximum_errors=VectorQuantity(
                finite_difference_errors, unit
            ),
        )

        # Construction and withheld evaluation remain separate from this point onward.
        # The configuration constructor has already rejected overlapping coordinates.
        training_reduced = np.asarray(
            configuration.training_reduced_momenta, dtype=np.float64
        )
        evaluation_reduced = np.asarray(
            configuration.evaluation_reduced_momenta, dtype=np.float64
        )
        retained_count = configuration.selected_band_index + 2
        training_spectrum = self._plane_wave_spectrum(
            configuration,
            potential,
            reciprocal,
            recoil,
            configuration.production_plane_wave_cutoff,
            training_reduced,
            retained_count,
        )
        evaluation_spectrum = self._plane_wave_spectrum(
            configuration,
            potential,
            reciprocal,
            recoil,
            configuration.production_plane_wave_cutoff,
            evaluation_reduced,
            retained_count,
        )
        selected = configuration.selected_band_index
        bands = Mathieu1dBandSamplesResult(
            training_reduced_momenta=VectorQuantity(training_reduced, unit),
            training_selected_energies=VectorQuantity(
                training_spectrum[:, selected], unit
            ),
            training_upper_energies=VectorQuantity(
                training_spectrum[:, selected + 1], unit
            ),
            training_external_gap=ScalarQuantity(
                float(
                    np.min(
                        training_spectrum[:, selected + 1]
                        - training_spectrum[:, selected]
                    )
                ),
                unit,
            ),
            evaluation_reduced_momenta=VectorQuantity(evaluation_reduced, unit),
            evaluation_selected_energies=VectorQuantity(
                evaluation_spectrum[:, selected], unit
            ),
            evaluation_upper_energies=VectorQuantity(
                evaluation_spectrum[:, selected + 1], unit
            ),
            evaluation_external_gap=ScalarQuantity(
                float(
                    np.min(
                        evaluation_spectrum[:, selected + 1]
                        - evaluation_spectrum[:, selected]
                    )
                ),
                unit,
            ),
        )

        training_coordinates = VectorQuantity(
            training_reduced * configuration.reciprocal_vector, unit
        )
        evaluation_coordinates = VectorQuantity(
            evaluation_reduced * configuration.reciprocal_vector, unit
        )
        training_target = BandSpectrumSamples1D(
            training_coordinates,
            reciprocal,
            MatrixQuantity(training_spectrum[:, selected : selected + 1], unit),
        )
        evaluation_target = BandSpectrumSamples1D(
            evaluation_coordinates,
            reciprocal,
            MatrixQuantity(evaluation_spectrum[:, selected : selected + 1], unit),
        )
        # A scalar selected band is represented as 1x1 operator samples so the shared
        # block-Fourier infrastructure retains its normal operator semantics.
        source = ReciprocalOperatorSamples1D(
            training_coordinates,
            reciprocal,
            tuple(
                ComplexMatrixQuantity(np.asarray([[value]], dtype=np.complex128), unit)
                for value in training_spectrum[:, selected]
            ),
        )
        mesh = CenteredUniformReciprocalMesh1D(
            reciprocal, configuration.reciprocal_training_mesh_size
        )
        # The complete transform owns all N coefficients. Range studies below derive
        # from this immutable parent rather than chaining truncations between ranges.
        complete = ReciprocalOperatorFourierTransformer1D().execute(
            source,
            mesh,
            configuration.coordinate_absolute_tolerance,
            configuration.reconstruction_absolute_tolerance,
        )
        hermiticity = BlockHoppingHermiticityAnalyzer1D().execute(
            complete.hopping_model,
            ScalarQuantity(configuration.hermiticity_absolute_tolerance, unit),
            configuration.reciprocal_training_mesh_size,
        )
        transform = Mathieu1dTransformResult(
            representatives=complete.hopping_model.representatives,
            hopping_blocks=ComplexVectorQuantity(
                self._scalar_blocks(complete.hopping_model.hopping_blocks), unit
            ),
            reconstructed_training=ComplexVectorQuantity(
                self._scalar_samples(complete.reconstructed), unit
            ),
            reconstruction_maximum_error=ScalarQuantity(
                complete.reconstruction_maximum_frobenius_error, unit
            ),
            reconstruction_absolute_tolerance=ScalarQuantity(
                complete.reconstruction_absolute_tolerance, unit
            ),
            reconstruction_passes=complete.reconstruction_passes,
            paired_representatives=hermiticity.paired_representatives,
            missing_opposite_representatives=(
                hermiticity.missing_opposite_representatives
            ),
            hermiticity_maximum_defect=hermiticity.maximum_frobenius_defect,
            hermiticity_absolute_tolerance=hermiticity.absolute_tolerance,
            hermiticity_passes=hermiticity.passes,
        )

        weights = VectorQuantity(
            np.asarray(configuration.fitting_weights, dtype=np.float64), unit
        )
        # Each range independently compares mediated truncation with a direct fit on
        # exactly the same representative inventory.
        ranges = tuple(
            self._calculate_range(
                configuration,
                source,
                complete,
                training_target,
                evaluation_target,
                training_coordinates,
                evaluation_coordinates,
                weights,
                maximum_range,
            )
            for maximum_range in configuration.hopping_ranges
        )
        return Mathieu1dCalculationResult(
            calculation_family=calculation_family,
            execution_id=execution_id,
            evidence_status=evidence_status,
            claim_boundary=claim_boundary,
            configuration=configuration,
            refinement=refinement,
            bands=bands,
            transform=transform,
            ranges=ranges,
        )

    @classmethod
    def _calculate_range(
        cls,
        configuration: Mathieu1dConfiguration,
        source: ReciprocalOperatorSamples1D,
        complete: ReciprocalOperatorFourierTransformResult1D,
        training_target: BandSpectrumSamples1D,
        evaluation_target: BandSpectrumSamples1D,
        training_coordinates: VectorQuantity,
        evaluation_coordinates: VectorQuantity,
        weights: VectorQuantity,
        maximum_range: int,
    ) -> Mathieu1dRangeResult:
        """Calculate one finite-range route pair and diagnostics."""
        if not isinstance(complete, ReciprocalOperatorFourierTransformResult1D):
            raise TypeError("complete must be a Fourier-transform result")
        unit = Unitless()
        # The mediated route discards complete-transform blocks outside the authored
        # symmetric range; the direct route below refits rather than reuses them.
        truncation = BlockHoppingTruncator1D().execute(
            complete.hopping_model, maximum_range
        )
        interpolator = BlockHoppingInterpolator1D()
        training_candidate = interpolator.execute(
            truncation.truncated, training_coordinates
        )
        evaluation_candidate = interpolator.execute(
            truncation.truncated, evaluation_coordinates
        )
        error_analyzer = BandApproximationErrorAnalyzer1D()
        training_error = error_analyzer.execute(
            training_target,
            training_candidate,
            configuration.coordinate_absolute_tolerance,
        )
        evaluation_error = error_analyzer.execute(
            evaluation_target,
            evaluation_candidate,
            configuration.coordinate_absolute_tolerance,
        )
        parseval = HoppingParsevalAnalyzer1D().execute(
            complete,
            truncation,
            ScalarQuantity(configuration.parseval_absolute_tolerance, unit),
        )
        # Positive authored weights make the fit objective explicit and prevent the
        # withheld evaluation inventory from influencing coefficient construction.
        direct = BlockHoppingLeastSquaresFitter1D().execute(
            source, truncation.truncated.representatives, weights
        )
        if direct.design_condition_number is None:
            raise RuntimeError("configured direct fit must have full numerical rank")
        route = BlockHoppingModelComparator1D().execute(
            truncation.truncated, direct.fitted_model, training_coordinates
        )
        shape = ScalarHoppingBandShapeAnalyzer1D().execute(
            truncation.truncated,
            evaluation_coordinates,
            ScalarQuantity(configuration.imaginary_absolute_tolerance, unit),
        )
        return Mathieu1dRangeResult(
            maximum_range=maximum_range,
            representatives=truncation.truncated.representatives,
            mediated_hopping_blocks=ComplexVectorQuantity(
                cls._scalar_blocks(truncation.truncated.hopping_blocks), unit
            ),
            direct_hopping_blocks=ComplexVectorQuantity(
                cls._scalar_blocks(direct.fitted_model.hopping_blocks), unit
            ),
            training_candidate=ComplexVectorQuantity(
                cls._scalar_samples(training_candidate), unit
            ),
            evaluation_candidate=ComplexVectorQuantity(
                cls._scalar_samples(evaluation_candidate), unit
            ),
            training_maximum_error=training_error.maximum_absolute_error,
            evaluation_maximum_error=evaluation_error.maximum_absolute_error,
            omitted_block_l2_norm=ScalarQuantity(
                truncation.omitted_block_l2_norm, unit
            ),
            parseval_training_squared_residual=(
                parseval.training_squared_frobenius_residual
            ),
            parseval_expected_squared_residual=(
                parseval.expected_squared_frobenius_residual
            ),
            parseval_absolute_residual=parseval.parseval_absolute_residual,
            parseval_absolute_tolerance=parseval.absolute_tolerance,
            parseval_passes=parseval.passes,
            direct_design_rank=direct.design_rank,
            direct_design_condition_number=direct.design_condition_number,
            direct_is_identified=direct.is_identified,
            direct_training_l2_residual=ScalarQuantity(
                direct.training_l2_frobenius_residual, unit
            ),
            direct_training_maximum_residual=ScalarQuantity(
                direct.training_maximum_frobenius_residual, unit
            ),
            route_coefficient_l2_defect=route.coefficient_l2_frobenius_defect,
            route_sampled_l2_defect=route.sampled_l2_frobenius_defect,
            route_sampled_maximum_defect=(route.sampled_maximum_frobenius_defect),
            bandwidth=shape.bandwidth,
            zone_center_curvature=shape.zone_center_curvature,
            maximum_imaginary_residual=shape.maximum_imaginary_residual,
            imaginary_absolute_tolerance=shape.imaginary_absolute_tolerance,
            band_shape_passes=shape.passes,
        )

    @staticmethod
    def _plane_wave_spectrum(
        configuration: Mathieu1dConfiguration,
        potential: PeriodicFourierPotential1D,
        reciprocal: ScalarQuantity,
        recoil: ScalarQuantity,
        cutoff: int,
        reduced: np.ndarray,
        band_count: int,
    ) -> np.ndarray:
        """Return ordered finite plane-wave eigenvalues."""
        basis = PlaneWaveBasis1D(reciprocal, cutoff)
        constructor = PlaneWaveFiberHamiltonian1DConstructor()
        return np.asarray(
            [
                np.linalg.eigvalsh(
                    constructor.execute(
                        float(momentum),
                        basis,
                        potential,
                        recoil,
                        configuration.duality_absolute_tolerance,
                    ).represented_matrix.magnitude
                )[:band_count]
                for momentum in reduced
            ],
            dtype=np.float64,
        )

    @staticmethod
    def _finite_difference_spectrum(
        configuration: Mathieu1dConfiguration,
        potential: PeriodicFourierPotential1D,
        recoil: ScalarQuantity,
        point_count: int,
        reduced: np.ndarray,
        band_count: int,
    ) -> np.ndarray:
        """Return ordered periodic finite-difference eigenvalues."""
        unit = Unitless()
        grid = PeriodicUniformGrid1D(
            ScalarQuantity(0.0, unit),
            ScalarQuantity(configuration.period, unit),
            point_count,
        )
        constructor = PeriodicFiniteDifferenceFiberHamiltonian1DConstructor()
        rows: list[np.ndarray] = []
        for momentum in reduced:
            matrix = constructor.execute(
                float(momentum),
                grid,
                potential,
                recoil,
                configuration.duality_absolute_tolerance,
            ).represented_matrix.to_csr()
            # A deterministic nonzero starting vector avoids treating ARPACK's random
            # initialization as undeclared execution state.
            values = eigsh(
                matrix,
                k=band_count,
                which="SA",
                return_eigenvectors=False,
                v0=np.full(
                    point_count,
                    1.0 / np.sqrt(float(point_count)),
                    dtype=np.float64,
                ),
            )
            rows.append(np.sort(np.asarray(values, dtype=np.float64)))
        return np.asarray(rows, dtype=np.float64)

    @staticmethod
    def _maximum_error(candidate: np.ndarray, reference: np.ndarray) -> float:
        """Return the maximum absolute entrywise discrepancy."""
        if candidate.shape != reference.shape:
            raise ValueError("candidate and reference shapes must agree")
        return float(np.max(np.abs(candidate - reference)))

    @staticmethod
    def _scalar_blocks(
        blocks: tuple[ComplexMatrixQuantity, ...],
    ) -> np.ndarray:
        """Return scalar complex hopping entries in declared order."""
        values = np.asarray(
            [block.magnitude[0, 0] for block in blocks], dtype=np.complex128
        )
        return Mathieu1dAnalyzer._canonical_complex(values)

    @staticmethod
    def _scalar_samples(samples: ReciprocalOperatorSamples1D) -> np.ndarray:
        """Return scalar complex reciprocal samples in coordinate order."""
        values = np.asarray(
            [matrix.magnitude[0, 0] for matrix in samples.matrices],
            dtype=np.complex128,
        )
        return Mathieu1dAnalyzer._canonical_complex(values)

    @staticmethod
    def _canonical_complex(values: np.ndarray) -> np.ndarray:
        """Normalize signed complex zeros for stable typed-wire round trips."""
        # JSON preserves the sign bit of floating zero. Canonicalizing it here avoids
        # platform-dependent byte differences with no mathematical distinction.
        real = np.where(values.real == 0.0, 0.0, values.real)
        imaginary = np.where(values.imag == 0.0, 0.0, values.imag)
        return np.asarray(real + 1j * imaginary, dtype=np.complex128)


__all__ = ["Mathieu1dAnalyzer"]
