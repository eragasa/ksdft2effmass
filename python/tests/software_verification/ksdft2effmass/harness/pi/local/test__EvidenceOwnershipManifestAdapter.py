r"""Software verification of ``EvidenceOwnershipManifestAdapter``.

Facet and represented meaning

The module verifies adaptation of retained evidence ownership metadata.

Intrinsic and cross-object scope

``EvidenceOwnershipManifestAdapter`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes compatibility behavior only, not scientific validation or UQ.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi.local import EvidenceOwnershipManifestAdapter

from .conftest import repository_root

pytestmark = pytest.mark.software_verification
SUT = EvidenceOwnershipManifestAdapter


def test_method__execute__maps_retained_boundary_owner_to_exact_agreement() -> None:
    """Evidence ID: SV-HL-004

    Requirement: Retained ``boundary_owned`` evidence maps to artifact-owned
    nondirectional
    agreement while preserving participant and evidence identities.

    Method: Adapt the accepted P1 evidence ownership manifest and select its CPN wire
    contract.

    Oracle: The accepted compatibility contract fixes the owner, relation, participants,
    direction, and four evidence identifiers.

    Acceptance: Adaptation passes and every represented field equals the fixed values.

    Interpretation: Failure identifies compatibility or retained-fixture drift.

    Limitations: The test does not establish CPN semantic correctness, scientific
    validity, or UQ.
    """
    root = repository_root()
    path = (
        root
        / ".pi/evidence/backend-neutral-cpn-P1-contract/test-ownership-manifest.json"
    )
    result = EvidenceOwnershipManifestAdapter().execute(path.read_bytes())
    assert result.validation.status == "PASS"
    relation = next(
        item
        for item in cast(Any, result.value)
        if item.module_path.endswith("test__workflow_cpn_v1_python_json_contract.py")
    )
    assert relation.evidence_ids == (
        "SV-CPN-027",
        "SV-CPN-028",
        "SV-CPN-087",
        "SV-CPN-088",
    )
    assert relation.ownership_kind == "artifact_owned"
    assert relation.owner_id == (
        "version-1 CPN Python runtime <-> version-1 CPN JSON Schema and wire contract"
    )
    assert relation.relation_kind == "agreement"
    assert relation.left_side_id == "workflow-cpn-v1-python-runtime"
    assert relation.right_side_id == "workflow-cpn-v1-json-schema-wire-contract"
    assert relation.direction == "none"
