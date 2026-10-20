"""Software verification for :class:`NumpyOperatorField`."""

from __future__ import annotations

from typing import cast

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.numpy.typing import Complex128Array

from ksdft2effmass.operators.representations.domains import (
    FiniteMomentumMeshDomain,
    FiniteTranslationDomain,
    MomentumSampleRole,
)
from ksdft2effmass.operators.representations.fields import (
    MatrixFieldABC,
    NumpyGaugeField,
    NumpyOperatorField,
    OperatorFieldABC,
    ProjectorFieldABC,
)

pytestmark = pytest.mark.software_verification


class TestNumpyOperatorField:
    """Establish operator-role, shape, domain, and immutable storage contracts."""

    @staticmethod
    def momentum_domain() -> FiniteMomentumMeshDomain:
        """Return one three-point momentum domain."""
        return FiniteMomentumMeshDomain(
            "construction-k-mesh",
            CenteredUniformMesh(1, 3, (0.0,)),
            "centered-reduced-reciprocal.v1",
            MomentumSampleRole.construction,
        )

    @staticmethod
    def square_values() -> Complex128Array:
        """Return three finite rank-two matrices."""
        return np.zeros((3, 2, 2), dtype=np.complex128)

    def test_construction__implements_only_operator_semantic_role(self) -> None:
        """The operator leaf has its intended nominal interfaces."""
        field = NumpyOperatorField(self.momentum_domain(), self.square_values())

        assert isinstance(field, MatrixFieldABC)
        assert isinstance(field, OperatorFieldABC)
        assert not isinstance(field, ProjectorFieldABC)
        assert field.dimension == 2

    def test_construction__does_not_infer_hermiticity(self) -> None:
        """A non-Hermitian matrix remains valid operator-role data."""
        values = self.square_values()
        values[0, 0, 1] = 1.0j

        field = NumpyOperatorField(self.momentum_domain(), values)

        assert field.values[0, 0, 1] == 1.0j

    def test_values__are_owned_immutable_bytes(self) -> None:
        """Caller mutation and write-flag changes cannot alter stored values."""
        caller = self.square_values()
        field = NumpyOperatorField(self.momentum_domain(), caller)
        caller[0, 0, 0] = 9.0

        assert field.values[0, 0, 0] == 0.0
        assert not field.values.flags.writeable
        with pytest.raises(ValueError):
            field.values.setflags(write=True)

    @pytest.mark.parametrize(
        ("values", "exception", "message"),
        [
            pytest.param(
                np.zeros((3, 2), dtype=np.complex128),
                ValueError,
                "shape",
                id="axes",
            ),
            pytest.param(
                np.zeros((2, 2, 2), dtype=np.complex128),
                ValueError,
                "cardinality",
                id="domain",
            ),
            pytest.param(
                np.zeros((3, 2, 3), dtype=np.complex128),
                ValueError,
                "square",
                id="square",
            ),
            pytest.param(
                np.zeros((3, 2, 2), dtype=np.complex64),
                TypeError,
                "complex128",
                id="dtype",
            ),
            pytest.param(
                np.full((3, 2, 2), np.nan + 0.0j, dtype=np.complex128),
                ValueError,
                "nonfinite",
                id="finite",
            ),
        ],
    )
    def test_construction__rejects_invalid_arrays(
        self,
        values: np.ndarray,
        exception: type[Exception],
        message: str,
    ) -> None:
        """Shape, domain correlation, dtype, and finiteness fail explicitly."""
        with pytest.raises(exception, match=message):
            NumpyOperatorField(self.momentum_domain(), cast(Complex128Array, values))

    def test_construction__rejects_wrong_domain_and_nonarray_values(self) -> None:
        """Momentum fields reject translation domains and broad array coercion."""
        translations = FiniteTranslationDomain(
            "symmetric-r1",
            ((-1,), (0,), (1,)),
            "integer-cell-translation.v1",
        )
        with pytest.raises(TypeError, match="FiniteMomentumMeshDomain"):
            NumpyOperatorField(
                cast(FiniteMomentumMeshDomain, translations), self.square_values()
            )
        with pytest.raises(TypeError, match="numpy.ndarray"):
            NumpyOperatorField(
                self.momentum_domain(), cast(Complex128Array, [[[0.0j]]])
            )

    def test_equality__requires_same_leaf_domain_and_values(self) -> None:
        """Exact equality never crosses semantic role leaves."""
        domain = self.momentum_domain()
        left = NumpyOperatorField(domain, self.square_values())
        right = NumpyOperatorField(domain, self.square_values())
        different_role = NumpyGaugeField(domain, self.square_values())

        assert left == right
        assert left != different_role
