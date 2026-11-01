#!/usr/bin/env python3
"""Independently verify one direct rank-two composite-alignment execution."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.verification import (
    Periodic1DCompositeBandAlignmentVerifier,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-controlled-rank2-n64-v2"
CALCULATION_FAMILY = (
    Periodic1DCompositeBandAlignmentCalculationResult.CALCULATION_FAMILY
)
RESULT_SCHEMA = Periodic1DCompositeBandAlignmentCalculationResult.RESULT_SCHEMA
PARENT_IDENTITY = Periodic1DCompositeBandAlignmentConfiguration.PARENT_IDENTITY
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
execution_path = execution_directory / "execution.json"
configuration_path = execution_directory / "inputs" / "configuration.json"
result_path = execution_directory / "results" / "result.json"
verification_directory = execution_directory / "verification"
temporary_directory = execution_directory / ".verification.incomplete"
if verification_directory.exists() or temporary_directory.exists():
    raise FileExistsError("refusing to overwrite composite-alignment verification")
if not all(
    path.is_file() for path in (execution_path, configuration_path, result_path)
):
    raise FileNotFoundError("the declared composite-alignment execution is incomplete")
codec = TypedJsonValueCodec()
execution = codec.deserialize_bytes(execution_path.read_bytes())
if not isinstance(execution, Mapping):
    raise TypeError("execution document must decode to a mapping")
if execution.get("execution_id") != EXECUTION_ID:
    raise ValueError("execution identifier does not match")
if execution.get("result_schema") != RESULT_SCHEMA:
    raise ValueError("result schema does not match")
if execution.get("calculation_family") != CALCULATION_FAMILY:
    raise ValueError("calculation family does not match")
if execution.get("parent_identity") != PARENT_IDENTITY:
    raise ValueError("parent identity does not match")
lattice_geometry_mapping = execution.get("lattice_geometry")
if not isinstance(lattice_geometry_mapping, Mapping):
    raise TypeError("execution lattice geometry must decode to a mapping")
lattice_period = lattice_geometry_mapping.get("lattice_period")
lattice_unit = lattice_geometry_mapping.get("lattice_unit")
if type(lattice_period) is not float:
    raise TypeError("execution lattice period must decode to a built-in float")
if type(lattice_unit) is not PhysicalUnit:
    raise TypeError("execution lattice unit must decode to PhysicalUnit")
lattice_geometry = Periodic1DLatticeGeometry(lattice_period, lattice_unit)
configuration_bytes = configuration_path.read_bytes()
result_bytes = result_path.read_bytes()
if (
    execution.get("configuration_sha256")
    != hashlib.sha256(configuration_bytes).hexdigest()
):
    raise ValueError("configuration bytes do not match execution.json")
if execution.get("result_sha256") != hashlib.sha256(result_bytes).hexdigest():
    raise ValueError("result bytes do not match execution.json")
configuration = Periodic1DCompositeBandAlignmentConfiguration.from_json(
    configuration_bytes
)
result = Periodic1DCompositeBandAlignmentCalculationResult.from_json(result_bytes)
if configuration.to_json() != configuration_bytes or result.to_json() != result_bytes:
    raise ValueError("calculation artifacts are not canonical typed JSON")
if result.configuration.to_json() != configuration_bytes:
    raise ValueError("configuration and result configuration differ")
if lattice_geometry != configuration.reduced_lattice_geometry:
    raise ValueError("execution lattice geometry does not match the study convention")
if result.configuration.parent_identity != execution.get("parent_identity"):
    raise ValueError("result and execution parent identities differ")
verified = Periodic1DCompositeBandAlignmentVerifier(result_wire=result_bytes).result()
temporary_directory.mkdir()
(temporary_directory / "verification.json").write_bytes(
    codec.serialize_bytes(
        {
            "schema_version": 2,
            "schema": (
                "ksdft2effmass.periodic1d-composite-band-alignment-verification."
                "direct.v2"
            ),
            "result_schema": RESULT_SCHEMA,
            "calculation_family": CALCULATION_FAMILY,
            "parent_identity": result.configuration.parent_identity,
            "execution_id": EXECUTION_ID,
            "lattice_geometry": {
                "lattice_period": lattice_geometry.lattice_period,
                "lattice_unit": lattice_geometry.lattice_unit,
            },
            "verification": verified.verification,
            "visualization_data": verified.visualization_data,
            "comparison_count": len(verified.verification.checks),
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
            "claim_boundary": (
                "Independent finite numerical verification only; not continuum "
                "isolation, uncertainty quantification, material validation, "
                "publication acceptance, or evidence sealing."
            ),
        }
    )
)
temporary_directory.rename(verification_directory)
if not verified.verification.passed:
    raise ValueError("composite-alignment independent verification failed")
