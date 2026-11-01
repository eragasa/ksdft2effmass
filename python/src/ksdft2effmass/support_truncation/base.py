"""Nominal scientific base for irreversible support truncation."""

from __future__ import annotations

from abc import ABC


class SupportTruncation(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify irreversible removal from a declared representation support.

    Concrete subclasses must identify the represented object, support index space,
    retained and omitted support, and any closure rule needed by that representation.
    This base does not select a physical domain, geometry, algorithm, tolerance,
    acceptance policy, or wire format.
    """

    __slots__ = ()


__all__ = ["SupportTruncation"]
