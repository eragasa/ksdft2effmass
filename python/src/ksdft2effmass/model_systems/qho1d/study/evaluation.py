"""Deterministic evaluation of the harmonic-oscillator study sweep."""

from __future__ import annotations

from ksdft2effmass.linalg import (
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import (
    LadderOperator1D,
)

from ...boundary_conditions import DirichletBoundaryCondition
from ...cartesian_grids import UniformCartesianGrid1D
from ...intervals import DirichletInterval
from ..comparison import Qho1dComparator
from ..model import (
    Qho1dAnalytical,
    Qho1dComparisonRequest,
    Qho1dFiniteDifference,
    Qho1dLadderOperators,
)
from .records import Qho1dStudyDefinition, Qho1dStudyResult


class Qho1dStudyEvaluator:
    """Evaluate the exact ordered Cartesian product in one study definition."""

    __slots__ = ("comparator",)

    def __init__(self, comparator: Qho1dComparator | None = None) -> None:
        """Construct the evaluator with an explicit or default comparator.

        Parameters
        ----------
        comparator
            Stateless reusable comparator. ``None`` constructs the supported default.
        """
        if comparator is not None and not isinstance(comparator, Qho1dComparator):
            raise TypeError("comparator must be Qho1dComparator or None")
        self.comparator = comparator or Qho1dComparator()

    def execute(self, definition: Qho1dStudyDefinition) -> Qho1dStudyResult:
        """Evaluate every declared comparison in deterministic order.

        Parameters
        ----------
        definition
            Exact study definition.

        Returns
        -------
        Qho1dStudyResult
            Immutable ordered comparison aggregate.
        """
        if not isinstance(definition, Qho1dStudyDefinition):
            raise TypeError("definition must be Qho1dStudyDefinition")
        analytical = Qho1dAnalytical(definition.parameters)
        comparisons = tuple(
            self.comparator.execute(
                Qho1dComparisonRequest(
                    analytical=analytical,
                    finite_difference=Qho1dFiniteDifference(
                        analytical=analytical,
                        interval=DirichletInterval(
                            grid=UniformCartesianGrid1D(
                                lower_bound=ScalarQuantity(-box, Unitless()),
                                upper_bound=ScalarQuantity(box, Unitless()),
                                requested_spacing=ScalarQuantity(spacing, Unitless()),
                            ),
                            boundary_condition=DirichletBoundaryCondition(
                                ScalarQuantity(0.0, Unitless())
                            ),
                        ),
                    ),
                    ladder_operators=Qho1dLadderOperators(
                        analytical=analytical,
                        ladder_operator=LadderOperator1D(retained),
                    ),
                )
            )
            for box in definition.box_half_widths
            for spacing in definition.grid_spacings
            for retained in definition.retained_dimensions
        )
        return Qho1dStudyResult(definition, comparisons)
