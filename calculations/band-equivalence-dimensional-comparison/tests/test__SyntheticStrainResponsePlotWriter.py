"""Software verification for campaign-owned M1/M2 response rendering."""

import math
from pathlib import Path

import matplotlib.pyplot as plt
import pytest
from matplotlib.axes import Axes

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainPath,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainResponseModel,
    SyntheticStrainResponseResult,
    calculate_synthetic_strain_response,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response_plotting import (  # noqa: E501
    render_strain_response_axes,
    write_strain_response_plots,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSyntheticStrainResponsePlotWriter:
    """Establish supplied-axes composition and campaign-owned file output."""

    @staticmethod
    def responses() -> tuple[
        SyntheticStrainResponseResult,
        SyntheticStrainResponseResult,
    ]:
        """Return one bounded pair with the maintained two-tolerance inventory."""
        arguments = (
            SyntheticStrainPath.RHOMBIC_2D,
            4,
            5,
            1.0 / 3.0,
            (0.0, 0.5, 1.0),
            math.pi / 8.0,
        )
        frozen = calculate_synthetic_strain_response(
            arguments[0],
            StrainResponseModel.M1_FROZEN,
            *arguments[1:],
            0.0,
            (1.0e-2, 1.0e-3),
        )
        radial = calculate_synthetic_strain_response(
            arguments[0],
            StrainResponseModel.M2_RADIAL,
            *arguments[1:],
            1.0,
            (1.0e-2, 1.0e-3),
        )
        return frozen, radial

    def test_render_strain_response_axes__supplied_axes__renders_each_panel(
        self,
    ) -> None:
        frozen, radial = self.responses()
        figure, array = plt.subplots(2, 2)
        axes = (
            (array[0, 0], array[0, 1]),
            (array[1, 0], array[1, 1]),
        )

        render_strain_response_axes(axes, frozen, radial)

        assert all(type(axis) is Axes for row in axes for axis in row)
        assert all(axis.get_title() for row in axes for axis in row)
        plt.close(figure)

    def test_write_strain_response_plots__valid_results__writes_pdf_and_png(
        self, tmp_path: Path
    ) -> None:
        frozen, radial = self.responses()

        outputs = write_strain_response_plots(
            frozen,
            radial,
            tmp_path,
            "Rhombic strain",
        )

        assert outputs == (
            tmp_path / "m1-m2-strain-response.pdf",
            tmp_path / "m1-m2-strain-response.png",
        )
        assert all(path.is_file() and path.stat().st_size > 0 for path in outputs)
