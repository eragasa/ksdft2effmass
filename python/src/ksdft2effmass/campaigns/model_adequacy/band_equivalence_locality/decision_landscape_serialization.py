"""Canonical artifacts and read-back verification for shell--scale landscapes."""

from __future__ import annotations

import json
import platform
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TypedDict, cast

import numpy as np

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.decision_landscape import (  # noqa: E501
    ShellScaleCaseDecisionLandscape,
    ShellScaleDecisionLandscapeRequest,
    ShellScaleDecisionLandscapeResult,
    ShellScaleDecisionPoint,
)

from .serialization import (
    BandEquivalenceLocalityRequestSerializer,
    CanonicalJsonDocument,
)

DECISION_REQUEST_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy."
    "band-equivalence-locality.shell-scale-decision-request.v1"
)
DECISION_RESULT_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy."
    "band-equivalence-locality.shell-scale-decision-result.v1"
)
DECISION_VERIFICATION_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy."
    "band-equivalence-locality.shell-scale-decision-verification.v1"
)


class _EnvironmentWire(TypedDict):
    ksdft2effmass: str
    matplotlib: str
    numpy: str
    platform: str
    projectkoios_optimization: str
    projectkoios_physkit: str
    python: str


class _RequestWire(TypedDict):
    environment: _EnvironmentWire
    scale_sample_count: int
    schema: str
    source_analysis_request_sha256: str
    status: str


class _PointWire(TypedDict):
    comparison_scale: float
    maximum_hamiltonian_error: float
    maximum_sorted_band_error: float
    pareto_efficient: bool
    retained_blocks: int
    scale_path_coordinate: float
    shell_index: int


class _CaseWire(TypedDict):
    calculated_vertex_count: int
    comparison_scales: list[float]
    gauge_amplitude: float
    name: str
    optimized_comparison_scale: float
    parent_scale: float
    pareto_efficient_vertex_count: int
    points: list[_PointWire]
    retained_block_counts: list[int]
    scale_path_coordinates: list[float]
    shell_indices: list[int]


class _ResultWire(TypedDict):
    cases: list[_CaseWire]
    construction_size: int
    decision_request_sha256: str
    evaluation_size: int
    family: str
    scale_sample_count: int
    schema: str
    status: str


class _VerificationWire(TypedDict):
    decision_request_sha256: str
    decision_result_sha256: str
    passes: bool
    schema: str
    source_analysis_request_sha256: str
    status: str


type _DecisionWire = _RequestWire | _ResultWire | _VerificationWire


@dataclass(frozen=True, slots=True)
class DecisionLandscapeEnvironment:
    """Record exact local software identifiers without claiming reproducibility."""

    python: str
    platform: str
    numpy: str
    matplotlib: str
    ksdft2effmass: str
    projectkoios_optimization: str
    projectkoios_physkit: str

    @classmethod
    def capture(cls) -> DecisionLandscapeEnvironment:
        """Capture the current bounded-development software environment."""
        return cls(
            python=platform.python_version(),
            platform=platform.platform(),
            numpy=np.__version__,
            matplotlib=_package_version("matplotlib"),
            ksdft2effmass=_package_version("ksdft2effmass"),
            projectkoios_optimization=_package_version("projectkoios-optimization"),
            projectkoios_physkit=_package_version("projectkoios-physkit"),
        )


@dataclass(frozen=True, slots=True)
class DecisionLandscapeArtifactResult:
    """Identify one written and independently read-back-checked artifact set."""

    source_request_path: Path
    decision_request_path: Path
    decision_result_path: Path
    verification_path: Path
    source_analysis_request_sha256: str
    decision_request_sha256: str
    decision_result_sha256: str


def _package_version(distribution: str) -> str:
    try:
        return version(distribution)
    except PackageNotFoundError:
        return "not-installed"


def _canonical_document(value: _DecisionWire) -> CanonicalJsonDocument:
    return CanonicalJsonDocument(
        (
            json.dumps(value, allow_nan=False, separators=(",", ":"), sort_keys=True)
            + "\n"
        ).encode("utf-8")
    )


def _environment_wire(value: DecisionLandscapeEnvironment) -> _EnvironmentWire:
    return {
        "ksdft2effmass": value.ksdft2effmass,
        "matplotlib": value.matplotlib,
        "numpy": value.numpy,
        "platform": value.platform,
        "projectkoios_optimization": value.projectkoios_optimization,
        "projectkoios_physkit": value.projectkoios_physkit,
        "python": value.python,
    }


def _point_wire(value: ShellScaleDecisionPoint) -> _PointWire:
    return {
        "comparison_scale": value.comparison_scale,
        "maximum_hamiltonian_error": value.maximum_hamiltonian_error,
        "maximum_sorted_band_error": value.maximum_sorted_band_error,
        "pareto_efficient": value.pareto_efficient,
        "retained_blocks": value.retained_blocks,
        "scale_path_coordinate": value.scale_path_coordinate,
        "shell_index": value.shell_index,
    }


def _case_wire(value: ShellScaleCaseDecisionLandscape) -> _CaseWire:
    return {
        "calculated_vertex_count": value.calculated_vertex_count,
        "comparison_scales": list(value.comparison_scales),
        "gauge_amplitude": value.gauge_amplitude,
        "name": value.name,
        "optimized_comparison_scale": value.optimized_comparison_scale,
        "parent_scale": value.parent_scale,
        "pareto_efficient_vertex_count": value.pareto_efficient_vertex_count,
        "points": [_point_wire(point) for point in value.points],
        "retained_block_counts": list(value.retained_block_counts),
        "scale_path_coordinates": list(value.scale_path_coordinates),
        "shell_indices": list(value.shell_indices),
    }


def _wire_dominates(candidate: _PointWire, point: _PointWire) -> bool:
    candidate_objective = (
        candidate["retained_blocks"],
        candidate["maximum_hamiltonian_error"],
        candidate["maximum_sorted_band_error"],
    )
    point_objective = (
        point["retained_blocks"],
        point["maximum_hamiltonian_error"],
        point["maximum_sorted_band_error"],
    )
    return (
        all(
            candidate_value <= point_value
            for candidate_value, point_value in zip(
                candidate_objective, point_objective, strict=True
            )
        )
        and candidate_objective != point_objective
    )


def _verify_result_semantics(value: _ResultWire) -> bool:
    """Recompute discrete-grid and dominance identities from parsed wire values."""
    for case in value["cases"]:
        shells = case["shell_indices"]
        blocks = case["retained_block_counts"]
        coordinates = case["scale_path_coordinates"]
        scales = case["comparison_scales"]
        points = case["points"]
        if (
            len(shells) != len(blocks)
            or len(coordinates) != value["scale_sample_count"]
            or len(scales) != len(coordinates)
            or len(points) != len(shells) * len(coordinates)
            or case["calculated_vertex_count"] != len(points)
            or case["pareto_efficient_vertex_count"]
            != sum(point["pareto_efficient"] for point in points)
            or coordinates[0] != 0.0
            or coordinates[-1] != 1.0
            or scales[0] != case["optimized_comparison_scale"]
            or scales[-1] != 1.0
        ):
            return False
        for scale_index, (coordinate, scale) in enumerate(
            zip(coordinates, scales, strict=True)
        ):
            for shell_index, (shell, block_count) in enumerate(
                zip(shells, blocks, strict=True)
            ):
                point = points[scale_index * len(shells) + shell_index]
                if (
                    point["scale_path_coordinate"] != coordinate
                    or point["comparison_scale"] != scale
                    or point["shell_index"] != shell
                    or point["retained_blocks"] != block_count
                ):
                    return False
        for point_index, point in enumerate(points):
            efficient = not any(
                other_index != point_index and _wire_dominates(other, point)
                for other_index, other in enumerate(points)
            )
            if point["pareto_efficient"] is not efficient:
                return False
    return True


class ShellScaleDecisionLandscapeRequestSerializer:
    """Serialize a landscape request with its complete source-request identity."""

    __slots__ = ()

    def execute(
        self,
        request: ShellScaleDecisionLandscapeRequest,
        environment: DecisionLandscapeEnvironment,
        source_analysis_request: CanonicalJsonDocument,
    ) -> CanonicalJsonDocument:
        """Return canonical request bytes without filesystem side effects."""
        if type(request) is not ShellScaleDecisionLandscapeRequest:
            raise TypeError("request must be ShellScaleDecisionLandscapeRequest")
        if type(environment) is not DecisionLandscapeEnvironment:
            raise TypeError("environment must be DecisionLandscapeEnvironment")
        if type(source_analysis_request) is not CanonicalJsonDocument:
            raise TypeError("source_analysis_request must be CanonicalJsonDocument")
        return _canonical_document(
            _RequestWire(
                environment=_environment_wire(environment),
                scale_sample_count=request.scale_sample_count,
                schema=DECISION_REQUEST_SCHEMA_ID,
                source_analysis_request_sha256=(
                    source_analysis_request.content_sha256()
                ),
                status="sampled-development-request-not-evidence",
            )
        )


class ShellScaleDecisionLandscapeResultSerializer:
    """Serialize calculated vertices with exact request binding."""

    __slots__ = ()

    def execute(
        self,
        result: ShellScaleDecisionLandscapeResult,
        decision_request: CanonicalJsonDocument,
    ) -> CanonicalJsonDocument:
        """Return canonical result bytes without filesystem side effects."""
        if type(result) is not ShellScaleDecisionLandscapeResult:
            raise TypeError("result must be ShellScaleDecisionLandscapeResult")
        if type(decision_request) is not CanonicalJsonDocument:
            raise TypeError("decision_request must be CanonicalJsonDocument")
        return _canonical_document(
            _ResultWire(
                cases=[_case_wire(case) for case in result.cases],
                construction_size=result.construction_size,
                decision_request_sha256=decision_request.content_sha256(),
                evaluation_size=result.evaluation_size,
                family=result.family.value,
                scale_sample_count=result.scale_sample_count,
                schema=DECISION_RESULT_SCHEMA_ID,
                status=result.status,
            )
        )


class ShellScaleDecisionLandscapeArtifactWriter:
    """Write, schema-check, re-read, and identity-check one family artifact set."""

    __slots__ = ()

    def execute(
        self,
        request: ShellScaleDecisionLandscapeRequest,
        result: ShellScaleDecisionLandscapeResult,
        output_directory: Path,
        environment: DecisionLandscapeEnvironment,
    ) -> DecisionLandscapeArtifactResult:
        """Write canonical files and fail closed on any read-back mismatch."""
        if not isinstance(output_directory, Path):
            raise TypeError("output_directory must be pathlib.Path")
        if result.family is not request.locality_request.family:
            raise ValueError("result family does not match the source request")
        if result.scale_sample_count != request.scale_sample_count:
            raise ValueError("result scale sample count does not match the request")
        from .decision_landscape_schemas import (  # avoid schema/serializer cycle
            DecisionLandscapeSchema,
            DecisionLandscapeSchemaKind,
        )

        output_directory.mkdir(parents=True, exist_ok=True)
        slug = result.family.name.lower().replace("_", "-")
        source = BandEquivalenceLocalityRequestSerializer().execute(
            request.locality_request
        )
        decision_request = ShellScaleDecisionLandscapeRequestSerializer().execute(
            request,
            environment,
            source,
        )
        decision_result = ShellScaleDecisionLandscapeResultSerializer().execute(
            result,
            decision_request,
        )
        request_schema = DecisionLandscapeSchema(DecisionLandscapeSchemaKind.REQUEST)
        result_schema = DecisionLandscapeSchema(DecisionLandscapeSchemaKind.RESULT)
        request_schema.validate(decision_request.canonical_bytes())
        result_schema.validate(decision_result.canonical_bytes())

        source_path = output_directory / f"{slug}-source-analysis-request.json"
        request_path = output_directory / f"{slug}-shell-scale-request.json"
        result_path = output_directory / f"{slug}-shell-scale-result.json"
        verification_path = output_directory / f"{slug}-shell-scale-verification.json"
        source.write_to(source_path)
        decision_request.write_to(request_path)
        decision_result.write_to(result_path)

        source_read = CanonicalJsonDocument(source_path.read_bytes())
        request_read = CanonicalJsonDocument(request_path.read_bytes())
        result_read = CanonicalJsonDocument(result_path.read_bytes())
        request_schema.validate(request_read.canonical_bytes())
        result_schema.validate(result_read.canonical_bytes())
        request_wire = cast(_RequestWire, json.loads(request_read.canonical_bytes()))
        result_wire = cast(_ResultWire, json.loads(result_read.canonical_bytes()))
        source_matches = (
            request_wire["source_analysis_request_sha256"]
            == source_read.content_sha256()
        )
        request_matches = (
            result_wire["decision_request_sha256"] == request_read.content_sha256()
        )
        content_matches = (
            source_read.canonical_bytes() == source.canonical_bytes()
            and request_read.canonical_bytes() == decision_request.canonical_bytes()
            and result_read.canonical_bytes() == decision_result.canonical_bytes()
        )
        semantics_match = _verify_result_semantics(result_wire)
        if (
            not source_matches
            or not request_matches
            or not content_matches
            or not semantics_match
        ):
            raise ValueError(
                "decision-landscape artifact read-back verification failed"
            )
        verification = _canonical_document(
            _VerificationWire(
                decision_request_sha256=request_read.content_sha256(),
                decision_result_sha256=result_read.content_sha256(),
                passes=True,
                schema=DECISION_VERIFICATION_SCHEMA_ID,
                source_analysis_request_sha256=source_read.content_sha256(),
                status="independent-canonical-read-back-verification-not-adequacy",
            )
        )
        verification_schema = DecisionLandscapeSchema(
            DecisionLandscapeSchemaKind.VERIFICATION
        )
        verification_schema.validate(verification.canonical_bytes())
        verification.write_to(verification_path)
        verification_read = CanonicalJsonDocument(verification_path.read_bytes())
        verification_schema.validate(verification_read.canonical_bytes())
        if verification_read.canonical_bytes() != verification.canonical_bytes():
            raise ValueError("verification artifact changed during read-back")
        return DecisionLandscapeArtifactResult(
            source_request_path=source_path,
            decision_request_path=request_path,
            decision_result_path=result_path,
            verification_path=verification_path,
            source_analysis_request_sha256=source_read.content_sha256(),
            decision_request_sha256=request_read.content_sha256(),
            decision_result_sha256=result_read.content_sha256(),
        )


__all__ = [
    "DECISION_REQUEST_SCHEMA_ID",
    "DECISION_RESULT_SCHEMA_ID",
    "DECISION_VERIFICATION_SCHEMA_ID",
    "DecisionLandscapeArtifactResult",
    "DecisionLandscapeEnvironment",
    "ShellScaleDecisionLandscapeArtifactWriter",
    "ShellScaleDecisionLandscapeRequestSerializer",
    "ShellScaleDecisionLandscapeResultSerializer",
]
