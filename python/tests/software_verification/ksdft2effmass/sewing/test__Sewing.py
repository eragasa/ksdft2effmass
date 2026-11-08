"""Software verification of the scientific sewing owners."""

from __future__ import annotations

from inspect import isabstract

import numpy as np
import pytest
from projectkoios.physkit.units import Unitless

import ksdft2effmass.solidstate as solidstate
from ksdft2effmass.sewing import (
    EmbeddedPositionReciprocalSewing,
    FiniteBoundarySewing,
    IdentityReciprocalSewing,
    PermutationPhaseReciprocalSewing,
    PlaneWaveIndexSewing,
    ProjectedSubspaceSewing,
    ReciprocalEndpointSewingInventory,
    ReciprocalEndpointSewingMap,
    SymmetrySewing,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]

type AbstractSewingCategory = (
    EmbeddedPositionReciprocalSewing
    | PermutationPhaseReciprocalSewing
    | PlaneWaveIndexSewing
    | ProjectedSubspaceSewing
    | SymmetrySewing
    | FiniteBoundarySewing
)


class TestSewing:
    """Preserve distinct sewing categories and concrete reciprocal values."""

    @pytest.mark.parametrize(
        "sewing_type",
        (
            EmbeddedPositionReciprocalSewing,
            PermutationPhaseReciprocalSewing,
            PlaneWaveIndexSewing,
            ProjectedSubspaceSewing,
            SymmetrySewing,
            FiniteBoundarySewing,
        ),
    )
    def test__reserved_category__is_abstract(
        self,
        sewing_type: type[AbstractSewingCategory],
    ) -> None:
        """Require each unimplemented scientific sewing category to remain abstract.

        Parameters
        ----------
        sewing_type
            Exact reserved sewing category under verification.
        """
        assert isabstract(sewing_type)

        with pytest.raises(TypeError, match="abstract"):
            sewing_type()

    def test__identity_reciprocal_sewing__acts_in_ambient_space(self) -> None:
        """Construct the named identity in the declared ambient dimension."""
        sewing = IdentityReciprocalSewing(ambient_dimension=4)

        assert sewing.endpoint_map.identifier == sewing.IDENTIFIER
        assert sewing.endpoint_map.ambient_dimension == 4
        assert type(sewing.endpoint_map.coefficient_map.unit) is Unitless
        np.testing.assert_array_equal(
            sewing.endpoint_map.coefficient_map.magnitude,
            np.eye(4, dtype=np.complex128),
        )

    def test__reciprocal_endpoint_inventory__round_trips_canonical_wire(self) -> None:
        """Preserve axis order and exact typed-record serialization."""
        identity = IdentityReciprocalSewing(ambient_dimension=3).endpoint_map
        inventory = ReciprocalEndpointSewingInventory(
            positive_axis_maps=(identity, identity),
        )

        wire = inventory.to_json()
        restored = ReciprocalEndpointSewingInventory.from_json(wire)

        assert restored.to_json() == wire
        assert restored.spatial_dimension == 2
        assert restored.ambient_dimension == 3
        assert type(restored.map_for_axis(0)) is ReciprocalEndpointSewingMap
        assert restored.map_for_axis(1).identifier == identity.identifier

    def test__solidstate__does_not_export_migrated_reciprocal_sewing(self) -> None:
        """Keep the legacy namespace from acting as a compatibility facade."""
        assert not hasattr(solidstate, "IdentityReciprocalSewing")
        assert not hasattr(solidstate, "ReciprocalEndpointSewingInventory")
        assert not hasattr(solidstate, "ReciprocalEndpointSewingMap")
