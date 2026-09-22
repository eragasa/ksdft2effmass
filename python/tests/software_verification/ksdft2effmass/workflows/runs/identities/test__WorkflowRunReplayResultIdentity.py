r"""Software verification of ``WorkflowRunReplayResultIdentity``.

Evidence profile: routine

Bounded artifact scope: the public ``WorkflowRunReplayResultIdentity`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by
``WorkflowRunReplayResultIdentity``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import WorkflowRunReplayResultIdentity

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunReplayResultIdentity


class TestWorkflowRunReplayResultIdentity:
    """Own software evidence for ``WorkflowRunReplayResultIdentity``."""

    def test_constructor__value__requires_lowercase_sha256_text(self) -> None:
        """Accept one lowercase SHA-256 digest and reject other representations.

        Evidence ID: SV-WFR-WORKFLOW-RUN-REPLAY-RESULT-IDENTITY-001

        Requirement: ``WorkflowRunReplayResultIdentity`` wraps exactly 64 lowercase
        hexadecimal characters representing a SHA-256 digest.

        Acceptance: A 64-character lowercase hexadecimal value constructs, malformed
        text raises ``ValueError``, and an integer raises ``TypeError``.
        """
        digest = "a" * 64
        assert SUT(digest).value == digest
        with pytest.raises(ValueError):
            SUT("identity.one")
        with pytest.raises(TypeError):
            SUT(1)  # type: ignore[arg-type]
