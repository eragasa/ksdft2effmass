#!/usr/bin/env python3
"""Render the stored authenticated aggregate figure inventory."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2 import (
    Periodic1DRank2CalculationVerification,
    Periodic1DRank2CalculationVerifier,
    Periodic1DRank2CalculationVisualizationData,
    Periodic1DRank2CalculationVisualizer,
    Periodic1DRank2ParentFamilyAnalysisRecord,
    Periodic1DRank2ParentFamilyVerification,
    Periodic1DRank2ParentFamilyVisualizationData,
    Periodic1DRank2ParentFamilyVisualizer,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-embedded-rank2-controlled-v2"
CALCULATION_FAMILY = "periodic1d-rank2-band-equivalence-hopping-locality"
CLAIM_BOUNDARY = (
    "Presentation from stored authenticated finite values only; no scientific "
    "verification rerun, evidence sealing, or publication."
)
DPI = 180
SCRIPT_PATH = Path(__file__).resolve()
EXECUTION_DIRECTORY = SCRIPT_PATH.parent / "executions" / EXECUTION_ID
RESULT_PATH = EXECUTION_DIRECTORY / "results" / "calculation.json"
VERIFICATION_PATH = EXECUTION_DIRECTORY / "verification" / "verification.json"
VERIFICATION_MANIFEST_PATH = EXECUTION_DIRECTORY / "verification" / "manifest.json"
FIGURES_DIRECTORY = EXECUTION_DIRECTORY / "figures"
TEMPORARY_DIRECTORY = EXECUTION_DIRECTORY / ".figures.incomplete"

if FIGURES_DIRECTORY.exists() or TEMPORARY_DIRECTORY.exists():
    raise FileExistsError("refusing to overwrite band-locality rendering")
if not all(
    path.is_file()
    for path in (RESULT_PATH, VERIFICATION_PATH, VERIFICATION_MANIFEST_PATH)
):
    raise FileNotFoundError("calculation and verification must precede rendering")

result_bytes = RESULT_PATH.read_bytes()
verification_bytes = VERIFICATION_PATH.read_bytes()
verification = Periodic1DRank2CalculationVerification.from_json(verification_bytes)
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

record = Periodic1DRank2CalculationVerifier(result_bytes).admit_stored(verification)
family_bytes = Periodic1DRank2ParentFamilyAnalysisRecord(record.parent_family).to_json()
family_sha256 = hashlib.sha256(family_bytes).hexdigest()
family_verification = verification.components[0]
if type(family_verification) is not (Periodic1DRank2ParentFamilyVerification):
    raise TypeError("stored family verification has the wrong type")
data = Periodic1DRank2ParentFamilyVisualizationData.from_analysis(
    record.parent_family,
    source_sha256=family_sha256,
)
if hashlib.sha256(data.to_json()).hexdigest() != (
    family_verification.visualization_data_sha256
):
    raise ValueError("stored verification authenticates different visualization data")
family_visualizations = Periodic1DRank2ParentFamilyVisualizer(
    data=data,
    verification=family_verification,
    dpi=DPI,
).visualize()
calculation_data = Periodic1DRank2CalculationVisualizationData.from_record(
    record,
    source_sha256=verification.subject_sha256,
)
if hashlib.sha256(calculation_data.to_json()).hexdigest() != (
    verification.visualization_data_sha256
):
    raise ValueError("stored verification authenticates different aggregate data")
calculation_visualizations = Periodic1DRank2CalculationVisualizer(
    data=calculation_data,
    verification=verification,
    dpi=DPI,
).visualize()
visualizations = family_visualizations | calculation_visualizations

TEMPORARY_DIRECTORY.mkdir()
for visualization in visualizations:
    (TEMPORARY_DIRECTORY / visualization.filename).write_bytes(visualization.png)
(TEMPORARY_DIRECTORY / "rendering.json").write_bytes(
    codec.serialize_bytes(
        {
            "schema_version": 1,
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "verification_sha256": hashlib.sha256(verification_bytes).hexdigest(),
            "figures": {
                visualization.filename: hashlib.sha256(visualization.png).hexdigest()
                for visualization in visualizations
            },
            "script_sha256": hashlib.sha256(SCRIPT_PATH.read_bytes()).hexdigest(),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
)
TEMPORARY_DIRECTORY.rename(FIGURES_DIRECTORY)
