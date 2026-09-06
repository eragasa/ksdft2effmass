r"""Software verification of ``WorkflowRunClaimCommitReceiptIdentity``.

Evidence profile: routine

Bounded artifact scope: the nominal WorkflowRun claim-commit receipt identity.

Facet and represented meaning

The identity names one exact supplied persistence commit receipt.

Intrinsic and cross-object scope

This module verifies only nominal identity construction.

VVUQ and scientific exclusions

This is software verification only and establishes no persistence operation, external
effect, scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import WorkflowRunClaimCommitReceiptIdentity

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunClaimCommitReceiptIdentity


class TestWorkflowRunClaimCommitReceiptIdentity:
    """Own nominal identity evidence for claim-commit receipts."""

    def test_constructor__nonempty_value__preserves_nominal_identity(self) -> None:
        """Construct a nonempty exact receipt identity.

        Evidence ID: SV-WFR-CLAIM-COMMIT-RECEIPT-IDENTITY-001
        """
        identity = SUT("receipt.one")
        assert identity.value == "receipt.one"
