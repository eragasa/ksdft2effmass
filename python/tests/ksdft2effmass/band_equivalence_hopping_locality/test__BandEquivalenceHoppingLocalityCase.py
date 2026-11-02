"""Tests for the dimension-general exact case record."""

from __future__ import annotations

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

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceHoppingLocalityCase:
    """Establish canonical nonorthogonal 2D/3D geometry decoding."""

    @staticmethod
    def _case(dimension: int) -> BandEquivalenceHoppingLocalityCase:
        lattice: DirectLattice2D | DirectLattice3D
        positive_bonds: tuple[tuple[int, ...], ...]
        if dimension == 2:
            lattice = DirectLattice2D(
                a1=np.array((1.0, 0.0), dtype=np.float64),
                a2=np.array((0.25, 1.5), dtype=np.float64),
            )
            positive_bonds = ((1, 0), (0, 1))
        else:
            lattice = DirectLattice3D(
                a1=np.array((1.0, 0.0, 0.0), dtype=np.float64),
                a2=np.array((0.25, 1.5, 0.0), dtype=np.float64),
                a3=np.array((0.1, 0.2, 2.0), dtype=np.float64),
            )
            positive_bonds = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        return BandEquivalenceHoppingLocalityCase(
            name=f"nonorthogonal-{dimension}d",
            dimension=dimension,
            parent_kind=ParentEnum.HERMITIAN_BRAVAIS,
            gauge_normalization=GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=positive_bonds,
            direct_metric=DirectLatticeMetric(lattice),
            shell_metric_scale=1.25,
        )

    @pytest.mark.parametrize("dimension", (2, 3))
    def test_canonical_round_trip_preserves_complete_primitive_basis(
        self, dimension: int
    ) -> None:
        case = self._case(dimension)

        restored = BandEquivalenceHoppingLocalityCase.from_json(case.to_json())

        assert restored.dimension == dimension
        assert np.array_equal(
            restored.direct_metric.primitive_basis,
            case.direct_metric.primitive_basis,
        )
        assert restored.to_json() == case.to_json()

    @pytest.mark.parametrize("dimension", (2, 3))
    def test_axis_decoder_distinguishes_invalid_type_from_invalid_value(
        self, dimension: int
    ) -> None:
        case = self._case(dimension)
        invalid_type = dict(case.to_dict())
        invalid_type["direct_lattice_primitive_vector_axis"] = 7
        invalid_value = dict(case.to_dict())
        invalid_value["direct_lattice_primitive_vector_axis"] = "rows"

        with pytest.raises(TypeError):
            BandEquivalenceHoppingLocalityCase.from_dict(invalid_type)
        with pytest.raises(ValueError):
            BandEquivalenceHoppingLocalityCase.from_dict(invalid_value)
