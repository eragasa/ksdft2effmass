"""Software verification for sampled shell--scale decision landscapes."""

import math

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.decision_landscape import (  # noqa: E501
    ShellScaleDecisionLandscapeCalculator,
    ShellScaleDecisionLandscapeRequest,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (  # noqa: E501
    FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityFamilyEnum,
    BandEquivalenceLocalityRequest,
    GaugeNormalizationEnum,
    ParentEnum,
)

pytestmark = pytest.mark.unit


class TestShellScaleDecisionLandscapeCalculator:
    """Establish sampling, objective, and dominance behavior."""

    def locality_request(self) -> BandEquivalenceLocalityRequest:
        """Return one bounded nonflat square-family request."""
        return BandEquivalenceLocalityRequest(
            family=BandEquivalenceLocalityFamilyEnum.SQUARE,
            synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
            cases=(
                BandEquivalenceLocalityCase(
                    name="square-directed-parent",
                    dimension=2,
                    parent_kind=ParentEnum.DIRECTED_AXIS,
                    gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
                    positive_bonds=((1, 0), (0, 1)),
                    direct_metric=DirectLatticeMetric(
                        DirectLattice2D(
                            a1=np.asarray((1.0, 0.0), dtype=np.float64),
                            a2=np.asarray((0.0, 1.0), dtype=np.float64),
                        )
                    ),
                    shell_metric_scale=1.0,
                ),
            ),
            construction_size=8,
            evaluation_size=9,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(math.pi / 4.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=9,
        )

    def test_execute__sampled_shell_scale_grid__marks_exact_nondominance(self) -> None:
        request = ShellScaleDecisionLandscapeRequest(
            locality_request=self.locality_request(),
            scale_sample_count=5,
        )
        result = ShellScaleDecisionLandscapeCalculator(
            request=request,
            analyzer=BandEquivalenceLocalityAnalyzer(request=request.locality_request),
        ).execute()

        request_wire = request.to_json()
        result_wire = result.to_json()
        assert (
            ShellScaleDecisionLandscapeRequest.from_json(request_wire).to_json()
            == request_wire
        )
        assert type(result).from_json(result_wire).to_json() == result_wire
        assert result.family is BandEquivalenceLocalityFamilyEnum.SQUARE
        assert result.scale_sample_count == 5
        assert len(result.cases) == 1
        case = result.cases[0]
        assert case.scale_path_coordinates == (0.0, 0.25, 0.5, 0.75, 1.0)
        assert case.comparison_scales[0] == pytest.approx(
            case.optimized_comparison_scale
        )
        assert case.comparison_scales[-1] == 1.0
        assert case.shell_indices == (0, 1, 2, 4, 5, 8, 9)
        assert case.metric_shell_values == case.shell_indices
        assert tuple(point.metric_shell_value for point in case.points) == tuple(
            point.shell_index for point in case.points
        )
        assert result.to_json() == result_wire
        assert b'"shell_indices"' in result_wire
        assert b'"metric_shell_values"' not in result_wire
        assert case.retained_block_counts == (1, 5, 9, 13, 21, 25, 29)
        assert case.calculated_vertex_count == 5 * len(case.shell_indices)
        assert all(
            math.isfinite(point.maximum_hamiltonian_error)
            and point.maximum_hamiltonian_error >= 0.0
            and math.isfinite(point.maximum_sorted_band_error)
            and point.maximum_sorted_band_error >= 0.0
            for point in case.points
        )
        assert all(
            point.maximum_sorted_band_error
            <= math.sqrt(2.0) * point.maximum_hamiltonian_error + 1.0e-14
            for point in case.points
        )

        objectives = tuple(
            (
                point.retained_blocks,
                point.maximum_hamiltonian_error,
                point.maximum_sorted_band_error,
            )
            for point in case.points
        )
        expected = tuple(
            not any(
                other_index != point_index
                and other[0] <= point[0]
                and other[1] <= point[1]
                and other[2] <= point[2]
                and (other[0] < point[0] or other[1] < point[1] or other[2] < point[2])
                for other_index, other in enumerate(objectives)
            )
            for point_index, point in enumerate(objectives)
        )
        assert tuple(point.pareto_efficient for point in case.points) == expected
        assert 0 < case.pareto_efficient_vertex_count < case.calculated_vertex_count

    @pytest.mark.parametrize("value", (True, 1, 1002))
    def test_request__invalid_scale_sample_count__raises(
        self, value: bool | int
    ) -> None:
        with pytest.raises(ValueError, match="scale_sample_count"):
            ShellScaleDecisionLandscapeRequest(
                locality_request=self.locality_request(),
                scale_sample_count=value,
            )
