"""Concrete periodic-2D rank-two study contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, final

from ksdft2effmass.periodic.periodic2d.rank2.models import (
    Periodic2DRank2BlockHoppingModel,
)
from ksdft2effmass.study.periodic import PeriodicStudyModelRole
from ksdft2effmass.study.periodic2d import (
    Periodic2DStudy,
    Periodic2DStudyOrchestrator,
)


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2Study(Periodic2DStudy[Periodic2DRank2BlockHoppingModel]):
    """Correlate one periodic-2D rank-two model with one study identity and role.

    Parameters
    ----------
    study_id
        Stable nonempty study identity, distinct from the scientific-model identity.
    model
        Exact complete periodic-2D rank-two block-hopping scientific model.
    model_role
        Explicit reference or candidate role in the named study comparison.

    Notes
    -----
    Ordered primitive vectors and their physical unit remain owned by the model. This
    value selects no metric-shell inventory, threshold, or analyzer policy.

    """

    study_id: str
    model: Periodic2DRank2BlockHoppingModel
    model_role: PeriodicStudyModelRole

    def __post_init__(self) -> None:
        """Validate exact study identity, model ownership, and comparison role."""
        if type(self.study_id) is not str:
            raise TypeError("study_id must be a built-in string")
        if not self.study_id:
            raise ValueError("study_id must be nonempty")
        if type(self.model) is not Periodic2DRank2BlockHoppingModel:
            raise TypeError("model must be Periodic2DRank2BlockHoppingModel")
        if type(self.model_role) is not PeriodicStudyModelRole:
            raise TypeError("model_role must be PeriodicStudyModelRole")

    @property
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained band-subspace rank two."""
        return 2


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2StudyOrchestrator(
    Periodic2DStudyOrchestrator[
        Periodic2DRank2BlockHoppingModel,
        Periodic2DRank2Study,
    ]
):
    """Construct one immutable periodic-2D rank-two study correlation."""

    study_id: str
    model: Periodic2DRank2BlockHoppingModel
    model_role: PeriodicStudyModelRole

    def __post_init__(self) -> None:
        """Validate exact orchestration inputs without coercion."""
        if type(self.study_id) is not str:
            raise TypeError("study_id must be a built-in string")
        if not self.study_id:
            raise ValueError("study_id must be nonempty")
        if type(self.model) is not Periodic2DRank2BlockHoppingModel:
            raise TypeError("model must be Periodic2DRank2BlockHoppingModel")
        if type(self.model_role) is not PeriodicStudyModelRole:
            raise TypeError("model_role must be PeriodicStudyModelRole")

    @property
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained band-subspace rank two."""
        return 2

    def execute(self) -> Periodic2DRank2Study:
        """Return the immutable one-model study correlation."""
        return Periodic2DRank2Study(
            study_id=self.study_id,
            model=self.model,
            model_role=self.model_role,
        )


__all__ = ["Periodic2DRank2Study", "Periodic2DRank2StudyOrchestrator"]
