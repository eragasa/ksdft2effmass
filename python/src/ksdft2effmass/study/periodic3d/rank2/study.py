"""Concrete periodic-3D rank-two study contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, final

from ksdft2effmass.periodic.periodic3d.rank2.models import (
    Periodic3DRank2BlockHoppingModel,
)
from ksdft2effmass.study.periodic import PeriodicStudyModelRole
from ksdft2effmass.study.periodic3d import (
    Periodic3DStudy,
    Periodic3DStudyOrchestrator,
)


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2Study(Periodic3DStudy[Periodic3DRank2BlockHoppingModel]):
    """Correlate one periodic-3D rank-two model with one study identity and role.

    Parameters
    ----------
    study_id
        Stable nonempty study identity, distinct from the scientific-model identity.
    model
        Exact complete periodic-3D rank-two block-hopping scientific model.
    model_role
        Explicit reference or candidate role in the named study comparison.

    Notes
    -----
    Crystal structure is model data. FCC, BCT, diamond, simple-cubic, and other valid
    geometries use this same class without structure-specific subclasses or branches.

    """

    study_id: str
    model: Periodic3DRank2BlockHoppingModel
    model_role: PeriodicStudyModelRole

    def __post_init__(self) -> None:
        """Validate exact study identity, model ownership, and comparison role."""
        if type(self.study_id) is not str:
            raise TypeError("study_id must be a built-in string")
        if not self.study_id:
            raise ValueError("study_id must be nonempty")
        if type(self.model) is not Periodic3DRank2BlockHoppingModel:
            raise TypeError("model must be Periodic3DRank2BlockHoppingModel")
        if type(self.model_role) is not PeriodicStudyModelRole:
            raise TypeError("model_role must be PeriodicStudyModelRole")

    @property
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained band-subspace rank two."""
        return 2


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2StudyOrchestrator(
    Periodic3DStudyOrchestrator[
        Periodic3DRank2BlockHoppingModel,
        Periodic3DRank2Study,
    ]
):
    """Construct one immutable periodic-3D rank-two study correlation."""

    study_id: str
    model: Periodic3DRank2BlockHoppingModel
    model_role: PeriodicStudyModelRole

    def __post_init__(self) -> None:
        """Validate exact orchestration inputs without coercion."""
        if type(self.study_id) is not str:
            raise TypeError("study_id must be a built-in string")
        if not self.study_id:
            raise ValueError("study_id must be nonempty")
        if type(self.model) is not Periodic3DRank2BlockHoppingModel:
            raise TypeError("model must be Periodic3DRank2BlockHoppingModel")
        if type(self.model_role) is not PeriodicStudyModelRole:
            raise TypeError("model_role must be PeriodicStudyModelRole")

    @property
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained band-subspace rank two."""
        return 2

    def execute(self) -> Periodic3DRank2Study:
        """Return the immutable one-model study correlation."""
        return Periodic3DRank2Study(
            study_id=self.study_id,
            model=self.model,
            model_role=self.model_role,
        )


__all__ = ["Periodic3DRank2Study", "Periodic3DRank2StudyOrchestrator"]
