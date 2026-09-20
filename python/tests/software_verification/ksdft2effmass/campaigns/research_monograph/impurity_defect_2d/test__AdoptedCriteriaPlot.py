r"""Software verification of ``AdoptedCriteriaPlot``.

Evidence profile: routine

Bounded artifact scope: Matplotlib-axis selection and adopted-criterion rendering.

Facet and represented meaning

The plot represents retained criterion identifiers, values, comparisons, thresholds,
and software dispositions as a diagnostic axis.

Intrinsic and cross-object scope

The plotter owns axis creation or reuse and deterministic criterion rendering. It does
not calculate criteria or decide scientific acceptance.

VVUQ and scientific exclusions

This is software verification of plotting behavior, not numerical verification,
scientific validation, uncertainty quantification, or human acceptance.
"""

from __future__ import annotations

import pytest
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ksdft2effmass.campaigns.research_monograph import (
    AdoptedCriteriaPlot,
    AdoptedCriterionPlotRecord,
)

pytestmark = pytest.mark.software_verification
SUT = AdoptedCriteriaPlot


class TestAdoptedCriteriaPlot:
    """Own software verification of adopted-criterion axis rendering."""

    def test_method__execute__uses_supplied_or_creates_new_axes(self) -> None:
        """Render identical criteria through both supported axis-selection routes.

        Evidence ID: SV-CAMPAIGN-DEFECT-2D-PLOTTING-001

        Requirement: The component accepts a Matplotlib ``Axes`` or ``None``.

        Method: Render two typed criterion rows first on supplied axes and then with
        the default constructor.

        Oracle: The public contract requires identity-preserving reuse of supplied
        axes and creation of new axes when none are supplied.

        Acceptance: The supplied object is returned, the expected title and two
        disposition markers are present, and the default route returns distinct
        Matplotlib axes with the same title.

        Interpretation: Passing verifies axis selection and criterion rendering.

        Limitations: Artist presence does not establish criterion correctness or
        scientific acceptance.
        """

        records = (
            AdoptedCriterionPlotRecord("residual", 1.0e-12, "<=", 1.0e-10, True),
            AdoptedCriterionPlotRecord("selection", 0.0, "==", 1.0, False),
        )
        figure = plt.figure()
        supplied = figure.add_subplot(1, 1, 1)
        try:
            rendered = SUT(supplied).execute(records)
            assert rendered is supplied
            assert rendered.get_title(loc="left") == "Adopted criteria"
            assert len(rendered.collections) == 1
            assert len(rendered.texts) == 4
            created = SUT().execute(records)
            try:
                assert isinstance(created, Axes)
                assert created is not supplied
                assert created.get_title(loc="left") == "Adopted criteria"
            finally:
                created_figure = created.figure
                assert isinstance(created_figure, Figure)
                plt.close(created_figure)
        finally:
            plt.close(figure)
