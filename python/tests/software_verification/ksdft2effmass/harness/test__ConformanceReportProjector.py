r"""Software verification of ``ConformanceReportProjector``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies a derived immutable report over one exact validation result.

Intrinsic and cross-object scope

The projector is the sole SUT; ValidationResult is an explicit source collaborator.

VVUQ and scientific exclusions

Passing establishes report derivation only, not source correctness, science, UQ, or
acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness import (
    ConformanceReportProjector,
    ValidationFinding,
    ValidationResult,
    ValidationRuleIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = ConformanceReportProjector


class TestConformanceReportProjector:
    """Verify exact, immutable, authority-free report derivation."""

    @staticmethod
    def _result() -> ValidationResult:
        """Construct one controlled identified failing validation result."""
        rule = ValidationRuleIdentity(
            requirement_identity="example.requirement",
            rule_identity="example.rule",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )
        finding = ValidationFinding.create(
            rule_identity=rule,
            code="EXAMPLE.FAIL",
            subject_identity="a" * 64,
            summary="Controlled failure.",
            affected_paths=("python/example.py",),
        )
        return ValidationResult.from_findings(
            validator_identity="example:1",
            rule_identities=(rule,),
            summary="Controlled validation",
            subject_identity="a" * 64,
            findings=(finding,),
            tool_identity="example-tool:1",
        )

    def test_method__execute__preserves_exact_source_closure(self) -> None:
        """Evidence ID: software-verification.harness.conformance.report.closure

        Requirement: A report preserves source-result, subject, status, rule, finding,
        and path identities.

        Method: Project one literal identified failing result.

        Oracle: Direct field extraction from the immutable source fixes every report
        field.

        Acceptance: Every report value equals the corresponding source value and has a
        derived identity.

        Interpretation: Failure identifies lossy or fabricated reporting.

        Limitations: Rendering, persistence, and promotion use are excluded.
        """
        source = self._result()
        report = SUT().execute(source)
        assert report.source_result_identity == source.result_identity
        assert report.subject_identity == source.subject_identity
        assert report.status == source.status
        assert report.blocking == source.blocking
        assert report.rule_identities == ("example.rule",)
        assert report.finding_identities == (source.findings[0].finding_identity,)
        assert report.affected_paths == source.affected_paths
        assert len(report.report_identity) == 64

    def test_method__execute__does_not_replace_or_mutate_source(self) -> None:
        """Evidence ID: software-verification.harness.conformance.report.nonmutation

        Requirement: Derived reporting neither replaces nor mutates its authoritative
        result.

        Method: Project the same frozen source twice and attempt report reassignment.

        Oracle: Value equality and frozen dataclass behavior define nonmutation.

        Acceptance: Repeated reports are equal, source identity is unchanged, and
        reassignment raises.

        Interpretation: Failure identifies mutable or authoritative report behavior.

        Limitations: External storage and rendering are excluded.
        """
        source = self._result()
        identity = source.result_identity
        first = SUT().execute(source)
        second = SUT().execute(source)
        assert first == second
        assert source.result_identity == identity
        with pytest.raises(FrozenInstanceError):
            first.blocking = False  # type: ignore[misc]
