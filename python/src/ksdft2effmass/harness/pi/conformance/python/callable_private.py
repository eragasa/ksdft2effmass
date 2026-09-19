"""Explicit-input callable and private-owner architecture rules.

This unsupported implementation sibling evaluates immutable facts produced by
:class:`~ksdft2effmass.harness.pi.conformance.python.production.PythonProductionSourceInspector`.
It deterministically enforces syntax-grounded callable ownership, non-underscore
top-level class names, hook-exception integrity, and cross-owner private calls only
when accepted facts establish both owners without name-binding inference. Current
facts establish no non-self receiver owner, so such private-looking calls are
structural observations. Semantic ownership of public, scientific, numerical,
comparison, compatibility, or validation policy remains a canonical review-only rule,
but produces no finding because the accepted facts contain no semantic metadata.

The evaluator accepts exact facts and exact hook exceptions only. It performs no
filesystem discovery, source repair, renaming, export decision, dependency-graph
analysis, or runtime dispatch inference. The retained facts currently represent calls,
not general non-call attribute access, so enforcement makes no broader claim.
Software-verification results from this module do not establish runtime behavior,
numerical verification, scientific validation, uncertainty quantification, or human
acceptance.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath

from .production import (
    PythonProductionCallableFact,
    PythonProductionCallableKind,
    PythonProductionInspectionResult,
    PythonProductionLexicalOwner,
    PythonProductionLocation,
    PythonProductionModuleInspection,
    PythonProductionScopeKind,
)


class PythonArchitectureRuleClassification(StrEnum):
    """Classify one rule independently of any finding outcome or severity."""

    DETERMINISTIC_ENFORCEMENT = "deterministic_enforcement"
    DETERMINISTIC_STRUCTURAL_OBSERVATION = "deterministic_structural_observation"
    REVIEW_ONLY_SIGNAL = "review_only_signal"


class PythonArchitectureFindingOutcome(StrEnum):
    """Identify whether a finding is a violation, observation, or review signal."""

    VIOLATION = "violation"
    OBSERVATION = "observation"
    REVIEW_SIGNAL = "review_signal"


class PythonArchitectureFindingSeverity(StrEnum):
    """Represent finding impact without changing the owning rule classification."""

    ERROR = "error"
    INFORMATION = "information"
    REVIEW = "review"


class PythonHookOwnerKind(StrEnum):
    """Identify the external contract category that owns an exact module hook."""

    FRAMEWORK = "framework"
    LANGUAGE = "language"
    PACKAGING = "packaging"


class PythonHookCallableShape(StrEnum):
    """Identify the exact named callable shape accepted by a hook exception."""

    FUNCTION = "function"
    ASYNC_FUNCTION = "async_function"


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonArchitectureRuleIdentity:
    """Represent one stable rule identity and exactly one classification.

    Parameters
    ----------
    rule_identity
        Stable versioned identity.
    classification
        Enforcement, structural-observation, or review-only classification.
    description
        Concise bounded meaning of the rule.
    """

    rule_identity: str
    classification: PythonArchitectureRuleClassification
    description: str

    def __post_init__(self) -> None:
        """Require normalized identities, exact classification, and description."""
        self._require_text(self.rule_identity, "rule_identity")
        self._require_text(self.description, "description")
        if type(self.classification) is not PythonArchitectureRuleClassification:
            raise TypeError(
                "classification must be PythonArchitectureRuleClassification"
            )

    @staticmethod
    def _require_text(value: str, name: str) -> None:
        """Require normalized nonempty single-line built-in text."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if (
            not value
            or "\n" in value
            or "\r" in value
            or unicodedata.normalize("NFC", value) != value
        ):
            raise ValueError(f"{name} must be normalized nonempty single-line text")


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonCallableIdentity:
    """Identify one exact callable fact within one source module.

    Parameters
    ----------
    qualified_name
        Dot-separated lexical callable name.
    kind
        Exact named-function, asynchronous-function, or lambda syntax kind.
    location
        Exact callable definition span.
    """

    qualified_name: str
    kind: PythonProductionCallableKind
    location: PythonProductionLocation

    def __post_init__(self) -> None:
        """Require a complete exact callable identity."""
        if type(self.qualified_name) is not str:
            raise TypeError("qualified_name must be a built-in str")
        if not self.qualified_name:
            raise ValueError("qualified_name must be nonempty")
        if type(self.kind) is not PythonProductionCallableKind:
            raise TypeError("kind must be PythonProductionCallableKind")
        if type(self.location) is not PythonProductionLocation:
            raise TypeError("location must be PythonProductionLocation")

    @classmethod
    def from_fact(cls, fact: PythonProductionCallableFact) -> PythonCallableIdentity:
        """Construct the exact identity retained by a callable fact.

        Parameters
        ----------
        fact
            Accepted immutable production callable fact.

        Returns
        -------
        PythonCallableIdentity
            Exact lexical identity and source span.
        """
        if type(fact) is not PythonProductionCallableFact:
            raise TypeError("fact must be PythonProductionCallableFact")
        return cls(
            qualified_name=fact.qualified_name,
            kind=fact.kind,
            location=fact.location,
        )


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonModuleHookException:
    """Bind one exact module callable to an external hook contract.

    Parameters
    ----------
    source_path
        Exact normalized repository-relative diagnostic path.
    source_sha256
        Exact lowercase SHA-256 identity of the supplied source bytes.
    callable_identity
        Exact callable name, syntax kind, and span.
    hook_owner
        Normalized external framework, language, or packaging owner identity.
    hook_kind
        External contract category.
    applicable_shape
        Exact named synchronous or asynchronous function shape.

    Notes
    -----
    The exception is not a waiver. The evaluator rejects duplicate, stale,
    identity-mismatched, shape-mismatched, and unused entries.
    """

    source_path: PurePosixPath
    source_sha256: str
    callable_identity: PythonCallableIdentity
    hook_owner: str
    hook_kind: PythonHookOwnerKind
    applicable_shape: PythonHookCallableShape

    def __post_init__(self) -> None:
        """Require exact normalized source, callable, and hook attribution."""
        if type(self.source_path) is not PurePosixPath:
            raise TypeError("source_path must be PurePosixPath")
        rendered = self.source_path.as_posix()
        if (
            rendered in {"", "."}
            or self.source_path.is_absolute()
            or ".." in self.source_path.parts
            or "\\" in rendered
            or unicodedata.normalize("NFC", rendered) != rendered
        ):
            raise ValueError("source_path must be normalized repository-relative POSIX")
        if type(self.source_sha256) is not str:
            raise TypeError("source_sha256 must be a built-in str")
        if len(self.source_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.source_sha256
        ):
            raise ValueError("source_sha256 must be lowercase SHA-256 hexadecimal")
        if type(self.callable_identity) is not PythonCallableIdentity:
            raise TypeError("callable_identity must be PythonCallableIdentity")
        PythonArchitectureRuleIdentity._require_text(self.hook_owner, "hook_owner")
        if type(self.hook_kind) is not PythonHookOwnerKind:
            raise TypeError("hook_kind must be PythonHookOwnerKind")
        if type(self.applicable_shape) is not PythonHookCallableShape:
            raise TypeError("applicable_shape must be PythonHookCallableShape")

    @property
    def sort_key(self) -> tuple[str, str, str, str, int, int, str, str, str]:
        """Return complete stable hook-exception ordering state."""
        location = self.callable_identity.location
        return (
            self.source_path.as_posix(),
            self.source_sha256,
            self.callable_identity.qualified_name,
            self.callable_identity.kind.value,
            location.line,
            location.column,
            self.hook_owner,
            self.hook_kind.value,
            self.applicable_shape.value,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonCallablePrivateRuleRequest:
    """Represent exact immutable inputs to callable/private-rule evaluation.

    Parameters
    ----------
    production_facts
        Accepted explicit-input production inspection result.
    hook_exceptions
        Exact immutable external-hook exception inputs.
    """

    production_facts: PythonProductionInspectionResult
    hook_exceptions: tuple[PythonModuleHookException, ...]

    def __post_init__(self) -> None:
        """Require exact accepted facts and immutable hook exception values."""
        if type(self.production_facts) is not PythonProductionInspectionResult:
            raise TypeError("production_facts must be PythonProductionInspectionResult")
        if type(self.hook_exceptions) is not tuple or any(
            type(exception) is not PythonModuleHookException
            for exception in self.hook_exceptions
        ):
            raise TypeError(
                "hook_exceptions must contain PythonModuleHookException values"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonArchitectureFinding:
    """Represent one exact attributed rule result.

    Parameters
    ----------
    rule
        Stable rule identity and classification.
    outcome, severity
        Finding result and impact, kept distinct from rule classification.
    source_path, source_sha256, location
        Exact source attribution; location is absent only for source-level exception
        identity failures.
    owner_identity
        Exact lexical caller or definition owner when statically represented.
    receiver_owner_identity
        Statically resolved receiver owner for cross-owner findings.
    callee_expression
        Exact retained call expression when the finding concerns a call.
    hook_exception
        Exact hook input when the finding concerns exception integrity.
    message
        Deterministic bounded diagnostic.
    """

    rule: PythonArchitectureRuleIdentity
    outcome: PythonArchitectureFindingOutcome
    severity: PythonArchitectureFindingSeverity
    source_path: PurePosixPath
    source_sha256: str
    location: PythonProductionLocation | None
    owner_identity: str | None
    receiver_owner_identity: str | None
    callee_expression: str | None
    hook_exception: PythonModuleHookException | None
    message: str

    def __post_init__(self) -> None:
        """Require canonical rule, compatible result state, and exact attribution."""
        if type(self.rule) is not PythonArchitectureRuleIdentity:
            raise TypeError("rule must be PythonArchitectureRuleIdentity")
        if self.rule not in PythonCallablePrivateRuleEvaluator.RULES:
            raise ValueError("rule must be one canonical callable/private rule")
        if type(self.outcome) is not PythonArchitectureFindingOutcome:
            raise TypeError("outcome must be PythonArchitectureFindingOutcome")
        if type(self.severity) is not PythonArchitectureFindingSeverity:
            raise TypeError("severity must be PythonArchitectureFindingSeverity")
        compatible = {
            PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT: (
                PythonArchitectureFindingOutcome.VIOLATION,
                PythonArchitectureFindingSeverity.ERROR,
            ),
            PythonArchitectureRuleClassification.DETERMINISTIC_STRUCTURAL_OBSERVATION: (
                PythonArchitectureFindingOutcome.OBSERVATION,
                PythonArchitectureFindingSeverity.INFORMATION,
            ),
            PythonArchitectureRuleClassification.REVIEW_ONLY_SIGNAL: (
                PythonArchitectureFindingOutcome.REVIEW_SIGNAL,
                PythonArchitectureFindingSeverity.REVIEW,
            ),
        }
        if (self.outcome, self.severity) != compatible[self.rule.classification]:
            raise ValueError("outcome and severity must match rule classification")
        if type(self.source_path) is not PurePosixPath:
            raise TypeError("source_path must be PurePosixPath")
        rendered_path = self.source_path.as_posix()
        if (
            rendered_path in {"", "."}
            or self.source_path.is_absolute()
            or ".." in self.source_path.parts
            or "\\" in rendered_path
            or unicodedata.normalize("NFC", rendered_path) != rendered_path
        ):
            raise ValueError("source_path must be normalized repository-relative POSIX")
        if type(self.source_sha256) is not str:
            raise TypeError("source_sha256 must be a built-in str")
        if len(self.source_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.source_sha256
        ):
            raise ValueError("source_sha256 must be lowercase SHA-256 hexadecimal")
        if (
            self.location is not None
            and type(self.location) is not PythonProductionLocation
        ):
            raise TypeError("location must be PythonProductionLocation or None")
        for name, value in (
            ("owner_identity", self.owner_identity),
            ("receiver_owner_identity", self.receiver_owner_identity),
            ("callee_expression", self.callee_expression),
        ):
            if value is not None:
                if type(value) is not str:
                    raise TypeError(f"{name} must be built-in str or None")
                if not value or unicodedata.normalize("NFC", value) != value:
                    raise ValueError(f"{name} must be normalized nonempty text or None")
        if (
            self.hook_exception is not None
            and type(self.hook_exception) is not PythonModuleHookException
        ):
            raise TypeError("hook_exception must be PythonModuleHookException or None")
        if type(self.message) is not str:
            raise TypeError("message must be a built-in str")
        if (
            not self.message
            or "\n" in self.message
            or "\r" in self.message
            or unicodedata.normalize("NFC", self.message) != self.message
        ):
            raise ValueError("message must be normalized nonempty single-line text")

    @property
    def sort_key(self) -> tuple[str, str, int, int, str, str, str, str]:
        """Return stable rule, path, span, owner, call, and message ordering state."""
        rule_order = PythonCallablePrivateRuleEvaluator.RULE_ORDER.index(
            self.rule.rule_identity
        )
        return (
            f"{rule_order:02d}",
            self.source_path.as_posix(),
            -1 if self.location is None else self.location.line,
            -1 if self.location is None else self.location.column,
            self.owner_identity or "",
            self.receiver_owner_identity or "",
            self.callee_expression or "",
            self.message,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonCallablePrivateRuleResult:
    """Represent immutable canonical rules and attributed findings.

    Parameters
    ----------
    rules
        Complete stable rule inventory in evaluator-defined order.
    findings
        Canonically ordered violations, observations, and review signals.
    """

    rules: tuple[PythonArchitectureRuleIdentity, ...]
    findings: tuple[PythonArchitectureFinding, ...]

    def __post_init__(self) -> None:
        """Require exact rule closure and canonical immutable finding order."""
        if type(self.rules) is not tuple or any(
            type(rule) is not PythonArchitectureRuleIdentity for rule in self.rules
        ):
            raise TypeError("rules must contain PythonArchitectureRuleIdentity values")
        if self.rules != PythonCallablePrivateRuleEvaluator.RULES:
            raise ValueError("rules must equal the exact canonical rule tuple")
        if type(self.findings) is not tuple or any(
            type(finding) is not PythonArchitectureFinding for finding in self.findings
        ):
            raise TypeError("findings must contain PythonArchitectureFinding values")
        if any(finding.rule not in self.rules for finding in self.findings):
            raise ValueError("every finding rule must belong to the canonical tuple")
        if self.findings != tuple(
            sorted(self.findings, key=lambda item: item.sort_key)
        ):
            raise ValueError("findings must be in canonical order")


class PythonCallablePrivateRuleEvaluator:
    """Evaluate exact callable/private rules over supplied production facts.

    The ActionObject has no mutable state. Resolution is deliberately conservative:
    a private call is prohibited only when accepted facts establish both owners
    without Python name-binding inference. Current facts establish lexical caller
    ownership and the explicitly permitted owner-local ``self`` case, but do not
    establish non-self receiver bindings. Class-name, constructor-name, alias,
    computed, parameter-shadowable, local-shadowable, and other non-self receivers
    therefore remain observations. General attribute access is outside the accepted
    call-fact representation.
    """

    __slots__ = ()

    HOOK_EXCEPTION_INTEGRITY = PythonArchitectureRuleIdentity(
        rule_identity="python.callable-private.hook-exception-integrity.v1",
        classification=PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT,
        description=(
            "Hook exceptions must be exact, unique, current, shape-matched, and used."
        ),
    )
    MODULE_CALLABLE_OWNER = PythonArchitectureRuleIdentity(
        rule_identity="python.callable-private.module-callable-owner.v1",
        classification=PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT,
        description="A module callable requires an exact applicable hook exception.",
    )
    TOP_LEVEL_CLASS_NAME = PythonArchitectureRuleIdentity(
        rule_identity="python.callable-private.top-level-class-name.v1",
        classification=PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT,
        description=("A top-level implementation class uses a non-underscore name."),
    )
    CROSS_OWNER_PRIVATE_CALL = PythonArchitectureRuleIdentity(
        rule_identity="python.callable-private.cross-owner-private-call.v1",
        classification=PythonArchitectureRuleClassification.DETERMINISTIC_ENFORCEMENT,
        description=(
            "A resolved class owner cannot call another owner's private method."
        ),
    )
    UNRESOLVED_PRIVATE_CALL = PythonArchitectureRuleIdentity(
        rule_identity="python.callable-private.unresolved-private-call.v1",
        classification=PythonArchitectureRuleClassification.DETERMINISTIC_STRUCTURAL_OBSERVATION,
        description=(
            "An unresolved private-looking call is retained without guessed ownership."
        ),
    )
    SEMANTIC_PRIVATE_POLICY = PythonArchitectureRuleIdentity(
        rule_identity="python.callable-private.semantic-private-policy.v1",
        classification=PythonArchitectureRuleClassification.REVIEW_ONLY_SIGNAL,
        description=(
            "Semantic policy ownership requires separately supplied explicit metadata."
        ),
    )
    RULES = (
        HOOK_EXCEPTION_INTEGRITY,
        MODULE_CALLABLE_OWNER,
        TOP_LEVEL_CLASS_NAME,
        CROSS_OWNER_PRIVATE_CALL,
        UNRESOLVED_PRIVATE_CALL,
        SEMANTIC_PRIVATE_POLICY,
    )
    RULE_ORDER = tuple(rule.rule_identity for rule in RULES)

    def execute(
        self, request: PythonCallablePrivateRuleRequest
    ) -> PythonCallablePrivateRuleResult:
        """Evaluate one explicit immutable request without mutating source or facts.

        Parameters
        ----------
        request
            Exact accepted production facts and exact hook exception inputs.

        Returns
        -------
        PythonCallablePrivateRuleResult
            Stable rule inventory and canonically attributed findings.

        Raises
        ------
        TypeError
            If the request is not the exact request DataObject.
        """
        if type(request) is not PythonCallablePrivateRuleRequest:
            raise TypeError("request must be PythonCallablePrivateRuleRequest")
        findings: list[PythonArchitectureFinding] = []
        valid_hooks = self._evaluate_hook_exceptions(request, findings)
        for module in request.production_facts.modules:
            if module.facts is None or module.source_sha256 is None:
                continue
            self._evaluate_module(module, valid_hooks, findings)
        return PythonCallablePrivateRuleResult(
            rules=self.RULES,
            findings=tuple(sorted(findings, key=lambda item: item.sort_key)),
        )

    def _evaluate_hook_exceptions(
        self,
        request: PythonCallablePrivateRuleRequest,
        findings: list[PythonArchitectureFinding],
    ) -> frozenset[PythonModuleHookException]:
        """Validate every hook input and return only exact applicable exceptions."""
        ordered = tuple(sorted(request.hook_exceptions, key=lambda item: item.sort_key))
        valid: set[PythonModuleHookException] = set()
        for exception in ordered:
            if ordered.count(exception) > 1:
                if not any(
                    finding.hook_exception == exception
                    and finding.message == "duplicate hook exception"
                    for finding in findings
                ):
                    findings.append(
                        self._hook_finding(
                            exception,
                            "duplicate hook exception",
                            location=None,
                            owner_identity=None,
                        )
                    )
                continue
            path_modules = tuple(
                module
                for module in request.production_facts.modules
                if module.path == exception.source_path
            )
            if not path_modules:
                findings.append(
                    self._hook_finding(
                        exception,
                        "stale hook source path",
                        location=None,
                        owner_identity=None,
                    )
                )
                continue
            identity_modules = tuple(
                module
                for module in path_modules
                if module.source_sha256 == exception.source_sha256
            )
            if not identity_modules:
                findings.append(
                    self._hook_finding(
                        exception,
                        "mismatched hook source identity",
                        location=None,
                        owner_identity=None,
                    )
                )
                continue
            callable_facts = tuple(
                fact
                for module in identity_modules
                if module.facts is not None
                for fact in module.facts.callables
                if PythonCallableIdentity.from_fact(fact) == exception.callable_identity
            )
            if not callable_facts:
                findings.append(
                    self._hook_finding(
                        exception,
                        "stale hook callable",
                        location=None,
                        owner_identity=None,
                    )
                )
                continue
            fact = callable_facts[0]
            expected_shape = self._shape_for(fact.kind)
            if (
                expected_shape is None
                or expected_shape is not exception.applicable_shape
            ):
                findings.append(
                    self._hook_finding(
                        exception,
                        "mismatched hook callable shape",
                        location=fact.location,
                        owner_identity=fact.qualified_name,
                    )
                )
                continue
            if fact.owners:
                findings.append(
                    self._hook_finding(
                        exception,
                        "unused hook for owned callable",
                        location=fact.location,
                        owner_identity=fact.qualified_name,
                    )
                )
                continue
            valid.add(exception)
        return frozenset(valid)

    def _evaluate_module(
        self,
        module: PythonProductionModuleInspection,
        valid_hooks: frozenset[PythonModuleHookException],
        findings: list[PythonArchitectureFinding],
    ) -> None:
        """Evaluate one successfully parsed module with exact source identity."""
        facts = module.facts
        source_sha256 = module.source_sha256
        if facts is None or source_sha256 is None:
            raise AssertionError("module evaluation requires successful exact facts")
        for callable_fact in facts.callables:
            if not callable_fact.owners:
                identity = PythonCallableIdentity.from_fact(callable_fact)
                exempt = any(
                    exception.source_path == module.path
                    and exception.source_sha256 == source_sha256
                    and exception.callable_identity == identity
                    for exception in valid_hooks
                )
                if not exempt:
                    findings.append(
                        PythonArchitectureFinding(
                            rule=self.MODULE_CALLABLE_OWNER,
                            outcome=PythonArchitectureFindingOutcome.VIOLATION,
                            severity=PythonArchitectureFindingSeverity.ERROR,
                            source_path=module.path,
                            source_sha256=source_sha256,
                            location=callable_fact.location,
                            owner_identity=callable_fact.qualified_name,
                            receiver_owner_identity=None,
                            callee_expression=None,
                            hook_exception=None,
                            message=("module callable lacks an exact hook exception"),
                        )
                    )
        for class_fact in facts.classes:
            if not class_fact.owners and class_fact.name.startswith("_"):
                findings.append(
                    PythonArchitectureFinding(
                        rule=self.TOP_LEVEL_CLASS_NAME,
                        outcome=PythonArchitectureFindingOutcome.VIOLATION,
                        severity=PythonArchitectureFindingSeverity.ERROR,
                        source_path=module.path,
                        source_sha256=source_sha256,
                        location=class_fact.location,
                        owner_identity=class_fact.qualified_name,
                        receiver_owner_identity=None,
                        callee_expression=None,
                        hook_exception=None,
                        message=(
                            "top-level implementation class name starts with underscore"
                        ),
                    )
                )
        for call in facts.calls:
            if call.callee_name is None or not self._is_private(call.callee_name):
                continue
            caller_owner = self._caller_owner(call.owners)
            receiver_owner = self._receiver_owner(
                call.receiver_expression, caller_owner
            )
            if caller_owner is not None and receiver_owner is not None:
                if caller_owner != receiver_owner:
                    findings.append(
                        PythonArchitectureFinding(
                            rule=self.CROSS_OWNER_PRIVATE_CALL,
                            outcome=PythonArchitectureFindingOutcome.VIOLATION,
                            severity=PythonArchitectureFindingSeverity.ERROR,
                            source_path=module.path,
                            source_sha256=source_sha256,
                            location=call.location,
                            owner_identity=caller_owner,
                            receiver_owner_identity=receiver_owner,
                            callee_expression=call.callee_expression,
                            hook_exception=None,
                            message="statically resolved cross-owner private call",
                        )
                    )
            else:
                findings.append(
                    PythonArchitectureFinding(
                        rule=self.UNRESOLVED_PRIVATE_CALL,
                        outcome=PythonArchitectureFindingOutcome.OBSERVATION,
                        severity=PythonArchitectureFindingSeverity.INFORMATION,
                        source_path=module.path,
                        source_sha256=source_sha256,
                        location=call.location,
                        owner_identity=caller_owner,
                        receiver_owner_identity=receiver_owner,
                        callee_expression=call.callee_expression,
                        hook_exception=None,
                        message=(
                            "private-looking call ownership is not statically resolved"
                        ),
                    )
                )

    def _hook_finding(
        self,
        exception: PythonModuleHookException,
        message: str,
        *,
        location: PythonProductionLocation | None,
        owner_identity: str | None,
    ) -> PythonArchitectureFinding:
        """Construct one hook violation with only verified source attribution."""
        return PythonArchitectureFinding(
            rule=self.HOOK_EXCEPTION_INTEGRITY,
            outcome=PythonArchitectureFindingOutcome.VIOLATION,
            severity=PythonArchitectureFindingSeverity.ERROR,
            source_path=exception.source_path,
            source_sha256=exception.source_sha256,
            location=location,
            owner_identity=owner_identity,
            receiver_owner_identity=None,
            callee_expression=None,
            hook_exception=exception,
            message=message,
        )

    @staticmethod
    def _shape_for(
        kind: PythonProductionCallableKind,
    ) -> PythonHookCallableShape | None:
        """Return the exact supported hook shape for one callable syntax kind."""
        if kind is PythonProductionCallableKind.FUNCTION:
            return PythonHookCallableShape.FUNCTION
        if kind is PythonProductionCallableKind.ASYNC_FUNCTION:
            return PythonHookCallableShape.ASYNC_FUNCTION
        return None

    @staticmethod
    def _is_private(name: str) -> bool:
        """Return whether a syntactic name is single-underscore private-looking."""
        return name.startswith("_") and not (
            name.startswith("__") and name.endswith("__")
        )

    @staticmethod
    def _caller_owner(
        owners: tuple[PythonProductionLexicalOwner, ...],
    ) -> str | None:
        """Return the innermost exact lexical class owner, when represented."""
        for owner in reversed(owners):
            if owner.kind is PythonProductionScopeKind.CLASS:
                return owner.qualified_name
        return None

    @staticmethod
    def _receiver_owner(
        receiver_expression: str | None,
        caller_owner: str | None,
    ) -> str | None:
        """Resolve only the authority-permitted exact owner-local self syntax."""
        if receiver_expression == "self":
            return caller_owner
        return None
