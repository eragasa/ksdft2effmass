"""Software verification for exact-Hermitian Hamiltonian refinement."""

from __future__ import annotations

from typing import cast

import numpy as np
import pytest
import scipy.sparse as sp  # type: ignore[import-untyped]

from ksdft2effmass.linalg import (
    ComplexMatrixQuantity,
    CsrComplexMatrixQuantity,
    CsrRealMatrixQuantity,
    RealMatrixQuantity,
    Unitless,
)
from ksdft2effmass.operators import (
    Hamiltonian,
    HermitianHamiltonian,
)

pytestmark = pytest.mark.software_verification


class TestHermitianHamiltonian:
    """Own exact refinement from general finite Hamiltonians."""

    def test_from_hamiltonian__exact_real_hermitian__retains_matrix(self) -> None:
        matrix = RealMatrixQuantity(
            np.array([[1.0, 2.0], [2.0, 3.0]]),
            Unitless(),
        )
        hamiltonian = Hamiltonian(matrix=matrix)

        hermitian = HermitianHamiltonian.from_hamiltonian(hamiltonian)

        assert isinstance(hermitian, Hamiltonian)
        assert hermitian.matrix is matrix

    def test_from_hamiltonian__exact_complex_hermitian__retains_matrix(self) -> None:
        matrix = ComplexMatrixQuantity(
            np.array([[1.0 + 0.0j, 2.0 + 3.0j], [2.0 - 3.0j, 4.0 + 0.0j]]),
            Unitless(),
        )

        hermitian = HermitianHamiltonian.from_hamiltonian(Hamiltonian(matrix=matrix))

        assert hermitian.matrix is matrix

    def test_from_hamiltonian__exact_sparse_hermitian__retains_matrix(self) -> None:
        real_matrix = CsrRealMatrixQuantity.from_csr(
            sp.csr_array(np.array([[1.0, 2.0], [2.0, 3.0]])),
            Unitless(),
        )
        complex_matrix = CsrComplexMatrixQuantity.from_csr(
            sp.csr_array(
                np.array(
                    [
                        [1.0 + 0.0j, 2.0 + 3.0j],
                        [2.0 - 3.0j, 4.0 + 0.0j],
                    ]
                )
            ),
            Unitless(),
        )

        real = HermitianHamiltonian.from_hamiltonian(Hamiltonian(matrix=real_matrix))
        complex_hamiltonian = HermitianHamiltonian.from_hamiltonian(
            Hamiltonian(matrix=complex_matrix)
        )

        assert real.matrix is real_matrix
        assert complex_hamiltonian.matrix is complex_matrix

    def test_from_hamiltonian__nonhermitian__rejects(self) -> None:
        hamiltonian = Hamiltonian(
            matrix=RealMatrixQuantity(
                np.array([[1.0, 1.0], [0.0, 1.0]]),
                Unitless(),
            )
        )

        with pytest.raises(ValueError, match="exactly Hermitian"):
            HermitianHamiltonian.from_hamiltonian(hamiltonian)

    def test_constructor__nonhermitian__cannot_bypass_refinement(self) -> None:
        with pytest.raises(ValueError, match="exactly Hermitian"):
            HermitianHamiltonian(
                matrix=RealMatrixQuantity(
                    np.array([[1.0, 1.0], [0.0, 1.0]]),
                    Unitless(),
                )
            )

    def test_from_hamiltonian__wrong_type__rejects(self) -> None:
        invalid = cast(Hamiltonian, RealMatrixQuantity(np.eye(2), Unitless()))

        with pytest.raises(TypeError, match="must be Hamiltonian"):
            HermitianHamiltonian.from_hamiltonian(invalid)
