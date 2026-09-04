r"""Software verification of ``DevelopmentTaskSelectionValidator``.

Evidence profile: routine

Bounded artifact scope: selected-Task existence and normalized lifecycle consistency.

Facet and represented meaning

The module verifies read-only findings for one normalized development Task selection.

Intrinsic and cross-object scope

``DevelopmentTaskSelectionValidator`` is the sole system under test. Authority,
prerequisite-result resolution, activation receipts, and Task execution are excluded.

VVUQ and scientific exclusions

This is software verification only. It establishes no authorization, numerical
verification, scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.harness import (
    ActivationReferenceRequirement,
    DevelopmentTaskSelection,
    DevelopmentTaskSelectionValidationPolicy,
    DevelopmentTaskSelectionValidator,
    HarnessState,
    HarnessTaskRegistry,
    ValidationStatus,
)

pytestmark = pytest.mark.software_verification
SUT = DevelopmentTaskSelectionValidator


class TestDevelopmentTaskSelectionValidator:
    """Own software evidence for selection-state validation."""

    @staticmethod
    def policy(
        *,
        activation: ActivationReferenceRequirement = (
            ActivationReferenceRequirement.OPTIONAL
        ),
        statuses: tuple[str, ...] = ("active",),
    ) -> DevelopmentTaskSelectionValidationPolicy:
        """Construct one explicit synthetic selection policy."""
        return DevelopmentTaskSelectionValidationPolicy(
            policy_identity="selection-policy:1",
            activation_reference_requirement=activation,
            eligible_task_statuses=statuses,
        )

    @staticmethod
    def replace_selection(
        state: HarnessState,
        selection: DevelopmentTaskSelection,
        tasks: HarnessTaskRegistry | None = None,
    ) -> HarnessState:
        """Rebuild a state around explicit selection inputs without stale identity."""
        return HarnessState.create(
            source_snapshot_identity=state.source_snapshot_identity,
            normalization_version=state.normalization_version,
            tasks=state.tasks if tasks is None else tasks,
            selection=selection,
            decisions=state.decisions,
            capabilities=state.capabilities,
            resources=state.resources,
            evidence=state.evidence,
            provenance=state.provenance,
        )

    def test_method__execute__accepts_consistent_active_selection(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.selection-validation.pass

        Requirement: A selected canonical Task whose lifecycle status is ``active``
        produces no structural selection finding.

        Acceptance: Validation returns completed, nonblocking ``pass`` for the exact
        normalized state identity.
        """
        result = SUT(self.policy()).execute(normalized_harness_state)

        assert result.status is ValidationStatus.PASS
        assert result.subject_identity == normalized_harness_state.identity.sha256
        assert not result.findings
        assert not result.blocking

    def test_method__execute__reports_absent_selected_task(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.selection-validation.missing

        Requirement: Selection must name a Task in the canonical normalized registry.

        Acceptance: An absent identity returns one blocking ``UNKNOWN_TASK`` finding
        without mutating the selection.
        """
        selection = replace(
            normalized_harness_state.selection,
            active_task_id="absent-task",
        )
        state = self.replace_selection(normalized_harness_state, selection)

        result = SUT(self.policy()).execute(state)

        assert result.status is ValidationStatus.FAIL
        assert result.blocking
        assert tuple(finding.code for finding in result.findings) == (
            "HV.SELECTION.UNKNOWN_TASK",
        )
        assert state.selection.active_task_id == "absent-task"

    def test_method__execute__applies_explicit_lifecycle_policy(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.selection-validation.lifecycle

        Requirement: Lifecycle eligibility is asserted only by an explicitly supplied
        policy over retained opaque Task status text.

        Acceptance: A planning Task fails a policy that explicitly permits only
        ``active`` and passes a policy with no lifecycle assertion.
        """
        original = normalized_harness_state.tasks.tasks[0]
        changed = replace(original, status="planning")
        tasks = HarnessTaskRegistry(1, (changed,))
        state = self.replace_selection(
            normalized_harness_state,
            normalized_harness_state.selection,
            tasks,
        )

        restricted = SUT(self.policy()).execute(state)
        unrestricted = SUT(self.policy(statuses=())).execute(state)

        assert tuple(finding.code for finding in restricted.findings) == (
            "HV.SELECTION.LIFECYCLE_INELIGIBLE",
        )
        assert unrestricted.status is ValidationStatus.PASS

    def test_method__execute__applies_activation_reference_policy(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.selection-validation.receipts

        Requirement: Activation-reference applicability follows the supplied policy,
        while receipt existence, authenticity, and authority remain unclaimed.

        Acceptance: The baseline selected Task fails a ``required`` policy because it
        has no reference and passes an ``optional`` policy.
        """
        required = SUT(
            self.policy(activation=ActivationReferenceRequirement.REQUIRED)
        ).execute(normalized_harness_state)
        optional = SUT(self.policy()).execute(normalized_harness_state)

        assert tuple(finding.code for finding in required.findings) == (
            "HV.SELECTION.ACTIVATION_REFERENCE_REQUIRED",
        )
        assert optional.status is ValidationStatus.PASS

    def test_method__execute__permits_inactive_receipt_references(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.selection-validation.inactive

        Requirement: An inactive selection with receipt references remains
        structurally representable and is not interpreted as authority.

        Acceptance: No selected Task produces ``pass`` without inspecting or rejecting
        the retained receipt reference.
        """
        selection = DevelopmentTaskSelection(
            schema_version=1,
            active_task_id=None,
            explicit_activation_receipt_ids=("receipt-1",),
            automatic_successor_activation=False,
        )
        state = self.replace_selection(normalized_harness_state, selection)

        result = SUT(self.policy()).execute(state)

        assert result.status is ValidationStatus.PASS
        assert result.findings == ()
