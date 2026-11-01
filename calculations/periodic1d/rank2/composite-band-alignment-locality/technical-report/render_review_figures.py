#!/usr/bin/env python3
"""Render provisional verified composite-alignment report figures."""

from __future__ import annotations

import hashlib
from pathlib import Path

from ksdft2effmass.periodic1d.rank2.band_alignment.composite.analysis import (
    Periodic1DCompositeBandAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.verification import (
    Periodic1DCompositeBandAlignmentVerifier,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.visualizations.inventory import (
    Periodic1DCompositeBandAlignmentVisualizationPlotEnum,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.visualizations.visualizer import (
    Periodic1DCompositeBandAlignmentVisualizer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)


def configuration() -> Periodic1DCompositeBandAlignmentConfiguration:
    """Return the exact frozen direct rank-two request."""
    return Periodic1DCompositeBandAlignmentConfiguration.frozen()


def main() -> int:
    """Calculate, independently verify, and render all report figures in memory."""
    report_root = Path(__file__).resolve().parent
    request = configuration()
    result = Periodic1DCompositeBandAlignmentAnalyzer(
        request,
        NumpyBatchedComplexUnitaryProcrustesSolver(),
    ).execute()
    verified = Periodic1DCompositeBandAlignmentVerifier(
        result_wire=result.to_json()
    ).result()
    if not verified.verification.passed:
        raise ValueError("report figures require passing independent verification")
    visualizations = Periodic1DCompositeBandAlignmentVisualizer(
        data=verified.visualization_data,
        verification=verified.verification,
        dpi=160,
    ).visualize()
    if {value.plot for value in visualizations} != set(
        Periodic1DCompositeBandAlignmentVisualizationPlotEnum
    ):
        raise ValueError("renderer did not return the closed report figure inventory")
    for visualization in visualizations:
        destination = report_root / visualization.plot.value
        destination.write_bytes(visualization.png)
        digest = hashlib.sha256(visualization.png).hexdigest()
        print(f"{visualization.plot.value}  {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
