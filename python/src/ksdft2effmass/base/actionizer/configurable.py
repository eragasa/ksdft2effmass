"""Configurable workflow data-object actionizer boundary."""

from __future__ import annotations

from abc import ABC

from ksdft2effmass.base import (
    DataObjectActionizer,
    DataObjectActionRequest,
    DataObjectActionResult,
)
from ksdft2effmass.base.actionizer.configuration import (
    AbstractActionConfiguration,
)
from ksdft2effmass.base.actionizer.request import (
    ConfigurableDataObjectActionRequest,
)


class ConfigurableDataObjectActionizer[
    ConfigurationT: AbstractActionConfiguration,
    RequestT: DataObjectActionRequest,
    ResultT: DataObjectActionResult,
](DataObjectActionizer[RequestT, ResultT], ABC):
    """Add exact immutable configuration typing to an actionizer."""

    __slots__ = ()

    configuration_type: type[ConfigurationT]

    def _require_configuration(
        self,
        *,
        request: ConfigurableDataObjectActionRequest[ConfigurationT],
    ) -> ConfigurationT:
        configuration = request.configuration
        if type(configuration) is not self.configuration_type:
            raise TypeError("action configuration contract differs")
        return configuration
