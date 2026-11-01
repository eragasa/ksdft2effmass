"""Shared frozen rank-two composite-alignment test values."""

import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)

from ksdft2effmass.periodic1d.rank2.band_alignment.composite.analysis import (
    Periodic1DCompositeBandAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)


@pytest.fixture(scope="session")
def composite_configuration() -> Periodic1DCompositeBandAlignmentConfiguration:
    """Return the exact frozen direct composite-alignment request."""
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


@pytest.fixture(scope="session")
def composite_result(
    composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
) -> Periodic1DCompositeBandAlignmentCalculationResult:
    """Calculate the frozen finite control once for the bounded test session."""
    analyzer = Periodic1DCompositeBandAlignmentAnalyzer(
        composite_configuration,
        NumpyBatchedComplexUnitaryProcrustesSolver(),
    )
    assert analyzer.request is composite_configuration
    return analyzer.execute()
