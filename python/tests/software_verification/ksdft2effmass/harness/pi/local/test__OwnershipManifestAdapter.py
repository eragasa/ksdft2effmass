r"""Software verification of ``OwnershipManifestAdapter``.

Facet and represented meaning

The module verifies project ownership-manifest adaptation.

Intrinsic and cross-object scope

``OwnershipManifestAdapter`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi.local import OwnershipManifestAdapter

from .conftest import repository_root

pytestmark = pytest.mark.software_verification
SUT = OwnershipManifestAdapter


def test_method__execute__preserves_scopes_and_rejects_duplicate_keys() -> None:
    """Evidence ID: SV-HL-041

    Requirement: Valid ownership scopes are preserved and ambiguous duplicate JSON keys
    fail closed.

    Method: Adapt the accepted P1 ownership bytes and one duplicate-key payload.

    Oracle: The accepted manifest contains file scopes; strict JSON admits one value per
    key.

    Acceptance: Valid adaptation passes with a file scope; duplicate input fails with no
    value.

    Interpretation: Failure indicates compatibility loss or permissive parsing.

    Limitations: The test does not validate task execution, scientific meaning, or UQ.
    """
    root = repository_root()
    path = root / ".pi/evidence/backend-neutral-cpn-P1-contract/task-ownership.json"
    result = OwnershipManifestAdapter().execute(path.read_bytes())
    assert result.validation.status == "PASS"
    scopes = [
        scope for _, _, values in cast(Any, result.value).writers for scope in values
    ]
    assert any(scope.scope_kind == "file" for scope in scopes)
    duplicate = OwnershipManifestAdapter().execute(b'{"task_id":"x","task_id":"y"}')
    assert duplicate.validation.status == "FAIL"
    assert duplicate.value is None
