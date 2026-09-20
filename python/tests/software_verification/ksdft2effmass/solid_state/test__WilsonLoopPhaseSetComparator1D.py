r"""Software verification of ``WilsonLoopPhaseSetComparator1D``.

Evidence profile: routine

Bounded artifact scope: unordered circular matching of equal-rank Wilson phase sets.

Facet and represented meaning

Optimal assignment, circular residuals, defects, and disposition are included.

Intrinsic and cross-object scope

Two canonical spectra are compared without positional band correspondence.

VVUQ and scientific exclusions

The authored phases verify software semantics, not a physical topological claim.
"""

import numpy as np
import pytest

from ksdft2effmass.solid_state import (
    WilsonLoopPhaseSetComparator1D,
    WilsonLoopSpectrum1D,
)

pytestmark = pytest.mark.software_verification
SUT = WilsonLoopPhaseSetComparator1D


class TestWilsonLoopPhaseSetComparator1D:
    """Verify optimal circular assignment rather than positional subtraction."""

    def test_method__execute__matches_across_principal_branch(self) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-033

        Requirement: Comparison treats phases as an unordered circular multiset.

        Acceptance: The minimum-cost assignment crosses stored positions and reports
        principal candidate-minus-reference residuals with the derived disposition.
        """
        reference = WilsonLoopSpectrum1D((-3.0, -2.0))
        candidate = WilsonLoopSpectrum1D((-2.1, 2.9))

        result = SUT().execute(reference, candidate, 0.4)

        assert result.matched_candidate_indices == (1, 0)
        np.testing.assert_allclose(
            result.signed_phase_residuals,
            (-0.3831853071795863, -0.10000000000000009),
            rtol=0.0,
            atol=5.0e-16,
        )
        assert result.maximum_absolute_phase_defect == abs(
            result.signed_phase_residuals[0]
        )
        assert result.passes
