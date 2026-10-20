"""Deterministic evaluation of the harmonic-oscillator study sweep."""

from __future__ import annotations

from ksdft2effmass.operators import (
    LadderOperator1D,
    ScalarQuantity,
    Unitless,
)

from ...boundary_conditions import DirichletBoundaryCondition
from ...cartesian_grids import UniformCartesianGrid1D
from ...intervals import DirichletInterval
from ..comparison import QHO1DComparator
from ..model import (
    QHO1DAnalytical,
    QHO1DComparisonRequest,
    QHO1DFiniteDifference,
    QHO1DLadderOperators,
)
from .records import QHO1DStudyDefinition, QHO1DStudyResult


class QHO1DStudyEvaluator:
    """Evaluate the exact ordered Cartesian product in one study definition."""

    __slots__ = ("comparator",)

    def __init__(self, comparator: QHO1DComparator | None = None) -> None:
        """Construct the evaluator with an explicit or default comparator.

        Parameters
        ----------
        comparator
            Stateless reusable comparator. ``None`` constructs the supported default.
        """
        if comparator is not None and not isinstance(comparator, QHO1DComparator):
            raise TypeError("comparator must be QHO1DComparator or None")
        self.comparator = comparator or QHO1DComparator()

    def execute(self, definition: QHO1DStudyDefinition) -> QHO1DStudyResult:
        """Evaluate every declared comparison in deterministic order.

        Parameters
        ----------
        definition
            Exact study definition.

        Returns
        -------
        QHO1DStudyResult
            Immutable ordered comparison aggregate.
        """
        if not isinstance(definition, QHO1DStudyDefinition):
            raise TypeError("definition must be QHO1DStudyDefinition")
        analytical = QHO1DAnalytical(definition.parameters)
        comparisons = tuple(
            self.comparator.execute(
                QHO1DComparisonRequest(
                    analytical=analytical,
                    finite_difference=QHO1DFiniteDifference(
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
                    ladder_operators=QHO1DLadderOperators(
                        analytical=analytical,
                        ladder_operator=LadderOperator1D(retained),
                    ),
                )
            )
            for box in definition.box_half_widths
            for spacing in definition.grid_spacings
            for retained in definition.retained_dimensions
        )
        return QHO1DStudyResult(definition, comparisons)
