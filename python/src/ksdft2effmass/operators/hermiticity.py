r"""Hermiticity analysis result and action object.

Hermiticity is measured for an operator record matrix ``H`` by the entrywise
maximum residual

.. math::

   \epsilon_H = \max_{i,j} |H_{ij} - H_{ji}^*|.

The acceptance policy ``epsilon_H <= tau`` belongs to
:class:`HermiticityAnalyzer`, not to the represented data object.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .records import OperatorRecord


def _finite_real(value: Any, name: str) -> float:
    """Return a Python float for documented real scalar validation rules."""

    if isinstance(value, bool | np.bool_ | str | bytes | complex | np.complexfloating):
        msg = f"{name} must be a real number"
        raise TypeError(msg)
    if not isinstance(value, int | float | np.integer | np.floating):
        msg = f"{name} must be a real number"
        raise TypeError(msg)
    real = float(value)
    if not np.isfinite(real):
        msg = f"{name} must be finite"
        raise ValueError(msg)
    return real


@dataclass(frozen=True, slots=True)
class HermiticityResult:
    """Immutable result of Hermiticity analysis.

    Parameters
    ----------
    residual
        Absolute entrywise maximum residual ``max(abs(H - H.conj().T))``.
    tolerance
        Finite non-negative tolerance used by the analyzer.

    Raises
    ------
    ValueError
        If ``residual`` or ``tolerance`` is nonfinite, or if ``tolerance`` is
        negative.
    """

    residual: float
    tolerance: float

    def __post_init__(self) -> None:
        residual = _finite_real(self.residual, "Hermiticity residual")
        tolerance = _finite_real(self.tolerance, "Hermiticity tolerance")
        if residual < 0.0:
            msg = "Hermiticity residual must be non-negative"
            raise ValueError(msg)
        if tolerance < 0.0:
            msg = "Hermiticity tolerance must be non-negative"
            raise ValueError(msg)
        object.__setattr__(self, "residual", residual)
        object.__setattr__(self, "tolerance", tolerance)

    @property
    def is_hermitian(self) -> bool:
        """Whether ``residual <= tolerance`` for the analyzer tolerance."""

        return self.residual <= self.tolerance


@dataclass(frozen=True, slots=True)
class HermiticityAnalyzer:
    """Action object for Hermiticity analysis and enforcement.

    The tolerance ``tau`` is analysis policy and is therefore stored on the
    analyzer, not on :class:`~ksdft2effmass.operators.OperatorRecord`.
    """

    tolerance: float = 1.0e-12

    def __post_init__(self) -> None:
        tolerance = _finite_real(self.tolerance, "Hermiticity tolerance")
        if tolerance < 0.0:
            msg = "Hermiticity tolerance must be non-negative"
            raise ValueError(msg)
        object.__setattr__(self, "tolerance", tolerance)

    def execute(self, record: OperatorRecord) -> HermiticityResult:
        """Analyze ``record`` and return an immutable result object."""

        residual_matrix = record.matrix - record.matrix.conj().T
        residual = float(np.max(np.abs(residual_matrix)))
        return HermiticityResult(residual=residual, tolerance=self.tolerance)

    def require(self, record: OperatorRecord) -> HermiticityResult:
        """Return the result or raise if the Hermiticity criterion fails.

        Raises
        ------
        ValueError
            If ``max(abs(H - H.conj().T))`` exceeds this analyzer's tolerance.
        """

        result = self.execute(record)
        if not result.is_hermitian:
            msg = (
                "operator matrix is not Hermitian within tolerance: "
                f"residual={result.residual:.6g}, tolerance={result.tolerance:.6g}"
            )
            raise ValueError(msg)
        return result
