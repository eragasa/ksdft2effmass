"""Factored Bravais lattice classifications and metric compatibility analysis.

Bravais classification combines a dimension-specific lattice system with a declared
conventional-cell centering. Classification records validate the standard 1, 5, and 14
system--centering combinations. They do not infer a classification from basis vectors;
caller-toleranced metric compatibility belongs to
:class:`BravaisMetricCompatibilityAnalyzer`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .lattices import DirectLattice, LatticeBasisVectors


type BravaisLattice = BravaisLattice1D | BravaisLattice2D | BravaisLattice3D


class BravaisCentering(StrEnum):
    """Conventional-cell centering used by supported Bravais classifications.

    ``P`` is primitive, ``C`` is the canonical base-centered setting, ``I`` is
    body-centered, ``F`` is face-centered, and ``R`` is rhombohedral centering.
    Axis-specific ``A`` or ``B`` settings must be transformed to the declared
    canonical ``C`` setting before construction.
    """

    P = "P"
    C = "C"
    I = "I"  # noqa: E741 - conventional body-centering symbol
    F = "F"
    R = "R"


class LatticeSystem1D(StrEnum):
    """One-dimensional lattice systems."""

    LINE = "line"


class LatticeSystem2D(StrEnum):
    """Two-dimensional lattice systems before centering is applied."""

    OBLIQUE = "oblique"
    RECTANGULAR = "rectangular"
    SQUARE = "square"
    HEXAGONAL = "hexagonal"


class LatticeSystem3D(StrEnum):
    """Three-dimensional lattice systems before centering is applied."""

    TRICLINIC = "triclinic"
    MONOCLINIC = "monoclinic"
    ORTHORHOMBIC = "orthorhombic"
    TETRAGONAL = "tetragonal"
    RHOMBOHEDRAL = "rhombohedral"
    HEXAGONAL = "hexagonal"
    CUBIC = "cubic"


@dataclass(frozen=True, slots=True)
class BravaisLattice1D:
    """Represent the unique one-dimensional Bravais classification.

    Parameters
    ----------
    system
        Must be :attr:`LatticeSystem1D.LINE`.
    centering
        Must be :attr:`BravaisCentering.P`.
    """

    system: LatticeSystem1D
    centering: BravaisCentering

    def __post_init__(self) -> None:
        """Validate the unique 1D system-centering combination."""
        if type(self.system) is not LatticeSystem1D:
            raise TypeError("system must be LatticeSystem1D")
        if type(self.centering) is not BravaisCentering:
            raise TypeError("centering must be BravaisCentering")
        if (
            self.system is not LatticeSystem1D.LINE
            or self.centering is not BravaisCentering.P
        ):
            raise ValueError("one-dimensional Bravais lattice must be line P")


@dataclass(frozen=True, slots=True)
class BravaisLattice2D:
    """Represent one of the five two-dimensional Bravais classifications.

    Parameters
    ----------
    system
        Declared two-dimensional lattice system.
    centering
        Conventional-cell centering valid for ``system``.
    """

    system: LatticeSystem2D
    centering: BravaisCentering

    def __post_init__(self) -> None:
        """Validate the selected 2D system-centering combination."""
        if type(self.system) is not LatticeSystem2D:
            raise TypeError("system must be LatticeSystem2D")
        if type(self.centering) is not BravaisCentering:
            raise TypeError("centering must be BravaisCentering")
        allowed = {
            LatticeSystem2D.OBLIQUE: (BravaisCentering.P,),
            LatticeSystem2D.RECTANGULAR: (
                BravaisCentering.P,
                BravaisCentering.C,
            ),
            LatticeSystem2D.SQUARE: (BravaisCentering.P,),
            LatticeSystem2D.HEXAGONAL: (BravaisCentering.P,),
        }
        if self.centering not in allowed[self.system]:
            raise ValueError("unsupported two-dimensional system-centering combination")


@dataclass(frozen=True, slots=True)
class BravaisLattice3D:
    """Represent one of the fourteen three-dimensional Bravais classifications.

    Parameters
    ----------
    system
        Declared three-dimensional lattice system.
    centering
        Conventional-cell centering valid for ``system``.
    """

    system: LatticeSystem3D
    centering: BravaisCentering

    def __post_init__(self) -> None:
        """Validate the selected 3D system-centering combination."""
        if type(self.system) is not LatticeSystem3D:
            raise TypeError("system must be LatticeSystem3D")
        if type(self.centering) is not BravaisCentering:
            raise TypeError("centering must be BravaisCentering")
        allowed = {
            LatticeSystem3D.TRICLINIC: (BravaisCentering.P,),
            LatticeSystem3D.MONOCLINIC: (
                BravaisCentering.P,
                BravaisCentering.C,
            ),
            LatticeSystem3D.ORTHORHOMBIC: (
                BravaisCentering.P,
                BravaisCentering.C,
                BravaisCentering.I,
                BravaisCentering.F,
            ),
            LatticeSystem3D.TETRAGONAL: (
                BravaisCentering.P,
                BravaisCentering.I,
            ),
            LatticeSystem3D.RHOMBOHEDRAL: (BravaisCentering.R,),
            LatticeSystem3D.HEXAGONAL: (BravaisCentering.P,),
            LatticeSystem3D.CUBIC: (
                BravaisCentering.P,
                BravaisCentering.I,
                BravaisCentering.F,
            ),
        }
        if self.centering not in allowed[self.system]:
            raise ValueError(
                "unsupported three-dimensional system-centering combination"
            )


@dataclass(frozen=True, slots=True)
class BravaisMetricCompatibilityResult:
    """Record compatibility of a direct basis with declared Bravais metric invariants.

    Parameters
    ----------
    direct
        Exact direct basis analyzed.
    bravais
        Exact declared Bravais classification analyzed.
    relative_tolerance
        Positive finite dimensionless tolerance supplied by the caller.
    compatible
        True exactly when no issue code is retained.
    maximum_dimensionless_residual
        Largest normalized metric-invariant residual, or ``None`` when dimensions
        prevent evaluation.
    issue_codes
        Sorted unique deterministic issue codes.

    Notes
    -----
    Compatibility establishes required metric invariants, not a unique maximal-symmetry
    classification. For example, a square metric also satisfies rectangular
    orthogonality. Conventional settings are: monoclinic unique axis ``b``, hexagonal
    ``a``--``b`` angle 60 or 120 degrees, and canonical base-centering ``C``.
    """

    direct: DirectLattice
    bravais: BravaisLattice
    relative_tolerance: float
    compatible: bool
    maximum_dimensionless_residual: float | None
    issue_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate correlated result state and deterministic findings."""
        from .lattices import DirectLattice1D, DirectLattice2D, DirectLattice3D

        if not isinstance(
            self.direct, DirectLattice1D | DirectLattice2D | DirectLattice3D
        ):
            raise TypeError("direct must be a supported direct lattice")
        if not isinstance(
            self.bravais, BravaisLattice1D | BravaisLattice2D | BravaisLattice3D
        ):
            raise TypeError("bravais must be a supported Bravais classification")
        if type(self.relative_tolerance) is not float:
            raise TypeError("relative_tolerance must be a built-in float")
        if not math.isfinite(self.relative_tolerance) or self.relative_tolerance <= 0.0:
            raise ValueError("relative_tolerance must be positive and finite")
        if type(self.compatible) is not bool:
            raise TypeError("compatible must be bool")
        if self.maximum_dimensionless_residual is not None:
            if type(self.maximum_dimensionless_residual) is not float:
                raise TypeError("maximum_dimensionless_residual must be float or None")
            if not math.isfinite(self.maximum_dimensionless_residual):
                raise ValueError("maximum_dimensionless_residual must be finite")
            if self.maximum_dimensionless_residual < 0.0:
                raise ValueError("maximum_dimensionless_residual must be nonnegative")
        if type(self.issue_codes) is not tuple or any(
            type(code) is not str for code in self.issue_codes
        ):
            raise TypeError("issue_codes must be a tuple of strings")
        if self.issue_codes != tuple(sorted(set(self.issue_codes))):
            raise ValueError("issue_codes must be sorted and unique")
        if self.compatible == bool(self.issue_codes):
            raise ValueError("compatible status must agree with issue_codes")
        if self.maximum_dimensionless_residual is None and self.compatible:
            raise ValueError("compatible result must retain a metric residual")
        if self.maximum_dimensionless_residual is not None and self.compatible != (
            self.maximum_dimensionless_residual <= self.relative_tolerance
        ):
            raise ValueError("compatible status must agree with residual and tolerance")


class BravaisMetricCompatibilityAnalyzer:
    """Analyze normalized conventional-cell metric invariants for a Bravais type."""

    __slots__ = ()

    def execute(
        self,
        direct: DirectLattice,
        bravais: BravaisLattice,
        *,
        relative_tolerance: float,
    ) -> BravaisMetricCompatibilityResult:
        """Return caller-toleranced metric compatibility.

        The residuals are normalized by the largest squared basis-vector length, except
        angle residuals, which compare dimensionless cosines. The action checks required
        invariants only and does not infer a unique highest-symmetry classification.
        """
        from .lattices import DirectLattice1D, DirectLattice2D, DirectLattice3D

        if not isinstance(direct, DirectLattice1D | DirectLattice2D | DirectLattice3D):
            raise TypeError("direct must be a supported direct lattice")
        if not isinstance(
            bravais, BravaisLattice1D | BravaisLattice2D | BravaisLattice3D
        ):
            raise TypeError("bravais must be a supported Bravais classification")
        if type(relative_tolerance) is not float:
            raise TypeError("relative_tolerance must be a built-in float")
        if not math.isfinite(relative_tolerance) or relative_tolerance <= 0.0:
            raise ValueError("relative_tolerance must be positive and finite")
        matching = (
            (type(direct) is DirectLattice1D and type(bravais) is BravaisLattice1D)
            or (type(direct) is DirectLattice2D and type(bravais) is BravaisLattice2D)
            or (type(direct) is DirectLattice3D and type(bravais) is BravaisLattice3D)
        )
        if not matching:
            return BravaisMetricCompatibilityResult(
                direct,
                bravais,
                relative_tolerance,
                False,
                None,
                ("SOLID_STATE.BRAVAIS_METRIC.DIMENSION_MISMATCH",),
            )
        vectors: LatticeBasisVectors
        if isinstance(direct, DirectLattice1D):
            vectors = (direct.vector,)
        elif isinstance(direct, DirectLattice2D | DirectLattice3D):
            vectors = direct.vectors
        else:
            raise AssertionError("validated direct lattice type was lost")
        gram = tuple(
            tuple(
                math.fsum(
                    left * right for left, right in zip(first, second, strict=True)
                )
                for second in vectors
            )
            for first in vectors
        )
        scale = max(gram[index][index] for index in range(len(gram)))
        residuals: list[float] = []
        if type(bravais) is BravaisLattice2D:
            if bravais.system is LatticeSystem2D.RECTANGULAR:
                residuals.append(abs(self._cosine(gram, 0, 1)))
            elif bravais.system is LatticeSystem2D.SQUARE:
                residuals.extend(
                    (
                        abs(self._cosine(gram, 0, 1)),
                        abs(gram[0][0] - gram[1][1]) / scale,
                    )
                )
            elif bravais.system is LatticeSystem2D.HEXAGONAL:
                residuals.extend(
                    (
                        abs(gram[0][0] - gram[1][1]) / scale,
                        abs(abs(self._cosine(gram, 0, 1)) - 0.5),
                    )
                )
        elif type(bravais) is BravaisLattice3D:
            if bravais.system is LatticeSystem3D.MONOCLINIC:
                residuals.extend(
                    (
                        abs(self._cosine(gram, 0, 1)),
                        abs(self._cosine(gram, 1, 2)),
                    )
                )
            elif bravais.system is LatticeSystem3D.ORTHORHOMBIC:
                residuals.extend(self._orthogonality(gram))
            elif bravais.system is LatticeSystem3D.TETRAGONAL:
                residuals.extend(self._orthogonality(gram))
                residuals.append(abs(gram[0][0] - gram[1][1]) / scale)
            elif bravais.system is LatticeSystem3D.RHOMBOHEDRAL:
                residuals.extend(self._equal_lengths(gram, scale))
                cosines = (
                    self._cosine(gram, 0, 1),
                    self._cosine(gram, 0, 2),
                    self._cosine(gram, 1, 2),
                )
                residuals.extend(
                    (
                        abs(cosines[0] - cosines[1]),
                        abs(cosines[0] - cosines[2]),
                    )
                )
            elif bravais.system is LatticeSystem3D.HEXAGONAL:
                residuals.extend(
                    (
                        abs(self._cosine(gram, 0, 2)),
                        abs(self._cosine(gram, 1, 2)),
                        abs(gram[0][0] - gram[1][1]) / scale,
                        abs(abs(self._cosine(gram, 0, 1)) - 0.5),
                    )
                )
            elif bravais.system is LatticeSystem3D.CUBIC:
                residuals.extend(self._orthogonality(gram))
                residuals.extend(self._equal_lengths(gram, scale))
        maximum = max((abs(value) for value in residuals), default=0.0)
        issues = (
            ()
            if maximum <= relative_tolerance
            else ("SOLID_STATE.BRAVAIS_METRIC.RESIDUAL_EXCEEDED",)
        )
        return BravaisMetricCompatibilityResult(
            direct,
            bravais,
            relative_tolerance,
            not issues,
            maximum,
            issues,
        )

    @staticmethod
    def _cosine(gram: tuple[tuple[float, ...], ...], left: int, right: int) -> float:
        """Return one dimensionless cosine from a positive Gram diagonal."""
        return gram[left][right] / math.sqrt(gram[left][left] * gram[right][right])

    @staticmethod
    def _orthogonality(
        gram: tuple[tuple[float, ...], ...],
    ) -> tuple[float, float, float]:
        """Return absolute cosine residuals for three axis pairs."""
        return (
            abs(BravaisMetricCompatibilityAnalyzer._cosine(gram, 0, 1)),
            abs(BravaisMetricCompatibilityAnalyzer._cosine(gram, 0, 2)),
            abs(BravaisMetricCompatibilityAnalyzer._cosine(gram, 1, 2)),
        )

    @staticmethod
    def _equal_lengths(
        gram: tuple[tuple[float, ...], ...], scale: float
    ) -> tuple[float, float]:
        """Return normalized three-dimensional equal-length residuals."""
        return (
            abs(gram[0][0] - gram[1][1]) / scale,
            abs(gram[0][0] - gram[2][2]) / scale,
        )
