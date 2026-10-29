"""Independent numerical reconstruction for rank-one Fourier locality."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.units import (
    ComplexVectorQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from .result import Periodic1DFourierLocalityCalculationResult
from .visualizations.data import Periodic1DFourierLocalityVisualizationData


@dataclass(frozen=True, slots=True)
class Periodic1DFourierLocalityIndependentReference:
    """Retain collision-free comparisons reconstructed without production actions."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not isinstance(self.comparisons, Mapping) or not self.comparisons:
            raise TypeError("comparisons must be a nonempty mapping")
        if any(
            type(name) is not str
            or not name
            or not isinstance(value, MaximumAbsoluteErrorComparison)
            for name, value in self.comparisons.items()
        ):
            raise TypeError("comparisons must contain named comparison values")
        object.__setattr__(
            self,
            "comparisons",
            MappingProxyType(dict(self.comparisons)),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DFourierLocalityIndependentReferenceRequest:
    """Bind the admitted result and exact verifier-derived projection."""

    result: Periodic1DFourierLocalityCalculationResult
    visualization_data: Periodic1DFourierLocalityVisualizationData

    def __post_init__(self) -> None:
        """Admit exact rank-one verification subject types."""
        if type(self.result) is not Periodic1DFourierLocalityCalculationResult:
            raise TypeError("result must be Periodic1DFourierLocalityCalculationResult")
        if type(self.visualization_data) is not (
            Periodic1DFourierLocalityVisualizationData
        ):
            raise TypeError(
                "visualization_data must be Fourier-locality visualization data"
            )


class Periodic1DFourierLocalityIndependentReferenceAnalyzer:
    """Reconstruct one bound result and projection with direct NumPy formulas."""

    __slots__ = ("_request",)

    def __init__(
        self, request: Periodic1DFourierLocalityIndependentReferenceRequest
    ) -> None:
        if type(request) is not Periodic1DFourierLocalityIndependentReferenceRequest:
            raise TypeError(
                "request must be Periodic1DFourierLocalityIndependentReferenceRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DFourierLocalityIndependentReferenceRequest:
        """Return the complete immutable reference request."""
        return self._request

    def execute(self) -> Periodic1DFourierLocalityIndependentReference:
        """Return independent comparisons for the bound result and projection."""
        result = self.request.result
        configuration = result.configuration
        unit = Unitless()
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}
        expected_evaluation_coordinates = np.asarray(
            configuration.evaluation_reduced_momenta(),
            dtype=np.float64,
        )
        self._add(
            comparisons,
            "evaluation_reduced_momenta",
            result.evaluation.reduced_momenta,
            VectorQuantity(expected_evaluation_coordinates, unit),
            0.0,
            0.0,
        )
        parent_identity_is_bound = (
            configuration.parent_identity == configuration.PARENT_IDENTITY
            and configuration.onsite_numerators
            == configuration.PARENT_ONSITE_NUMERATORS
            and configuration.positive_hopping_numerators
            == configuration.PARENT_POSITIVE_HOPPING_NUMERATORS
            and configuration.coefficient_denominator
            == configuration.PARENT_COEFFICIENT_DENOMINATOR
        )
        self._add(
            comparisons,
            "parent_identity_binding",
            ScalarQuantity(0.0 if parent_identity_is_bound else 1.0, unit),
            ScalarQuantity(0.0, unit),
            0.0,
            0.0,
        )
        evaluation_lowest, evaluation_adjacent = self._parent_bands(
            result.evaluation.reduced_momenta.magnitude,
        )
        self._add(
            comparisons,
            "evaluation_lowest_energies",
            result.evaluation.lowest_energies,
            VectorQuantity(evaluation_lowest, unit),
            configuration.energy_absolute_tolerance,
            configuration.relative_tolerance,
        )
        self._add(
            comparisons,
            "evaluation_adjacent_energies",
            result.evaluation.adjacent_energies,
            VectorQuantity(evaluation_adjacent, unit),
            configuration.energy_absolute_tolerance,
            configuration.relative_tolerance,
        )
        self._add(
            comparisons,
            "refinement_channel_names",
            ScalarQuantity(
                0.0
                if result.refinement_channel_names
                == configuration.refinement_channel_names()
                else 1.0,
                unit,
            ),
            ScalarQuantity(0.0, unit),
            0.0,
            0.0,
        )
        expected_refinement_vectors: list[np.ndarray] = []
        expected_first_passes: list[int | None] = []
        expected_sustained_passages: list[bool] = []
        for mesh in result.meshes:
            prefix = f"mesh_{mesh.construction_size}"
            coordinates = mesh.construction_reduced_momenta.magnitude
            lowest, adjacent = self._parent_bands(coordinates)
            self._add(
                comparisons,
                f"{prefix}_lowest_energies",
                mesh.lowest_energies,
                VectorQuantity(lowest, unit),
                configuration.energy_absolute_tolerance,
                configuration.relative_tolerance,
            )
            self._add(
                comparisons,
                f"{prefix}_adjacent_energies",
                mesh.adjacent_energies,
                VectorQuantity(adjacent, unit),
                configuration.energy_absolute_tolerance,
                configuration.relative_tolerance,
            )
            representatives = np.asarray(
                mesh.complete_representatives,
                dtype=np.float64,
            )
            complete_design = np.exp(
                -2j * np.pi * np.outer(representatives, coordinates)
            )
            complete_coefficients = complete_design @ lowest / mesh.construction_size
            construction_candidate = (
                np.exp(2j * np.pi * np.outer(coordinates, representatives))
                @ complete_coefficients
            )
            evaluation_candidate = (
                np.exp(
                    2j
                    * np.pi
                    * np.outer(
                        result.evaluation.reduced_momenta.magnitude,
                        representatives,
                    )
                )
                @ complete_coefficients
            )
            self._add(
                comparisons,
                f"{prefix}_complete_coefficients",
                mesh.complete_coefficients,
                ComplexVectorQuantity(complete_coefficients, unit),
                configuration.energy_absolute_tolerance,
                configuration.relative_tolerance,
            )
            self._add(
                comparisons,
                f"{prefix}_complete_construction_candidate",
                mesh.reconstructed_construction,
                VectorQuantity(construction_candidate.real, unit),
                configuration.energy_absolute_tolerance,
                configuration.relative_tolerance,
            )
            self._add(
                comparisons,
                f"{prefix}_complete_evaluation_candidate",
                mesh.complete_evaluation_candidate,
                VectorQuantity(evaluation_candidate.real, unit),
                configuration.energy_absolute_tolerance,
                configuration.relative_tolerance,
            )
            reconstruction_error = float(
                np.max(np.abs(lowest - construction_candidate.real))
            )
            interpolation_residual = evaluation_lowest - evaluation_candidate.real
            interpolation_maximum = float(np.max(np.abs(interpolation_residual)))
            interpolation_rms = float(
                np.sqrt(np.mean(np.abs(interpolation_residual) ** 2))
            )
            complete_lookup = dict(
                zip(mesh.complete_representatives, complete_coefficients, strict=True)
            )
            hermiticity_error = 0.0
            for representative, coefficient in complete_lookup.items():
                opposite = (
                    (-representative + mesh.construction_size // 2)
                    % mesh.construction_size
                ) - mesh.construction_size // 2
                hermiticity_error = max(
                    hermiticity_error,
                    float(abs(coefficient - np.conjugate(complete_lookup[opposite]))),
                )
            mesh_summaries = VectorQuantity(
                np.asarray(
                    [
                        reconstruction_error,
                        hermiticity_error,
                        interpolation_maximum,
                        interpolation_rms,
                    ],
                    dtype=np.float64,
                ),
                unit,
            )
            self._add(
                comparisons,
                f"{prefix}_complete_diagnostics",
                VectorQuantity(
                    np.asarray(
                        [
                            mesh.reconstruction_maximum_error.magnitude,
                            mesh.hermiticity_maximum_error.magnitude,
                            mesh.interpolation_maximum_error.magnitude,
                            mesh.interpolation_rms_error.magnitude,
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
                mesh_summaries,
                configuration.energy_absolute_tolerance,
                configuration.relative_tolerance,
            )
            refinement_values = [interpolation_maximum, interpolation_rms]
            mediated_total_errors: list[float] = []
            direct_total_errors: list[float] = []
            joint_passes: list[bool] = []
            maximum_triangle_violations: list[float] = []
            rms_triangle_violations: list[float] = []
            for range_result in mesh.ranges:
                range_prefix = f"{prefix}_range_{range_result.maximum_range}"
                support = np.asarray(range_result.representatives, dtype=np.float64)
                mediated_coefficients = np.asarray(
                    [complete_lookup[value] for value in range_result.representatives],
                    dtype=np.complex128,
                )
                construction_phases = np.exp(
                    2j * np.pi * np.outer(coordinates, support)
                )
                evaluation_phases = np.exp(
                    2j
                    * np.pi
                    * np.outer(
                        result.evaluation.reduced_momenta.magnitude,
                        support,
                    )
                )
                mediated_construction = construction_phases @ mediated_coefficients
                mediated_evaluation = evaluation_phases @ mediated_coefficients
                direct_design = [np.ones(mesh.construction_size, dtype=np.float64)]
                for representative in range(1, range_result.maximum_range + 1):
                    phases = 2.0 * np.pi * representative * coordinates
                    direct_design.extend((2.0 * np.cos(phases), -2.0 * np.sin(phases)))
                direct_matrix = np.column_stack(direct_design)
                parameters, _, direct_rank, singular_values = np.linalg.lstsq(
                    direct_matrix,
                    lowest,
                    rcond=None,
                )
                direct_by_representative: dict[int, complex] = {
                    0: complex(float(parameters[0]), 0.0)
                }
                for representative in range(1, range_result.maximum_range + 1):
                    index = 2 * representative - 1
                    positive = complex(
                        float(parameters[index]),
                        float(parameters[index + 1]),
                    )
                    direct_by_representative[representative] = positive
                    direct_by_representative[-representative] = positive.conjugate()
                direct_coefficients = np.asarray(
                    [
                        direct_by_representative[value]
                        for value in range_result.representatives
                    ],
                    dtype=np.complex128,
                )
                direct_construction = construction_phases @ direct_coefficients
                direct_evaluation = evaluation_phases @ direct_coefficients
                for route, observed, expected in (
                    (
                        "mediated_coefficients",
                        range_result.mediated_coefficients,
                        ComplexVectorQuantity(mediated_coefficients, unit),
                    ),
                    (
                        "direct_coefficients",
                        range_result.direct_coefficients,
                        ComplexVectorQuantity(direct_coefficients, unit),
                    ),
                    (
                        "mediated_construction",
                        range_result.mediated_construction_candidate,
                        VectorQuantity(mediated_construction.real, unit),
                    ),
                    (
                        "mediated_evaluation",
                        range_result.mediated_evaluation_candidate,
                        VectorQuantity(mediated_evaluation.real, unit),
                    ),
                    (
                        "direct_construction",
                        range_result.direct_construction_candidate,
                        VectorQuantity(direct_construction.real, unit),
                    ),
                    (
                        "direct_evaluation",
                        range_result.direct_evaluation_candidate,
                        VectorQuantity(direct_evaluation.real, unit),
                    ),
                ):
                    self._add(
                        comparisons,
                        f"{range_prefix}_{route}",
                        observed,
                        expected,
                        configuration.energy_absolute_tolerance,
                        configuration.relative_tolerance,
                    )
                truncation_residual = (
                    evaluation_candidate.real - mediated_evaluation.real
                )
                mediated_total_residual = evaluation_lowest - mediated_evaluation.real
                direct_total_residual = evaluation_lowest - direct_evaluation.real
                training_residual = direct_construction.real - lowest
                coefficient_defect = direct_coefficients - mediated_coefficients
                sampled_defect = direct_construction.real - mediated_construction.real
                omitted = np.asarray(
                    [
                        coefficient
                        for representative, coefficient in complete_lookup.items()
                        if representative not in range_result.representatives
                    ],
                    dtype=np.complex128,
                )
                omitted_norm = float(np.linalg.norm(omitted))
                parseval_observed = float(
                    np.mean(np.abs(lowest - mediated_construction.real) ** 2)
                )
                parseval_expected = omitted_norm**2
                condition = float(singular_values[0] / singular_values[-1])
                bandwidth = float(
                    np.max(mediated_evaluation.real) - np.min(mediated_evaluation.real)
                )
                curvature = float(
                    np.real(
                        -((2.0 * np.pi) ** 2)
                        * np.sum((support**2) * mediated_coefficients)
                    )
                )
                diagnostics = np.asarray(
                    [
                        np.max(np.abs(truncation_residual)),
                        np.sqrt(np.mean(np.abs(truncation_residual) ** 2)),
                        np.max(np.abs(mediated_total_residual)),
                        np.sqrt(np.mean(np.abs(mediated_total_residual) ** 2)),
                        np.max(np.abs(direct_total_residual)),
                        np.sqrt(np.mean(np.abs(direct_total_residual) ** 2)),
                        omitted_norm,
                        np.linalg.norm(training_residual),
                        np.max(np.abs(training_residual)),
                        np.linalg.norm(coefficient_defect),
                        np.linalg.norm(sampled_defect),
                        np.max(np.abs(sampled_defect)),
                        bandwidth,
                        curvature,
                        max(
                            np.max(np.abs(mediated_construction.imag)),
                            np.max(np.abs(mediated_evaluation.imag)),
                        ),
                    ],
                    dtype=np.float64,
                )
                mediated_total_errors.append(float(diagnostics[2]))
                direct_total_errors.append(float(diagnostics[4]))
                joint_passes.append(
                    diagnostics[2] <= configuration.application_threshold
                    and diagnostics[4] <= configuration.application_threshold
                )
                maximum_triangle_violations.append(
                    max(
                        0.0,
                        float(diagnostics[2] - interpolation_maximum - diagnostics[0]),
                    )
                )
                rms_triangle_violations.append(
                    max(
                        0.0,
                        float(diagnostics[3] - interpolation_rms - diagnostics[1]),
                    )
                )
                observed_diagnostics = VectorQuantity(
                    np.asarray(
                        [
                            range_result.truncation_maximum_error.magnitude,
                            range_result.truncation_rms_error.magnitude,
                            range_result.mediated_total_maximum_error.magnitude,
                            range_result.mediated_total_rms_error.magnitude,
                            range_result.direct_total_maximum_error.magnitude,
                            range_result.direct_total_rms_error.magnitude,
                            range_result.omitted_coefficient_l2_norm.magnitude,
                            range_result.direct_training_l2_residual.magnitude,
                            range_result.direct_training_maximum_residual.magnitude,
                            range_result.coefficient_l2_defect.magnitude,
                            range_result.sampled_l2_defect.magnitude,
                            range_result.sampled_maximum_defect.magnitude,
                            range_result.bandwidth.magnitude,
                            range_result.zone_center_curvature.magnitude,
                            range_result.maximum_imaginary_residual.magnitude,
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                )
                self._add(
                    comparisons,
                    f"{range_prefix}_diagnostics",
                    observed_diagnostics,
                    VectorQuantity(diagnostics, unit),
                    configuration.energy_absolute_tolerance,
                    configuration.relative_tolerance,
                )
                squared = np.asarray(
                    [
                        parseval_observed,
                        parseval_expected,
                        abs(parseval_observed - parseval_expected),
                    ],
                    dtype=np.float64,
                )
                self._add(
                    comparisons,
                    f"{range_prefix}_parseval",
                    VectorQuantity(
                        np.asarray(
                            [
                                range_result.parseval_observed_squared_residual.magnitude,
                                range_result.parseval_expected_squared_residual.magnitude,
                                range_result.parseval_absolute_residual.magnitude,
                            ],
                            dtype=np.float64,
                        ),
                        unit,
                    ),
                    VectorQuantity(squared, unit),
                    configuration.squared_energy_absolute_tolerance,
                    configuration.relative_tolerance,
                )
                self._add(
                    comparisons,
                    f"{range_prefix}_design_rank",
                    ScalarQuantity(float(range_result.direct_design_rank), unit),
                    ScalarQuantity(float(direct_rank), unit),
                    0.0,
                    0.0,
                )
                self._add(
                    comparisons,
                    f"{range_prefix}_design_condition",
                    ScalarQuantity(
                        range_result.direct_design_condition_number,
                        unit,
                    ),
                    ScalarQuantity(condition, unit),
                    configuration.dimensionless_absolute_tolerance,
                    configuration.relative_tolerance,
                )
                refinement_values.extend(
                    (
                        diagnostics[0],
                        diagnostics[1],
                        diagnostics[2],
                        diagnostics[3],
                        diagnostics[4],
                        diagnostics[5],
                        diagnostics[6],
                        diagnostics[9],
                        diagnostics[10],
                        diagnostics[11],
                    )
                )
            expected_nondominated = tuple(
                not any(
                    other_index != candidate_index
                    and mesh.ranges[other_index].maximum_range
                    <= mesh.ranges[candidate_index].maximum_range
                    and mediated_total_errors[other_index]
                    <= mediated_total_errors[candidate_index]
                    and (
                        mesh.ranges[other_index].maximum_range
                        < mesh.ranges[candidate_index].maximum_range
                        or mediated_total_errors[other_index]
                        < mediated_total_errors[candidate_index]
                    )
                    for other_index in range(len(mesh.ranges))
                )
                for candidate_index in range(len(mesh.ranges))
            )
            expected_near_tie = tuple(
                expected_nondominated[candidate_index]
                and any(
                    other_index != candidate_index
                    and expected_nondominated[other_index]
                    and abs(
                        mediated_total_errors[candidate_index]
                        - mediated_total_errors[other_index]
                    )
                    <= configuration.energy_absolute_tolerance
                    + configuration.relative_tolerance
                    * max(
                        abs(mediated_total_errors[candidate_index]),
                        abs(mediated_total_errors[other_index]),
                    )
                    for other_index in range(len(mesh.ranges))
                )
                for candidate_index in range(len(mesh.ranges))
            )
            passing_ranges = tuple(
                range_result.maximum_range
                for range_result, passes in zip(
                    mesh.ranges,
                    joint_passes,
                    strict=True,
                )
                if passes
            )
            expected_first = passing_ranges[0] if passing_ranges else None
            expected_sustained = expected_first is not None and all(
                passes
                for range_result, passes in zip(
                    mesh.ranges,
                    joint_passes,
                    strict=True,
                )
                if range_result.maximum_range >= expected_first
            )
            expected_first_passes.append(expected_first)
            expected_sustained_passages.append(expected_sustained)
            self._add(
                comparisons,
                f"{prefix}_nondominated_mask",
                VectorQuantity(
                    np.asarray(mesh.nondominated_mask, dtype=np.float64), unit
                ),
                VectorQuantity(
                    np.asarray(expected_nondominated, dtype=np.float64), unit
                ),
                0.0,
                0.0,
            )
            self._add(
                comparisons,
                f"{prefix}_near_tie_mask",
                VectorQuantity(np.asarray(mesh.near_tie_mask, dtype=np.float64), unit),
                VectorQuantity(np.asarray(expected_near_tie, dtype=np.float64), unit),
                0.0,
                0.0,
            )
            self._add(
                comparisons,
                f"{prefix}_first_joint_pass",
                ScalarQuantity(
                    float(
                        -1 if mesh.first_joint_pass is None else mesh.first_joint_pass
                    ),
                    unit,
                ),
                ScalarQuantity(
                    float(-1 if expected_first is None else expected_first), unit
                ),
                0.0,
                0.0,
            )
            self._add(
                comparisons,
                f"{prefix}_sustained_after_first_pass",
                ScalarQuantity(float(mesh.sustained_after_first_pass), unit),
                ScalarQuantity(float(expected_sustained), unit),
                0.0,
                0.0,
            )
            self._add(
                comparisons,
                f"{prefix}_maximum_triangle",
                VectorQuantity(
                    np.asarray(maximum_triangle_violations, dtype=np.float64), unit
                ),
                VectorQuantity(np.zeros(len(mesh.ranges), dtype=np.float64), unit),
                configuration.energy_absolute_tolerance,
                0.0,
            )
            self._add(
                comparisons,
                f"{prefix}_rms_triangle",
                VectorQuantity(
                    np.asarray(rms_triangle_violations, dtype=np.float64), unit
                ),
                VectorQuantity(np.zeros(len(mesh.ranges), dtype=np.float64), unit),
                configuration.energy_absolute_tolerance,
                0.0,
            )
            expected_refinement_vectors.append(
                np.asarray(refinement_values, dtype=np.float64)
            )
        expected_changes = np.vstack(
            [
                np.abs(fine - coarse)
                for coarse, fine in zip(
                    expected_refinement_vectors[:-1],
                    expected_refinement_vectors[1:],
                    strict=True,
                )
            ]
        )
        self._add(
            comparisons,
            "normalized_refinement_changes",
            result.normalized_refinement_changes,
            MatrixQuantity(expected_changes, unit),
            configuration.dimensionless_absolute_tolerance,
            0.0,
        )
        expected_coarse = expected_first_passes[:-1]
        expected_fine = expected_first_passes[1:]
        self._add(
            comparisons,
            "refinement_coarse_first_passes",
            VectorQuantity(
                np.asarray(
                    [
                        -1 if value is None else value
                        for value in result.refinement_coarse_first_passes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            VectorQuantity(
                np.asarray(
                    [-1 if value is None else value for value in expected_coarse],
                    dtype=np.float64,
                ),
                unit,
            ),
            0.0,
            0.0,
        )
        self._add(
            comparisons,
            "refinement_fine_first_passes",
            VectorQuantity(
                np.asarray(
                    [
                        -1 if value is None else value
                        for value in result.refinement_fine_first_passes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            VectorQuantity(
                np.asarray(
                    [-1 if value is None else value for value in expected_fine],
                    dtype=np.float64,
                ),
                unit,
            ),
            0.0,
            0.0,
        )
        production = result.meshes[-1]
        production_lowest, production_adjacent = self._parent_bands(
            production.construction_reduced_momenta.magnitude,
        )
        production_gaps = production_adjacent - production_lowest
        evaluation_gaps = evaluation_adjacent - evaluation_lowest
        construction_index = int(np.argmin(production_gaps))
        evaluation_index = int(np.argmin(evaluation_gaps))
        if production_gaps[construction_index] <= evaluation_gaps[evaluation_index]:
            expected_gap = float(production_gaps[construction_index])
            expected_gap_role = "construction"
            expected_gap_index = construction_index
            expected_gap_momentum = float(
                production.construction_reduced_momenta.magnitude[construction_index]
            )
        else:
            expected_gap = float(evaluation_gaps[evaluation_index])
            expected_gap_role = "evaluation"
            expected_gap_index = evaluation_index
            expected_gap_momentum = float(
                expected_evaluation_coordinates[evaluation_index]
            )
        self._add(
            comparisons,
            "minimum_sampled_gap",
            result.minimum_sampled_gap,
            ScalarQuantity(expected_gap, unit),
            configuration.energy_absolute_tolerance,
            configuration.relative_tolerance,
        )
        self._add(
            comparisons,
            "gap_minimizing_role",
            ScalarQuantity(
                0.0 if result.gap_minimizing_role == expected_gap_role else 1.0,
                unit,
            ),
            ScalarQuantity(0.0, unit),
            0.0,
            0.0,
        )
        self._add(
            comparisons,
            "gap_minimizing_index",
            ScalarQuantity(float(result.gap_minimizing_index), unit),
            ScalarQuantity(float(expected_gap_index), unit),
            0.0,
            0.0,
        )
        self._add(
            comparisons,
            "gap_minimizing_reduced_momentum",
            result.gap_minimizing_reduced_momentum,
            ScalarQuantity(expected_gap_momentum, unit),
            0.0,
            0.0,
        )
        self._add(
            comparisons,
            "sampled_gap_threshold_side",
            ScalarQuantity(
                float(
                    result.minimum_sampled_gap.magnitude
                    >= configuration.sampled_gap_threshold
                ),
                unit,
            ),
            ScalarQuantity(
                float(expected_gap >= configuration.sampled_gap_threshold),
                unit,
            ),
            0.0,
            0.0,
        )
        expected_refinement_pass = bool(
            np.all(expected_changes[-1] <= configuration.refinement_tolerance)
        )
        expected_passage_stable = expected_coarse[-1] == expected_fine[-1]
        expected_qualification = (
            expected_gap >= configuration.sampled_gap_threshold
            and expected_refinement_pass
            and expected_passage_stable
            and expected_first_passes[-1] is not None
            and expected_sustained_passages[-1]
        )
        self._add(
            comparisons,
            "finite_qualification_disposition",
            ScalarQuantity(float(result.finite_qualification_passes), unit),
            ScalarQuantity(float(expected_qualification), unit),
            0.0,
            0.0,
        )
        self._projection_comparisons(comparisons)
        return Periodic1DFourierLocalityIndependentReference(comparisons)

    def _parent_bands(
        self,
        coordinates: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        configuration = self.request.result.configuration
        denominator = float(configuration.coefficient_denominator)
        onsite = (
            np.asarray(configuration.onsite_numerators, dtype=np.float64) / denominator
        )
        hopping = (
            np.asarray(configuration.positive_hopping_numerators, dtype=np.float64)
            / denominator
        )
        spectra = []
        for coordinate in coordinates:
            phase = np.exp(2j * np.pi * coordinate)
            matrix = onsite + phase * hopping + phase.conjugate() * hopping.T
            spectra.append(np.linalg.eigvalsh(matrix))
        values = np.asarray(spectra, dtype=np.float64)
        return values[:, 0], values[:, 1]

    def _add(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
        name: str,
        observed: ScalarQuantity
        | VectorQuantity
        | ComplexVectorQuantity
        | MatrixQuantity,
        reference: ScalarQuantity
        | VectorQuantity
        | ComplexVectorQuantity
        | MatrixQuantity,
        absolute_tolerance: float,
        relative_tolerance: float,
    ) -> None:
        reference_values = np.asarray(reference.magnitude)
        tolerance = absolute_tolerance + relative_tolerance * float(
            np.max(np.abs(reference_values))
        )
        comparisons[name] = MaximumAbsoluteErrorComparison(
            observed,
            reference,
            ScalarQuantity(tolerance, observed.unit),
        )

    def _projection_comparisons(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
    ) -> None:
        result = self.request.result
        data = self.request.visualization_data
        unit = Unitless()
        production = result.meshes[-1]
        vector_comparisons = (
            (
                "evaluation_reduced_momenta",
                data.evaluation_reduced_momenta,
                result.evaluation.reduced_momenta,
            ),
            (
                "evaluation_lowest_energies",
                data.evaluation_lowest_energies,
                result.evaluation.lowest_energies,
            ),
            (
                "evaluation_adjacent_energies",
                data.evaluation_adjacent_energies,
                result.evaluation.adjacent_energies,
            ),
            (
                "evaluation_sampled_gaps",
                data.evaluation_sampled_gaps,
                result.evaluation.sampled_gaps,
            ),
            (
                "production_reduced_momenta",
                data.production_reduced_momenta,
                production.construction_reduced_momenta,
            ),
            (
                "production_sampled_gaps",
                data.production_sampled_gaps,
                VectorQuantity(
                    production.adjacent_energies.magnitude
                    - production.lowest_energies.magnitude,
                    unit,
                ),
            ),
            (
                "interpolation_maximum_errors",
                data.interpolation_maximum_errors,
                VectorQuantity(
                    np.asarray(
                        [
                            mesh.interpolation_maximum_error.magnitude
                            for mesh in result.meshes
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "refinement_maximum_changes",
                data.refinement_maximum_changes,
                VectorQuantity(
                    np.max(result.normalized_refinement_changes.magnitude, axis=1),
                    unit,
                ),
            ),
            (
                "production_complete_representatives",
                VectorQuantity(
                    np.asarray(
                        data.production_complete_representatives,
                        dtype=np.float64,
                    ),
                    unit,
                ),
                VectorQuantity(
                    np.asarray(production.complete_representatives, dtype=np.float64),
                    unit,
                ),
            ),
            (
                "production_complete_coefficient_magnitudes",
                data.production_complete_coefficient_magnitudes,
                VectorQuantity(
                    np.abs(production.complete_coefficients.magnitude),
                    unit,
                ),
            ),
        )
        for name, vector_observed, vector_reference in vector_comparisons:
            self._add(
                comparisons,
                f"visualization_{name}",
                vector_observed,
                vector_reference,
                0.0,
                0.0,
            )
        matrix_comparisons = (
            (
                "truncation_maximum_errors",
                data.truncation_maximum_errors,
                MatrixQuantity(
                    np.asarray(
                        [
                            [
                                item.truncation_maximum_error.magnitude
                                for item in mesh.ranges
                            ]
                            for mesh in result.meshes
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "mediated_total_maximum_errors",
                data.mediated_total_maximum_errors,
                MatrixQuantity(
                    np.asarray(
                        [
                            [
                                item.mediated_total_maximum_error.magnitude
                                for item in mesh.ranges
                            ]
                            for mesh in result.meshes
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "direct_total_maximum_errors",
                data.direct_total_maximum_errors,
                MatrixQuantity(
                    np.asarray(
                        [
                            [
                                item.direct_total_maximum_error.magnitude
                                for item in mesh.ranges
                            ]
                            for mesh in result.meshes
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "omitted_coefficient_l2_norms",
                data.omitted_coefficient_l2_norms,
                MatrixQuantity(
                    np.asarray(
                        [
                            [
                                item.omitted_coefficient_l2_norm.magnitude
                                for item in mesh.ranges
                            ]
                            for mesh in result.meshes
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "coefficient_l2_defects",
                data.coefficient_l2_defects,
                MatrixQuantity(
                    np.asarray(
                        [
                            [
                                item.coefficient_l2_defect.magnitude
                                for item in mesh.ranges
                            ]
                            for mesh in result.meshes
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "sampled_maximum_defects",
                data.sampled_maximum_defects,
                MatrixQuantity(
                    np.asarray(
                        [
                            [
                                item.sampled_maximum_defect.magnitude
                                for item in mesh.ranges
                            ]
                            for mesh in result.meshes
                        ],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "nondominated_masks",
                MatrixQuantity(
                    np.asarray(data.nondominated_masks, dtype=np.float64), unit
                ),
                MatrixQuantity(
                    np.asarray(
                        [mesh.nondominated_mask for mesh in result.meshes],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
            (
                "near_tie_masks",
                MatrixQuantity(np.asarray(data.near_tie_masks, dtype=np.float64), unit),
                MatrixQuantity(
                    np.asarray(
                        [mesh.near_tie_mask for mesh in result.meshes],
                        dtype=np.float64,
                    ),
                    unit,
                ),
            ),
        )
        for name, matrix_observed, matrix_reference in matrix_comparisons:
            self._add(
                comparisons,
                f"visualization_{name}",
                matrix_observed,
                matrix_reference,
                0.0,
                0.0,
            )
        self._add(
            comparisons,
            "visualization_first_joint_passes",
            VectorQuantity(
                np.asarray(
                    [
                        -1 if value is None else value
                        for value in data.first_joint_passes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            VectorQuantity(
                np.asarray(
                    [
                        -1 if mesh.first_joint_pass is None else mesh.first_joint_pass
                        for mesh in result.meshes
                    ],
                    dtype=np.float64,
                ),
                unit,
            ),
            0.0,
            0.0,
        )
        self._add(
            comparisons,
            "visualization_sustained_after_first_passes",
            VectorQuantity(
                np.asarray(data.sustained_after_first_passes, dtype=np.float64), unit
            ),
            VectorQuantity(
                np.asarray(
                    [mesh.sustained_after_first_pass for mesh in result.meshes],
                    dtype=np.float64,
                ),
                unit,
            ),
            0.0,
            0.0,
        )
        scalar_comparisons = (
            (
                "minimum_sampled_gap",
                data.minimum_sampled_gap,
                result.minimum_sampled_gap,
            ),
            (
                "sampled_gap_threshold",
                data.sampled_gap_threshold,
                ScalarQuantity(result.configuration.sampled_gap_threshold, unit),
            ),
            (
                "application_threshold",
                data.application_threshold,
                ScalarQuantity(result.configuration.application_threshold, unit),
            ),
        )
        for name, scalar_observed, scalar_reference in scalar_comparisons:
            self._add(
                comparisons,
                f"visualization_{name}",
                scalar_observed,
                scalar_reference,
                0.0,
                0.0,
            )
