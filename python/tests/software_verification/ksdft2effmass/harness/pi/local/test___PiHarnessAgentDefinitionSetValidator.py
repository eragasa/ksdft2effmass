r"""Software verification of ``_PiHarnessAgentDefinitionSetValidator``.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The artifact represents deterministic cross-file structural validation of one explicit
project Pi agent inventory.

Intrinsic and cross-object scope

The validator owns descriptor, settings, tool-role, skill-closure, and inventory
agreement. Agent performance and runtime isolation are owned separately.

VVUQ and scientific exclusions

This is software verification only. It establishes no agent performance, sandbox
security, scientific validity, protected authority, or human acceptance.
"""

import json
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local.agent_definition_validation import (
    _PiHarnessAgentDefinitionSetValidator,
)

pytestmark = pytest.mark.software_verification
SUT = _PiHarnessAgentDefinitionSetValidator


def write_descriptor(
    root: Path,
    filename: str,
    *,
    name: str,
    role: str,
    tools: str,
    skills: str = "audit-skill",
) -> None:
    """Evidence ID: Owns no identifier; writes one explicit flat descriptor fixture.

    Requirement: Tests need deterministic descriptors with controlled frontmatter.

    Acceptance: Write exactly one descriptor beneath the isolated agent root.
    """
    (root / filename).write_text(
        "---\n"
        f"name: {name}\n"
        "package: example\n"
        "description: Test descriptor.\n"
        f"tools: {tools}\n"
        "systemPromptMode: append\n"
        "inheritProjectContext: true\n"
        "inheritSkills: false\n"
        f"skills: {skills}\n"
        "skillPath: ../skills\n"
        f"acceptanceRole: {role}\n"
        "---\n\nTest body.\n",
        encoding="utf-8",
    )


def make_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    """Evidence ID: Owns no identifier; creates one isolated explicit inventory.

    Requirement: Validation tests must not inspect or mutate the maintained repository.

    Acceptance: Return canonical repository, agent, settings, and skill-root paths.
    """
    root = (tmp_path / "repository").resolve()
    agents = root / ".pi/agents"
    settings = root / ".pi/settings.json"
    skills = root / ".pi/skills"
    agents.mkdir(parents=True)
    (skills / "audit-skill").mkdir(parents=True)
    (skills / "audit-skill/SKILL.md").write_text("# Audit skill\n", encoding="utf-8")
    settings.write_text(
        json.dumps({"subagents": {"agentOverrides": {"gpt-pro": {"disabled": True}}}}),
        encoding="utf-8",
    )
    return root, agents, settings, skills


def test_method__execute_valid_inventory__reports_exact_counts(tmp_path: Path) -> None:
    """Evidence ID: software-verification.harness.agent-definition-set.valid-inventory

    Requirement: Valid unique writer and read-only descriptors, selected skills, and an
    explicitly allowed external override form one passing inventory.

    Acceptance: Validation returns PASS, two descriptors, two enabled agents, and no
    findings.
    """
    root, agents, settings, skills = make_inputs(tmp_path)
    write_descriptor(
        agents,
        "writer.md",
        name="writer",
        role="writer",
        tools="read, bash, edit, write",
    )
    write_descriptor(
        agents,
        "reviewer.md",
        name="reviewer",
        role="read-only",
        tools="read, bash",
    )

    result = SUT().execute(root, agents, settings, (skills,), ("gpt-pro",))

    assert result.status == "PASS"
    assert result.descriptor_count == 2
    assert result.enabled_count == 2
    assert result.findings == ()


def test_method__execute_cross_file_conflicts__reports_complete_findings(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.agent-set.cross-file-conflicts

    Requirement: Filename disagreement, duplicate runtime names, and stale disabled
    overrides are reported together rather than hidden by first-failure behavior.

    Acceptance: The exact finding-code set identifies both descriptor conflicts and the
    stale settings override.
    """
    root, agents, settings, skills = make_inputs(tmp_path)
    write_descriptor(
        agents,
        "first.md",
        name="duplicate",
        role="writer",
        tools="read, bash, edit, write",
    )
    write_descriptor(
        agents,
        "second.md",
        name="duplicate",
        role="writer",
        tools="read, bash, edit, write",
    )
    settings.write_text(
        json.dumps(
            {"subagents": {"agentOverrides": {"example.retired": {"disabled": True}}}}
        ),
        encoding="utf-8",
    )

    result = SUT().execute(root, agents, settings, (skills,))

    assert result.status == "FAIL"
    assert {finding.code for finding in result.findings} == {
        "AGENT.FILENAME_MISMATCH",
        "AGENT.OVERRIDE_STALE",
        "AGENT.RUNTIME_DUPLICATE",
    }


def test_method__execute_role_and_skill_conflicts__reports_each_contract(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.agent-set.role-skill-conflicts

    Requirement: Read-only edit capability, unsupported tools, and missing selected
    skills are independent structural defects.

    Acceptance: The exact finding-code set identifies all three defects.
    """
    root, agents, settings, skills = make_inputs(tmp_path)
    write_descriptor(
        agents,
        "reviewer.md",
        name="reviewer",
        role="read-only",
        tools="read, edit, network",
        skills="missing-skill",
    )

    result = SUT().execute(root, agents, settings, (skills,), ("gpt-pro",))

    assert result.status == "FAIL"
    assert {finding.code for finding in result.findings} == {
        "AGENT.ROLE_TOOL_MISMATCH",
        "AGENT.SKILL_MISSING",
        "AGENT.TOOLS_INVALID",
    }


def test_method__execute_skill_root__rejects_symlinked_skill_directory(
    tmp_path: Path,
) -> None:
    """Evidence ID: software-verification.harness.agent-set.skill-root-symlink

    Requirement: Skill discovery cannot traverse a symlinked child directory outside
    an explicitly confined skill root.

    Acceptance: A symlinked skill directory raises ``ValueError`` before its external
    ``SKILL.md`` can satisfy descriptor skill closure.
    """
    root, agents, settings, skills = make_inputs(tmp_path)
    write_descriptor(
        agents,
        "reviewer.md",
        name="reviewer",
        role="read-only",
        tools="read, bash",
        skills="external-skill",
    )
    outside = tmp_path / "outside-skill"
    outside.mkdir()
    (outside / "SKILL.md").write_text("# External\n", encoding="utf-8")
    try:
        (skills / "external-skill").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation is unavailable")

    with pytest.raises(ValueError, match="symlinked directories"):
        SUT().execute(root, agents, settings, (skills,), ("gpt-pro",))
