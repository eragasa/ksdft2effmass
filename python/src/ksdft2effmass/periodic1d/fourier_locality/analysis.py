"""Direct calculation of the compatible rank-one Fourier-locality control."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.physkit.linalg.eigen import SpectralDecomposition
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexVectorQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingModelComparator1D,
    BlockHoppingModelComparisonRequest1D,
    ScalarHermitianHoppingLeastSquaresFitRequest1D,
    ScalarHermitianHoppingLeastSquaresFitter1D,
)
from ksdft2effmass.hamiltonian import HermitianHamiltonian
from ksdft2effmass.solidstate import (
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingTruncationRequest1D,
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformRequest1D,
    ReciprocalOperatorSamples1D,
)

from .configuration import Periodic1DFourierLocalityConfiguration
from .result import (
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityEvaluationResult,
    Periodic1DFourierLocalityMeshResult,
    Periodic1DFourierLocalityRangeResult,
)


class Periodic1DFourierLocalityAnalyzer:
    """Calculate one finite rank-one Fourier-locality result without effects."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DFourierLocalityConfiguration) -> None:
        if type(request) is not Periodic1DFourierLocalityConfiguration:
            raise TypeError("request must be Periodic1DFourierLocalityConfiguration")
        self._request = request

    @property
    def request(self) -> Periodic1DFourierLocalityConfiguration:
        """Return the complete immutable Fourier-locality request."""
        return self._request

    def execute(self) -> Periodic1DFourierLocalityCalculationResult:
        """Return the complete correlated result for the bound configuration."""
        configuration = self.request
        unit = Unitless()
        reciprocal_period = ScalarQuantity(1.0, unit)
        evaluation_coordinates = VectorQuantity(
            np.asarray(
                configuration.evaluation_reduced_momenta(),
                dtype=np.float64,
            ),
            unit,
        )
        evaluation_lowest, evaluation_adjacent = self._parent_bands(
            evaluation_coordinates,
        )
        evaluation = Periodic1DFourierLocalityEvaluationResult(
            evaluation_coordinates,
            evaluation_lowest,
            evaluation_adjacent,
        )
        meshes: list[Periodic1DFourierLocalityMeshResult] = []
        for construction_size in configuration.construction_mesh_sizes:
            mesh = CenteredUniformReciprocalMesh1D(
                reciprocal_period,
                construction_size,
            )
            construction_lowest, construction_adjacent = self._parent_bands(
                mesh.coordinates,
            )
            source = self._scalar_samples(
                mesh.coordinates,
                reciprocal_period,
                construction_lowest,
            )
            transform = ReciprocalOperatorFourierTransformer1D(
                ReciprocalOperatorFourierTransformRequest1D(
                    source,
                    mesh,
                    configuration.dimensionless_absolute_tolerance,
                    configuration.energy_absolute_tolerance,
                )
            ).execute()
            complete_construction = self._scalar_vector(transform.reconstructed)
            complete_evaluation_samples = BlockHoppingInterpolator1D(
                BlockHoppingInterpolationRequest1D(
                    transform.hopping_model, evaluation_coordinates
                )
            ).execute()
            complete_evaluation = self._scalar_vector(complete_evaluation_samples)
            complete_coefficients = ComplexVectorQuantity(
                self._canonical_complex_values(
                    np.asarray(
                        [
                            block.magnitude[0, 0]
                            for block in transform.hopping_model.hopping_blocks
                        ],
                        dtype=np.complex128,
                    )
                ),
                unit,
            )
            interpolation_residual = (
                evaluation_lowest.magnitude - complete_evaluation.magnitude
            )
            interpolation_maximum = float(np.max(np.abs(interpolation_residual)))
            interpolation_rms = float(
                np.sqrt(np.mean(np.abs(interpolation_residual) ** 2))
            )
            hermiticity_maximum = self._complete_hermiticity_error(
                transform.hopping_model.representatives,
                complete_coefficients.magnitude,
                construction_size,
            )
            weights = VectorQuantity(
                np.ones(construction_size, dtype=np.float64),
                unit,
            )
            range_results: list[Periodic1DFourierLocalityRangeResult] = []
            joint_passes: list[bool] = []
            mediated_total_errors: list[float] = []
            for maximum_range in configuration.maximum_ranges:
                truncation = BlockHoppingTruncator1D(
                    BlockHoppingTruncationRequest1D(
                        transform.hopping_model, maximum_range
                    )
                ).execute()
                mediated_construction_samples = BlockHoppingInterpolator1D(
                    BlockHoppingInterpolationRequest1D(
                        truncation.truncated, mesh.coordinates
                    )
                ).execute()
                mediated_evaluation_samples = BlockHoppingInterpolator1D(
                    BlockHoppingInterpolationRequest1D(
                        truncation.truncated, evaluation_coordinates
                    )
                ).execute()
                mediated_construction = self._scalar_vector(
                    mediated_construction_samples
                )
                mediated_evaluation = self._scalar_vector(mediated_evaluation_samples)
                direct_fit = ScalarHermitianHoppingLeastSquaresFitter1D(
                    ScalarHermitianHoppingLeastSquaresFitRequest1D(
                        source, maximum_range, weights
                    )
                ).execute()
                if direct_fit.design_condition_number is None:
                    raise ValueError("direct scalar fit must be identified")
                direct_evaluation_samples = BlockHoppingInterpolator1D(
                    BlockHoppingInterpolationRequest1D(
                        direct_fit.fitted_model, evaluation_coordinates
                    )
                ).execute()
                direct_construction = self._scalar_vector(
                    direct_fit.reconstructed_training
                )
                direct_evaluation = self._scalar_vector(direct_evaluation_samples)
                route_comparison = BlockHoppingModelComparator1D(
                    BlockHoppingModelComparisonRequest1D(
                        truncation.truncated,
                        direct_fit.fitted_model,
                        mesh.coordinates,
                    )
                ).execute()
                mediated_coefficients = ComplexVectorQuantity(
                    self._canonical_complex_values(
                        np.asarray(
                            [
                                block.magnitude[0, 0]
                                for block in truncation.truncated.hopping_blocks
                            ],
                            dtype=np.complex128,
                        )
                    ),
                    unit,
                )
                direct_coefficients = ComplexVectorQuantity(
                    self._canonical_complex_values(
                        np.asarray(
                            [
                                block.magnitude[0, 0]
                                for block in direct_fit.fitted_model.hopping_blocks
                            ],
                            dtype=np.complex128,
                        )
                    ),
                    unit,
                )
                truncation_residual = (
                    complete_evaluation.magnitude - mediated_evaluation.magnitude
                )
                mediated_total_residual = (
                    evaluation_lowest.magnitude - mediated_evaluation.magnitude
                )
                direct_total_residual = (
                    evaluation_lowest.magnitude - direct_evaluation.magnitude
                )
                parseval_observed = float(
                    np.mean(
                        np.abs(
                            construction_lowest.magnitude
                            - mediated_construction.magnitude
                        )
                        ** 2
                    )
                )
                parseval_expected = truncation.omitted_block_l2_norm**2
                representatives = np.asarray(
                    truncation.truncated.representatives,
                    dtype=np.float64,
                )
                bandwidth = float(
                    np.max(mediated_evaluation.magnitude)
                    - np.min(mediated_evaluation.magnitude)
                )
                curvature = float(
                    np.real(
                        -((2.0 * np.pi) ** 2)
                        * np.sum(representatives**2 * mediated_coefficients.magnitude)
                    )
                )
                construction_imaginary = np.asarray(
                    [
                        matrix.magnitude[0, 0].imag
                        for matrix in mediated_construction_samples.matrices
                    ],
                    dtype=np.float64,
                )
                evaluation_imaginary = np.asarray(
                    [
                        matrix.magnitude[0, 0].imag
                        for matrix in mediated_evaluation_samples.matrices
                    ],
                    dtype=np.float64,
                )
                maximum_imaginary_residual = float(
                    max(
                        np.max(np.abs(construction_imaginary)),
                        np.max(np.abs(evaluation_imaginary)),
                    )
                )
                mediated_total_maximum = float(np.max(np.abs(mediated_total_residual)))
                direct_total_maximum = float(np.max(np.abs(direct_total_residual)))
                range_results.append(
                    Periodic1DFourierLocalityRangeResult(
                        maximum_range=maximum_range,
                        mediated_coefficients=mediated_coefficients,
                        direct_coefficients=direct_coefficients,
                        mediated_construction_candidate=mediated_construction,
                        mediated_evaluation_candidate=mediated_evaluation,
                        direct_construction_candidate=direct_construction,
                        direct_evaluation_candidate=direct_evaluation,
                        truncation_maximum_error=ScalarQuantity(
                            float(np.max(np.abs(truncation_residual))),
                            unit,
                        ),
                        truncation_rms_error=ScalarQuantity(
                            float(np.sqrt(np.mean(np.abs(truncation_residual) ** 2))),
                            unit,
                        ),
                        mediated_total_maximum_error=ScalarQuantity(
                            mediated_total_maximum,
                            unit,
                        ),
                        mediated_total_rms_error=ScalarQuantity(
                            float(
                                np.sqrt(np.mean(np.abs(mediated_total_residual) ** 2))
                            ),
                            unit,
                        ),
                        direct_total_maximum_error=ScalarQuantity(
                            direct_total_maximum,
                            unit,
                        ),
                        direct_total_rms_error=ScalarQuantity(
                            float(np.sqrt(np.mean(np.abs(direct_total_residual) ** 2))),
                            unit,
                        ),
                        omitted_coefficient_l2_norm=ScalarQuantity(
                            truncation.omitted_block_l2_norm,
                            unit,
                        ),
                        parseval_observed_squared_residual=ScalarQuantity(
                            parseval_observed,
                            unit,
                        ),
                        parseval_expected_squared_residual=ScalarQuantity(
                            parseval_expected,
                            unit,
                        ),
                        parseval_absolute_residual=ScalarQuantity(
                            abs(parseval_observed - parseval_expected),
                            unit,
                        ),
                        direct_design_rank=direct_fit.design_rank,
                        direct_design_condition_number=(
                            direct_fit.design_condition_number
                        ),
                        direct_training_l2_residual=ScalarQuantity(
                            direct_fit.training_l2_frobenius_residual,
                            unit,
                        ),
                        direct_training_maximum_residual=ScalarQuantity(
                            direct_fit.training_maximum_frobenius_residual,
                            unit,
                        ),
                        coefficient_l2_defect=(
                            route_comparison.coefficient_l2_frobenius_defect
                        ),
                        sampled_l2_defect=(
                            route_comparison.sampled_l2_frobenius_defect
                        ),
                        sampled_maximum_defect=(
                            route_comparison.sampled_maximum_frobenius_defect
                        ),
                        bandwidth=ScalarQuantity(bandwidth, unit),
                        zone_center_curvature=ScalarQuantity(curvature, unit),
                        maximum_imaginary_residual=ScalarQuantity(
                            maximum_imaginary_residual,
                            unit,
                        ),
                    )
                )
                mediated_total_errors.append(mediated_total_maximum)
                joint_passes.append(
                    mediated_total_maximum <= configuration.application_threshold
                    and direct_total_maximum <= configuration.application_threshold
                )
            nondominated_mask = self._nondominated_mask(
                configuration.maximum_ranges,
                tuple(mediated_total_errors),
            )
            near_tie_mask = self._near_tie_mask(
                nondominated_mask,
                tuple(mediated_total_errors),
                configuration.energy_absolute_tolerance,
                configuration.relative_tolerance,
            )
            passing_ranges = tuple(
                maximum_range
                for maximum_range, passes in zip(
                    configuration.maximum_ranges,
                    joint_passes,
                    strict=True,
                )
                if passes
            )
            first_joint_pass = passing_ranges[0] if passing_ranges else None
            sustained = first_joint_pass is not None and all(
                passes
                for maximum_range, passes in zip(
                    configuration.maximum_ranges,
                    joint_passes,
                    strict=True,
                )
                if maximum_range >= first_joint_pass
            )
            meshes.append(
                Periodic1DFourierLocalityMeshResult(
                    construction_size=construction_size,
                    construction_reduced_momenta=mesh.coordinates,
                    lowest_energies=construction_lowest,
                    adjacent_energies=construction_adjacent,
                    complete_coefficients=complete_coefficients,
                    reconstructed_construction=complete_construction,
                    complete_evaluation_candidate=complete_evaluation,
                    reconstruction_maximum_error=ScalarQuantity(
                        transform.reconstruction_maximum_frobenius_error,
                        unit,
                    ),
                    hermiticity_maximum_error=ScalarQuantity(
                        hermiticity_maximum,
                        unit,
                    ),
                    interpolation_maximum_error=ScalarQuantity(
                        interpolation_maximum,
                        unit,
                    ),
                    interpolation_rms_error=ScalarQuantity(
                        interpolation_rms,
                        unit,
                    ),
                    ranges=tuple(range_results),
                    nondominated_mask=nondominated_mask,
                    near_tie_mask=near_tie_mask,
                    first_joint_pass=first_joint_pass,
                    sustained_after_first_pass=sustained,
                )
            )
        refinement_channel_names = configuration.refinement_channel_names()
        normalized_refinement_changes = MatrixQuantity(
            np.vstack(
                [
                    np.abs(fine.refinement_vector() - coarse.refinement_vector())
                    for coarse, fine in zip(meshes[:-1], meshes[1:], strict=True)
                ]
            ),
            unit,
        )
        production = meshes[-1]
        production_gaps = (
            production.adjacent_energies.magnitude
            - production.lowest_energies.magnitude
        )
        evaluation_gaps = evaluation.sampled_gaps.magnitude
        construction_index = int(np.argmin(production_gaps))
        evaluation_index = int(np.argmin(evaluation_gaps))
        construction_gap = float(production_gaps[construction_index])
        evaluation_gap = float(evaluation_gaps[evaluation_index])
        if construction_gap <= evaluation_gap:
            minimum_gap = construction_gap
            gap_role = "construction"
            gap_index = construction_index
            gap_momentum = float(
                production.construction_reduced_momenta.magnitude[construction_index]
            )
        else:
            minimum_gap = evaluation_gap
            gap_role = "evaluation"
            gap_index = evaluation_index
            gap_momentum = float(evaluation.reduced_momenta.magnitude[evaluation_index])
        return Periodic1DFourierLocalityCalculationResult(
            calculation_family="periodic1d-rank1-fourier-locality",
            configuration=configuration,
            evaluation=evaluation,
            meshes=tuple(meshes),
            refinement_channel_names=refinement_channel_names,
            normalized_refinement_changes=normalized_refinement_changes,
            refinement_coarse_first_passes=tuple(
                mesh.first_joint_pass for mesh in meshes[:-1]
            ),
            refinement_fine_first_passes=tuple(
                mesh.first_joint_pass for mesh in meshes[1:]
            ),
            minimum_sampled_gap=ScalarQuantity(minimum_gap, unit),
            gap_minimizing_role=gap_role,
            gap_minimizing_index=gap_index,
            gap_minimizing_reduced_momentum=ScalarQuantity(gap_momentum, unit),
        )

    def _parent_bands(
        self,
        coordinates: VectorQuantity,
    ) -> tuple[VectorQuantity, VectorQuantity]:
        configuration = self.request
        denominator = float(configuration.coefficient_denominator)
        onsite = (
            np.asarray(
                configuration.onsite_numerators,
                dtype=np.complex128,
            )
            / denominator
        )
        positive_hopping = (
            np.asarray(
                configuration.positive_hopping_numerators,
                dtype=np.complex128,
            )
            / denominator
        )
        lowest: list[float] = []
        adjacent: list[float] = []
        for coordinate in coordinates.magnitude:
            phase = np.exp(2j * np.pi * coordinate)
            represented = (
                onsite
                + phase * positive_hopping
                + phase.conjugate() * positive_hopping.conj().T
            )
            symmetric = 0.5 * (represented + represented.conj().T)
            upper = np.triu(symmetric)
            represented = upper + np.triu(symmetric, 1).conj().T
            hamiltonian = HermitianHamiltonian(
                matrix=ComplexMatrixQuantity(represented, Unitless())
            )
            eigensystem = SpectralDecomposition(hamiltonian.matrix).eigensystem(2)
            lowest.append(float(eigensystem.eigenvalues.magnitude[0]))
            adjacent.append(float(eigensystem.eigenvalues.magnitude[1]))
        return (
            VectorQuantity(np.asarray(lowest, dtype=np.float64), Unitless()),
            VectorQuantity(np.asarray(adjacent, dtype=np.float64), Unitless()),
        )

    def _scalar_samples(
        self,
        coordinates: VectorQuantity,
        reciprocal_period: ScalarQuantity,
        values: VectorQuantity,
    ) -> ReciprocalOperatorSamples1D:
        return ReciprocalOperatorSamples1D(
            coordinates,
            reciprocal_period,
            tuple(
                ComplexMatrixQuantity(
                    np.asarray([[value]], dtype=np.complex128),
                    values.unit,
                )
                for value in values.magnitude
            ),
        )

    def _scalar_vector(self, samples: ReciprocalOperatorSamples1D) -> VectorQuantity:
        return VectorQuantity(
            np.asarray(
                [float(matrix.magnitude[0, 0].real) for matrix in samples.matrices],
                dtype=np.float64,
            ),
            samples.matrices[0].unit,
        )

    def _canonical_complex_values(self, values: Complex128Array) -> Complex128Array:
        canonical = np.asarray(
            np.where(values.real == 0.0, 0.0, values.real),
            dtype=np.complex128,
        )
        canonical.imag = np.where(values.imag == 0.0, 0.0, values.imag)
        return canonical

    def _complete_hermiticity_error(
        self,
        representatives: tuple[int, ...],
        coefficients: Complex128Array,
        construction_size: int,
    ) -> float:
        lookup = dict(zip(representatives, coefficients, strict=True))
        maximum_error = 0.0
        for representative, coefficient in lookup.items():
            opposite = (
                (-representative + construction_size // 2) % construction_size
            ) - construction_size // 2
            maximum_error = max(
                maximum_error,
                float(abs(coefficient - np.conjugate(lookup[opposite]))),
            )
        return maximum_error

    def _nondominated_mask(
        self,
        maximum_ranges: tuple[int, ...],
        errors: tuple[float, ...],
    ) -> tuple[bool, ...]:
        return tuple(
            not any(
                other_index != candidate_index
                and 2 * maximum_ranges[other_index] + 1
                <= 2 * maximum_ranges[candidate_index] + 1
                and errors[other_index] <= errors[candidate_index]
                and (
                    maximum_ranges[other_index] < maximum_ranges[candidate_index]
                    or errors[other_index] < errors[candidate_index]
                )
                for other_index in range(len(maximum_ranges))
            )
            for candidate_index in range(len(maximum_ranges))
        )

    def _near_tie_mask(
        self,
        nondominated_mask: tuple[bool, ...],
        errors: tuple[float, ...],
        absolute_tolerance: float,
        relative_tolerance: float,
    ) -> tuple[bool, ...]:
        return tuple(
            nondominated_mask[candidate_index]
            and any(
                other_index != candidate_index
                and nondominated_mask[other_index]
                and abs(errors[candidate_index] - errors[other_index])
                <= absolute_tolerance
                + relative_tolerance
                * max(
                    abs(errors[candidate_index]),
                    abs(errors[other_index]),
                )
                for other_index in range(len(errors))
            )
            for candidate_index in range(len(errors))
        )
