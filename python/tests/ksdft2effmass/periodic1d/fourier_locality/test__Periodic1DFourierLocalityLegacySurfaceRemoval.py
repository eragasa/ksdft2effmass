"""Software verification of the removed legacy M1 surface."""

from __future__ import annotations

import importlib.util

import pytest

from ksdft2effmass import periodic1d
from ksdft2effmass.periodic1d import fourier_locality, model

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DFourierLocalityLegacySurfaceRemoval:
    """Verify that the predecessor cannot remain an accidental public contract."""

    former_exports = frozenset(
        {
            "Periodic1DFiniteDifferenceConvergenceObservation",
            "Periodic1DFourierHamiltonianToyModel",
            "Periodic1DIsolatedBandCalculationDefinition",
            "Periodic1DIsolatedBandCalculationResult",
            "Periodic1DIsolatedBandCalculator",
            "Periodic1DIsolatedBandRangeResult",
            "Periodic1DIsolatedBandResultJsonSerializer",
            "Periodic1DIsolatedBandResultVerifier",
            "Periodic1DIsolatedBandVerificationResult",
            "Periodic1DPlaneWaveConvergenceObservation",
        }
    )

    def test__public_api__former_exports_are_absent(self) -> None:
        """Removed M1 names are absent from the supported periodic root."""
        assert self.former_exports.isdisjoint(periodic1d.__all__)
        assert all(not hasattr(periodic1d, name) for name in self.former_exports)

    def test__model__fourier_toy_parent_is_absent(self) -> None:
        """The superseded Fourier toy-parent record is not retained as a facade."""
        name = "Periodic1DFourierHamiltonianToyModel"
        assert name not in model.__all__
        assert not hasattr(model, name)

    def test__import__legacy_isolated_band_package_is_absent(self) -> None:
        """The predecessor package remains Git-recoverable but not importable."""
        assert (
            importlib.util.find_spec("ksdft2effmass.periodic1d.isolated_band") is None
        )

    def test__independent_reference__has_no_verification_values_facade(self) -> None:
        """Independent reconstruction is an analyzer, not a second verifier."""
        former_names = {
            "Periodic1DFourierLocalityIndependentVerification",
            "Periodic1DFourierLocalityIndependentVerificationRequest",
            "Periodic1DFourierLocalityIndependentVerifier",
        }
        assert former_names.isdisjoint(fourier_locality.__all__)
        assert all(not hasattr(fourier_locality, name) for name in former_names)
        assert (
            importlib.util.find_spec(
                "ksdft2effmass.periodic1d.fourier_locality.verification_values"
            )
            is None
        )
