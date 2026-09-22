r"""Software verification of ``PlaneWaveBackendCompilationCompiled``.

Evidence profile: routine

Bounded artifact scope: the successful portable-to-backend compilation result.

Facet and represented meaning

The module verifies the exact successful outcome tag and complete immutable backend
binding returned by calculator-neutral compilation.

Intrinsic and cross-object scope

``PlaneWaveBackendCompilationCompiled`` is the sole system under test. Backend
selection, native rendering, calculator execution, and binding production are excluded.

VVUQ and scientific exclusions

This is software verification with synthetic identities. It establishes no numerical
verification, scientific validation, uncertainty quantification, backend equivalence,
or human acceptance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.calculators.dft.pw import (
    PlaneWaveBackendBinding,
    PlaneWaveBackendBindingIdentity,
    PlaneWaveBackendCompilationCompiled,
    PlaneWaveBackendCompilationOutcome,
    PlaneWaveBackendIdentity,
    PlaneWaveBackendSupplement,
    PlaneWaveBackendSupplementIdentity,
    PlaneWaveEnergyCutoff,
    PlaneWaveNativeConfigurationIdentity,
    PlaneWaveObservationRequirementIdentity,
    PlaneWavePhysicalModelIdentity,
    PlaneWaveReciprocalMesh,
    PlaneWaveSimulationSpecification,
    PlaneWaveSimulationSpecificationIdentity,
)
from ksdft2effmass.units import UnitIdentity, UnitScalar

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveBackendCompilationCompiled


class TestPlaneWaveBackendCompilationCompiled:
    """Own software evidence for successful backend-compilation results."""

    @staticmethod
    def binding() -> PlaneWaveBackendBinding:
        """Return one complete synthetic backend binding for consuming tests.

        Evidence ID: Helper owns no identifier.

        Requirement: Supply exact immutable specification and supplement state to the
        result tests without reproducing backend compilation behavior.

        Acceptance: Return one valid complete ``PlaneWaveBackendBinding``.
        """
        return PlaneWaveBackendBinding(
            PlaneWaveBackendBindingIdentity("binding.synthetic"),
            PlaneWaveSimulationSpecification(
                PlaneWaveSimulationSpecificationIdentity("specification.synthetic"),
                PlaneWavePhysicalModelIdentity("physical-model.synthetic"),
                PlaneWaveEnergyCutoff(UnitScalar(408.0, UnitIdentity.ELECTRON_VOLT)),
                PlaneWaveReciprocalMesh((4, 4, 4), (False, False, False)),
                (PlaneWaveObservationRequirementIdentity("total-energy"),),
            ),
            PlaneWaveBackendSupplement(
                PlaneWaveBackendSupplementIdentity("supplement.synthetic"),
                PlaneWaveBackendIdentity("backend.synthetic"),
                PlaneWaveNativeConfigurationIdentity("native.synthetic"),
            ),
        )

    def test_constructor__compiled_result__retains_exact_complete_binding(self) -> None:
        """Evidence ID: SV-CALCULATOR-VERIFY-001

        Requirement: A successful compilation result carries the exact ``COMPILED``
        outcome and one complete backend binding without copying or partial state.

        Acceptance: Both fields preserve the supplied objects exactly and ordinary
        field reassignment raises ``FrozenInstanceError``.
        """
        binding = self.binding()
        result = SUT(PlaneWaveBackendCompilationOutcome.COMPILED, binding)

        assert result.outcome is PlaneWaveBackendCompilationOutcome.COMPILED
        assert result.binding is binding
        with pytest.raises(FrozenInstanceError):
            result.binding = binding  # type: ignore[misc]

    def test_constructor__outcome_and_binding__reject_wrong_semantic_types(
        self,
    ) -> None:
        """Evidence ID: SV-CALCULATOR-VERIFY-002

        Requirement: Successful compilation uses the exact closed outcome enum and
        exact backend-binding record; raw strings and unrelated values are rejected.

        Acceptance: Wrong semantic types raise ``TypeError`` while a correctly typed
        non-success outcome raises ``ValueError``.
        """
        binding = self.binding()
        with pytest.raises(TypeError, match="PlaneWaveBackendCompilationOutcome"):
            SUT("compiled", binding)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="COMPILED"):
            SUT(PlaneWaveBackendCompilationOutcome.ERROR, binding)
        with pytest.raises(TypeError, match="PlaneWaveBackendBinding"):
            SUT(
                PlaneWaveBackendCompilationOutcome.COMPILED,
                "binding.synthetic",  # type: ignore[arg-type]
            )
