r"""Software verification of ``MetalUnitInventory``.

Evidence profile: routine

Bounded artifact scope: exact canonical metal-unit roles and pinned authority identity.

Facet and represented meaning

The module verifies the immutable role-to-unit inventory and its source provenance.

Intrinsic and cross-object scope

``MetalUnitInventory`` is the sole system under test. Conversion arithmetic, native
records, serialization, and external authority retrieval are excluded.

VVUQ and scientific exclusions

This is structural software verification. It does not execute LAMMPS, authorize
undeclared conversions, establish conversion accuracy, or provide scientific
validation or uncertainty quantification.
"""

from dataclasses import replace
from hashlib import sha256

import pytest

from ksdft2effmass.units import METAL_UNIT_INVENTORY, MetalUnitInventory, UnitIdentity

pytestmark = pytest.mark.software_verification

SUT = MetalUnitInventory


class TestMetalUnitInventory:
    """Own cohesive software-verification evidence for ``MetalUnitInventory``."""

    def test_constructor__canonical_roles__matches_pinned_metal_inventory(self) -> None:
        """Evidence ID: SV-UNIT-INVENTORY-001

        Requirement: The public inventory records every canonical LAMMPS ``metal``
        role without introducing integration defaults.

        Acceptance: The ordered role values equal the exact documented inventory.
        """
        inventory = METAL_UNIT_INVENTORY

        assert type(inventory) is SUT
        assert (
            inventory.mass_unit,
            inventory.distance_unit,
            inventory.time_unit,
            inventory.energy_unit,
            inventory.velocity_unit,
            inventory.force_unit,
            inventory.torque_unit,
            inventory.temperature_unit,
            inventory.pressure_unit,
            inventory.dynamic_viscosity_unit,
            inventory.charge_unit,
            inventory.dipole_unit,
            inventory.electric_field_unit,
            inventory.density_unit,
        ) == (
            UnitIdentity.GRAM_PER_MOLE,
            UnitIdentity.ANGSTROM,
            UnitIdentity.PICOSECOND,
            UnitIdentity.ELECTRON_VOLT,
            UnitIdentity.ANGSTROM_PER_PICOSECOND,
            UnitIdentity.ELECTRON_VOLT_PER_ANGSTROM,
            UnitIdentity.ELECTRON_VOLT,
            UnitIdentity.KELVIN,
            UnitIdentity.BAR,
            UnitIdentity.POISE,
            UnitIdentity.ELEMENTARY_CHARGE_MULTIPLE,
            UnitIdentity.ELEMENTARY_CHARGE_ANGSTROM,
            UnitIdentity.VOLT_PER_ANGSTROM,
            UnitIdentity.GRAM_PER_CENTIMETER_POWER_DIMENSION,
        )

    def test_constructor__identity_and_authority__retains_exact_provenance(
        self,
    ) -> None:
        """Evidence ID: SV-UNIT-INVENTORY-002

        Requirement: The inventory carries stable versioned content and exact pinned
        authority identities, and each role is fail-closed.

        Acceptance: Identity, version, inventory hash, LAMMPS version and LAMMPS hash
        agree exactly; assigning a distance unit to the mass role is rejected.
        """
        inventory = METAL_UNIT_INVENTORY

        assert inventory.identity == "ksdft2effmass.units.metal-canonical-inventory"
        assert inventory.version == 1
        preimage = (
            "v1|ksdft2effmass.units.metal-canonical-inventory|1|gram_per_mole|"
            "angstrom|picosecond|electron_volt|angstrom_per_picosecond|"
            "electron_volt_per_angstrom|electron_volt|kelvin|bar|poise|"
            "elementary_charge_multiple|elementary_charge_angstrom|"
            "volt_per_angstrom|gram_per_centimeter^dimension|"
            "442a188db85bacf28bbbe47541382c09aa6ba6f2a8271bc2aadbf35d16987834"
        )
        assert inventory.content_identity.value == (
            "sha256:a6c80626e92f510b17bae0a2d3854624b796c5abdd62409b5993fad33db53120"
        )
        assert f"sha256:{sha256(preimage.encode('utf-8')).hexdigest()}" == (
            inventory.content_identity.value
        )
        assert inventory.authority.version == (
            "stable_22Jul2025_update6@9c5ab448c78a14fd534619622162ba418d6a1fb1"
        )
        assert inventory.authority.content_identity.value == (
            "sha256:442a188db85bacf28bbbe47541382c09aa6ba6f2a8271bc2aadbf35d16987834"
        )
        with pytest.raises(ValueError, match="mass_unit must be gram_per_mole"):
            replace(inventory, mass_unit=UnitIdentity.ANGSTROM)
