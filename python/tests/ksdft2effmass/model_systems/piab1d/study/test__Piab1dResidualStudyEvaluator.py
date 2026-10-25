r"""Software verification of the PhysKit-backed PIAB1D study evaluator."""

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from projectkoios.physkit.qm.piab1d.tise_fd import Piab1dTiseFdSolver

from ksdft2effmass.model_systems.piab1d import (
    Piab1dResidualStudyEvaluator,
    Piab1dStudyInputDeserializer,
)
from ksdft2effmass.model_systems.piab1d.study import evaluation as evaluation_module

pytestmark = pytest.mark.software_verification
SUT = Piab1dResidualStudyEvaluator


class TestPiab1dResidualStudyEvaluator:
    """Own software evidence for the residual-study composition."""

    @staticmethod
    def definition_bytes() -> bytes:
        path = (
            Path(__file__).resolve().parents[6]
            / "calculations"
            / "piab1d"
            / "input.json"
        )
        return path.read_bytes()

    def test_method__execute__preserves_reduction_and_quadrature_identities(
        self,
    ) -> None:
        definition = Piab1dStudyInputDeserializer().execute(self.definition_bytes())
        result = Piab1dResidualStudyEvaluator().execute(definition)

        assert result.hamiltonian.shape == (8, 8)
        assert result.hamiltonian.nonzero_count == 22
        np.testing.assert_array_equal(
            result.consistently_compressed.magnitude,
            np.zeros((8, 8)),
        )
        np.testing.assert_allclose(
            result.unmatched_compression.magnitude,
            result.discarded_sector.magnitude,
            atol=128.0 * np.finfo(np.float64).eps,
        )
        assert result.quadrature_rule is not None
        assert result.quadrature_normalized_eigenvectors is not None
        weights = result.quadrature_rule.interior_weights
        amplitudes = result.quadrature_normalized_eigenvectors.magnitude
        np.testing.assert_allclose(
            amplitudes.T @ (weights[:, None] * amplitudes),
            np.eye(8),
            atol=256.0 * np.finfo(np.float64).eps,
        )
        retained = amplitudes[:, :3]
        projector = result.reduced_hamiltonian.spectral_subspace.projector
        np.testing.assert_allclose(
            retained @ (weights[:, None] * retained).T,
            projector.magnitude,
            atol=256.0 * np.finfo(np.float64).eps,
        )
        assert not projector.magnitude.flags.writeable

    def test_method__execute__retains_exact_physkit_spectral_quantities(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The KSD result must not reconstruct PhysKit spectral quantities."""
        definition = Piab1dStudyInputDeserializer().execute(self.definition_bytes())
        solution = Piab1dTiseFdSolver(model=definition.model).solve(
            interior_points=definition.Nx_pts_interior
        )

        class FixedSolver:
            """Expose one precomputed solution through the bound-model contract."""

            def __init__(self, *, model: object) -> None:
                assert model is definition.model

            def solve(self, *, interior_points: int) -> object:
                assert interior_points == definition.Nx_pts_interior
                return solution

        monkeypatch.setattr(evaluation_module, "Piab1dTiseFdSolver", FixedSolver)

        result = Piab1dResidualStudyEvaluator().execute(definition)

        assert result.hamiltonian is solution.hamiltonian
        assert result.eigenvalues is solution.energies
        assert result.eigenvectors is solution.eigenvectors

    def test_method__execute__disabled_quadrature__retains_no_weighted_payload(
        self,
    ) -> None:
        definition = replace(
            Piab1dStudyInputDeserializer().execute(self.definition_bytes()),
            quadrature=False,
        )

        result = Piab1dResidualStudyEvaluator().execute(definition)

        assert result.quadrature_rule is None
        assert result.quadrature_normalized_eigenvectors is None
