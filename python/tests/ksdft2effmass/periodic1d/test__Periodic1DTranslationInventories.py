"""Tests for typed periodic-one-dimensional integer-index inventories."""

import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension

from ksdft2effmass.periodic1d.base import Periodic1DCapability
from ksdft2effmass.periodic1d.hopping_locality.inventory import (
    Periodic1DHoppingDiagnosticRangeInventory,
)
from ksdft2effmass.periodic1d.support_truncation.inventory import (
    Periodic1DSymmetricSupportInventory,
)
from ksdft2effmass.periodic1d.translations import (
    Periodic1DCyclicRepresentativeInventory,
    Periodic1DOrdinaryTranslationInventory,
    Periodic1DSymmetricTranslationRangeInventory,
)
from ksdft2effmass.real_space_support_truncation.support import (
    SymmetricRangeSupport1D,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DTranslationInventories:
    """Keep cyclic classes, ordinary translations, and support distinct."""

    def test__cyclic_inventory__retains_the_unpaired_nyquist_class(self) -> None:
        inventory = Periodic1DCyclicRepresentativeInventory(tuple(range(-4, 4)))

        assert inventory.point_count == 8
        assert inventory.negative_nyquist_representative == -4
        assert inventory.lattice_dimension is LatticeDimension.ONE
        assert inventory.ordinary_translation_inventory.translations == tuple(
            range(-3, 4)
        )

    def test__odd_cyclic_inventory__has_no_nyquist_class(self) -> None:
        inventory = Periodic1DCyclicRepresentativeInventory(tuple(range(-3, 4)))

        assert not inventory.has_nyquist_class
        assert inventory.ordinary_translation_inventory.translations == tuple(
            range(-3, 4)
        )
        with pytest.raises(ValueError, match="no Nyquist class"):
            _ = inventory.negative_nyquist_representative

    def test__cyclic_and_ordinary_inventories__remain_distinct_types(self) -> None:
        values = tuple(range(-3, 4))

        inventories: tuple[Periodic1DCapability, ...] = (
            Periodic1DCyclicRepresentativeInventory(values),
            Periodic1DOrdinaryTranslationInventory(values),
        )

        assert inventories[0] != inventories[1]

    def test__ordinary_inventory__requires_zero_and_conjugate_closure(self) -> None:
        with pytest.raises(ValueError, match="conjugate-closed"):
            Periodic1DOrdinaryTranslationInventory((-2, -1, 0, 1))
        with pytest.raises(ValueError, match="contain zero"):
            Periodic1DOrdinaryTranslationInventory((-2, -1, 1, 2))

    def test__ordinary_inventory__admits_sparse_conjugate_closed_support(self) -> None:
        inventory = Periodic1DOrdinaryTranslationInventory((-4, -1, 0, 1, 4))

        assert inventory.maximum_range == 4
        assert (
            tuple(
                displacement.components[0] for displacement in inventory.displacements
            )
            == inventory.translations
        )
        assert all(
            displacement.dimension is LatticeDimension.ONE
            for displacement in inventory.displacements
        )

    def test__symmetric_range_inventory__retains_ordered_neutral_ranges(self) -> None:
        inventory = Periodic1DSymmetricTranslationRangeInventory.from_maximum_ranges(
            (0, 1, 4)
        )

        assert inventory.maximum_ranges == (0, 1, 4)
        assert inventory.ranges[-1].translations == tuple(range(-4, 5))
        with pytest.raises(ValueError, match="strictly increasing"):
            Periodic1DSymmetricTranslationRangeInventory.from_maximum_ranges((1, 0))

    def test__diagnostic_and_support_inventories__have_distinct_roles(self) -> None:
        diagnostics = Periodic1DHoppingDiagnosticRangeInventory.from_maximum_ranges(
            (0, 2, 4)
        )
        supports = Periodic1DSymmetricSupportInventory.from_maximum_ranges((0, 2, 4))

        assert diagnostics.maximum_ranges == supports.maximum_ranges
        assert diagnostics.ranges == supports.ranges
        assert diagnostics.__class__.__module__ != supports.__class__.__module__

    def test__symmetric_range_support__exposes_ordinary_translations(self) -> None:
        support = SymmetricRangeSupport1D(maximum_range=3)

        assert support.translations == tuple(range(-3, 4))
        assert (
            Periodic1DOrdinaryTranslationInventory(support.translations).displacements
            == support.support.displacements
        )
