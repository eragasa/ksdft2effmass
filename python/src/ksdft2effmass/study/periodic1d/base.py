"""Periodic-1D study and orchestration bases."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.models import PeriodicModel
from ksdft2effmass.study.periodic import PeriodicStudy, PeriodicStudyOrchestrator


class Periodic1DStudy[ModelT: PeriodicModel](PeriodicStudy[ModelT], ABC):
    """Identify a study with one periodic spatial direction."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Prevent descendants from replacing one-dimensional identity."""
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic1DStudy subclasses cannot override spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[1]:
        """Return the exact built-in periodic spatial dimension one."""
        return 1


class Periodic1DStudyOrchestrator[
    ModelT: PeriodicModel,
    StudyT,
](PeriodicStudyOrchestrator[ModelT, StudyT], ABC):
    """Identify study orchestration for one periodic spatial direction."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Prevent descendants from replacing one-dimensional identity."""
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic1DStudyOrchestrator subclasses cannot override "
                "spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[1]:
        """Return the exact built-in periodic spatial dimension one."""
        return 1


__all__ = ["Periodic1DStudy", "Periodic1DStudyOrchestrator"]
