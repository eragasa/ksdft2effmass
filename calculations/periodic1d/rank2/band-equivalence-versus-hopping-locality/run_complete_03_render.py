#!/usr/bin/env python3
"""Render the stored authenticated complete-five-scale summary table."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.periodic1d import (
    Periodic1DRank2CompleteFiveScaleSummaryRenderer,
    Periodic1DRank2CompleteFiveScaleVerification,
    Periodic1DRank2CompleteFiveScaleVerifier,
    Periodic1DRank2CompleteFiveScaleVisualizationData,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-embedded-rank2-five-scale-complete-v1"
CALCULATION_FAMILY = "periodic1d-rank2-band-equivalence-hopping-locality"
CLAIM_BOUNDARY = (
    "Presentation from stored authenticated finite values only; no calculation or "
    "verification rerun, scientific validation, evidence sealing, or publication."
)
SCRIPT_PATH = Path(__file__).resolve()
EXECUTION_DIRECTORY = SCRIPT_PATH.parent / "executions" / EXECUTION_ID
RESULT_PATH = EXECUTION_DIRECTORY / "results" / "calculation.json"
VERIFICATION_PATH = EXECUTION_DIRECTORY / "verification" / "verification.json"
VERIFICATION_MANIFEST_PATH = EXECUTION_DIRECTORY / "verification" / "manifest.json"
RENDERING_DIRECTORY = EXECUTION_DIRECTORY / "rendering"
TEMPORARY_DIRECTORY = EXECUTION_DIRECTORY / ".rendering.incomplete"

if RENDERING_DIRECTORY.exists() or TEMPORARY_DIRECTORY.exists():
    raise FileExistsError("refusing to overwrite complete-five-scale rendering")
if not all(
    path.is_file()
    for path in (RESULT_PATH, VERIFICATION_PATH, VERIFICATION_MANIFEST_PATH)
):
    raise FileNotFoundError("calculation and verification must precede rendering")

result_bytes = RESULT_PATH.read_bytes()
verification_bytes = VERIFICATION_PATH.read_bytes()
verification = Periodic1DRank2CompleteFiveScaleVerification.from_json(
    verification_bytes
)
if verification.to_json() != verification_bytes:
    raise ValueError("verification artifact is not canonical typed JSON")
codec = TypedJsonValueCodec()
manifest_bytes = VERIFICATION_MANIFEST_PATH.read_bytes()
manifest = codec.deserialize_bytes(manifest_bytes)
if not isinstance(manifest, Mapping):
    raise TypeError("verification manifest must decode to a mapping")
if codec.serialize_bytes(manifest) != manifest_bytes:
    raise ValueError("verification manifest is not canonical typed JSON")
if manifest.get("calculation_family") != CALCULATION_FAMILY:
    raise ValueError("verification calculation family does not match")
if manifest.get("execution_id") != EXECUTION_ID:
    raise ValueError("verification execution identifier does not match")
if manifest.get("result_sha256") != hashlib.sha256(result_bytes).hexdigest():
    raise ValueError("verification manifest authenticates different result bytes")
if (
    manifest.get("verification_sha256")
    != hashlib.sha256(verification_bytes).hexdigest()
):
    raise ValueError("verification manifest authenticates different verification")

record = Periodic1DRank2CompleteFiveScaleVerifier(result_bytes).admit_stored(
    verification
)
visualization_data = Periodic1DRank2CompleteFiveScaleVisualizationData.from_record(
    record,
    source_sha256=verification.subject_sha256,
)
visualization_bytes = visualization_data.to_json()
if hashlib.sha256(visualization_bytes).hexdigest() != (
    verification.visualization_data_sha256
):
    raise ValueError("stored verification authenticates different visualization data")
summary_bytes = Periodic1DRank2CompleteFiveScaleSummaryRenderer(
    visualization_data
).render()

TEMPORARY_DIRECTORY.mkdir()
(TEMPORARY_DIRECTORY / "visualization-data.json").write_bytes(visualization_bytes)
(TEMPORARY_DIRECTORY / "complete-five-scale-summary.md").write_bytes(summary_bytes)
(TEMPORARY_DIRECTORY / "manifest.json").write_bytes(
    codec.serialize_bytes(
        {
            "schema_version": 1,
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "verification_sha256": hashlib.sha256(verification_bytes).hexdigest(),
            "visualization_data_sha256": hashlib.sha256(
                visualization_bytes
            ).hexdigest(),
            "summary_sha256": hashlib.sha256(summary_bytes).hexdigest(),
            "script_sha256": hashlib.sha256(SCRIPT_PATH.read_bytes()).hexdigest(),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
)
TEMPORARY_DIRECTORY.rename(RENDERING_DIRECTORY)
