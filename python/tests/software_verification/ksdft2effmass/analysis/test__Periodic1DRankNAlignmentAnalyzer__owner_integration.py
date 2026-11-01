"""Verify the reviewed owner capabilities required by higher-rank D1."""

from __future__ import annotations

import json
import math
from importlib.metadata import distribution

import numpy as np
import numpy.typing as npt
import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
    FinitePeriodicMatrixFourierTransformer,
    FinitePeriodicMatrixHermiticityAnalyzer,
    FinitePeriodicMatrixParsevalAnalyzer,
    FinitePeriodicMatrixSamples,
)
from projectkoios.physkit.units import Unitless

from ksdft2effmass.analysis.matrix_field import (
    MatrixFieldErrorAnalyzer,
    SymmetricRangeTailAnalyzer1D,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]

_OPTIMIZATION_REVISION = "f0fa13693543c89b2c40f11583a1140df0cf7b0b"
_PHYSKIT_REVISION = "3250679023cb131f98d50f8d3451335176c9effd"


class TestPeriodic1DRankNAlignmentAnalyzer:
    """Exercise odd transforms and fail-closed maximum-rule Procrustes selection."""

    def test_installed_distributions_match_selected_owner_revisions(self) -> None:
        """The synchronized environment retains both authorized immutable revisions."""
        expected = (
            (
                "projectkoios-optimization",
                "https://github.com/eragasa/projectkoios-optimization.git",
                _OPTIMIZATION_REVISION,
            ),
            (
                "projectkoios-physkit",
                "https://github.com/eragasa/projectkoios-physkit.git",
                _PHYSKIT_REVISION,
            ),
        )
        for package, url, revision in expected:
            direct_url_text = distribution(package).read_text("direct_url.json")
            assert direct_url_text is not None
            direct_url = json.loads(direct_url_text)
            assert direct_url["url"] == url
            assert direct_url["vcs_info"]["commit_id"] == revision
            assert direct_url["vcs_info"]["requested_revision"] == revision

    @staticmethod
    def _field(
        axis: npt.NDArray[np.float64],
    ) -> npt.NDArray[np.complex128]:
        """Return a finite-support Hermitian rank-three matrix field."""
        phase = 2.0 * np.pi * axis
        field = np.zeros((axis.size, 3, 3), dtype=np.complex128)
        field[:, 0, 0] = 0.8 + 0.2 * np.cos(phase)
        field[:, 1, 1] = -0.4 + 0.1 * np.sin(phase)
        field[:, 2, 2] = 0.15 - 0.05 * np.cos(phase)
        off_diagonal = 0.07 * np.exp(1.0j * phase)
        field[:, 0, 1] = off_diagonal
        field[:, 1, 0] = off_diagonal.conjugate()
        return field

    def test_physkit_odd_transform_preserves_physical_correlation(self) -> None:
        """The D1 mesh and shifted evaluation retain units, basis, and identities."""
        construction_size = 513
        evaluation_size = 8191
        construction_axis = -0.5 + np.arange(
            construction_size, dtype=np.float64
        ) / float(construction_size)
        construction = self._field(construction_axis)
        mesh = CenteredUniformMesh(1, construction_size, (0.0,))
        samples = FinitePeriodicMatrixSamples.from_array(
            mesh=mesh,
            matrix_samples=construction,
            energy_unit=Unitless(),
            energy_reference="D1-E-ref-zero",
            basis_identifier="D1-rank-three-retained-basis",
        )

        transform = FinitePeriodicMatrixFourierTransformer(source=samples).result()
        assert tuple(
            int(value) for value in transform.series.integer_modes[:, 0]
        ) == tuple(range(-256, 257))
        assert transform.series.energy_unit == Unitless()
        assert transform.series.energy_reference == "D1-E-ref-zero"
        assert transform.series.basis_identifier == "D1-rank-three-retained-basis"

        parseval = FinitePeriodicMatrixParsevalAnalyzer(transform=transform).result()
        hermiticity = FinitePeriodicMatrixHermiticityAnalyzer(
            transform=transform
        ).result()
        assert parseval.absolute_defect.magnitude < 2.0e-15
        assert hermiticity.twisted_cyclic_maximum_frobenius_defect.magnitude < 2.0e-15
        assert hermiticity.ordinary_maximum_frobenius_defect.magnitude < 2.0e-15

        modes = transform.series.integer_modes[:, 0]
        selected_indices = tuple(
            int(index) for index in np.flatnonzero(np.abs(modes) <= 1)
        )
        selected = transform.series.take(selected_indices)
        evaluation_axis = -0.5 + (
            np.arange(evaluation_size, dtype=np.float64) + 0.5
        ) / float(evaluation_size)
        evaluation = FinitePeriodicMatrixFourierTensorEvaluator(
            series=selected,
            coordinate_axes=(evaluation_axis,),
        ).result()
        assert evaluation.energy_unit == samples.energy_unit
        assert evaluation.energy_reference == samples.energy_reference
        assert evaluation.basis_identifier == samples.basis_identifier
        error = MatrixFieldErrorAnalyzer(
            approximation=evaluation.matrix_values,
            reference=self._field(evaluation_axis),
            norm_energy_scale=1.0,
        ).result()
        assert error.matrix_frobenius_maximum < 3.0e-15

        tail = SymmetricRangeTailAnalyzer1D().execute(
            transform.series,
            maximum_range=1,
            norm_energy_scale=1.0,
        )
        assert tail.retained_translations == (-1, 0, 1)
        assert tail.omitted_frobenius_l2_norm < 3.0e-15

    def test_maximum_rule_procrustes_is_oriented_and_strict(self) -> None:
        """Right actions are recovered and equality at the rank cutoff is deficient."""
        tolerance = ComplexUnitaryProcrustesTolerance(
            rank_absolute=1.0e-12,
            rank_relative=1.0e-10,
            validation_absolute=1.0e-12,
            validation_relative=1.0e-10,
            rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
        )
        source = np.zeros((1, 4, 3), dtype=np.complex128)
        source[0, :3, :] = np.eye(3, dtype=np.complex128)
        angle = 0.31
        expected = np.asarray(
            (
                (math.cos(angle), -math.sin(angle), 0.0),
                (math.sin(angle), math.cos(angle), 0.0),
                (0.0, 0.0, 1.0),
            ),
            dtype=np.complex128,
        )
        target = np.asarray(source @ expected, dtype=np.complex128)
        oriented = NumpyBatchedComplexUnitaryProcrustesSolver().solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source,
                target,
                tolerance,
            )
        )
        transformations = oriented.require_unique_right_unitary_transformations()
        assert transformations[0] == pytest.approx(expected, abs=2.0e-15)
        assert source[0] @ transformations[0] == pytest.approx(target[0], abs=2.0e-15)

        equality = 1.0e-10
        above = float(np.nextafter(equality, math.inf))
        square_source = np.stack(
            (np.eye(2, dtype=np.complex128), np.eye(2, dtype=np.complex128))
        )
        square_target = np.asarray(
            (np.diag((1.0, equality)), np.diag((1.0, above))),
            dtype=np.complex128,
        )
        rank_result = NumpyBatchedComplexUnitaryProcrustesSolver().solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                square_source,
                square_target,
                tolerance,
            )
        )
        assert rank_result.applied_rank_cutoffs == pytest.approx((equality, equality))
        assert rank_result.full_rank.tolist() == [False, True]
        assert rank_result.numerical_ranks.tolist() == [1, 2]
        with pytest.raises(ValueError, match="batch index \\(0,\\) is rank deficient"):
            rank_result.require_unique_right_unitary_transformations()
