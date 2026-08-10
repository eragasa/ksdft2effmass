r"""Software verification of human review public api and dependency boundary.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of package exports, defining-module identities, and the pure
production-module dependency boundary for the bounded review-packet API.

Intrinsic and cross-object scope

The primary owner is the human-review package/public-surface agreement. Individual
class behavior remains owned by the seven class-owned modules.

VVUQ and scientific exclusions

Passing establishes only structural software agreement. It does not establish human
acceptance, review quality, numerical verification, scientific validation, or UQ.
"""

import ast
from pathlib import Path

import pytest

import ksdft2effmass.harness.pi as public_package
from ksdft2effmass.harness.pi import (
    HumanReviewDecision,
    HumanReviewDecisionRecorder,
    HumanReviewFinding,
    HumanReviewObservation,
    HumanReviewPacket,
    HumanReviewPreparer,
    HumanReviewTarget,
)

pytestmark = pytest.mark.software_verification
PUBLIC_NAMES = (
    "HumanReviewTarget",
    "HumanReviewObservation",
    "HumanReviewFinding",
    "HumanReviewPacket",
    "HumanReviewDecision",
    "HumanReviewPreparer",
    "HumanReviewDecisionRecorder",
)


def test_public_api__package__exports_exact_defining_module_identities() -> None:
    """Evidence ID: ``SV-HARNESS-151``.

    Requirement: The seven authorized interfaces are package exports defined by
    human_review.

    Method: Resolve each name through the supported package and compare exact object
    identity
    and defining module.

    Oracle: The accepted seven-name public API and Python object identity are exact.

    Acceptance: Package values are the imported objects, appear in __all__, and share
    the exact
    defining module ksdft2effmass.harness.pi.human_review.

    Interpretation: Failure identifies missing, shadowed, or wrongly defined exports.

    Limitations: No serialization or CLI surface is authorized or checked.
    """
    expected = (
        HumanReviewTarget,
        HumanReviewObservation,
        HumanReviewFinding,
        HumanReviewPacket,
        HumanReviewDecision,
        HumanReviewPreparer,
        HumanReviewDecisionRecorder,
    )
    assert tuple(getattr(public_package, name) for name in PUBLIC_NAMES) == expected
    assert all(name in public_package.__all__ for name in PUBLIC_NAMES)
    assert {value.__module__ for value in expected} == {
        "ksdft2effmass.harness.pi.human_review"
    }


def test_artifact__dependency__excludes_external_and_workflow_boundaries() -> None:
    """Evidence ID: ``SV-HARNESS-152``.

    Requirement: The production module has no filesystem, Git, clock, network,
    subprocess,
    database, dynamic-import, workflow, or service-locator dependency.

    Method: Parse the exact production source and inspect top-level import roots and
    calls.

    Oracle: The authorized pure module needs only dataclasses, re, and lexical identity
    rules;
    the prohibited dependency/call vocabulary is explicit.

    Acceptance: Imports are exactly __future__, dataclasses, re, and identity;
    prohibited calls are
    absent.

    Interpretation: Failure identifies unauthorized external or dynamic behavior.

    Limitations: Static dependency inspection does not prove behavior of the Python
    runtime itself.
    """
    root = Path(__file__).resolve().parents[6]
    source_path = root / "python/src/ksdft2effmass/harness/pi/human_review.py"
    tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    imports = {
        node.module.split(".")[-1]
        if isinstance(node, ast.ImportFrom) and node.module
        else node.names[0].name.split(".")[0]
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
    }
    assert imports == {"__future__", "dataclasses", "re", "identity"}
    prohibited_calls = {
        "open",
        "exec",
        "eval",
        "__import__",
        "compile",
        "connect",
        "run",
        "Popen",
        "system",
    }
    assert (
        not {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        & prohibited_calls
    )
