"""Non-executable calculation scaffolds for controlled periodic-2D studies.

The scaffolds establish only nominal parent-model membership and dependency structure.
They do not construct represented operators, transport operators into a common space,
calculate hopping shells, alter gauges, interpolate withheld points, or establish
scientific validation.  The shell/gauge-locality study composes its represented-parent
baseline instead of inheriting from an unrelated calculation record.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.periodic import Periodic2DModel, PeriodicModelRole


def _validate_definition_id(value: str) -> None:
    if type(value) is not str:
        raise TypeError("definition_id must be a built-in str")
    if not value:
        raise ValueError("definition_id must be nonempty")


def _validate_parent_model(value: Periodic2DModel) -> None:
    if not isinstance(value, Periodic2DModel):
        raise TypeError("parent_model must inherit Periodic2DModel")
    if type(value.model_id) is not str:
        raise TypeError("parent model_id must be a built-in str")
    if not value.model_id:
        raise ValueError("parent model_id must be nonempty")
    if type(value.model_role) is not PeriodicModelRole:
        raise TypeError("parent model_role must be PeriodicModelRole")


@dataclass(frozen=True, slots=True)
class Periodic2DRepresentedParentCalculationScaffold:
    """Identify the parent boundary for represented-parent comparison (M4).

    Future controls must identify the full nonorthogonal primitive lattice and inverse
    metric, reduced-coordinate convention, each representation, common-space map,
    comparison momenta, refinement sequence, units, ordering, and energy reference.
    This record does not execute the maintained representation constructors or
    comparator.
    """

    definition_id: str
    parent_model: Periodic2DModel

    def __post_init__(self) -> None:
        """Require a stable definition identity and a nominal 2D parent model."""
        _validate_definition_id(self.definition_id)
        _validate_parent_model(self.parent_model)


@dataclass(frozen=True, slots=True)
class Periodic2DShellGaugeLocalityCalculationScaffold:
    """Compose the represented-parent baseline for shell/gauge locality (M5).

    The exact nonorthogonal primitive lattice, rank-three retention, shell inventories,
    constrained gauge attacks, hopping transforms, and withheld interpolation
    diagnostics remain future explicit inputs.
    """

    definition_id: str
    represented_parent_baseline: Periodic2DRepresentedParentCalculationScaffold

    def __post_init__(self) -> None:
        """Require a stable identity and the exact represented-parent scaffold type."""
        _validate_definition_id(self.definition_id)
        if type(self.represented_parent_baseline) is not (
            Periodic2DRepresentedParentCalculationScaffold
        ):
            raise TypeError(
                "represented_parent_baseline must be "
                "Periodic2DRepresentedParentCalculationScaffold"
            )

    @property
    def parent_model(self) -> Periodic2DModel:
        """Return the exact parent model supplied by the M4 baseline."""
        return self.represented_parent_baseline.parent_model


__all__ = [
    "Periodic2DRepresentedParentCalculationScaffold",
    "Periodic2DShellGaugeLocalityCalculationScaffold",
]
