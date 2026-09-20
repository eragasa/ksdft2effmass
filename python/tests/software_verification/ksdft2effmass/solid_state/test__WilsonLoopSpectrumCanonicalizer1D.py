r"""Software verification of ``WilsonLoopSpectrumCanonicalizer1D``.

Evidence profile: routine

Bounded artifact scope: modulo-``2*pi`` normalization and deterministic ordering.

Facet and represented meaning

Arbitrary finite phase representatives are mapped to canonical spectrum storage.

Intrinsic and cross-object scope

Principal-branch normalization and increasing ordering are included.

VVUQ and scientific exclusions

Authored phases establish software behavior only, not topology or validation.
"""

import numpy as np
import pytest

from ksdft2effmass.solid_state import WilsonLoopSpectrumCanonicalizer1D

pytestmark = pytest.mark.software_verification
SUT = WilsonLoopSpectrumCanonicalizer1D


class TestWilsonLoopSpectrumCanonicalizer1D:
    """Verify principal-branch normalization of unordered finite phases."""

    def test_method__execute__normalizes_nyquist_and_sorts(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-032

        Requirement: Equivalent phase representatives obtain canonical storage.

        Acceptance: ``pi`` and ``-3*pi`` both map to ``-pi`` before sorting.
        """
        result = SUT().execute((np.pi, 0.0, -3.0 * np.pi))

        assert result.eigenphases == (-np.pi, -np.pi, 0.0)
