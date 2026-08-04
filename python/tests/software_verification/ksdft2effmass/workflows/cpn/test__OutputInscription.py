"""Software verification for ``OutputInscription`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import OutputInscription

SUT = OutputInscription


def test_cpn_sv_p1_049_output_inscription_rejects_empty_or_wrong_templates() -> None:
    """SV-CPN-049: require a nonempty immutable token-template sequence.

    Public constructor rejection is the method and documented cardinality/type
    invariants are the oracle. Acceptance distinguishes ``ValueError`` for empty
    tuples and ``TypeError`` for mutable/wrong entries. Failure permits no-op output.
    """
    with pytest.raises(ValueError, match="must not be empty"):
        SUT(())
    with pytest.raises(TypeError):
        SUT([])  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
