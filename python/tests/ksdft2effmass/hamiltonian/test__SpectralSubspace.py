"""Software verification for the spectral-subspace abstraction boundary."""

from __future__ import annotations

import inspect

import pytest

from ksdft2effmass.hamiltonian import SpectralSubspace

pytestmark = pytest.mark.software_verification


class TestSpectralSubspace:
    """Own the intentionally abstract general spectral-subspace contract."""

    def test_class__unimplemented_general_case__is_abstract(self) -> None:
        assert inspect.isabstract(SpectralSubspace)
        assert {
            "full_dimension",
            "dimension",
            "projector",
            "reduction_map",
            "embedding_map",
        }.issubset(SpectralSubspace.__abstractmethods__)
