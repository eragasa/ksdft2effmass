"""In-memory periodic-3D Wannier field adaptation with synthetic test arrays."""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.physkit.periodic.lattice import DirectLattice3D, DirectLatticeMetric

from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.field_geometry import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.policy import (
    Periodic3DRankNBandEquivalenceHoppingLocalityPolicy,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.result import (
    Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.wannier_fields import (  # noqa: E501
    Periodic3DRankNWannierFieldProducer,
    Periodic3DRankNWannierFieldSource,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.attack import (
    Periodic3DRankNGaugeNormalizationEnum,
    Periodic3DRankNGivensGaugeAttack,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.definition import (
    Periodic3DRankNGaugeAlignment,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNWannierFieldProducer:
    """Qualify the in-memory adapter without claiming real DFT/Wannier evidence."""

    @staticmethod
    def _coordinates(size: int, shift: float) -> Float64Array:
        axis = -0.5 + (np.arange(size, dtype=np.float64) + shift) / float(size)
        return np.asarray(
            np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1),
            dtype=np.float64,
        )

    @staticmethod
    def _frames(coordinates: Float64Array, rank: int) -> Complex128Array:
        frame = np.zeros((rank + 2, rank), dtype=np.complex128)
        frame[:rank] = np.eye(rank, dtype=np.complex128)
        return np.asarray(
            np.broadcast_to(frame, (*coordinates.shape[:-1], rank + 2, rank)).copy(),
            dtype=np.complex128,
        )

    @staticmethod
    def _operators(coordinates: Float64Array, rank: int) -> Complex128Array:
        coordinate_sum = np.sum(coordinates, axis=-1)
        orbital = np.linspace(-0.5, 0.5, rank, dtype=np.float64)
        diagonal = orbital + 0.1 * coordinate_sum[..., None]
        return np.asarray(
            diagonal[..., :, None] * np.eye(rank, dtype=np.complex128),
            dtype=np.complex128,
        )

    @classmethod
    def _source(cls, rank: int = 5) -> Periodic3DRankNWannierFieldSource:
        construction = cls._coordinates(3, 0.5)
        evaluation = cls._coordinates(4, 0.5 + 1.0 / 3.0)
        return Periodic3DRankNWannierFieldSource(
            retained_rank=rank,
            operator_identifier="wannier-represented-hamiltonian",
            energy_reference="fermi-aligned-zero",
            energy_unit="electron-volt",
            basis_identifier="wannier-candidate-test-basis",
            construction_coordinates=construction,
            evaluation_coordinates=evaluation,
            construction_frames=cls._frames(construction, rank),
            evaluation_frames=cls._frames(evaluation, rank),
            construction_operators=cls._operators(construction, rank),
            evaluation_operators=cls._operators(evaluation, rank),
        )

    @staticmethod
    def _attack(rank: int = 5) -> Periodic3DRankNGivensGaugeAttack:
        return Periodic3DRankNGivensGaugeAttack(
            retained_rank=rank,
            circuit_depth=2,
            harmonic_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
            coefficient=math.pi / 8.0,
        )

    def test_applies_attack_to_admitted_wannier_fields(self) -> None:
        source = self._source()
        attack = self._attack()

        fields = Periodic3DRankNWannierFieldProducer(
            source=source,
            attack=attack,
            frame_isometry_absolute_tolerance=1.0e-12,
            operator_hermiticity_absolute_tolerance=1.0e-12,
        ).execute()

        assert fields.retained_rank == source.retained_rank
        assert fields.operator_identifier == source.operator_identifier
        assert fields.energy_reference == source.energy_reference
        assert fields.energy_unit == source.energy_unit
        assert fields.basis_identifier == source.basis_identifier
        assert np.array_equal(
            fields.reference_construction_frames,
            source.construction_frames,
        )
        assert np.array_equal(
            fields.comparison_construction_frames,
            attack.apply_to_frames(
                source.construction_coordinates,
                source.construction_frames,
            ),
        )
        assert np.array_equal(
            fields.comparison_evaluation_operators,
            attack.apply_to_operators(
                source.evaluation_coordinates,
                source.evaluation_operators,
            ),
        )
        assert fields.has_comparison_inverse_right_actions
        assert not source.construction_frames.flags.writeable
        assert not source.evaluation_operators.flags.writeable

    def test_without_attack_preserves_one_channel_without_an_oracle(self) -> None:
        source = self._source()

        fields = Periodic3DRankNWannierFieldProducer(
            source=source,
            attack=None,
            frame_isometry_absolute_tolerance=1.0e-12,
            operator_hermiticity_absolute_tolerance=1.0e-12,
        ).execute()

        assert np.array_equal(
            fields.comparison_construction_frames,
            fields.reference_construction_frames,
        )
        assert np.array_equal(
            fields.comparison_evaluation_operators,
            fields.reference_evaluation_operators,
        )
        assert not fields.has_comparison_inverse_right_actions

    def test_produced_fields_enter_the_parent_independent_analyzer(self) -> None:
        source = self._source()
        fields = Periodic3DRankNWannierFieldProducer(
            source=source,
            attack=self._attack(),
            frame_isometry_absolute_tolerance=1.0e-12,
            operator_hermiticity_absolute_tolerance=1.0e-12,
        ).execute()
        policy = Periodic3DRankNBandEquivalenceHoppingLocalityPolicy(
            construction_size=3,
            construction_offsets=(0.5, 0.5, 0.5),
            norm_energy_scale=1.0,
            band_tolerances=(1.0e-3,),
            gauge_alignments=(
                Periodic3DRankNGaugeAlignment.IDENTITY,
                Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
                Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
            ),
            shell_cap=3,
            procrustes_tolerance=ComplexUnitaryProcrustesTolerance(
                rank_absolute=1.0e-12,
                rank_relative=1.0e-10,
                validation_absolute=1.0e-12,
                validation_relative=1.0e-10,
                rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
            ),
            transport_rank_absolute=1.0e-10,
            transport_rank_relative=1.0e-12,
        )
        geometry = Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry(
            identifier="simple-cubic-test-geometry",
            direct_metric=DirectLatticeMetric(
                DirectLattice3D(
                    a1=np.array((1.0, 0.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0, 0.0), dtype=np.float64),
                    a3=np.array((0.0, 0.0, 1.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=1.0,
        )

        analysis = Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer(
            policy=policy,
            geometry=geometry,
            fields=fields,
        ).execute()

        assert analysis.retained_rank == 5
        assert analysis.operator_identifier == "wannier-represented-hamiltonian"
        assert tuple(item.alignment for item in analysis.alignments) == (
            Periodic3DRankNGaugeAlignment.IDENTITY,
            Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        )

        rank = source.retained_rank
        ambient_dimension = source.evaluation_frames.shape[-2]
        flat_source = replace(
            source,
            evaluation_coordinates=source.evaluation_coordinates.reshape(-1, 3),
            evaluation_frames=source.evaluation_frames.reshape(
                -1,
                ambient_dimension,
                rank,
            ),
            evaluation_operators=source.evaluation_operators.reshape(-1, rank, rank),
        )
        flat_fields = Periodic3DRankNWannierFieldProducer(
            source=flat_source,
            attack=self._attack(),
            frame_isometry_absolute_tolerance=1.0e-12,
            operator_hermiticity_absolute_tolerance=1.0e-12,
        ).execute()
        flat_analysis = Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer(
            policy=policy,
            geometry=geometry,
            fields=flat_fields,
        ).execute()

        assert tuple(item.alignment for item in flat_analysis.alignments) == (
            Periodic3DRankNGaugeAlignment.IDENTITY,
            Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        )
        for tensor_item, flat_item in zip(
            analysis.alignments,
            flat_analysis.alignments,
            strict=True,
        ):
            assert isinstance(
                tensor_item,
                Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
            )
            assert isinstance(
                flat_item,
                Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
            )
            assert flat_item.maximum_direct_matrix_difference == pytest.approx(
                tensor_item.maximum_direct_matrix_difference,
                abs=1.0e-12,
            )
            assert (
                flat_item.reference_interpolation_errors.maximum_matrix_frobenius
                == pytest.approx(
                    tensor_item.reference_interpolation_errors.maximum_matrix_frobenius,
                    abs=1.0e-12,
                )
            )

        shifted_construction = self._coordinates(3, 0.0)
        shifted_source = replace(
            source,
            construction_coordinates=shifted_construction,
            construction_frames=self._frames(shifted_construction, rank),
            construction_operators=self._operators(shifted_construction, rank),
        )
        shifted_fields = Periodic3DRankNWannierFieldProducer(
            source=shifted_source,
            attack=self._attack(),
            frame_isometry_absolute_tolerance=1.0e-12,
            operator_hermiticity_absolute_tolerance=1.0e-12,
        ).execute()
        shifted_analysis = Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer(
            policy=replace(policy, construction_offsets=(0.0, 0.0, 0.0)),
            geometry=geometry,
            fields=shifted_fields,
        ).execute()

        assert shifted_analysis.retained_rank == rank

        curve_analysis = Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer(
            policy=replace(policy, band_tolerances=()),
            geometry=geometry,
            fields=fields,
        ).execute()
        for alignment in curve_analysis.alignments:
            assert isinstance(
                alignment,
                Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
            )
            assert alignment.tolerance_decisions == ()

    def test_rejects_unqualified_frames_operators_and_attack_rank(self) -> None:
        source = self._source()
        nonisometric_frames = np.array(source.construction_frames, copy=True)
        nonisometric_frames[..., 0, 0] = 2.0
        nonhermitian_operators = np.array(source.evaluation_operators, copy=True)
        nonhermitian_operators[..., 0, 1] = 1.0

        with pytest.raises(ValueError, match="isometry"):
            Periodic3DRankNWannierFieldProducer(
                source=replace(source, construction_frames=nonisometric_frames),
                attack=None,
                frame_isometry_absolute_tolerance=1.0e-12,
                operator_hermiticity_absolute_tolerance=1.0e-12,
            ).execute()
        with pytest.raises(ValueError, match="Hermiticity"):
            Periodic3DRankNWannierFieldProducer(
                source=replace(source, evaluation_operators=nonhermitian_operators),
                attack=None,
                frame_isometry_absolute_tolerance=1.0e-12,
                operator_hermiticity_absolute_tolerance=1.0e-12,
            ).execute()
        with pytest.raises(ValueError, match="retained rank"):
            Periodic3DRankNWannierFieldProducer(
                source=source,
                attack=self._attack(rank=4),
                frame_isometry_absolute_tolerance=1.0e-12,
                operator_hermiticity_absolute_tolerance=1.0e-12,
            )
