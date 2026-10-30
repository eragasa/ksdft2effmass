"""Software verification for shell--scale decision-landscape rendering."""

from pathlib import Path

import pytest
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.decision_landscape import (
    ShellScaleCaseDecisionLandscape,
    ShellScaleDecisionLandscapeResult,
    ShellScaleDecisionPoint,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.decision_landscape_plotting import (
    ShellScaleDecisionLandscapePlotRequest,
    ShellScaleDecisionLandscapePlotWriter,
    shell_scale_sampled_cell_triangles,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (
    BandEquivalenceLocalityFamilyEnum,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestShellScaleDecisionLandscapePlotWriter:
    """Establish exact individual artifact writing."""

    def test_execute__one_case__writes_declared_pdf_and_png(
        self, tmp_path: Path
    ) -> None:
        case = ShellScaleCaseDecisionLandscape(
            name="square-directed-parent",
            parent_scale=1.0,
            gauge_amplitude=0.5,
            optimized_comparison_scale=0.8,
            shell_indices=(0, 1),
            retained_block_counts=(1, 5),
            scale_path_coordinates=(0.0, 1.0),
            comparison_scales=(0.8, 1.0),
            points=(
                ShellScaleDecisionPoint(0, 1, 0.0, 0.8, 0.4, 0.3, True),
                ShellScaleDecisionPoint(1, 5, 0.0, 0.8, 0.2, 0.15, True),
                ShellScaleDecisionPoint(0, 1, 1.0, 1.0, 0.5, 0.2, True),
                ShellScaleDecisionPoint(1, 5, 1.0, 1.0, 0.3, 0.05, True),
            ),
        )
        family = ShellScaleDecisionLandscapeResult(
            family=BandEquivalenceLocalityFamilyEnum.SQUARE,
            construction_size=4,
            evaluation_size=5,
            scale_sample_count=2,
            cases=(case,),
        )

        result = ShellScaleDecisionLandscapePlotWriter(
            request=ShellScaleDecisionLandscapePlotRequest(
                family_results=(family,),
                output_directory=tmp_path,
            )
        ).execute()

        assert result.individual_paths == (
            tmp_path / "square-directed-parent-shell-scale-decision-landscape.pdf",
            tmp_path / "square-directed-parent-shell-scale-decision-landscape.png",
        )
        assert result.principal_composite_paths == ()
        assert all(path.is_file() and path.stat().st_size > 0 for path in result.paths)
        assert shell_scale_sampled_cell_triangles(case) == (
            (0, 1, 3),
            (0, 3, 2),
        )
