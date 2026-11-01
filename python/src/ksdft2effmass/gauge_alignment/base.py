"""Nominal scientific base for retained-space gauge alignment."""

from __future__ import annotations

from abc import ABC


class GaugeAlignment(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify a gauge-alignment capability or its exact applicability boundary.

    Concrete subclasses must state the represented state space, gauge group, action
    convention, and whether a nontrivial alignment exists. Membership does not imply
    representation equivalence, frame transport, coefficient locality, support
    truncation, or successful numerical recovery. This base owns no solver, tolerance,
    acceptance policy, or wire format.
    """

    __slots__ = ()


__all__ = ["GaugeAlignment"]
