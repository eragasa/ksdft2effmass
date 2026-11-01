"""Canonical records for the embedded-subspace rank-two control."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import TYPE_CHECKING, Self

from projectkoios.optimization.alignment.closed_loop_polar_transport import (
    ClosedLoopPolarFrameTransportBackendFailureReason,
    ClosedLoopPolarFrameTransportBackendOperation,
    ClosedLoopPolarFrameTransportStatus,
)
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonic,
    PeriodicHarmonicMaximum,
    PeriodicHarmonicMaximumStatus,
)

from ksdft2effmass.numerical_consistency import (
    ReciprocalMeshRefinementFamily,
    ReciprocalMeshRefinementFamilyMember,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.family import (
    Periodic1DRank2TruncationFamilyAnalysis,
    Periodic1DRank2TruncationFamilyRequest,
)
from ksdft2effmass.real_space_support_truncation import (
    RealSpaceSupportTruncationFamily,
    RealSpaceSupportTruncationFamilyMember,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..amplitude_refinement.analysis import (
    Periodic1DRank2AdaptiveAmplitudeAnalysis,
    Periodic1DRank2AdaptiveAmplitudeConverged,
    Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DRank2AdaptiveAmplitudeQualificationStopped,
    Periodic1DRank2AdaptiveAmplitudeRequest,
    Periodic1DRank2AmplitudeRefinementLevel,
    Periodic1DRank2AmplitudeRefinementThresholds,
    Periodic1DRank2AmplitudeValidation,
)
from ..momentum_refinement.analysis import (
    Periodic1DRank2MomentumRefinementAnalysis,
    Periodic1DRank2MomentumRefinementConverged,
    Periodic1DRank2MomentumRefinementQualificationStopped,
    Periodic1DRank2MomentumRefinementRequest,
    Periodic1DRank2MomentumRefinementStep,
    Periodic1DRank2MomentumRefinementThresholds,
    Periodic1DRank2MomentumRefinementUnresolved,
)
from ..momentum_refinement.family import (
    Periodic1DRank2MomentumRefinementFamilyAnalysis,
    Periodic1DRank2MomentumRefinementFamilyRequest,
)
from ..parent_family.analysis import (
    Periodic1DRank2ParentFamilyAnalysis,
    Periodic1DRank2ParentFamilyRequest,
)
from ..parent_scale.request import Periodic1DRank2Request
from ..parent_scale.results import (
    Periodic1DRank2Analysis,
    Periodic1DRank2BandTransportBackendFailure,
    Periodic1DRank2BandTransportNumericallyUnresolved,
    Periodic1DRank2BandTransportThresholdFailure,
    Periodic1DRank2ExternalGapFailure,
    Periodic1DRank2HoppingPower,
    Periodic1DRank2PointAnalysis,
    Periodic1DRank2Qualification,
    Periodic1DRank2QualifiedParent,
)

if TYPE_CHECKING:
    from ksdft2effmass.periodic1d.rank2.support_truncation.request import (
        Periodic1DRank2SupportTruncationAnalysisRequest,
    )
    from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
        Periodic1DRank2SupportTruncationAnalysis,
        Periodic1DRank2TruncationPoint,
        Periodic1DRank2TruncationRange,
    )


class CalculationWireEnum(Enum):
    """Discriminate closed aggregate outcomes at one retained boundary."""

    MOMENTUM_QUALIFICATION_STOPPED = "momentum-qualification-stopped"
    MOMENTUM_CONVERGED = "momentum-converged"
    MOMENTUM_UNRESOLVED = "momentum-unresolved"
    AMPLITUDE_QUALIFICATION_STOPPED = "amplitude-qualification-stopped"
    AMPLITUDE_CONVERGED = "amplitude-converged"
    AMPLITUDE_LEVELS_EXHAUSTED = "amplitude-levels-exhausted"
    AMPLITUDE_EVALUATIONS_EXHAUSTED = "amplitude-evaluations-exhausted"
    TRUNCATION_QUALIFICATION_STOPPED = "truncation-qualification-stopped"
    TRUNCATION_COMPLETED = "truncation-completed"


class _QualificationWireVariant(StrEnum):
    """Discriminate qualification payloads only at the retained-wire boundary."""

    EXTERNAL_GAP_FAILURE = "external-gap-failure"
    BAND_TRANSPORT_BACKEND_FAILURE = "band-transport-backend-failure"
    BAND_TRANSPORT_NUMERICALLY_UNRESOLVED = "band-transport-numerically-unresolved"
    BAND_TRANSPORT_THRESHOLD_FAILURE = "band-transport-threshold-failure"
    QUALIFIED_PARENT = "qualified-parent"


def _fields(
    values: Mapping[str, SerializableValue],
    expected: set[str],
    name: str,
) -> None:
    if set(values) != expected:
        raise ValueError(f"{name} fields do not match")


def _integer(values: Mapping[str, SerializableValue], name: str) -> int:
    value = values[name]
    if type(value) is not int:
        raise TypeError(f"{name} must decode to a built-in integer")
    return value


def _boolean(values: Mapping[str, SerializableValue], name: str) -> bool:
    value = values[name]
    if type(value) is not bool:
        raise TypeError(f"{name} must decode to a built-in boolean")
    return value


def _integer_tuple(
    values: Mapping[str, SerializableValue],
    name: str,
) -> tuple[int, ...]:
    value = values[name]
    if type(value) is not tuple or any(type(item) is not int for item in value):
        raise TypeError(f"{name} must decode to a tuple of built-in integers")
    return value


def _floating(values: Mapping[str, SerializableValue], name: str) -> float:
    value = values[name]
    if type(value) is not float:
        raise TypeError(f"{name} must decode to a built-in float")
    return value


def _string(values: Mapping[str, SerializableValue], name: str) -> str:
    value = values[name]
    if type(value) is not str:
        raise TypeError(f"{name} must decode to a built-in string")
    return value


def _optional_float(
    values: Mapping[str, SerializableValue],
    name: str,
) -> float | None:
    value = values[name]
    if value is None:
        return None
    if type(value) is not float:
        raise TypeError(f"{name} must decode to a built-in float or null")
    return value


def _mapping_value(
    values: Mapping[str, SerializableValue],
    name: str,
) -> Mapping[str, SerializableValue]:
    value = values[name]
    if not isinstance(value, Mapping) or any(type(key) is not str for key in value):
        raise TypeError(f"{name} must decode to a string-keyed mapping")
    return value


def _mapping_tuple(
    values: Mapping[str, SerializableValue],
    name: str,
) -> tuple[Mapping[str, SerializableValue], ...]:
    value = values[name]
    if type(value) is not tuple:
        raise TypeError(f"{name} must decode to a tuple")
    items: list[Mapping[str, SerializableValue]] = []
    for item in value:
        if not isinstance(item, Mapping) or any(type(key) is not str for key in item):
            raise TypeError(f"{name} must contain string-keyed mappings")
        items.append(item)
    return tuple(items)


def _float_tuple(
    values: Mapping[str, SerializableValue],
    name: str,
) -> tuple[float, ...]:
    value = values[name]
    if type(value) is not tuple or any(type(item) is not float for item in value):
        raise TypeError(f"{name} must decode to a tuple of built-in floats")
    return value


def _request_mapping(
    request: Periodic1DRank2Request,
) -> Mapping[str, SerializableValue]:
    return {
        "parent_model_identifier": request.parent_model_identifier,
        "ambient_basis_identifier": request.ambient_basis_identifier,
        "retained_frame_identifier": request.retained_frame_identifier,
        "endpoint_sewing_identifier": request.endpoint_sewing_identifier,
        "energy_reference_identifier": request.energy_reference_identifier,
        "reciprocal_coordinate_convention": request.reciprocal_coordinate_convention,
        "gauge_attack_identifier": request.gauge_attack_identifier,
        "ambient_rank": request.ambient_rank,
        "retained_rank": request.retained_rank,
        "reciprocal_mesh_size": request.reciprocal_mesh_size,
        "amplitudes": request.amplitudes,
        "parent_hopping_scale": request.parent_hopping_scale,
        "minimum_external_gap": request.minimum_external_gap,
        "minimum_transport_singular_value": request.minimum_transport_singular_value,
        "frame_absolute_tolerance": request.frame_absolute_tolerance,
        "transport_rank_relative_tolerance": (
            request.transport_rank_relative_tolerance
        ),
        "transport_validation_relative_tolerance": (
            request.transport_validation_relative_tolerance
        ),
        "harmonic_absolute_degeneracy_tolerance": (
            request.harmonic_absolute_degeneracy_tolerance
        ),
        "harmonic_relative_degeneracy_tolerance": (
            request.harmonic_relative_degeneracy_tolerance
        ),
        "verification_absolute_tolerance": request.verification_absolute_tolerance,
    }


def _request_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2Request:
    identity_names = {
        "parent_model_identifier",
        "ambient_basis_identifier",
        "retained_frame_identifier",
        "endpoint_sewing_identifier",
        "energy_reference_identifier",
        "reciprocal_coordinate_convention",
        "gauge_attack_identifier",
    }
    float_names = {
        "parent_hopping_scale",
        "minimum_external_gap",
        "minimum_transport_singular_value",
        "frame_absolute_tolerance",
        "transport_rank_relative_tolerance",
        "transport_validation_relative_tolerance",
        "harmonic_absolute_degeneracy_tolerance",
        "harmonic_relative_degeneracy_tolerance",
    }
    _fields(
        values,
        identity_names
        | float_names
        | {
            "ambient_rank",
            "retained_rank",
            "reciprocal_mesh_size",
            "amplitudes",
            "verification_absolute_tolerance",
        },
        "embedded-subspace rank-two request mapping",
    )
    request = Periodic1DRank2Request(
        reciprocal_mesh_size=_integer(values, "reciprocal_mesh_size"),
        amplitudes=_float_tuple(values, "amplitudes"),
        parent_hopping_scale=_floating(values, "parent_hopping_scale"),
        minimum_external_gap=_floating(values, "minimum_external_gap"),
        minimum_transport_singular_value=_floating(
            values, "minimum_transport_singular_value"
        ),
        frame_absolute_tolerance=_floating(values, "frame_absolute_tolerance"),
        transport_rank_relative_tolerance=_floating(
            values, "transport_rank_relative_tolerance"
        ),
        transport_validation_relative_tolerance=_floating(
            values, "transport_validation_relative_tolerance"
        ),
        harmonic_absolute_degeneracy_tolerance=_floating(
            values, "harmonic_absolute_degeneracy_tolerance"
        ),
        harmonic_relative_degeneracy_tolerance=_floating(
            values, "harmonic_relative_degeneracy_tolerance"
        ),
    )
    if (
        _floating(values, "verification_absolute_tolerance")
        != request.verification_absolute_tolerance
    ):
        raise ValueError(
            "verification_absolute_tolerance does not match installed policy"
        )
    expected_identity: Mapping[str, int | str] = {
        "ambient_rank": request.ambient_rank,
        "retained_rank": request.retained_rank,
        "parent_model_identifier": request.parent_model_identifier,
        "ambient_basis_identifier": request.ambient_basis_identifier,
        "retained_frame_identifier": request.retained_frame_identifier,
        "endpoint_sewing_identifier": request.endpoint_sewing_identifier,
        "energy_reference_identifier": request.energy_reference_identifier,
        "reciprocal_coordinate_convention": request.reciprocal_coordinate_convention,
        "gauge_attack_identifier": request.gauge_attack_identifier,
    }
    for name, expected in expected_identity.items():
        observed = (
            _integer(values, name) if type(expected) is int else _string(values, name)
        )
        if observed != expected:
            raise ValueError(f"{name} does not identify the installed control")
    return request


@dataclass(frozen=True, slots=True)
class Periodic1DRank2QualificationRecord(BaseTypedRecord):
    """Retain one closed qualification variant without null padding."""

    qualification: Periodic1DRank2Qualification

    def __post_init__(self) -> None:
        allowed = (
            Periodic1DRank2ExternalGapFailure,
            Periodic1DRank2BandTransportBackendFailure,
            Periodic1DRank2BandTransportNumericallyUnresolved,
            Periodic1DRank2BandTransportThresholdFailure,
            Periodic1DRank2QualifiedParent,
        )
        if type(self.qualification) not in allowed:
            raise TypeError(
                "qualification must be one closed embedded-subspace/rank2 variant"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        qualification = self.qualification
        common: dict[str, SerializableValue] = {
            "minimum_external_gap": qualification.minimum_external_gap,
        }
        if type(qualification) is Periodic1DRank2ExternalGapFailure:
            return {
                "variant": _QualificationWireVariant.EXTERNAL_GAP_FAILURE.value,
            } | common
        if type(qualification) is Periodic1DRank2BandTransportBackendFailure:
            return {
                "variant": (
                    _QualificationWireVariant.BAND_TRANSPORT_BACKEND_FAILURE.value
                ),
                **common,
                "band_transport_backend_operation": qualification.operation.value,
                "band_transport_backend_failure_reason": qualification.reason.value,
                "band_transport_backend_link_index": qualification.link_index,
            }
        if type(qualification) is Periodic1DRank2BandTransportNumericallyUnresolved:
            return {
                "variant": (
                    _QualificationWireVariant.BAND_TRANSPORT_NUMERICALLY_UNRESOLVED.value
                ),
                **common,
                "band_transport_status": qualification.band_transport_status.value,
                "minimum_transport_singular_value": (
                    qualification.minimum_transport_singular_value
                ),
            }
        if type(qualification) is Periodic1DRank2BandTransportThresholdFailure:
            return {
                "variant": (
                    _QualificationWireVariant.BAND_TRANSPORT_THRESHOLD_FAILURE.value
                ),
                **common,
                "minimum_transport_singular_value": (
                    qualification.minimum_transport_singular_value
                ),
            }
        if type(qualification) is Periodic1DRank2QualifiedParent:
            return {
                "variant": _QualificationWireVariant.QUALIFIED_PARENT.value,
                **common,
                "minimum_transport_singular_value": (
                    qualification.minimum_transport_singular_value
                ),
                "maximum_transport_rank_cutoff": (
                    qualification.maximum_transport_rank_cutoff
                ),
                "maximum_transport_unitarity_defect": (
                    qualification.maximum_transport_unitarity_defect
                ),
                "maximum_primitive_link_frobenius_residual": (
                    qualification.maximum_primitive_link_frobenius_residual
                ),
                "closure_holonomy_phases": qualification.closure_holonomy_phases,
                "closure_alignment_residual": (
                    qualification.closure_alignment_residual
                ),
                "closure_alignment_unitarity_defect": (
                    qualification.closure_alignment_unitarity_defect
                ),
                "maximum_frame_orthonormality_defect": (
                    qualification.maximum_frame_orthonormality_defect
                ),
                "maximum_reference_hermiticity_defect": (
                    qualification.maximum_reference_hermiticity_defect
                ),
            }
        raise TypeError("qualification variant is not supported")

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        try:
            variant = _QualificationWireVariant(_string(values, "variant"))
        except ValueError as error:
            raise ValueError(
                "unknown embedded-subspace rank-two qualification variant"
            ) from error
        common = {"variant", "minimum_external_gap"}
        minimum_gap = _floating(values, "minimum_external_gap")
        if variant is _QualificationWireVariant.EXTERNAL_GAP_FAILURE:
            _fields(values, common, "external-gap qualification record")
            return cls(Periodic1DRank2ExternalGapFailure(minimum_gap))
        if variant is _QualificationWireVariant.BAND_TRANSPORT_BACKEND_FAILURE:
            _fields(
                values,
                common
                | {
                    "band_transport_backend_operation",
                    "band_transport_backend_failure_reason",
                    "band_transport_backend_link_index",
                },
                "band-transport backend qualification record",
            )
            try:
                operation = ClosedLoopPolarFrameTransportBackendOperation(
                    _string(values, "band_transport_backend_operation")
                )
                reason = ClosedLoopPolarFrameTransportBackendFailureReason(
                    _string(values, "band_transport_backend_failure_reason")
                )
            except ValueError as error:
                raise ValueError(
                    "unknown typed band-transport backend value"
                ) from error
            return cls(
                Periodic1DRank2BandTransportBackendFailure(
                    minimum_external_gap=minimum_gap,
                    operation=operation,
                    reason=reason,
                    link_index=_integer(values, "band_transport_backend_link_index"),
                )
            )
        if variant is _QualificationWireVariant.BAND_TRANSPORT_NUMERICALLY_UNRESOLVED:
            _fields(
                values,
                common
                | {
                    "band_transport_status",
                    "minimum_transport_singular_value",
                },
                "numerically unresolved band-transport qualification record",
            )
            try:
                status = ClosedLoopPolarFrameTransportStatus(
                    _string(values, "band_transport_status")
                )
            except ValueError as error:
                raise ValueError("unknown typed band-transport status") from error
            return cls(
                Periodic1DRank2BandTransportNumericallyUnresolved(
                    minimum_external_gap=minimum_gap,
                    band_transport_status=status,
                    minimum_transport_singular_value=_floating(
                        values, "minimum_transport_singular_value"
                    ),
                )
            )
        if variant is _QualificationWireVariant.BAND_TRANSPORT_THRESHOLD_FAILURE:
            _fields(
                values,
                common | {"minimum_transport_singular_value"},
                "band-transport threshold qualification record",
            )
            return cls(
                Periodic1DRank2BandTransportThresholdFailure(
                    minimum_external_gap=minimum_gap,
                    minimum_transport_singular_value=_floating(
                        values, "minimum_transport_singular_value"
                    ),
                )
            )
        if variant is not _QualificationWireVariant.QUALIFIED_PARENT:
            raise ValueError(
                "unsupported embedded-subspace rank-two qualification variant"
            )
        qualified_fields = {
            "minimum_transport_singular_value",
            "maximum_transport_rank_cutoff",
            "maximum_transport_unitarity_defect",
            "maximum_primitive_link_frobenius_residual",
            "closure_holonomy_phases",
            "closure_alignment_residual",
            "closure_alignment_unitarity_defect",
            "maximum_frame_orthonormality_defect",
            "maximum_reference_hermiticity_defect",
        }
        _fields(values, common | qualified_fields, "qualified-parent record")
        return cls(
            Periodic1DRank2QualifiedParent(
                minimum_external_gap=minimum_gap,
                minimum_transport_singular_value=_floating(
                    values, "minimum_transport_singular_value"
                ),
                maximum_transport_rank_cutoff=_floating(
                    values, "maximum_transport_rank_cutoff"
                ),
                maximum_transport_unitarity_defect=_floating(
                    values, "maximum_transport_unitarity_defect"
                ),
                maximum_primitive_link_frobenius_residual=_floating(
                    values, "maximum_primitive_link_frobenius_residual"
                ),
                closure_holonomy_phases=_float_tuple(values, "closure_holonomy_phases"),
                closure_alignment_residual=_floating(
                    values, "closure_alignment_residual"
                ),
                closure_alignment_unitarity_defect=_floating(
                    values, "closure_alignment_unitarity_defect"
                ),
                maximum_frame_orthonormality_defect=_floating(
                    values, "maximum_frame_orthonormality_defect"
                ),
                maximum_reference_hermiticity_defect=_floating(
                    values, "maximum_reference_hermiticity_defect"
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2HoppingPowerRecord(BaseTypedRecord):
    """Retain paired reference and attacked power at one displacement."""

    value: Periodic1DRank2HoppingPower

    def __post_init__(self) -> None:
        if type(self.value) is not Periodic1DRank2HoppingPower:
            raise TypeError("value must be Periodic1DRank2HoppingPower")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "displacement": self.value.displacement,
            "reference_normalized_squared_frobenius_norm": (
                self.value.reference_normalized_squared_frobenius_norm
            ),
            "comparison_normalized_squared_frobenius_norm": (
                self.value.comparison_normalized_squared_frobenius_norm
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {
                "displacement",
                "reference_normalized_squared_frobenius_norm",
                "comparison_normalized_squared_frobenius_norm",
            },
            "embedded-subspace/rank2 hopping-power record",
        )
        return cls(
            Periodic1DRank2HoppingPower(
                displacement=_integer(values, "displacement"),
                reference_normalized_squared_frobenius_norm=_floating(
                    values, "reference_normalized_squared_frobenius_norm"
                ),
                comparison_normalized_squared_frobenius_norm=_floating(
                    values, "comparison_normalized_squared_frobenius_norm"
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2HarmonicMaximumRecord(BaseTypedRecord):
    """Retain the complete restricted harmonic maximum value."""

    value: PeriodicHarmonicMaximum

    def __post_init__(self) -> None:
        if type(self.value) is not PeriodicHarmonicMaximum:
            raise TypeError("value must be PeriodicHarmonicMaximum")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        value = self.value
        harmonic = value.harmonic
        return {
            "harmonic": {
                "offset": harmonic.offset,
                "cosine_coefficient": harmonic.cosine_coefficient,
                "sine_coefficient": harmonic.sine_coefficient,
                "harmonic_order": harmonic.harmonic_order,
                "fundamental_interval_start": harmonic.fundamental_interval_start,
            },
            "maximum_value": value.maximum_value,
            "amplitude": value.amplitude,
            "canonical_maximizing_argument": value.canonical_maximizing_argument,
            "fundamental_period": value.fundamental_period,
            "applied_degeneracy_cutoff": value.applied_degeneracy_cutoff,
            "status": value.status.value,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {
                "harmonic",
                "maximum_value",
                "amplitude",
                "canonical_maximizing_argument",
                "fundamental_period",
                "applied_degeneracy_cutoff",
                "status",
            },
            "harmonic-maximum record",
        )
        harmonic_values = _mapping_value(values, "harmonic")
        _fields(
            harmonic_values,
            {
                "offset",
                "cosine_coefficient",
                "sine_coefficient",
                "harmonic_order",
                "fundamental_interval_start",
            },
            "harmonic record",
        )
        status_text = _string(values, "status")
        try:
            status = PeriodicHarmonicMaximumStatus(status_text)
        except ValueError as error:
            raise ValueError("unknown harmonic maximum status") from error
        return cls(
            PeriodicHarmonicMaximum(
                harmonic=PeriodicHarmonic(
                    offset=_floating(harmonic_values, "offset"),
                    cosine_coefficient=_floating(harmonic_values, "cosine_coefficient"),
                    sine_coefficient=_floating(harmonic_values, "sine_coefficient"),
                    harmonic_order=_integer(harmonic_values, "harmonic_order"),
                    fundamental_interval_start=_floating(
                        harmonic_values, "fundamental_interval_start"
                    ),
                ),
                maximum_value=_floating(values, "maximum_value"),
                amplitude=_floating(values, "amplitude"),
                canonical_maximizing_argument=_optional_float(
                    values, "canonical_maximizing_argument"
                ),
                fundamental_period=_floating(values, "fundamental_period"),
                applied_degeneracy_cutoff=_floating(
                    values, "applied_degeneracy_cutoff"
                ),
                status=status,
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2PointAnalysisRecord(BaseTypedRecord):
    """Retain one qualified embedded-subspace/rank2 amplitude point."""

    value: Periodic1DRank2PointAnalysis

    def __post_init__(self) -> None:
        if type(self.value) is not Periodic1DRank2PointAnalysis:
            raise TypeError("value must be Periodic1DRank2PointAnalysis")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        value = self.value
        return {
            "amplitude": value.amplitude,
            "maximum_band_defect": value.maximum_band_defect,
            "splitting_scale": value.splitting_scale,
            "harmonic_maximum": Periodic1DRank2HarmonicMaximumRecord(
                value.harmonic_maximum
            ).to_dict(),
            "discrete_maximum_correlation": value.discrete_maximum_correlation,
            "minimum_operator_threshold": value.minimum_operator_threshold,
            "exact_spectrum_joint_operator_threshold": (
                value.exact_spectrum_joint_operator_threshold
            ),
            "minimum_loss_reconstruction_defect": (
                value.minimum_loss_reconstruction_defect
            ),
            "reference_nonzero_hopping_weight": (
                value.reference_nonzero_hopping_weight
            ),
            "comparison_nonzero_hopping_weight": (
                value.comparison_nonzero_hopping_weight
            ),
            "reference_parseval_defect": value.reference_parseval_defect,
            "comparison_parseval_defect": value.comparison_parseval_defect,
            "hopping_powers": tuple(
                Periodic1DRank2HoppingPowerRecord(item).to_dict()
                for item in value.hopping_powers
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        floats = {
            "amplitude",
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
        }
        _fields(
            values,
            floats | {"harmonic_maximum", "hopping_powers"},
            "embedded-subspace/rank2 point record",
        )
        scalar = {name: _floating(values, name) for name in floats}
        return cls(
            Periodic1DRank2PointAnalysis(
                amplitude=scalar["amplitude"],
                maximum_band_defect=scalar["maximum_band_defect"],
                splitting_scale=scalar["splitting_scale"],
                harmonic_maximum=(
                    Periodic1DRank2HarmonicMaximumRecord.from_dict(
                        _mapping_value(values, "harmonic_maximum")
                    ).value
                ),
                discrete_maximum_correlation=scalar["discrete_maximum_correlation"],
                minimum_operator_threshold=scalar["minimum_operator_threshold"],
                exact_spectrum_joint_operator_threshold=scalar[
                    "exact_spectrum_joint_operator_threshold"
                ],
                minimum_loss_reconstruction_defect=scalar[
                    "minimum_loss_reconstruction_defect"
                ],
                reference_nonzero_hopping_weight=scalar[
                    "reference_nonzero_hopping_weight"
                ],
                comparison_nonzero_hopping_weight=scalar[
                    "comparison_nonzero_hopping_weight"
                ],
                reference_parseval_defect=scalar["reference_parseval_defect"],
                comparison_parseval_defect=scalar["comparison_parseval_defect"],
                hopping_powers=tuple(
                    Periodic1DRank2HoppingPowerRecord.from_dict(item).value
                    for item in _mapping_tuple(values, "hopping_powers")
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2AnalysisRecord(BaseTypedRecord):
    """Own canonical bytes for one immutable embedded-subspace/rank2 analysis."""

    analysis: Periodic1DRank2Analysis

    def __post_init__(self) -> None:
        if type(self.analysis) is not Periodic1DRank2Analysis:
            raise TypeError("analysis must be Periodic1DRank2Analysis")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "request": _request_mapping(self.analysis.request),
            "qualification": Periodic1DRank2QualificationRecord(
                self.analysis.qualification
            ).to_dict(),
            "points": tuple(
                Periodic1DRank2PointAnalysisRecord(point).to_dict()
                for point in self.analysis.points
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {"request", "qualification", "points"},
            "embedded-subspace/rank2 analysis record",
        )
        return cls(
            Periodic1DRank2Analysis(
                request=_request_from_mapping(_mapping_value(values, "request")),
                qualification=Periodic1DRank2QualificationRecord.from_dict(
                    _mapping_value(values, "qualification")
                ).qualification,
                points=tuple(
                    Periodic1DRank2PointAnalysisRecord.from_dict(item).value
                    for item in _mapping_tuple(values, "points")
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2ParentFamilyAnalysisRecord(BaseTypedRecord):
    """Own canonical bytes for one immutable parent-hopping family analysis."""

    analysis: Periodic1DRank2ParentFamilyAnalysis

    def __post_init__(self) -> None:
        if type(self.analysis) is not (Periodic1DRank2ParentFamilyAnalysis):
            raise TypeError("analysis must be Periodic1DRank2ParentFamilyAnalysis")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "request": {
                "template_request": _request_mapping(
                    self.analysis.request.template_request
                ),
                "parent_hopping_scales": (self.analysis.request.parent_hopping_scales),
            },
            "members": tuple(
                Periodic1DRank2AnalysisRecord(member).to_dict()
                for member in self.analysis.members
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {"request", "members"},
            "embedded-subspace/rank2 parent-family analysis record",
        )
        request_values = _mapping_value(values, "request")
        _fields(
            request_values,
            {"template_request", "parent_hopping_scales"},
            "embedded-subspace/rank2 parent-family request mapping",
        )
        request = Periodic1DRank2ParentFamilyRequest(
            template_request=_request_from_mapping(
                _mapping_value(request_values, "template_request")
            ),
            parent_hopping_scales=_float_tuple(request_values, "parent_hopping_scales"),
        )
        return cls(
            Periodic1DRank2ParentFamilyAnalysis(
                request=request,
                members=tuple(
                    Periodic1DRank2AnalysisRecord.from_dict(member).analysis
                    for member in _mapping_tuple(values, "members")
                ),
            )
        )


def _momentum_thresholds_mapping(
    value: Periodic1DRank2MomentumRefinementThresholds,
) -> Mapping[str, SerializableValue]:
    return {
        name: getattr(value, name)
        for name in (
            "maximum_parent_diagnostic_change",
            "maximum_correlation_change",
            "maximum_threshold_change",
            "maximum_hopping_weight_change",
            "maximum_hopping_power_change",
            "maximum_angle_change",
            "maximum_band_defect",
            "maximum_reconstruction_defect",
            "maximum_parseval_defect",
        )
    }


def _momentum_thresholds_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2MomentumRefinementThresholds:
    names = {
        "maximum_parent_diagnostic_change",
        "maximum_correlation_change",
        "maximum_threshold_change",
        "maximum_hopping_weight_change",
        "maximum_hopping_power_change",
        "maximum_angle_change",
        "maximum_band_defect",
        "maximum_reconstruction_defect",
        "maximum_parseval_defect",
    }
    _fields(values, names, "momentum thresholds")
    return Periodic1DRank2MomentumRefinementThresholds(
        **{name: _floating(values, name) for name in names}
    )


def _momentum_request_mapping(
    value: Periodic1DRank2MomentumRefinementRequest,
) -> Mapping[str, SerializableValue]:
    return {
        "template_request": _request_mapping(value.template_request),
        "reciprocal_mesh_sizes": value.reciprocal_mesh_sizes,
        "thresholds": _momentum_thresholds_mapping(value.thresholds),
        "required_stable_refinements": value.required_stable_refinements,
    }


def _momentum_request_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2MomentumRefinementRequest:
    _fields(
        values,
        {
            "template_request",
            "reciprocal_mesh_sizes",
            "thresholds",
            "required_stable_refinements",
        },
        "momentum request",
    )
    return Periodic1DRank2MomentumRefinementRequest(
        template_request=_request_from_mapping(
            _mapping_value(values, "template_request")
        ),
        reciprocal_mesh_sizes=_integer_tuple(values, "reciprocal_mesh_sizes"),
        thresholds=_momentum_thresholds_from_mapping(
            _mapping_value(values, "thresholds")
        ),
        required_stable_refinements=_integer(values, "required_stable_refinements"),
    )


def _momentum_step_mapping(
    value: Periodic1DRank2MomentumRefinementStep,
) -> Mapping[str, SerializableValue]:
    names = (
        "coarse_mesh_size",
        "fine_mesh_size",
        "maximum_parent_diagnostic_change",
        "maximum_shared_parent_eigenvalue_defect",
        "maximum_shared_parent_projector_defect",
        "maximum_correlation_change",
        "maximum_threshold_change",
        "maximum_hopping_weight_change",
        "maximum_hopping_power_change",
        "maximum_angle_change",
        "maximizing_angle_dispositions_stable",
        "maximum_band_defect",
        "maximum_reconstruction_defect",
        "maximum_parseval_defect",
        "within_tolerances",
    )
    return {name: getattr(value, name) for name in names}


def _momentum_step_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2MomentumRefinementStep:
    integer_names = {"coarse_mesh_size", "fine_mesh_size"}
    boolean_names = {
        "maximizing_angle_dispositions_stable",
        "within_tolerances",
    }
    float_names = {
        "maximum_parent_diagnostic_change",
        "maximum_shared_parent_eigenvalue_defect",
        "maximum_shared_parent_projector_defect",
        "maximum_correlation_change",
        "maximum_threshold_change",
        "maximum_hopping_weight_change",
        "maximum_hopping_power_change",
        "maximum_angle_change",
        "maximum_band_defect",
        "maximum_reconstruction_defect",
        "maximum_parseval_defect",
    }
    _fields(values, integer_names | boolean_names | float_names, "momentum step")
    return Periodic1DRank2MomentumRefinementStep(
        coarse_mesh_size=_integer(values, "coarse_mesh_size"),
        fine_mesh_size=_integer(values, "fine_mesh_size"),
        maximum_parent_diagnostic_change=_floating(
            values, "maximum_parent_diagnostic_change"
        ),
        maximum_shared_parent_eigenvalue_defect=_floating(
            values, "maximum_shared_parent_eigenvalue_defect"
        ),
        maximum_shared_parent_projector_defect=_floating(
            values, "maximum_shared_parent_projector_defect"
        ),
        maximum_correlation_change=_floating(values, "maximum_correlation_change"),
        maximum_threshold_change=_floating(values, "maximum_threshold_change"),
        maximum_hopping_weight_change=_floating(
            values, "maximum_hopping_weight_change"
        ),
        maximum_hopping_power_change=_floating(values, "maximum_hopping_power_change"),
        maximum_angle_change=_floating(values, "maximum_angle_change"),
        maximizing_angle_dispositions_stable=_boolean(
            values, "maximizing_angle_dispositions_stable"
        ),
        maximum_band_defect=_floating(values, "maximum_band_defect"),
        maximum_reconstruction_defect=_floating(
            values, "maximum_reconstruction_defect"
        ),
        maximum_parseval_defect=_floating(values, "maximum_parseval_defect"),
        within_tolerances=_boolean(values, "within_tolerances"),
    )


def _momentum_mapping(
    value: Periodic1DRank2MomentumRefinementAnalysis,
) -> Mapping[str, SerializableValue]:
    if type(value) is (Periodic1DRank2MomentumRefinementQualificationStopped):
        variant = CalculationWireEnum.MOMENTUM_QUALIFICATION_STOPPED
    elif type(value) is Periodic1DRank2MomentumRefinementConverged:
        variant = CalculationWireEnum.MOMENTUM_CONVERGED
    elif type(value) is Periodic1DRank2MomentumRefinementUnresolved:
        variant = CalculationWireEnum.MOMENTUM_UNRESOLVED
    else:
        raise TypeError("momentum_refinement must be one closed outcome variant")
    return {
        "variant": variant.value,
        "request": _momentum_request_mapping(value.request),
        "mesh_analyses": tuple(
            Periodic1DRank2AnalysisRecord(item).to_dict()
            for item in value.mesh_analyses
        ),
        "refinements": tuple(
            _momentum_step_mapping(item) for item in value.refinements
        ),
    }


def _momentum_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2MomentumRefinementAnalysis:
    _fields(
        values,
        {"variant", "request", "mesh_analyses", "refinements"},
        "momentum refinement",
    )
    try:
        variant = CalculationWireEnum(_string(values, "variant"))
    except ValueError as error:
        raise ValueError("unknown momentum-refinement variant") from error
    request = _momentum_request_from_mapping(_mapping_value(values, "request"))
    mesh_analyses = tuple(
        Periodic1DRank2AnalysisRecord.from_dict(item).analysis
        for item in _mapping_tuple(values, "mesh_analyses")
    )
    refinements = tuple(
        _momentum_step_from_mapping(item)
        for item in _mapping_tuple(values, "refinements")
    )
    if variant is CalculationWireEnum.MOMENTUM_QUALIFICATION_STOPPED:
        return Periodic1DRank2MomentumRefinementQualificationStopped(
            request=request,
            mesh_analyses=mesh_analyses,
            refinements=refinements,
        )
    if variant is CalculationWireEnum.MOMENTUM_CONVERGED:
        return Periodic1DRank2MomentumRefinementConverged(
            request=request,
            mesh_analyses=mesh_analyses,
            refinements=refinements,
        )
    if variant is CalculationWireEnum.MOMENTUM_UNRESOLVED:
        return Periodic1DRank2MomentumRefinementUnresolved(
            request=request,
            mesh_analyses=mesh_analyses,
            refinements=refinements,
        )
    raise ValueError("variant does not identify a momentum-refinement outcome")


def _amplitude_thresholds_mapping(
    value: Periodic1DRank2AmplitudeRefinementThresholds,
) -> Mapping[str, SerializableValue]:
    return {
        name: getattr(value, name)
        for name in (
            "maximum_correlation_defect",
            "maximum_operator_threshold_defect",
            "maximum_joint_threshold_defect",
            "maximum_hopping_weight_defect",
            "maximum_hopping_power_defect",
        )
    }


def _amplitude_thresholds_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2AmplitudeRefinementThresholds:
    names = {
        "maximum_correlation_defect",
        "maximum_operator_threshold_defect",
        "maximum_joint_threshold_defect",
        "maximum_hopping_weight_defect",
        "maximum_hopping_power_defect",
    }
    _fields(values, names, "amplitude thresholds")
    return Periodic1DRank2AmplitudeRefinementThresholds(
        **{name: _floating(values, name) for name in names}
    )


def _amplitude_request_mapping(
    value: Periodic1DRank2AdaptiveAmplitudeRequest,
) -> Mapping[str, SerializableValue]:
    return {
        "template_request": _request_mapping(value.template_request),
        "thresholds": _amplitude_thresholds_mapping(value.thresholds),
        "maximum_refinement_levels": value.maximum_refinement_levels,
        "maximum_evaluated_amplitudes": value.maximum_evaluated_amplitudes,
    }


def _amplitude_request_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2AdaptiveAmplitudeRequest:
    _fields(
        values,
        {
            "template_request",
            "thresholds",
            "maximum_refinement_levels",
            "maximum_evaluated_amplitudes",
        },
        "adaptive-amplitude request",
    )
    return Periodic1DRank2AdaptiveAmplitudeRequest(
        template_request=_request_from_mapping(
            _mapping_value(values, "template_request")
        ),
        thresholds=_amplitude_thresholds_from_mapping(
            _mapping_value(values, "thresholds")
        ),
        maximum_refinement_levels=_integer(values, "maximum_refinement_levels"),
        maximum_evaluated_amplitudes=_integer(values, "maximum_evaluated_amplitudes"),
    )


def _amplitude_check_mapping(
    value: Periodic1DRank2AmplitudeRefinementLevel | Periodic1DRank2AmplitudeValidation,
) -> Mapping[str, SerializableValue]:
    mapping: dict[str, SerializableValue] = {
        "level_index": value.level_index,
        "interpolation_nodes": value.interpolation_nodes,
        "evaluated_amplitudes": value.evaluated_amplitudes,
        "maximum_correlation_defect": value.maximum_correlation_defect,
        "maximum_operator_threshold_defect": (value.maximum_operator_threshold_defect),
        "maximum_joint_threshold_defect": value.maximum_joint_threshold_defect,
        "maximum_hopping_weight_defect": value.maximum_hopping_weight_defect,
        "maximum_hopping_power_defect": value.maximum_hopping_power_defect,
        "within_tolerances": value.within_tolerances,
    }
    if type(value) is Periodic1DRank2AmplitudeRefinementLevel:
        mapping["failing_interval_indices"] = value.failing_interval_indices
    elif type(value) is Periodic1DRank2AmplitudeValidation:
        mapping["failing_point_indices"] = value.failing_point_indices
    else:
        raise TypeError("amplitude check must be a level or validation")
    return mapping


def _amplitude_check_from_mapping(
    values: Mapping[str, SerializableValue],
    *,
    validation: bool,
) -> Periodic1DRank2AmplitudeRefinementLevel | Periodic1DRank2AmplitudeValidation:
    index_name = "failing_point_indices" if validation else "failing_interval_indices"
    names = {
        "level_index",
        "interpolation_nodes",
        "evaluated_amplitudes",
        "maximum_correlation_defect",
        "maximum_operator_threshold_defect",
        "maximum_joint_threshold_defect",
        "maximum_hopping_weight_defect",
        "maximum_hopping_power_defect",
        index_name,
        "within_tolerances",
    }
    _fields(values, names, "amplitude validation" if validation else "amplitude level")
    if validation:
        return Periodic1DRank2AmplitudeValidation(
            level_index=_integer(values, "level_index"),
            interpolation_nodes=_float_tuple(values, "interpolation_nodes"),
            evaluated_amplitudes=_float_tuple(values, "evaluated_amplitudes"),
            maximum_correlation_defect=_floating(values, "maximum_correlation_defect"),
            maximum_operator_threshold_defect=_floating(
                values, "maximum_operator_threshold_defect"
            ),
            maximum_joint_threshold_defect=_floating(
                values, "maximum_joint_threshold_defect"
            ),
            maximum_hopping_weight_defect=_floating(
                values, "maximum_hopping_weight_defect"
            ),
            maximum_hopping_power_defect=_floating(
                values, "maximum_hopping_power_defect"
            ),
            failing_point_indices=_integer_tuple(values, index_name),
            within_tolerances=_boolean(values, "within_tolerances"),
        )
    return Periodic1DRank2AmplitudeRefinementLevel(
        level_index=_integer(values, "level_index"),
        interpolation_nodes=_float_tuple(values, "interpolation_nodes"),
        evaluated_amplitudes=_float_tuple(values, "evaluated_amplitudes"),
        maximum_correlation_defect=_floating(values, "maximum_correlation_defect"),
        maximum_operator_threshold_defect=_floating(
            values, "maximum_operator_threshold_defect"
        ),
        maximum_joint_threshold_defect=_floating(
            values, "maximum_joint_threshold_defect"
        ),
        maximum_hopping_weight_defect=_floating(
            values, "maximum_hopping_weight_defect"
        ),
        maximum_hopping_power_defect=_floating(values, "maximum_hopping_power_defect"),
        failing_interval_indices=_integer_tuple(values, index_name),
        within_tolerances=_boolean(values, "within_tolerances"),
    )


def _amplitude_level_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2AmplitudeRefinementLevel:
    result = _amplitude_check_from_mapping(values, validation=False)
    if type(result) is not (Periodic1DRank2AmplitudeRefinementLevel):
        raise TypeError("amplitude level decoded to the wrong type")
    return result


def _amplitude_validation_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2AmplitudeValidation:
    result = _amplitude_check_from_mapping(values, validation=True)
    if type(result) is not Periodic1DRank2AmplitudeValidation:
        raise TypeError("amplitude validation decoded to the wrong type")
    return result


def _amplitude_mapping(
    value: Periodic1DRank2AdaptiveAmplitudeAnalysis,
) -> Mapping[str, SerializableValue]:
    mapping: dict[str, SerializableValue] = {
        "request": _amplitude_request_mapping(value.request),
        "evaluations": tuple(
            Periodic1DRank2AnalysisRecord(item).to_dict() for item in value.evaluations
        ),
    }
    if type(value) is (Periodic1DRank2AdaptiveAmplitudeQualificationStopped):
        mapping["variant"] = CalculationWireEnum.AMPLITUDE_QUALIFICATION_STOPPED.value
        return mapping
    if not isinstance(
        value,
        (
            Periodic1DRank2AdaptiveAmplitudeConverged,
            Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
            Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
        ),
    ):
        raise TypeError("adaptive_amplitude must be one closed outcome variant")
    mapping["levels"] = tuple(_amplitude_check_mapping(item) for item in value.levels)
    mapping["validations"] = tuple(
        _amplitude_check_mapping(item) for item in value.validations
    )
    if type(value) is Periodic1DRank2AdaptiveAmplitudeConverged:
        mapping["variant"] = CalculationWireEnum.AMPLITUDE_CONVERGED.value
    elif type(value) is (Periodic1DRank2AdaptiveAmplitudeLevelsExhausted):
        mapping["variant"] = CalculationWireEnum.AMPLITUDE_LEVELS_EXHAUSTED.value
    elif type(value) is (Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted):
        mapping["variant"] = CalculationWireEnum.AMPLITUDE_EVALUATIONS_EXHAUSTED.value
        mapping["blocked_amplitudes"] = value.blocked_amplitudes
    else:
        raise TypeError("adaptive_amplitude must be one closed outcome variant")
    return mapping


def _amplitude_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2AdaptiveAmplitudeAnalysis:
    try:
        variant = CalculationWireEnum(_string(values, "variant"))
    except ValueError as error:
        raise ValueError("unknown adaptive-amplitude variant") from error
    common_names = {"variant", "request", "evaluations"}
    if variant is CalculationWireEnum.AMPLITUDE_QUALIFICATION_STOPPED:
        _fields(values, common_names, "adaptive-amplitude qualification stop")
    else:
        expected = common_names | {"levels", "validations"}
        if variant is CalculationWireEnum.AMPLITUDE_EVALUATIONS_EXHAUSTED:
            expected.add("blocked_amplitudes")
        _fields(values, expected, "adaptive-amplitude outcome")
    request = _amplitude_request_from_mapping(_mapping_value(values, "request"))
    evaluations = tuple(
        Periodic1DRank2AnalysisRecord.from_dict(item).analysis
        for item in _mapping_tuple(values, "evaluations")
    )
    if variant is CalculationWireEnum.AMPLITUDE_QUALIFICATION_STOPPED:
        return Periodic1DRank2AdaptiveAmplitudeQualificationStopped(
            request=request,
            evaluations=evaluations,
        )
    levels = tuple(
        _amplitude_level_from_mapping(item) for item in _mapping_tuple(values, "levels")
    )
    validations = tuple(
        _amplitude_validation_from_mapping(item)
        for item in _mapping_tuple(values, "validations")
    )
    if variant is CalculationWireEnum.AMPLITUDE_CONVERGED:
        return Periodic1DRank2AdaptiveAmplitudeConverged(
            request=request,
            evaluations=evaluations,
            levels=levels,
            validations=validations,
        )
    if variant is CalculationWireEnum.AMPLITUDE_LEVELS_EXHAUSTED:
        return Periodic1DRank2AdaptiveAmplitudeLevelsExhausted(
            request=request,
            evaluations=evaluations,
            levels=levels,
            validations=validations,
        )
    if variant is CalculationWireEnum.AMPLITUDE_EVALUATIONS_EXHAUSTED:
        return Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted(
            request=request,
            evaluations=evaluations,
            levels=levels,
            validations=validations,
            blocked_amplitudes=_float_tuple(values, "blocked_amplitudes"),
        )
    raise ValueError("variant does not identify an adaptive-amplitude outcome")


def _truncation_request_mapping(
    value: Periodic1DRank2SupportTruncationAnalysisRequest,
) -> Mapping[str, SerializableValue]:
    return {
        "template_request": _request_mapping(value.template_request),
        "maximum_ranges": value.maximum_ranges,
        "evaluation_mesh_size": value.evaluation_mesh_size,
    }


def _truncation_request_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2SupportTruncationAnalysisRequest:
    from ksdft2effmass.periodic1d.rank2.support_truncation.request import (
        Periodic1DRank2SupportTruncationAnalysisRequest,
    )

    _fields(
        values,
        {"template_request", "maximum_ranges", "evaluation_mesh_size"},
        "truncation request",
    )
    return Periodic1DRank2SupportTruncationAnalysisRequest(
        template_request=_request_from_mapping(
            _mapping_value(values, "template_request")
        ),
        maximum_ranges=_integer_tuple(values, "maximum_ranges"),
        evaluation_mesh_size=_integer(values, "evaluation_mesh_size"),
    )


def _truncation_range_mapping(
    value: Periodic1DRank2TruncationRange,
) -> Mapping[str, SerializableValue]:
    return {
        name: getattr(value, name)
        for name in (
            "maximum_range",
            "reference_ordinary_omitted_power",
            "comparison_ordinary_omitted_power",
            "reference_total_omitted_power",
            "comparison_total_omitted_power",
            "reference_truncation_hamiltonian_maximum_error",
            "reference_truncation_hamiltonian_rms_error",
            "reference_truncation_spectral_maximum_error",
            "reference_truncation_spectral_rms_error",
            "comparison_truncation_hamiltonian_maximum_error",
            "comparison_truncation_hamiltonian_rms_error",
            "comparison_truncation_spectral_maximum_error",
            "comparison_truncation_spectral_rms_error",
            "comparison_total_hamiltonian_maximum_error",
            "comparison_total_hamiltonian_rms_error",
            "comparison_total_spectral_maximum_error",
            "comparison_total_spectral_rms_error",
        )
    }


def _truncation_range_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2TruncationRange:
    from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
        Periodic1DRank2TruncationRange,
    )

    float_names = {
        "reference_ordinary_omitted_power",
        "comparison_ordinary_omitted_power",
        "reference_total_omitted_power",
        "comparison_total_omitted_power",
        "reference_truncation_hamiltonian_maximum_error",
        "reference_truncation_hamiltonian_rms_error",
        "reference_truncation_spectral_maximum_error",
        "reference_truncation_spectral_rms_error",
        "comparison_truncation_hamiltonian_maximum_error",
        "comparison_truncation_hamiltonian_rms_error",
        "comparison_truncation_spectral_maximum_error",
        "comparison_truncation_spectral_rms_error",
        "comparison_total_hamiltonian_maximum_error",
        "comparison_total_hamiltonian_rms_error",
        "comparison_total_spectral_maximum_error",
        "comparison_total_spectral_rms_error",
    }
    _fields(values, {"maximum_range"} | float_names, "truncation range")
    return Periodic1DRank2TruncationRange(
        maximum_range=_integer(values, "maximum_range"),
        reference_ordinary_omitted_power=_floating(
            values, "reference_ordinary_omitted_power"
        ),
        comparison_ordinary_omitted_power=_floating(
            values, "comparison_ordinary_omitted_power"
        ),
        reference_total_omitted_power=_floating(
            values, "reference_total_omitted_power"
        ),
        comparison_total_omitted_power=_floating(
            values, "comparison_total_omitted_power"
        ),
        reference_truncation_hamiltonian_maximum_error=_floating(
            values, "reference_truncation_hamiltonian_maximum_error"
        ),
        reference_truncation_hamiltonian_rms_error=_floating(
            values, "reference_truncation_hamiltonian_rms_error"
        ),
        reference_truncation_spectral_maximum_error=_floating(
            values, "reference_truncation_spectral_maximum_error"
        ),
        reference_truncation_spectral_rms_error=_floating(
            values, "reference_truncation_spectral_rms_error"
        ),
        comparison_truncation_hamiltonian_maximum_error=_floating(
            values, "comparison_truncation_hamiltonian_maximum_error"
        ),
        comparison_truncation_hamiltonian_rms_error=_floating(
            values, "comparison_truncation_hamiltonian_rms_error"
        ),
        comparison_truncation_spectral_maximum_error=_floating(
            values, "comparison_truncation_spectral_maximum_error"
        ),
        comparison_truncation_spectral_rms_error=_floating(
            values, "comparison_truncation_spectral_rms_error"
        ),
        comparison_total_hamiltonian_maximum_error=_floating(
            values, "comparison_total_hamiltonian_maximum_error"
        ),
        comparison_total_hamiltonian_rms_error=_floating(
            values, "comparison_total_hamiltonian_rms_error"
        ),
        comparison_total_spectral_maximum_error=_floating(
            values, "comparison_total_spectral_maximum_error"
        ),
        comparison_total_spectral_rms_error=_floating(
            values, "comparison_total_spectral_rms_error"
        ),
    )


def _truncation_point_mapping(
    value: Periodic1DRank2TruncationPoint,
) -> Mapping[str, SerializableValue]:
    return {
        "amplitude": value.amplitude,
        "reference_nyquist_power": value.reference_nyquist_power,
        "comparison_nyquist_power": value.comparison_nyquist_power,
        "reference_ordinary_hermiticity_maximum_defect": (
            value.reference_ordinary_hermiticity_maximum_defect
        ),
        "comparison_ordinary_hermiticity_maximum_defect": (
            value.comparison_ordinary_hermiticity_maximum_defect
        ),
        "direct_spectral_maximum_defect": value.direct_spectral_maximum_defect,
        "comparison_interpolation_hamiltonian_maximum_error": (
            value.comparison_interpolation_hamiltonian_maximum_error
        ),
        "comparison_interpolation_hamiltonian_rms_error": (
            value.comparison_interpolation_hamiltonian_rms_error
        ),
        "comparison_interpolation_spectral_maximum_error": (
            value.comparison_interpolation_spectral_maximum_error
        ),
        "comparison_interpolation_spectral_rms_error": (
            value.comparison_interpolation_spectral_rms_error
        ),
        "ranges": tuple(_truncation_range_mapping(item) for item in value.ranges),
    }


def _truncation_point_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2TruncationPoint:
    from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
        Periodic1DRank2TruncationPoint,
    )

    float_names = {
        "amplitude",
        "reference_nyquist_power",
        "comparison_nyquist_power",
        "reference_ordinary_hermiticity_maximum_defect",
        "comparison_ordinary_hermiticity_maximum_defect",
        "direct_spectral_maximum_defect",
        "comparison_interpolation_hamiltonian_maximum_error",
        "comparison_interpolation_hamiltonian_rms_error",
        "comparison_interpolation_spectral_maximum_error",
        "comparison_interpolation_spectral_rms_error",
    }
    _fields(values, float_names | {"ranges"}, "truncation point")
    return Periodic1DRank2TruncationPoint(
        amplitude=_floating(values, "amplitude"),
        reference_nyquist_power=_floating(values, "reference_nyquist_power"),
        comparison_nyquist_power=_floating(values, "comparison_nyquist_power"),
        reference_ordinary_hermiticity_maximum_defect=_floating(
            values, "reference_ordinary_hermiticity_maximum_defect"
        ),
        comparison_ordinary_hermiticity_maximum_defect=_floating(
            values, "comparison_ordinary_hermiticity_maximum_defect"
        ),
        direct_spectral_maximum_defect=_floating(
            values, "direct_spectral_maximum_defect"
        ),
        comparison_interpolation_hamiltonian_maximum_error=_floating(
            values, "comparison_interpolation_hamiltonian_maximum_error"
        ),
        comparison_interpolation_hamiltonian_rms_error=_floating(
            values, "comparison_interpolation_hamiltonian_rms_error"
        ),
        comparison_interpolation_spectral_maximum_error=_floating(
            values, "comparison_interpolation_spectral_maximum_error"
        ),
        comparison_interpolation_spectral_rms_error=_floating(
            values, "comparison_interpolation_spectral_rms_error"
        ),
        ranges=tuple(
            _truncation_range_from_mapping(item)
            for item in _mapping_tuple(values, "ranges")
        ),
    )


def _truncation_mapping(
    value: Periodic1DRank2SupportTruncationAnalysis,
) -> Mapping[str, SerializableValue]:
    from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
        Periodic1DRank2TruncationCompleted,
        Periodic1DRank2TruncationQualificationStopped,
    )

    mapping: dict[str, SerializableValue] = {
        "request": _truncation_request_mapping(value.request),
        "qualification": Periodic1DRank2QualificationRecord(
            value.qualification
        ).to_dict(),
    }
    if type(value) is Periodic1DRank2TruncationQualificationStopped:
        mapping["variant"] = CalculationWireEnum.TRUNCATION_QUALIFICATION_STOPPED.value
    elif type(value) is Periodic1DRank2TruncationCompleted:
        mapping.update(
            {
                "variant": CalculationWireEnum.TRUNCATION_COMPLETED.value,
                "evaluation_coordinate_offset": value.evaluation_coordinate_offset,
                "minimum_construction_evaluation_separation": (
                    value.minimum_construction_evaluation_separation
                ),
                "points": tuple(
                    _truncation_point_mapping(item) for item in value.points
                ),
            }
        )
    else:
        raise TypeError("truncation must be one closed outcome variant")
    return mapping


def _truncation_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DRank2SupportTruncationAnalysis:
    from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
        Periodic1DRank2TruncationCompleted,
        Periodic1DRank2TruncationQualificationStopped,
    )

    try:
        variant = CalculationWireEnum(_string(values, "variant"))
    except ValueError as error:
        raise ValueError("unknown truncation variant") from error
    common_names = {"variant", "request", "qualification"}
    if variant is CalculationWireEnum.TRUNCATION_QUALIFICATION_STOPPED:
        _fields(values, common_names, "truncation qualification stop")
    elif variant is CalculationWireEnum.TRUNCATION_COMPLETED:
        _fields(
            values,
            common_names
            | {
                "evaluation_coordinate_offset",
                "minimum_construction_evaluation_separation",
                "points",
            },
            "completed truncation",
        )
    else:
        raise ValueError("variant does not identify a truncation outcome")
    request = _truncation_request_from_mapping(_mapping_value(values, "request"))
    qualification = Periodic1DRank2QualificationRecord.from_dict(
        _mapping_value(values, "qualification")
    ).qualification
    if variant is CalculationWireEnum.TRUNCATION_QUALIFICATION_STOPPED:
        return Periodic1DRank2TruncationQualificationStopped(
            request=request,
            qualification=qualification,
        )
    if type(qualification) is not Periodic1DRank2QualifiedParent:
        raise TypeError("completed truncation requires a qualified parent")
    return Periodic1DRank2TruncationCompleted(
        request=request,
        qualification=qualification,
        evaluation_coordinate_offset=_floating(values, "evaluation_coordinate_offset"),
        minimum_construction_evaluation_separation=_floating(
            values, "minimum_construction_evaluation_separation"
        ),
        points=tuple(
            _truncation_point_from_mapping(item)
            for item in _mapping_tuple(values, "points")
        ),
    )


def _control_key(
    value: Periodic1DRank2Request,
) -> tuple[float, ...]:
    return (
        value.parent_hopping_scale,
        value.minimum_external_gap,
        value.minimum_transport_singular_value,
        value.frame_absolute_tolerance,
        value.transport_rank_relative_tolerance,
        value.transport_validation_relative_tolerance,
        value.harmonic_absolute_degeneracy_tolerance,
        value.harmonic_relative_degeneracy_tolerance,
    )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2AdaptiveAmplitudeAnalysisRecord(BaseTypedRecord):
    """Retain one closed adaptive-amplitude outcome with generic typed JSON."""

    analysis: Periodic1DRank2AdaptiveAmplitudeAnalysis

    def __post_init__(self) -> None:
        if type(self.analysis) not in (
            Periodic1DRank2AdaptiveAmplitudeQualificationStopped,
            Periodic1DRank2AdaptiveAmplitudeConverged,
            Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
            Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
        ):
            raise TypeError("analysis must be one closed adaptive outcome")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return _amplitude_mapping(self.analysis)

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        return cls(_amplitude_from_mapping(values))


@dataclass(frozen=True, slots=True)
class Periodic1DRank2MomentumRefinementFamilyAnalysisRecord(BaseTypedRecord):
    """Retain one complete parent-scale momentum-refinement family."""

    analysis: Periodic1DRank2MomentumRefinementFamilyAnalysis

    def __post_init__(self) -> None:
        if type(self.analysis) is not Periodic1DRank2MomentumRefinementFamilyAnalysis:
            raise TypeError("analysis must be a momentum-refinement family analysis")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parent_hopping_scales": (
                self.analysis.request.parent_family_request.parent_hopping_scales
            ),
            "members": tuple(
                _momentum_mapping(member) for member in self.analysis.members
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {"parent_hopping_scales", "members"},
            "momentum-refinement family record",
        )
        scales = _float_tuple(values, "parent_hopping_scales")
        members = tuple(
            _momentum_from_mapping(item) for item in _mapping_tuple(values, "members")
        )
        if len(scales) != len(members) or not members:
            raise ValueError("momentum family scales and members must align")
        if any(
            type(member)
            not in (
                Periodic1DRank2MomentumRefinementQualificationStopped,
                Periodic1DRank2MomentumRefinementConverged,
                Periodic1DRank2MomentumRefinementUnresolved,
            )
            for member in members
        ):
            raise TypeError("members must contain closed momentum outcomes")
        first_request = members[0].request
        parent_request = Periodic1DRank2ParentFamilyRequest(
            template_request=members[-1].request.template_request,
            parent_hopping_scales=scales,
        )
        request = Periodic1DRank2MomentumRefinementFamilyRequest(
            parent_family_request=parent_request,
            reciprocal_mesh_sizes=first_request.reciprocal_mesh_sizes,
            thresholds=first_request.thresholds,
            required_stable_refinements=first_request.required_stable_refinements,
        )
        return cls(
            Periodic1DRank2MomentumRefinementFamilyAnalysis(
                request=request,
                refinement_family=ReciprocalMeshRefinementFamily(
                    request=request.refinement_family_request,
                    members=tuple(
                        ReciprocalMeshRefinementFamilyMember(
                            family_coordinate=scale,
                            outcome=member,
                        )
                        for scale, member in zip(scales, members, strict=True)
                    ),
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2TruncationFamilyAnalysisRecord(BaseTypedRecord):
    """Retain one complete parent-scale support-truncation family."""

    analysis: Periodic1DRank2TruncationFamilyAnalysis

    def __post_init__(self) -> None:
        if type(self.analysis) is not Periodic1DRank2TruncationFamilyAnalysis:
            raise TypeError("analysis must be a truncation-family analysis")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parent_hopping_scales": (
                self.analysis.request.parent_family_request.parent_hopping_scales
            ),
            "support_tolerance": self.analysis.request.support_tolerance,
            "members": tuple(
                _truncation_mapping(member) for member in self.analysis.members
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
            Periodic1DRank2TruncationCompleted,
            Periodic1DRank2TruncationQualificationStopped,
        )

        _fields(
            values,
            {"parent_hopping_scales", "support_tolerance", "members"},
            "truncation family record",
        )
        scales = _float_tuple(values, "parent_hopping_scales")
        support_tolerance = _floating(values, "support_tolerance")
        members = tuple(
            _truncation_from_mapping(item) for item in _mapping_tuple(values, "members")
        )
        if len(scales) != len(members) or not members:
            raise ValueError("truncation family scales and members must align")
        if any(
            type(member)
            not in (
                Periodic1DRank2TruncationQualificationStopped,
                Periodic1DRank2TruncationCompleted,
            )
            for member in members
        ):
            raise TypeError("members must contain closed truncation outcomes")
        first_request = members[0].request
        parent_request = Periodic1DRank2ParentFamilyRequest(
            template_request=members[-1].request.template_request,
            parent_hopping_scales=scales,
        )
        request = Periodic1DRank2TruncationFamilyRequest(
            parent_family_request=parent_request,
            maximum_ranges=first_request.maximum_ranges,
            evaluation_mesh_size=first_request.evaluation_mesh_size,
            support_tolerance=support_tolerance,
        )
        return cls(
            Periodic1DRank2TruncationFamilyAnalysis(
                request=request,
                truncation_family=RealSpaceSupportTruncationFamily(
                    request=request.truncation_family_request,
                    members=tuple(
                        RealSpaceSupportTruncationFamilyMember(
                            family_coordinate=scale,
                            outcome=member,
                        )
                        for scale, member in zip(scales, members, strict=True)
                    ),
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2CalculationRecord(BaseTypedRecord):
    """Retain one cohesive family, refinement, and truncation calculation."""

    parent_family: Periodic1DRank2ParentFamilyAnalysis
    momentum_refinement: Periodic1DRank2MomentumRefinementAnalysis
    adaptive_amplitude: Periodic1DRank2AdaptiveAmplitudeAnalysis
    truncation: Periodic1DRank2SupportTruncationAnalysis

    def __post_init__(self) -> None:
        from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
            Periodic1DRank2SupportTruncationAnalysis,
        )

        if type(self.parent_family) is not (Periodic1DRank2ParentFamilyAnalysis):
            raise TypeError("parent_family must be a parent-family analysis")
        if not isinstance(
            self.momentum_refinement,
            Periodic1DRank2MomentumRefinementAnalysis,
        ):
            raise TypeError("momentum_refinement must be a closed analysis outcome")
        if not isinstance(
            self.adaptive_amplitude,
            Periodic1DRank2AdaptiveAmplitudeAnalysis,
        ):
            raise TypeError("adaptive_amplitude must be a closed analysis outcome")
        if not isinstance(
            self.truncation,
            Periodic1DRank2SupportTruncationAnalysis,
        ):
            raise TypeError("truncation must be a closed analysis outcome")
        requests = (
            self.parent_family.request.template_request,
            self.momentum_refinement.request.template_request,
            self.adaptive_amplitude.request.template_request,
            self.truncation.request.template_request,
        )
        if any(
            _control_key(item) != _control_key(requests[0]) for item in requests[1:]
        ):
            raise ValueError("aggregate components must share one scientific control")
        if requests[0].parent_hopping_scale != 1.0:
            raise ValueError("aggregate parent-family template must be the full parent")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parent_family": (
                Periodic1DRank2ParentFamilyAnalysisRecord(self.parent_family).to_dict()
            ),
            "momentum_refinement": _momentum_mapping(self.momentum_refinement),
            "adaptive_amplitude": _amplitude_mapping(self.adaptive_amplitude),
            "truncation": _truncation_mapping(self.truncation),
        }

    @classmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        _fields(
            values,
            {
                "parent_family",
                "momentum_refinement",
                "adaptive_amplitude",
                "truncation",
            },
            "embedded-subspace rank-two calculation record",
        )
        return cls(
            parent_family=(
                Periodic1DRank2ParentFamilyAnalysisRecord.from_dict(
                    _mapping_value(values, "parent_family")
                ).analysis
            ),
            momentum_refinement=_momentum_from_mapping(
                _mapping_value(values, "momentum_refinement")
            ),
            adaptive_amplitude=_amplitude_from_mapping(
                _mapping_value(values, "adaptive_amplitude")
            ),
            truncation=_truncation_from_mapping(_mapping_value(values, "truncation")),
        )


class Periodic1DRank2ParentFamilyAnalysisRecorder:
    """Project one bound family analysis into its retained wire owner."""

    __slots__ = ("_analysis",)

    def __init__(
        self,
        analysis: Periodic1DRank2ParentFamilyAnalysis,
    ) -> None:
        if type(analysis) is not (Periodic1DRank2ParentFamilyAnalysis):
            raise TypeError("analysis must be Periodic1DRank2ParentFamilyAnalysis")
        self._analysis = analysis

    def result(
        self,
    ) -> Periodic1DRank2ParentFamilyAnalysisRecord:
        """Return the retained projection without rerunning its producer."""
        return Periodic1DRank2ParentFamilyAnalysisRecord(self._analysis)


class Periodic1DRank2AnalysisRecorder:
    """Project one bound analysis into its retained wire owner."""

    __slots__ = ("_analysis",)

    def __init__(self, analysis: Periodic1DRank2Analysis) -> None:
        if type(analysis) is not Periodic1DRank2Analysis:
            raise TypeError("analysis must be Periodic1DRank2Analysis")
        self._analysis = analysis

    def result(self) -> Periodic1DRank2AnalysisRecord:
        """Return the retained projection without rerunning its producer."""
        return Periodic1DRank2AnalysisRecord(self._analysis)


__all__ = [
    "CalculationWireEnum",
    "Periodic1DRank2AdaptiveAmplitudeAnalysisRecord",
    "Periodic1DRank2AnalysisRecord",
    "Periodic1DRank2CalculationRecord",
    "Periodic1DRank2AnalysisRecorder",
    "Periodic1DRank2HarmonicMaximumRecord",
    "Periodic1DRank2HoppingPowerRecord",
    "Periodic1DRank2MomentumRefinementFamilyAnalysisRecord",
    "Periodic1DRank2ParentFamilyAnalysisRecord",
    "Periodic1DRank2ParentFamilyAnalysisRecorder",
    "Periodic1DRank2PointAnalysisRecord",
    "Periodic1DRank2QualificationRecord",
    "Periodic1DRank2TruncationFamilyAnalysisRecord",
]
