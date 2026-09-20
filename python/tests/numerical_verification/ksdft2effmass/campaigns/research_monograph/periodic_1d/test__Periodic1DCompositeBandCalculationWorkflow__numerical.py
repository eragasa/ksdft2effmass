r"""Numerical verification of ``Periodic1DCompositeBandCalculationWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: execution-local Appendix G finite plane-wave parent matrices,
transported rank-two frames, projectors, Wilson spectra, complete block Fourier
coefficients, finite-range errors, and direct least-squares route comparisons.

Facet and represented meaning

The calculation Workflow's represented finite channels are compared with the direct
NumPy reconstruction owned by ``Periodic1DCompositeBandCalculationVerifier``.

Intrinsic and cross-object scope

The oracle independently assembles matrices, SVD transport, gauge attacks, direct
Fourier sums, eigenspectra, truncations, interpolation, and least squares without
importing production construction or analysis algorithms.

VVUQ and scientific exclusions

A pass establishes numerical verification of the finite represented calculation. It
does not establish basis convergence, material validity, polarization, topology,
scientific validation, uncertainty quantification, or human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeBandCalculationRequest,
    Periodic1DCompositeBandCalculationVerificationRequest,
    Periodic1DCompositeBandCalculationVerifier,
    Periodic1DCompositeBandCalculationWorkflow,
    Periodic1DCompositeCampaignDefinition,
    Periodic1DCompositeCampaignJsonSerializer,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.numerical_verification
SUT = Periodic1DCompositeBandCalculationWorkflow


class TestPeriodic1DCompositeBandCalculationWorkflow:
    """Own independent numerical reconstruction of calculated composite channels."""

    @staticmethod
    def repo_root() -> Path:
        """This helper owns no identifier; it locates the maintained input."""

        return Path(__file__).resolve().parents[7]

    @classmethod
    def definition(cls) -> Periodic1DCompositeCampaignDefinition:
        """This helper owns no identifier; it decodes the maintained input."""

        path = (
            cls.repo_root()
            / "calculations"
            / "research-monograph"
            / "periodic-1d"
            / "composite-input.json"
        )
        return Periodic1DCompositeCampaignJsonSerializer().deserialize(
            path.read_bytes()
        )

    @classmethod
    def request(cls) -> Periodic1DCompositeBandCalculationRequest:
        """This helper owns no identifier; it supplies explicit finite tolerances."""

        return Periodic1DCompositeBandCalculationRequest(
            cls.definition(),
            ScalarQuantity(1.0e-12, Unitless()),
            ScalarQuantity(1.0e-10, Unitless()),
            ScalarQuantity(0.0, Unitless()),
            ScalarQuantity(1.0e-12, Unitless()),
            ScalarQuantity(1.0e-10, Unitless()),
            ScalarQuantity(1.0e-10, Unitless()),
            1.0e-10,
        )

    def test_method__execute__agrees_with_independent_direct_reconstruction(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-002

        Requirement: Every calculated parent, gauge, Wilson, complete hopping,
        truncation, withheld, and direct-fit channel agrees with an independently
        implemented finite-dimensional route.

        Method: Execute the public Workflow, then pass its complete typed result to
        the direct-NumPy verifier under an explicit unitless tolerance.

        Oracle: The independent verifier's explicit plane-wave matrices, SVD transport,
        deterministic gauge attacks, direct Fourier sums, Hermitian eigenspectra,
        truncation/interpolation, and unconstrained complex least-squares route.

        Acceptance: Every parent and per-group defect is at most ``1e-11`` in the
        Appendix G dimensionless convention and both group dispositions pass.

        Interpretation: A pass establishes numerical verification of the documented
        finite composite calculation and its separate diagnostic channels.

        Limitations: This finite reconstruction does not establish basis convergence,
        material validity, polarization, topology, scientific validation, uncertainty
        quantification, or human acceptance.
        """

        calculated = SUT().execute(self.request())
        verification = Periodic1DCompositeBandCalculationVerifier().execute(
            Periodic1DCompositeBandCalculationVerificationRequest(
                calculated,
                ScalarQuantity(1.0e-11, Unitless()),
            )
        )

        assert verification.passes
        assert verification.parent_operator_maximum_absolute_defect.magnitude == 0.0
        assert verification.training_eigenvalue_maximum_absolute_defect.magnitude == 0.0
        assert verification.withheld_eigenvalue_maximum_absolute_defect.magnitude == 0.0
        low_pair, higher_pair = verification.groups
        assert low_pair.group_id == "low_pair"
        assert higher_pair.group_id == "higher_pair"
        assert low_pair.passes
        assert higher_pair.passes
        assert low_pair.source_projector_maximum_frobenius_defect.magnitude < 5.0e-12
        assert higher_pair.source_projector_maximum_frobenius_defect.magnitude < 5.0e-12
        assert low_pair.smooth_hopping_maximum_absolute_defect.magnitude < 5.0e-12
        assert higher_pair.smooth_hopping_maximum_absolute_defect.magnitude < 5.0e-12
        assert low_pair.range_diagnostic_maximum_absolute_defect.magnitude < 1.0e-11
        assert higher_pair.range_diagnostic_maximum_absolute_defect.magnitude < 1.0e-11
        assert low_pair.direct_route_maximum_absolute_defect.magnitude < 5.0e-12
        assert higher_pair.direct_route_maximum_absolute_defect.magnitude < 5.0e-12
