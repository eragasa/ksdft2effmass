#!/usr/bin/env python3
"""Independently verify one direct nonorthogonal periodic-3D locality execution."""

from __future__ import annotations

import hashlib
from pathlib import Path

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.band_equivalence_hopping_locality.verification import (
    BandEquivalenceHoppingLocalityVerificationThresholds,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.lifecycle import (
    Periodic3DRank2BandEquivalenceHoppingLocalityExecution,
    Periodic3DRank2BandEquivalenceHoppingLocalityExecutionVerification,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.reference import (
    Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.request import (
    Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.result import (
    Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.verification import (
    Periodic3DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier,
    Periodic3DRank2BandEquivalenceHoppingLocalityResultVerifier,
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
execution_directory = script_path.parent / "executions" / EXECUTION_ID
execution_path = execution_directory / "execution.json"
configuration_path = execution_directory / "inputs" / "configuration.json"
result_path = execution_directory / "results" / "result.json"
verification_directory = execution_directory / "verification"
temporary_directory = execution_directory / ".verification.incomplete"
if verification_directory.exists() or temporary_directory.exists():
    raise FileExistsError(
        "refusing to overwrite periodic-3D nonorthogonal verification"
    )
if not all(
    path.is_file()
    for path in (
        calculation_script_path,
        execution_path,
        configuration_path,
        result_path,
    )
):
    raise FileNotFoundError(
        "the declared periodic-3D nonorthogonal execution is incomplete"
    )
execution_bytes = execution_path.read_bytes()
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
if (
    execution.script_sha256
    != hashlib.sha256(calculation_script_path.read_bytes()).hexdigest()
):
    raise ValueError("calculation script bytes do not match execution.json")
configuration_bytes = configuration_path.read_bytes()
result_bytes = result_path.read_bytes()
if execution.configuration_sha256 != hashlib.sha256(configuration_bytes).hexdigest():
    raise ValueError("configuration bytes do not match execution.json")
if execution.result_sha256 != hashlib.sha256(result_bytes).hexdigest():
    raise ValueError("result bytes do not match execution.json")
configuration = Periodic3DRank2BandEquivalenceHoppingLocalityRequest.from_json(
    configuration_bytes
)
result = Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult.from_json(result_bytes)
if configuration.to_json() != configuration_bytes or result.to_json() != result_bytes:
    raise ValueError("calculation artifacts are not canonical typed JSON")
if result.request.to_json() != configuration_bytes:
    raise ValueError("configuration and result request differ")
verified = Periodic3DRank2BandEquivalenceHoppingLocalityResultVerifier(
    result_wire=result_bytes,
    diagnostic_verifier=Periodic3DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier(
        request=configuration,
        result=result.diagnostics,
    ),
    shell_power_analyzer=Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer(
        request=configuration
    ),
    thresholds=VERIFICATION_THRESHOLDS,
).result()
if not verified.verification.passed:
    raise ValueError("periodic-3D nonorthogonal independent verification failed")
temporary_directory.mkdir()
verification_record = Periodic3DRank2BandEquivalenceHoppingLocalityExecutionVerification(
    schema_version=1,
    schema=(
        "ksdft2effmass.periodic3d-rank2-nonorthogonal-"
        "band-equivalence-locality-verification.direct.v1"
    ),
    calculation_family=CALCULATION_FAMILY,
    study_family=STUDY_FAMILY,
    execution_id=EXECUTION_ID,
    verification=verified.verification,
    visualization_data=verified.visualization_data,
    comparison_count=len(verified.verification.checks),
    result_sha256=hashlib.sha256(result_bytes).hexdigest(),
    script_sha256=hashlib.sha256(script_path.read_bytes()).hexdigest(),
    claim_boundary=(
        "Independent finite numerical verification of synthetic FCC-Bravais "
        "and diamond-basis controls only; not a silicon calculation, "
        "continuum convergence, uncertainty quantification, material "
        "validation, publication acceptance, or evidence sealing."
    ),
)
(temporary_directory / "verification.json").write_bytes(verification_record.to_json())
temporary_directory.rename(verification_directory)
