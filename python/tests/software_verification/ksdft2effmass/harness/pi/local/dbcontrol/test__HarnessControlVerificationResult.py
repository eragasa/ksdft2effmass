r"""Software verification of ``HarnessControlVerificationResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the intrinsic behavior of
``HarnessControlVerificationResult``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessControlVerificationResult

SUT = HarnessControlVerificationResult

pytestmark = pytest.mark.software_verification


def test_constructor__reconstruction_fields__preserve_exact_values() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-result.reconstruction-fields-preserve-exact-values

    Requirement: Verification results distinguish source and reconstructed identities.

    Method: Construct the public result with distinct exact digest values.

    Oracle: Dataclass field order and supplied values are explicit public state.

    Acceptance: Semantic and raw identities remain distinct and exact.

    Interpretation: Failure indicates loss of reconstruction evidence.

    Limitations: No SQLite file is opened.
    """  # noqa: E501
    result = HarnessControlVerificationResult("ok", 0, "a", "b", "c", "d", True)
    assert (result.semantic_digest, result.reconstructed_semantic_digest) == ("a", "b")
    assert (result.raw_database_sha256, result.reconstructed_database_sha256) == (
        "c",
        "d",
    )
    assert result.projections_identical is True
