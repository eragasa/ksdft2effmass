r"""Software verification of ``HarmonicOscillatorNondimensionalizer``.

Evidence profile: routine

Bounded artifact scope: public normalized-scalar adaptation contract.

Facet and represented meaning

The class under test owns explicit adaptation of already nondimensional harmonic-
oscillator scalars to first-class Unitless quantities.

Intrinsic and cross-object scope

Exact scalar preservation and Unitless attachment are included.

VVUQ and scientific exclusions

This verifies typed adaptation only. It does not derive nondimensional scales or
establish numerical convergence, scientific validation, uncertainty quantification,
or human acceptance.
"""

import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems.harmonic_oscillator import (
    HarmonicOscillatorNondimensionalizer,
    ScalarQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = HarmonicOscillatorNondimensionalizer


class TestHarmonicOscillatorNondimensionalizer:
    """Own software evidence for ``HarmonicOscillatorNondimensionalizer``."""

    def test_method__execute__attaches_unitless_without_rescaling(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-018

        Requirement: The explicit nondimensionalization boundary preserves declared
        normalized magnitudes and attaches the Unitless type to every parameter.

        Acceptance: The public export is exact and inputs ``(2, 3, 4)`` become exact
        Unitless scalar quantities with those magnitudes.
        """
        assert model_systems.HarmonicOscillatorNondimensionalizer is (
            HarmonicOscillatorNondimensionalizer
        )

        parameters = HarmonicOscillatorNondimensionalizer().execute(2.0, 3.0, 4.0)

        assert parameters.hbar == ScalarQuantity(2.0, Unitless())
        assert parameters.mass == ScalarQuantity(3.0, Unitless())
        assert parameters.omega == ScalarQuantity(4.0, Unitless())
