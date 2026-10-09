"""Nominal configuration shared by configurable workflow actions."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.base.immutable import AbstractImmutableDataObject


class AbstractActionConfiguration(AbstractImmutableDataObject, ABC):
    """Require one stable identity for complete action configuration."""

    __slots__ = ()

    configuration_id: str
