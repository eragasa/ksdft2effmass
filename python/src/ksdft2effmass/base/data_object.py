"""Nominal root for workflow-owned data objects."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.base import DataObject


class AbstractDataObject(DataObject, ABC):
    """Nominal root for workflow-owned data objects."""

    __slots__ = ()
