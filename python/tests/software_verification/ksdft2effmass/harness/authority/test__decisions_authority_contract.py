r"""Software verification of the decisions and authority version-1 artifact.

Evidence profile: routine

Bounded artifact scope: the immutable DevelopmentDecision wire, legacy adaptation,
Task signature requirement, and operation-authorization agreement.

Facet and represented meaning

The artifact is the accepted immutable decision and default-unsigned authority API.

Intrinsic and cross-object scope

The architecture contract and fixed legacy fixture are independent exact oracles.
Tests cover canonical round trips, lossless mapping, immutable tuples, configured-Task
binding, and authorization-result binding.

VVUQ and scientific exclusions

This is software verification only. It grants no authority and establishes no
scientific validation, protected execution permission, or human acceptance.
"""

from __future__ import annotations

import base64
import dataclasses
import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from ksdft2effmass.harness import (
    DevelopmentAuthorityContext,
    DevelopmentAuthorityContextResolutionResult,
    DevelopmentAuthorityContextResolver,
    DevelopmentAuthorityDiagnostic,
    DevelopmentAuthorityLedgerSnapshot,
    DevelopmentAuthorityPolicy,
    DevelopmentAuthorityReconstructionReceipt,
    DevelopmentAuthorityResolutionSerializer,
    DevelopmentAuthoritySnapshotSource,
    DevelopmentAuthorizationRevocation,
    DevelopmentAuthorizationUse,
    DevelopmentDecisionSerializer,
    DevelopmentEligibilityReference,
    DevelopmentIssuerAnchorBinding,
    DevelopmentOperationAuthorizationInput,
    DevelopmentOperationAuthorizationSerializer,
    DevelopmentOperationAuthorizer,
    DevelopmentReviewAuthorization,
    DevelopmentReviewOperationBinding,
    DevelopmentSignatureEntry,
    DevelopmentSignedAuthoritySnapshot,
    DevelopmentSignedAuthoritySnapshotSerializer,
    DevelopmentTaskAuthorization,
    DevelopmentTaskOperationBinding,
    DevelopmentTaskSignatureConfiguration,
    DevelopmentTaskSignatureConfigurationSerializer,
    DevelopmentTaskSignatureRequirementResolver,
    DevelopmentTrustAnchor,
    DevelopmentTrustConfiguration,
    DevelopmentTrustConfigurationPin,
)

pytestmark = pytest.mark.software_verification


def framed_identity(domain: str, body: dict[str, object]) -> str:
    """Independently derive one expected framed identity for test setup.

    Evidence ID: Owns no identifier; supports the module's evidence owners.

    Requirement: Encode the accepted sorted compact framed SHA-256 formula without
    calling the production identity helper.

    Acceptance: Return the independently computed lowercase digest.
    """

    def normalize(value: object) -> object:
        if dataclasses.is_dataclass(value) and not isinstance(value, type):
            return normalize(dataclasses.asdict(value))
        if type(value) is dict:
            return {key: normalize(item) for key, item in value.items()}
        if type(value) in {tuple, list}:
            return [normalize(item) for item in value]
        if type(value) is bytes:
            return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")
        return value

    encoded = (
        json.dumps(normalize(body), sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    framed = domain.encode() + b"\x00v1\x00" + len(encoded).to_bytes(8, "big") + encoded
    return hashlib.sha256(framed).hexdigest()


def test_artifact__legacy_adaptation__preserves_exact_fields_and_bytes() -> None:
    """Legacy adaptation preserves every field and exact-byte provenance.

    Evidence ID: SV-AUTH-001

    Requirement: The one-way adapter copies the complete legacy checkpoint shape.

    Oracle: Fixed legacy fixture and SHA-256 exact-byte identity contract.

    Acceptance: Every formerly dropped field, array order, response, and scope agrees.
    """
    payload = Path(
        "../harness/fixtures/authority-v1/legacy-checkpoint-resolved.json"
    ).read_bytes()
    serializer = DevelopmentDecisionSerializer()
    decision = serializer.adapt_legacy(
        payload, decision_id="decision.one", source_path=".pi/checkpoints/legacy.json"
    )
    assert decision.recommendation == "A"
    assert decision.blocked_scope == "blocked"
    assert decision.safe_scope == "safe"
    assert decision.declared_authoritative_paths == ("AGENTS.md",)
    assert decision.declared_scope == "bounded historical scope"
    assert decision.authority_identity_status == "unavailable_legacy"
    assert decision.selected_option_id is None
    encoded = serializer.execute(decision)
    assert serializer.deserialize(encoded) == decision
    schema = json.loads(
        Path(
            "../harness/schemas/authority-v1/development-decision.schema.json"
        ).read_text()
    )
    Draft202012Validator(schema).validate(json.loads(encoded))
    with pytest.raises(dataclasses.FrozenInstanceError):
        decision.state = "unresolved"  # type: ignore[misc]
    directory_source = Path(
        "../.pi/checkpoints/H2-HC02-final-acceptance.json"
    ).read_bytes()
    directory_decision = serializer.adapt_legacy(
        directory_source,
        decision_id="decision.directory-declaration",
        source_path=".pi/checkpoints/H2-HC02-final-acceptance.json",
    )
    assert "python/src/ksdft2effmass/harness/pi/" in (
        directory_decision.declared_authoritative_paths
    )


def test_artifact__signature_requirement__defaults_unsigned_with_exact_revision() -> (
    None
):
    """Absent configuration resolves unsigned without weakening exact binding.

    Evidence ID: SV-AUTH-002

    Requirement: The absent per-Task setting is not_required at one composition ID.

    Oracle: Accepted framed SHA-256 configured-Task composition formula.

    Acceptance: Resolver returns resolved/default/not_required and exact identity.
    """
    task_record = "a" * 64
    body = {
        "schema_version": 1,
        "task_record_identity": task_record,
        "signature_configuration_identity": None,
        "signature_requirement": "not_required",
    }
    revision = framed_identity(
        "ksdft2effmass-development-configured-task-revision", body
    )
    result = DevelopmentTaskSignatureRequirementResolver().execute(
        task_id="task.one",
        task_record_identity=task_record,
        expected_task_revision=revision,
    )
    assert (result.status, result.source, result.signature_requirement) == (
        "resolved",
        "default",
        "not_required",
    )
    serializer = DevelopmentTaskSignatureConfigurationSerializer()
    encoded = serializer.execute(result)
    assert serializer.deserialize_result(encoded) == result
    schema = json.loads(
        Path(
            "../harness/schemas/authority-v1/task-signature-configuration.schema.json"
        ).read_text()
    )
    Draft202012Validator(schema).validate(json.loads(encoded))


def test_artifact__authorization__binds_unsigned_result_to_exact_operation() -> None:
    """Unsigned result is bound and claims no signed authority.

    Evidence ID: SV-AUTH-003

    Requirement: signature_not_required binds one exact requirement result/input.

    Oracle: Accepted closed authorization-result field contract.

    Acceptance: No context or authorization identity is emitted; mismatch errors.
    """
    task_record = "a" * 64
    revision = framed_identity(
        "ksdft2effmass-development-configured-task-revision",
        {
            "schema_version": 1,
            "task_record_identity": task_record,
            "signature_configuration_identity": None,
            "signature_requirement": "not_required",
        },
    )
    requirement = DevelopmentTaskSignatureRequirementResolver().execute(
        task_id="task.one",
        task_record_identity=task_record,
        expected_task_revision=revision,
    )
    binding = DevelopmentTaskOperationBinding(
        "task",
        requirement.result_identity,
        "repo",
        "source",
        "state",
        "selection",
        "task.one",
        revision,
        "start",
        "candidate",
        "operation",
        "attempt",
        "idempotency",
        "implementation",
        ("python/src/file.py",),
        ("req.one",),
        "architecture",
        "validator",
    )
    input_body = {
        "schema_version": 1,
        "input_identity": None,
        "operation_binding": binding,
    }
    input_body["input_identity"] = framed_identity(
        "ksdft2effmass-development-operation-authorization-input", input_body
    )
    operation = DevelopmentOperationAuthorizationInput(**input_body)
    result = DevelopmentOperationAuthorizer().execute(operation, requirement)
    assert result.status == "signature_not_required"
    assert result.context_identity is None
    assert result.authorization_id is None
    serializer = DevelopmentOperationAuthorizationSerializer()
    assert serializer.deserialize_input(serializer.execute(operation)) == operation
    encoded_result = serializer.execute(result)
    assert serializer.deserialize_result(encoded_result) == result
    schema = json.loads(
        Path(
            "../harness/schemas/authority-v1/operation-authorization.schema.json"
        ).read_text()
    )
    Draft202012Validator(schema).validate(json.loads(encoded_result))
    with pytest.raises(TypeError, match="operation authorization-family"):
        serializer.execute(requirement)


def test_artifact__authorization__rejects_forged_identity_and_task_binding() -> None:
    """Unsigned authorization rejects forged identities and a different Task binding.

    Evidence ID: SV-AUTH-004

    Requirement: The authorizer independently validates input and requirement
    identities and binds the exact Task ID and configured revision.

    Oracle: Accepted framed identities and exact Task-binding equality contract.

    Acceptance: Forged input identity and reidentified different-Task requirement both
    produce error without an authorization identity.
    """
    task_record = "a" * 64
    revision = framed_identity(
        "ksdft2effmass-development-configured-task-revision",
        {
            "schema_version": 1,
            "task_record_identity": task_record,
            "signature_configuration_identity": None,
            "signature_requirement": "not_required",
        },
    )
    requirement = DevelopmentTaskSignatureRequirementResolver().execute(
        task_id="task.one",
        task_record_identity=task_record,
        expected_task_revision=revision,
    )
    binding = DevelopmentTaskOperationBinding(
        "task",
        requirement.result_identity,
        "repo",
        "source",
        "state",
        "selection",
        "task.one",
        revision,
        "start",
        "candidate",
        "operation",
        "attempt",
        "idempotency",
        "implementation",
        ("python/src/file.py",),
        ("req.one",),
        "architecture",
        "validator",
    )
    input_body: dict[str, object] = {
        "schema_version": 1,
        "input_identity": None,
        "operation_binding": binding,
    }
    input_body["input_identity"] = framed_identity(
        "ksdft2effmass-development-operation-authorization-input", input_body
    )
    operation = DevelopmentOperationAuthorizationInput(**input_body)  # type: ignore[arg-type]
    forged_input = dataclasses.replace(operation, input_identity="0" * 64)
    assert (
        DevelopmentOperationAuthorizer().execute(forged_input, requirement).status
        == "error"
    )

    other_body = dataclasses.asdict(requirement)
    other_body["task_id"] = "task.two"
    other_body["result_identity"] = None
    other_body["result_identity"] = framed_identity(
        "ksdft2effmass-development-task-signature-requirement-result", other_body
    )
    other_requirement = dataclasses.replace(
        requirement,
        task_id="task.two",
        result_identity=other_body["result_identity"],  # type: ignore[arg-type]
    )
    assert (
        DevelopmentOperationAuthorizer().execute(operation, other_requirement).status
        == "error"
    )


def test_artifact__signed_ledger__head_only_keys_must_meet_threshold() -> None:
    """Ancestor signatures cannot satisfy the accepted head's issuer threshold.

    Evidence ID: SV-AUTH-005

    Requirement: Threshold and issuer checks use only keys verified on the head
    envelope while independently authenticating every ancestor envelope.

    Oracle: Two-key threshold with one distinct valid signer on each of two envelopes.

    Acceptance: Signature verification passes but head threshold verification fails.
    """
    ed25519 = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.ed25519")
    serialization = pytest.importorskip("cryptography.hazmat.primitives.serialization")
    private_keys = (
        ed25519.Ed25519PrivateKey.generate(),
        ed25519.Ed25519PrivateKey.generate(),
    )
    public_bytes = (
        private_keys[0]
        .public_key()
        .public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw),
        private_keys[1]
        .public_key()
        .public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw),
    )
    key_ids = (
        hashlib.sha256(
            b"ksdft2effmass-development-authority-key\x00v1\x00" + public_bytes[0]
        ).hexdigest(),
        hashlib.sha256(
            b"ksdft2effmass-development-authority-key\x00v1\x00" + public_bytes[1]
        ).hexdigest(),
    )
    anchors = (
        DevelopmentTrustAnchor(
            1,
            "anchor.0",
            key_ids[0],
            "ed25519",
            "raw-base64url",
            public_bytes[0],
            "issuer.one",
            "enabled",
        ),
        DevelopmentTrustAnchor(
            1,
            "anchor.1",
            key_ids[1],
            "ed25519",
            "raw-base64url",
            public_bytes[1],
            "issuer.one",
            "enabled",
        ),
    )
    policy = DevelopmentAuthorityPolicy(
        1,
        "record.policy",
        "0" * 64,
        0,
        None,
        "authority_policy",
        "issuer.one",
        None,
        0,
        "policy.document",
    )
    policy_body = dataclasses.asdict(policy)
    policy_body["record_content_identity"] = None
    policy = dataclasses.replace(
        policy,
        record_content_identity=framed_identity(
            "ksdft2effmass-development-authority-record", policy_body
        ),
    )
    snapshots = (
        DevelopmentAuthorityLedgerSnapshot(
            1, "ledger.one", 0, None, 0, 0, policy.record_content_identity, (policy,)
        ),
        DevelopmentAuthorityLedgerSnapshot(
            1,
            "ledger.one",
            1,
            "0" * 64,
            0,
            0,
            policy.record_content_identity,
            (policy,),
        ),
    )
    snapshots = (
        snapshots[0],
        dataclasses.replace(
            snapshots[1], predecessor_payload_identity=snapshots[0].payload_identity
        ),
    )
    serializer = DevelopmentSignedAuthoritySnapshotSerializer()
    payloads = (serializer.execute(snapshots[0]), serializer.execute(snapshots[1]))
    preimages = (
        b"ksdft2effmass-development-authority-snapshot\x00v1\x00"
        + len(payloads[0]).to_bytes(8, "big")
        + payloads[0],
        b"ksdft2effmass-development-authority-snapshot\x00v1\x00"
        + len(payloads[1]).to_bytes(8, "big")
        + payloads[1],
    )
    envelopes = (
        DevelopmentSignedAuthoritySnapshot(
            1,
            "harness-canonical-json-v1",
            "base64url-no-padding",
            payloads[0],
            (
                DevelopmentSignatureEntry(
                    "ed25519",
                    key_ids[0],
                    "raw-base64url",
                    private_keys[0].sign(preimages[0]),
                ),
            ),
        ),
        DevelopmentSignedAuthoritySnapshot(
            1,
            "harness-canonical-json-v1",
            "base64url-no-padding",
            payloads[1],
            (
                DevelopmentSignatureEntry(
                    "ed25519",
                    key_ids[1],
                    "raw-base64url",
                    private_keys[1].sign(preimages[1]),
                ),
            ),
        ),
    )
    head_identity = envelopes[-1].artifact_identity
    binding = DevelopmentIssuerAnchorBinding(
        "issuer.one", ("authority_policy",), ("anchor.0", "anchor.1"), 2
    )
    configuration = DevelopmentTrustConfiguration(
        1,
        "0" * 64,
        0,
        None,
        "trust.one",
        1,
        1,
        "harness-canonical-json-v1",
        ("local",),
        head_identity,
        snapshots[0].payload_identity,
        0,
        anchors,
        (binding,),
        "resolver.policy",
    )
    configuration_body = dataclasses.asdict(configuration)
    configuration_body["configuration_identity"] = None
    configuration = dataclasses.replace(
        configuration,
        configuration_identity=framed_identity(
            "ksdft2effmass-development-trust-configuration", configuration_body
        ),
    )
    pin = DevelopmentTrustConfigurationPin(
        1,
        "0" * 64,
        configuration.configuration_identity,
        0,
        "source.authority",
        "authentication.receipt",
    )
    pin_body = dataclasses.asdict(pin)
    pin_body["pin_identity"] = None
    pin = dataclasses.replace(
        pin,
        pin_identity=framed_identity(
            "ksdft2effmass-development-trust-configuration-pin", pin_body
        ),
    )
    source = DevelopmentAuthoritySnapshotSource(
        1, "0" * 64, "local", "source.reference", head_identity, 2, 1_000_000
    )
    source_body = dataclasses.asdict(source)
    source_body["source_descriptor_identity"] = None
    source = dataclasses.replace(
        source,
        source_descriptor_identity=framed_identity(
            "ksdft2effmass-development-authority-source", source_body
        ),
    )
    trust_schema = json.loads(
        Path(
            "../harness/schemas/authority-v1/trust-configuration.schema.json"
        ).read_text()
    )
    signed_schema = json.loads(
        Path(
            "../harness/schemas/authority-v1/signed-authority-snapshot.schema.json"
        ).read_text()
    )
    Draft202012Validator(trust_schema).validate(
        json.loads(serializer.execute(configuration))
    )
    Draft202012Validator(trust_schema).validate(json.loads(serializer.execute(source)))
    Draft202012Validator(signed_schema).validate(
        json.loads(serializer.execute(snapshots[-1]))
    )
    Draft202012Validator(signed_schema).validate(
        json.loads(serializer.execute(envelopes[-1]))
    )
    result = DevelopmentAuthorityContextResolver().execute(
        pin,
        configuration,
        source,
        (serializer.execute(envelopes[0]), serializer.execute(envelopes[1])),
    )
    assert result.status == "failed"
    assert result.receipt.signature_status == "passed"
    assert result.receipt.threshold_status == "failed"
    assert result.receipt.verified_key_ids == (key_ids[1],)


def test_artifact__signed_ledger__rejects_nonclosing_policy_reference() -> None:
    """Ledger reconstruction rejects a record governed by no earlier policy.

    Evidence ID: SV-AUTH-006

    Requirement: Complete ledger closure requires genesis policy and every later
    governing-policy reference to resolve to an earlier policy.

    Oracle: A validly signed one-snapshot ledger with one dangling policy reference.

    Acceptance: Cryptographic and record-chain checks pass; reference closure fails.
    """
    ed25519 = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.ed25519")
    serialization = pytest.importorskip("cryptography.hazmat.primitives.serialization")
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_bytes = private_key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    key_id = hashlib.sha256(
        b"ksdft2effmass-development-authority-key\x00v1\x00" + public_bytes
    ).hexdigest()
    anchor = DevelopmentTrustAnchor(
        1,
        "anchor.one",
        key_id,
        "ed25519",
        "raw-base64url",
        public_bytes,
        "issuer.one",
        "enabled",
    )
    policy = DevelopmentAuthorityPolicy(
        1,
        "record.policy",
        "0" * 64,
        0,
        None,
        "authority_policy",
        "issuer.one",
        None,
        0,
        "policy.document",
    )
    policy_body = dataclasses.asdict(policy)
    policy_body["record_content_identity"] = None
    policy = dataclasses.replace(
        policy,
        record_content_identity=framed_identity(
            "ksdft2effmass-development-authority-record", policy_body
        ),
    )
    reference = DevelopmentEligibilityReference(
        1,
        "record.reference",
        "0" * 64,
        1,
        policy.record_content_identity,
        "eligibility_reference",
        "issuer.one",
        "f" * 64,
        "eligibility.result",
        "subject.one",
    )
    reference_body = dataclasses.asdict(reference)
    reference_body["record_content_identity"] = None
    reference = dataclasses.replace(
        reference,
        record_content_identity=framed_identity(
            "ksdft2effmass-development-authority-record", reference_body
        ),
    )
    snapshot = DevelopmentAuthorityLedgerSnapshot(
        1,
        "ledger.one",
        0,
        None,
        0,
        1,
        policy.record_content_identity,
        (policy, reference),
    )
    serializer = DevelopmentSignedAuthoritySnapshotSerializer()
    payload = serializer.execute(snapshot)
    preimage = (
        b"ksdft2effmass-development-authority-snapshot\x00v1\x00"
        + len(payload).to_bytes(8, "big")
        + payload
    )
    envelope = DevelopmentSignedAuthoritySnapshot(
        1,
        "harness-canonical-json-v1",
        "base64url-no-padding",
        payload,
        (
            DevelopmentSignatureEntry(
                "ed25519", key_id, "raw-base64url", private_key.sign(preimage)
            ),
        ),
    )
    binding = DevelopmentIssuerAnchorBinding(
        "issuer.one", ("authority_policy", "eligibility_reference"), ("anchor.one",), 1
    )
    configuration = DevelopmentTrustConfiguration(
        1,
        "0" * 64,
        0,
        None,
        "trust.one",
        1,
        1,
        "harness-canonical-json-v1",
        ("local",),
        envelope.artifact_identity,
        snapshot.payload_identity,
        0,
        (anchor,),
        (binding,),
        "resolver.policy",
    )
    configuration_body = dataclasses.asdict(configuration)
    configuration_body["configuration_identity"] = None
    configuration = dataclasses.replace(
        configuration,
        configuration_identity=framed_identity(
            "ksdft2effmass-development-trust-configuration", configuration_body
        ),
    )
    pin = DevelopmentTrustConfigurationPin(
        1,
        "0" * 64,
        configuration.configuration_identity,
        0,
        "source.authority",
        "authentication.receipt",
    )
    pin_body = dataclasses.asdict(pin)
    pin_body["pin_identity"] = None
    pin = dataclasses.replace(
        pin,
        pin_identity=framed_identity(
            "ksdft2effmass-development-trust-configuration-pin", pin_body
        ),
    )
    source = DevelopmentAuthoritySnapshotSource(
        1,
        "0" * 64,
        "local",
        "source.reference",
        envelope.artifact_identity,
        1,
        1_000_000,
    )
    source_body = dataclasses.asdict(source)
    source_body["source_descriptor_identity"] = None
    source = dataclasses.replace(
        source,
        source_descriptor_identity=framed_identity(
            "ksdft2effmass-development-authority-source", source_body
        ),
    )
    result = DevelopmentAuthorityContextResolver().execute(
        pin, configuration, source, (serializer.execute(envelope),)
    )
    assert result.status == "failed"
    assert result.receipt.record_chain_status == "passed"
    assert result.receipt.reference_closure_status == "failed"


def test_artifact__resolution_serialization__round_trips_failed_result() -> None:
    """Resolution serializers preserve typed receipt and failed result wires.

    Evidence ID: SV-AUTH-007

    Requirement: Receipt and result deserialization reconstruct nested nominal types.

    Oracle: Exact canonical round trip and the closed failed-result runtime contract.

    Acceptance: Both public typed deserializers return values equal to their inputs.
    """
    diagnostic = DevelopmentAuthorityDiagnostic(
        "AUTH.SIGNATURE_CAPABILITY_UNAVAILABLE", None, "capability unavailable"
    )
    receipt = DevelopmentAuthorityReconstructionReceipt(
        1,
        "a" * 64,
        "b" * 64,
        "local",
        "c" * 64,
        "d" * 64,
        0,
        "e" * 64,
        None,
        None,
        None,
        0,
        "harness-canonical-json-v1",
        "resolver.v1",
        "passed",
        "passed",
        "passed",
        "failed",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        (),
        (diagnostic,),
    )
    result = DevelopmentAuthorityContextResolutionResult(1, "failed", receipt, None)
    serializer = DevelopmentAuthorityResolutionSerializer()
    assert serializer.deserialize_receipt(serializer.execute(receipt)) == receipt
    encoded_result = serializer.execute(result)
    assert serializer.deserialize_result(encoded_result) == result
    schema = json.loads(
        Path(
            "../harness/schemas/authority-v1/authority-resolution.schema.json"
        ).read_text()
    )
    Draft202012Validator(schema).validate(json.loads(encoded_result))
    with pytest.raises(TypeError, match="resolution-family"):
        serializer.execute(diagnostic)


@pytest.mark.parametrize(
    "schema_name",
    (
        pytest.param("development-decision.schema.json", id="development_decision"),
        pytest.param(
            "task-signature-configuration.schema.json",
            id="task_signature_configuration",
        ),
        pytest.param("trust-configuration.schema.json", id="trust_configuration"),
        pytest.param("signed-authority-snapshot.schema.json", id="signed_snapshot"),
        pytest.param("authority-resolution.schema.json", id="authority_resolution"),
        pytest.param(
            "operation-authorization.schema.json", id="operation_authorization"
        ),
    ),
)
def test_artifact__schema__is_strict_draft_2020_12(schema_name: str) -> None:
    """Every authority schema is valid Draft 2020-12 and rejects unknown keys.

    Evidence ID: SV-AUTH-008

    Requirement: Maintained schemas use valid Draft 2020-12 closed object variants.

    Oracle: The Draft 2020-12 metaschema and an object containing only an unknown key.

    Acceptance: Metaschema checking passes and the unknown object is rejected.
    """
    schema = json.loads(
        (Path("../harness/schemas/authority-v1") / schema_name).read_text()
    )
    Draft202012Validator.check_schema(schema)
    assert tuple(Draft202012Validator(schema).iter_errors({"unknown": 1}))


def identify_record(record: object) -> object:
    """Derive one exact record identity for focused ledger fixtures.

    Evidence ID: Owns no identifier; supports the module's evidence owners.

    Requirement: Apply the accepted independent authority-record identity formula.

    Acceptance: Return the same nominal record with its exact derived identity.
    """
    body = dataclasses.asdict(record)
    body["record_content_identity"] = None
    return dataclasses.replace(
        record,
        record_content_identity=framed_identity(
            "ksdft2effmass-development-authority-record", body
        ),
    )


def resolve_record_fixture(records: tuple[object, ...]) -> object:
    """Resolve one signed single-snapshot synthetic ledger fixture.

    Evidence ID: Owns no identifier; supports the module's evidence owners.

    Requirement: Supply exact public-key trust, source, envelope, and record inputs.

    Acceptance: Return the public resolver's closed result without altering it.
    """
    ed25519 = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.ed25519")
    serialization = pytest.importorskip("cryptography.hazmat.primitives.serialization")
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_bytes = private_key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    key_id = hashlib.sha256(
        b"ksdft2effmass-development-authority-key\x00v1\x00" + public_bytes
    ).hexdigest()
    anchor = DevelopmentTrustAnchor(
        1,
        "anchor.one",
        key_id,
        "ed25519",
        "raw-base64url",
        public_bytes,
        "issuer.one",
        "enabled",
    )
    typed_records = tuple(records)
    snapshot = DevelopmentAuthorityLedgerSnapshot(
        1,
        "ledger.one",
        0,
        None,
        0,
        len(typed_records) - 1,
        typed_records[0].record_content_identity,  # type: ignore[attr-defined]
        typed_records,  # type: ignore[arg-type]
    )
    serializer = DevelopmentSignedAuthoritySnapshotSerializer()
    payload = serializer.execute(snapshot)
    preimage = (
        b"ksdft2effmass-development-authority-snapshot\x00v1\x00"
        + len(payload).to_bytes(8, "big")
        + payload
    )
    envelope = DevelopmentSignedAuthoritySnapshot(
        1,
        "harness-canonical-json-v1",
        "base64url-no-padding",
        payload,
        (
            DevelopmentSignatureEntry(
                "ed25519", key_id, "raw-base64url", private_key.sign(preimage)
            ),
        ),
    )
    kinds = tuple(sorted({record.record_kind for record in typed_records}))  # type: ignore[attr-defined]
    binding = DevelopmentIssuerAnchorBinding("issuer.one", kinds, ("anchor.one",), 1)
    configuration = DevelopmentTrustConfiguration(
        1,
        "0" * 64,
        0,
        None,
        "trust.one",
        1,
        1,
        "harness-canonical-json-v1",
        ("local",),
        envelope.artifact_identity,
        snapshot.payload_identity,
        0,
        (anchor,),
        (binding,),
        "resolver.policy",
    )
    configuration = dataclasses.replace(
        configuration,
        configuration_identity=framed_identity(
            "ksdft2effmass-development-trust-configuration",
            {**dataclasses.asdict(configuration), "configuration_identity": None},
        ),
    )
    pin = DevelopmentTrustConfigurationPin(
        1,
        "0" * 64,
        configuration.configuration_identity,
        0,
        "source.authority",
        "authentication.receipt",
    )
    pin = dataclasses.replace(
        pin,
        pin_identity=framed_identity(
            "ksdft2effmass-development-trust-configuration-pin",
            {**dataclasses.asdict(pin), "pin_identity": None},
        ),
    )
    source = DevelopmentAuthoritySnapshotSource(
        1,
        "0" * 64,
        "local",
        "source.reference",
        envelope.artifact_identity,
        1,
        1_000_000,
    )
    source = dataclasses.replace(
        source,
        source_descriptor_identity=framed_identity(
            "ksdft2effmass-development-authority-source",
            {**dataclasses.asdict(source), "source_descriptor_identity": None},
        ),
    )
    return DevelopmentAuthorityContextResolver().execute(
        pin, configuration, source, (serializer.execute(envelope),)
    )


def make_closure_records(case: str) -> tuple[object, ...]:
    """Construct one semantic ledger-closure partition.

    Evidence ID: Owns no identifier; supports the module's evidence owners.

    Requirement: Vary only record/reference facts relevant to the named partition.

    Acceptance: Return a complete ordered record tuple with exact chain identities.
    """
    policy = identify_record(
        DevelopmentAuthorityPolicy(
            1,
            "record.policy",
            "0" * 64,
            0,
            None,
            "authority_policy",
            "issuer.one",
            None,
            0,
            "policy.document",
        )
    )
    binding = DevelopmentTaskOperationBinding(
        "task",
        "a" * 64,
        "repo",
        "source",
        "state",
        "selection",
        "task.one",
        "revision",
        "start",
        "candidate",
        "operation",
        "attempt",
        "idempotency",
        "implementation",
        ("python/src/file.py",),
        ("req.one",),
        "architecture",
        "validator",
    )
    auth = identify_record(
        DevelopmentTaskAuthorization(
            1,
            "record.auth",
            "0" * 64,
            1,
            policy.record_content_identity,  # type: ignore[attr-defined]
            "task_authorization",
            "issuer.one",
            policy.record_content_identity,  # type: ignore[attr-defined]
            "authorization.one",
            binding,
            1,
        )
    )
    records: list[object] = [policy, auth]
    if case == "duplicate_record_id":
        records[1] = identify_record(
            dataclasses.replace(auth, record_id="record.policy")
        )
    elif case == "duplicate_authorization_id":
        second = DevelopmentTaskAuthorization(
            1,
            "record.auth.two",
            "0" * 64,
            2,
            auth.record_content_identity,  # type: ignore[attr-defined]
            "task_authorization",
            "issuer.one",
            policy.record_content_identity,  # type: ignore[attr-defined]
            "authorization.one",
            binding,
            1,
        )
        records.append(identify_record(second))
    elif case in {"valid_use", "mismatched_use", "repeated_use"}:
        attempt = "other" if case == "mismatched_use" else "attempt"
        use = identify_record(
            DevelopmentAuthorizationUse(
                1,
                "record.use",
                "0" * 64,
                2,
                auth.record_content_identity,  # type: ignore[attr-defined]
                "authorization_use",
                "issuer.one",
                policy.record_content_identity,  # type: ignore[attr-defined]
                "authorization.one",
                "operation",
                attempt,
                "idempotency",
                "receipt.one",
            )
        )
        records.append(use)
        if case == "repeated_use":
            records.append(
                identify_record(
                    dataclasses.replace(
                        use,
                        record_id="record.use.two",
                        record_ordinal=3,
                        previous_record_content_identity=use.record_content_identity,
                        operation_receipt_identity="receipt.two",
                    )
                )
            )
    elif case in {
        "unknown_revocation",
        "late_replacement",
        "same_kind_replacement",
        "different_kind_replacement",
    }:
        replacement_id: str | None = None
        if case in {"same_kind_replacement", "different_kind_replacement"}:
            if case == "same_kind_replacement":
                replacement: object = DevelopmentTaskAuthorization(
                    1,
                    "record.replacement",
                    "0" * 64,
                    2,
                    auth.record_content_identity,  # type: ignore[attr-defined]
                    "task_authorization",
                    "issuer.one",
                    policy.record_content_identity,  # type: ignore[attr-defined]
                    "authorization.two",
                    binding,
                    1,
                )
            else:
                review_binding = DevelopmentReviewOperationBinding(
                    "review",
                    "a" * 64,
                    "repo",
                    "source",
                    "state",
                    "selection",
                    "task.one",
                    "revision",
                    "start",
                    "candidate",
                    "review.operation",
                    "review.attempt",
                    "review.idempotency",
                    "review",
                    (),
                    (),
                    "architecture",
                    "validator",
                    "subject",
                    "review.result",
                )
                replacement = DevelopmentReviewAuthorization(
                    1,
                    "record.replacement",
                    "0" * 64,
                    2,
                    auth.record_content_identity,  # type: ignore[attr-defined]
                    "review_authorization",
                    "issuer.one",
                    policy.record_content_identity,  # type: ignore[attr-defined]
                    "authorization.two",
                    review_binding,
                    1,
                )
            replacement = identify_record(replacement)
            records.append(replacement)
            replacement_id = "record.replacement"
        elif case == "late_replacement":
            replacement_id = "record.future"
        previous = records[-1].record_content_identity  # type: ignore[attr-defined]
        records.append(
            identify_record(
                DevelopmentAuthorizationRevocation(
                    1,
                    "record.revocation",
                    "0" * 64,
                    len(records),
                    previous,
                    "revocation",
                    "issuer.one",
                    policy.record_content_identity,  # type: ignore[attr-defined]
                    "record.unknown" if case == "unknown_revocation" else "record.auth",
                    "reason",
                    replacement_id,
                )
            )
        )
    return tuple(records)


@pytest.mark.parametrize(
    ("case", "expected_status"),
    (
        pytest.param("complete", "resolved", id="complete_closure"),
        pytest.param("valid_use", "resolved", id="valid_correlated_use"),
        pytest.param("duplicate_record_id", "failed", id="duplicate_record_id"),
        pytest.param(
            "duplicate_authorization_id", "failed", id="duplicate_authorization_id"
        ),
        pytest.param("mismatched_use", "failed", id="mismatched_use_correlation"),
        pytest.param("repeated_use", "failed", id="repeated_use"),
        pytest.param("unknown_revocation", "failed", id="unknown_revocation_target"),
        pytest.param("late_replacement", "failed", id="replacement_not_earlier"),
        pytest.param("same_kind_replacement", "resolved", id="same_kind_replacement"),
        pytest.param(
            "different_kind_replacement", "failed", id="different_kind_replacement"
        ),
    ),
)
def test_artifact__ledger_closure__enforces_reference_matrix(
    case: str, expected_status: str
) -> None:
    """Ledger closure enforces identity, use, and revocation relationships.

    Evidence ID: SV-AUTH-009

    Requirement: Complete closure accepts exact records and rejects duplicate IDs,
    mismatched/repeated uses, and unresolved or later revocation references.

    Oracle: The accepted ordered append-only closure rules for each semantic partition.

    Acceptance: Each partition returns the exact resolved or failed closed status.
    """
    result = resolve_record_fixture(make_closure_records(case))
    assert result.status == expected_status


def test_artifact__authorization__rejects_reidentified_record_forgery() -> None:
    """Signed authorization rejects a coherently reidentified record forgery.

    Evidence ID: SV-AUTH-010

    Requirement: Signed mode binds context records to the canonical head-snapshot
    payload identity authenticated by the reconstruction receipt.

    Oracle: A successful resolver result followed by changed records with recomputed
    record-head and context identities but the unchanged verified receipt.

    Acceptance: The authentic result is usable while the coherent forgery returns
    error because it cannot change the receipt's verified head-payload identity.
    """
    task_record = "b" * 64
    configuration = DevelopmentTaskSignatureConfiguration(
        1, "0" * 64, "task.one", task_record, "required"
    )
    configuration = dataclasses.replace(
        configuration,
        configuration_identity=framed_identity(
            "ksdft2effmass-development-task-signature-configuration",
            {**dataclasses.asdict(configuration), "configuration_identity": None},
        ),
    )
    revision = framed_identity(
        "ksdft2effmass-development-configured-task-revision",
        {
            "schema_version": 1,
            "task_record_identity": task_record,
            "signature_configuration_identity": configuration.configuration_identity,
            "signature_requirement": "required",
        },
    )
    requirement = DevelopmentTaskSignatureRequirementResolver().execute(
        task_id="task.one",
        task_record_identity=task_record,
        expected_task_revision=revision,
        configuration=configuration,
    )
    binding = dataclasses.replace(
        make_closure_records("complete")[1].operation_binding,  # type: ignore[attr-defined]
        signature_requirement_result_identity=requirement.result_identity,
        task_revision=revision,
    )
    policy = make_closure_records("complete")[0]
    authorization = identify_record(
        DevelopmentTaskAuthorization(
            1,
            "record.auth",
            "0" * 64,
            1,
            policy.record_content_identity,  # type: ignore[attr-defined]
            "task_authorization",
            "issuer.one",
            policy.record_content_identity,  # type: ignore[attr-defined]
            "authorization.one",
            binding,
            1,
        )
    )
    resolution = resolve_record_fixture((policy, authorization))
    assert resolution.status == "resolved"
    context = resolution.context
    assert isinstance(context, DevelopmentAuthorityContext)
    operation_body: dict[str, object] = {
        "schema_version": 1,
        "input_identity": None,
        "operation_binding": binding,
    }
    operation_body["input_identity"] = framed_identity(
        "ksdft2effmass-development-operation-authorization-input", operation_body
    )
    operation = DevelopmentOperationAuthorizationInput(**operation_body)  # type: ignore[arg-type]
    authorizer = DevelopmentOperationAuthorizer()
    assert authorizer.execute(operation, requirement, resolution).status == "authorized"
    forged_authorization = identify_record(
        dataclasses.replace(
            authorization,
            authorization_id="authorization.forged",
            record_content_identity="0" * 64,
        )
    )
    forged_context = dataclasses.replace(
        context,
        context_identity="0" * 64,
        record_head_identity=forged_authorization.record_content_identity,  # type: ignore[attr-defined]
        records=(policy, forged_authorization),  # type: ignore[arg-type]
    )
    forged_context = dataclasses.replace(
        forged_context,
        context_identity=framed_identity(
            "ksdft2effmass-development-authority-context",
            {**dataclasses.asdict(forged_context), "context_identity": None},
        ),
    )
    forged = DevelopmentAuthorityContextResolutionResult(
        1, "resolved", resolution.receipt, forged_context
    )
    assert authorizer.execute(operation, requirement, forged).status == "error"


def test_artifact__resolution_result__rejects_resolved_receipt_diagnostics() -> None:
    """Resolved context results require an empty receipt diagnostic tuple.

    Evidence ID: SV-AUTH-012

    Requirement: Runtime and JSON Schema both prohibit diagnostics on a resolved
    authority-context result even when every receipt status passed.

    Oracle: The accepted resolved-result discriminant requires ``diagnostics=[]``.

    Acceptance: Typed construction raises and schema validation reports an error for
    the same otherwise successful result with one diagnostic.
    """
    resolution = resolve_record_fixture(make_closure_records("complete"))
    assert resolution.status == "resolved"
    diagnostic = DevelopmentAuthorityDiagnostic(
        "AUTH.UNEXPECTED", None, "resolved receipt must have no diagnostics"
    )
    bad_receipt = dataclasses.replace(
        resolution.receipt, diagnostics=(diagnostic,)
    )
    with pytest.raises(ValueError, match="no diagnostics"):
        DevelopmentAuthorityContextResolutionResult(
            1, "resolved", bad_receipt, resolution.context
        )
    value = dataclasses.asdict(resolution)
    value["receipt"]["diagnostics"] = [dataclasses.asdict(diagnostic)]  # type: ignore[index]
    schema = json.loads(
        Path(
            "../harness/schemas/authority-v1/authority-resolution.schema.json"
        ).read_text()
    )
    assert tuple(Draft202012Validator(schema).iter_errors(value))


def test_artifact__schema_runtime__rejects_status_nullability_disagreement() -> None:
    """Schemas and deserializers reject invalid closed-result combinations.

    Evidence ID: SV-AUTH-011

    Requirement: Result status discriminates context, authorization, diagnostics, and
    nullable fields identically in JSON Schema and runtime deserialization.

    Oracle: Explicit combinations prohibited by the accepted status variants.

    Acceptance: Both schemas and both typed deserializers reject every invalid value.
    """
    task_record = "a" * 64
    revision = framed_identity(
        "ksdft2effmass-development-configured-task-revision",
        {
            "schema_version": 1,
            "task_record_identity": task_record,
            "signature_configuration_identity": None,
            "signature_requirement": "not_required",
        },
    )
    requirement = DevelopmentTaskSignatureRequirementResolver().execute(
        task_id="task.one",
        task_record_identity=task_record,
        expected_task_revision=revision,
    )
    binding = DevelopmentTaskOperationBinding(
        "task",
        requirement.result_identity,
        "repo",
        "source",
        "state",
        "selection",
        "task.one",
        revision,
        "start",
        "candidate",
        "operation",
        "attempt",
        "idempotency",
        "implementation",
        (),
        (),
        "architecture",
        "validator",
    )
    input_body: dict[str, object] = {
        "schema_version": 1,
        "input_identity": None,
        "operation_binding": binding,
    }
    input_body["input_identity"] = framed_identity(
        "ksdft2effmass-development-operation-authorization-input", input_body
    )
    operation = DevelopmentOperationAuthorizationInput(**input_body)  # type: ignore[arg-type]
    valid = DevelopmentOperationAuthorizer().execute(operation, requirement)
    operation_value = dataclasses.asdict(valid)
    operation_value["status"] = "authorized"
    operation_value["diagnostics"] = []
    operation_schema = json.loads(
        Path(
            "../harness/schemas/authority-v1/operation-authorization.schema.json"
        ).read_text()
    )
    assert tuple(Draft202012Validator(operation_schema).iter_errors(operation_value))
    operation_payload = (
        json.dumps(operation_value, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    with pytest.raises(ValueError):
        DevelopmentOperationAuthorizationSerializer().deserialize_result(
            operation_payload
        )

    diagnostic = DevelopmentAuthorityDiagnostic("AUTH.FAIL", None, "failed")
    receipt = DevelopmentAuthorityReconstructionReceipt(
        1,
        "a" * 64,
        "b" * 64,
        "local",
        "c" * 64,
        "d" * 64,
        0,
        "e" * 64,
        None,
        None,
        None,
        0,
        "harness-canonical-json-v1",
        "resolver.v1",
        "failed",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        "not_reached",
        (),
        (diagnostic,),
    )
    failed = DevelopmentAuthorityContextResolutionResult(1, "failed", receipt, None)
    resolution_value = dataclasses.asdict(failed)
    resolution_value["status"] = "resolved"
    resolution_schema = json.loads(
        Path(
            "../harness/schemas/authority-v1/authority-resolution.schema.json"
        ).read_text()
    )
    assert tuple(Draft202012Validator(resolution_schema).iter_errors(resolution_value))
    resolution_payload = (
        json.dumps(resolution_value, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    with pytest.raises(ValueError):
        DevelopmentAuthorityResolutionSerializer().deserialize_result(
            resolution_payload
        )
