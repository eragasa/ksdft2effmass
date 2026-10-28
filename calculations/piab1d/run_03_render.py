#!/usr/bin/env python3
"""Render verified figures for one direct PIAB1D execution."""

from __future__ import annotations

import hashlib
import inspect
import platform
from collections.abc import Mapping
from pathlib import Path

import matplotlib
import numpy as np

from ksdft2effmass.model_systems.piab1d import (
    Piab1dVerification,
    Piab1dVerifier,
    Piab1dVisualizationData,
    Piab1dVisualizer,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-core-n8-m3"

script_path = Path(__file__).resolve()
repository_root = script_path.parents[2]
execution_directory = script_path.parent / "executions" / EXECUTION_ID
result_path = execution_directory / "results" / "result.json"
verification_path = execution_directory / "verification" / "verification.json"
figures_directory = execution_directory / "figures"
temporary_figures_directory = execution_directory / ".figures.incomplete"
if figures_directory.exists():
    raise FileExistsError(f"refusing to overwrite {figures_directory}")
if temporary_figures_directory.exists():
    raise FileExistsError(
        f"incomplete rendering stage exists: {temporary_figures_directory}"
    )
if not result_path.is_file() or not verification_path.is_file():
    raise FileNotFoundError("calculation and verification must precede rendering")

codec = TypedJsonValueCodec()
result_bytes = result_path.read_bytes()
result_sha256 = hashlib.sha256(result_bytes).hexdigest()
result = codec.deserialize_bytes(result_bytes)
verification_bytes = verification_path.read_bytes()
verification_document = codec.deserialize_bytes(verification_bytes)
if not isinstance(result, Mapping) or not isinstance(verification_document, Mapping):
    raise TypeError("result and verification documents must decode to mappings")
if result.get("execution_id") != EXECUTION_ID:
    raise ValueError("result identity does not match the rendering target")
if verification_document.get("execution_id") != EXECUTION_ID:
    raise ValueError("verification identity does not match the rendering target")
verification_mapping = verification_document.get("verification")
if not isinstance(verification_mapping, Mapping):
    raise TypeError("verification document must contain a verification mapping")
verification = Piab1dVerification.from_dict(verification_mapping)
if not verification.passed:
    raise ValueError("rendering requires a passing verification record")
recorded_result_sha256 = verification_document.get("result_sha256")
if type(recorded_result_sha256) is not str:
    raise TypeError("verification result_sha256 must be a built-in string")
if recorded_result_sha256 != result_sha256:
    raise ValueError("verified result SHA-256 does not match the result bytes")
if verification.subject_sha256 != result_sha256:
    raise ValueError("verification value is bound to different result bytes")

visualization_mapping = verification_document.get("visualization_data")
if not isinstance(visualization_mapping, Mapping):
    raise TypeError("verification must contain visualization_data")
data = Piab1dVisualizationData.from_dict(visualization_mapping)
admitted = Piab1dVerifier(result_wire=result_bytes).admit_stored(
    verification=verification,
    visualization_data=data,
)
verification = admitted.verification
data = admitted.visualization_data
visualizer = Piab1dVisualizer(data=data, verification=verification)
visualizations = visualizer.visualize()
if {item.plot for item in visualizations} != set(visualizer.plots):
    raise RuntimeError("visualizer did not produce its declared plot inventory")

# Write every figure and its manifest behind an incomplete-stage name. The final
# rename exposes either the complete authenticated set or no published set.
temporary_figures_directory.mkdir()
output_paths = {
    visualization.plot: temporary_figures_directory / visualization.filename
    for visualization in visualizations
}
for visualization in visualizations:
    output_paths[visualization.plot].write_bytes(visualization.png)

visualizer_source_path = Path(inspect.getfile(Piab1dVisualizer)).resolve()
try:
    recorded_visualizer_source_path = visualizer_source_path.relative_to(
        repository_root
    ).as_posix()
except ValueError:
    recorded_visualizer_source_path = visualizer_source_path.as_posix()
rendering_document = {
    "schema": "ksdft2effmass.piab1d-rendering.v1",
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
    "script_path": script_path.relative_to(repository_root).as_posix(),
    "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
    "visualizer_source_path": recorded_visualizer_source_path,
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
        "Derived figures from one independently verified finite-dimensional "
        "illustrative result; not material validation or publication acceptance."
    ),
}
(temporary_figures_directory / "rendering.json").write_bytes(
    codec.serialize_bytes(rendering_document)
)
# The destination was rejected above, so this same-filesystem rename is atomic.
temporary_figures_directory.rename(figures_directory)
