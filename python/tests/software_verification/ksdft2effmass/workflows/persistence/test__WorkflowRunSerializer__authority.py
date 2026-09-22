r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: authority variants and canonical UTC microsecond timestamps.

Evidence profile: claim_bearing

Facet and represented meaning

Independent synthetic literals and public constructors specify all grant states,
authorization outcomes and snapshot-check values, including UTC year boundaries.

Intrinsic and cross-object scope

The codec preserves represented authority records without running authorization,
resolving an authority source, validating history closure or committing a claim.

VVUQ and scientific exclusions

Software representation evidence only. Supplied verification labels are synthetic;
these fixtures establish no authentic authority, scientific result or effect permission.
"""

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

import pytest

from ksdft2effmass import workflows as w
from ksdft2effmass.analysis import QuantityOfInterestResultValueSerializer
from ksdft2effmass.workflows import WorkflowRunSerializer

type AuthorityVariant = Literal["preparation", "claim", "denied", "error"]
type VerificationField = Literal[
    "content_verification",
    "authentication_verification",
    "predecessor_closure",
    "revocation_closure",
]

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Own independent authority wire oracles, not authorization-policy oracles."""

    @staticmethod
    def wire(variant: AuthorityVariant = "preparation") -> bytes:
        return (
            Path(__file__)
            .with_name("resources")
            .joinpath(f"workflow-run-authority-{variant}-v1.json")
            .read_bytes()
        )

    @staticmethod
    def make_run(genesis: w.WorkflowRun, variant: AuthorityVariant) -> w.WorkflowRun:
        """Construct one supplied authority record, without calling an authorizer."""
        reference = w.ScientificExecutionAuthorityReference(
            grant_identity=w.ExecutionGrantIdentity("grant"),
            grant_revision_identity=w.ExecutionGrantRevisionIdentity("grant-revision"),
            snapshot_identity=w.ScientificExecutionAuthoritySnapshotIdentity(
                "snapshot"
            ),
            state_identity=w.ScientificExecutionAuthorityStateIdentity("state"),
        )
        snapshot = w.ScientificExecutionAuthoritySnapshot(
            identity=reference.snapshot_identity,
            source_identity="synthetic-source",
            issuer_identity="synthetic-issuer",
            trust_configuration_identity="synthetic-trust",
            content_verification_identity="content-check",
            authentication_verification_identity="authentication-check",
            predecessor_closure_identity="predecessor-check",
            revocation_closure_identity="revocation-check",
            content_verification=(
                w.ScientificExecutionAuthorityVerificationKind.INDETERMINATE
                if variant == "error"
                else w.ScientificExecutionAuthorityVerificationKind.VERIFIED
            ),
            authentication_verification=(
                w.ScientificExecutionAuthorityVerificationKind.FAILED
                if variant == "denied"
                else w.ScientificExecutionAuthorityVerificationKind.VERIFIED
            ),
            predecessor_closure=w.ScientificExecutionAuthorityVerificationKind.VERIFIED,
            revocation_closure=w.ScientificExecutionAuthorityVerificationKind.VERIFIED,
            valid_from=datetime(1, 1, 1, 0, 0, 0, 1, tzinfo=UTC),
            valid_until=datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=UTC),
            verified_at=datetime(2024, 2, 29, 12, 34, 56, 123456, tzinfo=UTC),
            fresh_until=datetime(2024, 2, 29, 12, 34, 56, 654321, tzinfo=UTC),
            resolver_implementation_identity="synthetic-resolver:1",
        )
        state = {
            "preparation": w.ScientificExecutionGrantState.UNUSED,
            "claim": w.ScientificExecutionGrantState.RESERVED,
            "denied": w.ScientificExecutionGrantState.REVOKED,
            "error": w.ScientificExecutionGrantState.CLAIMED,
        }[variant]
        grant = w.ScientificExecutionAuthorityGrant(
            authority_reference=reference,
            authority_source_identity="synthetic-source",
            issuer_identity="synthetic-issuer",
            request_identity=w.SimulationExecutionRequestIdentity("request"),
            workflow_run_identity=genesis.identity,
            task_definition_identity=w.TaskDefinitionIdentity("task-definition"),
            task_instance_identity=w.TaskInstanceIdentity("task-instance"),
            activation_identity=w.TaskActivationIdentity("activation"),
            operation_identity=w.OperationIdentity("operation"),
            attempt_identity=w.AttemptIdentity("attempt"),
            executor_identity=w.ScientificExecutorIdentity("executor"),
            destination_identity=w.DispatchDestinationIdentity("destination"),
            resource_scope_identities=(
                w.DispatchResourceScopeIdentity("scope-a"),
                w.DispatchResourceScopeIdentity("scope-b"),
            ),
            input_result_reference_identities=(
                w.ResultObjectReferenceIdentity("input-a"),
                w.ResultObjectReferenceIdentity("input-b"),
            ),
            input_artifact_entry_identities=(
                w.ArtifactManifestEntryIdentity("artifact-a"),
                w.ArtifactManifestEntryIdentity("artifact-b"),
            ),
            valid_from=datetime(2024, 2, 29, 12, 34, 56, 1, tzinfo=UTC),
            valid_until=datetime(2024, 2, 29, 13, 34, 56, 999999, tzinfo=UTC),
            state=state,
            reserved_obligation_identity=(
                w.ObligationIdentity("obligation")
                if variant in ("claim", "error")
                else None
            ),
        )
        request = w.SimulationExecutionAuthorizationRequest(
            result_identity=w.SimulationExecutionAuthorizationResultIdentity(
                "authorization"
            ),
            phase=(
                w.SimulationExecutionAuthorizationPhase.CLAIM
                if variant == "claim"
                else w.SimulationExecutionAuthorizationPhase.PREPARATION
            ),
            grant=grant,
            snapshot=snapshot,
            request_identity=grant.request_identity,
            workflow_run_identity=genesis.identity,
            task_definition_identity=grant.task_definition_identity,
            task_instance_identity=grant.task_instance_identity,
            activation_identity=grant.activation_identity,
            operation_identity=grant.operation_identity,
            attempt_identity=grant.attempt_identity,
            executor_identity=grant.executor_identity,
            destination_identity=grant.destination_identity,
            obligation_identity=w.ObligationIdentity("obligation"),
            resource_scope_identities=grant.resource_scope_identities,
            input_result_reference_identities=grant.input_result_reference_identities,
            input_artifact_entry_identities=grant.input_artifact_entry_identities,
            evaluated_at=datetime(2024, 2, 29, 12, 34, 56, 123457, tzinfo=UTC),
        )
        kind = {
            "preparation": w.SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED,
            "claim": w.SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED,
            "denied": w.SimulationExecutionAuthorizationOutcomeKind.DENIED,
            "error": w.SimulationExecutionAuthorizationOutcomeKind.ERROR,
        }[variant]
        result = w.SimulationExecutionAuthorizationResult(
            identity=request.result_identity,
            request=request,
            kind=kind,
            authorized_grant_state=state
            if variant in ("preparation", "claim")
            else None,
            diagnostics=()
            if variant in ("preparation", "claim")
            else (f"synthetic {variant}",),
            authorizer_implementation_identity="synthetic-authorizer:1",
        )
        return replace(
            genesis, authority_references=(reference,), authorization_results=(result,)
        )

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("preparation", id="authorized_unused_preparation"),
            pytest.param("claim", id="authorized_reserved_claim"),
            pytest.param("denied", id="denied_revoked_grant"),
            pytest.param("error", id="error_claimed_grant"),
        ],
    )
    def test_method__serialize__matches_authority_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot, variant: AuthorityVariant
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-AUTHORITY-001

        Requirement: Every supplied authority field and UTC microsecond is serialized.

        Method: Serialize independent constructor graphs for four closed variants.

        Oracle: Fixed literal wires authored without the production codec.

        Acceptance: Entire canonical payload equals the selected independent literal.

        Interpretation: UTC extrema, leap-day values and ordered scopes are not lost.

        Limitations: These records are not authenticated or replayed grants.
        """
        result = SUT(result_codec=QuantityOfInterestResultValueSerializer()).serialize(
            self.make_run(genesis_snapshot.run, variant), genesis_snapshot.binding
        )
        assert result.status == "encoded", result.failure
        assert result.encoded is not None
        assert result.encoded.payload == self.wire(variant)

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("preparation", id="authorized_unused_preparation"),
            pytest.param("claim", id="authorized_reserved_claim"),
            pytest.param("denied", id="denied_revoked_grant"),
            pytest.param("error", id="error_claimed_grant"),
        ],
    )
    def test_method__deserialize__restores_authority_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot, variant: AuthorityVariant
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-AUTHORITY-002

        Requirement: Decoding retains supplied authority and exact UTC instants.

        Method: Decode the fixed literal and compare separately constructed records.

        Oracle: Independent full graph with seven distinct timestamp fields.

        Acceptance: Complete run and commit binding agree exactly.

        Interpretation: Reconstructed diagnostics and state remain supplied evidence.

        Limitations: No authorizer, authority source or clock is consulted.
        """
        result = SUT(
            result_codec=QuantityOfInterestResultValueSerializer()
        ).deserialize(self.wire(variant))
        assert result.status == "decoded", result.failure
        assert result.run == self.make_run(genesis_snapshot.run, variant)
        assert result.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        ("field", "kind", "wire_value"),
        [
            pytest.param(
                "content_verification",
                w.ScientificExecutionAuthorityVerificationKind.FAILED,
                b"failed",
                id="content_failed",
            ),
            pytest.param(
                "content_verification",
                w.ScientificExecutionAuthorityVerificationKind.INDETERMINATE,
                b"indeterminate",
                id="content_indeterminate",
            ),
            pytest.param(
                "authentication_verification",
                w.ScientificExecutionAuthorityVerificationKind.FAILED,
                b"failed",
                id="authentication_failed",
            ),
            pytest.param(
                "authentication_verification",
                w.ScientificExecutionAuthorityVerificationKind.INDETERMINATE,
                b"indeterminate",
                id="authentication_indeterminate",
            ),
            pytest.param(
                "predecessor_closure",
                w.ScientificExecutionAuthorityVerificationKind.FAILED,
                b"failed",
                id="predecessor_closure_failed",
            ),
            pytest.param(
                "predecessor_closure",
                w.ScientificExecutionAuthorityVerificationKind.INDETERMINATE,
                b"indeterminate",
                id="predecessor_closure_indeterminate",
            ),
            pytest.param(
                "revocation_closure",
                w.ScientificExecutionAuthorityVerificationKind.FAILED,
                b"failed",
                id="revocation_closure_failed",
            ),
            pytest.param(
                "revocation_closure",
                w.ScientificExecutionAuthorityVerificationKind.INDETERMINATE,
                b"indeterminate",
                id="revocation_closure_indeterminate",
            ),
        ],
    )
    def test_method__codec__preserves_each_snapshot_check(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        field: VerificationField,
        kind: w.ScientificExecutionAuthorityVerificationKind,
        wire_value: bytes,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-AUTHORITY-003

        Requirement: The four distinct verification outcomes remain independent fields.

        Method: Change one literal check and its matching public-constructor field.

        Oracle: Explicit field names and independently specified enum-to-wire pairs.

        Acceptance: Encoded bytes and entire reconstructed graph match exactly.

        Interpretation: Serialization does not replace supplied authorization by
        reevaluating inconsistent synthetic verification evidence.

        Limitations: This deliberately does not establish replay equality or authority.
        """
        run = self.make_run(genesis_snapshot.run, "preparation")
        result = run.authorization_results[0]
        snapshot = result.request.snapshot
        snapshot = replace(
            snapshot,
            content_verification=(
                kind
                if field == "content_verification"
                else snapshot.content_verification
            ),
            authentication_verification=(
                kind
                if field == "authentication_verification"
                else snapshot.authentication_verification
            ),
            predecessor_closure=(
                kind if field == "predecessor_closure" else snapshot.predecessor_closure
            ),
            revocation_closure=(
                kind if field == "revocation_closure" else snapshot.revocation_closure
            ),
        )
        run = replace(
            run,
            authorization_results=(
                replace(result, request=replace(result.request, snapshot=snapshot)),
            ),
        )
        prefix = b'"' + field.encode() + b'":{"fields":{"value":"'
        wire = self.wire().replace(prefix + b'verified"', prefix + wire_value + b'"')
        serializer = SUT(result_codec=QuantityOfInterestResultValueSerializer())
        encoded = serializer.serialize(run, genesis_snapshot.binding)
        assert encoded.status == "encoded", encoded.failure
        assert encoded.encoded is not None and encoded.encoded.payload == wire
        decoded = serializer.deserialize(wire)
        assert decoded.status == "decoded", decoded.failure
        assert decoded.run == run and decoded.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        "replacement",
        [
            pytest.param(b"2024-02-29T12:34:56.123456", id="naive_timestamp"),
            pytest.param(b"2024-02-29T12:34:56.123456Z", id="noncanonical_z_suffix"),
            pytest.param(b"2024-02-29T12:34:56.123456+01:00", id="nonzero_offset"),
            pytest.param(b"2024-02-29T12:34:56.12345+00:00", id="short_fraction"),
            pytest.param(b"2024-02-29T12:34:56.1234560+00:00", id="excess_fraction"),
            pytest.param(b"2024-02-29 12:34:56.123456+00:00", id="space_separator"),
            pytest.param(b"2023-02-29T12:34:56.123456+00:00", id="invalid_leap_day"),
            pytest.param(
                b"2024-02-29T12:34:60.123456+00:00", id="unsupported_leap_second"
            ),
        ],
    )
    def test_method__deserialize__rejects_noncanonical_utc(
        self, replacement: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-AUTHORITY-004

        Requirement: Known datetime tags require exact valid UTC microsecond spelling.

        Method: Replace the unique verification instant in the independent literal.

        Oracle: Version-one wire requires ISO T, six fractional digits and +00:00,
        with a calendar date representable by the owning Python datetime contract.

        Acceptance: Corrupt failure with no reconstructed run or binding.

        Interpretation: Equivalent instants in alternate spellings are not canonical.

        Limitations: No external clock, leap-second model or timing policy is tested.
        """
        wire = self.wire().replace(b"2024-02-29T12:34:56.123456+00:00", replacement)
        result = SUT(
            result_codec=QuantityOfInterestResultValueSerializer()
        ).deserialize(wire)
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None

    @pytest.mark.parametrize(
        ("original", "replacement"),
        [
            pytest.param(
                b"2024-02-29T12:34:56.654321+00:00",
                b"2024-02-29T12:34:56.123455+00:00",
                id="freshness_before_verification",
            ),
            pytest.param(
                b"2024-02-29T13:34:56.999999+00:00",
                b"2024-02-29T12:34:56.000000+00:00",
                id="grant_interval_reversed",
            ),
            pytest.param(
                b'"authorized_grant_state":{"fields":{"value":"unused"},"type":"ScientificExecutionGrantState"}',
                b'"authorized_grant_state":null',
                id="authorized_state_missing",
            ),
            pytest.param(
                b'"identity":{"fields":{"value":"authorization"},"type":"SimulationExecutionAuthorizationResultIdentity"}',
                b'"identity":{"fields":{"value":"detached"},"type":"SimulationExecutionAuthorizationResultIdentity"}',
                id="result_identity_detached_from_request",
            ),
        ],
    )
    def test_method__deserialize__rejects_authority_invariant_drift(
        self, original: bytes, replacement: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-AUTHORITY-005

        Requirement: Canonically spelled but intrinsically invalid authority is corrupt.

        Method: Mutate one interval, result discriminator or identity in the literal.

        Oracle: Public bounds, authorized-state closure and request/result identity.

        Acceptance: Failure is corrupt and exposes no partial run or binding.

        Interpretation: Canonical bytes alone do not establish valid records.

        Limitations: No authority authentication or cross-history closure is claimed.
        """
        assert original in self.wire()
        result = SUT(
            result_codec=QuantityOfInterestResultValueSerializer()
        ).deserialize(self.wire().replace(original, replacement))
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None
