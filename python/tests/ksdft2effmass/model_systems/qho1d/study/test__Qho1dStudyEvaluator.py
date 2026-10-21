r"""Software verification of ``Qho1dStudyEvaluator``.

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
from ksdft2effmass.model_systems.qho1d import (
    Qho1dStudyEvaluator,
    Qho1dStudyInputDeserializer,
    Qho1dStudyResult,
)

pytestmark = pytest.mark.software_verification
SUT = Qho1dStudyEvaluator


class TestQho1dStudyEvaluator:
    """Own software evidence for ``Qho1dStudyEvaluator``."""

    @staticmethod
    def input_path() -> Path:
        """Return the maintained QHO1D development input path."""
        return (
            Path(__file__).resolve().parents[6]
            / "calculations"
            / "qho1d"
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
        assert (
            research_monograph.HarmonicOscillatorStudyEvaluator is Qho1dStudyEvaluator
        )
        definition = Qho1dStudyInputDeserializer().execute(
            self.input_path().read_bytes()
        )

        result = Qho1dStudyEvaluator().execute(definition)

        assert isinstance(result, Qho1dStudyResult)
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
