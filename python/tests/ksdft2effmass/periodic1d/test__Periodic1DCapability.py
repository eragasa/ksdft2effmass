"""Tests for the shared periodic-one-dimensional capability contract."""

import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension

import ksdft2effmass.periodic1d.base as base_module
from ksdft2effmass.periodic1d.base import Periodic1DCapability
from ksdft2effmass.periodic1d.gauge_alignment.base import Periodic1DGaugeAlignment
from ksdft2effmass.periodic1d.hopping_locality.base import Periodic1DHoppingLocality
from ksdft2effmass.periodic1d.support_truncation.base import (
    Periodic1DSupportTruncation,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class _GaugeAlignmentProbe(Periodic1DGaugeAlignment):
    __slots__ = ()


class _HoppingLocalityProbe(Periodic1DHoppingLocality):
    __slots__ = ()


class _SupportTruncationProbe(Periodic1DSupportTruncation):
    __slots__ = ()


class TestPeriodic1DCapability:
    """Establish one shared dimension without inventing stronger geometry."""

    def test__defining_module__owns_the_dimensional_base(self) -> None:
        assert base_module.__all__ == ["Periodic1DCapability"]
        assert Periodic1DCapability.__module__ == "ksdft2effmass.periodic1d.base"

    def test__capability_bases__share_the_exact_physkit_dimension(self) -> None:
        values = (
            _GaugeAlignmentProbe(),
            _HoppingLocalityProbe(),
            _SupportTruncationProbe(),
        )

        assert all(isinstance(value, Periodic1DCapability) for value in values)
        assert tuple(value.lattice_dimension for value in values) == (
            LatticeDimension.ONE,
            LatticeDimension.ONE,
            LatticeDimension.ONE,
        )

    def test__dimensional_base__does_not_fabricate_geometry_or_support(self) -> None:
        value = _HoppingLocalityProbe()

        assert not hasattr(value, "lattice_geometry")
        assert not hasattr(value, "direct_lattice")
        assert not hasattr(value, "translations")
