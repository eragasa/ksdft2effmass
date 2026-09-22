r"""Software verification of conformance input and policy records.

Evidence profile: claim_bearing

Bounded artifact scope: normalized coding-standards conformance DataObjects.

Facet and represented meaning

This module verifies exact inputs, identities, policy requirements, and profile
bindings.

Intrinsic and cross-object scope

The records own intrinsic closure only; adapters and orchestration are separate owners.

VVUQ and scientific exclusions

Passing establishes software contracts only, not source correctness, science, UQ,
or acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import PurePosixPath

import pytest

from ksdft2effmass.harness import (
    CodingStandardRequirement,
    CodingStandardsPolicy,
    ConformanceInput,
    ConformanceInputRole,
    ConformanceSubject,
    PythonCodingStandardsContract,
    ValidationRuleIdentity,
)

pytestmark = pytest.mark.software_verification


class TestConformanceRecords:
    """Verify immutable exact-input and policy record invariants."""

    def test_classmethod__from_payload__derives_closed_subject_identity(self) -> None:
        """Evidence ID: software-verification.harness.conformance.records.identity

        Requirement: Exact input bytes and metadata determine one immutable subject
        identity.

        Method: Construct one input from literal bytes and one subject from that input.

        Oracle: SHA-256 fixes the input digest and repeated construction fixes equality.

        Acceptance: The digest has 64 lowercase characters and equal inputs derive
        equal subjects.

        Interpretation: Failure identifies nondeterministic or incomplete identity
        closure.

        Limitations: External file identity and adapter behavior are excluded.
        """
        source = ConformanceInput.from_payload(
            input_identity="source",
            role=ConformanceInputRole.SOURCE,
            path=PurePosixPath("python/tests/example.py"),
            payload=b"pass\n",
        )
        first = ConformanceSubject(
            subject_family_identity="python.test-evidence", inputs=(source,)
        )
        second = ConformanceSubject(
            subject_family_identity="python.test-evidence", inputs=(source,)
        )
        assert len(source.expected_sha256) == len(first.subject_identity) == 64
        assert source.observed_identity_matches
        assert first == second
        with pytest.raises(FrozenInstanceError):
            first.subject_identity = "0" * 64  # type: ignore[misc]

    def test_constructor__mismatched_observation__remains_representable(self) -> None:
        """Evidence ID: software-verification.harness.conformance.records.mismatch

        Requirement: A caller-observed identity mismatch remains an explicit
        validation input.

        Method: Supply bytes with a different well-formed expected digest.

        Oracle: SHA-256 of the literal payload is not 64 zeroes.

        Acceptance: Construction succeeds and observed_identity_matches is false.

        Interpretation: Failure would hide an input defect before closed validation.

        Limitations: The conformance action's error result is verified separately.
        """
        value = ConformanceInput(
            input_identity="source",
            role=ConformanceInputRole.SOURCE,
            path=PurePosixPath("python/tests/example.py"),
            expected_sha256="0" * 64,
            expected_byte_count=5,
            payload=b"pass\n",
            read_error=None,
        )
        assert not value.observed_identity_matches

    def test_classmethod__contract__binds_every_rule_without_reclassification(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.conformance.records.profile

        Requirement: The strict profile binds every policy rule exactly once to one
        adapter configuration.

        Method: Construct the public version-one policy, configuration, and profile.

        Oracle: Exact set equality between policy rules and binding rules defines
        closure.

        Acceptance: Identities are derived and binding names equal policy names in
        sorted order.

        Interpretation: Failure identifies omitted, added, or reclassified requirements.

        Limitations: Adapter execution and policy adequacy are excluded.
        """
        policy = PythonCodingStandardsContract.policy()
        configuration = PythonCodingStandardsContract.configuration()
        profile = PythonCodingStandardsContract.profile(policy, configuration)
        assert tuple(binding.rule_identity for binding in profile.bindings) == tuple(
            sorted(rule.rule_identity for rule in policy.rule_identities)
        )
        assert profile.policy_content_identity == policy.content_identity
        assert all(
            binding.configuration_identity == configuration.configuration_identity
            for binding in profile.bindings
        )

    def test_constructor__duplicate_policy_rule__is_rejected(self) -> None:
        """Evidence ID: software-verification.harness.conformance.records.unique-rule

        Requirement: One policy cannot assign conflicting meaning to one rule identity.

        Method: Construct two requirements containing the same exact rule.

        Oracle: Rule-identity uniqueness is an intrinsic policy invariant.

        Acceptance: Policy construction raises ValueError.

        Interpretation: Failure would make profile and finding attribution ambiguous.

        Limitations: Distinct semantic descriptions are not compared for equivalence.
        """
        rule = ValidationRuleIdentity(
            requirement_identity="example.requirement",
            rule_identity="example.rule",
            version_identity="1",
            required=True,
            not_applicable_permitted=False,
        )
        item = CodingStandardRequirement(
            rule_identity=rule, description="Controlled requirement."
        )
        with pytest.raises(ValueError):
            CodingStandardsPolicy(
                policy_identity="example.policy",
                policy_version="1",
                requirements=(item, item),
            )
