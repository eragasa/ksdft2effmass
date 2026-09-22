r"""Software verification of ``HarnessTaskGraphValidator``.

Evidence profile: routine

Bounded artifact scope: canonical normalized Harness Task graph references and cycles.

Facet and represented meaning

The module verifies deterministic structural findings over explicitly represented Task
parent, prerequisite, and supersession relationships.

Intrinsic and cross-object scope

``HarnessTaskGraphValidator`` is the sole system under test. Task lifecycle meaning,
prerequisite results, selection, authority, and execution are excluded.

VVUQ and scientific exclusions

This is software verification only. It establishes no numerical verification,
scientific validation, uncertainty quantification, protected authority, or acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.harness import (
    DevelopmentTaskSelection,
    HarnessState,
    HarnessTask,
    HarnessTaskGraphValidator,
    HarnessTaskRegistry,
    ValidationStatus,
)

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskGraphValidator


class TestHarnessTaskGraphValidator:
    """Own software evidence for normalized Task-graph validation."""

    @staticmethod
    def replace_tasks(
        state: HarnessState, tasks: tuple[HarnessTask, ...]
    ) -> HarnessState:
        """Rebuild a normalized state around an explicit Task tuple."""
        registry = HarnessTaskRegistry(1, tasks)
        selection = DevelopmentTaskSelection(
            schema_version=1,
            active_task_id=tasks[0].task_id,
            explicit_activation_receipt_ids=(),
            automatic_successor_activation=False,
        )
        return HarnessState.create(
            source_snapshot_identity=state.source_snapshot_identity,
            normalization_version=state.normalization_version,
            tasks=registry,
            selection=selection,
            decisions=state.decisions,
            capabilities=state.capabilities,
            resources=state.resources,
            evidence=state.evidence,
            provenance=state.provenance,
        )

    def test_method__execute__accepts_closed_acyclic_graph(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.task-graph-validation.pass

        Requirement: A closed acyclic canonical Task graph has no structural finding.

        Acceptance: Validation returns completed, nonblocking ``pass``.
        """
        result = SUT().execute(normalized_harness_state)

        assert result.status is ValidationStatus.PASS
        assert not result.findings
        assert not result.blocking

    def test_method__execute__reports_missing_relationship_targets(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.task-graph-validation.closure

        Requirement: Every represented parent, prerequisite, and supersession target
        must occur in the canonical Task registry.

        Acceptance: Three absent targets produce exactly the three relationship-
        specific missing-target findings in deterministic rule order.
        """
        task = replace(
            normalized_harness_state.tasks.tasks[0],
            parent_task_id="absent-parent",
            task_prerequisite_ids=("absent-prerequisite",),
            superseded_by_task_ids=("absent-replacement",),
        )
        state = self.replace_tasks(normalized_harness_state, (task,))

        result = SUT().execute(state)

        assert tuple(finding.code for finding in result.findings) == (
            "HV.TASK.PARENT_MISSING",
            "HV.TASK.PREREQUISITE_MISSING",
            "HV.TASK.SUPERSESSION_MISSING",
        )
        assert result.blocking

    def test_method__execute__reports_duplicate_task_resource_paths(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.task-graph-validation.paths

        Requirement: Canonical Task intake and documentation paths are unique across
        the normalized registry.

        Acceptance: Two Tasks sharing both paths return exactly the documentation and
        intake duplicate findings with the path retained.
        """
        base = normalized_harness_state.tasks.tasks[0]
        first = replace(
            base,
            task_id="task-a",
            intake_path="tasks/shared.md",
            documentation_path="docs/shared.md",
        )
        second = replace(
            base,
            task_id="task-b",
            intake_path="tasks/shared.md",
            documentation_path="docs/shared.md",
        )
        state = self.replace_tasks(normalized_harness_state, (first, second))

        result = SUT().execute(state)

        assert tuple(finding.code for finding in result.findings) == (
            "HV.TASK.DOCUMENTATION_PATH_DUPLICATE",
            "HV.TASK.INTAKE_PATH_DUPLICATE",
        )
        assert result.affected_paths == ("docs/shared.md", "tasks/shared.md")

    @pytest.mark.parametrize(
        ("relation", "expected_code"),
        (
            pytest.param("parent", "HV.TASK.PARENT_CYCLE", id="parent_cycle"),
            pytest.param(
                "prerequisite",
                "HV.TASK.PREREQUISITE_CYCLE",
                id="prerequisite_cycle",
            ),
            pytest.param(
                "supersession",
                "HV.TASK.SUPERSESSION_CYCLE",
                id="supersession_cycle",
            ),
        ),
    )
    def test_method__execute__reports_each_relationship_cycle(
        self,
        normalized_harness_state: HarnessState,
        relation: str,
        expected_code: str,
    ) -> None:
        """Evidence ID: software-verification.harness.task-graph-validation.cycles

        Requirement: Parent, prerequisite, and supersession relationships are each
        independently acyclic.

        Acceptance: Each two-Task semantic partition returns exactly its relation-
        specific cycle code and no missing-target finding.
        """
        base = normalized_harness_state.tasks.tasks[0]
        first_changes: dict[str, str | tuple[str, ...]] = {"task_id": "task-a"}
        second_changes: dict[str, str | tuple[str, ...]] = {"task_id": "task-b"}
        if relation == "parent":
            first_changes["parent_task_id"] = "task-b"
            second_changes["parent_task_id"] = "task-a"
        elif relation == "prerequisite":
            first_changes["task_prerequisite_ids"] = ("task-b",)
            second_changes["task_prerequisite_ids"] = ("task-a",)
        else:
            first_changes["superseded_by_task_ids"] = ("task-b",)
            second_changes["superseded_by_task_ids"] = ("task-a",)
        first = replace(base, **first_changes)  # type: ignore[arg-type]
        second = replace(base, **second_changes)  # type: ignore[arg-type]
        state = self.replace_tasks(normalized_harness_state, (first, second))

        result = SUT().execute(state)

        assert tuple(finding.code for finding in result.findings) == (expected_code,)
