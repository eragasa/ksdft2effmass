r"""Software verification of ``HarnessRepositoryLoader``.

Evidence profile: routine

Bounded artifact scope: the public ``HarnessRepositoryLoader`` source-loading contract.

Facet and represented meaning

The module verifies exact-source loading into one closed typed snapshot.

Intrinsic and cross-object scope

``HarnessRepositoryLoader`` is the sole system under test. The owning public decoders
remain collaborators; compilation and state validation are excluded.

VVUQ and scientific exclusions

This is software verification only. It establishes no authority, scientific validity,
protected execution, persistence, projection, or human acceptance.
"""

from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path, PurePosixPath

import pytest

from ksdft2effmass.harness import (
    DevelopmentDecision,
    DevelopmentTaskSelection,
    DevelopmentTaskSelectionSerializer,
    HarnessCompilerFailureCode,
    HarnessLegacyDecisionBinding,
    HarnessRepositoryLoader,
    HarnessSourceContract,
    HarnessSourceFamily,
    HarnessSourceFamilyContract,
    HarnessSourceLoadStatus,
    HarnessTask,
    HarnessTaskSerializer,
)
from ksdft2effmass.harness.pi import PiHarnessConfiguration

pytestmark = pytest.mark.software_verification
SUT = HarnessRepositoryLoader


class TestHarnessRepositoryLoader:
    """Own software evidence for exact, fail-closed repository loading."""

    @staticmethod
    def make_task() -> HarnessTask:
        """Construct one valid Task source; this helper owns no identifier."""
        return HarnessTask(
            schema_version=3,
            task_id="loader-test-task",
            title="Loader test Task",
            status="implementation",
            status_detail=None,
            parent_task_id=None,
            task_prerequisite_ids=(),
            external_prerequisite_ids=(),
            superseded_by_task_ids=(),
            explicit_activation_required=True,
            objective="Exercise exact repository loading.",
            authority_reference_paths=("docs/architecture/v2/index.md",),
            authorized_scope=("Synthetic software-verification input only.",),
            completion_criteria=("The exact represented contract is satisfied.",),
            exclusions=("No authority or scientific claim is represented.",),
            intake_path=None,
        )

    @staticmethod
    def source_payloads() -> tuple[tuple[str, bytes], ...]:
        """Return one exact source for every required family; no evidence ID."""
        task = HarnessTaskSerializer().execute(TestHarnessRepositoryLoader.make_task())
        selection = DevelopmentTaskSelectionSerializer().execute(
            DevelopmentTaskSelection(1, "loader-test-task", (), False)
        )
        capability = b"""{
  "schema_version": 1,
  "skill_id": "loader-test-skill",
  "behavior_version": 1,
  "entry_resource_id": "loader-test-entry",
  "trigger_capability_ids": ["loader-test-capability"],
  "required_resource_ids": ["loader-test-entry"],
  "side_effect_class": "read_only",
  "authorization_policy_id": "loader-test-policy",
  "retry_policy": "none",
  "termination_policy": "stop_after_result"
}
"""
        resource = b"""{
  "schema_version": 1,
  "manifest_id": "loader-test-resources",
  "manifest_version": 1,
  "layer": "generic",
  "extends_manifest_id": null,
  "resources": [
    {
      "schema_version": 1,
      "resource_id": "loader-test-entry",
      "resource_kind": "skill",
      "format_version": 1,
      "path": "skills/loader-test/SKILL.md",
      "content_identity": {
        "schema_version": 1,
        "algorithm": "sha256",
        "digest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
      },
      "dependency_ids": []
    }
  ]
}
"""
        agent = b"""---
name: loader-test-agent
package: loader-test
skills: loader-test-skill
acceptanceRole: read-only
---
Synthetic descriptor.
"""
        evidence = b"def test_placeholder() -> None:\n    assert True\n"
        return (
            ("tasks/task.json", task),
            ("selection/selection.json", selection),
            ("capabilities/skill.json", capability),
            ("resources/manifest.json", resource),
            ("agents/agent.md", agent),
            ("evidence/test_sample.py", evidence),
        )

    @staticmethod
    def make_contract(root: Path) -> HarnessSourceContract:
        """Construct the complete explicit source contract; no evidence ID."""
        specifications = (
            (HarnessSourceFamily.TASK, "tasks", ("tasks/task.json",), 3, 1),
            (
                HarnessSourceFamily.TASK_SELECTION,
                "selection",
                ("selection/selection.json",),
                1,
                1,
            ),
            (HarnessSourceFamily.DEVELOPMENT_DECISION, "decisions", (), 1, 0),
            (
                HarnessSourceFamily.CAPABILITY,
                "capabilities",
                ("capabilities/skill.json",),
                1,
                1,
            ),
            (
                HarnessSourceFamily.RESOURCE,
                "resources",
                ("resources/manifest.json",),
                1,
                1,
            ),
            (
                HarnessSourceFamily.AGENT_DEFINITION,
                "agents",
                ("agents/agent.md",),
                1,
                1,
            ),
            (
                HarnessSourceFamily.EVIDENCE,
                "evidence",
                ("evidence/test_sample.py",),
                1,
                1,
            ),
        )
        families = tuple(
            HarnessSourceFamilyContract(
                family=family,
                catalog_roots=(PurePosixPath(catalog_root),),
                source_paths=tuple(PurePosixPath(path) for path in source_paths),
                format_version=format_version,
                minimum_count=minimum_count,
            )
            for (
                family,
                catalog_root,
                source_paths,
                format_version,
                minimum_count,
            ) in specifications
        )
        return HarnessSourceContract(
            schema_version=1,
            repository_root=root,
            families=families,
            symlink_policy="reject",
        )

    @staticmethod
    def populate(root: Path) -> None:
        """Write runtime scratch sources beneath pytest's isolated path."""
        for directory in (
            "tasks",
            "selection",
            "decisions",
            "capabilities",
            "resources",
            "agents",
            "evidence",
        ):
            (root / directory).mkdir(parents=True, exist_ok=True)
        for relative, payload in TestHarnessRepositoryLoader.source_payloads():
            (root / relative).write_bytes(payload)

    def test_method__execute__loads_exact_typed_snapshot(self, tmp_path: Path) -> None:
        """Evidence ID: software-verification.harness.loader.exact-snapshot

        Requirement: One explicit complete stable source set produces one closed typed
        snapshot whose identities bind every exact source byte sequence.

        Acceptance: Loading succeeds, source order follows the family contract, every
        SHA-256 equals the independent ``hashlib`` oracle, and no diagnostic exists.
        """
        self.populate(tmp_path)
        contract = self.make_contract(tmp_path)

        result = SUT("loader-v1", PiHarnessConfiguration(1, ())).execute(contract)

        assert result.status is HarnessSourceLoadStatus.LOADED
        assert result.diagnostics == ()
        expected = dict(self.source_payloads())
        assert tuple(
            identity.relative_path.as_posix() for identity in result.snapshot.identities
        ) == tuple(expected)
        assert tuple(
            identity.sha256 for identity in result.snapshot.identities
        ) == tuple(hashlib.sha256(payload).hexdigest() for payload in expected.values())

    def test_method__execute__rejects_selected_symlink(self, tmp_path: Path) -> None:
        """Evidence ID: software-verification.harness.loader.symlink-rejection

        Requirement: A selected source must be a nonsymlink regular file beneath the
        explicit root.

        Acceptance: Replacing the evidence source with a symlink returns a failed load
        with no snapshot.
        """
        self.populate(tmp_path)
        source = tmp_path / "evidence/test_sample.py"
        target = tmp_path / "outside.py"
        target.write_bytes(source.read_bytes())
        source.unlink()
        try:
            source.symlink_to(target)
        except OSError:
            pytest.skip("symlink creation is unavailable")

        result = SUT("loader-v1", PiHarnessConfiguration(1, ())).execute(
            self.make_contract(tmp_path)
        )

        assert result.status is HarnessSourceLoadStatus.FAILED
        assert not hasattr(result, "snapshot")

    def test_method__execute__rejects_ancestor_symlink(self, tmp_path: Path) -> None:
        """Evidence ID: software-verification.harness.loader.ancestor-symlink

        Requirement: Every catalog-root and selected-path component is traversed
        relative to an open repository descriptor without following symlinks.

        Acceptance: Replacing the evidence catalog directory with a symlink to an
        outside directory returns exactly ``SYMLINK_REJECTED`` and no snapshot.
        """
        self.populate(tmp_path)
        outside = tmp_path.parent / f"{tmp_path.name}-outside"
        outside.mkdir()
        (outside / "test_sample.py").write_bytes(b"assert False\n")
        source = tmp_path / "evidence/test_sample.py"
        source.unlink()
        (tmp_path / "evidence").rmdir()
        try:
            (tmp_path / "evidence").symlink_to(outside, target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation is unavailable")

        result = SUT("loader-v1", PiHarnessConfiguration(1, ())).execute(
            self.make_contract(tmp_path)
        )

        assert result.status is HarnessSourceLoadStatus.FAILED
        assert tuple(item.code for item in result.diagnostics) == (
            HarnessCompilerFailureCode.SYMLINK_REJECTED,
        )
        assert not hasattr(result, "snapshot")

    def test_method__execute__rejects_ancestor_case_mismatch(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: software-verification.harness.loader.ancestor-case

        Requirement: Exact-case checking applies independently to every catalog-root
        and selected-path component.

        Acceptance: A differently cased evidence ancestor returns exactly
        ``CASE_MISMATCH`` and no snapshot.
        """
        self.populate(tmp_path)
        (tmp_path / "evidence").rename(tmp_path / "Evidence")

        result = SUT("loader-v1", PiHarnessConfiguration(1, ())).execute(
            self.make_contract(tmp_path)
        )

        assert result.status is HarnessSourceLoadStatus.FAILED
        assert tuple(item.code for item in result.diagnostics) == (
            HarnessCompilerFailureCode.CASE_MISMATCH,
        )
        assert not hasattr(result, "snapshot")

    def test_method__execute__uses_explicit_legacy_decision_binding(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: software-verification.harness.loader.legacy-decision-binding

        Requirement: Legacy checkpoint adaptation consumes only the exact selected
        path and explicit successor identity, predecessor, and adapter version.

        Acceptance: The loaded decision has the supplied successor identity and exact
        legacy source provenance; no identity is derived from path or checkpoint ID.
        """
        self.populate(tmp_path)
        legacy_path = PurePosixPath("decisions/checkpoint.json")
        payload = (
            Path(__file__).with_name("resources") / "legacy-checkpoint.json"
        ).read_bytes()
        (tmp_path / legacy_path.as_posix()).write_bytes(payload)
        base = self.make_contract(tmp_path)
        decision_family = replace(base.families[2], source_paths=(legacy_path,))
        contract = replace(
            base,
            families=(*base.families[:2], decision_family, *base.families[3:]),
            legacy_decision_bindings=(
                HarnessLegacyDecisionBinding(
                    source_path=legacy_path,
                    decision_id="explicit-successor",
                    predecessor_decision_id="prior-decision",
                    adapter_version="legacy-checkpoint-v1",
                ),
            ),
        )

        result = SUT("loader-v1", PiHarnessConfiguration(1, ())).execute(contract)

        assert result.status is HarnessSourceLoadStatus.LOADED
        decisions = tuple(
            record.value
            for record in result.snapshot.records
            if record.identity.family is HarnessSourceFamily.DEVELOPMENT_DECISION
        )
        assert len(decisions) == 1
        decision = decisions[0]
        assert isinstance(decision, DevelopmentDecision)
        assert decision.decision_id == "explicit-successor"
        assert decision.predecessor_decision_id == "prior-decision"
        assert decision.source_provenance.source_path == legacy_path.as_posix()
        assert (
            decision.source_provenance.source_artifact_identity
            == hashlib.sha256(payload).hexdigest()
        )

    def test_construction__family_contract__fixes_version_and_minimum(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.loader.family-contract

        Requirement: Each source family has one fixed supported format version and
        minimum count; callers cannot weaken complete-state admission.

        Acceptance: A Task family declaring selection's version and an evidence family
        declaring zero minimum both raise ``ValueError``.
        """
        with pytest.raises(ValueError, match="format_version"):
            HarnessSourceFamilyContract(
                family=HarnessSourceFamily.TASK,
                catalog_roots=(PurePosixPath("tasks"),),
                source_paths=(PurePosixPath("tasks/task.json"),),
                format_version=1,
                minimum_count=1,
            )
        with pytest.raises(ValueError, match="minimum_count"):
            HarnessSourceFamilyContract(
                family=HarnessSourceFamily.EVIDENCE,
                catalog_roots=(PurePosixPath("evidence"),),
                source_paths=(PurePosixPath("evidence/test_sample.py"),),
                format_version=1,
                minimum_count=0,
            )
