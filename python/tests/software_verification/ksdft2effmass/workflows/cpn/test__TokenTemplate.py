"""Software verification for ``TokenTemplate`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import (
    ContractValue,
    ContractValueKind,
    TokenField,
    TokenFieldAssignment,
    TokenTemplate,
    ValueExpression,
    ValueExpressionKind,
)

SUT = TokenTemplate


def _assign(field: TokenField, value: ContractValue) -> TokenFieldAssignment:
    return TokenFieldAssignment(
        field, ValueExpression(ValueExpressionKind.LITERAL, literal=value)
    )


def test_cpn_sv_p1_055_template_requires_unique_complete_assignments() -> None:
    """SV-CPN-055: enforce complete unique output routing assignments.

    Six required public fields form the independent oracle. Acceptance constructs
    that template and rejects a missing field and duplicate field with ``ValueError``.
    Failure permits produced tokens lacking contract routing state.
    """
    assignments = (
        _assign(TokenField.WORKFLOW_ID, ContractValue(ContractValueKind.STRING, "w")),
        _assign(TokenField.RUN_ID, ContractValue(ContractValueKind.STRING, "r")),
        _assign(TokenField.ATTEMPT_ID, ContractValue(ContractValueKind.STRING, "a")),
        _assign(
            TokenField.ITERATION_INDEX, ContractValue(ContractValueKind.INTEGER, 0)
        ),
        _assign(
            TokenField.PROVENANCE_IDS,
            ContractValue(ContractValueKind.STRING_SEQUENCE, ()),
        ),
        _assign(
            TokenField.PARENT_TOKEN_IDS,
            ContractValue(ContractValueKind.STRING_SEQUENCE, ()),
        ),
    )
    assert SUT("c", assignments).assignments == assignments
    with pytest.raises(ValueError, match="missing required"):
        SUT("c", assignments[:-1])
    with pytest.raises(ValueError, match="unique"):
        SUT("c", assignments + (assignments[0],))


pytestmark = pytest.mark.software_verification
