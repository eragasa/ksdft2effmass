"""Periodic-3D rank-N PhysKit block-hopping parent construction."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension
from projectkoios.physkit.periodic.lattice.hopping import BlockHoppingModel
from projectkoios.physkit.solidstate.tb.bloch import BlockHoppingBlochEvaluator
from projectkoios.physkit.units import MatrixQuantity, Unitless

from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.model import (
    Periodic3DRankNAnalyticCase,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.parent import (
    Periodic3DRankNBlockHoppingParentBuilder,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.attack import (
    Periodic3DRankNGaugeNormalizationEnum,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNBlockHoppingParentBuilder:
    """Qualify parent ownership independently of the synthetic gauge attack."""

    @staticmethod
    def _builder(
        hopping_scale: float = 1.0,
    ) -> Periodic3DRankNBlockHoppingParentBuilder:
        return Periodic3DRankNBlockHoppingParentBuilder(
            retained_rank=4,
            positive_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            hopping_scale=hopping_scale,
        )

    @staticmethod
    def _case(
        attack_coefficient: float,
        *,
        retained_rank: int = 4,
        positive_bonds: tuple[tuple[int, int, int], ...] = (
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
        ),
        parent_scale: float = 1.0,
        case_identifier: str = "parent-equivalence-control",
    ) -> Periodic3DRankNAnalyticCase:
        return Periodic3DRankNAnalyticCase(
            case_identifier=case_identifier,
            retained_rank=retained_rank,
            circuit_depth=2,
            positive_bonds=positive_bonds,
            gauge_normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
            parent_scale=parent_scale,
            attack_coefficient=attack_coefficient,
        )

    def test_constructs_exact_physkit_parent_metadata_and_support(self) -> None:
        builder = self._builder()

        model = builder.execute()
        displacements = tuple(term.displacement.components for term in model.terms)

        assert type(model) is BlockHoppingModel
        assert model.dimension is LatticeDimension.THREE
        assert model.basis_size == 8
        assert isinstance(model.energy_unit, Unitless)
        assert model.energy_reference == builder.ENERGY_REFERENCE
        assert model.basis_identifier == builder.basis_identifier
        assert model.identifier == builder.model_identifier
        assert len(displacements) == 13
        assert (0, 0, 0) in displacements
        assert (-2, 0, 0) in displacements
        assert (0, 0, 2) in displacements
        assert all(
            not term.coefficient.magnitude.flags.writeable for term in model.terms
        )

    def test_zero_hopping_scale_constructs_a_strictly_onsite_parent(self) -> None:
        model = self._builder(hopping_scale=0.0).execute()

        assert tuple(term.displacement.components for term in model.terms) == (
            (0, 0, 0),
        )
        assert np.diag(model.terms[0].coefficient.magnitude) == pytest.approx(
            (-0.4, -0.4 / 3.0, 0.4 / 3.0, 0.4, 2.7, 2.9, 3.1, 3.3)
        )

    @pytest.mark.parametrize("retained_rank", (3, 4, 8))
    @pytest.mark.parametrize("parent_scale", (0.0, 1.0))
    @pytest.mark.parametrize(
        "positive_bonds",
        (
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
                (-1, 1, 0),
                (-1, 0, 1),
                (0, -1, 1),
            ),
        ),
    )
    def test_physkit_bloch_evaluation_matches_independent_parent_formula(
        self,
        retained_rank: int,
        parent_scale: float,
        positive_bonds: tuple[tuple[int, int, int], ...],
    ) -> None:
        case = self._case(
            attack_coefficient=0.0,
            retained_rank=retained_rank,
            positive_bonds=positive_bonds,
            parent_scale=parent_scale,
        )
        axis = np.arange(5, dtype=np.float64) / 5.0
        coordinates = np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1)
        flat_coordinates = coordinates.reshape((-1, 3))

        evaluation = BlockHoppingBlochEvaluator().evaluate(
            case.parent_model,
            MatrixQuantity(flat_coordinates, Unitless()),
        )
        actual = np.stack(
            tuple(matrix.magnitude for matrix in evaluation.bloch_matrices)
        ).reshape(
            (*coordinates.shape[:-1], case.ambient_dimension, case.ambient_dimension)
        )

        assert actual == pytest.approx(
            case.parent_hamiltonians(coordinates), abs=3.0e-15
        )

    def test_parent_identity_excludes_attack_and_study_case_identity(self) -> None:
        first = self._case(attack_coefficient=0.0)
        second = self._case(attack_coefficient=math.pi / 4.0)
        other_case = self._case(
            attack_coefficient=0.0,
            case_identifier="other-study-case",
        )

        assert first.parent_model.identifier == second.parent_model.identifier
        assert first.parent_model.identifier == other_case.parent_model.identifier
        assert (
            first.parent_model.basis_identifier == second.parent_model.basis_identifier
        )
        assert first.model_identity != second.model_identity
        assert first.model_identity != other_case.model_identity

    def test_parent_identity_is_independent_of_bond_order_and_orientation(self) -> None:
        first = self._builder().execute()
        reordered = Periodic3DRankNBlockHoppingParentBuilder(
            retained_rank=4,
            positive_bonds=((0, 0, -1), (1, 0, 0), (0, 1, 0)),
            hopping_scale=1.0,
        ).execute()

        assert first.identifier == reordered.identifier
        assert tuple(term.displacement for term in first.terms) == tuple(
            term.displacement for term in reordered.terms
        )
        for first_term, reordered_term in zip(
            first.terms, reordered.terms, strict=True
        ):
            assert first_term.coefficient.magnitude == pytest.approx(
                reordered_term.coefficient.magnitude, abs=0.0
            )
