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

from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityCase,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.band_equivalence_hopping_locality.geometry import (
    BandEquivalenceHoppingLocalityMetricCovarianceDefectAnalyzer,
    BandEquivalenceHoppingLocalityMetricCovarianceDefectResult,
    BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum,
)
from ksdft2effmass.numerical_consistency import NumericalConsistency
from ksdft2effmass.real_space_support_truncation import MetricGeometry

pytestmark = pytest.mark.software_verification


def _orthogonal_case(dimension: int) -> BandEquivalenceHoppingLocalityCase:
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
    return BandEquivalenceHoppingLocalityCase(
        name=f"orthogonal-{dimension}d-covariance-control",
        dimension=dimension,
        parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
        gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
        positive_bonds=positive_bonds,
        direct_metric=direct_metric,
        shell_metric_scale=1.0,
    )


class TestBandEquivalenceHoppingLocalityMetricCovarianceDefectAnalyzer:
    """Establish typed probe identity, execution, and immutability."""

    def test_probe_enum__round_trips_stable_mapping_strings(self) -> None:
        assert issubclass(BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum, Enum)
        assert not issubclass(
            BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum, str
        )
        for probe in BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum:
            wire = probe.to_wire()
            assert type(wire) is str
            assert (
                BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum.from_wire(wire)
                is probe
            )
        with pytest.raises(TypeError, match="built-in string"):
            BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum.from_wire(
                cast(str, True)
            )
        with pytest.raises(ValueError, match="unsupported"):
            BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum.from_wire("unknown")

    @pytest.mark.parametrize(
        ("dimension", "expected_probe"),
        (
            (
                2,
                BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum.PRIMITIVE_BASIS_SHEAR_2D_V1,
            ),
            (
                3,
                BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum.PRIMITIVE_BASIS_SHEAR_3D_V1,
            ),
        ),
    )
    def test_execute__selects_dimensional_probe_without_changing_case_bytes(
        self,
        dimension: int,
        expected_probe: BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum,
    ) -> None:
        case = _orthogonal_case(dimension)
        wire = case.to_json()

        result = BandEquivalenceHoppingLocalityMetricCovarianceDefectAnalyzer(
            case
        ).execute()

        assert (
            type(result) is BandEquivalenceHoppingLocalityMetricCovarianceDefectResult
        )
        assert isinstance(result, NumericalConsistency)
        assert result.probe is expected_probe
        assert result.maximum_absolute_defect == pytest.approx(0.0, abs=1.0e-15)
        assert case.to_json() == wire

    def test_result__is_immutable_and_rejects_invalid_values(self) -> None:
        result = BandEquivalenceHoppingLocalityMetricCovarianceDefectResult(
            probe=(
                BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum.PRIMITIVE_BASIS_SHEAR_2D_V1
            ),
            maximum_absolute_defect=0.0,
        )
        with pytest.raises(FrozenInstanceError):
            result.maximum_absolute_defect = 1.0  # type: ignore[misc]
        with pytest.raises(TypeError, match="probe"):
            BandEquivalenceHoppingLocalityMetricCovarianceDefectResult(
                probe=cast(
                    BandEquivalenceHoppingLocalityMetricCovarianceProbeEnum, "probe"
                ),
                maximum_absolute_defect=0.0,
            )
        with pytest.raises(TypeError, match="built-in float"):
            BandEquivalenceHoppingLocalityMetricCovarianceDefectResult(
                probe=result.probe,
                maximum_absolute_defect=cast(float, True),
            )
        with pytest.raises(ValueError, match="finite and nonnegative"):
            BandEquivalenceHoppingLocalityMetricCovarianceDefectResult(
                probe=result.probe,
                maximum_absolute_defect=float("nan"),
            )

    def test_init__rejects_non_nominal_geometry(self) -> None:
        with pytest.raises(TypeError, match="inherit MetricGeometry"):
            BandEquivalenceHoppingLocalityMetricCovarianceDefectAnalyzer(
                cast(MetricGeometry, object())
            )
