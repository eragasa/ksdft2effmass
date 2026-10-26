"""Direct typed analysis of QHO1D spatial truncation."""

from __future__ import annotations

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.model_systems.analysis import BaseModelSystemAnalyzer
from ksdft2effmass.operators import LadderOperator1D

from ..boundary_conditions import DirichletBoundaryCondition
from ..cartesian_grids import UniformCartesianGrid1D
from ..intervals import DirichletInterval
from .case_sections import Qho1dResidualResult
from .comparison import Qho1dComparator
from .configuration import Qho1dConfiguration
from .model import (
    Qho1dAnalytical,
    Qho1dComparisonRequest,
    Qho1dComparisonResult,
    Qho1dFiniteDifference,
    Qho1dLadderOperators,
)
from .result import (
    Qho1dCalculationResult,
    Qho1dCaseResult,
    Qho1dStateComparisonResult,
)


class Qho1dAnalyzer(BaseModelSystemAnalyzer):
    """Calculate an ordered QHO1D spatial-truncation sweep.

    The analyzer owns calculation composition only. The analytical model,
    finite-difference representation, ladder operators, and common-coordinate
    comparator remain reusable domain owners.
    """

    __slots__ = ("_comparator",)

    def __init__(self, comparator: Qho1dComparator | None = None) -> None:
        """Construct the analyzer with an explicit or default comparator.

        Parameters
        ----------
        comparator
            Stateless common-coordinate comparison action. ``None`` constructs the
            supported default.

        Raises
        ------
        TypeError
            ``comparator`` is neither ``Qho1dComparator`` nor ``None``.
        """
        if comparator is not None and not isinstance(comparator, Qho1dComparator):
            raise TypeError("comparator must be Qho1dComparator or None")
        self._comparator = comparator or Qho1dComparator()

    def execute(
        self,
        configuration: Qho1dConfiguration,
        *,
        calculation_family: str,
        execution_id: str,
        evidence_status: str,
        claim_boundary: str,
    ) -> Qho1dCalculationResult:
        """Calculate one complete typed QHO1D result.

        Parameters
        ----------
        configuration
            Exact nondimensional sweep and state-visualization selection.
        calculation_family
            Stable family identifier without a publication revision suffix.
        execution_id
            Concrete execution identifier.
        evidence_status
            Explicit result classification.
        claim_boundary
            Human-readable limit on claims supported by this calculation.

        Returns
        -------
        Qho1dCalculationResult
            Immutable typed sweep and selected state-resolved comparison.

        Raises
        ------
        TypeError
            ``configuration`` or a metadata value has the wrong type.
        ValueError
            Metadata is empty or the selected case cannot be identified uniquely.
        """
        if not isinstance(configuration, Qho1dConfiguration):
            raise TypeError("configuration must be Qho1dConfiguration")
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
        comparisons = tuple(
            self._comparator.execute(
                self._request(configuration, box, spacing, retained)
            )
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
        state_comparison = self._state_comparison(
            selected[0], configuration.displayed_states
        )
        return Qho1dCalculationResult(
            calculation_family=calculation_family,
            execution_id=execution_id,
            evidence_status=evidence_status,
            claim_boundary=claim_boundary,
            configuration=configuration,
            cases=cases,
            selected_state_comparison=state_comparison,
        )

    @staticmethod
    def _request(
        configuration: Qho1dConfiguration,
        box_half_width: float,
        grid_spacing: float,
        retained_dimension: int,
    ) -> Qho1dComparisonRequest:
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

    @staticmethod
    def _case(comparison: Qho1dComparisonResult) -> Qho1dCaseResult:
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
                frobenius=ScalarQuantity(
                    float(np.linalg.norm(residual, ord="fro")),
                    hamiltonian.unit,
                )
            ),
        )

    @staticmethod
    def _state_comparison(
        comparison: Qho1dComparisonResult,
        displayed_states: int,
    ) -> Qho1dStateComparisonResult:
        request = comparison.request
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
