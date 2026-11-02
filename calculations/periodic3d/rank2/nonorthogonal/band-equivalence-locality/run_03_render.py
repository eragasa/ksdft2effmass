#!/usr/bin/env python3
"""Render authenticated outputs for one nonorthogonal periodic-3D execution."""

from __future__ import annotations

import hashlib
from pathlib import Path

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.band_equivalence_hopping_locality.verification import (
    BandEquivalenceHoppingLocalityVerificationThresholds,
)
from ksdft2effmass.band_equivalence_hopping_locality.visualizations import (
    BandEquivalenceHoppingLocalityVisualizationPlotEnum,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.lifecycle import (
    Periodic3DRank2BandEquivalenceHoppingLocalityExecution,
    Periodic3DRank2BandEquivalenceHoppingLocalityExecutionVerification,
    Periodic3DRank2BandEquivalenceHoppingLocalityRendering,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.reference import (
    Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.result import (
    Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.verification import (
    Periodic3DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier,
    Periodic3DRank2BandEquivalenceHoppingLocalityResultVerifier,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.visualizations.visualizer import (
    Periodic3DRank2BandEquivalenceHoppingLocalityVisualizer,
)

EXECUTION_ID = "direct-fcc-diamond-rank2-n8"
CALCULATION_FAMILY = "periodic3d-rank2-nonorthogonal-band-equivalence-locality"
STUDY_FAMILY = (
    "ksdft2effmass.campaign.model-adequacy.periodic3d-nonorthogonal."
    "band-equivalence-versus-hopping-locality"
)
VERIFICATION_THRESHOLDS = BandEquivalenceHoppingLocalityVerificationThresholds(
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
    raise FileExistsError("refusing to overwrite periodic-3D nonorthogonal rendering")
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
execution = Periodic3DRank2BandEquivalenceHoppingLocalityExecution.from_json(execution_bytes)
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
verification_record = (
    Periodic3DRank2BandEquivalenceHoppingLocalityExecutionVerification.from_json(
        verification_bytes
    )
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
result = Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult.from_json(result_bytes)
if result.to_json() != result_bytes:
    raise ValueError("result document is not canonical typed JSON")
admitted = Periodic3DRank2BandEquivalenceHoppingLocalityResultVerifier(
    result_wire=result_bytes,
    diagnostic_verifier=Periodic3DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier(
        request=result.request,
        result=result.diagnostics,
    ),
    shell_power_analyzer=Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer(
        request=result.request
    ),
    thresholds=VERIFICATION_THRESHOLDS,
).admit_stored(
    verification=verification,
    visualization_data=data,
)
visualizations = Periodic3DRank2BandEquivalenceHoppingLocalityVisualizer(
    data=admitted.visualization_data,
    verification=admitted.verification,
).visualize()
expected_plots = frozenset(BandEquivalenceHoppingLocalityVisualizationPlotEnum)
if {visualization.plot for visualization in visualizations} != expected_plots:
    raise ValueError("rendered plot inventory differs from the declared inventory")
temporary_directory.mkdir()
for visualization in visualizations:
    (temporary_directory / visualization.filename).write_bytes(visualization.png)
rendering = Periodic3DRank2BandEquivalenceHoppingLocalityRendering(
    schema_version=1,
    schema=(
        "ksdft2effmass.periodic3d-rank2-nonorthogonal-"
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
        "values; not a silicon calculation, new scientific evidence, "
        "publication acceptance, or evidence sealing."
    ),
)
(temporary_directory / "rendering.json").write_bytes(rendering.to_json())
temporary_directory.rename(figures_directory)
