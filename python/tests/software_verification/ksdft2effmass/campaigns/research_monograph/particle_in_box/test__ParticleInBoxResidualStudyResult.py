r"""Software verification of ``ParticleInBoxResidualStudyResult``.

Evidence profile: routine

Bounded artifact scope: immutable particle-in-a-box residual-study ResultObject.

Facet and represented meaning

The ResultObject retains one coherent evaluator outcome with immutable represented
arrays and diagnostics.

Intrinsic and cross-object scope

Operational array immutability and definition correlation are included.

VVUQ and scientific exclusions

This verifies result storage only, not numerical correctness, scientific validation,
uncertainty quantification, or human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    ParticleInBoxResidualStudyEvaluator,
    ParticleInBoxResidualStudyResult,
    ParticleInBoxStudyInputDeserializer,
)

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxResidualStudyResult


class TestParticleInBoxResidualStudyResult:
    """Own software evidence for ``ParticleInBoxResidualStudyResult``."""

    def test_constructor__immutable_storage__retains_evaluator_outcome(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-006

        Requirement: Result arrays are operationally immutable and correlated to the
        exact evaluated definition.

        Acceptance: The evaluator-produced projector rejects mutation and retains the
        same definition object.
        """
        root = Path(__file__).resolve().parents[7]
        definition = ParticleInBoxStudyInputDeserializer().execute(
            (
                root
                / "calculations"
                / "research-monograph"
                / "particle-in-box"
                / "input.json"
            ).read_bytes()
        )
        result = ParticleInBoxResidualStudyEvaluator().execute(definition)

        assert result.definition is definition
        with pytest.raises(ValueError, match="read-only"):
            result.projector.magnitude[0, 0] = 1.0
