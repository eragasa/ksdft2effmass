r"""Software verification of ``ObligationIdentity``.

Evidence profile: routine

Bounded artifact scope: the public ``ObligationIdentity`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by ``ObligationIdentity``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import ObligationIdentity

pytestmark = pytest.mark.software_verification
SUT = ObligationIdentity


class TestObligationIdentity:
    """Own software evidence for ``ObligationIdentity``."""

    def test_constructor__value__requires_nonempty_exact_text(self) -> None:
        """Accept nonempty text and reject empty or non-string identity values.

        Evidence ID: SV-WFR-OBLIGATION-IDENTITY-001

        Requirement: ``ObligationIdentity`` wraps one nonempty exact built-in string.

        Acceptance: Nonempty text constructs, empty text raises ``ValueError``, and
        an integer raises ``TypeError``.
        """
        assert SUT("identity.one").value == "identity.one"
        with pytest.raises(ValueError):
            SUT("")
        with pytest.raises(TypeError):
            SUT(1)  # type: ignore[arg-type]
