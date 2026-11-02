"""Tests for the shared periodic-three-dimensional capability contract."""

import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension

import ksdft2effmass.periodic3d.base as base_module
from ksdft2effmass.periodic3d.base import Periodic3DCapability
from ksdft2effmass.periodic3d.gauge_alignment.base import Periodic3DGaugeAlignment
from ksdft2effmass.periodic3d.hopping_locality.base import Periodic3DHoppingLocality
from ksdft2effmass.periodic3d.support_truncation.base import (
    Periodic3DSupportTruncation,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class _GaugeAlignmentProbe(Periodic3DGaugeAlignment):
    __slots__ = ()


class _HoppingLocalityProbe(Periodic3DHoppingLocality):
    __slots__ = ()


class _SupportTruncationProbe(Periodic3DSupportTruncation):
    __slots__ = ()


class TestPeriodic3DCapability:
    """Establish one shared dimension without inventing stronger geometry."""

    def test__defining_module__owns_the_dimensional_base(self) -> None:
        assert base_module.__all__ == ["Periodic3DCapability"]
        assert Periodic3DCapability.__module__ == "ksdft2effmass.periodic3d.base"

    def test__capability_bases__share_the_exact_physkit_dimension(self) -> None:
        values = (
            _GaugeAlignmentProbe(),
            _HoppingLocalityProbe(),
            _SupportTruncationProbe(),
        )

        assert all(isinstance(value, Periodic3DCapability) for value in values)
        assert tuple(value.lattice_dimension for value in values) == (
            LatticeDimension.THREE,
            LatticeDimension.THREE,
            LatticeDimension.THREE,
        )

    def test__dimensional_base__does_not_fabricate_geometry_or_support(self) -> None:
        value = _HoppingLocalityProbe()

        assert not hasattr(value, "lattice_geometry")
        assert not hasattr(value, "direct_lattice")
        assert not hasattr(value, "translations")
