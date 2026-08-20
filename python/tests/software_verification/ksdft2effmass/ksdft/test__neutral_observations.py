r"""Software verification of representation-neutral Kohn--Sham observations.

Evidence profile: routine

Bounded artifact scope: public neutral Kohn--Sham observation package contract.

Facet and represented meaning

The artifact represents ordered finite Kohn--Sham spectral and total-energy values
with explicit units and unavailable metadata states.

Intrinsic and cross-object scope

Intrinsic construction, exact represented state, numeric rejection, immutability,
and public exports are covered; aggregate compatibility is excluded.

VVUQ and scientific exclusions

These tests establish software behavior only, not many-body interpretation,
numerical verification, scientific validation, or uncertainty quantification.
"""

from __future__ import annotations

import math
from dataclasses import FrozenInstanceError

import pytest

import ksdft2effmass.ksdft as ksdft
from ksdft2effmass.ksdft import (
    Availability,
    EnergyUnit,
    KohnShamSpectralObservations,
    TotalEnergyObservation,
)

pytestmark = pytest.mark.software_verification


def test_public_api__package__exports_exact_neutral_observation_surface() -> None:
    """Evidence ID: SV-KSDFT-001

    Requirement: The neutral package exports only its documented enums and immutable
    observation records.

    Acceptance: ``__all__`` equals the exact architecture-owned inventory.
    """
    assert tuple(ksdft.__all__) == (
        "Availability",
        "EnergyUnit",
        "KohnShamSpectralObservations",
        "TotalEnergyObservation",
    )


def test_constructor__spectral_observations__preserves_ordered_finite_state() -> None:
    """Evidence ID: SV-KSDFT-002

    Requirement: Spectral observations preserve ordered finite Hartree eigenvalues,
    shape-compatible occupations, band count, and explicit unavailable metadata.

    Acceptance: Every public field equals the independently declared input.
    """
    observation = KohnShamSpectralObservations(
        eigenvalues=((-0.5, 0.25), (-0.4, 0.3)),
        eigenvalue_unit=EnergyUnit.HARTREE,
        occupations=((1.0, 0.0), (1.0, 0.0)),
        band_count=2,
        spin_channel_availability=Availability.NO_SPIN_RESOLVED_ARRAYS,
        energy_reference_availability=Availability.NOT_REPRESENTED,
    )
    assert observation.eigenvalues == ((-0.5, 0.25), (-0.4, 0.3))
    assert observation.occupations == ((1.0, 0.0), (1.0, 0.0))
    assert observation.band_count == 2
    assert observation.eigenvalue_unit is EnergyUnit.HARTREE
    assert (
        observation.spin_channel_availability
        is Availability.NO_SPIN_RESOLVED_ARRAYS
    )
    assert observation.energy_reference_availability is Availability.NOT_REPRESENTED


def test_constructor__numeric_inputs__rejects_invalid_scalar_values() -> None:
    """Evidence ID: SV-KSDFT-003

    Requirement: Public numeric boundaries reject booleans and numeric strings as
    wrong semantic types and reject nonfinite built-in floats as invalid values.

    Acceptance: Wrong types raise ``TypeError`` and nonfinite floats raise
    ``ValueError``.
    """
    with pytest.raises(TypeError):
        KohnShamSpectralObservations(
            eigenvalues=((-0.5,),),
            eigenvalue_unit=EnergyUnit.HARTREE,
            occupations=((1.0,),),
            band_count=True,
            spin_channel_availability=Availability.NO_SPIN_RESOLVED_ARRAYS,
            energy_reference_availability=Availability.NOT_REPRESENTED,
        )
    with pytest.raises(TypeError):
        TotalEnergyObservation(
            "-1.0",  # type: ignore[arg-type]
            EnergyUnit.HARTREE,
            Availability.NOT_REPRESENTED,
        )
    with pytest.raises(ValueError):
        TotalEnergyObservation(
            math.nan,
            EnergyUnit.HARTREE,
            Availability.NOT_REPRESENTED,
        )


def test_method__setattr__neutral_observations_are_immutable() -> None:
    """Evidence ID: SV-KSDFT-004

    Requirement: Neutral observation records are immutable through ordinary field
    assignment.

    Acceptance: Assignment raises ``FrozenInstanceError`` and state is unchanged.
    """
    energy = TotalEnergyObservation(
        -1.0, EnergyUnit.HARTREE, Availability.NOT_REPRESENTED
    )
    with pytest.raises(FrozenInstanceError):
        energy.value = 0.0  # type: ignore[misc]
    assert energy.value == -1.0
