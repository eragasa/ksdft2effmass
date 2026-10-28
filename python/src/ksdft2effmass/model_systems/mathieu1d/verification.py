"""Byte-owning independent verification for direct Mathieu1D results."""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
from projectkoios.physkit.units import (
    ComplexVectorQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from scipy import sparse  # type: ignore[import-untyped]
from scipy.sparse.linalg import eigsh  # type: ignore[import-untyped]

from ksdft2effmass.model_systems.analysis import BaseModelAnalysisVerifier
from ksdft2effmass.model_systems.verification import (
    VisualizationProjectionVerification,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue
from ksdft2effmass.verification import (
    CompositeVerification,
    MaximumAbsoluteErrorComparison,
)

from .configuration import Mathieu1dConfiguration
from .result import (
    Mathieu1dBandSamplesResult,
    Mathieu1dCalculationResult,
    Mathieu1dRangeResult,
    Mathieu1dRefinementResult,
    Mathieu1dTransformResult,
)
from .verification_values import (
    Mathieu1dIndependentVerification,
    Mathieu1dVerification,
)
from .visualization import Mathieu1dVisualizationData


class Mathieu1dVerifier(
    BaseModelAnalysisVerifier[
        Mathieu1dCalculationResult,
        Mathieu1dVerification,
        Mathieu1dVisualizationData,
    ]
):
    """Independently reconstruct and verify a canonical Mathieu1D result wire.

    Parameters
    ----------
    result_wire
        Exact immutable built-in ``bytes`` containing one canonical typed
        :class:`Mathieu1dCalculationResult`.

    Notes
    -----
    Admission uses the existing byte-owning model-analysis boundary. The independent
    route assembles represented plane-wave and finite-difference matrices directly,
    applies explicit finite Fourier sums and direct least squares, and does not call
    :class:`Mathieu1dAnalyzer`, the reusable Fourier/fitting actions, or any historical
    workflow.
    """

    __slots__ = ()

    @classmethod
    def _result_type(cls) -> type[Mathieu1dCalculationResult]:
        """Return the typed Mathieu1D root reconstructed by the shared boundary."""
        return Mathieu1dCalculationResult

    def _visualization_data(self) -> Mathieu1dVisualizationData:
        """Project authoritative result values through the existing boundary."""
        return Mathieu1dVisualizationData.from_result(self._result)

    def _verification_types(self) -> tuple[type[CompositeVerification], ...]:
        """Return the exact ordered Mathieu1D verification inventory."""
        return (
            Mathieu1dIndependentVerification,
            VisualizationProjectionVerification,
        )

    def _verification_components(
        self,
        visualization_data: Mathieu1dVisualizationData,
    ) -> tuple[CompositeVerification, ...]:
        """Return independent full-result and projection correlations."""
        expected = self._reconstruct(
            self._result.configuration,
            calculation_family=self._result.calculation_family,
            execution_id=self._result.execution_id,
            evidence_status=self._result.evidence_status,
            claim_boundary=self._result.claim_boundary,
        )
        reconstruction: dict[str, MaximumAbsoluteErrorComparison] = {}
        self._compare_values(
            "result",
            self._result.to_dict(),
            expected.to_dict(),
            self._result.configuration,
            reconstruction,
        )
        expected_data = Mathieu1dVisualizationData.from_result(expected)
        projection: dict[str, MaximumAbsoluteErrorComparison] = {}
        self._compare_values(
            "visualization",
            visualization_data.to_dict(),
            expected_data.to_dict(),
            self._result.configuration,
            projection,
        )
        return (
            Mathieu1dIndependentVerification.evaluate(reconstruction),
            VisualizationProjectionVerification.evaluate(projection),
        )

    def _verification(
        self,
        *,
        visualization_data_sha256: str,
        components: tuple[CompositeVerification, ...],
    ) -> Mathieu1dVerification:
        """Compose the standard byte-owning Mathieu1D aggregate."""
        return Mathieu1dVerification(
            subject_sha256=self._subject_sha256,
            visualization_data_sha256=visualization_data_sha256,
            components=components,
        )

    @classmethod
    def _reconstruct(
        cls,
        configuration: Mathieu1dConfiguration,
        *,
        calculation_family: str,
        execution_id: str,
        evidence_status: str,
        claim_boundary: str,
    ) -> Mathieu1dCalculationResult:
        """Independently reconstruct all scientific fields under admitted metadata.

        Parameters
        ----------
        configuration
            Constructor-validated controls embedded in the admitted result wire.
        calculation_family, execution_id, evidence_status, claim_boundary
            Metadata copied exactly so it is covered by the complete mapping comparison.

        Returns
        -------
        Mathieu1dCalculationResult
            Independently assembled result with the production wire's typed structure.
        """
        unit = Unitless()
        parent_reduced = np.asarray(
            configuration.parent_reduced_momenta, dtype=np.float64
        )
        # Verification repeats finite matrix assembly directly. It does not call the
        # production periodic-model constructors or accept their matrices as references.
        parent_reference = cls._plane_wave_spectrum(
            configuration,
            configuration.plane_wave_reference_cutoff,
            parent_reduced,
            configuration.compared_band_count,
        )
        plane_wave_errors = np.asarray(
            [
                cls._maximum_error(
                    cls._plane_wave_spectrum(
                        configuration,
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
                cls._maximum_error(
                    cls._finite_difference_spectrum(
                        configuration,
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

        training_reduced = np.asarray(
            configuration.training_reduced_momenta, dtype=np.float64
        )
        evaluation_reduced = np.asarray(
            configuration.evaluation_reduced_momenta, dtype=np.float64
        )
        retained_count = configuration.selected_band_index + 2
        training_spectrum = cls._plane_wave_spectrum(
            configuration,
            configuration.production_plane_wave_cutoff,
            training_reduced,
            retained_count,
        )
        evaluation_spectrum = cls._plane_wave_spectrum(
            configuration,
            configuration.production_plane_wave_cutoff,
            evaluation_reduced,
            retained_count,
        )
        selected = configuration.selected_band_index
        training_target = training_spectrum[:, selected]
        evaluation_target = evaluation_spectrum[:, selected]
        bands = Mathieu1dBandSamplesResult(
            training_reduced_momenta=VectorQuantity(training_reduced, unit),
            training_selected_energies=VectorQuantity(training_target, unit),
            training_upper_energies=VectorQuantity(
                training_spectrum[:, selected + 1], unit
            ),
            training_external_gap=ScalarQuantity(
                float(np.min(training_spectrum[:, selected + 1] - training_target)),
                unit,
            ),
            evaluation_reduced_momenta=VectorQuantity(evaluation_reduced, unit),
            evaluation_selected_energies=VectorQuantity(evaluation_target, unit),
            evaluation_upper_energies=VectorQuantity(
                evaluation_spectrum[:, selected + 1], unit
            ),
            evaluation_external_gap=ScalarQuantity(
                float(np.min(evaluation_spectrum[:, selected + 1] - evaluation_target)),
                unit,
            ),
        )

        # Write the finite transform explicitly so normalization and phase signs are
        # independently visible rather than inherited from the production action.
        point_count = configuration.reciprocal_training_mesh_size
        representatives = tuple(range(-(point_count // 2), point_count // 2))
        representative_array = np.asarray(representatives, dtype=np.float64)
        forward_phases = np.exp(
            -2j * np.pi * np.outer(representative_array, training_reduced)
        )
        complete_hoppings = (forward_phases @ training_target) / float(point_count)
        complete_reconstructed = cls._interpolate(
            representatives, complete_hoppings, training_reduced
        )
        reconstruction_error = float(
            np.max(np.abs(complete_reconstructed - training_target))
        )
        # The centered even inventory pairs the Nyquist representative by periodic
        # negation, not by requiring the literal integer ``-R`` to be present.
        lookup = {
            representative: index
            for index, representative in enumerate(representatives)
        }
        paired: list[int] = []
        missing: list[int] = []
        hermiticity_defects: list[float] = []
        for representative in representatives:
            candidates = tuple(
                value
                for value in representatives
                if (value + representative) % point_count == 0
            )
            if len(candidates) != 1:
                missing.append(representative)
                continue
            paired.append(representative)
            opposite = candidates[0]
            hermiticity_defects.append(
                abs(
                    complete_hoppings[lookup[representative]]
                    - np.conjugate(complete_hoppings[lookup[opposite]])
                )
            )
        hermiticity_maximum = float(max(hermiticity_defects, default=0.0))
        transform = Mathieu1dTransformResult(
            representatives=representatives,
            hopping_blocks=ComplexVectorQuantity(complete_hoppings, unit),
            reconstructed_training=ComplexVectorQuantity(complete_reconstructed, unit),
            reconstruction_maximum_error=ScalarQuantity(reconstruction_error, unit),
            reconstruction_absolute_tolerance=ScalarQuantity(
                configuration.reconstruction_absolute_tolerance, unit
            ),
            reconstruction_passes=(
                reconstruction_error <= configuration.reconstruction_absolute_tolerance
            ),
            paired_representatives=tuple(sorted(paired)),
            missing_opposite_representatives=tuple(sorted(missing)),
            hermiticity_maximum_defect=ScalarQuantity(hermiticity_maximum, unit),
            hermiticity_absolute_tolerance=ScalarQuantity(
                configuration.hermiticity_absolute_tolerance, unit
            ),
            hermiticity_passes=(
                not missing
                and hermiticity_maximum <= configuration.hermiticity_absolute_tolerance
            ),
        )

        weights = np.asarray(configuration.fitting_weights, dtype=np.float64)
        ranges = tuple(
            cls._reconstruct_range(
                configuration,
                representatives,
                complete_hoppings,
                training_reduced,
                training_target,
                evaluation_reduced,
                evaluation_target,
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
    def _reconstruct_range(
        cls,
        configuration: Mathieu1dConfiguration,
        complete_representatives: tuple[int, ...],
        complete_hoppings: np.ndarray,
        training_reduced: np.ndarray,
        training_target: np.ndarray,
        evaluation_reduced: np.ndarray,
        evaluation_target: np.ndarray,
        weights: np.ndarray,
        maximum_range: int,
    ) -> Mathieu1dRangeResult:
        """Independently reconstruct one mediated/direct finite-range result.

        Parameters
        ----------
        configuration
            Typed tolerances and fitting controls.
        complete_representatives, complete_hoppings
            Complete finite-transform parent inventory.
        training_reduced, training_target
            Coordinates and selected-band values used for construction.
        evaluation_reduced, evaluation_target
            Disjoint coordinates and selected-band values used only for evaluation.
        weights
            Positive weighted least-squares objective coefficients.
        maximum_range
            Symmetric retained representative radius.

        Returns
        -------
        Mathieu1dRangeResult
            Independently reconstructed coefficients and diagnostics.
        """
        unit = Unitless()
        retained_indices = tuple(
            index
            for index, representative in enumerate(complete_representatives)
            if abs(representative) <= maximum_range
        )
        retained_representatives = tuple(
            complete_representatives[index] for index in retained_indices
        )
        mediated = complete_hoppings[np.asarray(retained_indices, dtype=np.int64)]
        # The omitted norm is evaluated from the complement of the complete parent;
        # it is not inferred from the sampled reconstruction error.
        omitted_mask = np.ones(len(complete_representatives), dtype=np.bool_)
        omitted_mask[np.asarray(retained_indices, dtype=np.int64)] = False
        omitted_norm = float(np.linalg.norm(complete_hoppings[omitted_mask]))
        training_candidate = cls._interpolate(
            retained_representatives, mediated, training_reduced
        )
        evaluation_candidate = cls._interpolate(
            retained_representatives, mediated, evaluation_reduced
        )
        training_errors = np.abs(training_candidate.real - training_target)
        evaluation_errors = np.abs(evaluation_candidate.real - evaluation_target)
        training_squared = float(
            np.sum(np.abs(training_candidate - training_target) ** 2)
        )
        expected_squared = float(len(training_reduced) * omitted_norm**2)
        parseval_residual = abs(training_squared - expected_squared)

        representatives_array = np.asarray(retained_representatives, dtype=np.float64)
        design = np.exp(2j * np.pi * np.outer(training_reduced, representatives_array))
        square_root_weights = np.sqrt(weights)
        weighted_design = design * square_root_weights[:, np.newaxis]
        weighted_target = training_target * square_root_weights
        # Refit the same finite basis directly. This independent route deliberately
        # bypasses the reusable least-squares owner called by production.
        direct, _, rank, singular_values = np.linalg.lstsq(
            weighted_design, weighted_target, rcond=None
        )
        direct_training = design @ direct
        direct_residuals = direct_training - training_target
        condition = float(singular_values[0] / singular_values[-1])
        coefficient_defect = float(np.linalg.norm(direct - mediated))
        mediated_training = design @ mediated
        sampled_defect = direct_training - mediated_training
        curvature = np.sum(-((2.0 * np.pi * representatives_array) ** 2) * mediated)
        maximum_imaginary = max(
            float(np.max(np.abs(evaluation_candidate.imag))),
            abs(float(curvature.imag)),
        )
        return Mathieu1dRangeResult(
            maximum_range=maximum_range,
            representatives=retained_representatives,
            mediated_hopping_blocks=ComplexVectorQuantity(mediated, unit),
            direct_hopping_blocks=ComplexVectorQuantity(direct, unit),
            training_candidate=ComplexVectorQuantity(training_candidate, unit),
            evaluation_candidate=ComplexVectorQuantity(evaluation_candidate, unit),
            training_maximum_error=ScalarQuantity(float(np.max(training_errors)), unit),
            evaluation_maximum_error=ScalarQuantity(
                float(np.max(evaluation_errors)), unit
            ),
            omitted_block_l2_norm=ScalarQuantity(omitted_norm, unit),
            parseval_training_squared_residual=ScalarQuantity(training_squared, unit),
            parseval_expected_squared_residual=ScalarQuantity(expected_squared, unit),
            parseval_absolute_residual=ScalarQuantity(parseval_residual, unit),
            parseval_absolute_tolerance=ScalarQuantity(
                configuration.parseval_absolute_tolerance, unit
            ),
            parseval_passes=(
                parseval_residual <= configuration.parseval_absolute_tolerance
            ),
            direct_design_rank=int(rank),
            direct_design_condition_number=condition,
            direct_is_identified=(int(rank) == len(retained_representatives)),
            direct_training_l2_residual=ScalarQuantity(
                float(np.linalg.norm(direct_residuals)), unit
            ),
            direct_training_maximum_residual=ScalarQuantity(
                float(np.max(np.abs(direct_residuals))), unit
            ),
            route_coefficient_l2_defect=ScalarQuantity(coefficient_defect, unit),
            route_sampled_l2_defect=ScalarQuantity(
                float(np.linalg.norm(sampled_defect)), unit
            ),
            route_sampled_maximum_defect=ScalarQuantity(
                float(np.max(np.abs(sampled_defect))), unit
            ),
            bandwidth=ScalarQuantity(float(np.ptp(evaluation_candidate.real)), unit),
            zone_center_curvature=ScalarQuantity(float(curvature.real), unit),
            maximum_imaginary_residual=ScalarQuantity(maximum_imaginary, unit),
            imaginary_absolute_tolerance=ScalarQuantity(
                configuration.imaginary_absolute_tolerance, unit
            ),
            band_shape_passes=(
                maximum_imaginary <= configuration.imaginary_absolute_tolerance
            ),
        )

    @staticmethod
    def _plane_wave_spectrum(
        configuration: Mathieu1dConfiguration,
        cutoff: int,
        reduced: np.ndarray,
        band_count: int,
    ) -> np.ndarray:
        """Diagonalize independently assembled dense plane-wave fibers."""
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        dimension = indices.size
        potential = np.eye(dimension, dtype=np.float64) * (
            configuration.constant_coefficient
        )
        off_diagonal = np.full(
            dimension - 1,
            configuration.cosine_amplitude / 2.0,
            dtype=np.float64,
        )
        potential += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
        rows = []
        for momentum in reduced:
            kinetic = configuration.recoil_energy * (indices + momentum) ** 2
            matrix = potential + np.diag(kinetic)
            rows.append(np.linalg.eigvalsh(matrix)[:band_count])
        return np.asarray(rows, dtype=np.float64)

    @staticmethod
    def _finite_difference_spectrum(
        configuration: Mathieu1dConfiguration,
        point_count: int,
        reduced: np.ndarray,
        band_count: int,
    ) -> np.ndarray:
        """Diagonalize independently assembled sparse twisted-grid fibers."""
        # The periodic grid excludes the duplicate right endpoint. Bloch twist enters
        # only through the conjugate seam links assembled below.
        coordinates = (
            configuration.period
            * np.arange(point_count, dtype=np.float64)
            / float(point_count)
        )
        potential = (
            configuration.constant_coefficient
            + configuration.cosine_amplitude
            * np.cos(2.0 * np.pi * coordinates / configuration.period)
        )
        reciprocal_spacing = 2.0 * np.pi / float(point_count)
        link = configuration.recoil_energy / (reciprocal_spacing**2)
        rows: list[np.ndarray] = []
        for momentum in reduced:
            matrix = sparse.diags(
                (
                    np.full(point_count - 1, -link, dtype=np.complex128),
                    (2.0 * link + potential).astype(np.complex128),
                    np.full(point_count - 1, -link, dtype=np.complex128),
                ),
                offsets=(-1, 0, 1),
                shape=(point_count, point_count),
                format="lil",
                dtype=np.complex128,
            )
            seam = -link * np.exp(-2j * np.pi * momentum)
            matrix[0, point_count - 1] = seam
            matrix[point_count - 1, 0] = np.conjugate(seam)
            # Retain the sparse representation and provide deterministic ARPACK state;
            # independent verification must not hide a dense conversion.
            values = eigsh(
                matrix.tocsr(),
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
    def _interpolate(
        representatives: tuple[int, ...],
        hoppings: np.ndarray,
        reduced: np.ndarray,
    ) -> np.ndarray:
        """Evaluate an explicit finite Fourier sum."""
        return np.asarray(
            np.exp(
                2j
                * np.pi
                * np.outer(reduced, np.asarray(representatives, dtype=np.float64))
            )
            @ hoppings,
            dtype=np.complex128,
        )

    @staticmethod
    def _maximum_error(candidate: np.ndarray, reference: np.ndarray) -> float:
        """Return maximum absolute entrywise discrepancy."""
        return float(np.max(np.abs(candidate - reference)))

    @classmethod
    def _compare_values(
        cls,
        name: str,
        observed: SerializableValue,
        expected: SerializableValue,
        configuration: Mathieu1dConfiguration,
        output: dict[str, MaximumAbsoluteErrorComparison],
    ) -> None:
        """Recursively compare complete typed record mappings."""
        if isinstance(observed, BaseTypedRecord) and isinstance(
            expected, BaseTypedRecord
        ):
            cls._compare_values(
                name,
                observed.to_dict(),
                expected.to_dict(),
                configuration,
                output,
            )
            return
        if isinstance(observed, Mapping) and isinstance(expected, Mapping):
            # Compare the union so missing and unexpected fields become explicit failed
            # observations instead of disappearing through a common-key traversal.
            keys = sorted(set(observed) | set(expected))
            for key in keys:
                comparison_name = f"{name}.{key}"
                if key not in observed or key not in expected:
                    output[comparison_name] = cls._exact_comparison(False)
                    continue
                cls._compare_values(
                    comparison_name,
                    observed[key],
                    expected[key],
                    configuration,
                    output,
                )
            return
        if isinstance(observed, tuple) and isinstance(expected, tuple):
            output[f"{name}.length"] = cls._exact_comparison(
                len(observed) == len(expected)
            )
            for index, (observed_item, expected_item) in enumerate(
                zip(observed, expected, strict=False)
            ):
                cls._compare_values(
                    f"{name}[{index}]",
                    observed_item,
                    expected_item,
                    configuration,
                    output,
                )
            return
        quantity_types = (
            ScalarQuantity,
            VectorQuantity,
            ComplexVectorQuantity,
            MatrixQuantity,
        )
        if isinstance(observed, quantity_types) and isinstance(
            expected, quantity_types
        ):
            # Coordinate comparisons have their own geometric tolerance. All other
            # numeric fields use the declared finite reconstruction tolerance.
            tolerance = (
                configuration.coordinate_absolute_tolerance
                if "momenta" in name
                else configuration.reconstruction_absolute_tolerance
            )
            output[name] = MaximumAbsoluteErrorComparison(
                observed=observed,
                reference=expected,
                tolerance=ScalarQuantity(tolerance, observed.unit),
            )
            return
        if type(observed) is float and type(expected) is float:
            unit = Unitless()
            output[name] = MaximumAbsoluteErrorComparison(
                observed=ScalarQuantity(observed, unit),
                reference=ScalarQuantity(expected, unit),
                tolerance=ScalarQuantity(
                    configuration.reconstruction_absolute_tolerance, unit
                ),
            )
            return
        if type(observed) in (bool, int, str) and type(expected) is type(observed):
            output[name] = cls._exact_comparison(observed == expected)
            return
        output[name] = cls._exact_comparison(False)

    @staticmethod
    def _exact_comparison(passes: bool) -> MaximumAbsoluteErrorComparison:
        """Return one exact structural comparison."""
        unit = Unitless()
        return MaximumAbsoluteErrorComparison(
            observed=ScalarQuantity(0.0 if passes else 1.0, unit),
            reference=ScalarQuantity(0.0, unit),
            tolerance=ScalarQuantity(0.0, unit),
        )


__all__ = ["Mathieu1dVerifier"]
