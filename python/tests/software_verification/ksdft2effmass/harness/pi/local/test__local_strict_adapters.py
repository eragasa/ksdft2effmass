r"""Software verification of local strict adapters.

Facet and represented meaning
Software verification of strict project-record to generic-record adapters.

Intrinsic and cross-object scope
The artifact owner is the selected live-record adapter boundary; exact explicit bytes,
version compatibility, sorting, and fail-closed diagnostics are checked.

VVUQ and scientific exclusions
Passing establishes adapter software behavior only and excludes numerical verification,
scientific validation, UQ, physical meaning, and cross-language conformance.
"""

import json
from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi import ProjectProfile
from ksdft2effmass.harness.pi.local import (
    AdaptAgentRecords,
    AdaptChainRecord,
    AdaptCheckpointRecords,
    AdaptChecksumCatalog,
    AdaptEvidenceOwnershipManifest,
    AdaptOwnershipManifest,
    AdaptSkillInventory,
    AdaptTaskRecords,
    SelectEvidenceModules,
)

from .conftest import local_context, repository_root

pytestmark = pytest.mark.software_verification


def test_artifact__record_adapters__normalize_explicit_inputs() -> None:
    """Evidence ID
    SV-HL-003
    Requirement
    Task, chain, checkpoint, and agent adapters consume only caller-selected bytes and
    return generic records in deterministic identity order.
    Method
    Supply the current H4 chain/activation, all explicitly referenced task bytes, one
    resolved checkpoint, and two reversed agent documents.
    Oracle
    Selected record identities and lexical ordering are fixed by the supplied
    authoritative documents and accepted adapter contract.
    Acceptance
    All adaptations pass; tasks and agents are sorted, completed H4 remains explicitly
    activated without an active task, and the checkpoint is represented as
    resolved/resumed.
    Interpretation
    Failure indicates local adapter drift, provisional input incompatibility, or fixture
    selection error.
    Limitations
    No repository discovery, command authorization, numerical result, science, UQ, or
    cross-language claim is exercised.
    """
    root = repository_root()
    chain_bytes = (root / ".pi/chains/pi-harness-incubation.chain.json").read_bytes()
    activation_bytes = (
        root / ".pi/evidence/pi-harness-incubation/H4/activation.json"
    ).read_bytes()
    chain_obj = json.loads(chain_bytes)
    documents = tuple(
        (item["record"], (root / item["record"]).read_bytes())
        for item in reversed(chain_obj["task_sequence"])
    )
    tasks = AdaptTaskRecords().execute(documents, chain_bytes, activation_bytes)
    assert tasks.validation.status == "PASS"
    task_values = cast(Any, tasks.value)
    assert [x.task_id for x in task_values] == ["H0", "H1", "H2", "H3", "H4", "H5"]
    chain = AdaptChainRecord().execute(chain_bytes, task_values, activation_bytes)
    assert chain.validation.status == "PASS"
    assert cast(Any, chain.value).active_task_id is None
    assert cast(Any, chain.value).explicitly_activated_task_ids == ("H4",)
    checkpoint_path = ".pi/checkpoints/H2-HC02-final-acceptance.json"
    checkpoints = AdaptCheckpointRecords().execute(
        ((checkpoint_path, (root / checkpoint_path).read_bytes()),)
    )
    assert checkpoints.validation.status == "PASS"
    assert cast(Any, checkpoints.value)[0].resumption_status == "resumed"
    agent_paths = (
        ".pi/agents/ksdft2effmass-harness-local-test-parity-writer.md",
        ".pi/agents/ksdft2effmass-harness-local-python-writer.md",
    )
    agents = AdaptAgentRecords().execute(
        tuple((p, (root / p).read_bytes()) for p in agent_paths)
    )
    assert agents.validation.status == "PASS"
    agent_values = cast(Any, agents.value)
    assert tuple(x.agent_id for x in agent_values) == tuple(
        sorted(x.agent_id for x in agent_values)
    )


def test_artifact__compatibility_adapters__retain_exact_inventory() -> None:
    """Evidence ID
    SV-HL-004
    Requirement
    Ownership, evidence-ownership, checksum, and skill adapters preserve accepted
    compatibility while rejecting noncanonical selections.
    Method
    Adapt retained P1 task/evidence ownership manifests, a fixed checksum catalog, and
    the single explicitly extracted document-python-research-software descriptor.
    Oracle
    H4 requires P1 task ownership to normalize independently and retained
    ``boundary_owned`` evidence to map to artifact-owned nondirectional agreement with
    preserved IDs.
    Acceptance
    P1 task adaptation passes; the boundary relation has exact owner/sides/direction and
    IDs; checksum paths sort; the explicit skill selection contains only
    document-python-research-software.
    Interpretation
    Failure identifies a compatibility defect, resource cutover defect, or stale fixture
    assumption.
    Limitations
    Checksum file contents are not validated here; capability semantics, science, UQ,
    and portability are excluded.
    """
    root = repository_root()
    p1_root = root / ".pi/evidence/backend-neutral-cpn-P1-contract"
    ownership = AdaptOwnershipManifest().execute(
        (p1_root / "task-ownership.json").read_bytes()
    )
    assert ownership.validation.status == "PASS"
    scopes = [
        scope for _, _, values in cast(Any, ownership.value).writers for scope in values
    ]
    assert any(scope.scope_kind == "file" for scope in scopes)
    evidence = AdaptEvidenceOwnershipManifest().execute(
        (p1_root / "test-ownership-manifest.json").read_bytes()
    )
    assert evidence.validation.status == "PASS"
    relations = cast(Any, evidence.value)
    boundary = next(
        relation
        for relation in relations
        if relation.module_path.endswith(
            "test__workflow_cpn_v1_python_json_contract.py"
        )
    )
    assert boundary.evidence_ids == (
        "SV-CPN-027",
        "SV-CPN-028",
        "SV-CPN-087",
        "SV-CPN-088",
    )
    assert boundary.ownership_kind == "artifact_owned"
    assert boundary.owner_id == (
        "version-1 CPN Python runtime <-> version-1 CPN JSON Schema and wire contract"
    )
    assert boundary.relation_kind == "agreement"
    assert boundary.left_side_id == "workflow-cpn-v1-python-runtime"
    assert boundary.right_side_id == "workflow-cpn-v1-json-schema-wire-contract"
    assert boundary.direction == "none"
    checksums = AdaptChecksumCatalog().execute(
        b"b" * 64 + b"  z\n" + b"a" * 64 + b"  a\n"
    )
    assert checksums.validation.status == "PASS"
    assert [x.path for x in cast(Any, checksums.value).entries] == ["a", "z"]
    inventory_path = root / ".pi/skills/skill-capability-inventory.json"
    descriptor_path = (
        "harness/pi/skills/document-python-research-software/descriptor.json"
    )
    skills = AdaptSkillInventory().execute(
        inventory_path.read_bytes(),
        ((descriptor_path, (root / descriptor_path).read_bytes()),),
    )
    assert skills.validation.status == "PASS"
    selected_skills = cast(Any, skills.value)
    assert tuple(skill.skill_id for skill in selected_skills) == (
        "document-python-research-software",
    )


def test_artifact__adapter_faults__fail_closed_without_ambient_roots() -> None:
    """Evidence ID
    SV-HL-005
    Requirement
    Strict adapters reject duplicate JSON keys, missing selected task bytes, malformed
    catalogs, and evidence outside explicit profile scopes.
    Method
    Inject one controlled malformed input for each adapter family and pass the current
    explicit ProjectProfile to evidence selection.
    Oracle
    The local PIHL diagnostic registry and profile scope rules require deterministic
    failure without fallback discovery.
    Acceptance
    Every malformed adaptation returns FAIL with no value; in-scope bytes are returned
    unchanged and outside-scope bytes produce PIHL.EVIDENCE.OUTSIDE_SCOPE.
    Interpretation
    Failure indicates an unsafe permissive adapter or an obsolete profile oracle.
    Limitations
    This samples fault classes rather than every malformed JSON token and makes no
    numerical, scientific, UQ, or portability claim.
    """
    context = local_context()
    assert isinstance(context.profile, ProjectProfile)
    duplicate = AdaptOwnershipManifest().execute(b'{"task_id":"x","task_id":"y"}')
    assert duplicate.validation.status == "FAIL" and duplicate.value is None
    malformed = AdaptChecksumCatalog().execute(b"no separator")
    assert malformed.validation.status == "FAIL" and malformed.value is None
    root = repository_root()
    chain_bytes = (root / ".pi/chains/pi-harness-incubation.chain.json").read_bytes()
    activation_bytes = (
        root / ".pi/evidence/pi-harness-incubation/H4/activation.json"
    ).read_bytes()
    chain_obj = json.loads(chain_bytes)
    missing_task = AdaptTaskRecords().execute(
        tuple(
            (item["record"], (root / item["record"]).read_bytes())
            for item in chain_obj["task_sequence"]
            if item["id"] != "H3"
        ),
        chain_bytes,
        activation_bytes,
    )
    assert missing_task.validation.status == "FAIL" and missing_task.value is None
    assert "missing selected task bytes" in missing_task.validation.issues[0].detail
    selected = SelectEvidenceModules().execute(
        (("python/tests/software_verification/x.py", b"x"),), context.profile
    )
    assert selected.value == (("python/tests/software_verification/x.py", b"x"),)
    outside = SelectEvidenceModules().execute((("docs/x.py", b"x"),), context.profile)
    assert outside.validation.issues[0].code == "PIHL.EVIDENCE.OUTSIDE_SCOPE"
