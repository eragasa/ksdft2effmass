r"""Software verification of the PhysKit-backed PIAB1D study evaluator."""

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.model_systems.piab1d import (
    Piab1dResidualStudyEvaluator,
    Piab1dStudyInputDeserializer,
)

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
        definition = Piab1dStudyInputDeserializer().execute(
            self.definition_bytes()
        )
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
        np.testing.assert_allclose(
            retained @ (weights[:, None] * retained).T,
            result.projector.magnitude,
            atol=256.0 * np.finfo(np.float64).eps,
        )
        assert not result.projector.magnitude.flags.writeable

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
