"""Domain-facing facade for the fixed higher-rank D1 campaign calculation."""

from __future__ import annotations

from .case_calculation import HigherRankD1CaseCalculator
from .definition import HigherRankD1Definition
from .records import HigherRankD1CalculationResult


class HigherRankD1Calculator:
    """Calculate the fixed case inventory and aggregate its qualification."""

    __slots__ = ()

    def execute(
        self, definition: HigherRankD1Definition
    ) -> HigherRankD1CalculationResult:
        """Calculate all sixteen cases in canonical rank-major order."""
        if type(definition) is not HigherRankD1Definition:
            raise TypeError("definition must be HigherRankD1Definition")
        case_calculator = HigherRankD1CaseCalculator()
        cases = tuple(case_calculator.execute(case) for case in definition.cases)
        return HigherRankD1CalculationResult.aggregate(cases)


__all__ = ["HigherRankD1Calculator"]
