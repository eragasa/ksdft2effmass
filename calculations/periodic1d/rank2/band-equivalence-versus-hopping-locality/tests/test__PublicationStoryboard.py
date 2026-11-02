"""Contracts for the iterative rank-two publication-figure storyboard."""

from __future__ import annotations

import ast
from pathlib import Path

import matplotlib.image as mpimg
import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPublicationStoryboard:
    """Keep the design inventory closed, reproducible, and explicitly provisional."""

    @staticmethod
    def protocol_directory() -> Path:
        return Path(__file__).resolve().parents[1] / "protocol"

    def test_storyboard_has_the_closed_pdf_and_png_inventory(self) -> None:
        protocol = self.protocol_directory()
        output = protocol / "figures" / "storyboard"
        stems = (
            "01-analytic-benchmark",
            "02-five-scale-core-result",
            "03-hopping-locality-profiles",
            "04-equal-accuracy-range-inflation",
            "05-separated-error-channels",
            "06-numerical-controls",
        )

        assert tuple(path.name for path in sorted(output.iterdir())) == tuple(
            f"{stem}.{suffix}"
            for stem in stems
            for suffix in ("pdf", "png")
        )
        for stem in stems:
            pdf = (output / f"{stem}.pdf").read_bytes()
            png_path = output / f"{stem}.png"
            png = png_path.read_bytes()
            decoded = mpimg.imread(png_path)

            assert pdf.startswith(b"%PDF-")
            assert png.startswith(b"\x89PNG\r\n\x1a\n")
            assert decoded.ndim == 3
            assert decoded.size > 0

    def test_renderer_and_protocol_preserve_the_development_status_boundary(
        self,
    ) -> None:
        protocol = self.protocol_directory()
        renderer = protocol / "render_publication_storyboard.py"
        renderer_source = renderer.read_text(encoding="utf-8")
        ast.parse(renderer_source, filename=str(renderer))
        storyboard = (protocol / "publication-figure-storyboard.md").read_text(
            encoding="utf-8"
        )
        tex = (protocol / "experimental-protocol.tex").read_text(encoding="utf-8")

        assert "development tables" in renderer_source
        assert "direct-embedded-rank2-five-scale-complete-v1" in storyboard
        assert "not retained complete-five-scale evidence" in storyboard
        normalized_tex = " ".join(tex.split())
        assert "Publication figure storyboard (design-only)" in normalized_tex
        assert "must not read the development CSV files" in normalized_tex
