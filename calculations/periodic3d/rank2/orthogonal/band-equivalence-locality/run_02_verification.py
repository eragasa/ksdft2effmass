#!/usr/bin/env python3
"""Independently verify one direct orthogonal periodic-3D locality execution."""

from __future__ import annotations

import hashlib
from pathlib import Path

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.calculation import (
    BandEquivalenceLocalityVerifier,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (
    BandEquivalenceLocalityRequest,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.lifecycle import (
    BandEquivalenceLocalityExecution,
    BandEquivalenceLocalityExecutionVerification,
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
from projectkoios.physkit.units import ScalarQuantity, Unitless

EXECUTION_ID = "direct-simple-cubic-rank2-n8"
CALCULATION_FAMILY = "periodic3d-rank2-orthogonal-band-equivalence-locality"
STUDY_FAMILY = (
    "ksdft2effmass.campaign.model-adequacy.periodic3d."
    "band-equivalence-versus-hopping-locality"
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
    raise FileExistsError("refusing to overwrite periodic-3D locality verification")
if not all(
    path.is_file()
    for path in (
        calculation_script_path,
        execution_path,
        configuration_path,
        result_path,
    )
):
    raise FileNotFoundError("the declared periodic-3D locality execution is incomplete")
execution_bytes = execution_path.read_bytes()
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
configuration = BandEquivalenceLocalityRequest.from_json(configuration_bytes)
result = BandEquivalenceLocalityCalculationResult.from_json(result_bytes)
if configuration.to_json() != configuration_bytes or result.to_json() != result_bytes:
    raise ValueError("calculation artifacts are not canonical typed JSON")
if result.request.to_json() != configuration_bytes:
    raise ValueError("configuration and result request differ")
verified = BandEquivalenceLocalityResultVerifier(
    result_wire=result_bytes,
    diagnostic_verifier=BandEquivalenceLocalityVerifier(
        request=configuration,
        result=result.diagnostics,
    ),
    shell_power_analyzer=BandEquivalenceLocalityIndependentShellPowerAnalyzer(
        request=configuration
    ),
    thresholds=BandEquivalenceLocalityVerificationThresholds(
        stored_identity_maximum_defect=ScalarQuantity(5.0e-11, Unitless()),
        independent_parent_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
        independent_band_maximum_defect=ScalarQuantity(5.0e-14, Unitless()),
        independent_shell_power_maximum_defect=ScalarQuantity(
            5.0e-11,
            Unitless(),
        ),
    ),
).result()
if not verified.verification.passed:
    raise ValueError("periodic-3D locality independent verification failed")
temporary_directory.mkdir()
verification_record = BandEquivalenceLocalityExecutionVerification(
    schema_version=1,
    schema=(
        "ksdft2effmass.periodic3d-rank2-orthogonal-"
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
        "Independent finite numerical verification only; not continuum "
        "convergence, uncertainty quantification, material validation, "
        "publication acceptance, or evidence sealing."
    ),
)
(temporary_directory / "verification.json").write_bytes(verification_record.to_json())
temporary_directory.rename(verification_directory)
