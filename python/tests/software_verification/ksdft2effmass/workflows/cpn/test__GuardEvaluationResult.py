"""Software verification for ``GuardEvaluationResult`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import GuardEvaluationResult

SUT = GuardEvaluationResult


def test_cpn_sv_p1_047_guard_result_requires_exact_boolean() -> None:
    """SV-CPN-047: admit only built-in Boolean guard results.

    Exact Python type identity is the independent oracle. Acceptance admits both
    booleans and rejects integer ``1`` with ``TypeError``. Failure permits numeric
    truthiness to leak into the declarative contract.
    """
    assert SUT(True).value is True and SUT(False).value is False
    with pytest.raises(TypeError):
        SUT(1)  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
