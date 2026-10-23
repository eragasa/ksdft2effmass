"""D1 configuration for owner-supplied complex-unitary Procrustes operations."""

from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
    ComplexUnitaryProcrustesTolerance,
)


def higher_rank_d1_procrustes_tolerance() -> ComplexUnitaryProcrustesTolerance:
    """Return the frozen maximum-rule rank and integrity tolerance."""
    return ComplexUnitaryProcrustesTolerance(
        rank_absolute=1.0e-12,
        rank_relative=1.0e-10,
        validation_absolute=1.0e-12,
        validation_relative=1.0e-10,
        rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
    )


__all__ = ["higher_rank_d1_procrustes_tolerance"]
