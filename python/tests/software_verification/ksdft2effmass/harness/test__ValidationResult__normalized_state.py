r"""Software verification of ``ValidationResult``.

Evidence profile: routine

Bounded artifact scope: the public immutable validation rule, finding, and result
contract.

Facet and represented meaning

The module verifies exact identity binding, closed status invariants, derived blocking,
and composite child closure for normalized Harness validation outcomes.

Intrinsic and cross-object scope

``ValidationResult`` is the sole system under test. Domain-rule evaluation and
normalized-state construction are excluded.

VVUQ and scientific exclusions

This is software verification only. It establishes no pytest aggregation beyond these
cases, numerical verification, scientific validation, uncertainty quantification,
protected authority, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.harness import (
    ValidationApplicability,
    ValidationFinding,
    ValidationResult,
    ValidationRuleIdentity,
    ValidationStatus,
)

pytestmark = pytest.mark.software_verification
SUT = ValidationResult


class TestValidationResult:
    """Own software evidence for immutable validation-result behavior."""

    @staticmethod
    def make_rule(*, required: bool = True) -> ValidationRuleIdentity:
        """Construct one synthetic versioned rule; this helper owns no identifier."""
        return ValidationRuleIdentity(
            requirement_identity="test.validation.requirement",
            rule_identity="test.validation.rule",
            version_identity="1",
            required=required,
            not_applicable_permitted=False,
        )

    @staticmethod
    def make_finding(
        rule: ValidationRuleIdentity,
    ) -> ValidationFinding:
        """Construct one exact finding; this helper owns no identifier."""
        return ValidationFinding.create(
            rule_identity=rule,
            code="TEST.VALIDATION.FAILURE",
            subject_identity="subject-1",
            summary="The synthetic requirement failed.",
            affected_paths=("records/test.json",),
        )

    def test_class_method__from_findings__derives_pass_and_failure_state(self) -> None:
        """Evidence ID: software-verification.harness.validation-result.status

        Requirement: Executed leaf results derive pass or fail, affected paths, and
        blocking from exact findings and rule criticality.

        Acceptance: Empty findings produce a completed nonblocking pass; one required
        finding produces a completed blocking fail with the finding path.
        """
        rule = self.make_rule()
        passed = SUT.from_findings(
            validator_identity="validator:1",
            rule_identities=(rule,),
            summary="Synthetic validation",
            subject_identity="subject-1",
            findings=(),
            tool_identity="tool:1",
        )
        failed = SUT.from_findings(
            validator_identity="validator:1",
            rule_identities=(rule,),
            summary="Synthetic validation",
            subject_identity="subject-1",
            findings=(self.make_finding(rule),),
            tool_identity="tool:1",
        )

        assert passed.status is ValidationStatus.PASS
        assert passed.execution_completed
        assert not passed.blocking
        assert failed.status is ValidationStatus.FAIL
        assert failed.execution_completed
        assert failed.blocking
        assert failed.affected_paths == ("records/test.json",)

    def test_property__blocking__keeps_optional_failure_nonblocking(self) -> None:
        """Evidence ID: software-verification.harness.validation-result.criticality

        Requirement: Requirement criticality affects blocking rather than erasing a
        failed validation outcome.

        Acceptance: A failed optional rule remains ``fail`` and reports its finding,
        while ``blocking`` is exactly false.
        """
        optional_rule = self.make_rule(required=False)
        required_rule = replace(
            self.make_rule(),
            requirement_identity="test.validation.required-requirement",
            rule_identity="test.validation.required-rule",
        )
        result = SUT.from_findings(
            validator_identity="validator:1",
            rule_identities=tuple(
                sorted(
                    (optional_rule, required_rule),
                    key=lambda rule: rule.sort_key,
                )
            ),
            summary="Mixed-criticality synthetic validation",
            subject_identity="subject-1",
            findings=(self.make_finding(optional_rule),),
            tool_identity="tool:1",
        )

        assert result.status is ValidationStatus.FAIL
        assert result.findings
        assert not result.blocking

    def test_class_method__composite__applies_child_precedence_and_closure(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.validation-result.composite

        Requirement: A composite retains ordered child identities and derives status,
        findings, paths, and blocking from its complete child outcomes.

        Acceptance: A pass followed by a required fail produces one blocking failed
        composite with both child identities and the exact failed finding closure.
        """
        pass_rule = self.make_rule(required=False)
        fail_rule = replace(
            self.make_rule(),
            requirement_identity="test.validation.second-requirement",
            rule_identity="test.validation.second-rule",
        )
        passed = SUT.from_findings(
            validator_identity="pass-validator:1",
            rule_identities=(pass_rule,),
            summary="Passing child",
            subject_identity="subject-1",
            findings=(),
            tool_identity="tool:1",
        )
        finding = ValidationFinding.create(
            rule_identity=fail_rule,
            code="TEST.VALIDATION.SECOND_FAILURE",
            subject_identity="subject-1",
            summary="The second synthetic requirement failed.",
            affected_paths=("records/second.json",),
        )
        failed = SUT.from_findings(
            validator_identity="fail-validator:1",
            rule_identities=(fail_rule,),
            summary="Failing child",
            subject_identity="subject-1",
            findings=(finding,),
            tool_identity="tool:1",
        )

        result = SUT.composite(
            validator_identity="composite-validator:1",
            summary="Composite synthetic validation",
            subject_identity="subject-1",
            child_results=(passed, failed),
            tool_identity="tool:1",
        )

        assert result.status is ValidationStatus.FAIL
        assert result.child_result_identities == (
            passed.result_identity,
            failed.result_identity,
        )
        assert result.findings == (finding,)
        assert result.affected_paths == ("records/second.json",)
        assert result.blocking

    def test_construction__status_invariants__rejects_fabricated_pass(self) -> None:
        """Evidence ID: software-verification.harness.validation-result.invariants

        Requirement: Pass cannot coexist with findings, incomplete execution, an error
        diagnostic, or not-applicable state.

        Acceptance: Replacing a valid failed result's status with ``pass`` raises
        ``ValueError`` before a contradictory result can exist.
        """
        rule = self.make_rule()
        failed = SUT.from_findings(
            validator_identity="validator:1",
            rule_identities=(rule,),
            summary="Synthetic validation",
            subject_identity="subject-1",
            findings=(self.make_finding(rule),),
            tool_identity="tool:1",
        )

        with pytest.raises(ValueError, match="pass requires"):
            replace(
                failed,
                status=ValidationStatus.PASS,
                result_identity="",
            )

    def test_fields__result_identity__binds_complete_semantics(self) -> None:
        """Evidence ID: software-verification.harness.validation-result.identity

        Requirement: Result identity is deterministic and rejects stale identity after
        represented semantics change.

        Acceptance: Equal constructions have equal SHA-256 identities, while changing
        the summary and retaining the old identity raises ``ValueError``.
        """
        rule = self.make_rule()
        first = SUT.from_findings(
            validator_identity="validator:1",
            rule_identities=(rule,),
            summary="Synthetic validation",
            subject_identity="subject-1",
            findings=(),
            tool_identity="tool:1",
        )
        second = SUT.from_findings(
            validator_identity="validator:1",
            rule_identities=(rule,),
            summary="Synthetic validation",
            subject_identity="subject-1",
            findings=(),
            tool_identity="tool:1",
        )

        assert first.result_identity == second.result_identity
        assert len(first.result_identity) == 64
        with pytest.raises(ValueError, match="result_identity"):
            replace(first, summary="Changed summary")

    def test_construction__applicability__rejects_unpermitted_not_applicable(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.validation-result.applicability

        Requirement: ``not_applicable`` is valid only when every represented rule
        permits it and a reason is retained.

        Acceptance: Constructing ``not_applicable`` for the required applicable rule
        raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="do not permit"):
            SUT(
                validator_identity="validator:1",
                rule_identities=(self.make_rule(),),
                summary="Synthetic validation",
                applicability=ValidationApplicability.NOT_APPLICABLE,
                not_applicable_reason="Synthetic rule does not apply.",
                subject_identity="subject-1",
                execution_completed=False,
                status=ValidationStatus.NOT_APPLICABLE,
                findings=(),
                error_diagnostic=None,
                tool_identity="tool:1",
                configuration_identity=None,
                environment_identity=None,
                evidence_references=(),
                affected_paths=(),
                child_results=(),
                claim_boundary="synthetic software validation only",
            )
        with pytest.raises(ValueError, match="cannot use not_applicable"):
            SUT(
                validator_identity="validator:1",
                rule_identities=(self.make_rule(),),
                summary="Synthetic validation",
                applicability=ValidationApplicability.APPLICABLE,
                not_applicable_reason=None,
                subject_identity="subject-1",
                execution_completed=False,
                status=ValidationStatus.NOT_APPLICABLE,
                findings=(),
                error_diagnostic=None,
                tool_identity="tool:1",
                configuration_identity=None,
                environment_identity=None,
                evidence_references=(),
                affected_paths=(),
                child_results=(),
                claim_boundary="synthetic software validation only",
            )

    def test_construction__rule_identity__rejects_conflicting_metadata(self) -> None:
        """Evidence ID: software-verification.harness.validation-result.rule-identity

        Requirement: One stable rule identity cannot carry conflicting requirement
        metadata within a result.

        Acceptance: Repeating one rule identity with different criticality raises
        ``ValueError``.
        """
        required = self.make_rule()
        optional = replace(required, required=False)

        with pytest.raises(ValueError, match="rule_identity values must be unique"):
            SUT.from_findings(
                validator_identity="validator:1",
                rule_identities=(required, optional),
                summary="Conflicting rules",
                subject_identity="subject-1",
                findings=(),
                tool_identity="tool:1",
            )

    @pytest.mark.parametrize(
        "path",
        (
            pytest.param("/absolute/path", id="absolute_path"),
            pytest.param("records/../escape", id="parent_traversal"),
            pytest.param("records\\windows", id="backslash_path"),
        ),
    )
    def test_construction__affected_paths__rejects_unconfined_path(
        self, path: str
    ) -> None:
        """Evidence ID: software-verification.harness.validation-result.paths

        Requirement: Finding paths are normalized repository-relative paths.

        Acceptance: Absolute, parent-traversal, and backslash semantic partitions each
        raise ``ValueError``.
        """
        with pytest.raises(ValueError, match="repository-relative"):
            ValidationFinding.create(
                rule_identity=self.make_rule(),
                code="TEST.VALIDATION.PATH",
                subject_identity="subject-1",
                summary="Synthetic path finding.",
                affected_paths=(path,),
            )
