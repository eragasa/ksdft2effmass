#!/usr/bin/env python3
"""Calculate one direct controlled rank-two composite-alignment execution."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)

from ksdft2effmass.periodic1d.gauge_alignment.factory import (
    Periodic1DAlignmentStudyFactory,
    Periodic1DRank2AlignmentStudySpecification,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
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
configuration = Periodic1DCompositeBandAlignmentConfiguration.frozen()
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
temporary_directory = execution_directory.with_name(f".{EXECUTION_ID}.incomplete")
if execution_directory.exists() or temporary_directory.exists():
    raise FileExistsError("refusing to overwrite a composite-alignment execution")
lattice_geometry = configuration.reduced_lattice_geometry
study = Periodic1DAlignmentStudyFactory(
    Periodic1DRank2AlignmentStudySpecification(
        lattice_geometry=lattice_geometry,
        configuration=configuration,
        procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
    )
).create()
result = study.execute()
configuration_bytes = configuration.to_json()
result_bytes = result.to_json()
if (
    Periodic1DCompositeBandAlignmentConfiguration.from_json(
        configuration_bytes
    ).to_json()
    != configuration_bytes
):
    raise ValueError("configuration failed canonical typed admission")
if (
    Periodic1DCompositeBandAlignmentCalculationResult.from_json(result_bytes).to_json()
    != result_bytes
):
    raise ValueError("result failed canonical typed admission")
(temporary_directory / "inputs").mkdir(parents=True)
(temporary_directory / "results").mkdir()
(temporary_directory / "inputs" / "configuration.json").write_bytes(configuration_bytes)
(temporary_directory / "results" / "result.json").write_bytes(result_bytes)
(temporary_directory / "execution.json").write_bytes(
    TypedJsonValueCodec().serialize_bytes(
        {
            "schema_version": 2,
            "result_schema": RESULT_SCHEMA,
            "calculation_family": CALCULATION_FAMILY,
            "parent_identity": configuration.parent_identity,
            "execution_id": EXECUTION_ID,
            "lattice_geometry": {
                "lattice_period": lattice_geometry.lattice_period,
                "lattice_unit": lattice_geometry.lattice_unit,
            },
            "created_utc": datetime.now(UTC).isoformat(),
            "outcome": "completed",
            "evidence_status": "illustrative finite numerical control",
            "configuration_path": "inputs/configuration.json",
            "configuration_sha256": hashlib.sha256(configuration_bytes).hexdigest(),
            "result_path": "results/result.json",
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
            "software_versions": {
                "ksdft2effmass": version("ksdft2effmass"),
                "numpy": version("numpy"),
                "projectkoios-optimization": version("projectkoios-optimization"),
                "projectkoios-physkit": version("projectkoios-physkit"),
                "scipy": version("scipy"),
            },
            "claim_boundary": (
                "Finite sampled four-state parent, rank-two frame alignment, block "
                "Fourier transform, and truncation diagnostics only; not continuum "
                "isolation, uncertainty quantification, material validation, "
                "publication acceptance, or sealed evidence."
            ),
            "sealed": False,
        }
    )
)
(temporary_directory / "UNSEALED.md").write_text(
    "# Unsealed composite-band alignment execution\n\n"
    "This is an illustrative finite numerical control, not sealed evidence.\n",
    encoding="utf-8",
)
temporary_directory.rename(execution_directory)
