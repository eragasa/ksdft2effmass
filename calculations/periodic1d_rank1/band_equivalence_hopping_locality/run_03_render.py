#!/usr/bin/env python3
"""Render authenticated outputs for one rank-one Fourier-locality execution."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from pathlib import Path

from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityVerification,
    Periodic1DFourierLocalityVerifier,
    Periodic1DFourierLocalityVisualizationData,
    Periodic1DFourierLocalityVisualizer,
)
from ksdft2effmass.serialization import TypedJsonValueCodec

EXECUTION_ID = "direct-controlled-four-state-n256"
CALCULATION_FAMILY = "periodic1d-rank1-fourier-locality"
script_path = Path(__file__).resolve()
execution_directory = script_path.parent / "executions" / EXECUTION_ID
result_path = execution_directory / "results" / "result.json"
verification_path = execution_directory / "verification" / "verification.json"
figures_directory = execution_directory / "figures"
temporary_directory = execution_directory / ".figures.incomplete"
if figures_directory.exists() or temporary_directory.exists():
    raise FileExistsError("refusing to overwrite Fourier-locality rendering")
if not result_path.is_file() or not verification_path.is_file():
    raise FileNotFoundError("calculation and verification must precede rendering")
codec = TypedJsonValueCodec()
result_bytes = result_path.read_bytes()
verification_bytes = verification_path.read_bytes()
document = codec.deserialize_bytes(verification_bytes)
if not isinstance(document, Mapping):
    raise TypeError("verification document must decode to a mapping")
if codec.serialize_bytes(document) != verification_bytes:
    raise ValueError("verification document is not canonical typed JSON")
if document.get("execution_id") != EXECUTION_ID:
    raise ValueError("verification execution identifier does not match")
if document.get("calculation_family") != CALCULATION_FAMILY:
    raise ValueError("verification calculation family does not match")
if document.get("parent_identity") != (
    "ksdft2effmass.periodic1d.controlled-four-state-parent.v1"
):
    raise ValueError("verification parent identity does not match")
if document.get("result_sha256") != hashlib.sha256(result_bytes).hexdigest():
    raise ValueError("verification authenticates different result bytes")
verification_mapping = document.get("verification")
visualization_mapping = document.get("visualization_data")
if not isinstance(verification_mapping, Mapping):
    raise TypeError("verification aggregate must decode to a mapping")
if not isinstance(visualization_mapping, Mapping):
    raise TypeError("visualization data must decode to a mapping")
verification = Periodic1DFourierLocalityVerification.from_dict(verification_mapping)
data = Periodic1DFourierLocalityVisualizationData.from_dict(visualization_mapping)
admitted = Periodic1DFourierLocalityVerifier(result_wire=result_bytes).admit_stored(
    verification=verification,
    visualization_data=data,
)
visualizer = Periodic1DFourierLocalityVisualizer(
    data=admitted.visualization_data,
    verification=admitted.verification,
)
visualizations = visualizer.visualize()
temporary_directory.mkdir()
for visualization in visualizations:
    (temporary_directory / visualization.filename).write_bytes(visualization.png)
(temporary_directory / "rendering.json").write_bytes(
    codec.serialize_bytes(
        {
            "schema_version": 1,
            "schema": "ksdft2effmass.periodic1d-fourier-locality-rendering.direct.v1",
            "calculation_family": CALCULATION_FAMILY,
            "parent_identity": document["parent_identity"],
            "execution_id": EXECUTION_ID,
            "outcome": "completed",
            "verification_sha256": hashlib.sha256(verification_bytes).hexdigest(),
            "figures": {
                visualization.filename: hashlib.sha256(visualization.png).hexdigest()
                for visualization in visualizations
            },
            "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
            "claim_boundary": (
                "Presentation only from independently verified finite values; not "
                "new evidence, publication acceptance, or evidence sealing."
            ),
        }
    )
)
temporary_directory.rename(figures_directory)
