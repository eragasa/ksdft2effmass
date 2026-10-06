"""Nominal request accepted by configurable workflow actionizers."""

from __future__ import annotations

from abc import ABC
from typing import ClassVar

from ksdft2effmass.base import DataObjectActionRequest
from ksdft2effmass.base.actionizer.configuration import (
    AbstractActionConfiguration,
)


class ConfigurableDataObjectActionRequest[
    ConfigurationT: AbstractActionConfiguration,
](DataObjectActionRequest, ABC):
    """Require one complete immutable configuration on an action request."""

    __slots__ = ()

    CONTRACT_NAME: ClassVar[str]
    configuration: ConfigurationT
