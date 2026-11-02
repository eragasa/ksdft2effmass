"""Explicit energy normalization for Fourier error channels."""

from __future__ import annotations

import numpy as np
import pytest

from ksdft2effmass.band_equivalence_hopping_locality.fourier import error_channels

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceHoppingLocalityErrorChannels:
    def test_norm_energy_scale_controls_every_normalized_channel(self) -> None:
        reference = np.zeros((1, 2, 2), dtype=np.complex128)
        approximation = np.asarray(
            [[[2.0, 0.0], [0.0, -2.0]]],
            dtype=np.complex128,
        )

        unit_scale = error_channels(
            approximation,
            reference,
            norm_energy_scale=1.0,
        )
        double_scale = error_channels(
            approximation,
            reference,
            norm_energy_scale=2.0,
        )

        assert double_scale.maximum_hamiltonian == pytest.approx(
            unit_scale.maximum_hamiltonian / 2.0
        )
        assert double_scale.rms_hamiltonian == pytest.approx(
            unit_scale.rms_hamiltonian / 2.0
        )
        assert double_scale.maximum_band == pytest.approx(unit_scale.maximum_band / 2.0)
        assert double_scale.rms_band == pytest.approx(unit_scale.rms_band / 2.0)
