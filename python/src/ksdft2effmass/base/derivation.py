"""Nominal root for immutable workflow derivation records."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.base.immutable import AbstractImmutableDataObject


class AbstractDerivation(AbstractImmutableDataObject, ABC):
    """Nominal root for immutable workflow evidence-derived records."""

    __slots__ = ()
