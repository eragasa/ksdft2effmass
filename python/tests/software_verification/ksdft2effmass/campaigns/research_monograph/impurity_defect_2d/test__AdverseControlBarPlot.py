r"""Software verification of ``AdverseControlBarPlot``.

Evidence profile: routine

Bounded artifact scope: Matplotlib-axis selection and adverse-control bar rendering.

Facet and represented meaning

The plot represents retained numerical adverse diagnostics relative to their maximum
and preserves status-only controls as a separate display category.

Intrinsic and cross-object scope

The plotter owns axis creation or reuse, display normalization, and rendering. It does
not calculate adverse controls or interpret physical adequacy.

VVUQ and scientific exclusions

This is software verification of plotting behavior, not numerical verification,
scientific validation, uncertainty quantification, or human acceptance.
"""

from __future__ import annotations

import pytest
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from ksdft2effmass.campaigns.research_monograph import (
    AdverseControlBarPlot,
    AdverseControlPlotRecord,
)

pytestmark = pytest.mark.software_verification
SUT = AdverseControlBarPlot


class TestAdverseControlBarPlot:
    """Own software verification of adverse-control bar rendering."""

    def test_method__execute__uses_supplied_or_creates_new_axes(self) -> None:
        """Render numerical and status-only controls through both axis routes.

        Evidence ID: SV-CAMPAIGN-DEFECT-2D-PLOTTING-002

        Requirement: The component accepts a Matplotlib ``Axes`` or ``None`` and
        preserves numerical versus status-only display semantics.

        Method: Render one maximum numerical value, one half-maximum value, and one
        status-only record first on supplied axes and then on newly created axes.

        Oracle: Numerical widths are normalized by their maximum while a status-only
        record receives the documented fixed display width.

        Acceptance: Supplied axes are returned with widths ``1.0``, ``0.5``, and
        ``0.55``; the default route returns distinct Matplotlib axes.

        Interpretation: Passing verifies axis selection and bar-display semantics.

        Limitations: Relative bar widths are visualization policy, not physical units
        or validation evidence.
        """

        records = (
            AdverseControlPlotRecord("maximum", "discriminating", 2.0),
            AdverseControlPlotRecord("half", "discriminating", 1.0),
            AdverseControlPlotRecord("status", "unresolved", None),
        )
        figure = plt.figure()
        supplied = figure.add_subplot(1, 1, 1)
        try:
            rendered = SUT(supplied).execute(records)
            assert rendered is supplied
            assert rendered.get_title(loc="left") == "Adverse controls"
            bars = tuple(
                patch for patch in rendered.patches if isinstance(patch, Rectangle)
            )
            assert len(bars) == 3
            assert [bar.get_width() for bar in bars] == [1.0, 0.5, 0.55]
            created = SUT().execute(records)
            try:
                assert isinstance(created, Axes)
                assert created is not supplied
                assert created.get_title(loc="left") == "Adverse controls"
            finally:
                created_figure = created.figure
                assert isinstance(created_figure, Figure)
                plt.close(created_figure)
        finally:
            plt.close(figure)
