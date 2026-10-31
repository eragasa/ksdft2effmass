"""Nominal scientific base for state-space reduction."""

from __future__ import annotations

from abc import ABC


class SubspaceReduction(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify one explicit parent-space to retained-space reduction.

    Concrete subclasses must keep spectral selection, projection, coordinate
    compression, and discarded-state truncation distinguishable. This base owns no
    basis convention, tolerance, acceptance policy, or serialization format.
    """

    __slots__ = ()


__all__ = ["SubspaceReduction"]
