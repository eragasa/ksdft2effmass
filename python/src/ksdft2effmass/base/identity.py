"""Nominal root for immutable workflow identity records."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.base.immutable import AbstractImmutableDataObject


class AbstractIdentity(AbstractImmutableDataObject, ABC):
    """Nominal root for immutable workflow identity records."""

    __slots__ = ()
