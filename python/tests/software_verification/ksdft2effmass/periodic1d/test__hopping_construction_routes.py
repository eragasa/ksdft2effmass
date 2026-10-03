"""Software verification of periodic-1D hopping construction-route distinctions.

Evidence profile: routine

Facet and represented meaning
-----------------------------
The artifact distinguishes complete finite-mesh operator representations from effective
models constructed by symmetric truncation or weighted least-squares fitting.

Intrinsic and cross-object scope
--------------------------------
Exact route-result types, retained-operator identity, matrix rank, and effective-model
identity are covered using synthetic scalar hopping data.

VVUQ and scientific exclusions
------------------------------
Passing establishes software classification only, not approximation accuracy,
convergence, scientific validation, or uncertainty quantification.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_fits import BlockHoppingLeastSquaresFitter1D
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    EnergyReference,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.periodic import (
    PeriodicHermiticityStatus,
    PeriodicOperatorReference,
    PeriodicRetainedOperator,
    PeriodicRetainedOperatorConstructionKind,
    PeriodicRetainedSubspace,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)
from ksdft2effmass.periodic1d import (
    Periodic1DCompleteHoppingRepresentationResult,
    Periodic1DFittedHoppingEffectiveModelResult,
    Periodic1DTruncatedHoppingEffectiveModelResult,
)
from ksdft2effmass.solid_state import (
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformResult1D,
    ReciprocalOperatorSamples1D,
)

pytestmark = pytest.mark.software_verification


class TestPeriodic1DHoppingConstructionRoutes:
    """Own route-classification evidence for one synthetic retained operator."""

    @staticmethod
    def make_retained_operator() -> PeriodicRetainedOperator:
        """Return one rank-one exact retained operator identity."""
        parent = PeriodicOperatorReference("parent", "parent-H", "ambient", 1)
        definition = PeriodicRetentionDefinition(
            "retention",
            parent,
            "retained",
            PeriodicRetentionKind.SELECTED_BANDS,
            1,
            ("band-0",),
            "mesh",
            "selection",
            (),
            "provenance",
        )
        subspace = PeriodicRetainedSubspace(
            definition,
            "ambient",
            1,
            "frame",
            "spinless",
            "scalar",
            "periodic-sewing",
            "subspace-provenance",
        )
        return PeriodicRetainedOperator(
            "retained-H",
            parent,
            subspace,
            PeriodicRetainedOperatorConstructionKind.INVARIANT_RESTRICTION,
            EnergyReference("explicit zero", "dimensionless"),
            PeriodicHermiticityStatus.DECLARED_HERMITIAN,
            "operator-provenance",
        )

    @staticmethod
    def make_samples() -> ReciprocalOperatorSamples1D:
        """Return two scalar matrices on a complete centered mesh."""
        coordinates = VectorQuantity(np.asarray([-0.5, 0.0]), Unitless())
        matrices = tuple(
            ComplexMatrixQuantity(np.asarray([[value]]), Unitless())
            for value in (1.0, 2.0)
        )
        return ReciprocalOperatorSamples1D(
            coordinates, ScalarQuantity(1.0, Unitless()), matrices
        )

    @classmethod
    def make_transform(cls) -> ReciprocalOperatorFourierTransformResult1D:
        """Return one complete two-point finite Fourier transform."""
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        return ReciprocalOperatorFourierTransformer1D().execute(
            cls.make_samples(), mesh, 0.0, 1.0e-14
        )

    def test_artifact__complete_transform__is_operator_representation(self) -> None:
        """Evidence ID: SV-PERIODIC1D-HOPPING-ROUTES-001

        Requirement: A complete centered-mesh Fourier transform is explicitly typed as
        a representation of an exact retained operator, not an effective model.

        Acceptance: The result preserves the exact operator and complete transform.
        """
        operator = self.make_retained_operator()
        transform = self.make_transform()
        result = Periodic1DCompleteHoppingRepresentationResult(operator, transform)
        assert result.retained_operator is operator
        assert result.transform is transform
        assert not isinstance(result, Periodic1DTruncatedHoppingEffectiveModelResult)

    def test_artifact__truncation__constructs_effective_model(self) -> None:
        """Evidence ID: SV-PERIODIC1D-HOPPING-ROUTES-002

        Requirement: Symmetric finite-range truncation constructs a separately
        identified effective model while retaining its complete source result.

        Acceptance: The result exposes exactly the truncation's finite-range model.
        """
        truncation = BlockHoppingTruncator1D().execute(
            self.make_transform().hopping_model, 0
        )
        result = Periodic1DTruncatedHoppingEffectiveModelResult(
            "effective.truncated", self.make_retained_operator(), truncation
        )
        assert result.effective_model_id == "effective.truncated"
        assert result.model is truncation.truncated

    def test_artifact__weighted_fit__constructs_effective_model(self) -> None:
        """Evidence ID: SV-PERIODIC1D-HOPPING-ROUTES-003

        Requirement: Weighted least-squares fitting constructs a separately identified
        effective model and remains distinct from truncation and complete transform.

        Acceptance: The result exposes exactly the fit's coefficient model.
        """
        samples = self.make_samples()
        fit = BlockHoppingLeastSquaresFitter1D().execute(
            samples, (0,), VectorQuantity(np.ones(2), Unitless())
        )
        result = Periodic1DFittedHoppingEffectiveModelResult(
            "effective.fitted", self.make_retained_operator(), fit
        )
        assert result.effective_model_id == "effective.fitted"
        assert result.model is fit.fitted_model
        assert not isinstance(result, Periodic1DTruncatedHoppingEffectiveModelResult)
