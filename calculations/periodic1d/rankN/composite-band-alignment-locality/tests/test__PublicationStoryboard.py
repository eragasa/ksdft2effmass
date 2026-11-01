"""Contracts for the rank-N publication-oriented protocol storyboard."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]

CALCULATION = Path(__file__).resolve().parents[1]
PROTOCOL = CALCULATION / "protocol"
RENDERER = PROTOCOL / "render_publication_storyboard.py"


def _renderer_module() -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "rankn_publication_storyboard", RENDERER
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("Could not load the publication storyboard renderer")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class TestPublicationStoryboard:
    """Establish the closed inventory and explicit evidence boundary."""

    def test__inventory__contains_six_pdf_png_pairs(self) -> None:
        module = _renderer_module()
        assert module.STORYBOARD_STEMS == (
            "01-alignment-information-hierarchy",
            "02-rank-depth-scaling",
            "03-locality-and-support-consequences",
            "04-separated-error-channels",
            "05-claim-operands-and-unresolved-boundary",
            "06-numerical-controls",
        )

        figure_directory = PROTOCOL / "figures" / "storyboard"
        expected = {
            figure_directory / f"{stem}.{suffix}"
            for stem in module.STORYBOARD_STEMS
            for suffix in ("pdf", "png")
        }
        assert set(figure_directory.iterdir()) == expected
        for path in expected:
            signature = path.read_bytes()[:8]
            if path.suffix == ".pdf":
                assert signature.startswith(b"%PDF-")
            else:
                assert signature == b"\x89PNG\r\n\x1a\n"

    def test__protocol__states_provenance_and_unresolved_claim_boundary(self) -> None:
        protocol = (PROTOCOL / "experimental-protocol.tex").read_text()
        guide = (PROTOCOL / "publication-figure-storyboard.md").read_text()

        for stem in _renderer_module().STORYBOARD_STEMS:
            assert f"figures/storyboard/{stem}.pdf" in protocol
        assert "CALCULATED RESULT---UNSEALED" in protocol
        assert "complete locality-extension\nclaim remains unresolved" in protocol
        assert "integrity-admitted" in guide
        assert "not independently verified in full" in guide
        assert "unchanged coefficients" in guide
        assert "irreversible support-truncation policy" in guide
