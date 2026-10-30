"""Software verification for bounded synthetic-strain transition refinement."""

import math

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPathEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_scan import (  # noqa: E501
    SyntheticStrainTransitionRefiner,
)

pytestmark = pytest.mark.unit


class TestSyntheticStrainTransitionRefiner:
    """Establish bounded bisection of transitions visible on the base grid."""

    @pytest.mark.parametrize(
        "path",
        (SyntheticStrainPathEnum.RHOMBIC_2D, SyntheticStrainPathEnum.BAIN_3D),
    )
    def test_execute__201_point_scan__refines_detected_transition_brackets(
        self, path: SyntheticStrainPathEnum
    ) -> None:
        fractions = tuple(float(index) / 200.0 for index in range(201))
        base = SyntheticStrainCalculator(
            path=path,
            construction_size=8,
            strain_fractions=fractions,
            maximum_rotation_amplitude=math.pi / 4.0,
            tail_tolerances=(1.0e-1, 1.0e-2, 1.0e-3),
        ).execute()

        result = SyntheticStrainTransitionRefiner(
            base_result=base,
            maximum_refinement_depth=5,
        ).execute()

        wire = result.to_json()
        assert type(result).from_json(wire).to_json() == wire
        assert type(result).from_json(wire) == result
        assert result.base_sample_count == 201
        assert result.maximum_refinement_depth == 5
        assert result.shell_transitions
        assert result.bond_degeneracy_transitions
        assert result.maximum_final_bracket_width <= 0.005 / 32.0 + 1.0e-16
        assert all(
            bracket.left_retained_blocks != bracket.right_retained_blocks
            for bracket in result.shell_transitions
        )
        assert all(
            bracket.left_distinct_bond_lengths != bracket.right_distinct_bond_lengths
            for bracket in result.bond_degeneracy_transitions
        )
        first_bond_change = result.bond_degeneracy_transitions[0]
        assert first_bond_change.left_strain_fraction == 0.0
        assert first_bond_change.right_strain_fraction == pytest.approx(
            0.005 / 32.0,
            rel=0.0,
            abs=1.0e-18,
        )
        assert first_bond_change.left_distinct_bond_lengths == 1
        assert first_bond_change.right_distinct_bond_lengths == 2
        assert result.status == (
            "sampled-transition-brackets-not-continuum-certificates"
        )

    @pytest.mark.parametrize("depth", (True, 0, 21))
    def test_execute__invalid_refinement_depth__fails_closed(
        self, depth: bool | int
    ) -> None:
        base = SyntheticStrainCalculator(
            path=SyntheticStrainPathEnum.RHOMBIC_2D,
            construction_size=4,
            strain_fractions=(0.0, 1.0),
            maximum_rotation_amplitude=math.pi / 8.0,
            tail_tolerances=(1.0e-1,),
        ).execute()

        with pytest.raises(ValueError, match=r"built-in integer in \[1, 20\]"):
            SyntheticStrainTransitionRefiner(
                base_result=base,
                maximum_refinement_depth=depth,
            )
