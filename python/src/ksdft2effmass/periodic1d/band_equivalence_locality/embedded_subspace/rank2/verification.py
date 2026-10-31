"""Canonical-byte independent verification for embedded-subspace rank two."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Self

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.model_systems.verification import (
    BaseModelAnalysisVerification,
    VisualizationProjectionVerification,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue
from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from .family import Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysis
from .records import (
    Periodic1DEmbeddedSubspaceRank2AnalysisRecord,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord,
)
from .reference import (
    Periodic1DEmbeddedSubspaceRank2IndependentReferenceAnalyzer,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyIndependentReferenceAnalyzer,
    _IndependentParentFamilyReference,
)
from .results import (
    Periodic1DEmbeddedSubspaceRank2Analysis,
    Periodic1DEmbeddedSubspaceRank2BandTransportBackendFailure,
    Periodic1DEmbeddedSubspaceRank2BandTransportNumericallyUnresolved,
    Periodic1DEmbeddedSubspaceRank2BandTransportThresholdFailure,
    Periodic1DEmbeddedSubspaceRank2ExternalGapFailure,
    Periodic1DEmbeddedSubspaceRank2Qualification,
    Periodic1DEmbeddedSubspaceRank2QualifiedParent,
)
from .visualizations.data import (
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationData,
    Periodic1DEmbeddedSubspaceRank2VisualizationData,
)


class EmbeddedSubspaceRank2Verification(CompositeVerification):
    """Group independent parent, transport, alignment, and locality comparisons."""


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DEmbeddedSubspaceRank2Verification(BaseModelAnalysisVerification):
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


class EmbeddedSubspaceRank2ParentFamilyVerification(CompositeVerification):
    """Group independent comparisons across a parent-hopping family."""


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification(
    Periodic1DEmbeddedSubspaceRank2Verification
):
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
class Periodic1DEmbeddedSubspaceRank2VerificationResult(BaseTypedRecord):
    """Pair verification with its exact authenticated embedded projection."""

    verification: Periodic1DEmbeddedSubspaceRank2Verification
    visualization_data: Periodic1DEmbeddedSubspaceRank2VisualizationData

    def __post_init__(self) -> None:
        if type(self.verification) is not Periodic1DEmbeddedSubspaceRank2Verification:
            raise TypeError("verification must be embedded rank-two verification")
        if type(self.visualization_data) is not (
            Periodic1DEmbeddedSubspaceRank2VisualizationData
        ):
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
            verification=Periodic1DEmbeddedSubspaceRank2Verification.from_dict(
                verification
            ),
            visualization_data=(
                Periodic1DEmbeddedSubspaceRank2VisualizationData.from_dict(
                    visualization_data
                )
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2ParentFamilyVerificationResult(BaseTypedRecord):
    """Pair family verification with its exact authenticated projection."""

    verification: Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification
    visualization_data: Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationData

    def __post_init__(self) -> None:
        if type(self.verification) is not (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification
        ):
            raise TypeError("verification must be parent-family verification")
        if type(self.visualization_data) is not (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationData
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
                Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification.from_dict(
                    verification
                )
            ),
            visualization_data=(
                Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationData.from_dict(
                    visualization_data
                )
            ),
        )


class Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier:
    """Readmit canonical family bytes and compare every independently rebuilt member."""

    __slots__ = ("_subject_bytes",)

    def __init__(self, subject_bytes: bytes) -> None:
        if type(subject_bytes) is not bytes:
            raise TypeError("subject_bytes must be built-in bytes")
        self._subject_bytes = subject_bytes

    def result(
        self,
    ) -> Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification:
        """Authenticate canonical family bytes and return independent comparisons."""
        return self.result_with_visualization().verification

    def result_with_visualization(
        self,
    ) -> Periodic1DEmbeddedSubspaceRank2ParentFamilyVerificationResult:
        """Return verification paired with its authenticated family projection."""
        record = Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord.from_json(
            self._subject_bytes
        )
        if record.to_json() != self._subject_bytes:
            raise ValueError(
                "subject bytes are not the canonical retained representation"
            )
        subject_sha256 = hashlib.sha256(self._subject_bytes).hexdigest()
        visualization_data = (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationData.from_analysis(
                record.analysis,
                source_sha256=subject_sha256,
            )
        )
        reference = (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyIndependentReferenceAnalyzer(
                record.analysis.request
            ).execute()
        )
        reference_analysis = Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysis(
            request=reference.request,
            members=reference.members,
        )
        reference_visualization = (
            Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationData.from_analysis(
                reference_analysis,
                source_sha256=subject_sha256,
            )
        )
        components: tuple[CompositeVerification, ...] = (
            EmbeddedSubspaceRank2ParentFamilyVerification(
                _compare_parent_families(record.analysis, reference)
            ),
            VisualizationProjectionVerification(
                _compare_family_visualization_data(
                    visualization_data,
                    reference_visualization,
                    record.analysis.request.template_request.verification_absolute_tolerance,
                )
            ),
        )
        verification = Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification(
            subject_sha256=subject_sha256,
            visualization_data_sha256=hashlib.sha256(
                visualization_data.to_json()
            ).hexdigest(),
            components=components,
        )
        return Periodic1DEmbeddedSubspaceRank2ParentFamilyVerificationResult(
            verification=verification,
            visualization_data=visualization_data,
        )


class Periodic1DEmbeddedSubspaceRank2Verifier:
    """Readmit canonical analysis bytes and compare with direct reconstruction."""

    __slots__ = ("_subject_bytes",)

    def __init__(self, subject_bytes: bytes) -> None:
        if type(subject_bytes) is not bytes:
            raise TypeError("subject_bytes must be built-in bytes")
        self._subject_bytes = subject_bytes

    def result(self) -> Periodic1DEmbeddedSubspaceRank2Verification:
        """Authenticate canonical bytes and return independent comparisons."""
        return self.result_with_visualization().verification

    def result_with_visualization(
        self,
    ) -> Periodic1DEmbeddedSubspaceRank2VerificationResult:
        """Return verification paired with its authenticated projection."""
        record = Periodic1DEmbeddedSubspaceRank2AnalysisRecord.from_json(
            self._subject_bytes
        )
        if record.to_json() != self._subject_bytes:
            raise ValueError(
                "subject bytes are not the canonical retained representation"
            )
        subject_sha256 = hashlib.sha256(self._subject_bytes).hexdigest()
        visualization_data = (
            Periodic1DEmbeddedSubspaceRank2VisualizationData.from_analysis(
                record.analysis,
                source_sha256=subject_sha256,
            )
        )
        reference = Periodic1DEmbeddedSubspaceRank2IndependentReferenceAnalyzer(
            record.analysis.request
        ).execute()
        reference_visualization = (
            Periodic1DEmbeddedSubspaceRank2VisualizationData.from_analysis(
                reference,
                source_sha256=subject_sha256,
            )
        )
        components: tuple[CompositeVerification, ...] = (
            EmbeddedSubspaceRank2Verification(
                _compare_analyses(record.analysis, reference)
            ),
            VisualizationProjectionVerification(
                _compare_visualization_data(
                    visualization_data,
                    reference_visualization,
                    record.analysis.request.verification_absolute_tolerance,
                )
            ),
        )
        verification = Periodic1DEmbeddedSubspaceRank2Verification(
            subject_sha256=subject_sha256,
            visualization_data_sha256=hashlib.sha256(
                visualization_data.to_json()
            ).hexdigest(),
            components=components,
        )
        return Periodic1DEmbeddedSubspaceRank2VerificationResult(
            verification=verification,
            visualization_data=visualization_data,
        )


def _observation(value: float, tolerance: float) -> VerificationObservation:
    unit = Unitless()
    return VerificationObservation(
        value=ScalarQuantity(float(value), unit),
        tolerance=ScalarQuantity(float(tolerance), unit),
    )


def _compare_analyses(
    observed: Periodic1DEmbeddedSubspaceRank2Analysis,
    reference: Periodic1DEmbeddedSubspaceRank2Analysis,
) -> Mapping[str, VerificationObservation]:
    if observed.request != reference.request:
        raise ValueError("independent reference request does not match subject request")
    tolerance = observed.request.verification_absolute_tolerance
    observed_qualification = observed.qualification
    reference_qualification = reference.qualification
    observations: dict[str, VerificationObservation] = {
        "qualification_variant_defect": _observation(
            float(type(observed_qualification) is not type(reference_qualification)),
            0.0,
        ),
        "minimum_external_gap_absolute_defect": _observation(
            abs(
                observed_qualification.minimum_external_gap
                - reference_qualification.minimum_external_gap
            ),
            tolerance,
        ),
    }
    _add_qualification_observations(
        observations,
        observed_qualification,
        reference_qualification,
        tolerance,
    )
    observed_inventory = tuple(point.amplitude for point in observed.points)
    reference_inventory = tuple(point.amplitude for point in reference.points)
    observations["point_inventory_defect"] = _observation(
        float(observed_inventory != reference_inventory),
        0.0,
    )
    if observed_inventory != reference_inventory or not observed.points:
        return observations

    scalar_names = (
        "maximum_band_defect",
        "splitting_scale",
        "discrete_maximum_correlation",
        "minimum_operator_threshold",
        "exact_spectrum_joint_operator_threshold",
        "minimum_loss_reconstruction_defect",
        "reference_nonzero_hopping_weight",
        "comparison_nonzero_hopping_weight",
        "reference_parseval_defect",
        "comparison_parseval_defect",
    )
    scalar_defect = max(
        abs(getattr(candidate, name) - getattr(expected, name))
        for candidate, expected in zip(observed.points, reference.points, strict=True)
        for name in scalar_names
    )
    harmonic_scalar_names = (
        "maximum_value",
        "amplitude",
        "fundamental_period",
        "applied_degeneracy_cutoff",
    )
    harmonic_defect = max(
        defect
        for candidate, expected in zip(observed.points, reference.points, strict=True)
        for defect in (
            *(
                abs(
                    getattr(candidate.harmonic_maximum, name)
                    - getattr(expected.harmonic_maximum, name)
                )
                for name in harmonic_scalar_names
            ),
            abs(
                candidate.harmonic_maximum.harmonic.offset
                - expected.harmonic_maximum.harmonic.offset
            ),
            abs(
                candidate.harmonic_maximum.harmonic.cosine_coefficient
                - expected.harmonic_maximum.harmonic.cosine_coefficient
            ),
            abs(
                candidate.harmonic_maximum.harmonic.sine_coefficient
                - expected.harmonic_maximum.harmonic.sine_coefficient
            ),
        )
    )
    harmonic_argument_defect = max(
        _optional_float_defect(
            candidate.harmonic_maximum.canonical_maximizing_argument,
            expected.harmonic_maximum.canonical_maximizing_argument,
        )
        for candidate, expected in zip(observed.points, reference.points, strict=True)
    )
    harmonic_identity_defect = float(
        any(
            candidate.harmonic_maximum.harmonic.harmonic_order
            != expected.harmonic_maximum.harmonic.harmonic_order
            or (
                candidate.harmonic_maximum.harmonic.fundamental_interval_start
                != expected.harmonic_maximum.harmonic.fundamental_interval_start
            )
            or candidate.harmonic_maximum.status is not expected.harmonic_maximum.status
            for candidate, expected in zip(
                observed.points, reference.points, strict=True
            )
        )
    )
    observed_hopping_inventory = tuple(
        tuple(power.displacement for power in point.hopping_powers)
        for point in observed.points
    )
    reference_hopping_inventory = tuple(
        tuple(power.displacement for power in point.hopping_powers)
        for point in reference.points
    )
    observations.update(
        {
            "point_scalar_maximum_absolute_defect": _observation(
                scalar_defect, tolerance
            ),
            "harmonic_scalar_maximum_absolute_defect": _observation(
                harmonic_defect, tolerance
            ),
            "harmonic_argument_maximum_absolute_defect": _observation(
                harmonic_argument_defect, tolerance
            ),
            "harmonic_identity_defect": _observation(harmonic_identity_defect, 0.0),
            "hopping_inventory_defect": _observation(
                float(observed_hopping_inventory != reference_hopping_inventory),
                0.0,
            ),
        }
    )
    if observed_hopping_inventory == reference_hopping_inventory:
        hopping_defect = max(
            max(
                abs(
                    candidate_power.reference_normalized_squared_frobenius_norm
                    - expected_power.reference_normalized_squared_frobenius_norm
                ),
                abs(
                    candidate_power.comparison_normalized_squared_frobenius_norm
                    - expected_power.comparison_normalized_squared_frobenius_norm
                ),
            )
            for candidate, expected in zip(
                observed.points, reference.points, strict=True
            )
            for candidate_power, expected_power in zip(
                candidate.hopping_powers,
                expected.hopping_powers,
                strict=True,
            )
        )
        observations["hopping_power_maximum_absolute_defect"] = _observation(
            hopping_defect, tolerance
        )
    return observations


def _compare_parent_families(
    observed: Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysis,
    reference: _IndependentParentFamilyReference,
) -> Mapping[str, VerificationObservation]:
    if observed.request != reference.request:
        raise ValueError("independent family request does not match subject request")
    observed_inventory = tuple(
        member.request.parent_hopping_scale for member in observed.members
    )
    reference_inventory = tuple(
        member.request.parent_hopping_scale for member in reference.members
    )
    observations: dict[str, VerificationObservation] = {
        "member_inventory_defect": _observation(
            float(observed_inventory != reference_inventory),
            0.0,
        )
    }
    if observed_inventory != reference_inventory:
        return observations
    for index, (candidate, expected) in enumerate(
        zip(observed.members, reference.members, strict=True)
    ):
        for name, observation in _compare_analyses(candidate, expected).items():
            observations[f"member_{index}_{name}"] = observation
    return observations


def _add_qualification_observations(
    observations: dict[str, VerificationObservation],
    observed: Periodic1DEmbeddedSubspaceRank2Qualification,
    reference: Periodic1DEmbeddedSubspaceRank2Qualification,
    tolerance: float,
) -> None:
    if type(observed) is not type(reference):
        return
    if type(observed) is Periodic1DEmbeddedSubspaceRank2ExternalGapFailure:
        return
    if type(observed) is Periodic1DEmbeddedSubspaceRank2BandTransportBackendFailure:
        reference_backend = reference
        if type(reference_backend) is not type(observed):
            return
        observations["band_transport_backend_payload_defect"] = _observation(
            float(
                observed.operation is not reference_backend.operation
                or observed.reason is not reference_backend.reason
                or observed.link_index != reference_backend.link_index
            ),
            0.0,
        )
        return
    if (
        type(observed)
        is Periodic1DEmbeddedSubspaceRank2BandTransportNumericallyUnresolved
    ):
        reference_unresolved = reference
        if type(reference_unresolved) is not type(observed):
            return
        observations["band_transport_status_defect"] = _observation(
            float(
                observed.band_transport_status
                is not reference_unresolved.band_transport_status
            ),
            0.0,
        )
        observations["minimum_transport_singular_value_absolute_defect"] = _observation(
            abs(
                observed.minimum_transport_singular_value
                - reference_unresolved.minimum_transport_singular_value
            ),
            tolerance,
        )
        return
    if type(observed) is Periodic1DEmbeddedSubspaceRank2BandTransportThresholdFailure:
        reference_threshold = reference
        if type(reference_threshold) is not type(observed):
            return
        observations["minimum_transport_singular_value_absolute_defect"] = _observation(
            abs(
                observed.minimum_transport_singular_value
                - reference_threshold.minimum_transport_singular_value
            ),
            tolerance,
        )
        return
    if type(observed) is not Periodic1DEmbeddedSubspaceRank2QualifiedParent:
        return
    reference_qualified = reference
    if type(reference_qualified) is not type(observed):
        return
    scalar_names = (
        "minimum_transport_singular_value",
        "maximum_transport_rank_cutoff",
        "maximum_transport_unitarity_defect",
        "maximum_primitive_link_frobenius_residual",
        "closure_alignment_residual",
        "closure_alignment_unitarity_defect",
        "maximum_frame_orthonormality_defect",
        "maximum_reference_hermiticity_defect",
    )
    observations["qualification_scalar_maximum_absolute_defect"] = _observation(
        max(
            abs(getattr(observed, name) - getattr(reference_qualified, name))
            for name in scalar_names
        ),
        tolerance,
    )
    observations["closure_phase_maximum_absolute_defect"] = _observation(
        max(
            abs(candidate - expected)
            for candidate, expected in zip(
                observed.closure_holonomy_phases,
                reference_qualified.closure_holonomy_phases,
                strict=True,
            )
        ),
        tolerance,
    )


def _compare_visualization_data(
    observed: Periodic1DEmbeddedSubspaceRank2VisualizationData,
    reference: Periodic1DEmbeddedSubspaceRank2VisualizationData,
    tolerance: float,
) -> Mapping[str, VerificationObservation]:
    if not observed.amplitudes or not reference.amplitudes:
        return {
            "visualization_stopped_projection_defect": _observation(
                float(observed != reference),
                0.0,
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
        "visualization_vector_maximum_absolute_defect": _observation(
            vector_defect, tolerance
        ),
        "visualization_matrix_maximum_absolute_defect": _observation(
            matrix_defect, tolerance
        ),
        "visualization_inventory_defect": _observation(inventory_defect, 0.0),
    }


def _compare_family_visualization_data(
    observed: Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationData,
    reference: Periodic1DEmbeddedSubspaceRank2ParentFamilyVisualizationData,
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
        "family_visualization_vector_maximum_absolute_defect": _observation(
            vector_defect, tolerance
        ),
        "family_visualization_matrix_maximum_absolute_defect": _observation(
            matrix_defect, tolerance
        ),
        "family_visualization_source_identity_defect": _observation(
            float(observed.source_sha256 != reference.source_sha256),
            0.0,
        ),
    }


def _optional_float_defect(
    observed: float | None,
    reference: float | None,
) -> float:
    if observed is None or reference is None:
        return float(observed is not reference)
    return abs(observed - reference)


__all__ = [
    "EmbeddedSubspaceRank2ParentFamilyVerification",
    "EmbeddedSubspaceRank2Verification",
    "Periodic1DEmbeddedSubspaceRank2ParentFamilyVerification",
    "Periodic1DEmbeddedSubspaceRank2ParentFamilyVerificationResult",
    "Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier",
    "Periodic1DEmbeddedSubspaceRank2Verification",
    "Periodic1DEmbeddedSubspaceRank2VerificationResult",
    "Periodic1DEmbeddedSubspaceRank2Verifier",
]
