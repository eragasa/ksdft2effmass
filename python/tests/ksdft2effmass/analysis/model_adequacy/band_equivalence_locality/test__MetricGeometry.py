"""Software contracts for nominal metric-geometry analysis admission."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    DirectLattice3D,
    DirectLatticeMetric,
)

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityCase,
    GaugeNormalizationEnum,
    MetricGeometry,
    ParentEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.geometry import (
    metric_indices,
    metric_shell_classification,
)

pytestmark = pytest.mark.software_verification


def _square_metric() -> DirectLatticeMetric:
    return DirectLatticeMetric(
        DirectLattice2D(
            a1=np.asarray([1.0, 0.0], dtype=np.float64),
            a2=np.asarray([0.0, 1.0], dtype=np.float64),
        )
    )


def _cubic_metric() -> DirectLatticeMetric:
    return DirectLatticeMetric(
        DirectLattice3D(
            a1=np.asarray([1.0, 0.0, 0.0], dtype=np.float64),
            a2=np.asarray([0.0, 1.0, 0.0], dtype=np.float64),
            a3=np.asarray([0.0, 0.0, 1.0], dtype=np.float64),
        )
    )


def _orthogonal_case(dimension: int) -> BandEquivalenceLocalityCase:
    positive_bonds: tuple[tuple[int, ...], ...]
    if dimension == 2:
        direct_metric = _square_metric()
        positive_bonds = ((0, 1), (1, 0))
    elif dimension == 3:
        direct_metric = _cubic_metric()
        positive_bonds = ((0, 0, 1), (0, 1, 0), (1, 0, 0))
    else:
        raise ValueError("test geometry dimension must be two or three")
    return BandEquivalenceLocalityCase(
        name=f"orthogonal-{dimension}d-control",
        dimension=dimension,
        parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
        gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
        positive_bonds=positive_bonds,
        direct_metric=direct_metric,
        shell_metric_scale=1.0,
    )


@dataclass(frozen=True, slots=True)
class _StructuralMetricGeometry:
    dimension: int
    direct_metric: DirectLatticeMetric
    shell_metric_scale: float
    basis_offsets: tuple[tuple[float, ...], ...]


class TestMetricGeometry:
    """Require nominal admission while standardizing shared geometry validation."""

    def test_family_case__inherits_nominal_metric_geometry(self) -> None:
        assert issubclass(BandEquivalenceLocalityCase, MetricGeometry)

    def test_structural_match__is_not_admitted(self) -> None:
        geometry = _StructuralMetricGeometry(2, _square_metric(), 1.0, ())
        displacements = np.asarray([[0, 0]], dtype=np.int64)

        assert not isinstance(geometry, MetricGeometry)
        with pytest.raises(TypeError, match="inherit MetricGeometry"):
            metric_indices(geometry, displacements)  # type: ignore[arg-type]

    def test_family_case__uses_standard_metric_analysis_without_wire_change(
        self,
    ) -> None:
        geometry = BandEquivalenceLocalityCase(
            name="square-control",
            dimension=2,
            parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
            positive_bonds=((0, 1), (1, 0)),
            direct_metric=_square_metric(),
            shell_metric_scale=1.0,
        )
        wire = geometry.to_json()

        displacements = np.asarray(
            [[first, second] for first in range(-1, 2) for second in range(-1, 2)],
            dtype=np.int64,
        )
        labels = metric_indices(geometry, displacements)
        classification = metric_shell_classification(geometry, displacements)

        np.testing.assert_array_equal(
            np.asarray(classification.metric_shell_values, dtype=np.int64),
            labels,
        )
        assert tuple(sorted(set(labels.tolist()))) == (0, 1, 2)
        assert geometry.to_json() == wire

    @pytest.mark.parametrize(
        ("dimension", "expected_metric_values"),
        (
            (2, (0, 1, 2, 4, 5, 8)),
            (3, (0, 1, 2, 3, 4, 5, 6, 8, 9, 12)),
        ),
    )
    def test_dimensional_cutoffs__preserve_metric_values_and_support_counts(
        self,
        dimension: int,
        expected_metric_values: tuple[int, ...],
    ) -> None:
        geometry = _orthogonal_case(dimension)
        wire = geometry.to_json()
        displacements = np.asarray(
            tuple(product(range(-2, 3), repeat=dimension)),
            dtype=np.int64,
        )
        components = displacements.astype(np.float64)
        direct_values = np.rint(
            np.einsum(
                "ri,ij,rj->r",
                components,
                geometry.direct_metric.metric_tensor,
                components,
            )
        ).astype(np.int64)

        classification = metric_shell_classification(geometry, displacements)

        np.testing.assert_array_equal(
            classification.metric_shell_values,
            direct_values,
        )
        assert tuple(sorted(set(direct_values.tolist()))) == expected_metric_values
        assert tuple(
            sorted(set(classification.support_inventory.ordinal_shell_indices))
        ) == tuple(range(len(expected_metric_values)))
        for ordinal_shell_index, metric_shell_value in enumerate(
            expected_metric_values
        ):
            support = classification.support_inventory.support_through(
                ordinal_shell_index
            )
            assert support.retained_displacement_count == int(
                np.count_nonzero(direct_values <= metric_shell_value)
            )
        assert geometry.to_json() == wire
