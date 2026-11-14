"""Nominal root for KSD scientific models."""

from abc import ABC, abstractmethod


class Model(ABC):
    """Identify one KSD-owned scientific model.

    The root fixes only stable scientific identity. Domain, geometry, rank,
    representation, provider integration, and campaign policy belong to narrower
    owners.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Return the stable nonempty scientific-model identity.

        Returns
        -------
        str
            Identity used to correlate the model without implying validation.

        """


__all__ = ["Model"]
