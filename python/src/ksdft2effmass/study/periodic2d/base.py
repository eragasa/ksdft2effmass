"""Periodic-2D study and orchestration bases."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.models import PeriodicModel
from ksdft2effmass.study.periodic import PeriodicStudy, PeriodicStudyOrchestrator


class Periodic2DStudy[ModelT: PeriodicModel](PeriodicStudy[ModelT], ABC):
    """Identify a study with two periodic spatial directions."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Prevent descendants from replacing two-dimensional identity."""
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic2DStudy subclasses cannot override spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[2]:
        """Return the exact built-in periodic spatial dimension two."""
        return 2


class Periodic2DStudyOrchestrator[
    ModelT: PeriodicModel,
    StudyT,
](PeriodicStudyOrchestrator[ModelT, StudyT], ABC):
    """Identify study orchestration for two periodic spatial directions."""

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Prevent descendants from replacing two-dimensional identity."""
        super().__init_subclass__()
        if "spatial_dimension" in cls.__dict__:
            raise TypeError(
                "Periodic2DStudyOrchestrator subclasses cannot override "
                "spatial_dimension"
            )

    @property
    @final
    def spatial_dimension(self) -> Literal[2]:
        """Return the exact built-in periodic spatial dimension two."""
        return 2


__all__ = ["Periodic2DStudy", "Periodic2DStudyOrchestrator"]
