"""Independent reconstruction for controlled isolated-band results."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse.linalg import eigsh  # type: ignore[import-untyped]

from ksdft2effmass.analysis.model_systems import (
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicUniformGrid1D,
    PlaneWaveFiberHamiltonian1DConstructor,
)
from ksdft2effmass.operators import ScalarQuantity
from ksdft2effmass.solid_state import PlaneWaveBasis1D

from .definition import Periodic1DIsolatedBandCalculationDefinition
from .results import Periodic1DIsolatedBandCalculationResult


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandVerificationResult:
    """Retain independently reconstructed numerical-consistency evidence.

    Passing this verifier establishes internal numerical consistency with the frozen
    calculation definition. It does not establish material validity, uncertainty,
    convergence outside the declared controls, or scientific acceptance.
    """

    calculation: Periodic1DIsolatedBandCalculationResult
    spectral_maximum_absolute_defect: ScalarQuantity
    hopping_maximum_absolute_defect: ScalarQuantity
    diagnostics_match: bool
    absolute_tolerance: ScalarQuantity
    passes: bool

    def __post_init__(self) -> None:
        """Validate units, nonnegative defects, and the derived disposition."""
        if type(self.calculation) is not Periodic1DIsolatedBandCalculationResult:
            raise TypeError(
                "calculation must be Periodic1DIsolatedBandCalculationResult"
            )
        energy_unit = self.calculation.definition.parent_model.recoil_energy.unit
        for name, value in (
            (
                "spectral_maximum_absolute_defect",
                self.spectral_maximum_absolute_defect,
            ),
            ("hopping_maximum_absolute_defect", self.hopping_maximum_absolute_defect),
            ("absolute_tolerance", self.absolute_tolerance),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.unit != energy_unit:
                raise ValueError(f"{name} must use the calculation energy unit")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.diagnostics_match) is not bool:
            raise TypeError("diagnostics_match must be a built-in bool")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = (
            self.spectral_maximum_absolute_defect.magnitude
            <= self.absolute_tolerance.magnitude
            and self.hopping_maximum_absolute_defect.magnitude
            <= self.absolute_tolerance.magnitude
            and self.diagnostics_match
        )
        if self.passes is not expected:
            raise ValueError("passes must match reconstructed defects and diagnostics")


class Periodic1DIsolatedBandResultVerifier:
    """Reconstruct an isolated-band result without invoking its producer Action."""

    __slots__ = ()

    def execute(
        self, calculation: Periodic1DIsolatedBandCalculationResult
    ) -> Periodic1DIsolatedBandVerificationResult:
        """Reconstruct spectra, Fourier blocks, and range diagnostics."""
        if type(calculation) is not Periodic1DIsolatedBandCalculationResult:
            raise TypeError(
                "calculation must be Periodic1DIsolatedBandCalculationResult"
            )
        definition = calculation.definition
        spectral_defects: list[float] = []
        parent_reduced = np.asarray(
            definition.parent_sample_reduced_momenta, dtype=np.float64
        )
        reference = self._plane_wave_eigenvalues(
            definition,
            definition.plane_wave_reference_cutoff,
            parent_reduced,
            definition.compared_band_count,
        )
        spectral_defects.append(
            self._maximum_defect(
                calculation.parent_reference.eigenvalues.magnitude, reference
            )
        )
        for plane_wave_observation, cutoff in zip(
            calculation.plane_wave_convergence,
            definition.plane_wave_cutoffs,
            strict=True,
        ):
            values = self._plane_wave_eigenvalues(
                definition,
                cutoff,
                parent_reduced,
                definition.compared_band_count,
            )
            expected_error = self._maximum_defect(values, reference)
            spectral_defects.append(
                abs(
                    plane_wave_observation.maximum_absolute_error.magnitude
                    - expected_error
                )
            )
        for finite_difference_observation, point_count in zip(
            calculation.finite_difference_convergence,
            definition.finite_difference_points,
            strict=True,
        ):
            values = self._finite_difference_eigenvalues(
                definition,
                point_count,
                parent_reduced,
                definition.compared_band_count,
            )
            expected_error = self._maximum_defect(values, reference)
            spectral_defects.append(
                abs(
                    finite_difference_observation.maximum_absolute_error.magnitude
                    - expected_error
                )
            )

        training_reduced = (
            calculation.training_target.coordinates.magnitude
            / definition.parent_model.reciprocal_vector.magnitude
        )
        training_expected = self._plane_wave_eigenvalues(
            definition,
            definition.production_plane_wave_cutoff,
            training_reduced,
            1,
        )
        withheld_reduced = (
            calculation.withheld_target.coordinates.magnitude
            / definition.parent_model.reciprocal_vector.magnitude
        )
        withheld_expected = self._plane_wave_eigenvalues(
            definition,
            definition.production_plane_wave_cutoff,
            withheld_reduced,
            1,
        )
        spectral_defects.extend(
            (
                self._maximum_defect(
                    calculation.training_target.eigenvalues.magnitude,
                    training_expected,
                ),
                self._maximum_defect(
                    calculation.withheld_target.eigenvalues.magnitude,
                    withheld_expected,
                ),
            )
        )

        representatives = calculation.complete_transform.hopping_model.representatives
        expected_hoppings = self._direct_fourier_blocks(
            training_reduced,
            training_expected[:, 0],
            representatives,
        )
        retained_hoppings = np.asarray(
            [
                block.magnitude[0, 0]
                for block in calculation.complete_transform.hopping_model.hopping_blocks
            ],
            dtype=np.complex128,
        )
        hopping_defect = self._maximum_defect(retained_hoppings, expected_hoppings)
        diagnostics_match = self._diagnostics_match(
            calculation,
            training_reduced,
            withheld_reduced,
            training_expected[:, 0],
            withheld_expected[:, 0],
        )
        tolerance = ScalarQuantity(
            definition.reconstruction_absolute_tolerance,
            definition.parent_model.recoil_energy.unit,
        )
        spectral_defect = ScalarQuantity(max(spectral_defects), tolerance.unit)
        hopping_absolute_defect = ScalarQuantity(hopping_defect, tolerance.unit)
        passes = (
            spectral_defect.magnitude <= tolerance.magnitude
            and hopping_absolute_defect.magnitude <= tolerance.magnitude
            and diagnostics_match
        )
        return Periodic1DIsolatedBandVerificationResult(
            calculation,
            spectral_defect,
            hopping_absolute_defect,
            diagnostics_match,
            tolerance,
            passes,
        )

    def _diagnostics_match(
        self,
        calculation: Periodic1DIsolatedBandCalculationResult,
        training_reduced: np.ndarray,
        withheld_reduced: np.ndarray,
        training_values: np.ndarray,
        withheld_values: np.ndarray,
    ) -> bool:
        tolerance = calculation.definition.reconstruction_absolute_tolerance
        complete = calculation.complete_transform.hopping_model
        complete_lookup = {
            representative: block.magnitude[0, 0]
            for representative, block in zip(
                complete.representatives, complete.hopping_blocks, strict=True
            )
        }
        modulus = calculation.definition.reciprocal_mesh_size
        hermiticity_defect = max(
            (
                abs(
                    value
                    - np.conjugate(
                        complete_lookup[
                            next(
                                candidate
                                for candidate in complete.representatives
                                if (candidate + representative) % modulus == 0
                            )
                        ]
                    )
                )
                for representative, value in complete_lookup.items()
            ),
            default=0.0,
        )
        diagnostics = calculation.hopping_hermiticity
        if (
            diagnostics.paired_representatives
            != tuple(sorted(complete.representatives))
            or diagnostics.missing_opposite_representatives
        ):
            return False
        if not np.isclose(
            diagnostics.maximum_frobenius_defect.magnitude,
            hermiticity_defect,
            rtol=0.0,
            atol=tolerance,
        ):
            return False
        for result in calculation.range_study:
            model = result.truncation.truncated
            representatives = np.asarray(model.representatives, dtype=np.float64)
            blocks = np.asarray(
                [block.magnitude[0, 0] for block in model.hopping_blocks],
                dtype=np.complex128,
            )
            training_candidate = self._interpolate(
                training_reduced, representatives, blocks
            )
            withheld_candidate = self._interpolate(
                withheld_reduced, representatives, blocks
            )
            if not np.isclose(
                result.training_error.maximum_absolute_error.magnitude,
                float(np.max(np.abs(training_candidate.real - training_values))),
                rtol=0.0,
                atol=tolerance,
            ):
                return False
            if not np.isclose(
                result.withheld_error.maximum_absolute_error.magnitude,
                float(np.max(np.abs(withheld_candidate.real - withheld_values))),
                rtol=0.0,
                atol=tolerance,
            ):
                return False
            design = np.exp(2j * np.pi * np.outer(training_reduced, representatives))
            fitted, _, rank, singular_values = np.linalg.lstsq(
                design,
                training_values.astype(np.complex128)[:, None],
                rcond=None,
            )
            retained_fit = np.asarray(
                [
                    block.magnitude[0, 0]
                    for block in result.direct_fit.fitted_model.hopping_blocks
                ],
                dtype=np.complex128,
            )
            if self._maximum_defect(retained_fit, fitted[:, 0]) > tolerance:
                return False
            reconstructed_fit = design @ fitted[:, 0]
            fit_residual = reconstructed_fit - training_values
            if not np.isclose(
                result.direct_fit.training_l2_frobenius_residual,
                float(np.linalg.norm(fit_residual)),
                rtol=0.0,
                atol=tolerance,
            ) or not np.isclose(
                result.direct_fit.training_maximum_frobenius_residual,
                float(np.max(np.abs(fit_residual))),
                rtol=0.0,
                atol=tolerance,
            ):
                return False
            coefficient_defect = float(np.linalg.norm(retained_fit - blocks))
            fit_samples = self._interpolate(
                training_reduced, representatives, retained_fit
            )
            sampled_defects = fit_samples - training_candidate
            route = result.direct_mediated_comparison
            if (
                not np.isclose(
                    route.coefficient_l2_frobenius_defect.magnitude,
                    coefficient_defect,
                    rtol=0.0,
                    atol=tolerance,
                )
                or not np.isclose(
                    route.sampled_l2_frobenius_defect.magnitude,
                    float(np.linalg.norm(sampled_defects)),
                    rtol=0.0,
                    atol=tolerance,
                )
                or not np.isclose(
                    route.sampled_maximum_frobenius_defect.magnitude,
                    float(np.max(np.abs(sampled_defects))),
                    rtol=0.0,
                    atol=tolerance,
                )
            ):
                return False
            expected_identified = int(rank) == len(model.representatives)
            if result.direct_fit.is_identified is not expected_identified:
                return False
            if expected_identified:
                expected_condition = float(singular_values[0] / singular_values[-1])
                retained_condition = result.direct_fit.design_condition_number
                if retained_condition is None or not np.isclose(
                    retained_condition,
                    expected_condition,
                    rtol=0.0,
                    atol=tolerance,
                ):
                    return False
            omitted = np.asarray(
                [
                    value
                    for representative, value in complete_lookup.items()
                    if abs(representative) > result.maximum_range
                ],
                dtype=np.complex128,
            )
            omitted_norm = float(np.linalg.norm(omitted))
            if not np.isclose(
                result.truncation.omitted_block_l2_norm,
                omitted_norm,
                rtol=0.0,
                atol=tolerance,
            ):
                return False
            expected_parseval = float(
                calculation.definition.reciprocal_mesh_size * omitted_norm**2
            )
            training_squared = float(
                np.sum(np.square(np.abs(training_candidate - training_values)))
            )
            parseval_absolute_residual = abs(training_squared - expected_parseval)
            if (
                not np.isclose(
                    result.parseval.training_squared_frobenius_residual.magnitude,
                    training_squared,
                    rtol=0.0,
                    atol=tolerance,
                )
                or not np.isclose(
                    result.parseval.expected_squared_frobenius_residual.magnitude,
                    expected_parseval,
                    rtol=0.0,
                    atol=tolerance,
                )
                or not np.isclose(
                    result.parseval.parseval_absolute_residual.magnitude,
                    parseval_absolute_residual,
                    rtol=0.0,
                    atol=tolerance,
                )
            ):
                return False
            expected_bandwidth = float(np.ptp(withheld_candidate.real))
            expected_curvature = float(
                np.real(np.sum(-np.square(2.0 * np.pi * representatives) * blocks))
            )
            expected_maximum_imaginary = max(
                float(np.max(np.abs(withheld_candidate.imag))),
                abs(
                    float(
                        np.imag(
                            np.sum(-np.square(2.0 * np.pi * representatives) * blocks)
                        )
                    )
                ),
            )
            if (
                not np.isclose(
                    result.band_shape.bandwidth.magnitude,
                    expected_bandwidth,
                    rtol=0.0,
                    atol=tolerance,
                )
                or not np.isclose(
                    result.band_shape.zone_center_curvature.magnitude,
                    expected_curvature,
                    rtol=0.0,
                    atol=tolerance,
                )
                or not np.isclose(
                    result.band_shape.maximum_imaginary_residual.magnitude,
                    expected_maximum_imaginary,
                    rtol=0.0,
                    atol=tolerance,
                )
            ):
                return False
        return True

    def _plane_wave_eigenvalues(
        self,
        definition: Periodic1DIsolatedBandCalculationDefinition,
        cutoff: int,
        reduced_momenta: np.ndarray,
        band_count: int,
    ) -> np.ndarray:
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
                for momentum in reduced_momenta
            ],
            dtype=np.float64,
        )

    def _finite_difference_eigenvalues(
        self,
        definition: Periodic1DIsolatedBandCalculationDefinition,
        point_count: int,
        reduced_momenta: np.ndarray,
        band_count: int,
    ) -> np.ndarray:
        model = definition.parent_model
        grid = PeriodicUniformGrid1D(
            ScalarQuantity(0.0, model.potential.period.unit),
            model.potential.period,
            point_count,
        )
        constructor = PeriodicFiniteDifferenceFiberHamiltonian1DConstructor()
        values: list[np.ndarray] = []
        for momentum in reduced_momenta:
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

    @staticmethod
    def _direct_fourier_blocks(
        reduced_coordinates: np.ndarray,
        values: np.ndarray,
        representatives: tuple[int, ...],
    ) -> np.ndarray:
        return np.asarray(
            [
                np.mean(
                    values
                    * np.exp(-2j * np.pi * reduced_coordinates * float(representative))
                )
                for representative in representatives
            ],
            dtype=np.complex128,
        )

    @staticmethod
    def _interpolate(
        reduced_coordinates: np.ndarray,
        representatives: np.ndarray,
        blocks: np.ndarray,
    ) -> np.ndarray:
        return np.asarray(
            np.exp(2j * np.pi * np.outer(reduced_coordinates, representatives))
            @ blocks,
            dtype=np.complex128,
        )

    @staticmethod
    def _maximum_defect(candidate: np.ndarray, reference: np.ndarray) -> float:
        return float(np.max(np.abs(candidate - reference)))


__all__ = [
    "Periodic1DIsolatedBandResultVerifier",
    "Periodic1DIsolatedBandVerificationResult",
]
