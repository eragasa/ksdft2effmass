"""Canonical-byte verification for the cohesive embedded rank-two calculation."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Self

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.verification import VisualizationVerification

from .amplitude_refinement_verification import (
    EmbeddedSubspaceRank2AdaptiveAmplitudeVerification,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentVerifier,
)
from .records import (
    Periodic1DEmbeddedSubspaceRank2CalculationRecord,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord,
)
from .refinement_verification import (
    EmbeddedSubspaceRank2MomentumRefinementVerification,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier,
)
from .truncation.verification import (
    EmbeddedSubspaceRank2TruncationVerification,
    Periodic1DEmbeddedSubspaceRank2TruncationIndependentVerifier,
)
from .verification import (
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier,
)
from .visualizations.data import (
    Periodic1DEmbeddedSubspaceRank2CalculationVisualizationData,
)

type CalculationComponentVerification = (
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification
    | EmbeddedSubspaceRank2MomentumRefinementVerification
    | EmbeddedSubspaceRank2AdaptiveAmplitudeVerification
    | EmbeddedSubspaceRank2TruncationVerification
)


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2CalculationVerification(
    VisualizationVerification
):
    """Authenticate aggregate bytes and retain independent component checks."""

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CalculationComponentVerification, ...]

    component_types: ClassVar[
        Mapping[str, type[CalculationComponentVerification]]
    ] = (
        MappingProxyType(
            {
                "parent_family": (
                    Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification
                ),
                "momentum_refinement": (
                    EmbeddedSubspaceRank2MomentumRefinementVerification
                ),
                "adaptive_amplitude": (
                    EmbeddedSubspaceRank2AdaptiveAmplitudeVerification
                ),
                "truncation": EmbeddedSubspaceRank2TruncationVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        if (
            type(self.subject_sha256) is not str
            or len(self.subject_sha256) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.subject_sha256
            )
        ):
            raise ValueError("subject_sha256 must be a lowercase SHA-256 digest")
        if (
            type(self.visualization_data_sha256) is not str
            or len(self.visualization_data_sha256) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.visualization_data_sha256
            )
        ):
            raise ValueError(
                "visualization_data_sha256 must be a lowercase SHA-256 digest"
            )
        if tuple(type(component) for component in self.components) != tuple(
            self.component_types.values()
        ):
            raise ValueError("components must match the calculation inventory")

    @property
    def passed(self) -> bool:
        """Return whether every independent component verification passed."""
        return all(component.passed for component in self.components)

    def authenticated_visualization_data_sha256(self) -> str:
        """Return the digest bound to the aggregate visualization projection."""
        return self.visualization_data_sha256

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "subject_sha256": self.subject_sha256,
            "visualization_data_sha256": self.visualization_data_sha256,
            "components": {
                identifier: component.to_dict()
                for identifier, component in zip(
                    self.component_types,
                    self.components,
                    strict=True,
                )
            },
        }

    @classmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        if set(values) != {
            "subject_sha256",
            "visualization_data_sha256",
            "components",
        }:
            raise ValueError("calculation-verification fields do not match")
        subject_sha256 = values["subject_sha256"]
        visualization_data_sha256 = values["visualization_data_sha256"]
        components_value = values["components"]
        if type(subject_sha256) is not str:
            raise TypeError("subject_sha256 must decode to a string")
        if type(visualization_data_sha256) is not str:
            raise TypeError("visualization_data_sha256 must decode to a string")
        if not isinstance(components_value, Mapping):
            raise TypeError("components must decode to a mapping")
        if set(components_value) != set(cls.component_types):
            raise ValueError("calculation-verification components do not match")
        components: list[CalculationComponentVerification] = []
        for identifier, component_type in cls.component_types.items():
            component_value = components_value[identifier]
            if not isinstance(component_value, Mapping) or any(
                type(key) is not str for key in component_value
            ):
                raise TypeError("verification components must decode to mappings")
            components.append(component_type.from_dict(component_value))
        return cls(
            subject_sha256=subject_sha256,
            visualization_data_sha256=visualization_data_sha256,
            components=tuple(components),
        )


class Periodic1DEmbeddedSubspaceRank2CalculationVerifier:
    """Readmit canonical aggregate bytes and run independent scientific routes."""

    __slots__ = ("_subject_bytes",)

    def __init__(self, subject_bytes: bytes) -> None:
        if type(subject_bytes) is not bytes:
            raise TypeError("subject_bytes must be built-in bytes")
        self._subject_bytes = subject_bytes

    def _admit_subject(self) -> Periodic1DEmbeddedSubspaceRank2CalculationRecord:
        record = Periodic1DEmbeddedSubspaceRank2CalculationRecord.from_json(
            self._subject_bytes
        )
        if record.to_json() != self._subject_bytes:
            raise ValueError(
                "subject bytes are not the canonical retained representation"
            )
        return record

    def admit_stored(
        self,
        verification: Periodic1DEmbeddedSubspaceRank2CalculationVerification,
    ) -> Periodic1DEmbeddedSubspaceRank2CalculationRecord:
        """Admit stored verification without rerunning independent routes."""
        if type(verification) is not (
            Periodic1DEmbeddedSubspaceRank2CalculationVerification
        ):
            raise TypeError("verification must be calculation verification")
        record = self._admit_subject()
        subject_sha256 = hashlib.sha256(self._subject_bytes).hexdigest()
        if verification.subject_sha256 != subject_sha256:
            raise ValueError("verification authenticates different subject bytes")
        if not verification.passed:
            raise ValueError("stored aggregate verification did not pass")
        family_bytes = Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord(
            record.parent_family
        ).to_json()
        family_verification = verification.components[0]
        if type(family_verification) is not (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification
        ):
            raise TypeError("stored family verification has the wrong type")
        if family_verification.subject_sha256 != hashlib.sha256(
            family_bytes
        ).hexdigest():
            raise ValueError("stored family verification authenticates different bytes")
        visualization_data = (
            Periodic1DEmbeddedSubspaceRank2CalculationVisualizationData.from_record(
                record,
                source_sha256=subject_sha256,
            )
        )
        if (
            visualization_data.parent_family_visualization_data_sha256
            != family_verification.visualization_data_sha256
        ):
            raise ValueError("stored family verification authenticates different data")
        if hashlib.sha256(visualization_data.to_json()).hexdigest() != (
            verification.visualization_data_sha256
        ):
            raise ValueError(
                "stored verification authenticates different visualization data"
            )
        return record

    def result(self) -> Periodic1DEmbeddedSubspaceRank2CalculationVerification:
        """Authenticate bytes and return the closed component verification."""
        record = self._admit_subject()
        family_bytes = Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord(
            record.parent_family
        ).to_json()
        subject_sha256 = hashlib.sha256(self._subject_bytes).hexdigest()
        components: tuple[CalculationComponentVerification, ...] = (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier(
                family_bytes
            ).result(),
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier(
                record.momentum_refinement
            ).result(),
            Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentVerifier(
                record.adaptive_amplitude
            ).result(),
            Periodic1DEmbeddedSubspaceRank2TruncationIndependentVerifier(
                record.truncation
            ).result(),
        )
        visualization_data = (
            Periodic1DEmbeddedSubspaceRank2CalculationVisualizationData.from_record(
                record,
                source_sha256=subject_sha256,
            )
        )
        family_verification = components[0]
        if type(family_verification) is not (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification
        ):
            raise TypeError("family verification has the wrong type")
        if (
            visualization_data.parent_family_visualization_data_sha256
            != family_verification.visualization_data_sha256
        ):
            raise ValueError("family visualization projection identity does not match")
        return Periodic1DEmbeddedSubspaceRank2CalculationVerification(
            subject_sha256=subject_sha256,
            visualization_data_sha256=hashlib.sha256(
                visualization_data.to_json()
            ).hexdigest(),
            components=components,
        )


__all__ = [
    "Periodic1DEmbeddedSubspaceRank2CalculationVerification",
    "Periodic1DEmbeddedSubspaceRank2CalculationVerifier",
]
