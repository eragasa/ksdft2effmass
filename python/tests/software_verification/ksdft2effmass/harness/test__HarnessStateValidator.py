r"""Software verification of ``HarnessStateValidator``.

Evidence profile: routine

Bounded artifact scope: deterministic composition of explicit normalized Harness domain
validators plus aggregate decision and cross-domain closure rules.

Facet and represented meaning

The module verifies complete child-result retention, status precedence, decision
reference checks, and capability-to-resource closure over one immutable Harness state.

Intrinsic and cross-object scope

``HarnessStateValidator`` is the sole system under test. Leaf-rule algorithms are
covered by their owning modules; authority, repair, projection, and conformance parsing
are excluded.

VVUQ and scientific exclusions

This is software verification only. It establishes no numerical verification,
scientific validation, uncertainty quantification, protected authority, or acceptance.
"""

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.harness import (
    ActivationReferenceRequirement,
    DevelopmentDecision,
    DevelopmentDecisionSerializer,
    DevelopmentTaskSelectionValidationPolicy,
    DevelopmentTaskSelectionValidator,
    HarnessCapabilityCatalog,
    HarnessCapabilityCatalogValidator,
    HarnessEvidenceCatalogValidator,
    HarnessResourceCatalogValidator,
    HarnessState,
    HarnessStateValidator,
    HarnessTaskGraphValidator,
    ValidationResult,
    ValidationRuleIdentity,
    ValidationStatus,
)

pytestmark = pytest.mark.software_verification
SUT = HarnessStateValidator


class TestHarnessStateValidator:
    """Own software evidence for complete normalized-state validation composition."""

    class RaisingDomainValidator:
        """Synthetic protocol implementation that raises before producing a result."""

        __slots__ = ()
        RULES = (
            ValidationRuleIdentity(
                requirement_identity="test.validation.raising",
                rule_identity="test.validation.raising-rule",
                version_identity="1",
                required=True,
                not_applicable_permitted=False,
            ),
        )

        @property
        def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
            """Return the one synthetic required rule."""
            return self.RULES

        def execute(self, state: HarnessState) -> ValidationResult:
            """Raise a synthetic runtime error after receiving exact state."""
            if type(state) is not HarnessState:
                raise TypeError("state must be HarnessState")
            raise RuntimeError("sensitive synthetic detail")

    class MismatchedRuleValidator:
        """Synthetic validator that returns a result for an unadvertised rule."""

        __slots__ = ()
        ADVERTISED = ValidationRuleIdentity(
            requirement_identity="test.validation.binding",
            rule_identity="test.validation.advertised-rule",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )
        RETURNED = ValidationRuleIdentity(
            requirement_identity="test.validation.binding",
            rule_identity="test.validation.returned-rule",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )

        @property
        def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]:
            """Return the one advertised synthetic rule."""
            return (self.ADVERTISED,)

        def execute(self, state: HarnessState) -> ValidationResult:
            """Return a valid result bound to a different synthetic rule."""
            return ValidationResult.from_findings(
                validator_identity="MismatchedRuleValidator:1",
                rule_identities=(self.RETURNED,),
                summary="Synthetic mismatched child",
                subject_identity=state.identity.sha256,
                findings=(),
                tool_identity="test-tool:1",
            )

    @staticmethod
    def validators() -> tuple[
        DevelopmentTaskSelectionValidator
        | HarnessTaskGraphValidator
        | HarnessCapabilityCatalogValidator
        | HarnessResourceCatalogValidator
        | HarnessEvidenceCatalogValidator,
        ...,
    ]:
        """Return the explicit ordered public domain-validator composition."""
        policy = DevelopmentTaskSelectionValidationPolicy(
            policy_identity="selection-policy:1",
            activation_reference_requirement=ActivationReferenceRequirement.OPTIONAL,
            eligible_task_statuses=("active",),
        )
        return (
            DevelopmentTaskSelectionValidator(policy),
            HarnessTaskGraphValidator(),
            HarnessCapabilityCatalogValidator(),
            HarnessResourceCatalogValidator(),
            HarnessEvidenceCatalogValidator(),
        )

    @staticmethod
    def replace_capabilities(
        state: HarnessState, capabilities: HarnessCapabilityCatalog
    ) -> HarnessState:
        """Rebuild state around one explicit capability catalog."""
        return HarnessState.create(
            source_snapshot_identity=state.source_snapshot_identity,
            normalization_version=state.normalization_version,
            tasks=state.tasks,
            selection=state.selection,
            decisions=state.decisions,
            capabilities=capabilities,
            resources=state.resources,
            evidence=state.evidence,
            provenance=state.provenance,
        )

    @staticmethod
    def replace_decisions(
        state: HarnessState, decisions: tuple[DevelopmentDecision, ...]
    ) -> HarnessState:
        """Rebuild state around one explicit decision sequence."""
        return HarnessState.create(
            source_snapshot_identity=state.source_snapshot_identity,
            normalization_version=state.normalization_version,
            tasks=state.tasks,
            selection=state.selection,
            decisions=decisions,
            capabilities=state.capabilities,
            resources=state.resources,
            evidence=state.evidence,
            provenance=state.provenance,
        )

    def test_method__execute__composes_complete_passing_validation(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.state-validation.pass

        Requirement: The coordinator applies every explicit validator followed by its
        decision-sequence and cross-domain closure rules.

        Acceptance: A consistent state produces seven ordered passing child results,
        one nonblocking pass, and no findings.
        """
        result = SUT(self.validators()).execute(normalized_harness_state)

        assert result.status is ValidationStatus.PASS
        assert len(result.child_results) == 7
        assert result.child_result_identities == tuple(
            child.result_identity for child in result.child_results
        )
        assert not result.findings
        assert not result.blocking

    def test_method__execute__reports_cross_domain_resource_gap(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.state-validation.cross-domain

        Requirement: Every skill-required resource identity must occur in the complete
        normalized resource catalog.

        Acceptance: A skill requiring an absent entry returns one blocking
        ``SKILL_RESOURCE_MISSING`` aggregate finding.
        """
        catalog = normalized_harness_state.capabilities
        skill = replace(
            catalog.capabilities[0],
            entry_resource_id="absent-entry",
            required_resource_ids=("absent-entry",),
        )
        changed = HarnessCapabilityCatalog.create(
            model_version=1,
            normalization_version=normalized_harness_state.normalization_version,
            capabilities=(skill,),
            agent_definitions=catalog.agent_definitions,
        )
        state = self.replace_capabilities(normalized_harness_state, changed)

        result = SUT(()).execute(state)

        assert result.status is ValidationStatus.FAIL
        assert tuple(finding.code for finding in result.findings) == (
            "HV.CLOSURE.SKILL_RESOURCE_MISSING",
        )
        assert result.blocking

    def test_method__execute__reports_decision_reference_gap(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.state-validation.decisions

        Requirement: Every represented decision predecessor must occur in the same
        immutable decision sequence.

        Acceptance: One decision naming an absent predecessor returns exactly
        ``PREDECESSOR_MISSING`` without modifying the decision.
        """
        payload = (
            Path(__file__).with_name("resources") / "legacy-checkpoint.json"
        ).read_bytes()
        decision = DevelopmentDecisionSerializer().adapt_legacy(
            payload,
            decision_id="validation-decision",
            source_path="decisions/legacy-checkpoint.json",
            predecessor_decision_id="absent-decision",
        )
        decision = replace(decision, task_id=None)
        state = self.replace_decisions(normalized_harness_state, (decision,))

        result = SUT(()).execute(state)

        assert tuple(finding.code for finding in result.findings) == (
            "HV.DECISION.PREDECESSOR_MISSING",
        )
        assert state.decisions[0].predecessor_decision_id == "absent-decision"

    def test_method__execute__represents_child_exception_as_error(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.state-validation.error

        Requirement: An unexpected domain-validator exception becomes an identified
        error result without exposing exception text or fabricating pass evidence.

        Acceptance: The composite and first child use ``error``; the diagnostic names
        only ``RuntimeError`` and excludes the sensitive exception message.
        """
        result = SUT((self.RaisingDomainValidator(),)).execute(normalized_harness_state)

        child = result.child_results[0]
        assert result.status is ValidationStatus.ERROR
        assert child.status is ValidationStatus.ERROR
        assert child.error_diagnostic == "validator raised RuntimeError"
        assert "sensitive" not in child.error_diagnostic
        assert result.blocking

    def test_method__execute__rejects_child_rule_binding_mismatch(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.state-validation.rule-binding

        Requirement: Every child result must represent exactly the rules advertised by
        its explicit validator dependency.

        Acceptance: A valid result for an unadvertised rule becomes a blocking error
        whose diagnostic identifies only the binding mismatch.
        """
        result = SUT((self.MismatchedRuleValidator(),)).execute(
            normalized_harness_state
        )

        child = result.child_results[0]
        assert result.status is ValidationStatus.ERROR
        assert child.status is ValidationStatus.ERROR
        assert child.error_diagnostic == "child result rule identity mismatch"
        assert child.rule_identities == (self.MismatchedRuleValidator.ADVERTISED,)
