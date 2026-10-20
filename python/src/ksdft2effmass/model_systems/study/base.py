"""Nominal identity contract shared by concrete model-system studies."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelSystemStudyIdentity:
    """Identify one model-system study and its declared evidence status."""

    study_id: str
    evidence_status: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.study_id, "study_id"),
            (self.evidence_status, "evidence_status"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")


class ModelSystemStudyBase(ABC):
    """Require a concrete study definition to expose one validated identity."""

    __slots__ = ()

    @abstractmethod
    def study_identity(self) -> ModelSystemStudyIdentity:
        """Return the concrete study identifier and evidence status."""


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
