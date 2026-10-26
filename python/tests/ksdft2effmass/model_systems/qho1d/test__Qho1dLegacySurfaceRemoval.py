"""Software verification of the removed QHO1D predecessor surface."""

from __future__ import annotations

import importlib.util

from ksdft2effmass.campaigns import research_monograph
from ksdft2effmass.model_systems import qho1d
from ksdft2effmass.model_systems.study import ModelId, ModelSystemStudySchemaId


class TestQho1dLegacySurfaceRemoval:
    """Verify that predecessor APIs cannot remain accidental public contracts."""

    former_qho1d_exports = frozenset(
        {
            "Qho1dResultVerifier",
            "Qho1dStudyDefinition",
            "Qho1dStudyEvaluator",
            "Qho1dStudyInputDeserializer",
            "Qho1dStudyResult",
            "Qho1dStudyResultSerializer",
        }
    )
    former_monograph_exports = frozenset(
        {
            "HarmonicOscillatorResultVerifier",
            "HarmonicOscillatorStudyEvaluator",
            "HarmonicOscillatorStudyInputDeserializer",
            "HarmonicOscillatorStudyResultSerializer",
        }
    )

    def test_public_api__former_exports__are_absent(self) -> None:
        """Removed study and alias names are absent from both public roots."""
        assert self.former_qho1d_exports.isdisjoint(qho1d.__all__)
        assert self.former_monograph_exports.isdisjoint(research_monograph.__all__)
        assert all(not hasattr(qho1d, name) for name in self.former_qho1d_exports)
        assert all(
            not hasattr(research_monograph, name)
            for name in self.former_monograph_exports
        )

    def test_import__study_package__is_absent(self) -> None:
        """The predecessor package is removed rather than hidden behind a facade."""
        assert (
            importlib.util.find_spec("ksdft2effmass.model_systems.qho1d.study") is None
        )

    def test_identity__former_study_enums__are_absent(self) -> None:
        """Shared historical identity enums no longer advertise a QHO1D study."""
        assert "qho1d" not in ModelId.__members__
        assert "qho1d_v1" not in ModelSystemStudySchemaId.__members__
