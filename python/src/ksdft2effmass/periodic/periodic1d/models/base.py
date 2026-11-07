"""Nominal periodic-1D scientific-model bases."""

from abc import ABC, abstractmethod
from typing import Literal, final

from ksdft2effmass.periodic.models import PeriodicModel


class Periodic1DModel(PeriodicModel, ABC):
    """Identify a scientific model with one periodic spatial direction."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Reject attempts to replace the one-dimensional identity.

        Raises
        ------
        TypeError
            If a child declares its own ``spatial_dimension`` property.

        """
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic1DModel subclasses cannot override spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[1]:
        """Return the exact built-in integer one.

        Returns
        -------
        Literal[1]
            Built-in integer one.

        """
        return 1


class Periodic1DDefectModel(Periodic1DModel, ABC):
    """Identify a one-dimensional defect model with an explicit parent identity."""

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


__all__ = ["Periodic1DDefectModel", "Periodic1DModel"]
