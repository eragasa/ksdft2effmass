r"""Software verification of plane-wave study package exports.

Evidence profile: routine

Bounded artifact scope: package-root visibility of private stabilization contracts.

Facet and represented meaning

The artifact is a cross-package smoke test that verifies representative plane-wave
study contracts remain internal to their revisable implementation modules.

Intrinsic and cross-object scope

The package export surface across analysis, calculators, and campaigns is primary.
Class invariants, numerical behavior, execution, and serialization are excluded.

VVUQ and scientific exclusions

This is structural software verification only. It establishes no physical
correctness, scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

import ksdft2effmass.analysis as analysis
import ksdft2effmass.calculators as calculators
import ksdft2effmass.campaigns as campaigns

pytestmark = pytest.mark.software_verification


class TestPlaneWaveStudyPackageExports:
    """Own the private stabilization package-export smoke test."""

    def test_artifact__package_roots__keep_stabilization_contracts_internal(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-EXPORTS-001

        Requirement: Initial QoI, parameter-study, plane-wave, and campaign contracts
        remain absent from package roots until separate public stabilization.

        Acceptance: Representative analysis, calculator, and campaign contract names
        are not attributes of their corresponding package roots.
        """
        assert not hasattr(analysis, "ParameterStudyRevision")
        assert not hasattr(analysis, "FiniteSequenceParameterStudyRefiner")
        assert not hasattr(calculators, "PlaneWaveBackendBinding")
        assert not hasattr(campaigns, "PlaneWaveParameterStudyCompiler")
