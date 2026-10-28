"""Software verification of the removed PIAB1D predecessor surface."""

from __future__ import annotations

import importlib.util

from ksdft2effmass.model_systems import piab1d


class TestPiab1dLegacySurfaceRemoval:
    """Verify that predecessor APIs cannot remain accidental public contracts."""

    former_exports = frozenset(
        {
            "JsonValue",
            "Piab1dResidualStudyEvaluator",
            "Piab1dResidualStudyResult",
            "Piab1dResultVerifier",
            "Piab1dStudyDefinition",
            "Piab1dStudyInputDeserializer",
            "Piab1dStudyResultSerializer",
        }
    )

    def test_public_api__former_exports__are_absent(self) -> None:
        """Removed study names are absent from the PIAB1D public root."""
        assert self.former_exports.isdisjoint(piab1d.__all__)
        assert all(not hasattr(piab1d, name) for name in self.former_exports)

    def test_import__study_package__is_absent(self) -> None:
        """The predecessor package is removed rather than hidden behind a facade."""
        assert (
            importlib.util.find_spec("ksdft2effmass.model_systems.piab1d.study") is None
        )

    def test_import__generic_study_package__is_absent(self) -> None:
        """The orphaned generic predecessor base is absent from the package."""
        assert importlib.util.find_spec("ksdft2effmass.model_systems.study") is None
