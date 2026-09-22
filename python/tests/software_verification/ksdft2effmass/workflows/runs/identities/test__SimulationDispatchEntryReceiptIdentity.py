r"""Software verification of ``SimulationDispatchEntryReceiptIdentity``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-entry receipt identity DataObject.

Facet and represented meaning

This module verifies the exact nonempty identity-value contract.

Intrinsic and cross-object scope

Receipt correlation remains with ``SimulationDispatchEntryReceipt`` evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no persistence, execution,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import SimulationDispatchEntryReceiptIdentity

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchEntryReceiptIdentity


class TestSimulationDispatchEntryReceiptIdentity:
    """Own software evidence for ``SimulationDispatchEntryReceiptIdentity``."""

    def test_constructor__value__requires_nonempty_exact_text(self) -> None:
        """Accept only a nonempty built-in string.

        Evidence ID: SV-WFR-DISPATCH-ENTRY-RECEIPT-IDENTITY-001
        """
        assert SUT("receipt.one").value == "receipt.one"
        with pytest.raises(ValueError):
            SUT("")
        with pytest.raises(TypeError):
            SUT(1)  # type: ignore[arg-type]
