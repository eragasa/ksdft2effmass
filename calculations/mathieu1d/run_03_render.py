#!/usr/bin/env python3
"""Render authenticated outputs for one direct Mathieu1D execution."""

from __future__ import annotations

import hashlib
import inspect
import platform
import shutil
from collections.abc import Mapping
from pathlib import Path

import matplotlib
import numpy as np

from ksdft2effmass.model_systems.mathieu1d import (
    Mathieu1dVerification,
    Mathieu1dVerifier,
    Mathieu1dVisualizationData,
    Mathieu1dVisualizer,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-finite-reduction-n64"
CALCULATION_FAMILY = "mathieu1d-finite-reduction"
EVIDENCE_STATUS = "illustrative numerical experiment"
CLAIM_BOUNDARY = (
    "Presentation derived only from independently verified finite Mathieu1D values; "
    "not new evidence, continuum convergence, uncertainty quantification, material "
    "validation, publication acceptance, or evidence sealing."
)
VERIFICATION_CLAIM_BOUNDARY = (
    "Independent software and finite numerical verification only; not continuum "
    "convergence, uncertainty quantification, material validation, publication "
    "acceptance, or evidence sealing."
)
VERIFICATION_ROUTE = (
    "independent direct assembly of dense plane-wave fibers and sparse twisted "
    "finite-difference fibers, explicit finite Fourier sums, and NumPy weighted "
    "least squares without production analyzers or historical workflows"
)

script_path = Path(__file__).resolve()
repository_root = script_path.parents[2]
calculation_directory = script_path.parent
execution_directory = calculation_directory / "executions" / EXECUTION_ID
result_path = execution_directory / "results" / "result.json"
verification_path = execution_directory / "verification" / "verification.json"
figures_directory = execution_directory / "figures"
temporary_figures_directory = execution_directory / ".figures.incomplete"
execution_report_directory = execution_directory / "technical_report"
temporary_report_directory = execution_directory / ".technical_report.incomplete"
authored_report_directory = calculation_directory / "technical-report"
verification_script_path = calculation_directory / "run_02_verification.py"
if figures_directory.exists() or execution_report_directory.exists():
    raise FileExistsError("refusing to overwrite an existing Mathieu1D rendering")
if temporary_figures_directory.exists() or temporary_report_directory.exists():
    raise FileExistsError("an incomplete Mathieu1D rendering stage already exists")
if not result_path.is_file() or not verification_path.is_file():
    raise FileNotFoundError("calculation and verification must precede rendering")
if not authored_report_directory.is_dir():
    raise FileNotFoundError("the authored Mathieu1D technical report is absent")
required_report_sources = {
    "README.md",
    "technical-report.tex",
    "technical-report.pdf",
}
if not required_report_sources <= {
    path.name for path in authored_report_directory.iterdir() if path.is_file()
}:
    raise FileNotFoundError("the buildable Mathieu1D technical report is incomplete")
if (
    not (authored_report_directory / "technical-report.pdf")
    .read_bytes()
    .startswith(b"%PDF-")
):
    raise ValueError("the maintained Mathieu1D technical report is not a PDF")
if not verification_script_path.is_file():
    raise FileNotFoundError("the Mathieu1D verification script is absent")

codec = TypedJsonValueCodec()
result_bytes = result_path.read_bytes()
result_sha256 = hashlib.sha256(result_bytes).hexdigest()
verification_bytes = verification_path.read_bytes()
verification_document = codec.deserialize_bytes(verification_bytes)
if not isinstance(verification_document, Mapping):
    raise TypeError("verification document must decode to a mapping")
if codec.serialize_bytes(verification_document) != verification_bytes:
    raise ValueError("verification document is not canonical typed JSON")
if set(verification_document) != {
    "schema_version",
    "schema",
    "calculation_family",
    "execution_id",
    "evidence_status",
    "verification_route",
    "verification",
    "visualization_data",
    "comparison_count",
    "claim_boundary",
    "result_sha256",
    "script_sha256",
}:
    raise ValueError("verification document fields do not match")
if verification_document.get("schema_version") != 1:
    raise ValueError("verification declares an unexpected schema version")
if verification_document.get("execution_id") != EXECUTION_ID:
    raise ValueError("verification identifier does not match the rendering target")
if verification_document.get("calculation_family") != CALCULATION_FAMILY:
    raise ValueError("verification declares an unexpected calculation family")
if verification_document.get("evidence_status") != EVIDENCE_STATUS:
    raise ValueError("verification declares an unexpected evidence status")
if verification_document.get("schema") != (
    "ksdft2effmass.mathieu1d-verification.direct.v1"
):
    raise ValueError("verification declares an unexpected schema")
if verification_document.get("verification_route") != VERIFICATION_ROUTE:
    raise ValueError("verification declares an unexpected independent route")
if verification_document.get("claim_boundary") != VERIFICATION_CLAIM_BOUNDARY:
    raise ValueError("verification declares an unexpected claim boundary")
if (
    verification_document.get("script_sha256")
    != hashlib.sha256(verification_script_path.read_bytes()).hexdigest()
):
    raise ValueError("verification script digest does not match its source")
if verification_document.get("result_sha256") != result_sha256:
    raise ValueError("verified result SHA-256 differs from the result bytes")
verification_mapping = verification_document.get("verification")
visualization_mapping = verification_document.get("visualization_data")
if not isinstance(verification_mapping, Mapping):
    raise TypeError("verification must decode to a mapping")
if not isinstance(visualization_mapping, Mapping):
    raise TypeError("visualization_data must decode to a mapping")
verification = Mathieu1dVerification.from_dict(verification_mapping)
data = Mathieu1dVisualizationData.from_dict(visualization_mapping)
if verification.subject_sha256 != result_sha256:
    raise ValueError("verification authenticates different result bytes")
if not verification.passed:
    raise ValueError("rendering requires passing independent verification")
admitted = Mathieu1dVerifier(result_wire=result_bytes).admit_stored(
    verification=verification,
    visualization_data=data,
)
verification = admitted.verification
data = admitted.visualization_data
if verification_document.get("comparison_count") != len(verification.checks):
    raise ValueError("verification comparison count does not match the aggregate")
visualizer = Mathieu1dVisualizer(data=data, verification=verification)
visualizations = visualizer.visualize()
if {item.plot for item in visualizations} != set(visualizer.plots):
    raise RuntimeError("visualizer did not produce its declared plot inventory")

temporary_figures_directory.mkdir()
output_paths = {
    visualization.plot: temporary_figures_directory / visualization.filename
    for visualization in visualizations
}
for visualization in visualizations:
    output_paths[visualization.plot].write_bytes(visualization.png)

temporary_report_directory.mkdir()
for source in authored_report_directory.iterdir():
    if source.is_file() and source.suffix in {".tex", ".bib", ".md", ".pdf"}:
        shutil.copy2(source, temporary_report_directory / source.name)
for visualization in visualizations:
    (temporary_report_directory / visualization.filename).write_bytes(visualization.png)
visualizer_source_path = Path(inspect.getfile(Mathieu1dVisualizer)).resolve()
try:
    visualizer_source_locator = visualizer_source_path.relative_to(
        repository_root
    ).as_posix()
except ValueError:
    visualizer_source_locator = visualizer_source_path.as_posix()
rendering_document = {
    "schema": "ksdft2effmass.mathieu1d-rendering.direct.v1",
    "calculation_family": CALCULATION_FAMILY,
    "execution_id": EXECUTION_ID,
    "outcome": "completed",
    "evidence_status": EVIDENCE_STATUS,
    "result_path": result_path.relative_to(repository_root).as_posix(),
    "result_sha256": result_sha256,
    "verification_path": verification_path.relative_to(repository_root).as_posix(),
    "verification_sha256": hashlib.sha256(verification_bytes).hexdigest(),
    "figures": {
        path.name: {
            "media_type": "image/png",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in sorted(output_paths.values())
    },
    "technical_report": {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(temporary_report_directory.iterdir())
    },
    "script_path": script_path.relative_to(repository_root).as_posix(),
    "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
    "visualizer_source_path": visualizer_source_locator,
    "visualizer_source_sha256": hashlib.sha256(
        visualizer_source_path.read_bytes()
    ).hexdigest(),
    "runtime": {
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "matplotlib_version": matplotlib.__version__,
        "matplotlib_backend": str(matplotlib.get_backend()),
    },
    "claim_boundary": CLAIM_BOUNDARY,
}
(temporary_figures_directory / "rendering.json").write_bytes(
    codec.serialize_bytes(rendering_document)
)
temporary_report_directory.rename(execution_report_directory)
temporary_figures_directory.rename(figures_directory)
