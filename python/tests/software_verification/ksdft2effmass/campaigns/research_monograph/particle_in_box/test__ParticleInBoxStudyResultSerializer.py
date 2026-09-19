r"""Software verification of ``ParticleInBoxStudyResultSerializer``.

Evidence profile: routine

Bounded artifact scope: public version-one result and provenance serialization.

Facet and represented meaning

The serializer retains the historical numerical wire representation while binding
newly authored bytes to current public implementation sources.

Intrinsic and cross-object scope

Canonical JSON shape, numerical payload compatibility, and source identities are
included.

VVUQ and scientific exclusions

This verifies serialization compatibility only, not scientific validation,
uncertainty quantification, or human acceptance.
"""

import json
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    ParticleInBoxResidualStudyEvaluator,
    ParticleInBoxStudyInputDeserializer,
    ParticleInBoxStudyResultSerializer,
)
from ksdft2effmass.campaigns.research_monograph.particle_in_box import JsonValue

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxStudyResultSerializer


class TestParticleInBoxStudyResultSerializer:
    """Own software evidence for the particle-in-box result serializer."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing maintained campaign resources."""
        return Path(__file__).resolve().parents[7]

    def test_method__execute__preserves_payload_and_binds_public_sources(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-003

        Requirement: New serialization preserves the version-one numerical payload and
        records exact public implementation identities.

        Acceptance: Excluding provenance, decoded bytes equal the retained result and
        the nine current source paths are recorded.
        """
        root = self.repository_root()
        calculation = root / "calculations" / "research-monograph" / "particle-in-box"
        input_path = calculation / "input.json"
        definition = ParticleInBoxStudyInputDeserializer().execute(
            input_path.read_bytes()
        )
        result = ParticleInBoxResidualStudyEvaluator().execute(definition)
        authored = cast(
            dict[str, JsonValue],
            json.loads(
                ParticleInBoxStudyResultSerializer()
                .execute(result, input_path, calculation / "run_experiment.py", root)
                .decode("utf-8")
            ),
        )
        retained = cast(
            dict[str, JsonValue],
            json.loads((calculation / "result.json").read_text(encoding="utf-8")),
        )
        authored_provenance = cast(dict[str, JsonValue], authored.pop("provenance"))
        retained.pop("provenance")

        assert authored == retained
        identities = authored_provenance["implementation_identities"]
        assert isinstance(identities, list)
        assert len(identities) == 9
