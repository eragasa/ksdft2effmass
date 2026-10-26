"""Nominal identity contract shared by concrete model-system studies."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto


class ModelId(Enum):
    """Identify a supported controlled model system without stringly typing."""

    piab1d = auto()
    mathieu1d = auto()


class ModelSystemStudySchemaId(Enum):
    """Identify the closed schema owned by one model-system study definition."""

    piab1d_v1 = auto()
    piab1d_v2 = auto()
    mathieu1d_v1 = auto()


@dataclass(frozen=True, slots=True)
class ModelSystemStudyIdentity:
    """Identify one model and its closed study-definition schema."""

    model_id: ModelId
    schema_id: ModelSystemStudySchemaId

    def __post_init__(self) -> None:
        if type(self.model_id) is not ModelId:
            raise TypeError("model_id must be ModelId")
        if type(self.schema_id) is not ModelSystemStudySchemaId:
            raise TypeError("schema_id must be ModelSystemStudySchemaId")


class ModelSystemStudyBase(ABC):
    """Require a concrete study definition to expose one validated identity."""

    __slots__ = ()

    @abstractmethod
    def study_identity(self) -> ModelSystemStudyIdentity:
        """Return the concrete model and study-schema identity."""


def model_system_study_identity(
    study: ModelSystemStudyBase,
) -> ModelSystemStudyIdentity:
    """Read and validate identity through the shared nominal study boundary."""
    if not isinstance(study, ModelSystemStudyBase):
        raise TypeError("study must be ModelSystemStudyBase")
    identity = study.study_identity()
    if not isinstance(identity, ModelSystemStudyIdentity):
        raise TypeError("study_identity must return ModelSystemStudyIdentity")
    return identity
