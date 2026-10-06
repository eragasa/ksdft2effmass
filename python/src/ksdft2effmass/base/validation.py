"""Nominal root for immutable workflow validation records."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.base.immutable import AbstractImmutableDataObject


class AbstractValidation(AbstractImmutableDataObject, ABC):
    """Nominal root for immutable workflow contract-validation records."""

    __slots__ = ()
