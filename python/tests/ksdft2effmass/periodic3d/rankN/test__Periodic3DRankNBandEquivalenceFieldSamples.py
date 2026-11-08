"""Periodic-3D rank-N parent-independent represented-field contracts."""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.model import (
    Periodic3DRankNAnalyticCase,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.represented_fields import (  # noqa: E501
    Periodic3DRankNAnalyticCaseFieldSampler,
    Periodic3DRankNBandEquivalenceFieldSamples,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.transformation import (
    Periodic3DRankNGaugeNormalizationEnum,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNBandEquivalenceFieldSamples:
    """Qualify the model-independent sampled-field boundary."""

    @staticmethod
    def _coordinates(size: int, shift: float = 0.0) -> Float64Array:
        axis = (np.arange(size, dtype=np.float64) + shift) / float(size)
        return np.asarray(
            np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1),
            dtype=np.float64,
        )

    @staticmethod
    def _model() -> Periodic3DRankNAnalyticCase:
        return Periodic3DRankNAnalyticCase(
            case_identifier="simple-cubic-axis-control",
            retained_rank=3,
            circuit_depth=2,
            positive_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            gauge_normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
            parent_scale=1.0,
            transformation_coefficient=math.pi / 4.0,
        )

    @staticmethod
    def _constant_frames(
        coordinates: Float64Array,
        retained_rank: int,
    ) -> Complex128Array:
        frame = np.zeros((retained_rank + 2, retained_rank), dtype=np.complex128)
        frame[:retained_rank] = np.eye(retained_rank, dtype=np.complex128)
        return np.asarray(
            np.broadcast_to(
                frame,
                (*coordinates.shape[:-1], retained_rank + 2, retained_rank),
            ).copy(),
            dtype=np.complex128,
        )

    @staticmethod
    def _operators(
        coordinates: Float64Array,
        retained_rank: int,
    ) -> Complex128Array:
        diagonal = np.linspace(-0.5, 0.5, retained_rank)
        values = np.broadcast_to(
            np.diag(diagonal).astype(np.complex128),
            (*coordinates.shape[:-1], retained_rank, retained_rank),
        ).copy()
        return np.asarray(values, dtype=np.complex128)

    def test_analytic_sampler_preserves_every_existing_field_exactly(self) -> None:
        model = self._model()
        construction = self._coordinates(2)
        evaluation = self._coordinates(3, 0.25)

        fields = Periodic3DRankNAnalyticCaseFieldSampler(model).execute(
            construction,
            evaluation,
        )

        assert fields.retained_rank == model.retained_rank
        assert np.array_equal(
            fields.reference_construction_frames,
            model.reference_frames(construction),
        )
        assert np.array_equal(
            fields.reference_evaluation_frames,
            model.reference_frames(evaluation),
        )
        assert np.array_equal(
            fields.comparison_construction_frames,
            model.gauge_transformed_frames(construction),
        )
        assert np.array_equal(
            fields.comparison_evaluation_frames,
            model.gauge_transformed_frames(evaluation),
        )
        assert np.array_equal(
            fields.reference_construction_operators,
            model.exact_reduced_hamiltonians(construction),
        )
        assert np.array_equal(
            fields.reference_evaluation_operators,
            model.exact_reduced_hamiltonians(evaluation),
        )
        assert np.array_equal(
            fields.comparison_construction_operators,
            model.gauge_transformed_reduced_hamiltonians(construction),
        )
        assert np.array_equal(
            fields.comparison_evaluation_operators,
            model.gauge_transformed_reduced_hamiltonians(evaluation),
        )
        construction_inverse = fields.comparison_inverse_construction_right_actions
        evaluation_inverse = fields.comparison_inverse_evaluation_right_actions
        assert construction_inverse is not None
        assert evaluation_inverse is not None
        assert np.array_equal(
            construction_inverse,
            model.known_inverse_right_actions(construction),
        )
        assert np.array_equal(
            evaluation_inverse,
            model.known_inverse_right_actions(evaluation),
        )

    def test_accepts_provenance_bound_nonanalytic_fields(self) -> None:
        retained_rank = 5
        construction = self._coordinates(2)
        evaluation = self._coordinates(3, 0.25)
        construction_frames = self._constant_frames(construction, retained_rank)
        evaluation_frames = self._constant_frames(evaluation, retained_rank)
        construction_operators = self._operators(construction, retained_rank)
        evaluation_operators = self._operators(evaluation, retained_rank)
        construction_identity = np.broadcast_to(
            np.eye(retained_rank, dtype=np.complex128),
            (*construction.shape[:-1], retained_rank, retained_rank),
        ).copy()
        evaluation_identity = np.broadcast_to(
            np.eye(retained_rank, dtype=np.complex128),
            (*evaluation.shape[:-1], retained_rank, retained_rank),
        ).copy()

        fields = Periodic3DRankNBandEquivalenceFieldSamples(
            retained_rank=retained_rank,
            operator_identifier="wannier-represented-hamiltonian",
            energy_reference="dft-fermi-aligned-electron-volt",
            energy_unit="electron-volt",
            basis_identifier="wannier-candidate-sha256:test",
            construction_coordinates=construction,
            evaluation_coordinates=evaluation,
            reference_construction_frames=construction_frames,
            reference_evaluation_frames=evaluation_frames,
            comparison_construction_frames=construction_frames,
            comparison_evaluation_frames=evaluation_frames,
            reference_construction_operators=construction_operators,
            reference_evaluation_operators=evaluation_operators,
            comparison_construction_operators=construction_operators,
            comparison_evaluation_operators=evaluation_operators,
            comparison_inverse_construction_right_actions=np.asarray(
                construction_identity,
                dtype=np.complex128,
            ),
            comparison_inverse_evaluation_right_actions=np.asarray(
                evaluation_identity,
                dtype=np.complex128,
            ),
        )

        assert fields.retained_rank == 5
        assert fields.operator_identifier == "wannier-represented-hamiltonian"
        assert fields.energy_reference == "dft-fermi-aligned-electron-volt"
        assert fields.energy_unit == "electron-volt"
        assert not fields.construction_coordinates.flags.writeable
        assert not fields.reference_construction_frames.flags.writeable
        assert not fields.comparison_evaluation_operators.flags.writeable

    def test_prescribed_inverse_actions_are_optional_but_must_be_paired(self) -> None:
        model = self._model()
        fields = Periodic3DRankNAnalyticCaseFieldSampler(model).execute(
            self._coordinates(2),
            self._coordinates(3, 0.25),
        )

        without_inverse = replace(
            fields,
            comparison_inverse_construction_right_actions=None,
            comparison_inverse_evaluation_right_actions=None,
        )

        assert not without_inverse.has_comparison_inverse_right_actions
        with pytest.raises(ValueError, match="both present or absent"):
            replace(
                fields,
                comparison_inverse_construction_right_actions=None,
            )

    def test_rejects_mismatched_comparison_shapes(self) -> None:
        retained_rank = 3
        construction = self._coordinates(2)
        evaluation = self._coordinates(3, 0.25)
        construction_frames = self._constant_frames(construction, retained_rank)
        evaluation_frames = self._constant_frames(evaluation, retained_rank)
        construction_operators = self._operators(construction, retained_rank)
        evaluation_operators = self._operators(evaluation, retained_rank)
        construction_identity = np.broadcast_to(
            np.eye(retained_rank, dtype=np.complex128),
            (*construction.shape[:-1], retained_rank, retained_rank),
        ).copy()
        evaluation_identity = np.broadcast_to(
            np.eye(retained_rank, dtype=np.complex128),
            (*evaluation.shape[:-1], retained_rank, retained_rank),
        ).copy()

        with pytest.raises(ValueError, match="comparison_construction_frames"):
            Periodic3DRankNBandEquivalenceFieldSamples(
                retained_rank=retained_rank,
                operator_identifier="retained-hamiltonian",
                energy_reference="dimensionless-zero-v1",
                energy_unit="dimensionless",
                basis_identifier="test-basis",
                construction_coordinates=construction,
                evaluation_coordinates=evaluation,
                reference_construction_frames=construction_frames,
                reference_evaluation_frames=evaluation_frames,
                comparison_construction_frames=np.zeros(
                    (*construction.shape[:-1], 6, 2),
                    dtype=np.complex128,
                ),
                comparison_evaluation_frames=evaluation_frames,
                reference_construction_operators=construction_operators,
                reference_evaluation_operators=evaluation_operators,
                comparison_construction_operators=construction_operators,
                comparison_evaluation_operators=evaluation_operators,
                comparison_inverse_construction_right_actions=np.asarray(
                    construction_identity,
                    dtype=np.complex128,
                ),
                comparison_inverse_evaluation_right_actions=np.asarray(
                    evaluation_identity,
                    dtype=np.complex128,
                ),
            )
