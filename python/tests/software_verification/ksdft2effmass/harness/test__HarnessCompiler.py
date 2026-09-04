r"""Software verification of ``HarnessCompiler``.

Evidence profile: routine

Bounded artifact scope: the public ``HarnessCompiler`` pure compilation contract.

Facet and represented meaning

The module verifies complete-state construction and fail-closed family agreement for
one closed typed source snapshot.

Intrinsic and cross-object scope

``HarnessCompiler`` is the sole system under test. Source decoding and filesystem
consistency belong to ``HarnessRepositoryLoader`` and are excluded.

VVUQ and scientific exclusions

This is software verification only. It establishes no policy validation, authority,
scientific validity, protected execution, persistence, projection, or human acceptance.
"""

import hashlib
from dataclasses import replace
from pathlib import Path, PurePosixPath

import pytest

from ksdft2effmass.harness import (
    ArchivedTaskSource,
    DevelopmentDecision,
    DevelopmentDecisionSerializer,
    DevelopmentTaskSelection,
    HarnessCompilationStatus,
    HarnessCompiler,
    HarnessCompilerFailureCode,
    HarnessSourceFamily,
    HarnessSourceIdentity,
    HarnessSourceProvenance,
    HarnessSourceRecord,
    HarnessSourceSnapshot,
    HarnessTask,
)
from ksdft2effmass.harness.pi import (
    ArtifactIdentity,
    PiHarnessAgentDefinition,
    ResourceManifest,
    ResourceReference,
    SkillDescriptor,
)
from ksdft2effmass.harness.pi.conformance.python import PythonModuleSource

pytestmark = pytest.mark.software_verification
SUT = HarnessCompiler


class TestHarnessCompiler:
    """Own software evidence for the pure compiler ActionObject."""

    @staticmethod
    def make_task() -> HarnessTask:
        """Construct one valid Task input; this helper owns no identifier."""
        return HarnessTask(
            schema_version=3,
            task_id="compiler-test-task",
            title="Compiler test Task",
            status="implementation",
            status_detail=None,
            parent_task_id=None,
            task_prerequisite_ids=(),
            external_prerequisite_ids=(),
            superseded_by_task_ids=(),
            explicit_activation_required=True,
            objective="Exercise deterministic compiler state construction.",
            authority_reference_paths=("docs/architecture/v2/index.md",),
            authorized_scope=("Synthetic software-verification input only.",),
            completion_criteria=("The exact represented contract is satisfied.",),
            exclusions=("No authority or scientific claim is represented.",),
            intake_path=None,
        )

    @staticmethod
    def make_snapshot(
        *, task_path: str = "tasks/task.json", digest: str = "1" * 64
    ) -> HarnessSourceSnapshot:
        """Construct one closed typed snapshot; this helper owns no identifier."""
        task_identity = HarnessSourceIdentity(
            family=HarnessSourceFamily.TASK,
            relative_path=PurePosixPath(task_path),
            format_version=3,
            sha256=digest,
            byte_count=1,
        )
        selection_identity = HarnessSourceIdentity(
            family=HarnessSourceFamily.TASK_SELECTION,
            relative_path=PurePosixPath("selection/selection.json"),
            format_version=1,
            sha256="2" * 64,
            byte_count=1,
        )
        task_provenance = HarnessSourceProvenance(
            source_identity=task_identity,
            source_location="",
            normalized_location="/tasks/0",
        )
        selection_provenance = HarnessSourceProvenance(
            source_identity=selection_identity,
            source_location="",
            normalized_location="/selection",
        )
        selection = DevelopmentTaskSelection(
            schema_version=1,
            active_task_id="compiler-test-task",
            explicit_activation_receipt_ids=(),
            automatic_successor_activation=False,
        )
        decision_payload = (
            Path(__file__).with_name("resources") / "legacy-checkpoint.json"
        ).read_bytes()
        decision = DevelopmentDecisionSerializer().adapt_legacy(
            decision_payload,
            decision_id="compiler-test-decision",
            source_path="decisions/checkpoint.json",
        )
        decision_identity = HarnessSourceIdentity(
            family=HarnessSourceFamily.DEVELOPMENT_DECISION,
            relative_path=PurePosixPath("decisions/checkpoint.json"),
            format_version=1,
            sha256=hashlib.sha256(decision_payload).hexdigest(),
            byte_count=len(decision_payload),
        )
        decision_provenance = HarnessSourceProvenance(
            source_identity=decision_identity,
            source_location="",
            normalized_location="/decisions",
        )
        capability = SkillDescriptor(
            1,
            "compiler-test-skill",
            1,
            "compiler-test-entry",
            ("compiler-test-capability",),
            ("compiler-test-entry",),
            "read_only",
            "compiler-test-policy",
            "none",
            "stop_after_result",
        )
        resource = ResourceManifest(
            1,
            "compiler-test-resources",
            1,
            "generic",
            None,
            (
                ResourceReference(
                    1,
                    "compiler-test-entry",
                    "skill",
                    1,
                    "skills/compiler-test/SKILL.md",
                    ArtifactIdentity(1, "sha256", "4" * 64),
                    (),
                ),
            ),
        )
        agent = PiHarnessAgentDefinition(
            1,
            "compiler-test-agent",
            "compiler-test",
            "compiler-test.compiler-test-agent",
            "agents/agent.md",
            ArtifactIdentity(1, "sha256", "8" * 64),
            "read_only",
            ("compiler-test-skill",),
            True,
        )
        evidence = PythonModuleSource("evidence/test_sample.py", b"assert True\n")
        values = (
            (task_identity, TestHarnessCompiler.make_task(), task_provenance),
            (selection_identity, selection, selection_provenance),
            (decision_identity, decision, decision_provenance),
        )
        records = list(
            HarnessSourceRecord(
                identity=identity, value=value, provenance=(provenance,)
            )
            for identity, value, provenance in values
        )
        for family, path, value, source_digest in (
            (
                HarnessSourceFamily.CAPABILITY,
                "capabilities/skill.json",
                capability,
                "6" * 64,
            ),
            (
                HarnessSourceFamily.RESOURCE,
                "resources/manifest.json",
                resource,
                "7" * 64,
            ),
            (
                HarnessSourceFamily.AGENT_DEFINITION,
                "agents/agent.md",
                agent,
                "8" * 64,
            ),
            (
                HarnessSourceFamily.EVIDENCE,
                "evidence/test_sample.py",
                evidence,
                "9" * 64,
            ),
        ):
            if isinstance(value, PythonModuleSource):
                assert value.payload is not None
                source_digest = hashlib.sha256(value.payload).hexdigest()
                byte_count = len(value.payload)
            else:
                byte_count = 1
            identity = HarnessSourceIdentity(
                family=family,
                relative_path=PurePosixPath(path),
                format_version=1,
                sha256=source_digest,
                byte_count=byte_count,
            )
            provenance = HarnessSourceProvenance(
                source_identity=identity,
                source_location="",
                normalized_location=f"/{family.value}",
            )
            records.append(
                HarnessSourceRecord(
                    identity=identity, value=value, provenance=(provenance,)
                )
            )
        ordered_records = tuple(records)
        aggregate_provenance = tuple(
            sorted(
                (item for record in ordered_records for item in record.provenance),
                key=lambda item: (
                    item.normalized_location,
                    item.source_identity.relative_path.as_posix().encode("utf-8"),
                    item.source_location,
                ),
            )
        )
        return HarnessSourceSnapshot.create(
            source_contract_identity="b" * 64,
            identities=tuple(record.identity for record in ordered_records),
            records=ordered_records,
            provenance=aggregate_provenance,
        )

    def test_method__execute__constructs_one_complete_state(self) -> None:
        """Evidence ID: software-verification.harness.compiler.complete-state

        Requirement: A representable closed snapshot produces exactly one complete
        ``HarnessState`` and no blocking compilation diagnostic.

        Acceptance: The result is ``succeeded``; its registry and selection are exact,
        every required catalog contains its one represented value, and diagnostics are
        empty.
        """
        result = SUT("compiler-v1", "normalization-v1").execute(self.make_snapshot())

        assert result.status is HarnessCompilationStatus.SUCCEEDED
        assert result.diagnostics == ()
        assert result.state.tasks.task_ids == ("compiler-test-task",)
        assert result.state.selection.active_task_id == "compiler-test-task"
        assert tuple(item.decision_id for item in result.state.decisions) == (
            "compiler-test-decision",
        )
        assert tuple(
            item.skill_id for item in result.state.capabilities.capabilities
        ) == ("compiler-test-skill",)
        assert tuple(
            item.runtime_name for item in result.state.capabilities.agent_definitions
        ) == ("compiler-test.compiler-test-agent",)
        assert tuple(item.manifest_id for item in result.state.resources.resources) == (
            "compiler-test-resources",
        )
        assert tuple(item.path for item in result.state.evidence.evidence) == (
            "evidence/test_sample.py",
        )

    def test_method__execute__excludes_layout_from_state_identity(self) -> None:
        """Evidence ID: software-verification.harness.compiler.semantic-identity

        Requirement: Source path and raw-byte identity differences do not enter the
        normalized semantic state identity when decoded values are equal.

        Acceptance: Snapshots with different Task paths and source digests compile to
        exactly equal ``HarnessStateIdentity`` values.
        """
        compiler = SUT("compiler-v1", "normalization-v1")

        first = compiler.execute(self.make_snapshot())
        second = compiler.execute(
            self.make_snapshot(task_path="tasks/renamed.json", digest="3" * 64)
        )

        assert first.status is HarnessCompilationStatus.SUCCEEDED
        assert second.status is HarnessCompilationStatus.SUCCEEDED
        assert first.state.identity == second.state.identity

    def test_method__execute__fails_when_required_family_is_absent(self) -> None:
        """Evidence ID: software-verification.harness.compiler.required-families

        Requirement: Complete state requires at least one Task, capability, resource,
        agent definition, and evidence source plus exactly one selection.

        Acceptance: Removing the evidence record returns the exact closed
        ``UNREPRESENTABLE_NORMALIZATION`` failure with no partial state.
        """
        snapshot = self.make_snapshot()
        retained = snapshot.records[:-1]
        incomplete = HarnessSourceSnapshot.create(
            source_contract_identity=snapshot.source_contract_identity,
            identities=tuple(record.identity for record in retained),
            records=retained,
            provenance=tuple(
                sorted(
                    (item for record in retained for item in record.provenance),
                    key=lambda item: (
                        item.normalized_location,
                        item.source_identity.relative_path.as_posix().encode("utf-8"),
                        item.source_location,
                    ),
                )
            ),
        )

        result = SUT("compiler-v1", "normalization-v1").execute(incomplete)

        assert result.status is HarnessCompilationStatus.FAILED
        assert tuple(item.code for item in result.diagnostics) == (
            HarnessCompilerFailureCode.UNREPRESENTABLE_NORMALIZATION,
        )
        assert not hasattr(result, "state")

    def test_method__execute__maps_actual_state_provenance(self) -> None:
        """Evidence ID: software-verification.harness.compiler.state-provenance

        Requirement: Compiled provenance points into actual top-level ``HarnessState``
        locations rather than a synthetic source namespace.

        Acceptance: The exact normalized-location set covers Tasks, selection,
        capability values, resources, and source-level evidence at their state paths.
        """
        result = SUT("compiler-v1", "normalization-v1").execute(self.make_snapshot())

        assert result.status is HarnessCompilationStatus.SUCCEEDED
        assert {item.normalized_location for item in result.state.provenance} == {
            "/tasks/0",
            "/selection",
            "/decisions/0",
            "/capabilities/capabilities/0",
            "/capabilities/agent_definitions/0",
            "/resources/resources/0",
            "/evidence/sources/0",
        }

    def test_method__execute__rejects_unsupported_source_format(self) -> None:
        """Evidence ID: software-verification.harness.compiler.source-format

        Requirement: Compiler admission independently enforces each source family's
        owning format version even for a directly constructed closed snapshot.

        Acceptance: An evidence identity declaring version 2 returns exactly
        ``UNSUPPORTED_FORMAT_VERSION`` and no state.
        """
        snapshot = self.make_snapshot()
        retained = snapshot.records[:-1]
        evidence_record = snapshot.records[-1]
        identity = replace(evidence_record.identity, format_version=2)
        provenance = replace(evidence_record.provenance[0], source_identity=identity)
        record = HarnessSourceRecord(
            identity=identity,
            value=evidence_record.value,
            provenance=(provenance,),
        )
        records = (*retained, record)
        direct = HarnessSourceSnapshot.create(
            source_contract_identity=snapshot.source_contract_identity,
            identities=tuple(item.identity for item in records),
            records=records,
            provenance=tuple(
                sorted(
                    (item for value in records for item in value.provenance),
                    key=lambda item: item.sort_key,
                )
            ),
        )

        result = SUT("compiler-v1", "normalization-v1").execute(direct)

        assert result.status is HarnessCompilationStatus.FAILED
        assert tuple(item.code for item in result.diagnostics) == (
            HarnessCompilerFailureCode.UNSUPPORTED_FORMAT_VERSION,
        )
        assert not hasattr(result, "state")

    def test_construction__derived_identities__rejects_tampering(self) -> None:
        """Evidence ID: software-verification.harness.compiler.identity-tampering

        Requirement: Identity-bearing snapshots, catalogs, and successful results
        intrinsically reject values contradictory to their exact represented fields.

        Acceptance: Replacing each representative derived or cross-binding identity
        raises ``ValueError`` before a contradictory public value exists.
        """
        snapshot = self.make_snapshot()
        with pytest.raises(ValueError, match="snapshot_identity"):
            replace(snapshot, snapshot_identity="0" * 64)
        task_record = snapshot.records[0]
        task = task_record.value
        assert type(task) is HarnessTask
        changed_task_record = replace(
            task_record, value=replace(task, title="Contradictory parsed value")
        )
        with pytest.raises(ValueError, match="snapshot_identity"):
            replace(
                snapshot,
                records=(changed_task_record, *snapshot.records[1:]),
            )
        changed_snapshot = HarnessSourceSnapshot.create(
            source_contract_identity=snapshot.source_contract_identity,
            identities=snapshot.identities,
            records=(changed_task_record, *snapshot.records[1:]),
            provenance=snapshot.provenance,
        )
        assert changed_snapshot.snapshot_identity != snapshot.snapshot_identity
        task_variants = (
            replace(
                task,
                archived_source=ArchivedTaskSource(
                    "archive/compiler-test-task.md", "a" * 64
                ),
            ),
            replace(task, documentation_path="docs/compiler-test-task.md"),
        )
        for task_variant in task_variants:
            variant_record = replace(task_record, value=task_variant)
            with pytest.raises(ValueError, match="snapshot_identity"):
                replace(
                    snapshot,
                    records=(variant_record, *snapshot.records[1:]),
                )
        decision_record = snapshot.records[2]
        decision = decision_record.value
        assert type(decision) is DevelopmentDecision
        changed_provenance = replace(
            decision.source_provenance,
            adapter_version="legacy-checkpoint-v2",
        )
        changed_decision_record = replace(
            decision_record,
            value=replace(decision, source_provenance=changed_provenance),
        )
        with pytest.raises(ValueError, match="snapshot_identity"):
            replace(
                snapshot,
                records=(
                    *snapshot.records[:2],
                    changed_decision_record,
                    *snapshot.records[3:],
                ),
            )
        result = SUT("compiler-v1", "normalization-v1").execute(snapshot)
        assert result.status is HarnessCompilationStatus.SUCCEEDED
        with pytest.raises(ValueError, match="catalog_identity"):
            replace(result.state.evidence, catalog_identity="0" * 64)
        with pytest.raises(ValueError, match="bindings"):
            replace(result, source_snapshot_identity="f" * 64)

    def test_method__execute__fails_on_wrong_family_value(self) -> None:
        """Evidence ID: software-verification.harness.compiler.family-mismatch

        Requirement: A decoded value assigned to the wrong source family is an
        unrepresentable compilation input and cannot produce partial state.

        Acceptance: Compilation returns ``failed`` with exactly the closed
        ``SOURCE_FAMILY_MISMATCH`` blocking diagnostic and exposes no state field.
        """
        snapshot = self.make_snapshot()
        task_record, selection_record = snapshot.records[:2]
        wrong_record = HarnessSourceRecord(
            identity=task_record.identity,
            value=selection_record.value,
            provenance=task_record.provenance,
        )
        wrong_snapshot = HarnessSourceSnapshot.create(
            source_contract_identity=snapshot.source_contract_identity,
            identities=(wrong_record.identity, selection_record.identity),
            records=(wrong_record, selection_record),
            provenance=tuple(
                sorted(
                    (*wrong_record.provenance, *selection_record.provenance),
                    key=lambda item: (
                        item.normalized_location,
                        item.source_identity.relative_path.as_posix().encode("utf-8"),
                        item.source_location,
                    ),
                )
            ),
        )

        result = SUT("compiler-v1", "normalization-v1").execute(wrong_snapshot)

        assert result.status is HarnessCompilationStatus.FAILED
        assert tuple(item.code for item in result.diagnostics) == (
            HarnessCompilerFailureCode.SOURCE_FAMILY_MISMATCH,
        )
        assert not hasattr(result, "state")
