r"""Software verification of ``HarnessControlVerificationFinding``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the intrinsic immutable structured disagreement record.

Intrinsic and cross-object scope

Construction and closed-code validation are exercised with literal inputs only.

VVUQ and scientific exclusions

This is structural software verification only; scientific validation and uncertainty
quantification are excluded.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessControlVerificationFinding

SUT = HarnessControlVerificationFinding

pytestmark = pytest.mark.software_verification


def test_constructor__fields__preserves_structured_disagreement() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-finding.structured-fields

    Requirement: A control disagreement preserves its closed code, optional path, and
    stable explanatory message as immutable public state.

    Method: Construct one exact changed-artifact finding.

    Oracle: The supplied literal values independently define the expected fields.

    Acceptance: All three fields remain exactly equal to their inputs.

    Interpretation: Failure identifies loss of structured verification information.

    Limitations: Finding aggregation is covered by verifier evidence.
    """  # noqa: E501
    finding = HarnessControlVerificationFinding(
        "changed_artifact", "harness/task-graph.json", "candidate differs"
    )
    assert (finding.code, finding.path, finding.message) == (
        "changed_artifact",
        "harness/task-graph.json",
        "candidate differs",
    )


def test_constructor__unsupported_code__raises_value_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-finding.unsupported-code

    Requirement: Verification findings reject unregistered structural identities.

    Method: Construct a finding with one unsupported literal code.

    Oracle: The documented closed verification vocabulary excludes ``unknown``.

    Acceptance: Construction raises exactly ``ValueError``.

    Interpretation: Failure indicates an open or nondeterministic finding vocabulary.

    Limitations: Supported code semantics are exercised by verifier evidence.
    """  # noqa: E501
    with pytest.raises(ValueError):
        HarnessControlVerificationFinding("unknown", None, "unsupported")
