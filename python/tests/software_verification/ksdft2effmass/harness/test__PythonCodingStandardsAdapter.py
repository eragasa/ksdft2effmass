r"""Software verification of ``PythonCodingStandardsAdapter``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies v1 compatibility adaptation and strict project Python findings.

Intrinsic and cross-object scope

The adapter is the sole SUT; controlled resource files provide exact source cases.

VVUQ and scientific exclusions

Passing establishes static software behavior only, not test success, science, UQ, or
acceptance.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath

import pytest

from ksdft2effmass.harness import (
    ConformanceInput,
    ConformanceInputRole,
    ConformanceSubject,
    PythonCodingStandardsAdapter,
    PythonCodingStandardsContract,
    ValidationResult,
)
from ksdft2effmass.harness.pi.conformance.python import (
    PythonConformanceRequest,
    PythonConformanceResult,
    PythonConformanceValidator,
    PythonModuleSource,
)

pytestmark = pytest.mark.software_verification
SUT = PythonCodingStandardsAdapter
RESOURCE_ROOT = Path(__file__).parent / "resources/conformance"
REPOSITORY_PREFIX = (
    "python/tests/software_verification/ksdft2effmass/harness/resources/conformance"
)


class TestPythonCodingStandardsAdapter:
    """Verify explicit Python compatibility and strict-policy adaptation."""

    @staticmethod
    def _input(
        identity: str,
        role: ConformanceInputRole,
        represented_path: str,
        resource_name: str,
    ) -> ConformanceInput:
        """Construct one exact represented input from a maintained test resource."""
        return ConformanceInput.from_payload(
            input_identity=identity,
            role=role,
            path=PurePosixPath(represented_path),
            payload=(RESOURCE_ROOT / resource_name).read_bytes(),
        )

    @classmethod
    def _source_subject(
        cls, resource_name: str, represented_path: str
    ) -> ConformanceSubject:
        """Construct one source-only subject for selected strict rules."""
        return ConformanceSubject(
            subject_family_identity=(
                PythonCodingStandardsContract.SUBJECT_FAMILY_IDENTITY
            ),
            inputs=(
                cls._input(
                    "source",
                    ConformanceInputRole.SOURCE,
                    represented_path,
                    resource_name,
                ),
            ),
        )

    @classmethod
    def _compatibility_results(
        cls, subject: ConformanceSubject
    ) -> tuple[PythonConformanceResult, ValidationResult]:
        """Execute legacy and normalized compatibility paths over identical bytes."""
        ownership = subject.inputs_for_role(ConformanceInputRole.OWNERSHIP)[0]
        assert ownership.payload is not None
        sources = tuple(
            PythonModuleSource(item.path.as_posix(), item.payload)
            for item in subject.inputs_for_role(ConformanceInputRole.SOURCE)
            if item.payload is not None
        )
        legacy = PythonConformanceValidator().execute(
            PythonConformanceRequest(
                sources=sources,
                ownership_path=ownership.path.as_posix(),
                ownership_payload=ownership.payload,
            )
        )
        rule = next(
            item
            for item in PythonCodingStandardsContract.policy().rule_identities
            if item.rule_identity == "python.conformance.evidence-compatibility"
        )
        candidate = SUT().execute(
            subject,
            (rule,),
            PythonCodingStandardsContract.configuration(),
        )
        return legacy, candidate

    @classmethod
    def _positive_subject(cls) -> ConformanceSubject:
        """Construct the controlled source, ownership, and placed-resource subject."""
        inputs = (
            cls._input(
                "ownership",
                ConformanceInputRole.OWNERSHIP,
                f"{REPOSITORY_PREFIX}/positive-ownership.json",
                "positive-ownership.json",
            ),
            cls._input(
                "resource",
                ConformanceInputRole.AUTHORED_TEST_RESOURCE,
                f"{REPOSITORY_PREFIX}/case.json",
                "case.json",
            ),
            cls._input(
                "source",
                ConformanceInputRole.SOURCE,
                f"{REPOSITORY_PREFIX}/test__Example.py",
                "positive-source.txt",
            ),
        )
        return ConformanceSubject(
            subject_family_identity=PythonCodingStandardsContract.SUBJECT_FAMILY_IDENTITY,
            inputs=inputs,
        )

    @classmethod
    def _invalid_subject(cls) -> ConformanceSubject:
        """Construct the controlled strict-invalid source and misplaced resource."""
        path_text = (RESOURCE_ROOT / "misplaced-resource-path.txt").read_text().strip()
        return ConformanceSubject(
            subject_family_identity=(
                PythonCodingStandardsContract.SUBJECT_FAMILY_IDENTITY
            ),
            inputs=(
                cls._input(
                    "ownership",
                    ConformanceInputRole.OWNERSHIP,
                    f"{REPOSITORY_PREFIX}/invalid-ownership.json",
                    "invalid-ownership.json",
                ),
                cls._input(
                    "resource",
                    ConformanceInputRole.AUTHORED_TEST_RESOURCE,
                    path_text,
                    "case.json",
                ),
                cls._input(
                    "source",
                    ConformanceInputRole.SOURCE,
                    f"{REPOSITORY_PREFIX}/test__invalid_subject.py",
                    "invalid-source.txt",
                ),
            ),
        )

    def test_method__execute__accepts_controlled_class_owned_subject(self) -> None:
        """Evidence ID: software-verification.harness.conformance.python.valid

        Requirement: The adapter preserves v1 evidence checks and accepts strict
        class ownership, typing, and resource placement.

        Method: Execute every version-one policy rule over the controlled positive
        resources.

        Oracle: Manual fixture inspection shows one documented Test method, no module
        helper, precise annotations, and a resources path.

        Acceptance: The normalized result passes with every policy rule and no findings.

        Interpretation: Failure identifies compatibility or strict-rule disagreement.

        Limitations: The fixture is parsed but not imported or executed.
        """
        subject = self._positive_subject()
        policy = PythonCodingStandardsContract.policy()
        configuration = PythonCodingStandardsContract.configuration()
        result = SUT().execute(subject, policy.rule_identities, configuration)
        assert result.status.value == "pass"
        assert result.findings == ()
        assert result.subject_identity == subject.subject_identity
        assert result.rule_identities == policy.rule_identities
        assert result.configuration_identity == configuration.configuration_identity

    def test_method__execute__reports_complete_controlled_strict_defects(self) -> None:
        """Evidence ID: software-verification.harness.conformance.python.invalid

        Requirement: Module tests/helpers, undocumented methods, Any,
        cast-through-Any, object, erased containers, and misplaced resources remain
        distinct findings.

        Method: Execute the complete policy over one controlled invalid source and
        represented misplaced resource path.

        Oracle: Each literal source construct and path isolates one named strict rule.

        Acceptance: The result fails and contains every expected strict finding code.

        Interpretation: Failure identifies omitted parsing facts, policy routing, or
        diagnostic drift.

        Limitations: Legacy TE findings may additionally describe the deliberately
        invalid source.
        """
        subject = self._invalid_subject()
        policy = PythonCodingStandardsContract.policy()
        result = SUT().execute(
            subject,
            policy.rule_identities,
            PythonCodingStandardsContract.configuration(),
        )
        codes = {finding.code for finding in result.findings}
        assert {
            "HC.PYTHON.TEST_CLASS_OWNERSHIP",
            "HC.PYTHON.HELPER_OWNERSHIP",
            "HC.PYTHON.METHOD_DOCUMENTATION",
            "HC.PYTHON.TYPING_ANY",
            "HC.PYTHON.CAST_ANY",
            "HC.PYTHON.GENERIC_OBJECT",
            "HC.PYTHON.ERASED_CONTAINER",
            "HC.PYTHON.TEST_RESOURCE_PLACEMENT",
        } <= codes
        assert result.status.value == "fail"
        assert result.blocking

    def test_method__execute__preserves_v1_compatibility_findings(self) -> None:
        """Evidence ID: software-verification.harness.conformance.python.compatibility

        Requirement: The normalized compatibility rule retains v1 acceptance, finding
        multiplicity, meaning, and subject attribution under canonical result order.

        Method: Run the same controlled invalid source and ownership bytes through the
        v1 action and normalized adapter.

        Oracle: The implemented v1 result is the compatibility reference; normalized
        ordering is the shared ValidationResult lexical order.

        Acceptance: Status agrees, TE code multisets agree, and every normalized TE
        finding names one represented input path.

        Interpretation: Failure identifies lost, added, or misattributed v1 behavior.

        Limitations: Strict HC findings are additive and excluded from the comparison.
        """
        subject = self._invalid_subject()
        ownership = subject.inputs_for_role(ConformanceInputRole.OWNERSHIP)[0]
        source = subject.inputs_for_role(ConformanceInputRole.SOURCE)[0]
        assert ownership.payload is not None
        assert source.payload is not None
        legacy = PythonConformanceValidator().execute(
            PythonConformanceRequest(
                sources=(PythonModuleSource(source.path.as_posix(), source.payload),),
                ownership_path=ownership.path.as_posix(),
                ownership_payload=ownership.payload,
            )
        )
        policy = PythonCodingStandardsContract.policy()
        candidate = SUT().execute(
            subject,
            policy.rule_identities,
            PythonCodingStandardsContract.configuration(),
        )
        candidate_te = tuple(
            finding for finding in candidate.findings if finding.code.startswith("TE.")
        )
        assert candidate.status.value == legacy.status.lower()
        assert tuple(finding.code for finding in candidate_te) == tuple(
            sorted(finding.code for finding in legacy.findings)
        )
        represented_paths = {item.path.as_posix() for item in subject.inputs}
        assert all(
            set(finding.affected_paths) <= represented_paths for finding in candidate_te
        )

    def test_method__execute__preserves_ownership_and_parse_failure_compatibility(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.conformance.python.failure-paths

        Requirement: Compatibility adaptation preserves legacy ownership selection,
        parse-failure behavior, diagnostics, and claim boundary.

        Method: Compare both actions for an unowned malformed source and an owned
        malformed source.

        Oracle: The existing PythonConformanceValidator remains the v1 reference.

        Acceptance: Each pair has equal status and TE codes, and the normalized claim
        boundary retains the complete legacy claim-boundary tuple.

        Interpretation: Failure identifies pre-parsing or lossy compatibility mapping.

        Limitations: Strict rules are excluded to isolate v1 compatibility semantics.
        """
        positive = self._positive_subject()
        ownership = positive.inputs_for_role(ConformanceInputRole.OWNERSHIP)[0]
        positive_source = positive.inputs_for_role(ConformanceInputRole.SOURCE)[0]
        unowned = ConformanceSubject(
            subject_family_identity=positive.subject_family_identity,
            inputs=(
                ownership,
                positive_source,
                self._input(
                    "unowned-source",
                    ConformanceInputRole.SOURCE,
                    f"{REPOSITORY_PREFIX}/test__unowned.py",
                    "syntax-invalid-source.txt",
                ),
            ),
        )
        owned_invalid = ConformanceSubject(
            subject_family_identity=positive.subject_family_identity,
            inputs=(
                self._input(
                    "ownership",
                    ConformanceInputRole.OWNERSHIP,
                    f"{REPOSITORY_PREFIX}/syntax-invalid-ownership.json",
                    "syntax-invalid-ownership.json",
                ),
                self._input(
                    "source",
                    ConformanceInputRole.SOURCE,
                    f"{REPOSITORY_PREFIX}/test__syntax_invalid.py",
                    "syntax-invalid-source.txt",
                ),
            ),
        )
        first_legacy, first_candidate = self._compatibility_results(unowned)
        second_legacy, second_candidate = self._compatibility_results(owned_invalid)
        assert first_candidate.status.value == first_legacy.status.lower()
        assert second_candidate.status.value == second_legacy.status.lower()
        assert tuple(item.code for item in first_candidate.findings) == tuple(
            sorted(item.code for item in first_legacy.findings)
        )
        assert tuple(item.code for item in second_candidate.findings) == tuple(
            sorted(item.code for item in second_legacy.findings)
        )
        assert first_candidate.claim_boundary == (
            "implemented Python evidence-structure compatibility only; excludes "
            + ", ".join(first_legacy.claim_boundary)
        )
        assert second_candidate.claim_boundary == (
            "implemented Python evidence-structure compatibility only; excludes "
            + ", ".join(second_legacy.claim_boundary)
        )

    def test_method__execute__accepts_exact_pytest_framework_callables(self) -> None:
        """Evidence ID: software-verification.harness.conformance.python.hooks

        Requirement: Exact pytest fixtures and hooks may remain at conftest module
        scope without creating a general helper exception.

        Method: Apply only the helper-ownership rule to a controlled conftest source.

        Oracle: The literal fixture decorator and pytest hook name are framework-owned
        entry points under the project policy.

        Acceptance: The adapter returns pass without helper-ownership findings.

        Interpretation: Failure identifies overbroad rejection of exact framework
        callables.

        Limitations: Pytest execution and arbitrary plugin hooks are excluded.
        """
        hook_subject = self._source_subject(
            "framework-conftest.txt",
            "python/tests/software_verification/example/conftest.py",
        )
        fixture_subject = self._source_subject(
            "ordinary-fixture-source.txt",
            "python/tests/software_verification/example/test__fixture.py",
        )
        rule = next(
            rule
            for rule in PythonCodingStandardsContract.policy().rule_identities
            if rule.rule_identity == "python.conformance.helper-ownership"
        )
        configuration = PythonCodingStandardsContract.configuration()
        hook_result = SUT().execute(hook_subject, (rule,), configuration)
        fixture_result = SUT().execute(fixture_subject, (rule,), configuration)
        assert hook_result.status.value == fixture_result.status.value == "pass"
        assert hook_result.findings == fixture_result.findings == ()

    def test_method__execute__rejects_near_match_pytest_hook(self) -> None:
        """Evidence ID: software-verification.harness.conformance.python.near-hook

        Requirement: A pytest-like name that is absent from the versioned hook
        inventory receives no framework-owned exemption.

        Method: Apply helper ownership to a conftest containing pytest_not_a_hook.

        Oracle: The literal name is distinct from every supported pytest hook.

        Acceptance: The result fails with exactly one helper-ownership finding.

        Interpretation: Failure identifies permissive prefix-based hook inference.

        Limitations: The supported hook inventory is structural, not a plugin audit.
        """
        subject = self._source_subject(
            "near-hook-source.txt",
            "python/tests/software_verification/example/conftest.py",
        )
        rule = next(
            rule
            for rule in PythonCodingStandardsContract.policy().rule_identities
            if rule.rule_identity == "python.conformance.helper-ownership"
        )
        result = SUT().execute(
            subject, (rule,), PythonCodingStandardsContract.configuration()
        )
        assert tuple(finding.code for finding in result.findings) == (
            "HC.PYTHON.HELPER_OWNERSHIP",
        )

    def test_method__execute__detects_extended_typing_and_callable_facts(self) -> None:
        """Evidence ID: software-verification.harness.conformance.python.typing-facts

        Requirement: Qualified Any, quoted and qualified containers, type-comment
        object, incomplete mappings, and lambda helpers remain visible to policy.

        Method: Apply the four typing rules and helper rule to one controlled source.

        Oracle: Each literal syntax form fixes at least one corresponding finding.

        Acceptance: The result contains Any, object, erased-container, and helper
        finding codes.

        Interpretation: Failure identifies a parser fact or adapter routing gap.

        Limitations: This fixture is not a complete Python name resolver.
        """
        subject = self._source_subject(
            "typing-source.txt",
            "python/tests/software_verification/example/test__typing.py",
        )
        selected_names = {
            "python.conformance.typing-any",
            "python.conformance.generic-object",
            "python.conformance.erased-container",
            "python.conformance.helper-ownership",
        }
        rules = tuple(
            rule
            for rule in PythonCodingStandardsContract.policy().rule_identities
            if rule.rule_identity in selected_names
        )
        result = SUT().execute(
            subject, rules, PythonCodingStandardsContract.configuration()
        )
        codes = {finding.code for finding in result.findings}
        assert {
            "HC.PYTHON.TYPING_ANY",
            "HC.PYTHON.GENERIC_OBJECT",
            "HC.PYTHON.ERASED_CONTAINER",
            "HC.PYTHON.HELPER_OWNERSHIP",
        } <= codes
        assert (
            sum(
                finding.code == "HC.PYTHON.ERASED_CONTAINER"
                for finding in result.findings
            )
            == 3
        )

    def test_method__execute__respects_shadowing_and_explicit_object_semantics(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.conformance.python.typing-policy

        Requirement: Local Any/object/container names are not typing/builtin facts,
        and genuine all-Python-object annotations require explicit configuration.

        Method: Validate one shadowed-name source and one configured object annotation.

        Oracle: Lexical module bindings and the exact path:line declaration determine
        the two permitted cases.

        Acceptance: Both selected-rule results pass without findings.

        Interpretation: Failure identifies name-resolution or policy-configuration
        drift.

        Limitations: Configuration declares semantics; syntax inspection cannot prove
        that a domain genuinely includes every Python object.
        """
        policy = PythonCodingStandardsContract.policy()
        rules = tuple(
            rule
            for rule in policy.rule_identities
            if rule.rule_identity
            in {
                "python.conformance.typing-any",
                "python.conformance.generic-object",
                "python.conformance.erased-container",
            }
        )
        shadowed = self._source_subject(
            "shadowed-names-source.txt",
            "python/tests/software_verification/example/test__shadowed.py",
        )
        universal_path = "python/tests/software_verification/example/test__universal.py"
        universal = self._source_subject("universal-object-source.txt", universal_path)
        shadowed_result = SUT().execute(
            shadowed, rules, PythonCodingStandardsContract.configuration()
        )
        universal_result = SUT().execute(
            universal,
            rules,
            PythonCodingStandardsContract.configuration(
                universal_object_annotations=(f"{universal_path}:1",)
            ),
        )
        assert shadowed_result.status.value == universal_result.status.value == "pass"
        assert shadowed_result.findings == universal_result.findings == ()

    def test_method__execute__rejects_direct_input_identity_mismatch(self) -> None:
        """Evidence ID: software-verification.harness.conformance.python.input-identity

        Requirement: Direct public adapter use cannot validate bytes other than the
        represented subject identity.

        Method: Replace one positive source digest with 64 zeroes and separately
        replace the ownership payload with an explicit represented read failure.

        Oracle: Neither input can establish the represented successful bytes.

        Acceptance: Both direct executions return blocking errors over every selected
        rule.

        Interpretation: Failure identifies an outer-validator-only identity check.

        Limitations: Filesystem observation remains caller-owned.
        """
        valid = self._positive_subject()
        source = valid.inputs_for_role(ConformanceInputRole.SOURCE)[0]
        assert source.payload is not None
        mismatch = ConformanceInput(
            input_identity=source.input_identity,
            role=source.role,
            path=source.path,
            expected_sha256="0" * 64,
            expected_byte_count=source.expected_byte_count,
            payload=source.payload,
            read_error=None,
        )
        subject = ConformanceSubject(
            subject_family_identity=valid.subject_family_identity,
            inputs=tuple(
                mismatch if item.role is ConformanceInputRole.SOURCE else item
                for item in valid.inputs
            ),
        )
        policy = PythonCodingStandardsContract.policy()
        mismatch_result = SUT().execute(
            subject,
            policy.rule_identities,
            PythonCodingStandardsContract.configuration(),
        )
        ownership = valid.inputs_for_role(ConformanceInputRole.OWNERSHIP)[0]
        read_failure = ConformanceInput(
            input_identity=ownership.input_identity,
            role=ownership.role,
            path=ownership.path,
            expected_sha256=ownership.expected_sha256,
            expected_byte_count=ownership.expected_byte_count,
            payload=None,
            read_error="controlled read failure",
        )
        unavailable = ConformanceSubject(
            subject_family_identity=valid.subject_family_identity,
            inputs=tuple(
                read_failure if item.role is ConformanceInputRole.OWNERSHIP else item
                for item in valid.inputs
            ),
        )
        unavailable_result = SUT().execute(
            unavailable,
            policy.rule_identities,
            PythonCodingStandardsContract.configuration(),
        )
        assert (
            mismatch_result.status.value == unavailable_result.status.value == "error"
        )
        assert mismatch_result.rule_identities == policy.rule_identities
        assert unavailable_result.rule_identities == policy.rule_identities
        assert mismatch_result.blocking and unavailable_result.blocking

    def test_method__execute__compatibility_error_retains_selected_rule_closure(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.conformance.python.error-closure

        Requirement: A compatibility input error cannot drop other selected rules from
        the public adapter result.

        Method: Execute the complete policy with a source but no ownership input.

        Oracle: The compatibility rule requires exactly one ownership input while the
        invocation selected the complete policy rule tuple.

        Acceptance: The error result retains every selected rule and remains blocking.

        Interpretation: Failure identifies incomplete direct-adapter result closure.

        Limitations: The outer coordinator's mismatch defense is independently tested.
        """
        subject = self._source_subject(
            "positive-source.txt",
            f"{REPOSITORY_PREFIX}/test__Example.py",
        )
        policy = PythonCodingStandardsContract.policy()
        result = SUT().execute(
            subject,
            policy.rule_identities,
            PythonCodingStandardsContract.configuration(),
        )
        assert result.status.value == "error"
        assert result.rule_identities == policy.rule_identities
        assert result.blocking

    def test_method__execute__is_repeatable_and_nonmutating(self) -> None:
        """Evidence ID: software-verification.harness.conformance.python.nonmutation

        Requirement: Adapter execution depends only on explicit immutable inputs and
        does not repair source bytes.

        Method: Snapshot resource bytes and execute the same subject twice.

        Oracle: Immutable request values and pure syntax inspection require equal
        results and unchanged bytes.

        Acceptance: Results compare equal and every selected resource retains exact
        bytes.

        Interpretation: Failure identifies hidden state, nondeterminism, or mutation.

        Limitations: External callers and filesystem adapters are excluded.
        """
        names = ("positive-ownership.json", "case.json", "positive-source.txt")
        before = tuple((RESOURCE_ROOT / name).read_bytes() for name in names)
        subject = self._positive_subject()
        policy = PythonCodingStandardsContract.policy()
        configuration = PythonCodingStandardsContract.configuration()
        first = SUT().execute(subject, policy.rule_identities, configuration)
        second = SUT().execute(subject, policy.rule_identities, configuration)
        after = tuple((RESOURCE_ROOT / name).read_bytes() for name in names)
        assert first == second
        assert after == before
