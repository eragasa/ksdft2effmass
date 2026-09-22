r"""Software verification of explicit-input callable and private-owner rule contract.

Evidence profile: claim_bearing

Bounded artifact scope: explicit-input callable and private-owner rule contract.

Facet and represented meaning

This module verifies exact hook exceptions, canonical records, deterministic syntax
enforcement, conservative call-owner observations, and metadata-free review boundaries.

Intrinsic and cross-object scope

Immutable rule, callable-identity, exception, request, finding, and result records own
intrinsic closure; one evaluator owns cross-record policy over accepted production
facts. Option B text, Python binding limitations, exact authored facts, and stable
expected findings are the oracles.

VVUQ and scientific exclusions

Passing establishes bounded structural software behavior only. It establishes no
runtime dispatch completeness, semantic ownership classification, numerical
verification, scientific validation, uncertainty quantification, support disposition,
source repair, export decision, or human acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path, PurePosixPath
from typing import Literal

import pytest

from ksdft2effmass.harness.pi.conformance.python.callable_private import (
    PythonArchitectureFinding,
    PythonArchitectureFindingOutcome,
    PythonArchitectureFindingSeverity,
    PythonArchitectureRuleClassification,
    PythonArchitectureRuleIdentity,
    PythonCallableIdentity,
    PythonCallablePrivateRuleEvaluator,
    PythonCallablePrivateRuleRequest,
    PythonCallablePrivateRuleResult,
    PythonHookCallableShape,
    PythonHookOwnerKind,
    PythonModuleHookException,
)
from ksdft2effmass.harness.pi.conformance.python.production import (
    PythonProductionCallableKind,
    PythonProductionInspectionResult,
    PythonProductionLocation,
    PythonProductionModuleInspection,
    PythonProductionSource,
    PythonProductionSourceInspector,
    PythonProductionSourceProfile,
)

pytestmark = pytest.mark.software_verification
RESOURCE = (
    Path(__file__).parent / "resources/callable_private_rules/representative.py.txt"
)
SOURCE_PATH = PurePosixPath("python/src/example/representative.py")


class TestCallablePrivateRules:
    """Verify the artifact contract through exact unsupported implementation values."""

    @staticmethod
    def inspect(
        payload: bytes, *, path: PurePosixPath = SOURCE_PATH
    ) -> PythonProductionInspectionResult:
        """Produce accepted representative facts from exact caller-supplied bytes."""
        source = PythonProductionSource.from_payload(
            input_identity="callable-private-test",
            path=path,
            payload=payload,
        )
        return PythonProductionSourceInspector().execute(
            PythonProductionSourceProfile(), (source,)
        )

    @staticmethod
    def module(
        inspection: PythonProductionInspectionResult,
    ) -> PythonProductionModuleInspection:
        """Return the sole successful module from one controlled inspection."""
        module = inspection.modules[0]
        assert module.facts is not None
        assert module.source_sha256 is not None
        return module

    @classmethod
    def hook_for(
        cls,
        inspection: PythonProductionInspectionResult,
        qualified_name: str,
        *,
        source_path: PurePosixPath = SOURCE_PATH,
        source_sha256: str | None = None,
        shape: PythonHookCallableShape | None = None,
    ) -> PythonModuleHookException:
        """Bind one exact retained callable to a controlled external hook identity."""
        module = cls.module(inspection)
        facts = module.facts
        assert facts is not None
        callable_fact = next(
            fact for fact in facts.callables if fact.qualified_name == qualified_name
        )
        applicable_shape = shape
        if applicable_shape is None:
            applicable_shape = (
                PythonHookCallableShape.ASYNC_FUNCTION
                if callable_fact.kind is PythonProductionCallableKind.ASYNC_FUNCTION
                else PythonHookCallableShape.FUNCTION
            )
        return PythonModuleHookException(
            source_path=source_path,
            source_sha256=source_sha256 or module.source_sha256 or "",
            callable_identity=PythonCallableIdentity.from_fact(callable_fact),
            hook_owner="pytest.console-entry-point",
            hook_kind=PythonHookOwnerKind.FRAMEWORK,
            applicable_shape=applicable_shape,
        )

    @staticmethod
    def evaluate_result(
        inspection: PythonProductionInspectionResult,
        *exceptions: PythonModuleHookException,
    ) -> PythonCallablePrivateRuleResult:
        """Execute the artifact and return its immutable canonical result."""
        return PythonCallablePrivateRuleEvaluator().execute(
            PythonCallablePrivateRuleRequest(
                production_facts=inspection,
                hook_exceptions=exceptions,
            )
        )

    @classmethod
    def evaluate(
        cls,
        inspection: PythonProductionInspectionResult,
        *exceptions: PythonModuleHookException,
    ) -> tuple[PythonArchitectureFinding, ...]:
        """Execute the artifact and return its immutable findings."""
        return cls.evaluate_result(inspection, *exceptions).findings

    def test_artifact__callable_private_rules__enforces_only_grounded_syntax(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.callable-private.option-b

        Requirement: Exact hooks permit entry points; dangling callables and
        underscore top-level class names violate Option B, owner-local ``self``
        mechanics are permitted, and non-self private calls are only observations.

        Method: Inspect the maintained fixture, supply the exact ``run`` hook, and
        project stable rule, outcome, owner, receiver, call, and span fields.

        Oracle: Accepted Option B text, Python syntax, and manual inspection of the
        exact authored fixture.

        Acceptance: Findings are exactly one dangling-callable violation, one
        non-underscore-name violation, and two unresolved-call observations; there is
        no cross-owner or semantic-policy finding.

        Interpretation: Failure identifies unsound enforcement, attribution, or
        semantic inference.

        Limitations: The fixture is parsed but never imported or executed.
        """
        inspection = self.inspect(RESOURCE.read_bytes())
        findings = self.evaluate(inspection, self.hook_for(inspection, "run"))
        assert tuple(
            (
                finding.rule.rule_identity,
                finding.outcome,
                finding.owner_identity,
                finding.receiver_owner_identity,
                finding.callee_expression,
                None if finding.location is None else finding.location.line,
            )
            for finding in findings
        ) == (
            (
                "python.callable-private.module-callable-owner.v1",
                PythonArchitectureFindingOutcome.VIOLATION,
                "dangling",
                None,
                None,
                8,
            ),
            (
                "python.callable-private.top-level-class-name.v1",
                PythonArchitectureFindingOutcome.VIOLATION,
                "_HiddenOwner",
                None,
                None,
                12,
            ),
            (
                "python.callable-private.unresolved-private-call.v1",
                PythonArchitectureFindingOutcome.OBSERVATION,
                "DescriptiveOwner",
                None,
                "OtherOwner()._secret",
                22,
            ),
            (
                "python.callable-private.unresolved-private-call.v1",
                PythonArchitectureFindingOutcome.OBSERVATION,
                "DescriptiveOwner",
                None,
                "dynamic_target._dynamic",
                23,
            ),
        )
        assert all(finding.source_path == SOURCE_PATH for finding in findings)
        assert all(
            finding.source_sha256 == self.module(inspection).source_sha256
            for finding in findings
        )
        assert all(finding.callee_expression != "self._local" for finding in findings)
        assert all(
            finding.rule
            is not PythonCallablePrivateRuleEvaluator.CROSS_OWNER_PRIVATE_CALL
            for finding in findings
        )
        assert all(
            finding.rule
            is not PythonCallablePrivateRuleEvaluator.SEMANTIC_PRIVATE_POLICY
            for finding in findings
        )

    def test_artifact__private_calls__observes_shadowable_nonself_receivers(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.callable-private.shadowing

        Requirement: Class-name, constructor-name, alias, computed,
        parameter-shadowable, and local-shadowable receivers are observations because
        v1 facts do not establish their Python bindings.

        Method: Inspect exact inline counterexamples containing direct class-name and
        zero-argument-constructor spellings plus parameter, local, alias, and computed
        receivers.

        Oracle: Python names can be rebound and accepted production facts retain no
        assignment, parameter-binding, import-binding, or dispatch resolution.

        Acceptance: All six non-self private calls are unresolved observations with no
        receiver owner or cross-owner violation; ``self._local()`` emits no finding.

        Interpretation: Failure identifies name-based ownership inference.

        Limitations: Richer binding facts require separate future authority.
        """
        inspection = self.inspect(
            b"class Caller:\n"
            b"    def _local(self):\n        return None\n"
            b"    def evaluate(self, OtherOwner, target):\n"
            b"        self._local()\n"
            b"        OtherOwner._secret()\n"
            b"        OtherOwner()._secret()\n"
            b"        alias = OtherOwner\n"
            b"        alias._secret()\n"
            b"        LocalOwner = target\n"
            b"        LocalOwner._secret()\n"
            b"        factory()._secret()\n"
            b"        target._secret()\n"
            b"class OtherOwner:\n"
            b"    def _secret(self):\n        return None\n"
        )
        findings = self.evaluate(inspection)
        observations = tuple(
            finding
            for finding in findings
            if finding.rule
            is PythonCallablePrivateRuleEvaluator.UNRESOLVED_PRIVATE_CALL
        )
        assert tuple(finding.callee_expression for finding in observations) == (
            "OtherOwner._secret",
            "OtherOwner()._secret",
            "alias._secret",
            "LocalOwner._secret",
            "factory()._secret",
            "target._secret",
        )
        assert all(finding.receiver_owner_identity is None for finding in observations)
        assert all(
            finding.rule
            is not PythonCallablePrivateRuleEvaluator.CROSS_OWNER_PRIVATE_CALL
            for finding in findings
        )
        assert all(finding.callee_expression != "self._local" for finding in findings)
        assert all(
            finding.rule
            is not PythonCallablePrivateRuleEvaluator.SEMANTIC_PRIVATE_POLICY
            for finding in findings
        )

    @pytest.mark.parametrize(
        ("case", "expected_message", "has_verified_location", "expected_owner"),
        (
            pytest.param(
                "stale_path",
                "stale hook source path",
                False,
                None,
                id="stale_source_path",
            ),
            pytest.param(
                "source_mismatch",
                "mismatched hook source identity",
                False,
                None,
                id="mismatched_source_identity",
            ),
            pytest.param(
                "stale_callable",
                "stale hook callable",
                False,
                None,
                id="stale_callable_identity",
            ),
            pytest.param(
                "shape_mismatch",
                "mismatched hook callable shape",
                True,
                "run",
                id="mismatched_callable_shape",
            ),
            pytest.param(
                "unused_owned",
                "unused hook for owned callable",
                True,
                "DescriptiveOwner.evaluate",
                id="unused_owned_callable",
            ),
        ),
    )
    def test_artifact__hook_exceptions__rejects_with_verified_attribution(
        self,
        case: Literal[
            "stale_path",
            "source_mismatch",
            "stale_callable",
            "shape_mismatch",
            "unused_owned",
        ],
        expected_message: str,
        has_verified_location: bool,
        expected_owner: str | None,
    ) -> None:
        """Evidence ID: software-verification.harness.callable-private.hook-rejection

        Requirement: Nonapplicable hook inputs fail closed, and source locations are
        retained only after source identity and callable matching verifies them.

        Method: Alter one exact binding dimension per semantic parameter case.

        Oracle: Exact source identity, callable identity, lexical owner, and named
        function-shape fields from accepted facts.

        Acceptance: Each case emits one exact integrity violation retaining the hook
        input; stale path/identity/callable cases have no verified location or owner,
        while shape and owned-callable cases retain the matched fact attribution.

        Interpretation: Failure identifies an unsound exemption or false attribution.

        Limitations: External framework behavior is represented, not invoked.
        """
        inspection = self.inspect(RESOURCE.read_bytes())
        base = self.hook_for(inspection, "run")
        if case == "stale_path":
            exception = self.hook_for(
                inspection,
                "run",
                source_path=PurePosixPath("python/src/example/missing.py"),
            )
        elif case == "source_mismatch":
            exception = self.hook_for(inspection, "run", source_sha256="0" * 64)
        elif case == "stale_callable":
            exception = PythonModuleHookException(
                source_path=base.source_path,
                source_sha256=base.source_sha256,
                callable_identity=PythonCallableIdentity(
                    qualified_name="missing",
                    kind=PythonProductionCallableKind.FUNCTION,
                    location=PythonProductionLocation(
                        line=1, column=0, end_line=1, end_column=1
                    ),
                ),
                hook_owner=base.hook_owner,
                hook_kind=base.hook_kind,
                applicable_shape=base.applicable_shape,
            )
        elif case == "shape_mismatch":
            exception = self.hook_for(
                inspection,
                "run",
                shape=PythonHookCallableShape.ASYNC_FUNCTION,
            )
        else:
            exception = self.hook_for(inspection, "DescriptiveOwner.evaluate")
        hook_findings = tuple(
            finding
            for finding in self.evaluate(inspection, exception)
            if finding.rule
            is PythonCallablePrivateRuleEvaluator.HOOK_EXCEPTION_INTEGRITY
        )
        assert len(hook_findings) == 1
        finding = hook_findings[0]
        assert finding.message == expected_message
        assert finding.hook_exception == exception
        assert (finding.location is not None) is has_verified_location
        assert finding.owner_identity == expected_owner
        assert finding.outcome is PythonArchitectureFindingOutcome.VIOLATION

    def test_artifact__hook_exceptions__rejects_duplicates_without_false_span(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.callable-private.hook-duplicate

        Requirement: Duplicate exact hooks are rejected without claiming an unverified
        source span and do not exempt a module callable.

        Method: Supply the same immutable exception twice.

        Oracle: Tuple multiplicity, exact DataObject equality, and verified-attribution
        policy.

        Acceptance: One duplicate violation retains the exact hook but has no location
        or owner, and the ``run`` callable remains a violation.

        Interpretation: Failure identifies duplicate collapse, waiver, or false span.

        Limitations: Unequal owner labels represent distinct explicit contracts.
        """
        inspection = self.inspect(RESOURCE.read_bytes())
        hook = self.hook_for(inspection, "run")
        findings = self.evaluate(inspection, hook, hook)
        duplicate = next(
            finding
            for finding in findings
            if finding.message == "duplicate hook exception"
        )
        assert duplicate.hook_exception == hook
        assert duplicate.location is None
        assert duplicate.owner_identity is None
        assert any(finding.owner_identity == "run" for finding in findings)

    def test_artifact__callable_private_rules__retains_canonical_classifications(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.callable-private.classifications

        Requirement: The exact canonical rule tuple retains all three classifications,
        while metadata-free private methods emit no semantic-policy signal.

        Method: Execute representative facts and inspect the complete rule tuple and
        emitted finding rules.

        Oracle: The accepted three-way Phase 2 classification contract and exact
        versioned canonical records.

        Acceptance: Six exact rules occur in canonical order with four enforcement,
        one observation, and one review-only classification; no review finding exists.

        Interpretation: Failure identifies rule substitution, reclassification, or
        semantic inference from underscore spelling.

        Limitations: No semantic metadata is supplied or invented.
        """
        inspection = self.inspect(RESOURCE.read_bytes())
        result = self.evaluate_result(inspection, self.hook_for(inspection, "run"))
        assert result.rules == PythonCallablePrivateRuleEvaluator.RULES
        assert tuple(rule.classification for rule in result.rules) == (
            PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT,
            PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT,
            PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT,
            PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT,
            PythonArchitectureRuleClassification.DETERMINISTIC_STRUCTURAL_OBSERVATION,
            PythonArchitectureRuleClassification.REVIEW_ONLY_SIGNAL,
        )
        assert not any(
            finding.rule is PythonCallablePrivateRuleEvaluator.SEMANTIC_PRIVATE_POLICY
            for finding in result.findings
        )

    def test_artifact__hook_records__reject_invalid_source_identity(self) -> None:
        """Evidence ID: software-verification.harness.callable-private.hook-records

        Requirement: Hook records require exact normalized repository-relative paths,
        lowercase hexadecimal SHA-256, and precise semantic types.

        Method: Replace one exact field of a valid hook with wrong-type or invalid
        same-type values.

        Oracle: POSIX path semantics and lowercase SHA-256 grammar.

        Acceptance: Wrong semantic types raise ``TypeError`` and malformed paths or
        digests raise ``ValueError``.

        Interpretation: Failure identifies a hook record that can carry ambiguous
        source attribution.

        Limitations: Digest-to-content correspondence is checked by evaluation.
        """
        inspection = self.inspect(RESOURCE.read_bytes())
        hook = self.hook_for(inspection, "run")
        with pytest.raises(ValueError, match="repository-relative POSIX"):
            replace(hook, source_path=PurePosixPath("../outside.py"))
        with pytest.raises(ValueError, match="lowercase SHA-256"):
            replace(hook, source_sha256="A" * 64)
        with pytest.raises(TypeError, match="source_path must be PurePosixPath"):
            replace(hook, source_path="pkg/source.py")  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="source_sha256 must be a built-in str"):
            replace(hook, source_sha256=7)  # type: ignore[arg-type]

    def test_artifact__finding_records__rejects_impostor_and_contradictory_state(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.callable-private.finding-closure

        Requirement: Findings require a canonical rule, compatible
        classification/outcome/severity, normalized nonempty paths, and lowercase
        hexadecimal SHA-256 attribution.

        Method: Replace one field of a valid finding with exact contradictory or
        malformed values, including an equal-identity impostor rule.

        Oracle: Canonical evaluator rules, three-way result compatibility, POSIX path
        semantics, and lowercase SHA-256 grammar.

        Acceptance: Wrong semantic types raise ``TypeError``; impostor, contradictory,
        invalid path, and invalid digest values raise ``ValueError``.

        Interpretation: Failure identifies constructible contradictory result state.

        Limitations: Cryptographic content correspondence remains the caller's supplied
        production-fact contract.
        """
        inspection = self.inspect(RESOURCE.read_bytes())
        base = self.evaluate_result(inspection).findings[0]
        impostor = PythonArchitectureRuleIdentity(
            rule_identity=base.rule.rule_identity,
            classification=base.rule.classification,
            description="Impostor description.",
        )
        with pytest.raises(ValueError, match="canonical callable/private rule"):
            replace(base, rule=impostor)
        with pytest.raises(ValueError, match="match rule classification"):
            replace(base, outcome=PythonArchitectureFindingOutcome.OBSERVATION)
        with pytest.raises(ValueError, match="match rule classification"):
            replace(base, severity=PythonArchitectureFindingSeverity.INFORMATION)
        with pytest.raises(ValueError, match="repository-relative POSIX"):
            replace(base, source_path=PurePosixPath("../outside.py"))
        with pytest.raises(ValueError, match="lowercase SHA-256"):
            replace(base, source_sha256="A" * 64)
        with pytest.raises(TypeError, match="source_path must be PurePosixPath"):
            replace(base, source_path="pkg/source.py")  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="source_sha256 must be a built-in str"):
            replace(base, source_sha256=7)  # type: ignore[arg-type]

    def test_artifact__result_records__require_exact_canonical_closure(self) -> None:
        """Evidence ID: software-verification.harness.callable-private.result-closure

        Requirement: A result contains the exact canonical rule tuple and canonically
        ordered findings whose rules belong to that tuple.

        Method: Construct results with reversed rules, one same-identity impostor rule,
        and reversed findings.

        Oracle: Exact tuple equality with evaluator-owned rules and finding sort keys.

        Acceptance: Every noncanonical construction raises the precise ``ValueError``
        boundary while the evaluator result constructs successfully.

        Interpretation: Failure identifies substitutable or contradictory result state.

        Limitations: The test does not reproduce evaluator finding selection.
        """
        inspection = self.inspect(RESOURCE.read_bytes())
        result = self.evaluate_result(inspection)
        with pytest.raises(ValueError, match="exact canonical rule tuple"):
            PythonCallablePrivateRuleResult(
                rules=tuple(reversed(result.rules)), findings=()
            )
        impostor = replace(result.rules[0], description="Impostor description.")
        with pytest.raises(ValueError, match="exact canonical rule tuple"):
            PythonCallablePrivateRuleResult(
                rules=(impostor, *result.rules[1:]), findings=()
            )
        with pytest.raises(ValueError, match="canonical order"):
            PythonCallablePrivateRuleResult(
                rules=result.rules,
                findings=tuple(reversed(result.findings)),
            )

    def test_artifact__callable_private_records__are_deeply_immutable(self) -> None:
        """Evidence ID: software-verification.harness.callable-private.immutability

        Requirement: Every claimed rule, callable identity, hook, request, finding, and
        result record family is frozen, with tuple-owned collections.

        Method: Construct one exact family graph and attempt one field assignment on
        each record type.

        Oracle: Frozen slotted dataclass and tuple semantics.

        Acceptance: Every assignment raises ``FrozenInstanceError`` and all retained
        collections remain tuples.

        Interpretation: Failure identifies mutable retained policy or parser state.

        Limitations: Reflection outside ordinary public APIs is excluded.
        """
        inspection = self.inspect(RESOURCE.read_bytes())
        hook = self.hook_for(inspection, "run")
        request = PythonCallablePrivateRuleRequest(
            production_facts=inspection, hook_exceptions=(hook,)
        )
        result = PythonCallablePrivateRuleEvaluator().execute(request)
        finding = result.findings[0]
        rule = result.rules[0]
        identity = hook.callable_identity
        assert type(request.hook_exceptions) is tuple
        assert type(result.rules) is tuple
        assert type(result.findings) is tuple
        with pytest.raises(FrozenInstanceError):
            rule.description = "changed"  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            identity.qualified_name = "changed"  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            hook.hook_owner = "changed"  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            request.hook_exceptions = ()  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            finding.message = "changed"  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            result.findings = ()  # type: ignore[misc]

    def test_artifact__callable_private_rules__has_no_discovery_repair_or_export_effect(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Evidence ID: software-verification.harness.callable-private.boundaries

        Requirement: Evaluation consumes only supplied facts, mutates neither bytes nor
        facts, performs no discovery or repair, and creates no supported import route.

        Method: Build facts first, prohibit path reads/writes during evaluation, compare
        exact input values, and inspect the accepted package namespace.

        Oracle: Exact immutable input equality, prohibited filesystem effects, and
        deliberate package export membership.

        Acceptance: Evaluation succeeds without reads/writes, inputs remain unchanged,
        and the evaluator is absent from the package namespace.

        Interpretation: Failure identifies discovery, mutation, repair, or export
        widening.

        Limitations: Git and external processes are not invoked by the evaluator.
        """
        payload = RESOURCE.read_bytes()
        inspection = self.inspect(payload)
        original = inspection
        hook = self.hook_for(inspection, "run")

        def prohibit_read(path: Path) -> bytes:
            raise AssertionError(f"unexpected read: {path}")

        def prohibit_write(path: Path, data: bytes) -> int:
            raise AssertionError(f"unexpected write: {path} {len(data)}")

        monkeypatch.setattr(Path, "read_bytes", prohibit_read)
        monkeypatch.setattr(Path, "write_bytes", prohibit_write)
        assert self.evaluate(inspection, hook)
        assert inspection == original

        import ksdft2effmass.harness.pi.conformance.python as python_conformance

        assert not hasattr(python_conformance, "PythonCallablePrivateRuleEvaluator")
        assert payload.startswith(b"from __future__ import annotations")
