"""Software verification of removed periodic-1D Fourier-locality surfaces."""

from __future__ import annotations

import importlib.util

import pytest

import ksdft2effmass.periodic.periodic1d.models as periodic1d_models
import ksdft2effmass.periodic1d.fourier_locality as fourier_locality
from ksdft2effmass import periodic1d

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DFourierLocalityLegacySurfaceRemoval:
    """Verify that predecessor APIs cannot become accidental public contracts."""

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

    def test__Periodic1DFourierLocalityLegacySurfaceRemoval__keeps_root_non_eager(
        self,
    ) -> None:
        """Keep the periodic-1D root free of an eager export inventory."""
        assert not hasattr(periodic1d, "__all__")

    def test__Periodic1DFourierLocalityLegacySurfaceRemoval__removes_former_exports(
        self,
    ) -> None:
        """Remove every predecessor Fourier-locality root export."""
        assert all(not hasattr(periodic1d, name) for name in self.former_exports)

    def test__Periodic1DFourierLocalityLegacySurfaceRemoval__removes_toy_parent_name(
        self,
    ) -> None:
        """Do not expose the superseded toy parent from the new model namespace."""
        assert not hasattr(periodic1d_models, "Periodic1DFourierHamiltonianToyModel")

    def test__Periodic1DFourierLocalityLegacySurfaceRemoval__removes_toy_model_module(
        self,
    ) -> None:
        """Do not restore a toy-model compatibility module below the new owner."""
        assert importlib.util.find_spec("ksdft2effmass.periodic1d.model") is None
        assert (
            importlib.util.find_spec(
                "ksdft2effmass.periodic.periodic1d.models.toy_models"
            )
            is None
        )

    def test__Periodic1DFourierLocalityLegacySurfaceRemoval__removes_isolated_package(
        self,
    ) -> None:
        """Keep the predecessor isolated-band package non-importable."""
        assert (
            importlib.util.find_spec("ksdft2effmass.periodic1d.isolated_band") is None
        )

    def test__Periodic1DFourierLocalityLegacySurfaceRemoval__removes_verifier_exports(
        self,
    ) -> None:
        """Do not expose a second verifier through the Fourier-locality package."""
        former_names = {
            "Periodic1DFourierLocalityIndependentVerification",
            "Periodic1DFourierLocalityIndependentVerificationRequest",
            "Periodic1DFourierLocalityIndependentVerifier",
        }

        assert former_names.isdisjoint(fourier_locality.__all__)

    def test__Periodic1DFourierLocalityLegacySurfaceRemoval__removes_verifier_facade(
        self,
    ) -> None:
        """Keep the predecessor verification-values facade non-importable."""
        assert (
            importlib.util.find_spec(
                "ksdft2effmass.periodic1d.fourier_locality.verification_values"
            )
            is None
        )
