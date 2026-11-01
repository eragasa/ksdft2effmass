"""Matrix-field normalization admission."""

from __future__ import annotations

from projectkoios.numerics.validation import exact_finite_float


def positive_norm_energy_scale(value: float) -> float:
    """Validate one positive finite binary64 normalization energy scale."""
    result = exact_finite_float(value, "norm_energy_scale")
    if result <= 0.0:
        raise ValueError("norm_energy_scale must be positive")
    return result


__all__ = ["positive_norm_energy_scale"]
