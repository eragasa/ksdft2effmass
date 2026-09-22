r"""Software verification of ``DispatchDestinationIdentity``.

Evidence profile: routine

Bounded artifact scope: the public ``DispatchDestinationIdentity`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by
``DispatchDestinationIdentity``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import DispatchDestinationIdentity

pytestmark = pytest.mark.software_verification
SUT = DispatchDestinationIdentity


class TestDispatchDestinationIdentity:
    """Own software evidence for ``DispatchDestinationIdentity``."""

    def test_constructor__value__requires_nonempty_exact_text(self) -> None:
        """Accept nonempty text and reject empty or non-string identity values.

        Evidence ID: SV-WFR-DISPATCH-DESTINATION-IDENTITY-001

        Requirement: ``DispatchDestinationIdentity`` wraps one nonempty exact
        built-in string.

        Acceptance: Nonempty text constructs, empty text raises ``ValueError``, and
        an integer raises ``TypeError``.
        """
        assert SUT("identity.one").value == "identity.one"
        with pytest.raises(ValueError):
            SUT("")
        with pytest.raises(TypeError):
            SUT(1)  # type: ignore[arg-type]
