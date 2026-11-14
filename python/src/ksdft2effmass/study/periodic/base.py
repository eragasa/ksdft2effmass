"""Dimension-neutral periodic study and orchestration contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.periodic.models import PeriodicModel, SpatialDimension
from ksdft2effmass.serialization.enums import StrWireEnum


class PeriodicStudyModelRole(StrWireEnum):
    """Identify a model's explicit role in a study comparison.

    ``reference`` identifies the model that defines the comparison baseline.
    ``candidate`` identifies the model assessed against that baseline. The role is not
    part of a single-model analysis request and does not imply acceptance or validation.

    """

    reference = "reference"
    candidate = "candidate"


class PeriodicStudy[ModelT: PeriodicModel](ABC):
    """Correlate one named periodic investigation with one exact model.

    Notes
    -----
    A study is not a numerical calculator or an implicit multi-model comparison.
    Dimension, rank, analysis inventory, persistence, and evidence status belong to
    narrower owners.

    """

    __slots__ = ()

    study_id: str
    model: ModelT
    model_role: PeriodicStudyModelRole

    @property
    @abstractmethod
    def spatial_dimension(self) -> SpatialDimension:
        """Return the exact periodic spatial dimension."""

    @property
    def model_id(self) -> str:
        """Return the scientific-model identity retained by this study."""
        return self.model.model_id


class PeriodicStudyOrchestrator[
    ModelT: PeriodicModel,
    StudyT,
](ABC):
    """Construct one typed periodic study without choosing comparison policy."""

    __slots__ = ()

    study_id: str
    model: ModelT
    model_role: PeriodicStudyModelRole

    @property
    @abstractmethod
    def spatial_dimension(self) -> SpatialDimension:
        """Return the exact periodic spatial dimension."""

    @abstractmethod
    def execute(self) -> StudyT:
        """Return the immutable one-model study correlation."""

    @property
    def model_id(self) -> str:
        """Return the scientific-model identity selected for orchestration."""
        return self.model.model_id


__all__ = [
    "PeriodicStudy",
    "PeriodicStudyModelRole",
    "PeriodicStudyOrchestrator",
]
