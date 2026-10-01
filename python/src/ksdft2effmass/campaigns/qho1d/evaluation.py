"""Deterministic evaluation of the harmonic-oscillator study sweep."""

from __future__ import annotations

from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    UniformCartesianGrid1D,
)
from ksdft2effmass.analysis.model_systems.harmonic_oscillator import (
    HarmonicOscillatorAnalytical,
    HarmonicOscillatorComparator,
    HarmonicOscillatorComparisonRequest,
    HarmonicOscillatorFiniteDifference,
    HarmonicOscillatorLadderOperators,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import LadderOperator1D

from .records import HarmonicOscillatorStudyDefinition, HarmonicOscillatorStudyResult


class HarmonicOscillatorStudyEvaluator:
    """Evaluate the exact ordered Cartesian product in one study definition."""

    __slots__ = ("comparator",)

    def __init__(self, comparator: HarmonicOscillatorComparator | None = None) -> None:
        """Construct the evaluator with an explicit or default comparator.

        Parameters
        ----------
        comparator
            Stateless reusable comparator. ``None`` constructs the supported default.
        """
        if comparator is not None and not isinstance(
            comparator, HarmonicOscillatorComparator
        ):
            raise TypeError("comparator must be HarmonicOscillatorComparator or None")
        self.comparator = comparator or HarmonicOscillatorComparator()

    def execute(
        self, definition: HarmonicOscillatorStudyDefinition
    ) -> HarmonicOscillatorStudyResult:
        """Evaluate every declared comparison in deterministic order.

        Parameters
        ----------
        definition
            Exact study definition.

        Returns
        -------
        HarmonicOscillatorStudyResult
            Immutable ordered comparison aggregate.
        """
        if not isinstance(definition, HarmonicOscillatorStudyDefinition):
            raise TypeError("definition must be HarmonicOscillatorStudyDefinition")
        analytical = HarmonicOscillatorAnalytical(definition.parameters)
        comparisons = tuple(
            self.comparator.execute(
                HarmonicOscillatorComparisonRequest(
                    analytical=analytical,
                    finite_difference=HarmonicOscillatorFiniteDifference(
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
                    ladder_operators=HarmonicOscillatorLadderOperators(
                        analytical=analytical,
                        ladder_operator=LadderOperator1D(retained),
                    ),
                )
            )
            for box in definition.box_half_widths
            for spacing in definition.grid_spacings
            for retained in definition.retained_dimensions
        )
        return HarmonicOscillatorStudyResult(definition, comparisons)
