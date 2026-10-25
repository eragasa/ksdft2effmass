"""Producer-independent reconstruction of single-band Fourier-reduction evidence."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from ksdft2effmass.model_systems import (
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicUniformGrid1D,
    PlaneWaveFiberHamiltonian1DConstructor,
)
from ksdft2effmass.solidstate import PlaneWaveBasis1D
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
)
from scipy.sparse.linalg import eigsh  # type: ignore[import-untyped]

from .definition import SingleBandFourierReductionExperimentDefinition
from .results import SingleBandFourierReductionExperimentResult


@dataclass(frozen=True, slots=True)
class SingleBandFourierReductionVerificationResult:
    """Retain quantitative defects from a separate direct reconstruction."""

    experiment_result: SingleBandFourierReductionExperimentResult
    energy_maximum_absolute_defect: ScalarQuantity
    squared_energy_maximum_absolute_defect: ScalarQuantity
    energy_absolute_tolerance: ScalarQuantity
    squared_energy_absolute_tolerance: ScalarQuantity
    structural_checks_pass: bool
    passes: bool

    def __post_init__(self) -> None:
        """Validate units, nonnegative values, and the derived disposition."""
        if (
            type(self.experiment_result)
            is not SingleBandFourierReductionExperimentResult
        ):
            raise TypeError(
                "experiment_result must be SingleBandFourierReductionExperimentResult"
            )
        energy_unit = self.experiment_result.definition.parent_model.recoil_energy.unit
        squared_unit = self.experiment_result.reduction.range_study[
            0
        ].parseval.absolute_tolerance.unit
        for name, value, unit in (
            (
                "energy_maximum_absolute_defect",
                self.energy_maximum_absolute_defect,
                energy_unit,
            ),
            (
                "squared_energy_maximum_absolute_defect",
                self.squared_energy_maximum_absolute_defect,
                squared_unit,
            ),
            ("energy_absolute_tolerance", self.energy_absolute_tolerance, energy_unit),
            (
                "squared_energy_absolute_tolerance",
                self.squared_energy_absolute_tolerance,
                squared_unit,
            ),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.unit != unit:
                raise ValueError(f"{name} has the wrong unit")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.structural_checks_pass) is not bool:
            raise TypeError("structural_checks_pass must be a built-in bool")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = (
            self.structural_checks_pass
            and self.energy_maximum_absolute_defect.magnitude
            <= self.energy_absolute_tolerance.magnitude
            and self.squared_energy_maximum_absolute_defect.magnitude
            <= self.squared_energy_absolute_tolerance.magnitude
        )
        if self.passes is not expected:
            raise ValueError("passes must match defects, tolerances, and structure")


class SingleBandFourierReductionExperimentVerifier:
    """Rebuild the finite protocol without calling the producer or Workflow Action.

    This is an independent software route, not an independent physical oracle. It
    shares NumPy, SciPy, the parent-matrix constructors, and declared conventions with
    the producer, but directly implements selection, Fourier, interpolation, weighted
    least squares, gap, locality, and diagnostic formulas.
    """

    __slots__ = ()

    def execute(
        self, result: SingleBandFourierReductionExperimentResult
    ) -> SingleBandFourierReductionVerificationResult:
        """Reconstruct every retained numerical channel and return maximum defects."""
        if type(result) is not SingleBandFourierReductionExperimentResult:
            raise TypeError("result must be SingleBandFourierReductionExperimentResult")
        definition = result.definition
        energy_defects: list[float] = []
        squared_defects: list[float] = []
        structural = True

        parent_reduced = np.asarray(
            definition.parent_sample_reduced_momenta, dtype=np.float64
        )
        reference = self._plane_wave(
            definition,
            definition.plane_wave_reference_cutoff,
            parent_reduced,
            definition.compared_band_count,
        )
        energy_defects.append(
            self._maximum(result.parent_reference.eigenvalues.magnitude, reference)
        )
        for plane_wave_observation, cutoff in zip(
            result.plane_wave_refinement, definition.plane_wave_cutoffs, strict=True
        ):
            values = self._plane_wave(
                definition, cutoff, parent_reduced, definition.compared_band_count
            )
            energy_defects.append(
                abs(
                    plane_wave_observation.maximum_absolute_error.magnitude
                    - self._maximum(values, reference)
                )
            )
        for finite_difference_observation, point_count in zip(
            result.finite_difference_refinement,
            definition.finite_difference_points,
            strict=True,
        ):
            values = self._finite_difference(
                definition,
                point_count,
                parent_reduced,
                definition.compared_band_count,
            )
            energy_defects.append(
                abs(
                    finite_difference_observation.maximum_absolute_error.magnitude
                    - self._maximum(values, reference)
                )
            )

        training_reduced = np.asarray(
            definition.training_reduced_momenta, dtype=np.float64
        )
        evaluation_reduced = np.asarray(
            definition.evaluation_reduced_momenta, dtype=np.float64
        )
        selected = definition.selected_band_index
        retained_count = selected + 2
        training_spectrum = self._plane_wave(
            definition,
            definition.production_plane_wave_cutoff,
            training_reduced,
            retained_count,
        )
        evaluation_spectrum = self._plane_wave(
            definition,
            definition.production_plane_wave_cutoff,
            evaluation_reduced,
            retained_count,
        )
        training_values = training_spectrum[:, selected]
        evaluation_values = evaluation_spectrum[:, selected]
        request = result.reduction.request
        energy_defects.extend(
            (
                self._maximum(
                    request.training_target.eigenvalues.magnitude[:, 0], training_values
                ),
                self._maximum(
                    request.evaluation_target.eigenvalues.magnitude[:, 0],
                    evaluation_values,
                ),
                abs(
                    self._required_gap(result.training_gap.external_minimum_gap)
                    - self._external_gap(training_spectrum, selected)
                ),
                abs(
                    self._required_gap(result.evaluation_gap.external_minimum_gap)
                    - self._external_gap(evaluation_spectrum, selected)
                ),
            )
        )

        complete = result.reduction.complete_transform.hopping_model
        representatives = complete.representatives
        expected_complete = self._fourier(
            training_reduced, training_values, representatives
        )
        retained_complete = self._blocks(complete.hopping_blocks)
        energy_defects.append(self._maximum(retained_complete, expected_complete))
        reconstructed = self._interpolate(
            training_reduced,
            np.asarray(representatives, dtype=np.float64),
            expected_complete,
        )
        expected_reconstruction = self._maximum(reconstructed, training_values)
        energy_defects.append(
            abs(
                result.reduction.complete_transform.reconstruction_maximum_frobenius_error
                - expected_reconstruction
            )
        )
        lookup = dict(zip(representatives, expected_complete, strict=True))
        modulus = definition.reciprocal_training_mesh_size
        hermiticity = max(
            abs(
                value
                - np.conjugate(
                    lookup[
                        next(
                            candidate
                            for candidate in representatives
                            if (candidate + representative) % modulus == 0
                        )
                    ]
                )
            )
            for representative, value in lookup.items()
        )
        energy_defects.append(
            abs(
                result.reduction.hopping_hermiticity.maximum_frobenius_defect.magnitude
                - hermiticity
            )
        )
        retained_hermiticity = result.reduction.hopping_hermiticity
        structural = structural and (
            retained_hermiticity.paired_representatives
            == tuple(sorted(representatives))
            and not retained_hermiticity.missing_opposite_representatives
        )

        weights = np.asarray(definition.fitting_weights, dtype=np.float64)
        for range_result in result.reduction.range_study:
            range_representatives = np.asarray(
                range_result.truncation.truncated.representatives, dtype=np.float64
            )
            expected_blocks = np.asarray(
                [lookup[int(value)] for value in range_representatives],
                dtype=np.complex128,
            )
            actual_blocks = self._blocks(
                range_result.truncation.truncated.hopping_blocks
            )
            energy_defects.append(self._maximum(actual_blocks, expected_blocks))
            training_candidate = self._interpolate(
                training_reduced, range_representatives, expected_blocks
            )
            evaluation_candidate = self._interpolate(
                evaluation_reduced, range_representatives, expected_blocks
            )
            energy_defects.extend(
                (
                    abs(
                        range_result.training_error.maximum_absolute_error.magnitude
                        - self._maximum(training_candidate.real, training_values)
                    ),
                    abs(
                        range_result.evaluation_error.maximum_absolute_error.magnitude
                        - self._maximum(evaluation_candidate.real, evaluation_values)
                    ),
                )
            )
            design = np.exp(
                2j * np.pi * np.outer(training_reduced, range_representatives)
            )
            square_root_weights = np.sqrt(weights)
            fitted, _, rank, singular = np.linalg.lstsq(
                design * square_root_weights[:, None],
                training_values.astype(np.complex128) * square_root_weights,
                rcond=None,
            )
            fitted_retained = self._blocks(
                range_result.direct_fit.fitted_model.hopping_blocks
            )
            energy_defects.append(self._maximum(fitted_retained, fitted))
            fitted_samples = design @ fitted
            fit_residual = fitted_samples - training_values
            energy_defects.extend(
                (
                    abs(
                        range_result.direct_fit.training_l2_frobenius_residual
                        - float(np.linalg.norm(fit_residual))
                    ),
                    abs(
                        range_result.direct_fit.training_maximum_frobenius_residual
                        - float(np.max(np.abs(fit_residual)))
                    ),
                    abs(
                        range_result.route_comparison.coefficient_l2_frobenius_defect.magnitude
                        - float(np.linalg.norm(fitted - expected_blocks))
                    ),
                    abs(
                        range_result.route_comparison.sampled_l2_frobenius_defect.magnitude
                        - float(np.linalg.norm(fitted_samples - training_candidate))
                    ),
                    abs(
                        range_result.route_comparison.sampled_maximum_frobenius_defect.magnitude
                        - float(np.max(np.abs(fitted_samples - training_candidate)))
                    ),
                )
            )
            structural = structural and range_result.direct_fit.design_rank == int(rank)
            if range_result.direct_fit.design_condition_number is None:
                structural = structural and int(rank) < len(range_representatives)
            else:
                energy_defects.append(
                    abs(
                        range_result.direct_fit.design_condition_number
                        - float(singular[0] / singular[-1])
                    )
                )
            omitted = np.asarray(
                [
                    value
                    for representative, value in lookup.items()
                    if abs(representative) > range_result.maximum_range
                ],
                dtype=np.complex128,
            )
            omitted_norm = float(np.linalg.norm(omitted))
            energy_defects.append(
                abs(range_result.truncation.omitted_block_l2_norm - omitted_norm)
            )
            training_squared = float(
                np.sum(np.square(np.abs(training_candidate - training_values)))
            )
            expected_squared = float(modulus * omitted_norm**2)
            parseval_residual = abs(training_squared - expected_squared)
            squared_defects.extend(
                (
                    abs(
                        range_result.parseval.training_squared_frobenius_residual.magnitude
                        - training_squared
                    ),
                    abs(
                        range_result.parseval.expected_squared_frobenius_residual.magnitude
                        - expected_squared
                    ),
                    abs(
                        range_result.parseval.parseval_absolute_residual.magnitude
                        - parseval_residual
                    ),
                )
            )
            curvature = np.sum(
                -np.square(2.0 * np.pi * range_representatives) * expected_blocks
            )
            maximum_imaginary = max(
                float(np.max(np.abs(evaluation_candidate.imag))),
                abs(float(curvature.imag)),
            )
            energy_defects.extend(
                (
                    abs(
                        range_result.band_shape.bandwidth.magnitude
                        - float(np.ptp(evaluation_candidate.real))
                    ),
                    abs(
                        range_result.band_shape.zone_center_curvature.magnitude
                        - float(curvature.real)
                    ),
                    abs(
                        range_result.band_shape.maximum_imaginary_residual.magnitude
                        - maximum_imaginary
                    ),
                )
            )

        energy_unit = definition.parent_model.recoil_energy.unit
        squared_unit = result.reduction.range_study[0].parseval.absolute_tolerance.unit
        energy_tolerance = definition.tolerances.reconstruction_absolute
        squared_tolerance = definition.tolerances.parseval_absolute
        maximum_energy = max(energy_defects, default=0.0)
        maximum_squared = max(squared_defects, default=0.0)
        passes = (
            structural
            and maximum_energy <= energy_tolerance.magnitude
            and maximum_squared <= squared_tolerance.magnitude
        )
        return SingleBandFourierReductionVerificationResult(
            result,
            ScalarQuantity(float(maximum_energy), energy_unit),
            ScalarQuantity(float(maximum_squared), squared_unit),
            energy_tolerance,
            squared_tolerance,
            structural,
            passes,
        )

    @staticmethod
    def _required_gap(value: ScalarQuantity | None) -> float:
        """Return a gap magnitude guaranteed by the experiment result contract."""
        if value is None:
            raise ValueError("experiment result requires a sampled external gap")
        return value.magnitude

    @staticmethod
    def _external_gap(values: np.ndarray, selected: int) -> float:
        """Return the sampled direct gap to represented neighboring bands."""
        candidates: list[float] = []
        if selected > 0:
            candidates.append(
                float(np.min(values[:, selected] - values[:, selected - 1]))
            )
        if selected + 1 < values.shape[1]:
            candidates.append(
                float(np.min(values[:, selected + 1] - values[:, selected]))
            )
        return min(candidates)

    @staticmethod
    def _fourier(
        reduced: np.ndarray, values: np.ndarray, representatives: tuple[int, ...]
    ) -> np.ndarray:
        """Apply the declared negative-exponent, one-over-N forward transform."""
        return np.asarray(
            [
                np.mean(values * np.exp(-2j * np.pi * reduced * representative))
                for representative in representatives
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _interpolate(
        reduced: np.ndarray, representatives: np.ndarray, blocks: np.ndarray
    ) -> np.ndarray:
        """Apply the declared positive-exponent, unit-normalized inverse transform."""
        return np.asarray(
            np.exp(2j * np.pi * np.outer(reduced, representatives)) @ blocks,
            dtype=np.complex128,
        )

    @staticmethod
    def _blocks(blocks: tuple[ComplexMatrixQuantity, ...]) -> np.ndarray:
        """Extract scalar complex magnitudes from validated hopping blocks."""
        return np.asarray(
            [block.magnitude[0, 0] for block in blocks], dtype=np.complex128
        )

    @staticmethod
    def _maximum(candidate: np.ndarray, reference: np.ndarray) -> float:
        """Return a maximum elementwise absolute defect."""
        return float(np.max(np.abs(candidate - reference)))

    @staticmethod
    def _plane_wave(
        definition: SingleBandFourierReductionExperimentDefinition,
        cutoff: int,
        reduced: np.ndarray,
        band_count: int,
    ) -> np.ndarray:
        """Rebuild finite plane-wave eigenvalues directly from represented matrices."""
        model = definition.parent_model
        basis = PlaneWaveBasis1D(model.reciprocal_vector, cutoff)
        constructor = PlaneWaveFiberHamiltonian1DConstructor()
        return np.asarray(
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

    @staticmethod
    def _finite_difference(
        definition: SingleBandFourierReductionExperimentDefinition,
        point_count: int,
        reduced: np.ndarray,
        band_count: int,
    ) -> np.ndarray:
        """Rebuild centered periodic finite-difference eigenvalues directly."""
        model = definition.parent_model
        grid = PeriodicUniformGrid1D(
            ScalarQuantity(0.0, model.potential.period.unit),
            model.potential.period,
            point_count,
        )
        constructor = PeriodicFiniteDifferenceFiberHamiltonian1DConstructor()
        values: list[np.ndarray] = []
        for momentum in reduced:
            matrix = constructor.execute(
                float(momentum),
                grid,
                model.potential,
                model.recoil_energy,
                model.duality_absolute_tolerance,
            ).represented_matrix.to_csr()
            values.append(
                np.sort(
                    np.asarray(
                        eigsh(
                            matrix,
                            k=band_count,
                            which="SA",
                            return_eigenvectors=False,
                            v0=np.full(
                                point_count,
                                1.0 / np.sqrt(float(point_count)),
                                dtype=np.float64,
                            ),
                        ),
                        dtype=np.float64,
                    )
                )
            )
        return np.asarray(values, dtype=np.float64)


__all__ = [
    "SingleBandFourierReductionExperimentVerifier",
    "SingleBandFourierReductionVerificationResult",
]
