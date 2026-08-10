r"""Software verification of workflow cpn python public api.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

--------------------------------------
Software verification of the Workflow CPN Python public import/API surface, a runtime
software artifact rather than a physical or numerical model.

Intrinsic and cross-object scope

--------------------------------
The Workflow CPN Python public import/API surface is the primary artifact owner. Its
approved Python export contract is the exact runtime oracle within version 1 scope.

VVUQ and scientific exclusions

------------------------------
Passing confirms only the inspected Python API contract; failure indicates contract or
evidence drift. Numerical verification, scientific validation, uncertainty
quantification, physical correctness, engine execution, persistence, and cross-language
conformance are excluded."""

import pytest

import ksdft2effmass.workflows.cpn as cpn

pytestmark = pytest.mark.software_verification

EXPECTED_EXPORTS = (
    "ArcDefinition",
    "ArcDirection",
    "ColorDefinition",
    "ContractValue",
    "ContractValueKind",
    "CpnBindingError",
    "CpnContractError",
    "CpnDefinitionError",
    "CpnDefinitionValidator",
    "CpnErrorCode",
    "CpnErrorDetail",
    "CpnExpressionEvaluator",
    "CpnFiringError",
    "CpnGuardEvaluationError",
    "CpnIssueCode",
    "CpnMarking",
    "CpnMarkingError",
    "CpnMarkingValidator",
    "CpnNetDefinition",
    "CpnToken",
    "CpnValidationIssue",
    "CpnValidationResult",
    "FiringRequest",
    "FiringResult",
    "GuardEvaluationResult",
    "GuardExpression",
    "GuardOperator",
    "InputArcMode",
    "InputInscription",
    "OutcomeScope",
    "OutcomeStatus",
    "OutcomeTerminality",
    "OutputInscription",
    "PlaceDefinition",
    "PlaceMarking",
    "TokenBinding",
    "TokenField",
    "TokenFieldAssignment",
    "TokenOutcome",
    "TokenPattern",
    "TokenTemplate",
    "TransitionBinding",
    "TransitionDefinition",
    "TransitionEnablementResult",
    "TransitionEnabler",
    "TransitionFirer",
    "TransitionNotEnabledError",
    "ValueExpression",
    "ValueExpressionKind",
)


def test_artifact__public_api__exposes_approved_export_inventory() -> None:
    """Evidence ID: SV-CPN-023

    Requirement: The Workflow CPN package exposes the approved 49-name sorted, unique,
    resolvable
    public export surface.

    Method: Inspect the public ``__all__`` sequence and resolve every listed public
    attribute;
    no warnings are expected.

    Oracle: The accepted fixed literal inventory independently fixes all 49 names,
    order, and
    name-to-object identity.

    Acceptance: The sequence has length 49, equals its sorted set, and every resolved
    object has the
    listed ``__name__``.

    Interpretation: Pass supports the exercised public API surface; failure may arise
    from package or
    evidence-contract drift.

    Limitations: Import topology, member runtime behavior, scientific validation, UQ,
    and
    cross-language claims are excluded."""
    assert tuple(cpn.__all__) == EXPECTED_EXPORTS
    assert tuple(getattr(cpn, name).__name__ for name in EXPECTED_EXPORTS) == (
        EXPECTED_EXPORTS
    )
