#!/usr/bin/env python3
"""Render provisional authenticated composite-alignment report illustrations."""

from __future__ import annotations

import hashlib
from pathlib import Path

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)

from ksdft2effmass.periodic1d.rank2.band_alignment.composite import (
    Periodic1DCompositeBandAlignmentAnalyzer,
    Periodic1DCompositeBandAlignmentConfiguration,
    Periodic1DCompositeBandAlignmentVerifier,
    Periodic1DCompositeBandAlignmentVisualizationPlotEnum,
    Periodic1DCompositeBandAlignmentVisualizer,
)


def configuration() -> Periodic1DCompositeBandAlignmentConfiguration:
    """Return the exact frozen direct rank-two request."""
    configuration_type = Periodic1DCompositeBandAlignmentConfiguration
    return configuration_type(
        parent_identity=configuration_type.PARENT_IDENTITY,
        onsite_numerators=configuration_type.PARENT_ONSITE_NUMERATORS,
        positive_hopping_numerators=(
            configuration_type.PARENT_POSITIVE_HOPPING_NUMERATORS
        ),
        coefficient_denominator=configuration_type.PARENT_COEFFICIENT_DENOMINATOR,
        retained_rank=2,
        construction_size=64,
        evaluation_size=257,
        evaluation_shift_numerator=1,
        evaluation_shift_denominator=65,
        hopping_ranges=configuration_type.HOPPING_RANGES,
        attack_constant_angle=0.30,
        attack_sine_coefficients=(0.65, 0.30),
        sampled_gap_threshold=0.5,
        overlap_singular_value_threshold=0.8,
        procrustes_rank_absolute_tolerance=1.0e-14,
        procrustes_rank_relative_tolerance=1.0e-12,
        energy_absolute_tolerance=1.0e-11,
        dimensionless_absolute_tolerance=1.0e-12,
    )


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
