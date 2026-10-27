r"""Software verification of ``Piab1dResidualStudyResult``.

Evidence profile: routine

Bounded artifact scope: immutable particle-in-a-box residual-study ResultObject.

Facet and represented meaning

The ResultObject retains one coherent evaluator outcome with immutable represented
arrays and diagnostics.

Intrinsic and cross-object scope

Operational array immutability and definition correlation are included.

VVUQ and scientific exclusions

This verifies result storage only, not numerical correctness, scientific validation,
uncertainty quantification, or human acceptance.
"""

from pathlib import Path

import pytest
from projectkoios.physkit.units import MatrixQuantity

from ksdft2effmass.hamiltonian import ReducedHamiltonian
from ksdft2effmass.model_systems.piab1d import (
    Piab1dResidualStudyEvaluator,
    Piab1dResidualStudyResult,
    Piab1dStudyInputDeserializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = Piab1dResidualStudyResult


class TestPiab1dResidualStudyResult:
    """Own software evidence for ``Piab1dResidualStudyResult``."""

    def test_constructor__immutable_storage__retains_evaluator_outcome(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-006

        Requirement: Result arrays are operationally immutable and correlated to the
        exact evaluated definition.

        Acceptance: The evaluator-produced projector rejects mutation and retains the
        same definition object.
        """
        root = Path(__file__).resolve().parents[6]
        definition = Piab1dStudyInputDeserializer().execute(
            (root / "calculations" / "piab1d" / "input.json").read_bytes()
        )
        result = Piab1dResidualStudyEvaluator().execute(definition)

        assert result.definition is definition
        projector = result.reduced_hamiltonian.spectral_subspace.projector
        with pytest.raises(ValueError, match="read-only"):
            projector.magnitude[0, 0] = 1.0

    def test_result__reduced_hamiltonian__binds_all_representations(self) -> None:
        root = Path(__file__).resolve().parents[6]
        definition = Piab1dStudyInputDeserializer().execute(
            (root / "calculations" / "piab1d" / "input.json").read_bytes()
        )
        result = Piab1dResidualStudyEvaluator().execute(definition)

        reduced = result.reduced_hamiltonian

        assert type(reduced) is ReducedHamiltonian
        assert reduced.spectral_subspace.full_dimension == 8
        assert reduced.spectral_subspace.dimension == 3
        assert reduced.spectral_subspace.projector.magnitude.shape == (8, 8)
        assert isinstance(reduced.matrix, MatrixQuantity)
        assert isinstance(reduced.embedded.matrix, MatrixQuantity)
        assert reduced.matrix.magnitude.shape == (3, 3)
        assert reduced.embedded.matrix.magnitude.shape == (8, 8)
