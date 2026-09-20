r"""Software verification of ``ParticleInBoxStudyDefinition``.

Evidence profile: routine

Bounded artifact scope: immutable version-one particle-in-a-box study definition.

Facet and represented meaning

The DataObject retains exact study controls and boundary-reference text.

Intrinsic and cross-object scope

Positive controls and retained/full dimension ordering are included.

VVUQ and scientific exclusions

This verifies input invariants only, not numerical correctness, scientific validation,
uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.campaigns.research_monograph import ParticleInBoxStudyDefinition

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxStudyDefinition


class TestParticleInBoxStudyDefinition:
    """Own software evidence for ``ParticleInBoxStudyDefinition``."""

    def test_constructor__dimension_contract__rejects_oversized_retention(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-005

        Requirement: The retained dimension cannot exceed the finite coordinate-space
        dimension.

        Acceptance: Retaining four states from a three-point space raises ValueError.
        """
        with pytest.raises(ValueError, match="must not exceed"):
            ParticleInBoxStudyDefinition(
                1,
                "study",
                "illustrative numerical experiment",
                1.0,
                1.0,
                1.0,
                3,
                4,
                "cyclic",
                "comparison only",
            )
