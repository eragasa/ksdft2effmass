"""Software verification for frozen-parent synthetic-strain diagnostics."""

import math

import numpy as np
import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    strain,
    strain_response,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSyntheticStrainGaugeLocality:
    """Establish volume normalization, invariants, and physical-range response."""

    @pytest.mark.parametrize(
        ("path", "size"),
        (
            (strain.SyntheticStrainPath.RHOMBIC_2D, 16),
            (strain.SyntheticStrainPath.BAIN_3D, 8),
        ),
    )
    def test_path__frozen_gauge__preserves_power_while_physical_range_changes(
        self, path: strain.SyntheticStrainPath, size: int
    ) -> None:
        result = strain.calculate_synthetic_strain(
            path,
            size,
            (0.0, 0.5, 1.0),
            math.pi / 4.0,
            (1.0e-3,),
        )

        assert result.maximum_parseval_defect < 2.0e-14
        assert result.maximum_strain_invariance_defect == 0.0
        assert all(
            np.linalg.det(np.asarray(point.metric)) == pytest.approx(1.0, abs=2.0e-13)
            for point in result.points
        )
        assert max(
            point.restricted_alignment_residual for point in result.points
        ) == pytest.approx(
            min(point.restricted_alignment_residual for point in result.points),
            abs=1.0e-15,
        )
        assert result.points[0].maximum_bond_length != pytest.approx(
            result.points[-1].maximum_bond_length
        )

    def test_bain_common_cell_map__fcc_endpoint__is_unimodular_isometry(self) -> None:
        transform = np.asarray(strain.BAIN_FCC_UNIMODULAR_MAP, dtype=np.int64)
        assert round(float(np.linalg.det(transform))) == 1

        reference_fcc_metric = np.asarray(
            ((0.5, 0.25, 0.25), (0.25, 0.5, 0.25), (0.25, 0.25, 0.5))
        )
        unit_volume_fcc_metric = reference_fcc_metric * 2.0 ** (4.0 / 3.0)
        endpoint = strain.calculate_synthetic_strain(
            strain.SyntheticStrainPath.BAIN_3D,
            8,
            (0.0,),
            math.pi / 4.0,
            (1.0e-3,),
        ).points[0]
        assert transform.T @ unit_volume_fcc_metric @ transform == pytest.approx(
            np.asarray(endpoint.metric), abs=2.0e-15
        )

        reference_offset = np.asarray((0.25, 0.25, 0.25))
        bain_offset = np.asarray(strain.BAIN_DIAMOND_BASIS_OFFSETS[1])
        assert transform @ bain_offset == pytest.approx(reference_offset, abs=1.0e-15)

        reference_bonds = np.asarray(
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
                (-1, 1, 0),
                (-1, 0, 1),
                (0, -1, 1),
            )
        )
        mapped = np.linalg.solve(transform, reference_bonds.T).T.astype(np.int64)
        canonical = {
            tuple(vector if tuple(vector) > tuple(-vector) else -vector)
            for vector in mapped
        }
        assert canonical == {
            (0, 0, 1),
            (0, 1, 0),
            (1, -1, -1),
            (1, -1, 0),
            (1, 0, -1),
            (1, 0, 0),
        }
        for size in range(2, 9):
            images = {
                tuple((transform @ np.asarray(index)) % size)
                for index in np.ndindex((size, size, size))
            }
            assert len(images) == size**3

    @pytest.mark.parametrize(
        "path",
        (strain.SyntheticStrainPath.RHOMBIC_2D, strain.SyntheticStrainPath.BAIN_3D),
    )
    def test_m1__frozen_parent__has_zero_aligned_strain_difference(
        self, path: strain.SyntheticStrainPath
    ) -> None:
        result = strain_response.calculate_synthetic_strain_response(
            path,
            strain_response.StrainResponseModel.M1_FROZEN,
            8,
            9,
            1.0 / 3.0,
            (0.0, 1.0),
            math.pi / 4.0,
            0.0,
            (1.0e-3,),
        )

        assert all(
            point.delta_interpolation.maximum_hamiltonian < 2.0e-14
            for point in result.points
        )
        assert all(
            point.maximum_pointwise_frame_alignment_residual < 2.0e-14
            for point in result.points
        )
        assert all(
            point.aligned_strain_perturbation.maximum_hamiltonian < 2.0e-14
            for point in result.points
        )
        assert all(
            cutoff.delta_total is not None
            and cutoff.delta_total.maximum_hamiltonian < 2.0e-14
            for point in result.points
            for cutoff in point.cutoffs
        )

    def test_m2__radial_response__produces_qualified_nonzero_perturbation(self) -> None:
        result = strain_response.calculate_synthetic_strain_response(
            strain.SyntheticStrainPath.RHOMBIC_2D,
            strain_response.StrainResponseModel.M2_RADIAL,
            8,
            17,
            1.0 / 3.0,
            (0.0, 1.0),
            math.pi / 4.0,
            1.0,
            (1.0e-3,),
        )

        reference, strained = result.points
        assert reference.minimum_hopping_response == pytest.approx(1.0)
        assert reference.maximum_hopping_response == pytest.approx(1.0)
        assert strained.minimum_hopping_response < 1.0
        assert strained.maximum_hopping_response > 1.0
        assert strained.minimum_sampled_external_isolation_gap > 1.8
        assert strained.minimum_frame_overlap_singular_value > 0.99
        assert strained.aligned_strain_perturbation.maximum_hamiltonian > 1.0e-3
        assert strained.maximum_traceless_strain_component > 0.0
        assert strained.delta_offsite_power > 0.0
        assert np.isfinite(strained.delta_interpolation.maximum_hamiltonian)
        assert any(
            cutoff.delta_total is not None
            and cutoff.delta_total.maximum_hamiltonian
            > strained.delta_interpolation.maximum_hamiltonian
            for cutoff in strained.cutoffs
        )

    def test_inputs__odd_mesh_and_boolean_amplitude__fail_closed(self) -> None:
        with pytest.raises(ValueError, match="even"):
            strain.calculate_synthetic_strain(
                strain.SyntheticStrainPath.RHOMBIC_2D,
                15,
                (0.0, 1.0),
                math.pi / 4.0,
                (1.0e-3,),
            )
        with pytest.raises(ValueError, match="built-in float"):
            strain.calculate_synthetic_strain(
                strain.SyntheticStrainPath.RHOMBIC_2D,
                16,
                (0.0, 1.0),
                True,
                (1.0e-3,),
            )
