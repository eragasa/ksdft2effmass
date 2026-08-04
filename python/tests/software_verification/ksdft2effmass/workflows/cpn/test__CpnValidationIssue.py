"""Software verification for ``CpnValidationIssue`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import CpnIssueCode, CpnValidationIssue

SUT = CpnValidationIssue


def test_cpn_sv_p1_045_issue_owns_typed_canonical_context() -> None:
    """SV-CPN-045: validate issue fields and canonicalize related identities.

    Exact public tuple storage and exception taxonomy are the oracles. Acceptance
    requires sorting, ``TypeError`` for a string code, and ``ValueError`` for an
    empty message. Failure destabilizes validation diagnostics.
    """
    issue = SUT(CpnIssueCode.UNKNOWN_COLOR, ("places", "p"), ("z", "a"), "unknown")
    assert issue.related_ids == ("a", "z")
    with pytest.raises(TypeError):
        SUT("unknown_color", (), (), "bad")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT(CpnIssueCode.UNKNOWN_COLOR, (), (), "")


pytestmark = pytest.mark.software_verification
