"""Software verification for exact sampled Pareto classification."""

from __future__ import annotations

import math

import pytest

from ksdft2effmass.analysis.pareto import SampledParetoClassifier

pytestmark = pytest.mark.software_verification


class TestSampledParetoClassifier:
    """Establish exact minimization dominance and strict numeric boundaries."""

    def test_execute__retains_equal_and_tradeoff_points_but_rejects_dominated(
        self,
    ) -> None:
        """Weak-all and strict-any dominance preserves duplicates and tradeoffs."""
        objectives = (
            (1.0, 4.0, 4.0),
            (2.0, 3.0, 3.0),
            (3.0, 2.0, 2.0),
            (3.0, 3.0, 3.0),
            (2.0, 3.0, 3.0),
        )

        result = SampledParetoClassifier(objectives=objectives).result()

        assert result == (True, True, True, False, True)

    def test_execute__supports_any_common_positive_objective_dimension(self) -> None:
        """Prespecified finite dimensions require no weighting."""
        assert SampledParetoClassifier(objectives=((0.0,), (1.0,))).result() == (
            True,
            False,
        )
        assert SampledParetoClassifier(
            objectives=((0.0, 1.0, 2.0, 3.0), (1.0, 0.0, 2.0, 3.0))
        ).result() == (True, True)

    def test_execute__rejects_ambiguous_or_nonfinite_objectives(self) -> None:
        """Booleans, integers, ragged rows, and nonfinite values fail closed."""
        with pytest.raises(TypeError, match="nonempty tuple"):
            SampledParetoClassifier(objectives=())
        with pytest.raises(TypeError, match="built-in floats"):
            SampledParetoClassifier(
                objectives=((True, 1.0),)  # type: ignore[arg-type]
            )
        with pytest.raises(TypeError, match="built-in floats"):
            SampledParetoClassifier(
                objectives=((1, 1.0),)  # type: ignore[arg-type]
            )
        with pytest.raises(ValueError, match="common dimension"):
            SampledParetoClassifier(objectives=((1.0,), (1.0, 2.0)))
        with pytest.raises(ValueError, match="finite"):
            SampledParetoClassifier(objectives=((math.inf,),))
