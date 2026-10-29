"""Direct typed analysis of QHO1D spatial truncation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.linalg.matrix.norm import FrobeniusMatrixNorm
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.operators import LadderOperator1D

from ..boundary_conditions import DirichletBoundaryCondition
from ..cartesian_grids import UniformCartesianGrid1D
from ..intervals import DirichletInterval
from .analytical import Qho1dAnalytical
from .case_sections import Qho1dResidualResult
from .comparison import Qho1dComparator
from .comparison_records import Qho1dComparisonRequest, Qho1dComparisonResult
from .configuration import Qho1dConfiguration
from .finite_difference import Qho1dFiniteDifference
from .ladder_operators import Qho1dLadderOperators
from .result import (
    Qho1dCalculationResult,
    Qho1dCaseResult,
    Qho1dStateComparisonResult,
)


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dAnalysisRequest:
    """Bind one complete QHO1D calculation and result-identity request."""

    configuration: Qho1dConfiguration
    calculation_family: str
    execution_id: str
    evidence_status: str
    claim_boundary: str

    def __post_init__(self) -> None:
        """Admit the typed configuration and nonempty result-identity metadata."""
        if type(self.configuration) is not Qho1dConfiguration:
            raise TypeError("configuration must be Qho1dConfiguration")
        for name, value in (
            ("calculation_family", self.calculation_family),
            ("execution_id", self.execution_id),
            ("evidence_status", self.evidence_status),
            ("claim_boundary", self.claim_boundary),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")


class Qho1dAnalyzer:
    """Calculate an ordered QHO1D spatial-truncation sweep.

    The analyzer owns calculation composition only. The analytical model,
    finite-difference representation, ladder operators, and common-coordinate
    comparator remain reusable domain owners.
    """

    __slots__ = ("_request",)

    def __init__(self, request: Qho1dAnalysisRequest) -> None:
        if type(request) is not Qho1dAnalysisRequest:
            raise TypeError("request must be Qho1dAnalysisRequest")
        self._request = request

    @property
    def request(self) -> Qho1dAnalysisRequest:
        """Return the complete immutable calculation request."""
        return self._request

    def execute(self) -> Qho1dCalculationResult:
        """Calculate one complete typed QHO1D result.

        Returns
        -------
        Qho1dCalculationResult
            Immutable typed sweep and selected state-resolved comparison.

        Raises
        ------
        ValueError
            The selected case cannot be identified uniquely.
        """
        request = self.request
        configuration = request.configuration
        comparisons = tuple(
            Qho1dComparator(self._comparison_request(box, spacing, retained)).execute()
            for box in configuration.box_half_widths
            for spacing in configuration.grid_spacings
            for retained in configuration.retained_dimensions
        )
        cases = tuple(self._case(comparison) for comparison in comparisons)
        selected = tuple(
            comparison
            for comparison in comparisons
            if (
                comparison.request.box_half_width.magnitude
                == configuration.selected_box_half_width
                and comparison.request.requested_grid_spacing.magnitude
                == configuration.selected_grid_spacing
                and comparison.request.retained_dimension
                == configuration.selected_retained_dimension
            )
        )
        if len(selected) != 1:
            raise ValueError("selected configuration must identify one comparison")
        state_comparison = self._state_comparison(selected[0])
        return Qho1dCalculationResult(
            calculation_family=request.calculation_family,
            execution_id=request.execution_id,
            evidence_status=request.evidence_status,
            claim_boundary=request.claim_boundary,
            configuration=configuration,
            cases=cases,
            selected_state_comparison=state_comparison,
        )

    def _comparison_request(
        self,
        box_half_width: float,
        grid_spacing: float,
        retained_dimension: int,
    ) -> Qho1dComparisonRequest:
        configuration = self.request.configuration
        analytical = Qho1dAnalytical(configuration.parameters)
        interval = DirichletInterval(
            grid=UniformCartesianGrid1D(
                lower_bound=ScalarQuantity(-box_half_width, Unitless()),
                upper_bound=ScalarQuantity(box_half_width, Unitless()),
                requested_spacing=ScalarQuantity(grid_spacing, Unitless()),
            ),
            boundary_condition=DirichletBoundaryCondition(
                ScalarQuantity(0.0, Unitless())
            ),
        )
        return Qho1dComparisonRequest(
            analytical=analytical,
            finite_difference=Qho1dFiniteDifference(
                analytical=analytical,
                interval=interval,
            ),
            ladder_operators=Qho1dLadderOperators(
                analytical=analytical,
                ladder_operator=LadderOperator1D(retained_dimension),
            ),
        )

    def _case(self, comparison: Qho1dComparisonResult) -> Qho1dCaseResult:
        request = comparison.request
        hamiltonian = request.finite_difference.hamiltonian().to_dense()
        residual = (
            hamiltonian.magnitude @ comparison.injection.magnitude
            - comparison.injection.magnitude
            @ comparison.reference_hamiltonian.magnitude
        )
        return Qho1dCaseResult(
            representation=comparison.representation,
            alignment=comparison.alignment,
            hamiltonian_comparison=comparison.hamiltonian_comparison,
            residual=Qho1dResidualResult(
                frobenius=FrobeniusMatrixNorm(
                    MatrixQuantity(residual, hamiltonian.unit)
                ).result()
            ),
        )

    def _state_comparison(
        self,
        comparison: Qho1dComparisonResult,
    ) -> Qho1dStateComparisonResult:
        request = comparison.request
        displayed_states = self.request.configuration.displayed_states
        coordinates = comparison.grid_coordinates
        spacing = comparison.grid_spacing
        oscillator_length = request.parameters.oscillator_length.magnitude
        analytical = request.analytical.number_state_wavefunctions(
            VectorQuantity(coordinates.magnitude / oscillator_length, Unitless()),
            request.retained_dimension,
        )
        hamiltonian = request.finite_difference.hamiltonian().to_dense()
        eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian.magnitude)
        finite_states = eigenvectors[:, : request.retained_dimension] / np.sqrt(
            spacing.magnitude
        )
        for state in range(request.retained_dimension):
            overlap = spacing.magnitude * np.dot(
                analytical.magnitude[:, state], finite_states[:, state]
            )
            if overlap < 0.0:
                finite_states[:, state] *= -1.0
        return Qho1dStateComparisonResult(
            box_half_width=request.box_half_width,
            grid_spacing=spacing,
            retained_dimension=request.retained_dimension,
            displayed_states=displayed_states,
            coordinates=coordinates,
            analytical_wavefunctions=analytical,
            finite_wavefunctions=MatrixQuantity(finite_states, analytical.unit),
            analytical_energies=request.analytical.number_state_energies(
                request.retained_dimension
            ),
            finite_energies=VectorQuantity(
                eigenvalues[: request.retained_dimension], hamiltonian.unit
            ),
        )
