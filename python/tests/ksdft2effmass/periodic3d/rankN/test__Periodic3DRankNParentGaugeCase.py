"""Periodic-3D arbitrary-rank synthetic case-composition contracts."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Float64Array

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.case import (
    Periodic3DRankNParentGaugeCase,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.transformation import (
    Periodic3DRankNGaugeNormalizationEnum,
    Periodic3DRankNGivensGaugeTransformation,
)
from periodic3d_rankn_analytic_case_support import (
    PERIODIC3D_RANK_N_TEST_BASIS_INVENTORY,
    SyntheticPeriodic3DRankNParentModel,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNParentGaugeCase:
    """Qualify exact model structure without presenting a calculated study result."""

    @staticmethod
    def _coordinates() -> Float64Array:
        first = np.arange(2, dtype=np.float64) / 2.0
        second = np.arange(2, dtype=np.float64) / 2.0
        third = np.arange(3, dtype=np.float64) / 3.0
        mesh = np.stack(np.meshgrid(first, second, third, indexing="ij"), axis=-1)
        return np.asarray(mesh, dtype=np.float64)

    @staticmethod
    def _case(retained_rank: int = 3) -> Periodic3DRankNParentGaugeCase:
        bonds = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        return Periodic3DRankNParentGaugeCase(
            case_identifier="simple-cubic-axis-control",
            parent_model=SyntheticPeriodic3DRankNParentModel(
                retained_rank=retained_rank,
                bond_inventory=bonds,
                coupling_scale=1.0,
                basis=PERIODIC3D_RANK_N_TEST_BASIS_INVENTORY.basis_identity_for_rank(
                    retained_rank
                ),
                role=PeriodicModelRole.CONTROL_MODEL,
            ),
            gauge_transformation=Periodic3DRankNGivensGaugeTransformation(
                retained_rank=retained_rank,
                circuit_depth=2,
                harmonic_bonds=bonds,
                normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
                coefficient=math.pi / 4.0,
            ),
        )

    def test_parent_has_selected_shape_ordering_and_gap_bound(self) -> None:
        case = self._case(retained_rank=4)
        coordinates = self._coordinates()

        retained = case.retained_energies(coordinates)
        exterior = case.exterior_energies(coordinates)
        parent = case.parent_hamiltonians(coordinates)
        frame = case.reference_frames(coordinates)

        assert case.ambient_dimension == 8
        assert case.basis_identity is case.parent_model.basis_identity
        assert case.basis_identity.dimension == case.band_subspace_rank
        assert retained.shape == (2, 2, 3, 4)
        assert exterior.shape == (2, 2, 3, 4)
        assert parent.shape == (2, 2, 3, 8, 8)
        assert frame.shape == (2, 2, 3, 8, 4)
        assert float(np.min(np.diff(retained, axis=-1))) > 0.0
        sampled_gap = float(np.min(exterior[..., 0] - retained[..., -1]))
        assert sampled_gap >= case.isolation_gap_lower_bound - 1.0e-15
        projected = np.swapaxes(frame.conjugate(), -1, -2) @ parent @ frame
        assert projected == pytest.approx(case.exact_reduced_hamiltonians(coordinates))
        assert not parent.flags.writeable
        assert not frame.flags.writeable

    def test_gauge_is_special_unitary_and_oracle_restores_reference(self) -> None:
        case = self._case()
        coordinates = self._coordinates()

        transformation = case.gauge_transformation
        gauge = case.gauge_unitaries(coordinates)
        inverse = case.known_inverse_right_actions(coordinates)
        gauge_transformed_frame = case.gauge_transformed_frames(coordinates)
        gauge_transformed_operator = case.gauge_transformed_reduced_hamiltonians(
            coordinates
        )
        identity = np.eye(case.retained_rank, dtype=np.complex128)

        assert type(transformation) is Periodic3DRankNGivensGaugeTransformation
        assert transformation.retained_rank == case.retained_rank
        assert transformation.circuit_depth == case.circuit_depth
        assert transformation.harmonic_bonds == case.positive_bonds
        assert transformation.normalization is case.gauge_normalization
        assert transformation.coefficient == case.transformation_coefficient
        assert gauge == pytest.approx(transformation.unitaries(coordinates), abs=0.0)
        assert np.swapaxes(gauge.conjugate(), -1, -2) @ gauge == pytest.approx(
            np.broadcast_to(identity, gauge.shape), abs=2.0e-15
        )
        assert np.linalg.det(gauge) == pytest.approx(
            np.ones(coordinates.shape[:-1]), abs=2.0e-15
        )
        assert gauge_transformed_frame @ inverse == pytest.approx(
            case.reference_frames(coordinates), abs=2.0e-15
        )
        assert (
            np.swapaxes(inverse.conjugate(), -1, -2)
            @ gauge_transformed_operator
            @ inverse
        ) == pytest.approx(case.exact_reduced_hamiltonians(coordinates), abs=2.0e-15)
        assert not gauge.flags.writeable

    def test_rejects_mismatched_parent_and_transformation_correlation(self) -> None:
        parent = self._case().parent_model
        with pytest.raises(ValueError, match="retained ranks must match"):
            Periodic3DRankNParentGaugeCase(
                case_identifier="simple-cubic-axis-control",
                parent_model=parent,
                gauge_transformation=Periodic3DRankNGivensGaugeTransformation(
                    retained_rank=4,
                    circuit_depth=2,
                    harmonic_bonds=parent.positive_bonds,
                    normalization=(Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM),
                    coefficient=math.pi / 4.0,
                ),
            )
        with pytest.raises(ValueError, match="harmonic bonds must match"):
            Periodic3DRankNParentGaugeCase(
                case_identifier="simple-cubic-axis-control",
                parent_model=parent,
                gauge_transformation=Periodic3DRankNGivensGaugeTransformation(
                    retained_rank=parent.band_subspace_rank,
                    circuit_depth=2,
                    harmonic_bonds=((1, 0, 0),),
                    normalization=(Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM),
                    coefficient=math.pi / 4.0,
                ),
            )

    def test_rejects_dimension_mismatch_and_transformation_bound(self) -> None:
        with pytest.raises(ValueError, match=r"shape \(\.\.\., 3\)"):
            self._case().parent_hamiltonians(np.zeros((2, 2, 2), dtype=np.float64))
        with pytest.raises(ValueError, match="pi/4"):
            Periodic3DRankNGivensGaugeTransformation(
                retained_rank=3,
                circuit_depth=1,
                harmonic_bonds=(
                    (1, 0, 0),
                    (0, 1, 0),
                    (0, 0, 1),
                    (-1, 1, 0),
                    (-1, 0, 1),
                    (0, -1, 1),
                ),
                normalization=Periodic3DRankNGaugeNormalizationEnum.BOND_RMS,
                coefficient=math.pi / 4.0,
            )
