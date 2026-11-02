"""Tests for the shared periodic-two-dimensional capability contract."""

import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension

import ksdft2effmass.periodic2d.base as base_module
from ksdft2effmass.periodic2d.base import Periodic2DCapability
from ksdft2effmass.periodic2d.gauge_alignment.base import Periodic2DGaugeAlignment
from ksdft2effmass.periodic2d.hopping_locality.base import Periodic2DHoppingLocality
from ksdft2effmass.periodic2d.support_truncation.base import (
    Periodic2DSupportTruncation,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class _GaugeAlignmentProbe(Periodic2DGaugeAlignment):
    __slots__ = ()


class _HoppingLocalityProbe(Periodic2DHoppingLocality):
    __slots__ = ()


class _SupportTruncationProbe(Periodic2DSupportTruncation):
    __slots__ = ()


class TestPeriodic2DCapability:
    """Establish one shared dimension without inventing stronger geometry."""

    def test__defining_module__owns_the_dimensional_base(self) -> None:
        assert base_module.__all__ == ["Periodic2DCapability"]
        assert Periodic2DCapability.__module__ == "ksdft2effmass.periodic2d.base"

    def test__capability_bases__share_the_exact_physkit_dimension(self) -> None:
        values = (
            _GaugeAlignmentProbe(),
            _HoppingLocalityProbe(),
            _SupportTruncationProbe(),
        )

        assert all(isinstance(value, Periodic2DCapability) for value in values)
        assert tuple(value.lattice_dimension for value in values) == (
            LatticeDimension.TWO,
            LatticeDimension.TWO,
            LatticeDimension.TWO,
        )

    def test__dimensional_base__does_not_fabricate_geometry_or_support(self) -> None:
        value = _HoppingLocalityProbe()

        assert not hasattr(value, "lattice_geometry")
        assert not hasattr(value, "direct_lattice")
        assert not hasattr(value, "translations")
