"""Software verification of generic PNG visualization path admission."""

from __future__ import annotations

from enum import Enum

import pytest

from ksdft2effmass.visualizations import PngVisualization

pytestmark = pytest.mark.software_verification
SUT = PngVisualization


class _UnsafePlot(Enum):
    """Provide invalid cross-platform output names."""

    traversal = "../escape.png"
    windows_traversal = "..\\escape.png"
    nested = "nested/escape.png"
    wrong_suffix = "figure.pdf"
    empty_stem = ".png"
    windows_reserved = "CON.png"
    windows_reserved_with_space = "CON .png"
    windows_forbidden_character = "bad:name.png"


class TestPngVisualization:
    """Own safe generic PNG basename admission."""

    @pytest.mark.parametrize("plot", tuple(_UnsafePlot))
    def test_init__unsafe_or_non_png_plot_value__rejects_before_decoding(
        self,
        plot: _UnsafePlot,
    ) -> None:
        with pytest.raises(ValueError, match="basenames"):
            SUT(plot=plot, png=b"not inspected")
