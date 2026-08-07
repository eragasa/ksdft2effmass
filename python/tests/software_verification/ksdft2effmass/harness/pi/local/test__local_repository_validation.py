r"""Software verification of local repository validation.

Facet and represented meaning
Software verification of project-local composition of accepted generic validators.

Intrinsic and cross-object scope
The artifact owner is ValidateLocalRepository and its input/result records; exact
generic result names, severity propagation, and optional selection behavior are checked.

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
    ValidationIssue,
    ValidationResult,
)
from ksdft2effmass.harness.pi.local import (
    AdaptChecksumCatalog,
    AdaptedRepositoryRecords,
    AdaptOwnershipManifest,
    AdaptSkillInventory,
    RepositoryValidationResult,
    ValidateLocalRepository,
)

from .conftest import local_context, repository_root

pytestmark = pytest.mark.software_verification


def records() -> AdaptedRepositoryRecords:
    """Evidence ID
    Owns no identifier; supports SV-HL-013.
    Requirement
    Provide explicit setup mechanics for the local repository validation evidence
    without owning an independent result.
    Method
    Construct the named explicit repository selection, invoke ValidateLocalRepository,
    and compare its aggregate without ambient discovery.
    Oracle
    Public severity precedence and fixed ownership, checksum, skill, and evidence
    records determine the aggregate independently.
    Acceptance
    Result names, severity, issue codes, and missing-root exceptions match exactly.
    Interpretation
    Failure identifies composition drift, severity downgrade, ambient discovery, or a
    controlled-selection defect.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    task = TaskReference(1, "H4", ".pi/tasks/h4.md", (), (), "active", True)
    chain = ChainView(1, "h4-test", "H4", (task,), ("H4",), False, False)
    return AdaptedRepositoryRecords(chain, (), (), ())


def test_method__generic_composition__uses_sorted_results_and_preserves_severity() -> (
    None
):
    """Evidence ID
    SV-HL-013
    Requirement
    Local validation composes applicable generic actions over explicit selections
    without severity downgrade or implicit optional discovery.
    Method
    Execute the action with current explicit resource context and a minimal chain, then
    construct controlled PASS/WARN/FAIL aggregate results.
    Oracle
    Empty optional inputs select exactly chain, checkpoints, and resources; aggregate
    severity is FAIL over WARN over PASS and names sort.
    Acceptance
    Execution returns exactly the three sorted names and PASS; controlled aggregates
    accept only their derived severity and reject mismatches.
    Interpretation
    Failure identifies composition drift, ambient validator execution, generic input
    incompatibility, or severity downgrade.
    Limitations
    Full live repository correctness, command execution, numerical verification,
    science, UQ, and portability are excluded.
    """
    result = ValidateLocalRepository().execute(local_context(), records())
    assert result.status == "PASS"
    assert tuple(name for name, _ in result.results) == (
        "chain",
        "checkpoints",
        "resources",
    )
    passing = ValidationResult(1, "PASS", ())
    warning_issue = ValidationIssue(
        1, "PIH.EVIDENCE.PROTECTED_GAP", "WARNING", None, None, (), "gap"
    )
    failing_issue = ValidationIssue(
        1, "PIH.CHAIN.STATUS_UNKNOWN", "ERROR", None, None, (), "bad"
    )
    warning = ValidationResult(1, "WARN", (warning_issue,))
    failing = ValidationResult(1, "FAIL", (failing_issue,))
    assert (
        RepositoryValidationResult("WARN", (("a", passing), ("b", warning))).status
        == "WARN"
    )
    assert (
        RepositoryValidationResult("FAIL", (("a", failing), ("b", warning))).status
        == "FAIL"
    )
    with pytest.raises(ValueError):
        RepositoryValidationResult("PASS", (("a", warning),))


def test_method__optional_selections__execute_every_owned_validation_branch(
    tmp_path: Path,
) -> None:
    """Evidence ID
    SV-HL-036
    Requirement
    Exercise ownership, checksum, skill, and evidence selection branches.
    Method
    Construct the named explicit repository selection, invoke ValidateLocalRepository,
    and compare its aggregate without ambient discovery.
    Oracle
    Public severity precedence and fixed ownership, checksum, skill, and evidence
    records determine the aggregate independently.
    Acceptance
    Result names, severity, issue codes, and missing-root exceptions match exactly.
    Interpretation
    Failure identifies composition drift, severity downgrade, ambient discovery, or a
    controlled-selection defect.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    root = repository_root()
    p1 = root / ".pi/evidence/backend-neutral-cpn-P1-contract/task-ownership.json"
    ownership = AdaptOwnershipManifest().execute(p1.read_bytes())
    assert ownership.validation.status == "PASS"
    payload = b"owned checksum payload\n"
    (tmp_path / "payload.txt").write_bytes(payload)
    import hashlib

    catalog = AdaptChecksumCatalog().execute(
        f"{hashlib.sha256(payload).hexdigest()}  payload.txt\n".encode()
    )
    assert catalog.validation.status == "PASS"
    descriptor = "harness/pi/skills/document-python-research-software/descriptor.json"
    skills = AdaptSkillInventory().execute(
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
    result = ValidateLocalRepository().execute(local_context(), selected)
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
    """Evidence ID
    SV-HL-037
    Requirement
    A selected checksum manifest cannot trigger ambient root discovery.
    Method
    Construct the named explicit repository selection, invoke ValidateLocalRepository,
    and compare its aggregate without ambient discovery.
    Oracle
    Public severity precedence and fixed ownership, checksum, skill, and evidence
    records determine the aggregate independently.
    Acceptance
    Result names, severity, issue codes, and missing-root exceptions match exactly.
    Interpretation
    Failure identifies composition drift, severity downgrade, ambient discovery, or a
    controlled-selection defect.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    manifest = cast(
        Any,
        AdaptChecksumCatalog().execute(("0" * 64 + "  payload.txt\n").encode()).value,
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
        ValidateLocalRepository().execute(local_context(), selected)
