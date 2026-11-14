"""Nominal periodic-2D scientific-model bases."""

from abc import ABC, abstractmethod
from typing import Literal, final

from ksdft2effmass.periodic.models import PeriodicModel


class Periodic2DModel(PeriodicModel, ABC):
    """Identify a scientific model with two periodic spatial directions."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Reject attempts to replace the two-dimensional identity.

        Raises
        ------
        TypeError
            If a child declares its own ``spatial_dimension`` property.

        """
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic2DModel subclasses cannot override spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[2]:
        """Return the exact built-in integer two.

        Returns
        -------
        Literal[2]
            Built-in integer two.

        """
        return 2


class Periodic2DDefectModel(Periodic2DModel, ABC):
    """Identify a two-dimensional defect model with an explicit parent identity."""

    __slots__ = ()

    @property
    @abstractmethod
    def parent_model_id(self) -> str:
        """Return the stable nonempty identity of the pristine parent model.

        Returns
        -------
        str
            Identity of the defect-free scientific parent.

        """


__all__ = ["Periodic2DDefectModel", "Periodic2DModel"]
