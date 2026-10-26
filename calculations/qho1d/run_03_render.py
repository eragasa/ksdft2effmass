#!/usr/bin/env python3
"""Render authenticated figures for one direct QHO1D execution."""

from __future__ import annotations

import hashlib
import inspect
import platform
import shutil
from collections.abc import Mapping
from pathlib import Path

import matplotlib
import numpy as np

from ksdft2effmass.model_systems.qho1d import (
    Qho1dVerification,
    Qho1dVisualizationData,
    Qho1dVisualizer,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-spatial-truncation-3x3x3-physkit-norms"

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
authored_report_directory = calculation_directory / "technical_report"
if figures_directory.exists() or execution_report_directory.exists():
    raise FileExistsError("refusing to overwrite an existing QHO1D rendering")
if temporary_figures_directory.exists() or temporary_report_directory.exists():
    raise FileExistsError("an incomplete QHO1D rendering stage already exists")
if not result_path.is_file() or not verification_path.is_file():
    raise FileNotFoundError("calculation and verification must precede rendering")
if not authored_report_directory.is_dir():
    raise FileNotFoundError("the authored QHO1D technical report is absent")

codec = TypedJsonValueCodec()
result_bytes = result_path.read_bytes()
result_sha256 = hashlib.sha256(result_bytes).hexdigest()
verification_bytes = verification_path.read_bytes()
verification_document = codec.deserialize_bytes(verification_bytes)
if not isinstance(verification_document, Mapping):
    raise TypeError("verification document must decode to a mapping")
if verification_document.get("execution_id") != EXECUTION_ID:
    raise ValueError("verification identity does not match the rendering target")
if verification_document.get("result_sha256") != result_sha256:
    raise ValueError("verified result SHA-256 differs from the result bytes")
verification_mapping = verification_document.get("verification")
visualization_mapping = verification_document.get("visualization_data")
if not isinstance(verification_mapping, Mapping):
    raise TypeError("verification must decode to a mapping")
if not isinstance(visualization_mapping, Mapping):
    raise TypeError("visualization_data must decode to a mapping")
verification = Qho1dVerification.from_dict(verification_mapping)
data = Qho1dVisualizationData.from_dict(visualization_mapping)
if verification.subject_sha256 != result_sha256:
    raise ValueError("verification authenticates different result bytes")
visualizer = Qho1dVisualizer(data=data, verification=verification)
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
visualizer_source_path = Path(inspect.getfile(Qho1dVisualizer)).resolve()
try:
    visualizer_source_locator = visualizer_source_path.relative_to(
        repository_root
    ).as_posix()
except ValueError:
    visualizer_source_locator = visualizer_source_path.as_posix()
rendering_document = {
    "schema": "ksdft2effmass.qho1d-rendering.v1",
    "execution_id": EXECUTION_ID,
    "outcome": "completed",
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
    "claim_boundary": (
        "Derived figures and report source from independently verified finite "
        "results; not new evidence, physical validation, or publication acceptance."
    ),
}
(temporary_figures_directory / "rendering.json").write_bytes(
    codec.serialize_bytes(rendering_document)
)
temporary_report_directory.rename(execution_report_directory)
temporary_figures_directory.rename(figures_directory)
