"""Periodic-3D study and orchestration bases."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.models import PeriodicModel
from ksdft2effmass.study.periodic import PeriodicStudy, PeriodicStudyOrchestrator


class Periodic3DStudy[ModelT: PeriodicModel](PeriodicStudy[ModelT], ABC):
    """Identify a study with three periodic spatial directions."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Prevent descendants from replacing three-dimensional identity."""
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic3DStudy subclasses cannot override spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[3]:
        """Return the exact built-in periodic spatial dimension three."""
        return 3


class Periodic3DStudyOrchestrator[
    ModelT: PeriodicModel,
    StudyT,
](PeriodicStudyOrchestrator[ModelT, StudyT], ABC):
    """Identify study orchestration for three periodic spatial directions."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Prevent descendants from replacing three-dimensional identity."""
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic3DStudyOrchestrator subclasses cannot override "
                "spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[3]:
        """Return the exact built-in periodic spatial dimension three."""
        return 3


__all__ = ["Periodic3DStudy", "Periodic3DStudyOrchestrator"]
