r"""Software verification of ``ParticleInBoxResidualStudyEvaluator``.

Evidence profile: routine

Bounded artifact scope: public version-one residual-study composition.

Facet and represented meaning

The ActionObject composes public model-system, operator, projection, and residual
operations for one exact study definition.

Intrinsic and cross-object scope

Finite dimensions, exact zero residual, discarded-sector identity, and immutable
result arrays are included.

VVUQ and scientific exclusions

This verifies software composition only, not continuum convergence, scientific
validation, uncertainty quantification, or human acceptance.
"""

from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    ParticleInBoxResidualStudyEvaluator,
    ParticleInBoxStudyInputDeserializer,
)

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxResidualStudyEvaluator


class TestParticleInBoxResidualStudyEvaluator:
    """Own software evidence for the residual-study evaluator."""

    @staticmethod
    def definition_bytes() -> bytes:
        """Return maintained version-one input bytes."""
        path = (
            Path(__file__).resolve().parents[7]
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "input.json"
        )
        return path.read_bytes()

    def test_method__execute__preserves_projector_and_discarded_sector_identities(
        self,
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-002

        Requirement: The evaluator composes the exact retained-space constructions
        without conflating their different represented meanings.

        Acceptance: The result has dimension eight, a zero consistent residual, an
        unmatched residual equal to the discarded sector, and immutable arrays.
        """
        definition = ParticleInBoxStudyInputDeserializer().execute(
            self.definition_bytes()
        )
        result = ParticleInBoxResidualStudyEvaluator().execute(definition)

        assert result.hamiltonian.shape == (8, 8)
        assert result.hamiltonian.nonzero_count == 22
        np.testing.assert_array_equal(
            result.consistently_compressed.magnitude, np.zeros((8, 8))
        )
        np.testing.assert_allclose(
            result.unmatched_compression.magnitude,
            result.discarded_sector.magnitude,
            atol=128.0 * np.finfo(np.float64).eps,
        )
        assert not result.projector.magnitude.flags.writeable
