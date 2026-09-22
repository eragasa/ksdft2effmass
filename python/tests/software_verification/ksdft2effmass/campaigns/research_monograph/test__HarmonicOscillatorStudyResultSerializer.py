r"""Software verification of ``HarmonicOscillatorStudyResultSerializer``.

Evidence profile: routine

Bounded artifact scope: version-one harmonic-oscillator monograph result serialization.

Facet and represented meaning

The class under test serializes one evaluated Appendix E sweep into canonical
version-one JSON with explicit input, runner, and implementation source identities.

Intrinsic and cross-object scope

The supported public import, case count, retained source paths, and exact public
implementation inventory are included. Independent numerical reconstruction and
interpretation of calculated values are excluded.

VVUQ and scientific exclusions

This is software verification of a retained wire contract. It establishes no
numerical verification, convergence, provenance truth beyond checked source bytes,
scientific validation, uncertainty quantification, or human acceptance.
"""

import json
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns import research_monograph
from ksdft2effmass.campaigns.research_monograph import (
    HarmonicOscillatorStudyEvaluator,
    HarmonicOscillatorStudyInputDeserializer,
    HarmonicOscillatorStudyResultSerializer,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)

pytestmark = pytest.mark.software_verification
SUT = HarmonicOscillatorStudyResultSerializer


class TestHarmonicOscillatorStudyResultSerializer:
    """Own software evidence for ``HarmonicOscillatorStudyResultSerializer``."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing the maintained campaign resources."""
        return Path(__file__).resolve().parents[6]

    @classmethod
    def calculation_root(cls) -> Path:
        """Return the maintained harmonic-oscillator calculation directory."""
        return (
            cls.repository_root()
            / "calculations"
            / "research-monograph"
            / "harmonic-oscillator"
        )

    def test_method__execute__binds_public_implementation_identities(self) -> None:
        """Evidence ID: SV-MONOGRAPH-HO-003

        Requirement: A newly authored result preserves the version-one study payload
        and binds the thin runner plus exact public model-system, operator, and
        campaign implementation sources without rewriting the retained result.

        Acceptance: The public package resolves to the documented serializer; decoded
        output has 27 cases, maintained input and runner paths, and the ten exact
        public implementation paths with lowercase SHA-256 identities.
        """
        assert research_monograph.HarmonicOscillatorStudyResultSerializer is (
            HarmonicOscillatorStudyResultSerializer
        )
        root = self.repository_root()
        calculation = self.calculation_root()
        definition = HarmonicOscillatorStudyInputDeserializer().execute(
            (calculation / "input.json").read_bytes()
        )
        result = HarmonicOscillatorStudyEvaluator().execute(definition)

        encoded = HarmonicOscillatorStudyResultSerializer().execute(
            result,
            calculation / "input.json",
            calculation / "run_experiment.py",
            root,
        )
        payload = cast(JsonValue, json.loads(encoded.decode("utf-8")))
        assert isinstance(payload, dict)
        cases = payload["cases"]
        provenance = payload["provenance"]
        assert isinstance(cases, list)
        assert len(cases) == 27
        assert isinstance(provenance, dict)
        assert provenance["input_path"] == (
            "calculations/research-monograph/harmonic-oscillator/input.json"
        )
        assert provenance["script_path"] == (
            "calculations/research-monograph/harmonic-oscillator/run_experiment.py"
        )
        identities = provenance["implementation_identities"]
        assert isinstance(identities, list)
        assert len(identities) == 10
        expected_paths = {
            "python/src/ksdft2effmass/analysis/model_systems/intervals.py",
            (
                "python/src/ksdft2effmass/analysis/model_systems/"
                "harmonic_oscillator/model.py"
            ),
            (
                "python/src/ksdft2effmass/analysis/model_systems/"
                "harmonic_oscillator/comparison.py"
            ),
            "python/src/ksdft2effmass/operators/finite_differences.py",
            "python/src/ksdft2effmass/operators/ladder_operators.py",
            "python/src/ksdft2effmass/operators/quantities.py",
            (
                "python/src/ksdft2effmass/campaigns/research_monograph/"
                "harmonic_oscillator/records.py"
            ),
            (
                "python/src/ksdft2effmass/campaigns/research_monograph/"
                "harmonic_oscillator/input.py"
            ),
            (
                "python/src/ksdft2effmass/campaigns/research_monograph/"
                "harmonic_oscillator/evaluation.py"
            ),
            (
                "python/src/ksdft2effmass/campaigns/research_monograph/"
                "harmonic_oscillator/serialization.py"
            ),
        }
        observed_paths = {
            self.assert_identity(identities[0]),
            self.assert_identity(identities[1]),
            self.assert_identity(identities[2]),
            self.assert_identity(identities[3]),
            self.assert_identity(identities[4]),
            self.assert_identity(identities[5]),
            self.assert_identity(identities[6]),
            self.assert_identity(identities[7]),
            self.assert_identity(identities[8]),
            self.assert_identity(identities[9]),
        }
        assert observed_paths == expected_paths

    @staticmethod
    def assert_identity(value: JsonValue) -> str:
        """Assert one implementation identity and return its source path."""
        identity = cast(dict[str, JsonValue], value)
        path = identity["path"]
        sha256 = identity["sha256"]
        assert isinstance(path, str)
        assert isinstance(sha256, str)
        assert len(sha256) == 64
        return path
