"""Software verification for ordered periodic basis identities."""

from __future__ import annotations

import inspect

import pytest

from ksdft2effmass.periodic.operators.basis import (
    LabeledComponentBasisCoordinate,
    PeriodicBasisFamily,
    PeriodicBasisIdentity,
    PlaneWaveBasisCoordinate,
    SlaterKosterOrbital,
    SlaterKosterOrbitalBasisCoordinate,
    WannierOrbitalBasisCoordinate,
)
from ksdft2effmass.periodic.periodic1d.operators.basis import Periodic1DBasisIdentity
from ksdft2effmass.periodic.periodic2d.operators.basis import Periodic2DBasisIdentity
from ksdft2effmass.periodic.periodic3d.operators.basis import Periodic3DBasisIdentity

pytestmark = pytest.mark.software_verification


class TestPeriodicBasisIdentity:
    """Own exact coordinate keys, equality, validation, and canonical wire behavior."""

    def test_hierarchy__dimension_neutral_owner__is_abstract(self) -> None:
        assert inspect.isabstract(PeriodicBasisIdentity)

    def test_wire_round_trip__dimensional_types__remain_exact(self) -> None:
        identities: tuple[PeriodicBasisIdentity, ...] = (
            Periodic1DBasisIdentity(
                display_identifier="one-dimensional",
                coordinates=(PlaneWaveBasisCoordinate((0,)),),
            ),
            Periodic2DBasisIdentity(
                display_identifier="two-dimensional",
                coordinates=(PlaneWaveBasisCoordinate((0, 1)),),
            ),
            Periodic3DBasisIdentity(
                display_identifier="three-dimensional",
                coordinates=(PlaneWaveBasisCoordinate((0, 1, -1)),),
            ),
        )

        for identity in identities:
            restored = type(identity).from_json(identity.to_json())

            assert type(restored) is type(identity)
            assert restored == identity
            assert restored.spatial_dimension == identity.spatial_dimension

    def test_equality__different_display_identifier__uses_ordered_coordinates_only(
        self,
    ) -> None:
        first = Periodic2DBasisIdentity(
            display_identifier="first display name",
            coordinates=(
                LabeledComponentBasisCoordinate("valence"),
                LabeledComponentBasisCoordinate("conduction"),
            ),
        )
        renamed = Periodic2DBasisIdentity(
            display_identifier="renamed",
            coordinates=first.coordinates,
        )
        reordered = Periodic2DBasisIdentity(
            display_identifier="first display name",
            coordinates=tuple(reversed(first.coordinates)),
        )

        assert first == renamed
        assert hash(first) == hash(renamed)
        assert first != reordered
        assert first.family is PeriodicBasisFamily.LABELED_COMPONENT
        assert first.spatial_dimension == 2
        assert first.dimension == 2
        other_dimension: PeriodicBasisIdentity = Periodic3DBasisIdentity(
            display_identifier="first display name",
            coordinates=first.coordinates,
        )
        assert first != other_dimension

    def test_coordinate_families__exact_keys__remain_distinct(self) -> None:
        plane_wave = PlaneWaveBasisCoordinate((1, -2, 3), component_label="up")
        wannier = WannierOrbitalBasisCoordinate(
            native_ordinal=0,
            qualified_orbital_label="Si-A:p_x",
        )
        slater_koster = SlaterKosterOrbitalBasisCoordinate(
            site_label="A",
            orbital=SlaterKosterOrbital.P_X,
        )

        assert plane_wave.reciprocal_index == (1, -2, 3)
        assert wannier.native_ordinal == 0
        assert slater_koster.spin_component is None
        assert len({plane_wave, wannier, slater_koster}) == 3

    def test_to_json__round_trip__preserves_order_and_exact_family(self) -> None:
        identity = Periodic3DBasisIdentity(
            display_identifier="diamond-spinless-sp3s-star",
            coordinates=(
                SlaterKosterOrbitalBasisCoordinate(
                    site_label="A",
                    orbital=SlaterKosterOrbital.S,
                ),
                SlaterKosterOrbitalBasisCoordinate(
                    site_label="A",
                    orbital=SlaterKosterOrbital.P_X,
                ),
            ),
        )

        mapping = identity.to_dict()
        wire = identity.to_json()
        restored = Periodic3DBasisIdentity.from_json(wire)

        assert mapping["schema_version"] == 2
        assert mapping["spatial_dimension"] == 3
        assert restored == identity
        assert restored.display_identifier == identity.display_identifier
        assert restored.family is PeriodicBasisFamily.SLATER_KOSTER_ORBITAL
        assert restored.coordinates == identity.coordinates
        assert wire == restored.to_json()
        assert wire.endswith(b"\n")

    def test_from_dict__wrong_schema_or_spatial_dimension__rejects(self) -> None:
        identity = Periodic2DBasisIdentity(
            display_identifier="two-dimensional",
            coordinates=(PlaneWaveBasisCoordinate((0, 0)),),
        )
        wrong_schema = dict(identity.to_dict())
        wrong_schema["schema_version"] = 1
        wrong_dimension = dict(identity.to_dict())
        wrong_dimension["spatial_dimension"] = 3

        with pytest.raises(ValueError, match="schema_version must be 2"):
            Periodic2DBasisIdentity.from_dict(wrong_schema)
        with pytest.raises(ValueError, match="does not match"):
            Periodic2DBasisIdentity.from_dict(wrong_dimension)

    def test_constructor__mixed_duplicate_or_unqualified_coordinates__rejects(
        self,
    ) -> None:
        labeled = LabeledComponentBasisCoordinate("state-0")

        with pytest.raises(ValueError, match="one basis family"):
            Periodic1DBasisIdentity(
                display_identifier="mixed",
                coordinates=(labeled, PlaneWaveBasisCoordinate((0,))),
            )
        with pytest.raises(ValueError, match="unique"):
            Periodic1DBasisIdentity(
                display_identifier="duplicate",
                coordinates=(labeled, labeled),
            )
        with pytest.raises(ValueError, match="must match"):
            Periodic2DBasisIdentity(
                display_identifier="wrong plane-wave dimension",
                coordinates=(PlaneWaveBasisCoordinate((0,)),),
            )
        with pytest.raises(TypeError, match="excluding booleans"):
            PlaneWaveBasisCoordinate((True,))
        with pytest.raises(ValueError, match="must not be empty"):
            WannierOrbitalBasisCoordinate(
                native_ordinal=0,
                qualified_orbital_label="",
            )
        with pytest.raises(TypeError, match="SlaterKosterOrbital"):
            SlaterKosterOrbitalBasisCoordinate(
                site_label="A",
                orbital="p_x",  # type: ignore[arg-type]
            )
