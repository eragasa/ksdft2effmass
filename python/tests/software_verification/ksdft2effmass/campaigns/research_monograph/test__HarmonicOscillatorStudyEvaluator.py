r"""Software verification of ``HarmonicOscillatorStudyEvaluator``.

Evidence profile: routine

Bounded artifact scope: ordered harmonic-oscillator monograph study evaluation.

Facet and represented meaning

The class under test composes the exact ordered Cartesian sweep declared by one
harmonic-oscillator monograph study definition.

Intrinsic and cross-object scope

The supported public import, deterministic ordering, result count, and request
correlation are included. Numerical correctness of each comparison and JSON
serialization are excluded.

VVUQ and scientific exclusions

This is software verification of campaign composition. It establishes no numerical
verification, convergence, scientific validation, uncertainty quantification, or
human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns import research_monograph
from ksdft2effmass.campaigns.research_monograph import (
    HarmonicOscillatorStudyEvaluator,
    HarmonicOscillatorStudyInputDeserializer,
    HarmonicOscillatorStudyResult,
)

pytestmark = pytest.mark.software_verification
SUT = HarmonicOscillatorStudyEvaluator


class TestHarmonicOscillatorStudyEvaluator:
    """Own software evidence for ``HarmonicOscillatorStudyEvaluator``."""

    @staticmethod
    def input_path() -> Path:
        """Return the maintained Appendix E input path."""
        return (
            Path(__file__).resolve().parents[6]
            / "calculations"
            / "research-monograph"
            / "harmonic-oscillator"
            / "input.json"
        )

    def test_method__execute__evaluates_declared_ordered_sweep(self) -> None:
        """Evidence ID: SV-MONOGRAPH-HO-002

        Requirement: The public evaluator executes the maintained ordered 3-by-3-by-3
        Cartesian sweep and retains each exact request correlation.

        Acceptance: The package import resolves to the documented class, the result
        contains 27 comparisons, and its first and final requests equal the declared
        endpoint combinations.
        """
        assert research_monograph.HarmonicOscillatorStudyEvaluator is (
            HarmonicOscillatorStudyEvaluator
        )
        definition = HarmonicOscillatorStudyInputDeserializer().execute(
            self.input_path().read_bytes()
        )

        result = HarmonicOscillatorStudyEvaluator().execute(definition)

        assert isinstance(result, HarmonicOscillatorStudyResult)
        assert len(result.comparisons) == 27
        first = result.comparisons[0].request
        final = result.comparisons[-1].request
        assert (
            first.box_half_width.magnitude,
            first.requested_grid_spacing.magnitude,
            first.retained_dimension,
        ) == (4.0, 0.2, 2)
        assert (
            final.box_half_width.magnitude,
            final.requested_grid_spacing.magnitude,
            final.retained_dimension,
        ) == (8.0, 0.05, 6)
