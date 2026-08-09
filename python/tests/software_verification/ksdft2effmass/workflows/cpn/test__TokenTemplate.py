r"""Software verification of ``TokenTemplate``.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``TokenTemplate``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
``TokenTemplate`` is the sole primary SUT. Tests exercise its documented public contract
with synthetic routing inputs; exact constructor, language, enum, ordering, and
error-taxonomy rules provide the independent oracles. Collaborators only construct
inputs or expose public outcomes.

VVUQ and scientific exclusions

------------------------------
Passing means the named software contracts hold; failure may identify an implementation,
fixture, oracle transcription, environment, or public-contract inconsistency. This
module excludes numerical verification, scientific validation, uncertainty
quantification, physical correctness, persistence and engine-adapter behavior, and
cross-language conformance."""

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


def make_token_field_assignment(
    field: TokenField, value: ContractValue
) -> TokenFieldAssignment:
    """Evidence ID: Owns no identifier; supports SV-CPN-055, SV-CPN-144.

    Requirement: Provide explicit synthetic setup or assertion mechanics without
    creating an
    independent pass claim.

    Method: Construct or transform the public CPN test inputs required by the listed
    evidence
    owners. Prior helper description: local synthetic setup only.

    Oracle: The helper has no independent oracle; each supported test owns and documents
    the
    applicable contract oracle.

    Acceptance: Return the exact public object or deterministic setup consumed by every
    listed
    evidence owner, without swallowing exceptions or asserting a separate result.

    Interpretation: A helper failure blocks or invalidates its listed evidence owners
    but is not an
    independent evidence failure.

    Limitations: The helper is synthetic, supports only the complete identifier list
    above, owns no
    independent evidence ID, and establishes no numerical verification, scientific
    validation, uncertainty quantification, physical meaning, or cross-language
    conformance."""
    return TokenFieldAssignment(
        field, ValueExpression(ValueExpressionKind.LITERAL, literal=value)
    )


def test_constructor__fields__template_requires_unique_complete_assignments() -> None:
    """Evidence ID: SV-CPN-055

    Requirement: ``TokenTemplate`` preserves the exact accepted state for its
    ``fields`` contract.

    Method: Construct the public SUT and inspect retained exact public outcomes.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact state oracle.

    Acceptance: Every retained exact state assertion holds.

    Interpretation: Pass supports only this accepted-state partition; failure may
    identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    assignments = (
        make_token_field_assignment(
            TokenField.WORKFLOW_ID, ContractValue(ContractValueKind.STRING, "w")
        ),
        make_token_field_assignment(
            TokenField.RUN_ID, ContractValue(ContractValueKind.STRING, "r")
        ),
        make_token_field_assignment(
            TokenField.ATTEMPT_ID, ContractValue(ContractValueKind.STRING, "a")
        ),
        make_token_field_assignment(
            TokenField.ITERATION_INDEX, ContractValue(ContractValueKind.INTEGER, 0)
        ),
        make_token_field_assignment(
            TokenField.PROVENANCE_IDS,
            ContractValue(ContractValueKind.STRING_SEQUENCE, ()),
        ),
        make_token_field_assignment(
            TokenField.PARENT_TOKEN_IDS,
            ContractValue(ContractValueKind.STRING_SEQUENCE, ()),
        ),
    )
    assert SUT("c", assignments).assignments == assignments


def test_constructor__fields__rejects_invalid_state() -> None:
    """Evidence ID: SV-CPN-144

    Requirement: ``TokenTemplate`` rejects the documented invalid state for its
    ``fields`` contract.

    Method: Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact error-taxonomy oracle.

    Acceptance: Every retained invalid call raises the documented exact public
    exception.

    Interpretation: Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    assignments = (
        make_token_field_assignment(
            TokenField.WORKFLOW_ID, ContractValue(ContractValueKind.STRING, "w")
        ),
        make_token_field_assignment(
            TokenField.RUN_ID, ContractValue(ContractValueKind.STRING, "r")
        ),
        make_token_field_assignment(
            TokenField.ATTEMPT_ID, ContractValue(ContractValueKind.STRING, "a")
        ),
        make_token_field_assignment(
            TokenField.ITERATION_INDEX, ContractValue(ContractValueKind.INTEGER, 0)
        ),
        make_token_field_assignment(
            TokenField.PROVENANCE_IDS,
            ContractValue(ContractValueKind.STRING_SEQUENCE, ()),
        ),
        make_token_field_assignment(
            TokenField.PARENT_TOKEN_IDS,
            ContractValue(ContractValueKind.STRING_SEQUENCE, ()),
        ),
    )
    with pytest.raises(ValueError, match="missing required"):
        SUT("c", assignments[:-1])
    with pytest.raises(ValueError, match="unique"):
        SUT("c", assignments + (assignments[0],))


pytestmark = pytest.mark.software_verification
