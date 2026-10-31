"""Exact-byte independent verification for periodic-1D band-equivalence locality."""

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

from .records import Periodic1DBandEquivalenceLocalityAnalysisRecord
from .reference import (
    Periodic1DBandEquivalenceLocalityIndependentReferenceAnalyzer,
)
from .results import Periodic1DBandEquivalenceLocalityAnalysis
from .visualizations import Periodic1DBandEquivalenceLocalityVisualizationData


class BandEquivalenceLocalityVerification(CompositeVerification):
    """Group independently reconstructed scientific observations."""


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DBandEquivalenceLocalityVerification(BaseModelAnalysisVerification):
    """Authenticate supplied result bytes, projection bytes, and comparisons."""

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    component_types: ClassVar[Mapping[str, type[CompositeVerification]]] = (
        MappingProxyType(
            {
                "band_equivalence_locality": BandEquivalenceLocalityVerification,
                "visualization_projection": VisualizationProjectionVerification,
            }
        )
    )

    def __post_init__(self) -> None:
        self._validate_common_fields()
        if tuple(type(component) for component in self.components) != tuple(
            self.component_types.values()
        ):
            raise ValueError("components must match the band-equivalence inventory")

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
        subject_digest = values["subject_sha256"]
        visualization_digest = values["visualization_data_sha256"]
        components_value = values["components"]
        if type(subject_digest) is not str or type(visualization_digest) is not str:
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
            subject_sha256=subject_digest,
            visualization_data_sha256=visualization_digest,
            components=tuple(components),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalenceLocalityVerificationResult(BaseTypedRecord):
    """Pair verification with the exact authenticated rendering projection."""

    verification: Periodic1DBandEquivalenceLocalityVerification
    visualization_data: Periodic1DBandEquivalenceLocalityVisualizationData

    def __post_init__(self) -> None:
        if type(self.verification) is not Periodic1DBandEquivalenceLocalityVerification:
            raise TypeError(
                "verification must be Periodic1DBandEquivalenceLocalityVerification"
            )
        if (
            type(self.visualization_data)
            is not Periodic1DBandEquivalenceLocalityVisualizationData
        ):
            raise TypeError(
                "visualization_data must be the band-equivalence projection"
            )
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
            raise ValueError("verified-result fields do not match")
        verification = values["verification"]
        visualization_data = values["visualization_data"]
        if not isinstance(verification, Mapping):
            raise TypeError("verification must decode to a mapping")
        if not isinstance(visualization_data, Mapping):
            raise TypeError("visualization_data must decode to a mapping")
        return cls(
            verification=Periodic1DBandEquivalenceLocalityVerification.from_dict(
                verification
            ),
            visualization_data=(
                Periodic1DBandEquivalenceLocalityVisualizationData.from_dict(
                    visualization_data
                )
            ),
        )


class Periodic1DBandEquivalenceLocalityVerifier:
    """Readmit canonical result bytes and compare with a direct-sum reference."""

    __slots__ = ("_subject_bytes",)

    def __init__(self, subject_bytes: bytes) -> None:
        if type(subject_bytes) is not bytes:
            raise TypeError("subject_bytes must be built-in bytes")
        self._subject_bytes = subject_bytes

    def result(self) -> Periodic1DBandEquivalenceLocalityVerificationResult:
        """Verify canonical bytes and derive the authenticated plot projection."""
        record = Periodic1DBandEquivalenceLocalityAnalysisRecord.from_json(
            self._subject_bytes
        )
        if record.to_json() != self._subject_bytes:
            raise ValueError(
                "subject bytes are not the canonical retained representation"
            )
        subject_sha256 = hashlib.sha256(self._subject_bytes).hexdigest()
        visualization_data = (
            Periodic1DBandEquivalenceLocalityVisualizationData.from_analysis(
                record.analysis,
                source_sha256=subject_sha256,
            )
        )
        reference = Periodic1DBandEquivalenceLocalityIndependentReferenceAnalyzer(
            record.analysis.request
        ).execute()
        reference_visualization = (
            Periodic1DBandEquivalenceLocalityVisualizationData.from_analysis(
                reference,
                source_sha256=subject_sha256,
            )
        )
        components: tuple[CompositeVerification, ...] = (
            BandEquivalenceLocalityVerification(
                _compare_analyses(record.analysis, reference)
            ),
            VisualizationProjectionVerification(
                _compare_visualization_data(
                    visualization_data,
                    reference_visualization,
                    record.analysis.request.numerical_absolute_tolerance,
                )
            ),
        )
        projection_digest = hashlib.sha256(visualization_data.to_json()).hexdigest()
        verification = Periodic1DBandEquivalenceLocalityVerification(
            subject_sha256=subject_sha256,
            visualization_data_sha256=projection_digest,
            components=components,
        )
        return Periodic1DBandEquivalenceLocalityVerificationResult(
            verification,
            visualization_data,
        )


def _observation(value: float, tolerance: float) -> VerificationObservation:
    unit = Unitless()
    return VerificationObservation(
        ScalarQuantity(float(value), unit),
        ScalarQuantity(tolerance, unit),
    )


def _compare_analyses(
    observed: Periodic1DBandEquivalenceLocalityAnalysis,
    reference: Periodic1DBandEquivalenceLocalityAnalysis,
) -> Mapping[str, VerificationObservation]:
    if observed.request != reference.request:
        raise ValueError("independent reference request does not match subject request")
    tolerance = observed.request.numerical_absolute_tolerance
    scalar_names = (
        "maximum_band_defect",
        "discrete_maximum_correlation",
        "analytic_maximum_correlation",
        "correlation_quadrature_defect",
        "global_alignment_angle",
        "optimal_splitting_scale",
        "irreducible_operator_squared_loss",
        "minimum_operator_threshold",
        "exact_spectrum_joint_operator_threshold",
        "cyclic_nyquist_power",
        "reconstruction_maximum_frobenius_error",
        "interpolation_hamiltonian_maximum_error",
        "interpolation_spectral_maximum_error",
    )
    scalar_defect = max(
        abs(getattr(candidate, name) - getattr(expected, name))
        for candidate, expected in zip(observed.points, reference.points, strict=True)
        for name in scalar_names
    )
    observed_hopping_inventory = tuple(
        tuple(item.displacement for item in point.hopping_powers)
        for point in observed.points
    )
    reference_hopping_inventory = tuple(
        tuple(item.displacement for item in point.hopping_powers)
        for point in reference.points
    )
    hopping_inventory_defect = float(
        observed_hopping_inventory != reference_hopping_inventory
    )
    hopping_power_defect = max(
        abs(
            candidate_power.normalized_squared_frobenius_norm
            - expected_power.normalized_squared_frobenius_norm
        )
        for candidate, expected in zip(observed.points, reference.points, strict=True)
        for candidate_power, expected_power in zip(
            candidate.hopping_powers, expected.hopping_powers, strict=True
        )
    )
    observed_range_inventory = tuple(
        tuple(item.maximum_range for item in point.ranges) for point in observed.points
    )
    reference_range_inventory = tuple(
        tuple(item.maximum_range for item in point.ranges) for point in reference.points
    )
    range_inventory_defect = float(
        observed_range_inventory != reference_range_inventory
    )
    range_names = (
        "ordinary_omitted_block_l2_norm",
        "truncation_hamiltonian_maximum_error",
        "total_hamiltonian_maximum_error",
        "truncation_spectral_maximum_error",
        "total_spectral_maximum_error",
    )
    range_value_defect = max(
        abs(getattr(candidate_range, name) - getattr(expected_range, name))
        for candidate, expected in zip(observed.points, reference.points, strict=True)
        for candidate_range, expected_range in zip(
            candidate.ranges, expected.ranges, strict=True
        )
        for name in range_names
    )
    return {
        "point_scalar_maximum_absolute_defect": _observation(scalar_defect, tolerance),
        "hopping_inventory_defect": _observation(hopping_inventory_defect, 0.0),
        "hopping_power_maximum_absolute_defect": _observation(
            hopping_power_defect, tolerance
        ),
        "range_inventory_defect": _observation(range_inventory_defect, 0.0),
        "range_value_maximum_absolute_defect": _observation(
            range_value_defect, tolerance
        ),
    }


def _compare_visualization_data(
    observed: Periodic1DBandEquivalenceLocalityVisualizationData,
    reference: Periodic1DBandEquivalenceLocalityVisualizationData,
    tolerance: float,
) -> Mapping[str, VerificationObservation]:
    scalar_vectors = (
        "amplitudes",
        "discrete_correlations",
        "analytic_correlations",
        "operator_thresholds",
        "joint_thresholds",
        "nyquist_powers",
    )
    scalar_defect = max(
        abs(candidate - expected)
        for name in scalar_vectors
        for candidate, expected in zip(
            getattr(observed, name),
            getattr(reference, name),
            strict=True,
        )
    )
    inventory_defect = float(
        observed.source_sha256 != reference.source_sha256
        or observed.maximum_ranges != reference.maximum_ranges
        or observed.hopping_displacements != reference.hopping_displacements
    )
    matrix_defect = max(
        abs(candidate - expected)
        for name in (
            "total_hamiltonian_errors",
            "total_spectral_errors",
            "hopping_powers",
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
        "visualization_scalar_maximum_absolute_defect": _observation(
            scalar_defect, tolerance
        ),
        "visualization_inventory_defect": _observation(inventory_defect, 0.0),
        "visualization_matrix_maximum_absolute_defect": _observation(
            matrix_defect, tolerance
        ),
    }


__all__ = [
    "BandEquivalenceLocalityVerification",
    "Periodic1DBandEquivalenceLocalityVerification",
    "Periodic1DBandEquivalenceLocalityVerificationResult",
    "Periodic1DBandEquivalenceLocalityVerifier",
]
