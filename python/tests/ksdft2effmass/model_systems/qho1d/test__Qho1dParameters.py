r"""Software verification of ``Qho1dParameters``.

Evidence profile: routine

Bounded artifact scope: public unit-aware oscillator-parameter invariants.

Facet and represented meaning

The class under test owns the declared public Qho1dParameters contract.

Intrinsic and cross-object scope

Intrinsic representation and directly documented compatibility behavior are included.

VVUQ and scientific exclusions

This verifies dimensional admissibility and immutable represented values. It does not
establish model adequacy, scientific validation, uncertainty quantification, or human
acceptance.
"""

from dataclasses import FrozenInstanceError

import pytest
from projectkoios.physkit.units import (
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass import model_systems
from ksdft2effmass.model_systems.qho1d import (
    Qho1dNondimensionalizationRequest,
    Qho1dNondimensionalizer,
    Qho1dParameters,
)

pytestmark = pytest.mark.software_verification
SUT = Qho1dParameters


class TestQho1dParameters:
    """Own software evidence for ``Qho1dParameters``."""

    def test_public_api__package__exports_supported_parameters_class(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-001

        Requirement: Qho1dParameters is available through the supported
        public model-systems import surface.

        Acceptance: The package binding is the documented class object.
        """
        assert model_systems.Qho1dParameters is (Qho1dParameters)

    def test_constructor__quantities__enforces_dimensional_contract(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-002

        Requirement: Parameters are positive immutable quantities that are either all
        Unitless under explicit nondimensionalization or carry compatible action,
        mass, and inverse-time dimensions.

        Acceptance: The normalized record has one Unitless oscillator length; mixed
        unit modes, wrong physical dimensions, and nonpositive values are rejected;
        field assignment raises FrozenInstanceError.
        """
        parameters = Qho1dNondimensionalizer(
            Qho1dNondimensionalizationRequest(1.0, 1.0, 1.0)
        ).execute()

        assert parameters.oscillator_length == ScalarQuantity(1.0, Unitless())
        physical = Qho1dParameters(
            hbar=ScalarQuantity(1.0, PhysicalUnit("joule * second")),
            mass=ScalarQuantity(1.0, PhysicalUnit("kilogram")),
            omega=ScalarQuantity(1.0, PhysicalUnit("1 / second")),
        )
        assert physical.oscillator_length == ScalarQuantity(1.0, PhysicalUnit("meter"))
        with pytest.raises(ValueError, match="must not mix"):
            Qho1dParameters(
                hbar=ScalarQuantity(1.0, PhysicalUnit("joule * second")),
                mass=ScalarQuantity(1.0, Unitless()),
                omega=ScalarQuantity(1.0, Unitless()),
            )
        with pytest.raises(ValueError, match="hbar has incompatible"):
            Qho1dParameters(
                hbar=ScalarQuantity(1.0, PhysicalUnit("meter")),
                mass=ScalarQuantity(1.0, PhysicalUnit("kilogram")),
                omega=ScalarQuantity(1.0, PhysicalUnit("1 / second")),
            )
        with pytest.raises(ValueError, match="hbar must be positive"):
            Qho1dParameters(
                hbar=ScalarQuantity(0.0, Unitless()),
                mass=ScalarQuantity(1.0, Unitless()),
                omega=ScalarQuantity(1.0, Unitless()),
            )
        with pytest.raises(FrozenInstanceError):
            parameters.mass = ScalarQuantity(2.0, Unitless())  # type: ignore[misc]
