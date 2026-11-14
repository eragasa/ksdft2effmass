"""Nominal periodic-3D scientific-model bases."""

from abc import ABC, abstractmethod
from typing import Literal, final

from ksdft2effmass.periodic.models import PeriodicModel


class Periodic3DModel(PeriodicModel, ABC):
    """Identify a scientific model with three periodic spatial directions."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Reject attempts to replace the three-dimensional identity.

        Raises
        ------
        TypeError
            If a child declares its own ``spatial_dimension`` property.

        """
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic3DModel subclasses cannot override spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[3]:
        """Return the exact built-in integer three.

        Returns
        -------
        Literal[3]
            Built-in integer three.

        """
        return 3


class Periodic3DDefectModel(Periodic3DModel, ABC):
    """Identify a three-dimensional defect model with an explicit parent identity."""

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


__all__ = ["Periodic3DDefectModel", "Periodic3DModel"]
