"""Canonical artifacts and semantic read-back checks for finite strain scans."""

from __future__ import annotations

import json
import platform
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TypedDict, cast

import numpy as np

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainPath,
    SyntheticStrainResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainResponseModel,
    StrainWitnessControl,
    SyntheticStrainResponseResult,
    SyntheticStrainWitnessScanResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan import (  # noqa: E501
    SampledStrainMaximum,
    SampledStrainMinimum,
    StrainApproximationEnvelope,
    StrainBondDegeneracyTransitionBracket,
    StrainCutoffApproximationEnvelope,
    StrainErrorChannelEnvelope,
    StrainLocalityEnvelope,
    StrainQualificationEnvelope,
    StrainResponseEnvelope,
    StrainResponseMechanismEnvelope,
    StrainShellTransitionBracket,
    StrainWitnessRequirementEnvelope,
    SyntheticStrainScanAssessor,
    SyntheticStrainScanRequest,
    SyntheticStrainScanSummary,
    SyntheticStrainTransitionRefinementResult,
    SyntheticStrainTransitionRefiner,
)

from .serialization import CanonicalJsonDocument
from .strain_serialization import (
    SyntheticStrainResponseResultSerializer,
    SyntheticStrainResultSerializer,
    SyntheticStrainWitnessResultSerializer,
    deserialize_synthetic_strain_response_result,
    deserialize_synthetic_strain_result,
    deserialize_synthetic_strain_witness_result,
)

SCAN_REQUEST_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy."
    "gauge-locality-under-synthetic-strain.scan.request.v1"
)
SCAN_RESULT_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy."
    "gauge-locality-under-synthetic-strain.scan.result.v1"
)
SCAN_VERIFICATION_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy."
    "gauge-locality-under-synthetic-strain.scan.verification.v1"
)


class _EnvironmentWire(TypedDict):
    ksdft2effmass: str
    numpy: str
    platform: str
    projectkoios_optimization: str
    projectkoios_physkit: str
    python: str


class _RequestWire(TypedDict):
    environment: _EnvironmentWire
    geometry_construction_size: int
    maximum_rotation_amplitude: float
    maximum_transition_refinement_depth: int
    path: str
    radial_decay_beta: float
    response_construction_size: int
    response_evaluation_shift: float
    response_evaluation_size: int
    schema: str
    status: str
    strain_fractions: list[float]
    tail_tolerances: list[float]
    witness_construction_size: int


class _SampledExtremeWire(TypedDict):
    strain_fraction: float
    value: float


class _WitnessEnvelopeWire(TypedDict):
    control: str
    fixed_candidate_maximum: float
    fixed_candidate_maximum_strain_fraction: float
    maximum_correlation: float
    maximum_correlation_strain_fraction: float
    maximum_splitting_scale: float
    maximum_splitting_scale_strain_fraction: float
    minimum_correlation: float
    minimum_correlation_strain_fraction: float
    minimum_splitting_scale: float
    minimum_splitting_scale_strain_fraction: float
    optimized_maximum: float
    optimized_maximum_strain_fraction: float


class _LocalityEnvelopeWire(TypedDict):
    maximum_physical_radius: float | None
    maximum_physical_radius_strain_fraction: float | None
    maximum_retained_blocks: int | None
    maximum_retained_blocks_strain_fraction: float | None
    tail_tolerance: float


class _ResponseEnvelopeWire(TypedDict):
    control: str
    maximum_aligned_hamiltonian_defect: float
    maximum_strain_fraction: float


class _QualificationEnvelopeWire(TypedDict):
    control: str
    external_isolation_gap: _SampledExtremeWire
    frame_overlap_singular_value: _SampledExtremeWire
    pointwise_frame_alignment_residual: _SampledExtremeWire
    restricted_global_frame_alignment_residual: _SampledExtremeWire
    seed_overlap: _SampledExtremeWire


class _ErrorEnvelopeWire(TypedDict):
    maximum_band: _SampledExtremeWire
    maximum_hamiltonian: _SampledExtremeWire
    rms_band: _SampledExtremeWire
    rms_hamiltonian: _SampledExtremeWire
    sample_count: int


class _CutoffEnvelopeWire(TypedDict):
    delta_omitted_power: _SampledExtremeWire
    delta_total: _ErrorEnvelopeWire | None
    delta_truncation: _ErrorEnvelopeWire | None
    omitted_power: _SampledExtremeWire
    tail_tolerance: float
    total: _ErrorEnvelopeWire | None
    truncation: _ErrorEnvelopeWire | None


class _ApproximationEnvelopeWire(TypedDict):
    aligned_strain_perturbation: _ErrorEnvelopeWire
    control: str
    cutoffs: list[_CutoffEnvelopeWire]
    delta_interpolation: _ErrorEnvelopeWire
    delta_nyquist_power: _SampledExtremeWire
    interpolation: _ErrorEnvelopeWire
    nyquist_power: _SampledExtremeWire


class _MechanismEnvelopeWire(TypedDict):
    control: str
    delta_offsite_power_maximum: _SampledExtremeWire
    delta_onsite_power_maximum: _SampledExtremeWire
    hopping_response_maximum: _SampledExtremeWire
    hopping_response_minimum: _SampledExtremeWire
    scalar_component_maximum: _SampledExtremeWire
    scalar_component_rms_maximum: _SampledExtremeWire
    traceless_component_maximum: _SampledExtremeWire
    traceless_component_rms_maximum: _SampledExtremeWire


class _SummaryWire(TypedDict):
    approximations: list[_ApproximationEnvelopeWire]
    base_sample_count: int
    locality: list[_LocalityEnvelopeWire]
    maximum_direct_band_defect: float
    maximum_direct_band_defect_strain_fraction: float
    maximum_volume_defect: float
    maximum_volume_defect_strain_fraction: float
    mechanisms: list[_MechanismEnvelopeWire]
    qualifications: list[_QualificationEnvelopeWire]
    responses: list[_ResponseEnvelopeWire]
    status: str
    witness_requirements: list[_WitnessEnvelopeWire]


class _ShellTransitionWire(TypedDict):
    left_retained_blocks: int | None
    left_strain_fraction: float
    right_retained_blocks: int | None
    right_strain_fraction: float
    tail_tolerance: float


class _BondTransitionWire(TypedDict):
    left_distinct_bond_lengths: int
    left_strain_fraction: float
    right_distinct_bond_lengths: int
    right_strain_fraction: float


class _TransitionsWire(TypedDict):
    base_sample_count: int
    bond_degeneracy_transitions: list[_BondTransitionWire]
    maximum_final_bracket_width: float
    maximum_refinement_depth: int
    shell_transitions: list[_ShellTransitionWire]
    status: str


class _WitnessDigestWire(TypedDict):
    control: str
    sha256: str


class _SourceDigestsWire(TypedDict):
    frozen_response_sha256: str
    geometry_sha256: str
    radial_response_sha256: str
    witnesses: list[_WitnessDigestWire]


class _ResultWire(TypedDict):
    path: str
    scan_request_sha256: str
    schema: str
    source_sha256: _SourceDigestsWire
    status: str
    summary: _SummaryWire
    transitions: _TransitionsWire


class _VerificationWire(TypedDict):
    passes: bool
    scan_request_sha256: str
    scan_result_sha256: str
    schema: str
    source_sha256: _SourceDigestsWire
    status: str


type _ScanWire = _RequestWire | _ResultWire | _VerificationWire


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanEnvironment:
    """Record local software identifiers without claiming reproducibility."""

    python: str
    platform: str
    numpy: str
    ksdft2effmass: str
    projectkoios_optimization: str
    projectkoios_physkit: str

    @classmethod
    def capture(cls) -> SyntheticStrainScanEnvironment:
        """Capture the current finite-scan software environment."""
        return cls(
            python=platform.python_version(),
            platform=platform.platform(),
            numpy=np.__version__,
            ksdft2effmass=_package_version("ksdft2effmass"),
            projectkoios_optimization=_package_version("projectkoios-optimization"),
            projectkoios_physkit=_package_version("projectkoios-physkit"),
        )


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanArtifactPaths:
    """Identify every source and derived document in one scan artifact set."""

    request_path: Path
    geometry_path: Path
    witness_paths: tuple[Path, ...]
    frozen_response_path: Path
    radial_response_path: Path
    result_path: Path
    verification_path: Path


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanArtifactResult:
    """Report the paths and identities of a verified finite-scan artifact set."""

    paths: SyntheticStrainScanArtifactPaths
    scan_request_sha256: str
    scan_result_sha256: str
    source_sha256: tuple[str, ...]


def _package_version(distribution: str) -> str:
    try:
        return version(distribution)
    except PackageNotFoundError:
        return "not-installed"


def _canonical_document(value: _ScanWire) -> CanonicalJsonDocument:
    return CanonicalJsonDocument(
        (
            json.dumps(value, allow_nan=False, separators=(",", ":"), sort_keys=True)
            + "\n"
        ).encode("utf-8")
    )


def _environment_wire(value: SyntheticStrainScanEnvironment) -> _EnvironmentWire:
    return {
        "ksdft2effmass": value.ksdft2effmass,
        "numpy": value.numpy,
        "platform": value.platform,
        "projectkoios_optimization": value.projectkoios_optimization,
        "projectkoios_physkit": value.projectkoios_physkit,
        "python": value.python,
    }


def _maximum_wire(value: SampledStrainMaximum) -> _SampledExtremeWire:
    return {"strain_fraction": value.strain_fraction, "value": value.value}


def _minimum_wire(value: SampledStrainMinimum) -> _SampledExtremeWire:
    return {"strain_fraction": value.strain_fraction, "value": value.value}


def _error_envelope_wire(value: StrainErrorChannelEnvelope) -> _ErrorEnvelopeWire:
    return {
        "maximum_band": _maximum_wire(value.maximum_band),
        "maximum_hamiltonian": _maximum_wire(value.maximum_hamiltonian),
        "rms_band": _maximum_wire(value.rms_band),
        "rms_hamiltonian": _maximum_wire(value.rms_hamiltonian),
        "sample_count": value.sample_count,
    }


def _optional_error_envelope_wire(
    value: StrainErrorChannelEnvelope | None,
) -> _ErrorEnvelopeWire | None:
    return None if value is None else _error_envelope_wire(value)


def _witness_envelope_wire(
    value: StrainWitnessRequirementEnvelope,
) -> _WitnessEnvelopeWire:
    return {
        "control": value.control.value,
        "fixed_candidate_maximum": value.fixed_candidate_maximum,
        "fixed_candidate_maximum_strain_fraction": (
            value.fixed_candidate_maximum_strain_fraction
        ),
        "maximum_correlation": value.maximum_correlation,
        "maximum_correlation_strain_fraction": (
            value.maximum_correlation_strain_fraction
        ),
        "maximum_splitting_scale": value.maximum_splitting_scale,
        "maximum_splitting_scale_strain_fraction": (
            value.maximum_splitting_scale_strain_fraction
        ),
        "minimum_correlation": value.minimum_correlation,
        "minimum_correlation_strain_fraction": (
            value.minimum_correlation_strain_fraction
        ),
        "minimum_splitting_scale": value.minimum_splitting_scale,
        "minimum_splitting_scale_strain_fraction": (
            value.minimum_splitting_scale_strain_fraction
        ),
        "optimized_maximum": value.optimized_maximum,
        "optimized_maximum_strain_fraction": (
            value.optimized_maximum_strain_fraction
        ),
    }


def _locality_envelope_wire(value: StrainLocalityEnvelope) -> _LocalityEnvelopeWire:
    return {
        "maximum_physical_radius": value.maximum_physical_radius,
        "maximum_physical_radius_strain_fraction": (
            value.maximum_physical_radius_strain_fraction
        ),
        "maximum_retained_blocks": value.maximum_retained_blocks,
        "maximum_retained_blocks_strain_fraction": (
            value.maximum_retained_blocks_strain_fraction
        ),
        "tail_tolerance": value.tail_tolerance,
    }


def _response_envelope_wire(value: StrainResponseEnvelope) -> _ResponseEnvelopeWire:
    return {
        "control": value.control.value,
        "maximum_aligned_hamiltonian_defect": (
            value.maximum_aligned_hamiltonian_defect
        ),
        "maximum_strain_fraction": value.maximum_strain_fraction,
    }


def _qualification_envelope_wire(
    value: StrainQualificationEnvelope,
) -> _QualificationEnvelopeWire:
    return {
        "control": value.control.value,
        "external_isolation_gap": _minimum_wire(value.external_isolation_gap),
        "frame_overlap_singular_value": _minimum_wire(
            value.frame_overlap_singular_value
        ),
        "pointwise_frame_alignment_residual": _maximum_wire(
            value.pointwise_frame_alignment_residual
        ),
        "restricted_global_frame_alignment_residual": _maximum_wire(
            value.restricted_global_frame_alignment_residual
        ),
        "seed_overlap": _minimum_wire(value.seed_overlap),
    }


def _cutoff_envelope_wire(
    value: StrainCutoffApproximationEnvelope,
) -> _CutoffEnvelopeWire:
    return {
        "delta_omitted_power": _maximum_wire(value.delta_omitted_power),
        "delta_total": _optional_error_envelope_wire(value.delta_total),
        "delta_truncation": _optional_error_envelope_wire(value.delta_truncation),
        "omitted_power": _maximum_wire(value.omitted_power),
        "tail_tolerance": value.tail_tolerance,
        "total": _optional_error_envelope_wire(value.total),
        "truncation": _optional_error_envelope_wire(value.truncation),
    }


def _approximation_envelope_wire(
    value: StrainApproximationEnvelope,
) -> _ApproximationEnvelopeWire:
    return {
        "aligned_strain_perturbation": _error_envelope_wire(
            value.aligned_strain_perturbation
        ),
        "control": value.control.value,
        "cutoffs": [_cutoff_envelope_wire(item) for item in value.cutoffs],
        "delta_interpolation": _error_envelope_wire(value.delta_interpolation),
        "delta_nyquist_power": _maximum_wire(value.delta_nyquist_power),
        "interpolation": _error_envelope_wire(value.interpolation),
        "nyquist_power": _maximum_wire(value.nyquist_power),
    }


def _mechanism_envelope_wire(
    value: StrainResponseMechanismEnvelope,
) -> _MechanismEnvelopeWire:
    return {
        "control": value.control.value,
        "delta_offsite_power_maximum": _maximum_wire(
            value.delta_offsite_power_maximum
        ),
        "delta_onsite_power_maximum": _maximum_wire(
            value.delta_onsite_power_maximum
        ),
        "hopping_response_maximum": _maximum_wire(value.hopping_response_maximum),
        "hopping_response_minimum": _minimum_wire(value.hopping_response_minimum),
        "scalar_component_maximum": _maximum_wire(value.scalar_component_maximum),
        "scalar_component_rms_maximum": _maximum_wire(
            value.scalar_component_rms_maximum
        ),
        "traceless_component_maximum": _maximum_wire(
            value.traceless_component_maximum
        ),
        "traceless_component_rms_maximum": _maximum_wire(
            value.traceless_component_rms_maximum
        ),
    }


def _summary_wire(value: SyntheticStrainScanSummary) -> _SummaryWire:
    return {
        "approximations": [
            _approximation_envelope_wire(item) for item in value.approximations
        ],
        "base_sample_count": value.base_sample_count,
        "locality": [_locality_envelope_wire(item) for item in value.locality],
        "maximum_direct_band_defect": value.maximum_direct_band_defect,
        "maximum_direct_band_defect_strain_fraction": (
            value.maximum_direct_band_defect_strain_fraction
        ),
        "maximum_volume_defect": value.maximum_volume_defect,
        "maximum_volume_defect_strain_fraction": (
            value.maximum_volume_defect_strain_fraction
        ),
        "mechanisms": [
            _mechanism_envelope_wire(item) for item in value.mechanisms
        ],
        "qualifications": [
            _qualification_envelope_wire(item) for item in value.qualifications
        ],
        "responses": [_response_envelope_wire(item) for item in value.responses],
        "status": value.status,
        "witness_requirements": [
            _witness_envelope_wire(item) for item in value.witness_requirements
        ],
    }


def _shell_transition_wire(
    value: StrainShellTransitionBracket,
) -> _ShellTransitionWire:
    return {
        "left_retained_blocks": value.left_retained_blocks,
        "left_strain_fraction": value.left_strain_fraction,
        "right_retained_blocks": value.right_retained_blocks,
        "right_strain_fraction": value.right_strain_fraction,
        "tail_tolerance": value.tail_tolerance,
    }


def _bond_transition_wire(
    value: StrainBondDegeneracyTransitionBracket,
) -> _BondTransitionWire:
    return {
        "left_distinct_bond_lengths": value.left_distinct_bond_lengths,
        "left_strain_fraction": value.left_strain_fraction,
        "right_distinct_bond_lengths": value.right_distinct_bond_lengths,
        "right_strain_fraction": value.right_strain_fraction,
    }


def _transitions_wire(
    value: SyntheticStrainTransitionRefinementResult,
) -> _TransitionsWire:
    return {
        "base_sample_count": value.base_sample_count,
        "bond_degeneracy_transitions": [
            _bond_transition_wire(item) for item in value.bond_degeneracy_transitions
        ],
        "maximum_final_bracket_width": value.maximum_final_bracket_width,
        "maximum_refinement_depth": value.maximum_refinement_depth,
        "shell_transitions": [
            _shell_transition_wire(item) for item in value.shell_transitions
        ],
        "status": value.status,
    }


def _source_digests_wire(
    geometry: CanonicalJsonDocument,
    witnesses: tuple[tuple[StrainWitnessControl, CanonicalJsonDocument], ...],
    frozen: CanonicalJsonDocument,
    radial: CanonicalJsonDocument,
) -> _SourceDigestsWire:
    return {
        "frozen_response_sha256": frozen.content_sha256(),
        "geometry_sha256": geometry.content_sha256(),
        "radial_response_sha256": radial.content_sha256(),
        "witnesses": [
            {"control": control.value, "sha256": document.content_sha256()}
            for control, document in witnesses
        ],
    }


def _request_from_wire(value: _RequestWire) -> SyntheticStrainScanRequest:
    if value["schema"] != SCAN_REQUEST_SCHEMA_ID:
        raise ValueError("document is not a synthetic-strain scan request")
    return SyntheticStrainScanRequest(
        path=SyntheticStrainPath(value["path"]),
        strain_fractions=tuple(value["strain_fractions"]),
        geometry_construction_size=value["geometry_construction_size"],
        witness_construction_size=value["witness_construction_size"],
        response_construction_size=value["response_construction_size"],
        response_evaluation_size=value["response_evaluation_size"],
        response_evaluation_shift=value["response_evaluation_shift"],
        maximum_rotation_amplitude=value["maximum_rotation_amplitude"],
        radial_decay_beta=value["radial_decay_beta"],
        tail_tolerances=tuple(value["tail_tolerances"]),
        maximum_transition_refinement_depth=(
            value["maximum_transition_refinement_depth"]
        ),
    )


def _assert_sources_match_request(
    request: SyntheticStrainScanRequest,
    geometry: SyntheticStrainResult,
    witnesses: tuple[SyntheticStrainWitnessScanResult, ...],
    frozen: SyntheticStrainResponseResult,
    radial: SyntheticStrainResponseResult,
) -> None:
    fractions = request.strain_fractions
    if (
        geometry.path is not request.path
        or geometry.construction_size != request.geometry_construction_size
        or geometry.maximum_rotation_amplitude != request.maximum_rotation_amplitude
        or geometry.tail_tolerances != request.tail_tolerances
        or tuple(point.strain_fraction for point in geometry.points) != fractions
    ):
        raise ValueError("geometry source does not match the scan request")
    if len(witnesses) != len(StrainWitnessControl) or {
        result.control for result in witnesses
    } != set(StrainWitnessControl):
        raise ValueError("witness sources must contain each control exactly once")
    for result in witnesses:
        expected_beta = (
            request.radial_decay_beta
            if result.control is StrainWitnessControl.RADIAL_RESPONSE
            else 0.0
        )
        if (
            result.path is not request.path
            or result.construction_size != request.witness_construction_size
            or result.maximum_rotation_amplitude
            != request.maximum_rotation_amplitude
            or result.radial_decay_beta != expected_beta
            or tuple(point.strain_fraction for point in result.points) != fractions
        ):
            raise ValueError("witness source does not match the scan request")
    for response_result, model, beta in (
        (frozen, StrainResponseModel.M1_FROZEN, 0.0),
        (radial, StrainResponseModel.M2_RADIAL, request.radial_decay_beta),
    ):
        if (
            response_result.path is not request.path
            or response_result.model is not model
            or response_result.construction_size
            != request.response_construction_size
            or response_result.evaluation_size != request.response_evaluation_size
            or response_result.evaluation_shift != request.response_evaluation_shift
            or response_result.maximum_rotation_amplitude
            != request.maximum_rotation_amplitude
            or response_result.radial_decay_beta != beta
            or response_result.tail_tolerances != request.tail_tolerances
            or tuple(
                point.strain_fraction for point in response_result.points
            )
            != fractions
        ):
            raise ValueError("response source does not match the scan request")


class SyntheticStrainScanRequestSerializer:
    """Serialize one complete finite strain-scan request."""

    __slots__ = ()

    def execute(
        self,
        request: SyntheticStrainScanRequest,
        environment: SyntheticStrainScanEnvironment,
    ) -> CanonicalJsonDocument:
        """Return canonical request bytes without filesystem side effects."""
        if type(request) is not SyntheticStrainScanRequest:
            raise TypeError("request must be SyntheticStrainScanRequest")
        if type(environment) is not SyntheticStrainScanEnvironment:
            raise TypeError("environment must be SyntheticStrainScanEnvironment")
        return _canonical_document(
            _RequestWire(
                environment=_environment_wire(environment),
                geometry_construction_size=request.geometry_construction_size,
                maximum_rotation_amplitude=request.maximum_rotation_amplitude,
                maximum_transition_refinement_depth=(
                    request.maximum_transition_refinement_depth
                ),
                path=request.path.value,
                radial_decay_beta=request.radial_decay_beta,
                response_construction_size=request.response_construction_size,
                response_evaluation_shift=request.response_evaluation_shift,
                response_evaluation_size=request.response_evaluation_size,
                schema=SCAN_REQUEST_SCHEMA_ID,
                status="finite-sampled-strain-scan-request",
                strain_fractions=list(request.strain_fractions),
                tail_tolerances=list(request.tail_tolerances),
                witness_construction_size=request.witness_construction_size,
            )
        )


class SyntheticStrainScanResultSerializer:
    """Serialize derived envelopes and transition brackets with source binding."""

    __slots__ = ()

    def execute(
        self,
        path: SyntheticStrainPath,
        summary: SyntheticStrainScanSummary,
        transitions: SyntheticStrainTransitionRefinementResult,
        scan_request: CanonicalJsonDocument,
        geometry: CanonicalJsonDocument,
        witnesses: tuple[tuple[StrainWitnessControl, CanonicalJsonDocument], ...],
        frozen: CanonicalJsonDocument,
        radial: CanonicalJsonDocument,
    ) -> CanonicalJsonDocument:
        """Return canonical derived-result bytes without filesystem side effects."""
        if type(path) is not SyntheticStrainPath:
            raise TypeError("path must be SyntheticStrainPath")
        if type(summary) is not SyntheticStrainScanSummary:
            raise TypeError("summary must be SyntheticStrainScanSummary")
        if type(transitions) is not SyntheticStrainTransitionRefinementResult:
            raise TypeError(
                "transitions must be SyntheticStrainTransitionRefinementResult"
            )
        for name, document in (
            ("scan_request", scan_request),
            ("geometry", geometry),
            ("frozen", frozen),
            ("radial", radial),
        ):
            if type(document) is not CanonicalJsonDocument:
                raise TypeError(f"{name} must be CanonicalJsonDocument")
        if type(witnesses) is not tuple or any(
            type(item) is not tuple
            or len(item) != 2
            or type(item[0]) is not StrainWitnessControl
            or type(item[1]) is not CanonicalJsonDocument
            for item in witnesses
        ):
            raise TypeError(
                "witnesses must pair StrainWitnessControl with CanonicalJsonDocument"
            )
        return _canonical_document(
            _ResultWire(
                path=path.value,
                scan_request_sha256=scan_request.content_sha256(),
                schema=SCAN_RESULT_SCHEMA_ID,
                source_sha256=_source_digests_wire(
                    geometry, witnesses, frozen, radial
                ),
                status="sampled-strain-scan-result-not-continuum-certificate",
                summary=_summary_wire(summary),
                transitions=_transitions_wire(transitions),
            )
        )


class SyntheticStrainScanArtifactVerifier:
    """Re-read source artifacts and recompute all derived scan records."""

    __slots__ = ()

    def execute(
        self, paths: SyntheticStrainScanArtifactPaths
    ) -> CanonicalJsonDocument:
        """Validate identities and semantic reconstruction, then write verification."""
        if type(paths) is not SyntheticStrainScanArtifactPaths:
            raise TypeError("paths must be SyntheticStrainScanArtifactPaths")
        from .strain_scan_schemas import (
            SyntheticStrainScanSchema,
            SyntheticStrainScanSchemaKind,
        )
        from .strain_schemas import SyntheticStrainSchema, SyntheticStrainSchemaKind

        request_document = CanonicalJsonDocument(paths.request_path.read_bytes())
        geometry_document = CanonicalJsonDocument(paths.geometry_path.read_bytes())
        witness_documents = tuple(
            CanonicalJsonDocument(path.read_bytes()) for path in paths.witness_paths
        )
        frozen_document = CanonicalJsonDocument(
            paths.frozen_response_path.read_bytes()
        )
        radial_document = CanonicalJsonDocument(
            paths.radial_response_path.read_bytes()
        )
        result_document = CanonicalJsonDocument(paths.result_path.read_bytes())

        SyntheticStrainScanSchema(SyntheticStrainScanSchemaKind.REQUEST).validate(
            request_document.canonical_bytes()
        )
        SyntheticStrainSchema(SyntheticStrainSchemaKind.M0_RESULT).validate(
            geometry_document.canonical_bytes()
        )
        witness_schema = SyntheticStrainSchema(
            SyntheticStrainSchemaKind.WITNESS_RESULT
        )
        for document in witness_documents:
            witness_schema.validate(document.canonical_bytes())
        SyntheticStrainSchema(SyntheticStrainSchemaKind.M1_RESULT).validate(
            frozen_document.canonical_bytes()
        )
        SyntheticStrainSchema(SyntheticStrainSchemaKind.M2_RESULT).validate(
            radial_document.canonical_bytes()
        )
        SyntheticStrainScanSchema(SyntheticStrainScanSchemaKind.RESULT).validate(
            result_document.canonical_bytes()
        )

        request_wire = cast(
            _RequestWire, json.loads(request_document.canonical_bytes())
        )
        request = _request_from_wire(request_wire)
        geometry = deserialize_synthetic_strain_result(geometry_document)
        witnesses = tuple(
            deserialize_synthetic_strain_witness_result(document)
            for document in witness_documents
        )
        frozen = deserialize_synthetic_strain_response_result(frozen_document)
        radial = deserialize_synthetic_strain_response_result(radial_document)
        ordered_witnesses = tuple(
            sorted(witnesses, key=lambda item: item.control.value)
        )
        ordered_witness_documents = tuple(
            sorted(
                zip(
                    (item.control for item in witnesses),
                    witness_documents,
                    strict=True,
                ),
                key=lambda item: item[0].value,
            )
        )
        _assert_sources_match_request(
            request, geometry, ordered_witnesses, frozen, radial
        )

        summary = SyntheticStrainScanAssessor().execute(
            geometry, ordered_witnesses, frozen, radial
        )
        transitions = SyntheticStrainTransitionRefiner().execute(
            geometry, request.maximum_transition_refinement_depth
        )
        expected_result = SyntheticStrainScanResultSerializer().execute(
            request.path,
            summary,
            transitions,
            request_document,
            geometry_document,
            ordered_witness_documents,
            frozen_document,
            radial_document,
        )
        if result_document.canonical_bytes() != expected_result.canonical_bytes():
            raise ValueError(
                "synthetic-strain scan result fails source-bound semantic read-back"
            )

        source_sha256 = _source_digests_wire(
            geometry_document,
            ordered_witness_documents,
            frozen_document,
            radial_document,
        )
        verification = _canonical_document(
            _VerificationWire(
                passes=True,
                scan_request_sha256=request_document.content_sha256(),
                scan_result_sha256=result_document.content_sha256(),
                schema=SCAN_VERIFICATION_SCHEMA_ID,
                source_sha256=source_sha256,
                status="canonical-read-back-and-semantic-reconstruction-passed",
            )
        )
        schema = SyntheticStrainScanSchema(
            SyntheticStrainScanSchemaKind.VERIFICATION
        )
        schema.validate(verification.canonical_bytes())
        verification.write_to(paths.verification_path)
        reread = CanonicalJsonDocument(paths.verification_path.read_bytes())
        schema.validate(reread.canonical_bytes())
        if reread.canonical_bytes() != verification.canonical_bytes():
            raise ValueError("strain-scan verification changed during read-back")
        return reread


class SyntheticStrainScanArtifactWriter:
    """Write and independently verify one complete finite strain-scan artifact set."""

    __slots__ = ()

    def execute(
        self,
        request: SyntheticStrainScanRequest,
        summary: SyntheticStrainScanSummary,
        transitions: SyntheticStrainTransitionRefinementResult,
        geometry: SyntheticStrainResult,
        witnesses: tuple[SyntheticStrainWitnessScanResult, ...],
        frozen: SyntheticStrainResponseResult,
        radial: SyntheticStrainResponseResult,
        output_directory: Path,
        environment: SyntheticStrainScanEnvironment,
    ) -> SyntheticStrainScanArtifactResult:
        """Write canonical sources and derived records, then verify their read-back."""
        if type(request) is not SyntheticStrainScanRequest:
            raise TypeError("request must be SyntheticStrainScanRequest")
        if type(geometry) is not SyntheticStrainResult:
            raise TypeError("geometry must be SyntheticStrainResult")
        if type(witnesses) is not tuple or any(
            type(item) is not SyntheticStrainWitnessScanResult for item in witnesses
        ):
            raise TypeError(
                "witnesses must be a tuple of SyntheticStrainWitnessScanResult"
            )
        if type(frozen) is not SyntheticStrainResponseResult:
            raise TypeError("frozen must be SyntheticStrainResponseResult")
        if type(radial) is not SyntheticStrainResponseResult:
            raise TypeError("radial must be SyntheticStrainResponseResult")
        if type(environment) is not SyntheticStrainScanEnvironment:
            raise TypeError("environment must be SyntheticStrainScanEnvironment")
        if not isinstance(output_directory, Path):
            raise TypeError("output_directory must be pathlib.Path")
        if type(summary) is not SyntheticStrainScanSummary:
            raise TypeError("summary must be SyntheticStrainScanSummary")
        if type(transitions) is not SyntheticStrainTransitionRefinementResult:
            raise TypeError(
                "transitions must be SyntheticStrainTransitionRefinementResult"
            )
        _assert_sources_match_request(request, geometry, witnesses, frozen, radial)
        from .strain_scan_schemas import (
            SyntheticStrainScanSchema,
            SyntheticStrainScanSchemaKind,
        )
        from .strain_schemas import SyntheticStrainSchema, SyntheticStrainSchemaKind

        output_directory.mkdir(parents=True, exist_ok=True)
        slug = (
            "rhombic-2d"
            if request.path is SyntheticStrainPath.RHOMBIC_2D
            else "bain-3d"
        )
        request_document = SyntheticStrainScanRequestSerializer().execute(
            request, environment
        )
        geometry_document = SyntheticStrainResultSerializer().execute(geometry)
        ordered_witnesses = tuple(
            sorted(witnesses, key=lambda item: item.control.value)
        )
        witness_documents = tuple(
            (item.control, SyntheticStrainWitnessResultSerializer().execute(item))
            for item in ordered_witnesses
        )
        frozen_document = SyntheticStrainResponseResultSerializer().execute(frozen)
        radial_document = SyntheticStrainResponseResultSerializer().execute(radial)
        result_document = SyntheticStrainScanResultSerializer().execute(
            request.path,
            summary,
            transitions,
            request_document,
            geometry_document,
            witness_documents,
            frozen_document,
            radial_document,
        )

        SyntheticStrainScanSchema(SyntheticStrainScanSchemaKind.REQUEST).validate(
            request_document.canonical_bytes()
        )
        SyntheticStrainScanSchema(SyntheticStrainScanSchemaKind.RESULT).validate(
            result_document.canonical_bytes()
        )
        SyntheticStrainSchema(SyntheticStrainSchemaKind.M0_RESULT).validate(
            geometry_document.canonical_bytes()
        )
        witness_schema = SyntheticStrainSchema(
            SyntheticStrainSchemaKind.WITNESS_RESULT
        )
        for _, document in witness_documents:
            witness_schema.validate(document.canonical_bytes())
        SyntheticStrainSchema(SyntheticStrainSchemaKind.M1_RESULT).validate(
            frozen_document.canonical_bytes()
        )
        SyntheticStrainSchema(SyntheticStrainSchemaKind.M2_RESULT).validate(
            radial_document.canonical_bytes()
        )

        request_path = output_directory / f"{slug}-strain-scan-request.json"
        geometry_path = output_directory / f"{slug}-geometry-source.json"
        witness_paths = tuple(
            output_directory
            / f"{slug}-{control.name.lower().replace('_', '-')}-witness-source.json"
            for control, _ in witness_documents
        )
        frozen_path = output_directory / f"{slug}-frozen-response-source.json"
        radial_path = output_directory / f"{slug}-radial-response-source.json"
        result_path = output_directory / f"{slug}-strain-scan-result.json"
        verification_path = output_directory / f"{slug}-strain-scan-verification.json"
        request_document.write_to(request_path)
        geometry_document.write_to(geometry_path)
        for path, (_, document) in zip(
            witness_paths, witness_documents, strict=True
        ):
            document.write_to(path)
        frozen_document.write_to(frozen_path)
        radial_document.write_to(radial_path)
        result_document.write_to(result_path)
        paths = SyntheticStrainScanArtifactPaths(
            request_path=request_path,
            geometry_path=geometry_path,
            witness_paths=witness_paths,
            frozen_response_path=frozen_path,
            radial_response_path=radial_path,
            result_path=result_path,
            verification_path=verification_path,
        )
        SyntheticStrainScanArtifactVerifier().execute(paths)
        return SyntheticStrainScanArtifactResult(
            paths=paths,
            scan_request_sha256=request_document.content_sha256(),
            scan_result_sha256=result_document.content_sha256(),
            source_sha256=(
                geometry_document.content_sha256(),
                *(document.content_sha256() for _, document in witness_documents),
                frozen_document.content_sha256(),
                radial_document.content_sha256(),
            ),
        )


__all__ = [
    "SCAN_REQUEST_SCHEMA_ID",
    "SCAN_RESULT_SCHEMA_ID",
    "SCAN_VERIFICATION_SCHEMA_ID",
    "SyntheticStrainScanArtifactPaths",
    "SyntheticStrainScanArtifactResult",
    "SyntheticStrainScanArtifactVerifier",
    "SyntheticStrainScanArtifactWriter",
    "SyntheticStrainScanEnvironment",
    "SyntheticStrainScanRequestSerializer",
    "SyntheticStrainScanResultSerializer",
]
