r"""Software verification of ``CodingStandardsConformanceValidator``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies explicit policy, profile, adapter, and input composition.

Intrinsic and cross-object scope

The validator is the sole SUT; the Python adapter is an explicit collaborator.

VVUQ and scientific exclusions

Passing establishes structural orchestration only, not behavior, science, UQ, or
acceptance.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath

import pytest

from ksdft2effmass.harness import (
    CodingStandardsConformanceValidator,
    ConformanceAdapterConfiguration,
    ConformanceInput,
    ConformanceInputRole,
    ConformanceProfile,
    ConformanceRequest,
    ConformanceSubject,
    PythonCodingStandardsAdapter,
    PythonCodingStandardsContract,
    ValidationResult,
    ValidationRuleIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = CodingStandardsConformanceValidator
RESOURCE_ROOT = Path(__file__).parent / "resources/conformance"
REPOSITORY_PREFIX = (
    "python/tests/software_verification/ksdft2effmass/harness/resources/conformance"
)


class _ExtraAdapter:
    """Controlled compatible-shaped adapter absent from the selected profile."""

    @property
    def adapter_identity(self) -> str:
        """Return a distinct adapter identity."""
        return "python.extra-adapter"

    @property
    def adapter_version(self) -> str:
        """Return the controlled adapter version."""
        return "1"

    @property
    def subject_family_identities(self) -> tuple[str, ...]:
        """Return the Python test-evidence family."""
        return (PythonCodingStandardsContract.SUBJECT_FAMILY_IDENTITY,)

    @property
    def rule_identities(self) -> tuple[str, ...]:
        """Return no supported rules because execution is prohibited."""
        return ()

    def execute(
        self,
        subject: ConformanceSubject,
        rules: tuple[ValidationRuleIdentity, ...],
        configuration: ConformanceAdapterConfiguration,
    ) -> ValidationResult:
        """Reject invocation because exact profile closure must stop first."""
        raise AssertionError("extra adapter must not execute")


class TestCodingStandardsConformanceValidator:
    """Verify deterministic fail-closed conformance composition."""

    @staticmethod
    def _subject(*, mismatched_source: bool = False) -> ConformanceSubject:
        """Construct one controlled explicit subject with optional source mismatch."""
        ownership_payload = (RESOURCE_ROOT / "positive-ownership.json").read_bytes()
        source_payload = (RESOURCE_ROOT / "positive-source.txt").read_bytes()
        resource_payload = (RESOURCE_ROOT / "case.json").read_bytes()
        source = ConformanceInput.from_payload(
            input_identity="source",
            role=ConformanceInputRole.SOURCE,
            path=PurePosixPath(f"{REPOSITORY_PREFIX}/test__Example.py"),
            payload=source_payload,
        )
        if mismatched_source:
            source = ConformanceInput(
                input_identity="source",
                role=ConformanceInputRole.SOURCE,
                path=source.path,
                expected_sha256="0" * 64,
                expected_byte_count=len(source_payload),
                payload=source_payload,
                read_error=None,
            )
        return ConformanceSubject(
            subject_family_identity=PythonCodingStandardsContract.SUBJECT_FAMILY_IDENTITY,
            inputs=(
                ConformanceInput.from_payload(
                    input_identity="ownership",
                    role=ConformanceInputRole.OWNERSHIP,
                    path=PurePosixPath(f"{REPOSITORY_PREFIX}/positive-ownership.json"),
                    payload=ownership_payload,
                ),
                ConformanceInput.from_payload(
                    input_identity="resource",
                    role=ConformanceInputRole.AUTHORED_TEST_RESOURCE,
                    path=PurePosixPath(f"{REPOSITORY_PREFIX}/case.json"),
                    payload=resource_payload,
                ),
                source,
            ),
        )

    @classmethod
    def _request(cls) -> ConformanceRequest:
        """Construct one complete controlled positive invocation."""
        policy = PythonCodingStandardsContract.policy()
        configuration = PythonCodingStandardsContract.configuration()
        return ConformanceRequest(
            subject=cls._subject(),
            policy=policy,
            profile=PythonCodingStandardsContract.profile(policy, configuration),
            adapters=(PythonCodingStandardsAdapter(),),
            configurations=(configuration,),
        )

    def test_method__execute__composes_complete_normalized_result(self) -> None:
        """Evidence ID: software-verification.harness.conformance.validator.complete

        Requirement: A compatible explicit invocation returns one composite covering
        every policy rule.

        Method: Execute the controlled policy, profile, adapter, configuration, and
        subject.

        Oracle: The profile exact binding set and positive adapter fixture fix a
        complete pass.

        Acceptance: Status is pass, every rule is retained, and one identified child
        is present.

        Interpretation: Failure identifies composition, coverage, or identity drift.

        Limitations: Adapter rule adequacy and source execution are excluded.
        """
        request = self._request()
        result = SUT().execute(request)
        assert result.status.value == "pass"
        assert result.rule_identities == request.policy.rule_identities
        assert len(result.child_results) == 1
        assert result.subject_identity == request.subject.subject_identity
        assert result.configuration_identity == request.profile.content_identity

    def test_method__execute__missing_adapter_fails_closed(self) -> None:
        """Evidence ID: software-verification.harness.conformance.missing-adapter

        Requirement: A required rule cannot disappear when its profiled adapter is
        absent.

        Method: Remove the adapter while retaining the complete profile and
        configuration.

        Oracle: Every profile binding names the absent adapter identity.

        Acceptance: The normalized result is error, blocking, and still contains every
        policy rule.

        Interpretation: Failure would silently weaken an explicit coding policy.

        Limitations: Adapter loading and discovery are intentionally outside the action.
        """
        valid = self._request()
        request = ConformanceRequest(
            subject=valid.subject,
            policy=valid.policy,
            profile=valid.profile,
            adapters=(),
            configurations=valid.configurations,
        )
        result = SUT().execute(request)
        assert result.status.value == "error"
        assert result.blocking
        assert result.rule_identities == valid.policy.rule_identities

    def test_method__execute__incomplete_profile_fails_closed(self) -> None:
        """Evidence ID: software-verification.harness.conformance.profile-closure

        Requirement: A profile cannot omit a policy requirement.

        Method: Construct an identified profile with the final binding omitted.

        Oracle: Exact policy-rule and binding-rule set equality defines completeness.

        Acceptance: Execution returns one blocking error over the complete policy rules.

        Interpretation: Failure would let profile selection weaken policy meaning.

        Limitations: Profile serialization is outside this version-one contract.
        """
        valid = self._request()
        profile = ConformanceProfile(
            profile_identity=valid.profile.profile_identity,
            profile_version=valid.profile.profile_version,
            subject_family_identity=valid.profile.subject_family_identity,
            policy_identity=valid.profile.policy_identity,
            policy_version=valid.profile.policy_version,
            policy_content_identity=valid.profile.policy_content_identity,
            bindings=valid.profile.bindings[:-1],
        )
        request = ConformanceRequest(
            subject=valid.subject,
            policy=valid.policy,
            profile=profile,
            adapters=valid.adapters,
            configurations=valid.configurations,
        )
        result = SUT().execute(request)
        assert result.status.value == "error"
        assert result.rule_identities == valid.policy.rule_identities

    def test_method__execute__rejects_unprofiled_adapter_and_configuration(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.conformance.exact-inventory

        Requirement: The explicit adapter and configuration inventories must exactly
        equal profile selections rather than merely contain them.

        Method: Add one extra adapter and, separately, one extra configuration to the
        controlled valid request.

        Oracle: The profile binding set names only the default Python adapter and
        configuration identity.

        Acceptance: Both invocations return blocking error results before adaptation.

        Interpretation: Failure identifies ignored or unaudited invocation inputs.

        Limitations: Adapter discovery is excluded because all values are explicit.
        """
        valid = self._request()
        adapter_request = ConformanceRequest(
            subject=valid.subject,
            policy=valid.policy,
            profile=valid.profile,
            adapters=(PythonCodingStandardsAdapter(), _ExtraAdapter()),
            configurations=valid.configurations,
        )
        extra = PythonCodingStandardsContract.configuration(
            universal_object_annotations=(
                "python/tests/software_verification/example.py:1",
            )
        )
        configuration_request = ConformanceRequest(
            subject=valid.subject,
            policy=valid.policy,
            profile=valid.profile,
            adapters=valid.adapters,
            configurations=tuple(
                sorted(
                    (*valid.configurations, extra),
                    key=lambda item: (
                        item.adapter_identity,
                        item.adapter_version,
                        item.configuration_identity,
                    ),
                )
            ),
        )
        adapter_result = SUT().execute(adapter_request)
        configuration_result = SUT().execute(configuration_request)
        assert adapter_result.status.value == "error"
        assert configuration_result.status.value == "error"
        assert adapter_result.blocking and configuration_result.blocking

    def test_method__execute__input_identity_mismatch_fails_before_adapter(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.conformance.input-identity

        Requirement: Source bytes that disagree with their expected identity fail
        closed.

        Method: Replace the source expected digest with a distinct valid SHA-256 value.

        Oracle: The literal source digest cannot equal 64 zeroes.

        Acceptance: Execution returns a blocking error without a pass or fail claim.

        Interpretation: Failure would validate bytes other than the identified subject.

        Limitations: Filesystem observation remains caller-owned.
        """
        valid = self._request()
        request = ConformanceRequest(
            subject=self._subject(mismatched_source=True),
            policy=valid.policy,
            profile=valid.profile,
            adapters=valid.adapters,
            configurations=valid.configurations,
        )
        result = SUT().execute(request)
        assert result.status.value == "error"
        assert result.blocking
        assert not result.execution_completed
