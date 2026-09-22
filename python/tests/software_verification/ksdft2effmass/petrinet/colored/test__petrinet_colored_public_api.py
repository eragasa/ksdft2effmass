r"""Software verification of petrinet.colored public value surface.

Evidence profile: routine

Bounded artifact scope: package exports and dependency direction for the implemented
Architecture v2 value/token and marking/binding slices.

Facet and represented meaning

The artifact is the supported full-name ``ksdft2effmass.petrinet.colored`` import
surface and its inward generic dependency boundary.

Intrinsic and cross-object scope

Exact exports and the prohibition on generic imports from Workflow or concrete
scientific domains are covered. Class-local invariants are owned by class tests.

VVUQ and scientific exclusions

These structural checks establish software ownership only. They establish no
numerical verification, scientific validation, uncertainty quantification,
calculation execution, or human acceptance.
"""

from __future__ import annotations

import ast
from itertools import chain
from pathlib import Path

import pytest

import ksdft2effmass.petrinet.colored as colored

pytestmark = pytest.mark.software_verification


def collect_import_names(package_root: Path) -> set[str]:
    """Evidence ID: Owns no identifier; supports dependency evidence in this module.

    Requirement: Dependency evidence needs every syntactic import in the bounded
    package modules.

    Acceptance: The helper returns absolute modules and imported parent members for
    every parsed import statement.
    """
    trees = map(
        lambda path: ast.walk(ast.parse(path.read_text(encoding="utf-8"))),
        package_root.glob("*.py"),
    )
    nodes = tuple(chain.from_iterable(trees))
    direct = {
        alias.name
        for node in nodes
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    from_modules = {
        node.module
        for node in nodes
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    from_members = {
        f"{node.module}.{alias.name}"
        for node in nodes
        if isinstance(node, ast.ImportFrom) and node.module is not None
        for alias in node.names
    }
    relative_members = {
        alias.name
        for node in nodes
        if isinstance(node, ast.ImportFrom) and node.level > 0
        for alias in node.names
    }
    return direct | from_modules | from_members | relative_members


def test_public_api__exports__uses_exact_full_name_value_surface() -> None:
    """Evidence ID: SV-PETRINET-017

    Requirement: The implemented v2 slices export only their supported full-name
    generic value, token, marking, binding, and nominal identity records.

    Acceptance: ``__all__`` exactly equals the fixed documented name inventory.
    """
    assert colored.__all__ == [
        "ColoredPetriNetArcDefinition",
        "ColoredPetriNetArcIdentity",
        "ColoredPetriNetBinding",
        "ColoredPetriNetBindingAssignment",
        "ColoredPetriNetBindingSelector",
        "ColoredPetriNetBindingSelectorIdentity",
        "ColoredPetriNetBindingVariableIdentity",
        "ColoredPetriNetColorDefinition",
        "ColoredPetriNetColorIdentity",
        "ColoredPetriNetDefinition",
        "ColoredPetriNetDefinitionIdentity",
        "ColoredPetriNetDefinitionValidator",
        "ColoredPetriNetEnablementFailure",
        "ColoredPetriNetEnablementFailureCode",
        "ColoredPetriNetEnablementFailureIdentity",
        "ColoredPetriNetEnablementResult",
        "ColoredPetriNetEnablementResultIdentity",
        "ColoredPetriNetExpressionEvaluator",
        "ColoredPetriNetExpressionEvaluatorIdentity",
        "ColoredPetriNetFiringAudit",
        "ColoredPetriNetFiringFailure",
        "ColoredPetriNetFiringFailureCode",
        "ColoredPetriNetFiringFailureIdentity",
        "ColoredPetriNetFiringInput",
        "ColoredPetriNetFiringOutcomeKind",
        "ColoredPetriNetFiringResult",
        "ColoredPetriNetFiringResultIdentity",
        "ColoredPetriNetGuardEvaluationResult",
        "ColoredPetriNetGuardExpression",
        "ColoredPetriNetGuardOperator",
        "ColoredPetriNetInhibitorEvaluation",
        "ColoredPetriNetInhibitorPattern",
        "ColoredPetriNetInputInscription",
        "ColoredPetriNetInputMode",
        "ColoredPetriNetMarking",
        "ColoredPetriNetMarkingIdentity",
        "ColoredPetriNetMarkingValidator",
        "ColoredPetriNetOrderingPolicyIdentity",
        "ColoredPetriNetOutputInscription",
        "ColoredPetriNetPlaceDefinition",
        "ColoredPetriNetPlaceIdentity",
        "ColoredPetriNetPlaceMarking",
        "ColoredPetriNetProducedToken",
        "ColoredPetriNetSelectionDirective",
        "ColoredPetriNetSelectionDirectiveIdentity",
        "ColoredPetriNetSelectionFailureCode",
        "ColoredPetriNetSelectionOutcomeKind",
        "ColoredPetriNetSelectionPolicy",
        "ColoredPetriNetSelectionResult",
        "ColoredPetriNetSelectionResultIdentity",
        "ColoredPetriNetToken",
        "ColoredPetriNetTokenIdentity",
        "ColoredPetriNetTokenOccurrence",
        "ColoredPetriNetTokenPattern",
        "ColoredPetriNetTokenTemplate",
        "ColoredPetriNetTransitionDefinition",
        "ColoredPetriNetTransitionEnabler",
        "ColoredPetriNetTransitionEnablerIdentity",
        "ColoredPetriNetTransitionFirer",
        "ColoredPetriNetTransitionFirerIdentity",
        "ColoredPetriNetTransitionIdentity",
        "ColoredPetriNetValidationIssue",
        "ColoredPetriNetValidationIssueCode",
        "ColoredPetriNetValidationResult",
        "ColoredPetriNetValue",
        "ColoredPetriNetValueExpression",
        "ColoredPetriNetValueExpressionKind",
        "ColoredPetriNetValueKind",
    ]


def test_artifact__dependency__excludes_domain_imports() -> None:
    """Evidence ID: SV-PETRINET-018

    Requirement: The generic package must not depend on Workflow, calculator,
    integration, persistence, or scientific-domain owners.

    Acceptance: No absolute or relative import in the implemented package resolves
    to a prohibited package prefix.
    """
    package_root = Path(colored.__file__).parent
    prohibited = (
        "ksdft2effmass.workflows",
        "ksdft2effmass.calculators",
        "ksdft2effmass.integration",
        "ksdft2effmass.persistence",
        "ksdft2effmass.periodic",
        "ksdft2effmass.ksdft",
        "workflows",
        "calculators",
        "integration",
        "persistence",
        "periodic",
        "ksdft",
    )
    imported = collect_import_names(package_root)
    assert not any(name.startswith(prohibited) for name in imported)
