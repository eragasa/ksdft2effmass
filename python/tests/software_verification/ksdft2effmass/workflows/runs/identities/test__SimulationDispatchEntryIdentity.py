r"""Software verification of ``SimulationDispatchEntryIdentity``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-entry identity DataObject.

Facet and represented meaning

This module verifies the exact nonempty identity-value contract.

Intrinsic and cross-object scope

Cross-record dispatch-entry correlations remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no persistence, execution,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import SimulationDispatchEntryIdentity

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchEntryIdentity


class TestSimulationDispatchEntryIdentity:
    """Own software evidence for ``SimulationDispatchEntryIdentity``."""

    def test_constructor__value__requires_nonempty_exact_text(self) -> None:
        """Accept only a nonempty built-in string.

        Evidence ID: SV-WFR-DISPATCH-ENTRY-IDENTITY-001
        """
        assert SUT("entry.one").value == "entry.one"
        with pytest.raises(ValueError):
            SUT("")
        with pytest.raises(TypeError):
            SUT(1)  # type: ignore[arg-type]
