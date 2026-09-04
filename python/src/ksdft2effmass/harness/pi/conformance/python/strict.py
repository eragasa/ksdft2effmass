"""Explicit Python coding-standards adapter for normalized conformance results."""

from __future__ import annotations

import re
from pathlib import PurePosixPath

from ....conformance import (
    CodingStandardRequirement,
    CodingStandardsPolicy,
    ConformanceAdapterConfiguration,
    ConformanceInput,
    ConformanceInputRole,
    ConformanceProfile,
    ConformanceProfileBinding,
    ConformanceSubject,
)
from ....validation import ValidationFinding, ValidationResult, ValidationRuleIdentity
from .model import PythonCallableFact
from .parser import PythonTestModuleParser
from .validation import (
    PythonConformanceRequest,
    PythonConformanceValidator,
    PythonModuleSource,
)


class PythonCodingStandardsContract:
    """Own the version-one Python coding-standards policy and profile construction."""

    __slots__ = ()
    SUBJECT_FAMILY_IDENTITY = "python.test-evidence"
    POLICY_IDENTITY = "python.coding-standards"
    POLICY_VERSION = "1"
    PROFILE_IDENTITY = "ksdft2effmass.python.strict"
    PROFILE_VERSION = "1"
    ADAPTER_IDENTITY = "python.coding-standards-adapter"
    ADAPTER_VERSION = "1"
    CONFIGURATION_PAYLOAD = b"schema_version=1\nuniversal_object_annotations=\n"
    RULE_DEFINITIONS = (
        (
            "python.evidence.compatibility",
            "python.conformance.evidence-compatibility",
            "Preserve implemented Python maintained-evidence conformance findings.",
        ),
        (
            "python.pytest.test-class-ownership",
            "python.conformance.test-class-ownership",
            "Collected pytest tests must be methods of explicit Test owner classes.",
        ),
        (
            "python.pytest.helper-ownership",
            "python.conformance.helper-ownership",
            "Module callables must be exact framework hooks or class-owned behavior.",
        ),
        (
            "python.pytest.method-documentation",
            "python.conformance.method-documentation",
            "Collected class-owned test methods must carry maintained evidence "
            "documentation.",
        ),
        (
            "python.typing.any",
            "python.conformance.typing-any",
            "Source must not import or use typing.Any.",
        ),
        (
            "python.typing.cast-any",
            "python.conformance.cast-any",
            "Source must not cast through typing.Any.",
        ),
        (
            "python.typing.generic-object",
            "python.conformance.generic-object",
            "Annotations must not use object as an unspecified software boundary.",
        ),
        (
            "python.typing.erased-container",
            "python.conformance.erased-container",
            "Container annotations must retain explicit element and key/value types.",
        ),
        (
            "python.pytest.resource-placement",
            "python.conformance.test-resource-placement",
            "Authored test resources must reside beneath the applicable tests "
            "resources directory.",
        ),
    )

    @classmethod
    def policy(cls) -> CodingStandardsPolicy:
        """Return the exact immutable version-one strict Python policy."""
        requirements = tuple(
            sorted(
                (
                    CodingStandardRequirement(
                        rule_identity=ValidationRuleIdentity(
                            requirement_identity=requirement,
                            rule_identity=rule,
                            version_identity="1",
                            required=True,
                            not_applicable_permitted=False,
                        ),
                        description=description,
                    )
                    for requirement, rule, description in cls.RULE_DEFINITIONS
                ),
                key=lambda item: item.rule_identity.sort_key,
            )
        )
        return CodingStandardsPolicy(
            policy_identity=cls.POLICY_IDENTITY,
            policy_version=cls.POLICY_VERSION,
            requirements=requirements,
        )

    @classmethod
    def compatibility_policy(cls) -> CodingStandardsPolicy:
        """Return the exact implemented-evidence compatibility policy subset."""
        policy = cls.policy()
        return CodingStandardsPolicy(
            policy_identity=f"{cls.POLICY_IDENTITY}.compatibility",
            policy_version=cls.POLICY_VERSION,
            requirements=tuple(
                requirement
                for requirement in policy.requirements
                if requirement.rule_identity.rule_identity
                == "python.conformance.evidence-compatibility"
            ),
        )

    @classmethod
    def configuration(
        cls, *, universal_object_annotations: tuple[str, ...] = ()
    ) -> ConformanceAdapterConfiguration:
        """Return version-one configuration with explicit universal-object uses."""
        if type(universal_object_annotations) is not tuple or any(
            type(item) is not str for item in universal_object_annotations
        ):
            raise TypeError(
                "universal_object_annotations must contain built-in str values"
            )
        if universal_object_annotations != tuple(
            sorted(set(universal_object_annotations))
        ) or any(
            re.fullmatch(r"[^,\n\r]+:[1-9][0-9]*", item) is None
            for item in universal_object_annotations
        ):
            raise ValueError(
                "universal_object_annotations must be sorted unique path:line values"
            )
        payload = (
            "schema_version=1\nuniversal_object_annotations="
            + ",".join(universal_object_annotations)
            + "\n"
        ).encode("utf-8")
        return ConformanceAdapterConfiguration(
            configuration_identity="",
            adapter_identity=cls.ADAPTER_IDENTITY,
            adapter_version=cls.ADAPTER_VERSION,
            payload=payload,
        )

    @staticmethod
    def _object_annotation_exemptions(
        configuration: ConformanceAdapterConfiguration,
    ) -> frozenset[str] | None:
        try:
            text = configuration.payload.decode("utf-8")
        except UnicodeDecodeError:
            return None
        lines = text.splitlines()
        if len(lines) != 2 or lines[0] != "schema_version=1":
            return None
        prefix = "universal_object_annotations="
        if not lines[1].startswith(prefix):
            return None
        value = lines[1].removeprefix(prefix)
        items = () if value == "" else tuple(value.split(","))
        if items != tuple(sorted(set(items))) or any(
            re.fullmatch(r"[^,\n\r]+:[1-9][0-9]*", item) is None for item in items
        ):
            return None
        canonical = (
            "schema_version=1\nuniversal_object_annotations=" + ",".join(items) + "\n"
        )
        return frozenset(items) if text == canonical else None

    @classmethod
    def profile(
        cls,
        policy: CodingStandardsPolicy,
        configuration: ConformanceAdapterConfiguration,
    ) -> ConformanceProfile:
        """Bind every supplied policy rule to the version-one Python adapter."""
        if type(policy) is not CodingStandardsPolicy:
            raise TypeError("policy must be CodingStandardsPolicy")
        if type(configuration) is not ConformanceAdapterConfiguration:
            raise TypeError("configuration must be ConformanceAdapterConfiguration")
        bindings = tuple(
            sorted(
                (
                    ConformanceProfileBinding(
                        rule_identity=rule.rule_identity,
                        adapter_identity=cls.ADAPTER_IDENTITY,
                        adapter_version=cls.ADAPTER_VERSION,
                        configuration_identity=configuration.configuration_identity,
                    )
                    for rule in policy.rule_identities
                ),
                key=lambda item: item.sort_key,
            )
        )
        return ConformanceProfile(
            profile_identity=cls.PROFILE_IDENTITY,
            profile_version=cls.PROFILE_VERSION,
            subject_family_identity=cls.SUBJECT_FAMILY_IDENTITY,
            policy_identity=policy.policy_identity,
            policy_version=policy.policy_version,
            policy_content_identity=policy.content_identity,
            bindings=bindings,
        )


class PythonCodingStandardsAdapter:
    """Adapt implemented checks and strict syntax facts without filesystem I/O."""

    __slots__ = ()
    _TOOL = "ksdft2effmass.harness.pi.conformance.python:1"
    _PYTEST_HOOKS = frozenset(
        {
            "pytest_addoption",
            "pytest_collection",
            "pytest_collection_finish",
            "pytest_collection_modifyitems",
            "pytest_collect_file",
            "pytest_configure",
            "pytest_deselected",
            "pytest_ignore_collect",
            "pytest_internalerror",
            "pytest_keyboard_interrupt",
            "pytest_report_collectionfinish",
            "pytest_report_header",
            "pytest_runtest_call",
            "pytest_runtest_logreport",
            "pytest_runtest_makereport",
            "pytest_runtest_setup",
            "pytest_runtest_teardown",
            "pytest_sessionfinish",
            "pytest_sessionstart",
            "pytest_terminal_summary",
            "pytest_unconfigure",
        }
    )

    @property
    def adapter_identity(self) -> str:
        """Return the stable adapter identity."""
        return PythonCodingStandardsContract.ADAPTER_IDENTITY

    @property
    def adapter_version(self) -> str:
        """Return the exact adapter behavior version."""
        return PythonCodingStandardsContract.ADAPTER_VERSION

    @property
    def subject_family_identities(self) -> tuple[str, ...]:
        """Return the one supported Python test-evidence family."""
        return (PythonCodingStandardsContract.SUBJECT_FAMILY_IDENTITY,)

    @property
    def rule_identities(self) -> tuple[str, ...]:
        """Return every supported policy rule identity in canonical order."""
        return tuple(
            sorted(
                rule for _, rule, _ in PythonCodingStandardsContract.RULE_DEFINITIONS
            )
        )

    def execute(
        self,
        subject: ConformanceSubject,
        rules: tuple[ValidationRuleIdentity, ...],
        configuration: ConformanceAdapterConfiguration,
    ) -> ValidationResult:
        """Apply only selected compatible rules to one exact explicit subject."""
        if type(subject) is not ConformanceSubject:
            raise TypeError("subject must be ConformanceSubject")
        if type(rules) is not tuple or any(
            type(rule) is not ValidationRuleIdentity for rule in rules
        ):
            raise TypeError("rules must contain ValidationRuleIdentity values")
        if type(configuration) is not ConformanceAdapterConfiguration:
            raise TypeError("configuration must be ConformanceAdapterConfiguration")
        object_exemptions = PythonCodingStandardsContract._object_annotation_exemptions(
            configuration
        )
        if (
            configuration.adapter_identity != self.adapter_identity
            or configuration.adapter_version != self.adapter_version
            or object_exemptions is None
        ):
            return self._error(
                subject, rules, configuration, "adapter configuration is unsupported"
            )
        if subject.subject_family_identity not in self.subject_family_identities:
            return self._error(
                subject, rules, configuration, "subject family is unsupported"
            )
        if any(
            item.read_error is not None or not item.observed_identity_matches
            for item in subject.inputs
        ):
            return self._error(
                subject,
                rules,
                configuration,
                "explicit input bytes do not match their represented identity",
            )
        rule_names = {rule.rule_identity for rule in rules}
        if not rule_names or not rule_names <= set(self.rule_identities):
            return self._error(
                subject, rules, configuration, "selected rule identity is unsupported"
            )
        sources = subject.inputs_for_role(ConformanceInputRole.SOURCE)
        if not sources:
            return self._error(
                subject, rules, configuration, "at least one Python source is required"
            )
        findings: list[ValidationFinding] = []
        rules_by_name = {rule.rule_identity: rule for rule in rules}
        compatibility_rule = rules_by_name.get(
            "python.conformance.evidence-compatibility"
        )
        compatibility_result: ValidationResult | None = None
        if compatibility_rule is not None:
            compatibility = self._compatibility_result(
                subject, compatibility_rule, configuration
            )
            if compatibility.status.value == "error":
                return self._error(
                    subject,
                    rules,
                    configuration,
                    compatibility.error_diagnostic
                    or "compatibility adapter could not establish a result",
                )
            if len(rules) == 1:
                return compatibility
            compatibility_result = compatibility
            findings.extend(compatibility.findings)
        strict_rules_selected = any(
            name != "python.conformance.evidence-compatibility"
            for name in rules_by_name
        )
        try:
            models = (
                tuple(
                    PythonTestModuleParser.execute(
                        item.path.as_posix(), self._payload(item)
                    )
                    for item in sources
                )
                if strict_rules_selected
                else ()
            )
        except (UnicodeError, SyntaxError) as exc:
            return self._error(
                subject,
                rules,
                configuration,
                f"Python source parsing raised {type(exc).__name__}",
            )
        for model in models:
            self._callable_findings(
                subject, model.path, model.callables, rules_by_name, findings
            )
            self._line_findings(
                subject,
                model.path,
                model.any_reference_lines,
                rules_by_name.get("python.conformance.typing-any"),
                "HC.PYTHON.TYPING_ANY",
                "Importing or using typing.Any is prohibited.",
                findings,
            )
            self._line_findings(
                subject,
                model.path,
                model.cast_any_lines,
                rules_by_name.get("python.conformance.cast-any"),
                "HC.PYTHON.CAST_ANY",
                "Casting through typing.Any is prohibited.",
                findings,
            )
            self._line_findings(
                subject,
                model.path,
                model.object_annotation_lines,
                rules_by_name.get("python.conformance.generic-object"),
                "HC.PYTHON.GENERIC_OBJECT",
                "object annotations are prohibited as unspecified software boundaries.",
                findings,
                excluded_locations=object_exemptions,
            )
            self._line_findings(
                subject,
                model.path,
                model.erased_container_annotation_lines,
                rules_by_name.get("python.conformance.erased-container"),
                "HC.PYTHON.ERASED_CONTAINER",
                "Container annotations require explicit element and key/value types.",
                findings,
            )
        placement_rule = rules_by_name.get("python.conformance.test-resource-placement")
        if placement_rule is not None:
            for item in subject.inputs_for_role(
                ConformanceInputRole.AUTHORED_TEST_RESOURCE
            ):
                parts = item.path.parts
                test_index = 1 if parts[:2] == ("python", "tests") else None
                if test_index is None or "resources" not in parts[test_index + 1 :]:
                    findings.append(
                        ValidationFinding.create(
                            rule_identity=placement_rule,
                            code="HC.PYTHON.TEST_RESOURCE_PLACEMENT",
                            subject_identity=subject.subject_identity,
                            summary=(
                                "Authored test resource is outside tests resources."
                            ),
                            affected_paths=(item.path.as_posix(),),
                        )
                    )
        return ValidationResult.from_findings(
            validator_identity="PythonCodingStandardsAdapter:1",
            rule_identities=rules,
            summary="Python coding-standards conformance",
            subject_identity=subject.subject_identity,
            findings=tuple(findings),
            tool_identity=self._TOOL,
            configuration_identity=configuration.configuration_identity,
            evidence_references=tuple(
                sorted({item.expected_sha256 for item in subject.inputs})
            ),
            claim_boundary=(
                "static Python coding-standards conformance only; excludes test "
                "execution, semantic ownership, scientific validity, and acceptance"
                + (
                    ""
                    if compatibility_result is None
                    else f"; {compatibility_result.claim_boundary}"
                )
            ),
        )

    @staticmethod
    def _payload(item: ConformanceInput) -> bytes:
        if type(item) is not ConformanceInput or item.payload is None:
            raise TypeError("successful ConformanceInput payload is required")
        return item.payload

    def _compatibility_result(
        self,
        subject: ConformanceSubject,
        rule: ValidationRuleIdentity,
        configuration: ConformanceAdapterConfiguration,
    ) -> ValidationResult:
        ownership = subject.inputs_for_role(ConformanceInputRole.OWNERSHIP)
        profiles = subject.inputs_for_role(ConformanceInputRole.PROFILE)
        migrations = subject.inputs_for_role(ConformanceInputRole.MIGRATION)
        if len(ownership) != 1 or len(profiles) > 1 or len(migrations) > 1:
            return self._error(
                subject,
                (rule,),
                configuration,
                "compatibility checks require one ownership and at most one profile "
                "and migration input",
            )
        sources = subject.inputs_for_role(ConformanceInputRole.SOURCE)
        profile = profiles[0] if profiles else None
        migration = migrations[0] if migrations else None
        ownership_input = ownership[0]
        request = PythonConformanceRequest(
            sources=tuple(
                PythonModuleSource(item.path.as_posix(), self._payload(item))
                for item in sources
            ),
            ownership_path=ownership_input.path.as_posix(),
            ownership_payload=self._payload(ownership_input),
            migration_path=None if migration is None else migration.path.as_posix(),
            migration_payload=None if migration is None else self._payload(migration),
            profile_path=None if profile is None else profile.path.as_posix(),
            profile_payload=None if profile is None else self._payload(profile),
        )
        result = PythonConformanceValidator().execute(request)
        findings = tuple(
            ValidationFinding.create(
                rule_identity=rule,
                code=item.code,
                subject_identity=subject.subject_identity,
                summary=(
                    " ".join(item.message.split())
                    + ("" if item.line is None else f" Line {item.line}.")
                ),
                affected_paths=self._affected_path(subject, item.path),
            )
            for item in result.findings
        )
        return ValidationResult.from_findings(
            validator_identity="PythonEvidenceCompatibilityAdapter:1",
            rule_identities=(rule,),
            summary="Implemented Python evidence conformance compatibility",
            subject_identity=subject.subject_identity,
            findings=findings,
            tool_identity=self._TOOL,
            configuration_identity=configuration.configuration_identity,
            evidence_references=tuple(
                sorted({item.expected_sha256 for item in subject.inputs})
            ),
            claim_boundary=(
                "implemented Python evidence-structure compatibility only; excludes "
                + ", ".join(result.claim_boundary)
            ),
        )

    @staticmethod
    def _affected_path(subject: ConformanceSubject, path: str) -> tuple[str, ...]:
        represented = {item.path.as_posix() for item in subject.inputs}
        return (path,) if path in represented else ()

    @staticmethod
    def _callable_findings(
        subject: ConformanceSubject,
        path: str,
        callables: tuple[PythonCallableFact, ...],
        rules: dict[str, ValidationRuleIdentity],
        findings: list[ValidationFinding],
    ) -> None:
        for value in callables:
            if type(value) is not PythonCallableFact:
                raise TypeError("callables must contain PythonCallableFact values")
            test_rule = rules.get("python.conformance.test-class-ownership")
            if value.is_test and (
                value.owner_class_name is None
                or not value.owner_class_name.startswith("Test")
            ):
                if test_rule is not None:
                    findings.append(
                        ValidationFinding.create(
                            rule_identity=test_rule,
                            code="HC.PYTHON.TEST_CLASS_OWNERSHIP",
                            subject_identity=subject.subject_identity,
                            summary=(
                                f"Collected test at line {value.line} lacks a Test "
                                "owner class."
                            ),
                            affected_paths=(path,),
                        )
                    )
            documentation_rule = rules.get("python.conformance.method-documentation")
            if (
                documentation_rule is not None
                and value.is_test
                and value.owner_class_name is not None
                and value.owner_class_name.startswith("Test")
                and not value.has_documentation
            ):
                findings.append(
                    ValidationFinding.create(
                        rule_identity=documentation_rule,
                        code="HC.PYTHON.METHOD_DOCUMENTATION",
                        subject_identity=subject.subject_identity,
                        summary=(
                            f"Collected test method at line {value.line} lacks "
                            "documentation."
                        ),
                        affected_paths=(path,),
                    )
                )
            helper_rule = rules.get("python.conformance.helper-ownership")
            if (
                helper_rule is not None
                and value.owner_class_name is None
                and not value.is_test
                and not PythonCodingStandardsAdapter._framework_owned(path, value)
            ):
                findings.append(
                    ValidationFinding.create(
                        rule_identity=helper_rule,
                        code="HC.PYTHON.HELPER_OWNERSHIP",
                        subject_identity=subject.subject_identity,
                        summary=(
                            f"Module callable at line {value.line} lacks an explicit "
                            "class owner."
                        ),
                        affected_paths=(path,),
                    )
                )

    @staticmethod
    def _framework_owned(path: str, value: PythonCallableFact) -> bool:
        if type(value) is not PythonCallableFact:
            raise TypeError("value must be PythonCallableFact")
        if any(decorator == "pytest.fixture" for decorator in value.decorator_names):
            return True
        return (
            PurePosixPath(path).name == "conftest.py"
            and value.name in PythonCodingStandardsAdapter._PYTEST_HOOKS
        )

    @staticmethod
    def _line_findings(
        subject: ConformanceSubject,
        path: str,
        lines: tuple[int, ...],
        rule: ValidationRuleIdentity | None,
        code: str,
        summary: str,
        findings: list[ValidationFinding],
        *,
        excluded_locations: frozenset[str] = frozenset(),
    ) -> None:
        if rule is None:
            return
        findings.extend(
            ValidationFinding.create(
                rule_identity=rule,
                code=code,
                subject_identity=subject.subject_identity,
                summary=f"{summary} Line {line}.",
                affected_paths=(path,),
            )
            for line in lines
            if f"{path}:{line}" not in excluded_locations
        )

    def _error(
        self,
        subject: ConformanceSubject,
        rules: tuple[ValidationRuleIdentity, ...],
        configuration: ConformanceAdapterConfiguration,
        diagnostic: str,
    ) -> ValidationResult:
        return ValidationResult.error(
            validator_identity="PythonCodingStandardsAdapter:1",
            rule_identities=rules,
            summary="Python coding-standards adapter could not establish pass or fail",
            subject_identity=subject.subject_identity,
            error_diagnostic=diagnostic,
            tool_identity=self._TOOL,
            configuration_identity=configuration.configuration_identity,
            claim_boundary=(
                "static Python coding-standards conformance only; excludes test "
                "execution, semantic ownership, scientific validity, and acceptance"
            ),
        )
