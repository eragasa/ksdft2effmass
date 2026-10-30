"""Domain-facing facade for the fixed higher-rank D1 campaign calculation."""

from __future__ import annotations

from .case_calculation import HigherRankD1CaseCalculator
from .definition import HigherRankD1Definition
from .records import HigherRankD1CalculationResult


class HigherRankD1Calculator:
    """Calculate the bound fixed case inventory and aggregate its qualification."""

    __slots__ = ("_definition",)

    def __init__(self, *, definition: HigherRankD1Definition) -> None:
        if type(definition) is not HigherRankD1Definition:
            raise TypeError("definition must be HigherRankD1Definition")
        self._definition = definition

    def execute(self) -> HigherRankD1CalculationResult:
        """Calculate all sixteen bound cases in canonical rank-major order."""
        cases = tuple(
            HigherRankD1CaseCalculator(definition=case).execute()
            for case in self._definition.cases
        )
        return HigherRankD1CalculationResult.aggregate(cases)


__all__ = ["HigherRankD1Calculator"]
