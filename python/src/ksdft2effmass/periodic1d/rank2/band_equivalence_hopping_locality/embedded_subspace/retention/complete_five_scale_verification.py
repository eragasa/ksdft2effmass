"""Independent verification of canonical complete-five-scale bytes."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.periodic1d.rank2.support_truncation.family_verification import (
    Periodic1DRank2TruncationFamilyIndependentVerifier,
)
from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.verification import (
    CompositeVerification,
    MemberwiseCompositeVerificationComposer,
    VisualizationVerification,
)

from ..amplitude_refinement.verification import (
    Periodic1DRank2AdaptiveAmplitudeIndependentVerifier,
)
from ..momentum_refinement.family_verification import (
    Periodic1DRank2MomentumRefinementFamilyIndependentVerifier,
)
from .complete_five_scale import Periodic1DRank2CompleteFiveScaleCalculationRecord
from .complete_five_scale_visualization_data import (
    Periodic1DRank2CompleteFiveScaleVisualizationData,
)
from .records import Periodic1DRank2ParentFamilyAnalysisRecord
from .verification import Periodic1DRank2ParentFamilyVerifier


@dataclass(frozen=True, slots=True)
class Periodic1DRank2CompleteFiveScaleVerification(VisualizationVerification):
    """Authenticate aggregate and projection bytes with independent observations."""

    subject_sha256: str
    visualization_data_sha256: str
    verification: CompositeVerification

    def __post_init__(self) -> None:
        for name in ("subject_sha256", "visualization_data_sha256"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if len(value) != 64 or any(
                character not in "0123456789abcdef" for character in value
            ):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
        if type(self.verification) is not CompositeVerification:
            raise TypeError("verification must be an exact CompositeVerification")

    @property
    def passed(self) -> bool:
        """Return whether every independently produced observation passes."""
        return self.verification.passed

    def authenticated_visualization_data_sha256(self) -> str:
        """Return the authenticated complete-scope projection digest."""
        return self.visualization_data_sha256

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "subject_sha256": self.subject_sha256,
            "visualization_data_sha256": self.visualization_data_sha256,
            "verification": self.verification.to_dict(),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "subject_sha256",
            "visualization_data_sha256",
            "verification",
        }:
            raise ValueError("complete-five-scale verification fields do not match")
        subject_sha256 = values["subject_sha256"]
        visualization_data_sha256 = values["visualization_data_sha256"]
        verification = values["verification"]
        if (
            type(subject_sha256) is not str
            or type(visualization_data_sha256) is not str
        ):
            raise TypeError("verification digests must decode to built-in strings")
        if not isinstance(verification, Mapping):
            raise TypeError("verification must decode to a mapping")
        return cls(
            subject_sha256=subject_sha256,
            visualization_data_sha256=visualization_data_sha256,
            verification=CompositeVerification.from_dict(verification),
        )


class Periodic1DRank2CompleteFiveScaleVerifier:
    """Readmit exact bytes and independently reconstruct every scientific member."""

    __slots__ = ("_subject_bytes",)

    def __init__(self, subject_bytes: bytes) -> None:
        if type(subject_bytes) is not bytes:
            raise TypeError("subject_bytes must be built-in bytes")
        self._subject_bytes = subject_bytes

    def _admit_subject(self) -> Periodic1DRank2CompleteFiveScaleCalculationRecord:
        record = Periodic1DRank2CompleteFiveScaleCalculationRecord.from_json(
            self._subject_bytes
        )
        if record.to_json() != self._subject_bytes:
            raise ValueError(
                "subject bytes are not the canonical retained representation"
            )
        return record

    def result(self) -> Periodic1DRank2CompleteFiveScaleVerification:
        """Return canonical-byte authentication and independent reconstruction."""
        record = self._admit_subject()
        parent_bytes = Periodic1DRank2ParentFamilyAnalysisRecord(
            record.parent_family
        ).to_json()
        parent_verification = Periodic1DRank2ParentFamilyVerifier(parent_bytes).result()
        component_verifications = (
            *parent_verification.components,
            Periodic1DRank2MomentumRefinementFamilyIndependentVerifier(
                record.momentum_refinement_family
            ).result(),
            Periodic1DRank2AdaptiveAmplitudeIndependentVerifier(
                record.adaptive_amplitude
            ).result(),
            *tuple(
                Periodic1DRank2TruncationFamilyIndependentVerifier(family).result()
                for family in record.truncation_mesh_stability.refinement_families
            ),
        )
        verification = MemberwiseCompositeVerificationComposer(
            component_verifications
        ).result()
        subject_sha256 = hashlib.sha256(self._subject_bytes).hexdigest()
        visualization_data = (
            Periodic1DRank2CompleteFiveScaleVisualizationData.from_record(
                record,
                source_sha256=subject_sha256,
            )
        )
        return Periodic1DRank2CompleteFiveScaleVerification(
            subject_sha256=subject_sha256,
            visualization_data_sha256=hashlib.sha256(
                visualization_data.to_json()
            ).hexdigest(),
            verification=verification,
        )

    def admit_stored(
        self,
        verification: Periodic1DRank2CompleteFiveScaleVerification,
    ) -> Periodic1DRank2CompleteFiveScaleCalculationRecord:
        """Admit passing stored verification without rerunning independent routes."""
        if type(verification) is not Periodic1DRank2CompleteFiveScaleVerification:
            raise TypeError("verification must be complete-five-scale verification")
        record = self._admit_subject()
        subject_sha256 = hashlib.sha256(self._subject_bytes).hexdigest()
        if verification.subject_sha256 != subject_sha256:
            raise ValueError("verification authenticates different subject bytes")
        if not verification.passed:
            raise ValueError("stored complete-five-scale verification did not pass")
        visualization_data = (
            Periodic1DRank2CompleteFiveScaleVisualizationData.from_record(
                record,
                source_sha256=subject_sha256,
            )
        )
        if hashlib.sha256(visualization_data.to_json()).hexdigest() != (
            verification.visualization_data_sha256
        ):
            raise ValueError(
                "stored verification authenticates different visualization data"
            )
        return record


__all__ = [
    "Periodic1DRank2CompleteFiveScaleVerification",
    "Periodic1DRank2CompleteFiveScaleVerifier",
]
