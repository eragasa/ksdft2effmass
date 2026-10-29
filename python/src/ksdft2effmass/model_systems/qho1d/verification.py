"""Independent verification of direct typed QHO1D results."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from scipy.special import eval_hermite  # type: ignore[import-untyped]

from ksdft2effmass.model_systems.analysis import BaseModelAnalysisVerifier
from ksdft2effmass.model_systems.verification import (
    VisualizationProjectionVerification,
)
from ksdft2effmass.verification import (
    CompositeVerification,
    MaximumAbsoluteErrorComparison,
)

from .result import Qho1dCalculationResult, Qho1dCaseResult
from .verification_values import (
    Qho1dHamiltonianComparisonVerification,
    Qho1dResidualVerification,
    Qho1dSampledStateAlignmentVerification,
    Qho1dSpatialRepresentationVerification,
    Qho1dStateComparisonVerification,
    Qho1dVerification,
)
from .visualizations.data import Qho1dVisualizationData

type ReferenceQuantity = ScalarQuantity | VectorQuantity | MatrixQuantity


@dataclass(frozen=True, slots=True)
class Qho1dIndependentReferenceComparisons:
    """Retain operation-partitioned independent QHO1D comparisons.

    Parameters
    ----------
    spatial_representation
        Finite-grid geometry and represented-dimension comparisons.
    sampled_state_alignment
        Gram-correction and injection comparisons.
    hamiltonian_comparison
        Common-coordinate operator and discrepancy comparisons.
    residual
        Full-space intertwining-residual comparisons.
    state_comparison
        Named comparisons for the selected state-resolved case.
    visualization_projection
        Named correlations between authoritative results and projected plot data.

    Raises
    ------
    TypeError
        A partition is not a string-keyed comparison mapping.
    ValueError
        A partition is empty or observation names collide across partitions.
    """

    spatial_representation: Mapping[str, MaximumAbsoluteErrorComparison]
    sampled_state_alignment: Mapping[str, MaximumAbsoluteErrorComparison]
    hamiltonian_comparison: Mapping[str, MaximumAbsoluteErrorComparison]
    residual: Mapping[str, MaximumAbsoluteErrorComparison]
    state_comparison: Mapping[str, MaximumAbsoluteErrorComparison]
    visualization_projection: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        names: set[str] = set()
        for field_name in (
            "spatial_representation",
            "sampled_state_alignment",
            "hamiltonian_comparison",
            "residual",
            "state_comparison",
            "visualization_projection",
        ):
            values = getattr(self, field_name)
            if not isinstance(values, Mapping):
                raise TypeError(f"{field_name} must be a mapping")
            if not values:
                raise ValueError(f"{field_name} must be nonempty")
            copied: dict[str, MaximumAbsoluteErrorComparison] = {}
            for name, comparison in values.items():
                if type(name) is not str or not name:
                    raise TypeError("comparison names must be nonempty strings")
                if not isinstance(comparison, MaximumAbsoluteErrorComparison):
                    raise TypeError(
                        "comparison mappings must contain maximum-error comparisons"
                    )
                if name in names:
                    raise ValueError("independent comparison names must be unique")
                names.add(name)
                copied[name] = comparison
            object.__setattr__(self, field_name, MappingProxyType(copied))


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dIndependentReferenceRequest:
    """Bind one result and its verifier-derived visualization projection."""

    result: Qho1dCalculationResult
    visualization_data: Qho1dVisualizationData

    def __post_init__(self) -> None:
        """Admit the complete typed independent-reference request."""
        if type(self.result) is not Qho1dCalculationResult:
            raise TypeError("result must be Qho1dCalculationResult")
        if type(self.visualization_data) is not Qho1dVisualizationData:
            raise TypeError("visualization_data must be Qho1dVisualizationData")


class Qho1dIndependentReferenceAnalyzer:
    """Reconstruct one bound QHO1D subject without production analyzers."""

    __slots__ = ("_request",)

    def __init__(self, request: Qho1dIndependentReferenceRequest) -> None:
        if type(request) is not Qho1dIndependentReferenceRequest:
            raise TypeError("request must be Qho1dIndependentReferenceRequest")
        self._request = request

    @property
    def request(self) -> Qho1dIndependentReferenceRequest:
        """Return the complete immutable independent-reference request."""
        return self._request

    def execute(self) -> Qho1dIndependentReferenceComparisons:
        """Return independent comparisons for one decoded QHO1D result.

        Returns
        -------
        Qho1dIndependentReferenceComparisons
            Sweep, selected-state, and visualization-projection comparisons.

        Raises
        ------
        ValueError
            An independent Gram matrix is not positive definite or the selected case
            is absent.
        """
        result = self.request.result
        representation: dict[str, MaximumAbsoluteErrorComparison] = {}
        alignment: dict[str, MaximumAbsoluteErrorComparison] = {}
        hamiltonian: dict[str, MaximumAbsoluteErrorComparison] = {}
        residual: dict[str, MaximumAbsoluteErrorComparison] = {}
        references: dict[tuple[float, float, int], Mapping[str, ReferenceQuantity]] = {}
        for index, case in enumerate(result.cases):
            reference = self._case_reference(case)
            references[case.key] = reference
            prefix = f"case_{index:02d}"
            self._append_case_comparisons(
                representation,
                alignment,
                hamiltonian,
                residual,
                prefix,
                case,
                reference,
            )
        selected_key = (
            result.configuration.selected_box_half_width,
            result.configuration.selected_grid_spacing,
            result.configuration.selected_retained_dimension,
        )
        selected_reference = references.get(selected_key)
        if selected_reference is None:
            raise ValueError("selected QHO1D reference case is absent")
        state = self._state_comparisons(selected_reference)
        projection = self._projection_comparisons()
        return Qho1dIndependentReferenceComparisons(
            spatial_representation=representation,
            sampled_state_alignment=alignment,
            hamiltonian_comparison=hamiltonian,
            residual=residual,
            state_comparison=state,
            visualization_projection=projection,
        )

    def _case_reference(
        self,
        case: Qho1dCaseResult,
    ) -> Mapping[str, ReferenceQuantity]:
        configuration = self.request.result.configuration
        box = case.box_half_width.magnitude
        requested_spacing = case.requested_grid_spacing.magnitude
        retained = case.retained_dimension
        expected_points = int(round(2.0 * box / requested_spacing)) - 1
        spacing = 2.0 * box / (expected_points + 1)
        coordinates = -box + spacing * np.arange(
            1, expected_points + 1, dtype=np.float64
        )
        oscillator_length = math.sqrt(
            configuration.hbar / (configuration.mass * configuration.omega)
        )
        dimensionless = coordinates / oscillator_length
        sampled = np.empty((expected_points, retained), dtype=np.float64)
        for degree in range(retained):
            normalization = 1.0 / math.sqrt(
                oscillator_length
                * math.sqrt(math.pi)
                * float(2**degree)
                * float(math.factorial(degree))
            )
            sampled[:, degree] = (
                math.sqrt(spacing)
                * normalization
                * eval_hermite(degree, dimensionless)
                * np.exp(-0.5 * np.square(dimensionless))
            )
        gram = sampled.T @ sampled
        eigenvalues, eigenvectors = np.linalg.eigh(gram)
        if eigenvalues[0] <= 0.0:
            raise ValueError("independent sampled-state Gram matrix is not positive")
        inverse = eigenvectors @ np.diag(np.power(eigenvalues, -0.5)) @ eigenvectors.T
        injection = sampled @ inverse
        kinetic_prefactor = configuration.hbar**2 / (
            2.0 * configuration.mass * spacing**2
        )
        diagonal = 2.0 * kinetic_prefactor + 0.5 * configuration.mass * (
            configuration.omega**2
        ) * np.square(coordinates)
        hamiltonian = np.diag(diagonal)
        hamiltonian += np.diag(np.full(expected_points - 1, -kinetic_prefactor), 1)
        hamiltonian += np.diag(np.full(expected_points - 1, -kinetic_prefactor), -1)
        pulled_back = injection.T @ hamiltonian @ injection
        reference = np.diag(
            configuration.hbar
            * configuration.omega
            * (np.arange(retained, dtype=np.float64) + 0.5)
        )
        difference = pulled_back - reference
        diagonal_difference = np.diag(np.diag(difference))
        off_diagonal_difference = difference - diagonal_difference
        absolute = float(np.linalg.norm(difference, ord="fro"))
        reference_scale = float(np.linalg.norm(reference, ord="fro"))
        residual = hamiltonian @ injection - injection @ reference
        return MappingProxyType(
            {
                "interior_points": ScalarQuantity(float(expected_points), Unitless()),
                "grid_spacing": ScalarQuantity(spacing, Unitless()),
                "grid_coordinates": VectorQuantity(coordinates, Unitless()),
                "injection": MatrixQuantity(injection, Unitless()),
                "gram_matrix": MatrixQuantity(gram, Unitless()),
                "gram_inverse_square_root": MatrixQuantity(inverse, Unitless()),
                "pulled_back_hamiltonian": MatrixQuantity(pulled_back, Unitless()),
                "reference_hamiltonian": MatrixQuantity(reference, Unitless()),
                "difference": MatrixQuantity(difference, Unitless()),
                "gram_deviation": ScalarQuantity(
                    float(np.linalg.norm(gram - np.eye(retained), ord="fro")),
                    Unitless(),
                ),
                "gram_condition_number": ScalarQuantity(
                    float(eigenvalues[-1] / eigenvalues[0]), Unitless()
                ),
                "injection_isometry_error": ScalarQuantity(
                    float(
                        np.linalg.norm(
                            injection.T @ injection - np.eye(retained), ord="fro"
                        )
                    ),
                    Unitless(),
                ),
                "absolute_discrepancy": ScalarQuantity(absolute, Unitless()),
                "relative_discrepancy": ScalarQuantity(
                    absolute / reference_scale, Unitless()
                ),
                "diagonal_discrepancy": ScalarQuantity(
                    float(np.linalg.norm(diagonal_difference, ord="fro")),
                    Unitless(),
                ),
                "off_diagonal_discrepancy": ScalarQuantity(
                    float(np.linalg.norm(off_diagonal_difference, ord="fro")),
                    Unitless(),
                ),
                "residual_frobenius": ScalarQuantity(
                    float(np.linalg.norm(residual, ord="fro")), Unitless()
                ),
                "hamiltonian": MatrixQuantity(hamiltonian, Unitless()),
                "analytical_wavefunctions": MatrixQuantity(
                    sampled / math.sqrt(spacing), Unitless()
                ),
            }
        )

    def _comparison(
        self,
        observed: ReferenceQuantity,
        reference: ReferenceQuantity,
        tolerance: float,
    ) -> MaximumAbsoluteErrorComparison:
        return MaximumAbsoluteErrorComparison(
            observed=observed,
            reference=reference,
            tolerance=ScalarQuantity(tolerance, Unitless()),
        )

    def _append_case_comparisons(
        self,
        representation: dict[str, MaximumAbsoluteErrorComparison],
        alignment: dict[str, MaximumAbsoluteErrorComparison],
        hamiltonian: dict[str, MaximumAbsoluteErrorComparison],
        residual: dict[str, MaximumAbsoluteErrorComparison],
        prefix: str,
        case: Qho1dCaseResult,
        reference: Mapping[str, ReferenceQuantity],
    ) -> None:
        observed: Mapping[str, ReferenceQuantity] = {
            "interior_points": ScalarQuantity(float(case.interior_points), Unitless()),
            "grid_spacing": case.grid_spacing,
            "grid_coordinates": case.grid_coordinates,
            "injection": case.injection,
            "gram_matrix": case.gram_matrix,
            "gram_inverse_square_root": case.gram_inverse_square_root,
            "pulled_back_hamiltonian": case.pulled_back_hamiltonian,
            "reference_hamiltonian": case.reference_hamiltonian,
            "difference": case.difference,
            "gram_deviation": case.gram_deviation,
            "gram_condition_number": case.gram_condition_number,
            "injection_isometry_error": case.injection_isometry_error,
            "absolute_discrepancy": case.absolute_discrepancy,
            "relative_discrepancy": case.relative_discrepancy,
            "diagonal_discrepancy": case.diagonal_discrepancy,
            "off_diagonal_discrepancy": case.off_diagonal_discrepancy,
            "residual_frobenius": case.residual_frobenius,
        }
        representation_names = {
            "interior_points",
            "grid_spacing",
            "grid_coordinates",
        }
        alignment_names = {
            "injection",
            "gram_matrix",
            "gram_inverse_square_root",
            "gram_deviation",
            "gram_condition_number",
            "injection_isometry_error",
        }
        for name, value in observed.items():
            if name in representation_names:
                destination = representation
            elif name in alignment_names:
                destination = alignment
            elif name == "residual_frobenius":
                destination = residual
            else:
                destination = hamiltonian
            destination[f"{prefix}_{name}_maximum_absolute_error"] = self._comparison(
                value,
                reference[name],
                2.0e-14 if name in representation_names else 5.0e-11,
            )

    def _state_comparisons(
        self,
        reference: Mapping[str, ReferenceQuantity],
    ) -> Mapping[str, MaximumAbsoluteErrorComparison]:
        result = self.request.result
        state = result.selected_state_comparison
        hamiltonian = reference["hamiltonian"]
        analytical = reference["analytical_wavefunctions"]
        if not isinstance(hamiltonian, MatrixQuantity) or not isinstance(
            analytical, MatrixQuantity
        ):
            raise TypeError("independent state references must be matrices")
        eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian.magnitude)
        finite = eigenvectors[:, : state.retained_dimension] / math.sqrt(
            state.grid_spacing.magnitude
        )
        for index in range(state.retained_dimension):
            overlap = state.grid_spacing.magnitude * np.dot(
                analytical.magnitude[:, index], finite[:, index]
            )
            if overlap < 0.0:
                finite[:, index] *= -1.0
        analytical_energies = (
            result.configuration.hbar
            * result.configuration.omega
            * (np.arange(state.retained_dimension, dtype=np.float64) + 0.5)
        )
        return MappingProxyType(
            {
                "state_coordinates_maximum_absolute_error": self._comparison(
                    state.coordinates,
                    reference["grid_coordinates"],
                    2.0e-14,
                ),
                (
                    "state_analytical_wavefunction_maximum_absolute_error"
                ): self._comparison(
                    state.analytical_wavefunctions,
                    analytical,
                    2.0e-12,
                ),
                "state_finite_wavefunction_maximum_absolute_error": self._comparison(
                    state.finite_wavefunctions,
                    MatrixQuantity(finite, Unitless()),
                    2.0e-12,
                ),
                "state_analytical_energy_maximum_absolute_error": self._comparison(
                    state.analytical_energies,
                    VectorQuantity(analytical_energies, Unitless()),
                    2.0e-14,
                ),
                "state_finite_energy_maximum_absolute_error": self._comparison(
                    state.finite_energies,
                    VectorQuantity(eigenvalues[: state.retained_dimension], Unitless()),
                    2.0e-12,
                ),
            }
        )

    def _projection_comparisons(
        self,
    ) -> Mapping[str, MaximumAbsoluteErrorComparison]:
        result = self.request.result
        data = self.request.visualization_data
        first_result = result.cases[0]
        first_projection = data.cases[0]
        return MappingProxyType(
            {
                "visualization_case_count_error": self._comparison(
                    ScalarQuantity(float(len(data.cases)), Unitless()),
                    ScalarQuantity(float(len(result.cases)), Unitless()),
                    0.0,
                ),
                "visualization_first_relative_discrepancy_error": self._comparison(
                    first_projection.relative_discrepancy,
                    first_result.relative_discrepancy,
                    0.0,
                ),
                (
                    "visualization_selected_coordinate_maximum_absolute_error"
                ): self._comparison(
                    data.selected_state_comparison.coordinates,
                    result.selected_state_comparison.coordinates,
                    0.0,
                ),
                (
                    "visualization_selected_finite_energy_maximum_absolute_error"
                ): self._comparison(
                    data.selected_state_comparison.finite_energies,
                    result.selected_state_comparison.finite_energies,
                    0.0,
                ),
            }
        )


class Qho1dVerifier(
    BaseModelAnalysisVerifier[
        Qho1dCalculationResult,
        Qho1dVerification,
        Qho1dVisualizationData,
    ]
):
    """Derive, authenticate, and independently verify one QHO1D result."""

    __slots__ = ()

    @classmethod
    def _result_type(cls) -> type[Qho1dCalculationResult]:
        """Return the typed QHO1D root reconstructed by the shared boundary."""
        return Qho1dCalculationResult

    def _visualization_data(self) -> Qho1dVisualizationData:
        return Qho1dVisualizationData(
            configuration=self._result.configuration,
            cases=self._result.cases,
            selected_state_comparison=self._result.selected_state_comparison,
        )

    def _verification_types(self) -> tuple[type[CompositeVerification], ...]:
        return (
            Qho1dSpatialRepresentationVerification,
            Qho1dSampledStateAlignmentVerification,
            Qho1dHamiltonianComparisonVerification,
            Qho1dResidualVerification,
            Qho1dStateComparisonVerification,
            VisualizationProjectionVerification,
        )

    def _verification_components(
        self,
        visualization_data: Qho1dVisualizationData,
    ) -> tuple[CompositeVerification, ...]:
        reference = Qho1dIndependentReferenceAnalyzer(
            Qho1dIndependentReferenceRequest(self._result, visualization_data)
        ).execute()
        return (
            Qho1dSpatialRepresentationVerification.evaluate(
                reference.spatial_representation
            ),
            Qho1dSampledStateAlignmentVerification.evaluate(
                reference.sampled_state_alignment
            ),
            Qho1dHamiltonianComparisonVerification.evaluate(
                reference.hamiltonian_comparison
            ),
            Qho1dResidualVerification.evaluate(reference.residual),
            Qho1dStateComparisonVerification.evaluate(reference.state_comparison),
            VisualizationProjectionVerification.evaluate(
                reference.visualization_projection
            ),
        )

    def _verification(
        self,
        *,
        visualization_data_sha256: str,
        components: tuple[CompositeVerification, ...],
    ) -> Qho1dVerification:
        return Qho1dVerification(
            subject_sha256=self._subject_sha256,
            visualization_data_sha256=visualization_data_sha256,
            components=components,
        )
