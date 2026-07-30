r"""Hermiticity analysis action objects."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .records import OperatorRecord


@dataclass(frozen=True, slots=True)
class HermiticityResult:
    """Immutable result of Hermiticity analysis.

    Parameters
    ----------
    residual
        Absolute entrywise maximum residual ``max(abs(H - H.conj().T))``.
    tolerance
        Finite non-negative tolerance used by the analyzer.
    is_hermitian
        Whether ``residual <= tolerance``.
    """

    residual: float
    tolerance: float
    is_hermitian: bool

    def __post_init__(self) -> None:
        residual = float(self.residual)
        tolerance = float(self.tolerance)
        if not np.isfinite(residual):
            msg = "Hermiticity residual must be finite"
            raise ValueError(msg)
        if not np.isfinite(tolerance):
            msg = "Hermiticity tolerance must be finite"
            raise ValueError(msg)
        if tolerance < 0.0:
            msg = "Hermiticity tolerance must be non-negative"
            raise ValueError(msg)
        object.__setattr__(self, "residual", residual)
        object.__setattr__(self, "tolerance", tolerance)
        object.__setattr__(self, "is_hermitian", bool(self.is_hermitian))


@dataclass(frozen=True, slots=True)
class HermiticityAnalyzer:
    """Action object for Hermiticity analysis and enforcement.

    The tolerance is analysis policy and is therefore stored on the analyzer,
    not on :class:`~ksdft2effmass.operators.OperatorRecord`.
    """

    tolerance: float = 1.0e-12

    def __post_init__(self) -> None:
        try:
            tolerance = float(self.tolerance)
        except (TypeError, ValueError) as exc:
            msg = "Hermiticity tolerance must be finite numeric metadata"
            raise ValueError(msg) from exc
        if not np.isfinite(tolerance):
            msg = "Hermiticity tolerance must be finite"
            raise ValueError(msg)
        if tolerance < 0.0:
            msg = "Hermiticity tolerance must be non-negative"
            raise ValueError(msg)
        object.__setattr__(self, "tolerance", tolerance)

    def execute(self, record: OperatorRecord) -> HermiticityResult:
        """Analyze ``record`` and return an immutable result object."""

        residual_matrix = record.matrix - record.matrix.conj().T
        residual = float(np.max(np.abs(residual_matrix)))
        return HermiticityResult(
            residual=residual,
            tolerance=self.tolerance,
            is_hermitian=residual <= self.tolerance,
        )

    def require(self, record: OperatorRecord) -> HermiticityResult:
        """Return the result or raise if the Hermiticity criterion fails."""

        result = self.execute(record)
        if not result.is_hermitian:
            msg = (
                "operator matrix is not Hermitian within tolerance: "
                f"residual={result.residual:.6g}, tolerance={result.tolerance:.6g}"
            )
            raise ValueError(msg)
        return result
