"""Fail-closed finite-quotient admission for the selected rank-N Bain map.

The predicate in this module mirrors the exact arithmetic contract proved in
``projectkoios-formal`` merge commit
``b98d23fe23bb5bc940c6be4cfcbc79c3569c45e7``.  It validates KSD-owned runtime
period inputs only.  Executing this Python code is not a Lean proof and does not
establish mesh convergence or scientific adequacy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

BainPeriodTriple = tuple[int, int, int]
BainIntegerMatrix3 = tuple[
    tuple[int, int, int],
    tuple[int, int, int],
    tuple[int, int, int],
]


def periodic3d_bain_finite_quotient_is_admitted(
    periods: BainPeriodTriple,
) -> bool:
    """Return whether ``periods`` satisfy the exact Bain quotient criterion.

    The coordinate order is ``(N1, N2, N3)``. Periods are dimensionless
    cell-count moduli represented by arbitrary-precision built-in Python
    integers, so fixed-width overflow does not occur. Admission requires
    positive integers, ``N2 == N3``, and ``N1`` dividing ``N2``. Unsupported
    runtime values return ``False`` rather than receiving a fallback map.
    """
    if type(periods) is not tuple or len(periods) != 3:
        return False
    if any(type(period) is not int or period <= 0 for period in periods):
        return False
    first, second, third = periods
    return second == third and second % first == 0


@dataclass(frozen=True, slots=True)
class Periodic3DBainFiniteQuotientAdmissionCertificate:
    """Certify one runtime period triple against the reviewed exact criterion.

    Construction fails closed. Periods are dimensionless cell-count moduli
    represented by arbitrary-precision built-in Python integers, so fixed-width
    overflow does not occur. The retained object certifies only that the
    supplied periods satisfy the theorem's arithmetic hypotheses for the fixed
    matrices. It does not authenticate a mesh object or result.
    """

    FORMAL_REPOSITORY: ClassVar[str] = (
        "https://github.com/eragasa/projectkoios-formal.git"
    )
    FORMAL_MERGE_COMMIT: ClassVar[str] = "b98d23fe23bb5bc940c6be4cfcbc79c3569c45e7"
    FORMAL_PULL_REQUEST: ClassVar[int] = 58
    FORMAL_ADMISSION_THEOREM: ClassVar[str] = (
        "ProjectKoios.Crosswalks.PhysKit.bainMixedModuliAdmissionCertificate_iff"
    )
    FORMAL_BIJECTION_THEOREM: ClassVar[str] = (
        "ProjectKoios.Crosswalks.PhysKit."
        "bain_integerDiagonalLattice_quotientMap_bijective"
    )
    BAIN_TO_FCC_MATRIX: ClassVar[BainIntegerMatrix3] = (
        (1, 1, 0),
        (0, 0, 1),
        (0, -1, 0),
    )
    FCC_TO_BAIN_MATRIX: ClassVar[BainIntegerMatrix3] = (
        (1, 0, 1),
        (0, 0, -1),
        (0, 1, 0),
    )

    periods: BainPeriodTriple

    def __post_init__(self) -> None:
        if type(self.periods) is not tuple or len(self.periods) != 3:
            raise TypeError("periods must be an exact three-tuple")
        if any(type(period) is not int for period in self.periods):
            raise TypeError("periods must contain built-in integers")
        if any(period <= 0 for period in self.periods):
            raise ValueError("periods must be positive")
        first, second, third = self.periods
        if second != third:
            raise ValueError("Bain finite quotient requires N2 == N3")
        if second % first != 0:
            raise ValueError("Bain finite quotient requires N1 to divide N2")

    @property
    def first_period(self) -> int:
        """Return ``N1`` in the theorem-to-runtime coordinate order."""
        return self.periods[0]

    @property
    def second_period(self) -> int:
        """Return ``N2`` in the theorem-to-runtime coordinate order."""
        return self.periods[1]

    @property
    def third_period(self) -> int:
        """Return ``N3`` in the theorem-to-runtime coordinate order."""
        return self.periods[2]


__all__ = [
    "BainIntegerMatrix3",
    "BainPeriodTriple",
    "Periodic3DBainFiniteQuotientAdmissionCertificate",
    "periodic3d_bain_finite_quotient_is_admitted",
]
