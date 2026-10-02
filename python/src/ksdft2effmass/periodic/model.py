"""Nominal scientific-model hierarchy for one to three periodic dimensions."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Literal, final

SpatialDimension = Literal[1, 2, 3]


class PeriodicModelRole(Enum):
    """Classify the evidentiary role of a periodic scientific model.

    ``TOY`` identifies a controlled model used to isolate mathematical, numerical,
    or software behavior. ``MATERIAL_REFERENCE`` identifies an explicitly specified
    material model without implying scientific validation or physical completeness.
    """

    TOY = "toy"
    MATERIAL_REFERENCE = "material_reference"


class PeriodicModel(ABC):
    """Define enforced nominal membership in the periodic scientific hierarchy.

    Concrete models must provide a stable nonempty model identity and an exact model
    role. A dimension-specific nominal base supplies the spatial dimension. The base
    owns no campaign, execution, serializer, tolerance, represented operator, or
    scientific-acceptance behavior.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Return the stable nonempty identity of the scientific model."""

    @property
    @abstractmethod
    def model_role(self) -> PeriodicModelRole:
        """Return the exact toy or material-reference role of the model."""

    @property
    @abstractmethod
    def spatial_dimension(self) -> SpatialDimension:
        """Return the exact built-in spatial dimension represented by the model."""


class Periodic1DModel(PeriodicModel, ABC):
    """Identify a scientific model with one periodic spatial direction."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Reject attempts to override the enforced one-dimensional identity."""
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic1DModel subclasses cannot override spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[1]:
        """Return the exact built-in integer one."""
        return 1


class Periodic2DModel(PeriodicModel, ABC):
    """Identify a scientific model with two periodic spatial directions."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Reject attempts to override the enforced two-dimensional identity."""
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic2DModel subclasses cannot override spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[2]:
        """Return the exact built-in integer two."""
        return 2


class Periodic3DModel(PeriodicModel, ABC):
    """Identify a scientific model with three periodic spatial directions."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Reject attempts to override the enforced three-dimensional identity."""
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic3DModel subclasses cannot override spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[3]:
        """Return the exact built-in integer three."""
        return 3


class Periodic1DDefectModel(Periodic1DModel, ABC):
    """Identify a one-dimensional defect model with an explicit parent identity."""

    __slots__ = ()

    @property
    @abstractmethod
    def parent_model_id(self) -> str:
        """Return the stable nonempty identity of the pristine parent model."""


class Periodic2DDefectModel(Periodic2DModel, ABC):
    """Identify a two-dimensional defect model with an explicit parent identity."""

    __slots__ = ()

    @property
    @abstractmethod
    def parent_model_id(self) -> str:
        """Return the stable nonempty identity of the pristine parent model."""


class Periodic3DDefectModel(Periodic3DModel, ABC):
    """Identify a three-dimensional defect model with an explicit parent identity."""

    __slots__ = ()

    @property
    @abstractmethod
    def parent_model_id(self) -> str:
        """Return the stable nonempty identity of the pristine parent model."""


__all__ = [
    "Periodic1DDefectModel",
    "Periodic1DModel",
    "Periodic2DDefectModel",
    "Periodic2DModel",
    "Periodic3DDefectModel",
    "Periodic3DModel",
    "PeriodicModel",
    "PeriodicModelRole",
    "SpatialDimension",
]
