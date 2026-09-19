"""Caller-toleranced direct--reciprocal lattice duality analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, PhysicalUnit

from .lattices import (
    DirectLattice,
    DirectLattice1D,
    DirectLattice2D,
    DirectLattice3D,
    LatticeBasisVectors,
    ReciprocalLattice,
    ReciprocalLattice1D,
    ReciprocalLattice2D,
    ReciprocalLattice3D,
)


@dataclass(frozen=True, slots=True)
class LatticeDualityResult:
    """Record direct--reciprocal duality analysis.

    Parameters
    ----------
    direct
        Exact direct basis analyzed.
    reciprocal
        Exact reciprocal basis analyzed.
    absolute_tolerance
        Positive finite dimensionless tolerance supplied by the caller.
    compatible
        True exactly when no issue code is retained.
    maximum_absolute_residual
        Maximum absolute component of ``A B^T - 2*pi*I`` after reciprocal-unit
        conversion, or ``None`` when dimensions or units prevent evaluation.
    issue_codes
        Sorted unique deterministic issue codes.
    """

    direct: DirectLattice
    reciprocal: ReciprocalLattice
    absolute_tolerance: float
    compatible: bool
    maximum_absolute_residual: float | None
    issue_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate correlated inputs, tolerance, residual, and issue ordering."""
        if not isinstance(
            self.direct, DirectLattice1D | DirectLattice2D | DirectLattice3D
        ):
            raise TypeError("direct must be a supported direct lattice")
        if not isinstance(
            self.reciprocal,
            ReciprocalLattice1D | ReciprocalLattice2D | ReciprocalLattice3D,
        ):
            raise TypeError("reciprocal must be a supported reciprocal lattice")
        if type(self.absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(self.absolute_tolerance) or self.absolute_tolerance <= 0.0:
            raise ValueError("absolute_tolerance must be positive and finite")
        if type(self.compatible) is not bool:
            raise TypeError("compatible must be bool")
        if self.maximum_absolute_residual is not None:
            if type(self.maximum_absolute_residual) is not float:
                raise TypeError("maximum_absolute_residual must be float or None")
            if not math.isfinite(self.maximum_absolute_residual):
                raise ValueError("maximum_absolute_residual must be finite")
            if self.maximum_absolute_residual < 0.0:
                raise ValueError("maximum_absolute_residual must be nonnegative")
        if type(self.issue_codes) is not tuple or any(
            type(code) is not str for code in self.issue_codes
        ):
            raise TypeError("issue_codes must be a tuple of strings")
        if self.issue_codes != tuple(sorted(set(self.issue_codes))):
            raise ValueError("issue_codes must be sorted and unique")
        if self.compatible == bool(self.issue_codes):
            raise ValueError("compatible status must agree with issue_codes")
        if self.maximum_absolute_residual is None and self.compatible:
            raise ValueError("compatible result must retain a duality residual")
        if self.maximum_absolute_residual is not None and self.compatible != (
            self.maximum_absolute_residual <= self.absolute_tolerance
        ):
            raise ValueError("compatible status must agree with residual and tolerance")


class LatticeDualityAnalyzer:
    """Analyze the represented relation ``A B^T = 2*pi*I``."""

    __slots__ = ()

    def execute(
        self,
        direct: DirectLattice,
        reciprocal: ReciprocalLattice,
        *,
        absolute_tolerance: float,
    ) -> LatticeDualityResult:
        """Return duality residuals after explicit reciprocal-unit conversion.

        Parameters
        ----------
        direct
            One supported direct lattice.
        reciprocal
            One supported reciprocal lattice.
        absolute_tolerance
            Positive finite built-in float applied componentwise to the dimensionless
            duality residual.
        """
        if not isinstance(direct, DirectLattice1D | DirectLattice2D | DirectLattice3D):
            raise TypeError("direct must be a supported direct lattice")
        if not isinstance(
            reciprocal,
            ReciprocalLattice1D | ReciprocalLattice2D | ReciprocalLattice3D,
        ):
            raise TypeError("reciprocal must be a supported reciprocal lattice")
        if type(absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(absolute_tolerance) or absolute_tolerance <= 0.0:
            raise ValueError("absolute_tolerance must be positive and finite")
        direct_dimension = (
            1
            if type(direct) is DirectLattice1D
            else 2
            if type(direct) is DirectLattice2D
            else 3
        )
        reciprocal_dimension = (
            1
            if type(reciprocal) is ReciprocalLattice1D
            else 2
            if type(reciprocal) is ReciprocalLattice2D
            else 3
        )
        if direct_dimension != reciprocal_dimension:
            return LatticeDualityResult(
                direct,
                reciprocal,
                absolute_tolerance,
                False,
                None,
                ("SOLID_STATE.LATTICE_DUALITY.DIMENSION_MISMATCH",),
            )
        target = PhysicalUnit(f"1 / ({direct.unit.expression})")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(reciprocal.unit, target):
            return LatticeDualityResult(
                direct,
                reciprocal,
                absolute_tolerance,
                False,
                None,
                ("SOLID_STATE.LATTICE_DUALITY.UNIT_MISMATCH",),
            )
        factor = MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(reciprocal.unit, target)
        direct_vectors: LatticeBasisVectors
        reciprocal_vectors: LatticeBasisVectors
        if type(direct) is DirectLattice1D and type(reciprocal) is ReciprocalLattice1D:
            direct_vectors = (direct.vector,)
            reciprocal_vectors = (reciprocal.vector,)
        elif (
            type(direct) is DirectLattice2D and type(reciprocal) is ReciprocalLattice2D
        ):
            direct_vectors = direct.vectors
            reciprocal_vectors = reciprocal.vectors
        elif (
            type(direct) is DirectLattice3D and type(reciprocal) is ReciprocalLattice3D
        ):
            direct_vectors = direct.vectors
            reciprocal_vectors = reciprocal.vectors
        else:
            return LatticeDualityResult(
                direct,
                reciprocal,
                absolute_tolerance,
                False,
                None,
                ("SOLID_STATE.LATTICE_DUALITY.DIMENSION_MISMATCH",),
            )
        maximum = 0.0
        for row, direct_vector in enumerate(direct_vectors):
            for column, reciprocal_vector in enumerate(reciprocal_vectors):
                value = math.fsum(
                    direct_component * reciprocal_component * factor
                    for direct_component, reciprocal_component in zip(
                        direct_vector, reciprocal_vector, strict=True
                    )
                )
                expected = 2.0 * math.pi if row == column else 0.0
                maximum = max(maximum, abs(value - expected))
        issues = (
            ()
            if maximum <= absolute_tolerance
            else ("SOLID_STATE.LATTICE_DUALITY.RESIDUAL_EXCEEDED",)
        )
        return LatticeDualityResult(
            direct,
            reciprocal,
            absolute_tolerance,
            not issues,
            maximum,
            issues,
        )
