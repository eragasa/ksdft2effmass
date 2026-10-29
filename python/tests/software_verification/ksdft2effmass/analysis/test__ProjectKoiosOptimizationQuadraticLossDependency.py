"""Software verification of the pinned optimization quadratic-loss dependency.

These tests establish consuming-project API and bounded numerical behavior only. They
do not define HSH normalization, select a backend for a campaign, or establish
scientific model adequacy.
"""

from __future__ import annotations

import json
import math
from importlib.metadata import distribution
from typing import Protocol, cast

import numpy as np
import numpy.typing as npt
import pytest
from projectkoios.optimization.quadratic.quadratic import (
    PositiveDefiniteQuadraticLoss,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]

_EXPECTED_COMMIT = "ef608716ae9f515f56406dd517c1a8b7487d3391"


class _SparseMatrixView(Protocol):
    def toarray(self) -> npt.NDArray[np.float64]: ...


class TestProjectKoiosOptimizationQuadraticLossDependency:
    """Own consuming-project smoke evidence for the pinned quadratic facade."""

    def test_installed_distribution__binds_exact_owner_commit(self) -> None:
        """The resolved wheel retains the authorized immutable Git revision."""
        direct_url_text = distribution("projectkoios-optimization").read_text(
            "direct_url.json"
        )
        assert direct_url_text is not None
        direct_url = json.loads(direct_url_text)

        assert direct_url["url"] == (
            "https://github.com/eragasa/projectkoios-optimization.git"
        )
        assert direct_url["vcs_info"]["commit_id"] == _EXPECTED_COMMIT
        assert direct_url["vcs_info"]["requested_revision"] == _EXPECTED_COMMIT

    def test_public_facade__evaluates_dense_unit_free_quadratic(self) -> None:
        """The default facade preserves tuple state and completed-square behavior."""
        loss = PositiveDefiniteQuadraticLoss(
            (1.0, -2.0),
            ((4.0, 1.0), (1.0, 3.0)),
            0.25,
        )

        assert loss.center == (1.0, -2.0)
        assert loss.matrix == ((4.0, 1.0), (1.0, 3.0))
        assert loss.minimum_squared_loss == 0.25
        assert loss.dimension == 2
        assert loss.sparse is False
        assert loss.squared_loss((3.0, -1.0)) == pytest.approx(
            23.25, rel=0.0, abs=4.0e-15
        )
        assert loss.root_loss((3.0, -1.0)) == pytest.approx(
            math.sqrt(23.25), rel=0.0, abs=1.0e-15
        )

    def test_public_facade__evaluates_sparse_unit_free_quadratic(self) -> None:
        """Explicit sparse selection preserves the same bounded loss behavior."""
        loss = PositiveDefiniteQuadraticLoss(
            (1.0, -2.0),
            ((4.0, 1.0), (1.0, 3.0)),
            0.25,
            sparse=True,
        )

        assert loss.center == (1.0, -2.0)
        assert loss.minimum_squared_loss == 0.25
        assert loss.dimension == 2
        assert loss.sparse is True
        sparse_matrix = cast(_SparseMatrixView, loss.matrix)
        assert np.array_equal(
            sparse_matrix.toarray(), np.asarray(((4.0, 1.0), (1.0, 3.0)))
        )
        assert loss.squared_loss((3.0, -1.0)) == pytest.approx(
            23.25, rel=0.0, abs=4.0e-15
        )
