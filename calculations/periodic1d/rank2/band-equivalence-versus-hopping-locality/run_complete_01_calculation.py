#!/usr/bin/env python3
"""Calculate the proposed complete five-scale rank-two aggregate."""

from __future__ import annotations

import hashlib
import math
import subprocess
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.amplitude_refinement.analysis import (  # noqa: E501
    Periodic1DRank2AdaptiveAmplitudeAnalyzer,
    Periodic1DRank2AdaptiveAmplitudeRequest,
    Periodic1DRank2AmplitudeRefinementThresholds,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.momentum_refinement.analysis import (  # noqa: E501
    Periodic1DRank2MomentumRefinementThresholds,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.momentum_refinement.family import (  # noqa: E501
    Periodic1DRank2MomentumRefinementFamilyAnalyzer,
    Periodic1DRank2MomentumRefinementFamilyRequest,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_family.analysis import (  # noqa: E501
    Periodic1DRank2ParentFamilyAnalyzer,
    Periodic1DRank2ParentFamilyRequest,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.request import (  # noqa: E501
    Periodic1DRank2Request,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention.complete_five_scale import (  # noqa: E501
    Periodic1DRank2CompleteFiveScaleCalculationRecord,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.family import (
    Periodic1DRank2TruncationFamilyAnalyzer,
    Periodic1DRank2TruncationFamilyRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.mesh_stability import (
    Periodic1DRank2TruncationMeshStabilityAssessment,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-embedded-rank2-five-scale-complete-v1"
CALCULATION_FAMILY = "periodic1d-rank2-band-equivalence-hopping-locality"
EVIDENCE_STATUS = "unsealed candidate complete-scope finite numerical control"
CLAIM_BOUNDARY = (
    "Candidate finite numerical calculation only; not scientific validation, "
    "continuum convergence, evidence sealing, promotion, or publication acceptance."
)
SCRIPT_PATH = Path(__file__).resolve()
EXECUTION_DIRECTORY = SCRIPT_PATH.parent / "executions" / EXECUTION_ID
TEMPORARY_DIRECTORY = EXECUTION_DIRECTORY.with_name(
    f".{EXECUTION_DIRECTORY.name}.incomplete"
)
DRAFT_TOLERANCE = 1.01e-8
SUPPORT_TOLERANCE = 1.0e-8
PARENT_HOPPING_SCALES = (0.0, 0.25, 0.5, 0.75, 1.0)
PARENT_FAMILY_MESH_SIZE = 256
PARENT_FAMILY_AMPLITUDE_INTERVALS = 32
MOMENTUM_MESH_SIZES = (32, 64, 128, 256, 512)
MOMENTUM_AMPLITUDE_INTERVALS = 64
MOMENTUM_REQUIRED_STABLE_REFINEMENTS = 2
ADAPTIVE_MESH_SIZE = 128
ADAPTIVE_INITIAL_AMPLITUDE_INTERVALS = 8
ADAPTIVE_MAXIMUM_REFINEMENT_LEVELS = 4
ADAPTIVE_MAXIMUM_EVALUATED_AMPLITUDES = 129
TRUNCATION_CONSTRUCTION_MESH_SIZES = (128, 256, 512)
TRUNCATION_MAXIMUM_RANGE = 16

if EXECUTION_DIRECTORY.exists() or TEMPORARY_DIRECTORY.exists():
    raise FileExistsError("refusing to overwrite a complete-five-scale execution")
repository = next(
    parent for parent in SCRIPT_PATH.parents if (parent / ".git").exists()
)
source_revision = subprocess.run(
    ("git", "-C", str(repository), "rev-parse", "HEAD"),
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
source_status = subprocess.run(
    ("git", "-C", str(repository), "status", "--porcelain"),
    check=True,
    capture_output=True,
    text=True,
).stdout
if source_status:
    raise ValueError("complete-five-scale execution requires a clean source worktree")

family_amplitudes = tuple(
    float(index * math.pi / (4 * PARENT_FAMILY_AMPLITUDE_INTERVALS))
    for index in range(PARENT_FAMILY_AMPLITUDE_INTERVALS + 1)
)
momentum_amplitudes = tuple(
    float(index * math.pi / (4 * MOMENTUM_AMPLITUDE_INTERVALS))
    for index in range(MOMENTUM_AMPLITUDE_INTERVALS + 1)
)
adaptive_amplitudes = tuple(
    float(index * math.pi / (4 * ADAPTIVE_INITIAL_AMPLITUDE_INTERVALS))
    for index in range(ADAPTIVE_INITIAL_AMPLITUDE_INTERVALS + 1)
)
family_template = Periodic1DRank2Request(
    reciprocal_mesh_size=PARENT_FAMILY_MESH_SIZE,
    amplitudes=family_amplitudes,
    parent_hopping_scale=PARENT_HOPPING_SCALES[-1],
    minimum_external_gap=1.0,
    minimum_transport_singular_value=0.99,
    frame_absolute_tolerance=1.0e-10,
    transport_rank_relative_tolerance=1.0e-12,
    transport_validation_relative_tolerance=1.0e-10,
    harmonic_absolute_degeneracy_tolerance=1.0e-14,
    harmonic_relative_degeneracy_tolerance=1.0e-13,
)
parent_family_request = Periodic1DRank2ParentFamilyRequest(
    template_request=family_template,
    parent_hopping_scales=PARENT_HOPPING_SCALES,
)
transporter = ClosedLoopPolarFrameTransporter()
parent_family = Periodic1DRank2ParentFamilyAnalyzer(
    request=parent_family_request,
    transporter=transporter,
).execute()

momentum_template = Periodic1DRank2Request(
    reciprocal_mesh_size=MOMENTUM_MESH_SIZES[0],
    amplitudes=momentum_amplitudes,
    parent_hopping_scale=PARENT_HOPPING_SCALES[-1],
    minimum_external_gap=1.0,
    minimum_transport_singular_value=0.99,
    frame_absolute_tolerance=1.0e-10,
    transport_rank_relative_tolerance=1.0e-12,
    transport_validation_relative_tolerance=1.0e-10,
    harmonic_absolute_degeneracy_tolerance=1.0e-14,
    harmonic_relative_degeneracy_tolerance=1.0e-13,
)
momentum_parent_family_request = Periodic1DRank2ParentFamilyRequest(
    template_request=momentum_template,
    parent_hopping_scales=PARENT_HOPPING_SCALES,
)
momentum_thresholds = Periodic1DRank2MomentumRefinementThresholds(
    maximum_parent_diagnostic_change=DRAFT_TOLERANCE,
    maximum_correlation_change=DRAFT_TOLERANCE,
    maximum_threshold_change=DRAFT_TOLERANCE,
    maximum_hopping_weight_change=DRAFT_TOLERANCE,
    maximum_hopping_power_change=DRAFT_TOLERANCE,
    maximum_angle_change=DRAFT_TOLERANCE,
    maximum_band_defect=DRAFT_TOLERANCE,
    maximum_reconstruction_defect=DRAFT_TOLERANCE,
    maximum_parseval_defect=DRAFT_TOLERANCE,
)
momentum_refinement_family = Periodic1DRank2MomentumRefinementFamilyAnalyzer(
    request=Periodic1DRank2MomentumRefinementFamilyRequest(
        parent_family_request=momentum_parent_family_request,
        reciprocal_mesh_sizes=MOMENTUM_MESH_SIZES,
        thresholds=momentum_thresholds,
        required_stable_refinements=MOMENTUM_REQUIRED_STABLE_REFINEMENTS,
    ),
    transporter=transporter,
).execute()

adaptive_template = Periodic1DRank2Request(
    reciprocal_mesh_size=ADAPTIVE_MESH_SIZE,
    amplitudes=adaptive_amplitudes,
    parent_hopping_scale=PARENT_HOPPING_SCALES[-1],
    minimum_external_gap=1.0,
    minimum_transport_singular_value=0.99,
    frame_absolute_tolerance=1.0e-10,
    transport_rank_relative_tolerance=1.0e-12,
    transport_validation_relative_tolerance=1.0e-10,
    harmonic_absolute_degeneracy_tolerance=1.0e-14,
    harmonic_relative_degeneracy_tolerance=1.0e-13,
)
adaptive_amplitude = Periodic1DRank2AdaptiveAmplitudeAnalyzer(
    request=Periodic1DRank2AdaptiveAmplitudeRequest(
        template_request=adaptive_template,
        thresholds=Periodic1DRank2AmplitudeRefinementThresholds(
            maximum_correlation_defect=DRAFT_TOLERANCE,
            maximum_operator_threshold_defect=DRAFT_TOLERANCE,
            maximum_joint_threshold_defect=DRAFT_TOLERANCE,
            maximum_hopping_weight_defect=DRAFT_TOLERANCE,
            maximum_hopping_power_defect=DRAFT_TOLERANCE,
        ),
        maximum_refinement_levels=ADAPTIVE_MAXIMUM_REFINEMENT_LEVELS,
        maximum_evaluated_amplitudes=ADAPTIVE_MAXIMUM_EVALUATED_AMPLITUDES,
    ),
    transporter=transporter,
).execute()

truncation_families = tuple(
    Periodic1DRank2TruncationFamilyAnalyzer(
        request=Periodic1DRank2TruncationFamilyRequest.every_integer_through(
            parent_family_request=Periodic1DRank2ParentFamilyRequest(
                template_request=Periodic1DRank2Request(
                    reciprocal_mesh_size=construction_mesh_size,
                    amplitudes=family_amplitudes,
                    parent_hopping_scale=PARENT_HOPPING_SCALES[-1],
                    minimum_external_gap=1.0,
                    minimum_transport_singular_value=0.99,
                    frame_absolute_tolerance=1.0e-10,
                    transport_rank_relative_tolerance=1.0e-12,
                    transport_validation_relative_tolerance=1.0e-10,
                    harmonic_absolute_degeneracy_tolerance=1.0e-14,
                    harmonic_relative_degeneracy_tolerance=1.0e-13,
                ),
                parent_hopping_scales=PARENT_HOPPING_SCALES,
            ),
            maximum_range=TRUNCATION_MAXIMUM_RANGE,
            evaluation_mesh_size=4 * construction_mesh_size + 1,
            support_tolerance=SUPPORT_TOLERANCE,
        ),
        transporter=transporter,
    ).execute()
    for construction_mesh_size in TRUNCATION_CONSTRUCTION_MESH_SIZES
)
record = Periodic1DRank2CompleteFiveScaleCalculationRecord(
    parent_family=parent_family,
    momentum_refinement_family=momentum_refinement_family,
    adaptive_amplitude=adaptive_amplitude,
    truncation_mesh_stability=Periodic1DRank2TruncationMeshStabilityAssessment(
        truncation_families
    ),
)
result_bytes = record.to_json()
if type(record).from_json(result_bytes).to_json() != result_bytes:
    raise ValueError("complete-five-scale record failed canonical typed admission")

(TEMPORARY_DIRECTORY / "results").mkdir(parents=True)
(TEMPORARY_DIRECTORY / "results" / "calculation.json").write_bytes(result_bytes)
(TEMPORARY_DIRECTORY / "execution.json").write_bytes(
    TypedJsonValueCodec().serialize_bytes(
        {
            "schema_version": 1,
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "created_utc": datetime.now(UTC).isoformat(),
            "result_path": "results/calculation.json",
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "script_sha256": hashlib.sha256(SCRIPT_PATH.read_bytes()).hexdigest(),
            "source_revision": source_revision,
            "source_worktree_clean": True,
            "software_versions": {
                "ksdft2effmass": version("ksdft2effmass"),
                "numpy": version("numpy"),
                "projectkoios-optimization": version("projectkoios-optimization"),
                "projectkoios-physkit": version("projectkoios-physkit"),
                "scipy": version("scipy"),
            },
            "evidence_status": EVIDENCE_STATUS,
            "claim_boundary": CLAIM_BOUNDARY,
            "sealed": False,
        }
    )
)
(TEMPORARY_DIRECTORY / "UNSEALED.md").write_text(
    "# Unsealed execution\n\n"
    "This candidate finite numerical control is not sealed scientific evidence.\n",
    encoding="utf-8",
)
TEMPORARY_DIRECTORY.rename(EXECUTION_DIRECTORY)
