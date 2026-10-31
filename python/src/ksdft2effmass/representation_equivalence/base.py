"""Nominal scientific base for represented-operator equivalence."""

from __future__ import annotations

from abc import ABC


class RepresentationEquivalence(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify one equivalence assessment on explicitly aligned state spaces.

    Concrete subclasses must state the represented spaces and admitted basis or gauge
    action. Equality of eigenvalues alone is not representation equivalence. This base
    owns no alignment algorithm, tolerance, acceptance policy, or wire format.
    """

    __slots__ = ()


__all__ = ["RepresentationEquivalence"]
