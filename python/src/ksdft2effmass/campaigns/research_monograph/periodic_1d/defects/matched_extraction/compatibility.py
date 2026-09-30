"""Represented-operator compatibility for matched defect extraction."""

from __future__ import annotations

from .records import (
    CompatibilityResult,
    RepresentedOperator,
)


class MatchedDefectOperatorCompatibilityAnalyzer:
    """Check every represented convention needed before direct subtraction."""

    __slots__ = ()

    def execute(
        self, reference: RepresentedOperator, candidate: RepresentedOperator
    ) -> CompatibilityResult:
        """Compare every declared convention required for direct subtraction.

        Parameters
        ----------
        reference, candidate
            Represented finite operators to compare without implicit conversion.

        Returns
        -------
        CompatibilityResult
            Compatible status or sorted structured stop codes.
        """
        left = reference.basis
        right = candidate.basis
        fields = (
            ("STATE_SPACE", left.state_space_id, right.state_space_id),
            ("DIMENSION", left.dimension, right.dimension),
            ("CELL_COUNT", left.cell_count, right.cell_count),
            ("ORBITAL_COUNT", left.orbital_count, right.orbital_count),
            ("SPIN_COUNT", left.spin_count, right.spin_count),
            ("MOMENTUM", left.reduced_momentum, right.reduced_momentum),
            ("SITE_ORDER", left.site_ordering, right.site_ordering),
            ("ORBITAL_ORDER", left.orbital_ordering, right.orbital_ordering),
            ("SPIN_ORDER", left.spin_ordering, right.spin_ordering),
            ("COORDINATE_FRAME", left.coordinate_frame, right.coordinate_frame),
            ("ENERGY_UNIT", left.energy_unit, right.energy_unit),
            ("ENERGY_REFERENCE", left.energy_reference, right.energy_reference),
            ("GEOMETRY", left.geometry_id, right.geometry_id),
            ("SUBSPACE", left.subspace_id, right.subspace_id),
        )
        issues = tuple(
            sorted(
                f"DEFECT.COMPATIBILITY.{code}"
                for code, first, second in fields
                if first != second
            )
        )
        return CompatibilityResult("stopped" if issues else "compatible", issues)
