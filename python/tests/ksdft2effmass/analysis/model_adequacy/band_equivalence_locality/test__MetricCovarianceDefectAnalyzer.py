"""Software contracts for the family-owned metric-covariance probe."""

from dataclasses import FrozenInstanceError
from enum import Enum
from typing import cast

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    DirectLattice3D,
    DirectLatticeMetric,
)

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityMetricCovarianceDefectAnalyzer,
    BandEquivalenceLocalityMetricCovarianceDefectResult,
    BandEquivalenceLocalityMetricCovarianceProbeEnum,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.numerical_consistency import NumericalConsistency
from ksdft2effmass.real_space_support_truncation import MetricGeometry

pytestmark = pytest.mark.software_verification


def _orthogonal_case(dimension: int) -> BandEquivalenceLocalityCase:
    direct_metric: DirectLatticeMetric
    positive_bonds: tuple[tuple[int, ...], ...]
    if dimension == 2:
        direct_metric = DirectLatticeMetric(
            DirectLattice2D(
                a1=np.asarray((1.0, 0.0), dtype=np.float64),
                a2=np.asarray((0.0, 1.0), dtype=np.float64),
            )
        )
        positive_bonds = ((1, 0), (0, 1))
    elif dimension == 3:
        direct_metric = DirectLatticeMetric(
            DirectLattice3D(
                a1=np.asarray((1.0, 0.0, 0.0), dtype=np.float64),
                a2=np.asarray((0.0, 1.0, 0.0), dtype=np.float64),
                a3=np.asarray((0.0, 0.0, 1.0), dtype=np.float64),
            )
        )
        positive_bonds = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    else:
        raise ValueError("test dimension must be two or three")
    return BandEquivalenceLocalityCase(
        name=f"orthogonal-{dimension}d-covariance-control",
        dimension=dimension,
        parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
        gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
        positive_bonds=positive_bonds,
        direct_metric=direct_metric,
        shell_metric_scale=1.0,
    )


class TestBandEquivalenceLocalityMetricCovarianceDefectAnalyzer:
    """Establish typed probe identity, execution, and immutability."""

    def test_probe_enum__round_trips_stable_mapping_strings(self) -> None:
        assert issubclass(BandEquivalenceLocalityMetricCovarianceProbeEnum, Enum)
        assert not issubclass(BandEquivalenceLocalityMetricCovarianceProbeEnum, str)
        for probe in BandEquivalenceLocalityMetricCovarianceProbeEnum:
            wire = probe.to_wire()
            assert type(wire) is str
            assert (
                BandEquivalenceLocalityMetricCovarianceProbeEnum.from_wire(wire)
                is probe
            )
        with pytest.raises(TypeError, match="built-in string"):
            BandEquivalenceLocalityMetricCovarianceProbeEnum.from_wire(cast(str, True))
        with pytest.raises(ValueError, match="unsupported"):
            BandEquivalenceLocalityMetricCovarianceProbeEnum.from_wire("unknown")

    @pytest.mark.parametrize(
        ("dimension", "expected_probe"),
        (
            (
                2,
                BandEquivalenceLocalityMetricCovarianceProbeEnum.PRIMITIVE_BASIS_SHEAR_2D_V1,
            ),
            (
                3,
                BandEquivalenceLocalityMetricCovarianceProbeEnum.PRIMITIVE_BASIS_SHEAR_3D_V1,
            ),
        ),
    )
    def test_execute__selects_dimensional_probe_without_changing_case_bytes(
        self,
        dimension: int,
        expected_probe: BandEquivalenceLocalityMetricCovarianceProbeEnum,
    ) -> None:
        case = _orthogonal_case(dimension)
        wire = case.to_json()

        result = BandEquivalenceLocalityMetricCovarianceDefectAnalyzer(case).execute()

        assert type(result) is BandEquivalenceLocalityMetricCovarianceDefectResult
        assert isinstance(result, NumericalConsistency)
        assert result.probe is expected_probe
        assert result.maximum_absolute_defect == pytest.approx(0.0, abs=1.0e-15)
        assert case.to_json() == wire

    def test_result__is_immutable_and_rejects_invalid_values(self) -> None:
        result = BandEquivalenceLocalityMetricCovarianceDefectResult(
            probe=(
                BandEquivalenceLocalityMetricCovarianceProbeEnum.PRIMITIVE_BASIS_SHEAR_2D_V1
            ),
            maximum_absolute_defect=0.0,
        )
        with pytest.raises(FrozenInstanceError):
            result.maximum_absolute_defect = 1.0  # type: ignore[misc]
        with pytest.raises(TypeError, match="probe"):
            BandEquivalenceLocalityMetricCovarianceDefectResult(
                probe=cast(BandEquivalenceLocalityMetricCovarianceProbeEnum, "probe"),
                maximum_absolute_defect=0.0,
            )
        with pytest.raises(TypeError, match="built-in float"):
            BandEquivalenceLocalityMetricCovarianceDefectResult(
                probe=result.probe,
                maximum_absolute_defect=cast(float, True),
            )
        with pytest.raises(ValueError, match="finite and nonnegative"):
            BandEquivalenceLocalityMetricCovarianceDefectResult(
                probe=result.probe,
                maximum_absolute_defect=float("nan"),
            )

    def test_init__rejects_non_nominal_geometry(self) -> None:
        with pytest.raises(TypeError, match="inherit MetricGeometry"):
            BandEquivalenceLocalityMetricCovarianceDefectAnalyzer(
                cast(MetricGeometry, object())
            )
