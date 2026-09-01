r"""Software verification of retired ``workflows.cpn`` public capability.

Evidence profile: claim_bearing

Bounded artifact scope: the retired import route, removed source package, and absence
of abbreviated compatibility exports from the live Workflow package.

Facet and represented meaning

The artifact represents public Python capability retirement, not a colored-Petri-net
mathematical or scientific result.

Intrinsic and cross-object scope

The exact former 49-name inventory is the independent compatibility oracle. The test
checks import discovery, source-tree absence, and root-package non-aliasing together.

VVUQ and scientific exclusions

Passing establishes only removal of the former Python route and aliases. It does not
establish generic CPN semantics, historical wire equivalence, scientific validation,
uncertainty quantification, release status, or external-consumer compatibility.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

import ksdft2effmass.workflows as workflows

pytestmark = pytest.mark.software_verification
REPOSITORY_ROOT = Path(__file__).resolve().parents[5]

FORMER_EXPORTS = {
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
}


def test_artifact__public_api__retire_workflows_cpn_without_aliases() -> None:
    """Evidence ID: SV-CPN-174

    Requirement: The authorized v1 compatibility retirement removes the importable
    ``ksdft2effmass.workflows.cpn`` package and does not alias any former abbreviated
    export into the live Workflow root.

    Method: Query standard import discovery, inspect the exact source path, and compare
    the former fixed export inventory against the current package namespace.

    Oracle: The accepted former 49-name inventory and authorized legacy-retirement
    decision define the exact prohibited route and aliases.

    Acceptance: Import discovery returns ``None``, the source directory is absent, and
    every former export is absent from both ``__all__`` and the root module namespace.

    Interpretation: Failure identifies surviving import capability, source discovery,
    or a compatibility alias that would keep the retired route live.

    Limitations: Git history and versioned v1 specifications are retained but are not
    executed; this test makes no release, scientific, numerical, or VVUQ claim.

    Provenance: Human-authorized ``migration.v2.petrinet.colored.legacy-retirement``.
    """
    assert importlib.util.find_spec("ksdft2effmass.workflows.cpn") is None
    assert not (
        REPOSITORY_ROOT / "python/src/ksdft2effmass/workflows/cpn"
    ).exists()
    assert FORMER_EXPORTS.isdisjoint(workflows.__all__)
    assert all(not hasattr(workflows, name) for name in FORMER_EXPORTS)
