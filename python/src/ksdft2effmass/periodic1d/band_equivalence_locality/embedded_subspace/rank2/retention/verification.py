"""Canonical-byte independent verification for embedded-subspace rank two."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Self

from ksdft2effmass.model_systems.verification import (
    BaseModelAnalysisVerification,
    VisualizationProjectionVerification,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue
from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from ..parent_family.analysis import (
    Periodic1DRank2ParentFamilyAnalysis,
)
from ..parent_family.verification import (
    EmbeddedSubspaceRank2ParentFamilyVerification,
    Periodic1DRank2ParentFamilyIndependentVerifier,
)
from ..parent_scale.independent_reference import (
    Periodic1DRank2IndependentReferenceAnalyzer,
)
from ..parent_scale.verification import (
    EmbeddedSubspaceRank2Verification,
    Periodic1DRank2AnalysisVerificationAssessor,
)
from .records import (
    Periodic1DRank2AnalysisRecord,
    Periodic1DRank2ParentFamilyAnalysisRecord,
)
from .visualization_data import (
    Periodic1DRank2ParentFamilyVisualizationData,
    Periodic1DRank2VisualizationData,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2Verification(BaseModelAnalysisVerification):
    """Authenticate exact subject bytes, projection bytes, and comparisons."""

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "embedded_subspace_rank2": EmbeddedSubspaceRank2Verification,
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        self._validate_common_fields()
        if tuple(type(component) for component in self.components) != tuple(
            self.component_types.values()
        ):
            raise ValueError("components must match the embedded-subspace inventory")

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
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "subject_sha256",
            "visualization_data_sha256",
            "components",
        }:
            raise ValueError("verification fields do not match")
        subject_sha256 = values["subject_sha256"]
        visualization_data_sha256 = values["visualization_data_sha256"]
        components_value = values["components"]
        if (
            type(subject_sha256) is not str
            or type(visualization_data_sha256) is not str
        ):
            raise TypeError("verification digests must decode to strings")
        if not isinstance(components_value, Mapping):
            raise TypeError("verification components must decode to a mapping")
        if set(components_value) != set(cls.component_types):
            raise ValueError("verification component fields do not match")
        components: list[CompositeVerification] = []
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


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2ParentFamilyVerification(Periodic1DRank2Verification):
    """Authenticate exact parent-family bytes and independent reconstruction."""

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "embedded_subspace_rank2_parent_family": (
                    EmbeddedSubspaceRank2ParentFamilyVerification
                ),
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2VerificationResult(BaseTypedRecord):
    """Pair verification with its exact authenticated embedded projection."""

    verification: Periodic1DRank2Verification
    visualization_data: Periodic1DRank2VisualizationData

    def __post_init__(self) -> None:
        if type(self.verification) is not Periodic1DRank2Verification:
            raise TypeError("verification must be embedded rank-two verification")
        if type(self.visualization_data) is not (Periodic1DRank2VisualizationData):
            raise TypeError("visualization_data must be the embedded projection")
        digest = hashlib.sha256(self.visualization_data.to_json()).hexdigest()
        if digest != self.verification.visualization_data_sha256:
            raise ValueError("verification does not authenticate visualization_data")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "verification": self.verification.to_dict(),
            "visualization_data": self.visualization_data.to_dict(),
        }

    @classmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        if set(values) != {"verification", "visualization_data"}:
            raise ValueError("embedded verified-result fields do not match")
        verification = values["verification"]
        visualization_data = values["visualization_data"]
        if not isinstance(verification, Mapping):
            raise TypeError("verification must decode to a mapping")
        if not isinstance(visualization_data, Mapping):
            raise TypeError("visualization_data must decode to a mapping")
        return cls(
            verification=Periodic1DRank2Verification.from_dict(verification),
            visualization_data=(
                Periodic1DRank2VisualizationData.from_dict(visualization_data)
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2ParentFamilyVerificationResult(BaseTypedRecord):
    """Pair family verification with its exact authenticated projection."""

    verification: Periodic1DRank2ParentFamilyVerification
    visualization_data: Periodic1DRank2ParentFamilyVisualizationData

    def __post_init__(self) -> None:
        if type(self.verification) is not (Periodic1DRank2ParentFamilyVerification):
            raise TypeError("verification must be parent-family verification")
        if type(self.visualization_data) is not (
            Periodic1DRank2ParentFamilyVisualizationData
        ):
            raise TypeError("visualization_data must be the parent-family projection")
        digest = hashlib.sha256(self.visualization_data.to_json()).hexdigest()
        if digest != self.verification.visualization_data_sha256:
            raise ValueError("verification does not authenticate visualization_data")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "verification": self.verification.to_dict(),
            "visualization_data": self.visualization_data.to_dict(),
        }

    @classmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        if set(values) != {"verification", "visualization_data"}:
            raise ValueError("family verified-result fields do not match")
        verification = values["verification"]
        visualization_data = values["visualization_data"]
        if not isinstance(verification, Mapping):
            raise TypeError("verification must decode to a mapping")
        if not isinstance(visualization_data, Mapping):
            raise TypeError("visualization_data must decode to a mapping")
        return cls(
            verification=(
                Periodic1DRank2ParentFamilyVerification.from_dict(verification)
            ),
            visualization_data=(
                Periodic1DRank2ParentFamilyVisualizationData.from_dict(
                    visualization_data
                )
            ),
        )


class Periodic1DRank2ParentFamilyVerifier:
    """Readmit canonical family bytes and compare every independently rebuilt member."""

    __slots__ = ("_subject_bytes",)

    def __init__(self, subject_bytes: bytes) -> None:
        if type(subject_bytes) is not bytes:
            raise TypeError("subject_bytes must be built-in bytes")
        self._subject_bytes = subject_bytes

    def result(
        self,
    ) -> Periodic1DRank2ParentFamilyVerification:
        """Authenticate canonical family bytes and return independent comparisons."""
        return self.result_with_visualization().verification

    def result_with_visualization(
        self,
    ) -> Periodic1DRank2ParentFamilyVerificationResult:
        """Return verification paired with its authenticated family projection."""
        record = Periodic1DRank2ParentFamilyAnalysisRecord.from_json(
            self._subject_bytes
        )
        if record.to_json() != self._subject_bytes:
            raise ValueError(
                "subject bytes are not the canonical retained representation"
            )
        subject_sha256 = hashlib.sha256(self._subject_bytes).hexdigest()
        visualization_data = Periodic1DRank2ParentFamilyVisualizationData.from_analysis(
            record.analysis,
            source_sha256=subject_sha256,
        )
        independent_verification = Periodic1DRank2ParentFamilyIndependentVerifier(
            record.analysis
        ).result()
        reference = independent_verification.reference
        reference_analysis = Periodic1DRank2ParentFamilyAnalysis(
            request=reference.request,
            members=reference.members,
        )
        reference_visualization = (
            Periodic1DRank2ParentFamilyVisualizationData.from_analysis(
                reference_analysis,
                source_sha256=subject_sha256,
            )
        )
        components: tuple[CompositeVerification, ...] = (
            independent_verification.verification,
            VisualizationProjectionVerification(
                _compare_family_visualization_data(
                    visualization_data,
                    reference_visualization,
                    record.analysis.request.template_request.verification_absolute_tolerance,
                )
            ),
        )
        verification = Periodic1DRank2ParentFamilyVerification(
            subject_sha256=subject_sha256,
            visualization_data_sha256=hashlib.sha256(
                visualization_data.to_json()
            ).hexdigest(),
            components=components,
        )
        return Periodic1DRank2ParentFamilyVerificationResult(
            verification=verification,
            visualization_data=visualization_data,
        )


class Periodic1DRank2Verifier:
    """Readmit canonical analysis bytes and compare with direct reconstruction."""

    __slots__ = ("_subject_bytes",)

    def __init__(self, subject_bytes: bytes) -> None:
        if type(subject_bytes) is not bytes:
            raise TypeError("subject_bytes must be built-in bytes")
        self._subject_bytes = subject_bytes

    def result(self) -> Periodic1DRank2Verification:
        """Authenticate canonical bytes and return independent comparisons."""
        return self.result_with_visualization().verification

    def result_with_visualization(
        self,
    ) -> Periodic1DRank2VerificationResult:
        """Return verification paired with its authenticated projection."""
        record = Periodic1DRank2AnalysisRecord.from_json(self._subject_bytes)
        if record.to_json() != self._subject_bytes:
            raise ValueError(
                "subject bytes are not the canonical retained representation"
            )
        subject_sha256 = hashlib.sha256(self._subject_bytes).hexdigest()
        visualization_data = Periodic1DRank2VisualizationData.from_analysis(
            record.analysis,
            source_sha256=subject_sha256,
        )
        reference = Periodic1DRank2IndependentReferenceAnalyzer(
            record.analysis.request
        ).execute()
        reference_visualization = Periodic1DRank2VisualizationData.from_analysis(
            reference,
            source_sha256=subject_sha256,
        )
        components: tuple[CompositeVerification, ...] = (
            Periodic1DRank2AnalysisVerificationAssessor(
                record.analysis,
                reference,
            ).assess(),
            VisualizationProjectionVerification(
                _compare_visualization_data(
                    visualization_data,
                    reference_visualization,
                    record.analysis.request.verification_absolute_tolerance,
                )
            ),
        )
        verification = Periodic1DRank2Verification(
            subject_sha256=subject_sha256,
            visualization_data_sha256=hashlib.sha256(
                visualization_data.to_json()
            ).hexdigest(),
            components=components,
        )
        return Periodic1DRank2VerificationResult(
            verification=verification,
            visualization_data=visualization_data,
        )


def _compare_visualization_data(
    observed: Periodic1DRank2VisualizationData,
    reference: Periodic1DRank2VisualizationData,
    tolerance: float,
) -> Mapping[str, VerificationObservation]:
    if not observed.amplitudes or not reference.amplitudes:
        return {
            "visualization_stopped_projection_defect": (
                VerificationObservation.dimensionless(
                    float(observed != reference),
                    0.0,
                )
            )
        }
    vector_names = (
        "amplitudes",
        "correlations",
        "operator_thresholds",
        "joint_thresholds",
        "reference_nonzero_weights",
        "comparison_nonzero_weights",
        "band_defects",
        "reconstruction_defects",
        "reference_parseval_defects",
        "comparison_parseval_defects",
    )
    vector_defect = max(
        abs(candidate - expected)
        for name in vector_names
        for candidate, expected in zip(
            getattr(observed, name),
            getattr(reference, name),
            strict=True,
        )
    )
    matrix_defect = max(
        abs(candidate - expected)
        for name in ("reference_hopping_powers", "comparison_hopping_powers")
        for candidate_row, expected_row in zip(
            getattr(observed, name),
            getattr(reference, name),
            strict=True,
        )
        for candidate, expected in zip(
            candidate_row,
            expected_row,
            strict=True,
        )
    )
    inventory_defect = float(
        observed.source_sha256 != reference.source_sha256
        or observed.hopping_displacements != reference.hopping_displacements
    )
    return {
        "visualization_vector_maximum_absolute_defect": (
            VerificationObservation.dimensionless(vector_defect, tolerance)
        ),
        "visualization_matrix_maximum_absolute_defect": (
            VerificationObservation.dimensionless(matrix_defect, tolerance)
        ),
        "visualization_inventory_defect": VerificationObservation.dimensionless(
            inventory_defect, 0.0
        ),
    }


def _compare_family_visualization_data(
    observed: Periodic1DRank2ParentFamilyVisualizationData,
    reference: Periodic1DRank2ParentFamilyVisualizationData,
    tolerance: float,
) -> Mapping[str, VerificationObservation]:
    vector_defect = max(
        abs(candidate - expected)
        for name in (
            "parent_hopping_scales",
            "amplitudes",
            "minimum_external_gaps",
            "minimum_transport_singular_values",
        )
        for candidate, expected in zip(
            getattr(observed, name),
            getattr(reference, name),
            strict=True,
        )
    )
    matrix_defect = max(
        abs(candidate - expected)
        for name in (
            "correlations",
            "operator_thresholds",
            "reference_nonzero_weights",
            "comparison_nonzero_weights",
        )
        for candidate_row, expected_row in zip(
            getattr(observed, name),
            getattr(reference, name),
            strict=True,
        )
        for candidate, expected in zip(
            candidate_row,
            expected_row,
            strict=True,
        )
    )
    return {
        "family_visualization_vector_maximum_absolute_defect": (
            VerificationObservation.dimensionless(vector_defect, tolerance)
        ),
        "family_visualization_matrix_maximum_absolute_defect": (
            VerificationObservation.dimensionless(matrix_defect, tolerance)
        ),
        "family_visualization_source_identity_defect": (
            VerificationObservation.dimensionless(
                float(observed.source_sha256 != reference.source_sha256),
                0.0,
            )
        ),
    }


__all__ = [
    "Periodic1DRank2ParentFamilyVerification",
    "Periodic1DRank2ParentFamilyVerificationResult",
    "Periodic1DRank2ParentFamilyVerifier",
    "Periodic1DRank2Verification",
    "Periodic1DRank2VerificationResult",
    "Periodic1DRank2Verifier",
]
