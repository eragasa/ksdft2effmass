"""Concrete periodic-1D rank-two study contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, final

from ksdft2effmass.periodic.periodic1d.rank2.models import (
    Periodic1DRank2BlockHoppingModel,
)
from ksdft2effmass.study.periodic import PeriodicStudyModelRole
from ksdft2effmass.study.periodic1d import (
    Periodic1DStudy,
    Periodic1DStudyOrchestrator,
)


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2Study(Periodic1DStudy[Periodic1DRank2BlockHoppingModel]):
    """Correlate one periodic-1D rank-two model with one study identity and role.

    Parameters
    ----------
    study_id
        Stable nonempty study identity, distinct from the scientific-model identity.
    model
        Exact complete periodic-1D rank-two block-hopping scientific model.
    model_role
        Explicit reference or candidate role in the named study comparison.

    Notes
    -----
    This value neither consumes the historical ``BlockHoppingModel1D`` contract nor
    selects an analysis, threshold, persistence route, or evidence status.

    """

    study_id: str
    model: Periodic1DRank2BlockHoppingModel
    model_role: PeriodicStudyModelRole

    def __post_init__(self) -> None:
        """Validate exact study identity, model ownership, and comparison role."""
        if type(self.study_id) is not str:
            raise TypeError("study_id must be a built-in string")
        if not self.study_id:
            raise ValueError("study_id must be nonempty")
        if type(self.model) is not Periodic1DRank2BlockHoppingModel:
            raise TypeError("model must be Periodic1DRank2BlockHoppingModel")
        if type(self.model_role) is not PeriodicStudyModelRole:
            raise TypeError("model_role must be PeriodicStudyModelRole")

    @property
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained band-subspace rank two."""
        return 2


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2StudyOrchestrator(
    Periodic1DStudyOrchestrator[
        Periodic1DRank2BlockHoppingModel,
        Periodic1DRank2Study,
    ]
):
    """Construct one immutable periodic-1D rank-two study correlation."""

    study_id: str
    model: Periodic1DRank2BlockHoppingModel
    model_role: PeriodicStudyModelRole

    def __post_init__(self) -> None:
        """Validate exact orchestration inputs without coercion."""
        if type(self.study_id) is not str:
            raise TypeError("study_id must be a built-in string")
        if not self.study_id:
            raise ValueError("study_id must be nonempty")
        if type(self.model) is not Periodic1DRank2BlockHoppingModel:
            raise TypeError("model must be Periodic1DRank2BlockHoppingModel")
        if type(self.model_role) is not PeriodicStudyModelRole:
            raise TypeError("model_role must be PeriodicStudyModelRole")

    @property
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained band-subspace rank two."""
        return 2

    def execute(self) -> Periodic1DRank2Study:
        """Return the immutable one-model study correlation."""
        return Periodic1DRank2Study(
            study_id=self.study_id,
            model=self.model,
            model_role=self.model_role,
        )


__all__ = ["Periodic1DRank2Study", "Periodic1DRank2StudyOrchestrator"]
