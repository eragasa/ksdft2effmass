"""Shared strict scalar validation for active experiment contracts."""

from __future__ import annotations

import math


def _finite_float(name: str, value: float) -> None:
    """Reject booleans, strings, non-built-in scalars, and nonfinite values."""
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
