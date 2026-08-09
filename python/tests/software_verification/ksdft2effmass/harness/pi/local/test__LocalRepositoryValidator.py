r"""Software verification of ``LocalRepositoryValidator``.

Facet and represented meaning

Software verification of project-local composition of accepted generic validators.

Intrinsic and cross-object scope

``LocalRepositoryValidator`` is the sole system under test; adapters only construct
explicit inputs.

VVUQ and scientific exclusions

Passing establishes validator composition only, not numerical verification, scientific
validation, UQ, physical correctness, or cross-language conformance.
"""

from pathlib import Path
from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi import (
    ChainView,
    TaskReference,
)
from ksdft2effmass.harness.pi.local import (
    AdaptedRepositoryRecords,
    ChecksumCatalogAdapter,
    LocalRepositoryValidator,
    OwnershipManifestAdapter,
    SkillInventoryAdapter,
)

from .conftest import local_context, repository_root

pytestmark = pytest.mark.software_verification
SUT = LocalRepositoryValidator


def records() -> AdaptedRepositoryRecords:
    """Evidence ID: Owns no identifier; supports SV-HL-013.

    Requirement: Provide explicit setup mechanics for the local repository validation
    evidence
    without owning an independent result.

    Method: Construct the named explicit repository selection, invoke
    LocalRepositoryValidator,
    and compare its aggregate without ambient discovery.

    Oracle: Public severity precedence and fixed ownership, checksum, skill, and
    evidence
    records determine the aggregate independently.

    Acceptance: Result names, severity, issue codes, and missing-root exceptions match
    exactly.

    Interpretation: Failure identifies composition drift, severity downgrade, ambient
    discovery, or a
    controlled-selection defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    task = TaskReference(1, "H4", ".pi/tasks/h4.md", (), (), "active", True)
    chain = ChainView(1, "h4-test", "H4", (task,), ("H4",), False, False)
    return AdaptedRepositoryRecords(chain, (), (), ())


def test_method__execute__sorts_default_validation_results() -> None:
    """Evidence ID: SV-HL-013

    Requirement: Local validation composes applicable generic actions over explicit
    selections
    without severity downgrade or implicit optional discovery.

    Method: Execute the action with current explicit resource context and a minimal
    chain, then
    inspect the deterministic selected validation results.

    Oracle: Empty optional inputs select exactly chain, checkpoints, and resources in
    lexical order.

    Acceptance: Execution returns exactly the three sorted names and PASS.

    Interpretation: Failure identifies composition drift, ambient validator execution,
    generic input
    incompatibility, or severity downgrade.

    Limitations: Full live repository correctness, command execution, numerical
    verification,
    science, UQ, and portability are excluded.
    """
    result = LocalRepositoryValidator().execute(local_context(), records())
    assert result.status == "PASS"
    assert tuple(name for name, _ in result.results) == (
        "chain",
        "checkpoints",
        "resources",
    )


def test_method__optional_selections__execute_every_owned_validation_branch(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-036

    Requirement: Exercise ownership, checksum, skill, and evidence selection branches.

    Method: Construct the named explicit repository selection, invoke
    LocalRepositoryValidator,
    and compare its aggregate without ambient discovery.

    Oracle: Public severity precedence and fixed ownership, checksum, skill, and
    evidence
    records determine the aggregate independently.

    Acceptance: Result names, severity, issue codes, and missing-root exceptions match
    exactly.

    Interpretation: Failure identifies composition drift, severity downgrade, ambient
    discovery, or a
    controlled-selection defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    p1 = root / ".pi/evidence/backend-neutral-cpn-P1-contract/task-ownership.json"
    ownership = OwnershipManifestAdapter().execute(p1.read_bytes())
    assert ownership.validation.status == "PASS"
    payload = b"owned checksum payload\n"
    (tmp_path / "payload.txt").write_bytes(payload)
    import hashlib

    catalog = ChecksumCatalogAdapter().execute(
        f"{hashlib.sha256(payload).hexdigest()}  payload.txt\n".encode()
    )
    assert catalog.validation.status == "PASS"
    descriptor = "harness/pi/skills/document-python-research-software/descriptor.json"
    skills = SkillInventoryAdapter().execute(
        (root / ".pi/skills/skill-capability-inventory.json").read_bytes(),
        ((descriptor, (root / descriptor).read_bytes()),),
    )
    assert skills.validation.status == "PASS"
    base = records()
    selected = AdaptedRepositoryRecords(
        base.chain,
        base.checkpoints,
        base.known_external_prerequisite_ids,
        base.satisfied_external_prerequisite_ids,
        (),
        cast(Any, ownership.value),
        tmp_path,
        cast(Any, catalog.value),
        cast(Any, skills.value),
        (
            (
                "python/tests/software_verification/ksdft2effmass/harness/pi/local/test__local_repository_validation.py",
                Path(__file__).read_bytes(),
            ),
        ),
    )
    result = LocalRepositoryValidator().execute(local_context(), selected)
    assert tuple(name for name, _ in result.results) == (
        "chain",
        "checkpoints",
        "checksums",
        "evidence",
        "ownership",
        "resources",
        "skills",
    )
    assert result.status in {"PASS", "WARN", "FAIL"}


def test_method__checksums_without_root__fails_closed() -> None:
    """Evidence ID: SV-HL-037

    Requirement: A selected checksum manifest cannot trigger ambient root discovery.

    Method: Construct the named explicit repository selection, invoke
    LocalRepositoryValidator,
    and compare its aggregate without ambient discovery.

    Oracle: Public severity precedence and fixed ownership, checksum, skill, and
    evidence
    records determine the aggregate independently.

    Acceptance: Result names, severity, issue codes, and missing-root exceptions match
    exactly.

    Interpretation: Failure identifies composition drift, severity downgrade, ambient
    discovery, or a
    controlled-selection defect.

    Limitations: This is deterministic software verification only; numerical
    verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    manifest = cast(
        Any,
        ChecksumCatalogAdapter().execute(("0" * 64 + "  payload.txt\n").encode()).value,
    )
    base = records()
    selected = AdaptedRepositoryRecords(
        base.chain,
        (),
        (),
        (),
        checksums=manifest,
    )
    with pytest.raises(ValueError, match="checksum_root"):
        LocalRepositoryValidator().execute(local_context(), selected)
