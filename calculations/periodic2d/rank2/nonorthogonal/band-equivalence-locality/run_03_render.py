#!/usr/bin/env python3
"""Render authenticated outputs for one nonorthogonal periodic-2D execution."""

from __future__ import annotations

import hashlib
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.calculation import (
    BandEquivalenceLocalityVerifier,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.lifecycle import (
    BandEquivalenceLocalityExecution,
    BandEquivalenceLocalityExecutionVerification,
    BandEquivalenceLocalityRendering,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.reference import (
    BandEquivalenceLocalityIndependentShellPowerAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.result import (
    BandEquivalenceLocalityCalculationResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.verification import (
    BandEquivalenceLocalityResultVerifier,
    BandEquivalenceLocalityVerificationThresholds,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.visualizations import (
    BandEquivalenceLocalityVisualizationPlotEnum,
    BandEquivalenceLocalityVisualizer,
)
from projectkoios.physkit.units import ScalarQuantity, Unitless

EXECUTION_ID = "direct-triangular-honeycomb-rank2-n16"
CALCULATION_FAMILY = "periodic2d-rank2-nonorthogonal-band-equivalence-locality"
STUDY_FAMILY = (
    "ksdft2effmass.campaign.model-adequacy.periodic2d-nonorthogonal."
    "band-equivalence-versus-hopping-locality"
)
VERIFICATION_THRESHOLDS = BandEquivalenceLocalityVerificationThresholds(
    stored_identity_maximum_defect=ScalarQuantity(5.0e-11, Unitless()),
    independent_parent_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
    independent_band_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
    independent_shell_power_maximum_defect=ScalarQuantity(5.0e-11, Unitless()),
)
script_path = Path(__file__).resolve()
calculation_script_path = script_path.with_name("run_01_calculation.py")
verification_script_path = script_path.with_name("run_02_verification.py")
execution_directory = script_path.parent / "executions" / EXECUTION_ID
execution_path = execution_directory / "execution.json"
result_path = execution_directory / "results" / "result.json"
verification_path = execution_directory / "verification" / "verification.json"
figures_directory = execution_directory / "figures"
temporary_directory = execution_directory / ".figures.incomplete"
if figures_directory.exists() or temporary_directory.exists():
    raise FileExistsError(
        "refusing to overwrite nonorthogonal periodic-2D locality rendering"
    )
if not all(
    path.is_file()
    for path in (
        calculation_script_path,
        verification_script_path,
        execution_path,
        result_path,
        verification_path,
    )
):
    raise FileNotFoundError("calculation and verification must precede rendering")
execution_bytes = execution_path.read_bytes()
result_bytes = result_path.read_bytes()
verification_bytes = verification_path.read_bytes()
execution = BandEquivalenceLocalityExecution.from_json(execution_bytes)
if execution.to_json() != execution_bytes:
    raise ValueError("execution document is not canonical typed JSON")
if execution.execution_id != EXECUTION_ID:
    raise ValueError("execution identifier does not match")
if execution.calculation_family != CALCULATION_FAMILY:
    raise ValueError("calculation family does not match")
if execution.study_family != STUDY_FAMILY:
    raise ValueError("study family does not match")
if execution.outcome != "completed":
    raise ValueError("calculation outcome is not completed")
if execution.result_sha256 != hashlib.sha256(result_bytes).hexdigest():
    raise ValueError("result bytes do not match execution.json")
if (
    execution.script_sha256
    != hashlib.sha256(calculation_script_path.read_bytes()).hexdigest()
):
    raise ValueError("calculation script bytes do not match execution.json")
verification_record = BandEquivalenceLocalityExecutionVerification.from_json(
    verification_bytes
)
if verification_record.to_json() != verification_bytes:
    raise ValueError("verification document is not canonical typed JSON")
if verification_record.execution_id != EXECUTION_ID:
    raise ValueError("verification execution identifier does not match")
if verification_record.calculation_family != CALCULATION_FAMILY:
    raise ValueError("verification calculation family does not match")
if verification_record.study_family != STUDY_FAMILY:
    raise ValueError("verification study family does not match")
if verification_record.result_sha256 != hashlib.sha256(result_bytes).hexdigest():
    raise ValueError("verification authenticates different result bytes")
if (
    verification_record.script_sha256
    != hashlib.sha256(verification_script_path.read_bytes()).hexdigest()
):
    raise ValueError("verification script bytes do not match verification.json")
verification = verification_record.verification
data = verification_record.visualization_data
result = BandEquivalenceLocalityCalculationResult.from_json(result_bytes)
if result.to_json() != result_bytes:
    raise ValueError("result document is not canonical typed JSON")
admitted = BandEquivalenceLocalityResultVerifier(
    result_wire=result_bytes,
    diagnostic_verifier=BandEquivalenceLocalityVerifier(
        request=result.request,
        result=result.diagnostics,
    ),
    shell_power_analyzer=BandEquivalenceLocalityIndependentShellPowerAnalyzer(
        request=result.request
    ),
    thresholds=VERIFICATION_THRESHOLDS,
).admit_stored(
    verification=verification,
    visualization_data=data,
)
visualizations = BandEquivalenceLocalityVisualizer(
    data=admitted.visualization_data,
    verification=admitted.verification,
).visualize()
expected_plots = frozenset(BandEquivalenceLocalityVisualizationPlotEnum)
if {visualization.plot for visualization in visualizations} != expected_plots:
    raise ValueError("rendered plot inventory differs from the declared inventory")
temporary_directory.mkdir()
for visualization in visualizations:
    (temporary_directory / visualization.filename).write_bytes(visualization.png)
rendering = BandEquivalenceLocalityRendering(
    schema_version=1,
    schema=(
        "ksdft2effmass.periodic2d-rank2-nonorthogonal-"
        "band-equivalence-locality-rendering.direct.v1"
    ),
    calculation_family=CALCULATION_FAMILY,
    study_family=STUDY_FAMILY,
    execution_id=EXECUTION_ID,
    outcome="completed",
    verification_sha256=hashlib.sha256(verification_bytes).hexdigest(),
    figures={
        visualization.filename: hashlib.sha256(visualization.png).hexdigest()
        for visualization in visualizations
    },
    script_sha256=hashlib.sha256(script_path.read_bytes()).hexdigest(),
    claim_boundary=(
        "Presentation only from independently verified finite synthetic "
        "nonorthogonal values; not graphene, new scientific evidence, "
        "publication acceptance, or evidence sealing."
    ),
)
(temporary_directory / "rendering.json").write_bytes(rendering.to_json())
temporary_directory.rename(figures_directory)
