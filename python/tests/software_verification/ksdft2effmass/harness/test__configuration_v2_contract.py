r"""Software verification of HarnessConfiguration v2 phase-1 contract.

Evidence profile: routine

Bounded artifact scope: the version-1 harness configuration value, wire, resolution,
identity, validation, and public-import contract.

Facet and represented meaning

The artifact represents immutable harness composition data resolved from exact source
and independently authoritative Pi settings bytes.

Intrinsic and cross-object scope

Constructors own intrinsic type, path, ordering, and distinctness invariants. Named
actions own strict JSON, cross-component compatibility, and source resolution.

VVUQ and scientific exclusions

This is software verification only. It establishes no filesystem availability,
authority, scientific validity, protected execution, or human acceptance.
"""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import cast

import pytest

import ksdft2effmass.harness as api

pytestmark = pytest.mark.software_verification
REPO_ROOT = Path(__file__).resolve().parents[5]
SOURCE_PATH = REPO_ROOT / "harness/configuration.json"


def load_source() -> api.HarnessConfigurationSource:
    """Evidence ID: Owns no identifier; supports the module's evidence owners.

    Requirement: Load the exact checked-in source through the public deserializer.

    Acceptance: Return the decoded immutable source or propagate a setup failure.
    """
    return api.HarnessConfigurationSourceJsonDeserializer().execute(
        SOURCE_PATH.read_bytes()
    )


def resolve(
    pi_payload: bytes = b'{"subagents":{"agentOverrides":{}}}',
) -> api.HarnessConfigurationResolutionResult:
    """Evidence ID: Owns no identifier; supports the module's evidence owners.

    Requirement: Resolve the exact source with explicit representative Pi bytes.

    Acceptance: Return the closed public resolution result without interpretation.
    """
    return api.HarnessConfigurationResolver().execute(
        "harness/configuration.json",
        SOURCE_PATH.read_bytes(),
        ".pi/settings.json",
        pi_payload,
    )


def test_artifact__public_api__exports_exact_configuration_surface() -> None:
    """Evidence ID: software-verification.harness-configuration.phase1.public-api

    Requirement: The v2 harness package exports exactly the approved configuration,
    identity, Task, registry, and selection objects and actions.

    Acceptance: ``__all__`` equals the literal approved inventory and every name is
    importable.
    """
    expected = (
        "ContentIdentity",
        "SnapshotIdentity",
        "HumanReviewConfiguration",
        "HarnessPersistenceConfiguration",
        "PythonConformanceConfiguration",
        "HarnessResourceConfiguration",
        "HarnessCatalogConfiguration",
        "HarnessConfigurationSource",
        "HarnessConfiguration",
        "HarnessConfigurationSourceBinding",
        "HarnessConfigurationResolutionFinding",
        "HarnessConfigurationResolutionResult",
        "HarnessConfigurationSourceJsonSerializer",
        "HarnessConfigurationSourceJsonDeserializer",
        "HarnessConfigurationResolver",
        "HarnessConfigurationValidator",
        "HarnessConfigurationJsonSerializer",
        "HarnessConfigurationJsonDeserializer",
        "ArchivedTaskSource",
        "HarnessTask",
        "HarnessTaskSerializer",
        "HarnessTaskDeserializer",
        "HarnessTaskRegistry",
        "DevelopmentTaskSelection",
        "DevelopmentTaskSelectionSerializer",
        "DevelopmentTaskSelectionDeserializer",
        "DevelopmentDecision",
        "DevelopmentDecisionOption",
        "DevelopmentDecisionSerializer",
        "DevelopmentDecisionSourceProvenance",
        "DevelopmentAuthorityContext",
        "DevelopmentAuthorityContextResolutionResult",
        "DevelopmentAuthorityContextResolver",
        "DevelopmentAuthorityDiagnostic",
        "DevelopmentAuthorityLedgerSnapshot",
        "DevelopmentAuthorityPolicy",
        "DevelopmentAuthorityReconstructionReceipt",
        "DevelopmentAuthorityResolutionSerializer",
        "DevelopmentAuthoritySnapshotSource",
        "DevelopmentAuthorizationRevocation",
        "DevelopmentAuthorizationUse",
        "DevelopmentEligibilityReference",
        "DevelopmentIssuerAnchorBinding",
        "DevelopmentOperationAuthorizationInput",
        "DevelopmentOperationAuthorizationResult",
        "DevelopmentOperationAuthorizationSerializer",
        "DevelopmentOperationAuthorizer",
        "DevelopmentPromotionAuthorization",
        "DevelopmentPromotionOperationBinding",
        "DevelopmentReviewAuthorization",
        "DevelopmentReviewOperationBinding",
        "DevelopmentSignatureEntry",
        "DevelopmentSignedAuthoritySnapshot",
        "DevelopmentSignedAuthoritySnapshotSerializer",
        "DevelopmentTaskAuthorization",
        "DevelopmentTaskOperationBinding",
        "DevelopmentTaskSignatureConfiguration",
        "DevelopmentTaskSignatureConfigurationSerializer",
        "DevelopmentTaskSignatureRequirementResolver",
        "DevelopmentTaskSignatureRequirementResult",
        "DevelopmentTrustAnchor",
        "DevelopmentTrustConfiguration",
        "DevelopmentTrustConfigurationPin",
        "DevelopmentTrustConfigurationSerializer",
    )
    assert api.__all__ == expected
    assert all(hasattr(api, name) for name in expected)


def test_artifact__data_objects__are_frozen_and_reject_noncanonical_values() -> None:
    """Evidence ID: software-verification.harness-configuration.phase1.data-objects

    Requirement: Public configuration values are frozen/slotted and reject Boolean
    versions, mutable or unsorted roots, duplicate paths, and external paths.

    Acceptance: Mutation and every representative invalid partition raise the exact
    contract error family.
    """
    source = load_source()
    with pytest.raises(FrozenInstanceError):
        source.schema_version = 2  # type: ignore[misc]
    assert not hasattr(source, "__dict__")
    with pytest.raises(TypeError):
        api.HarnessConfigurationSource(
            True,
            source.pi_settings_path,
            source.human_review,
            source.persistence,
            source.python_conformance,
            source.resources,
            source.catalogs,
        )
    with pytest.raises(ValueError, match="distinct"):
        api.HarnessPersistenceConfiguration("same", "same", "other")
    with pytest.raises(TypeError, match="tuple"):
        api.HarnessCatalogConfiguration(
            "tasks", cast(tuple[str, ...], ["agents"]), ("checkpoints",), ("skills",)
        )
    with pytest.raises(ValueError, match="sorted"):
        api.HarnessCatalogConfiguration(
            "tasks", ("z", "a"), ("checkpoints",), ("skills",)
        )
    with pytest.raises(ValueError, match="root-relative"):
        api.HumanReviewConfiguration("/tmp/reviews", None)


def test_artifact__source_wire__is_canonical_strict_and_round_trips() -> None:
    """Evidence ID: software-verification.harness-configuration.phase1.source-wire

    Requirement: The checked-in authoring document is exact two-space canonical JSON
    with ordered members, literal Unicode, and one final LF; noncanonical, duplicate,
    unknown, missing, and wrong-type payloads are rejected.

    Acceptance: Serialization reproduces checked-in bytes exactly and each malformed
    representative raises ``TypeError`` or ``ValueError``.
    """
    payload = SOURCE_PATH.read_bytes()
    source = load_source()
    assert api.HarnessConfigurationSourceJsonSerializer().execute(source) == payload
    assert payload.endswith(b"\n") and not payload.endswith(b"\n\n")
    noncanonical = payload.replace(
        b'  "schema_version": 1,\n', b' "schema_version": 1,\n'
    )
    duplicate = payload.replace(
        b'  "schema_version": 1,\n',
        b'  "schema_version": 1,\n  "schema_version": 1,\n',
    )
    unknown = payload.replace(
        b'  "pi_settings_path":', b'  "unknown": 0,\n  "pi_settings_path":'
    )
    missing = payload.replace(b'  "schema_version": 1,\n', b"")
    wrong_type = payload.replace(
        b'  "schema_version": 1,', b'  "schema_version": true,'
    )
    deserializer = api.HarnessConfigurationSourceJsonDeserializer()
    with pytest.raises((TypeError, ValueError)):
        deserializer.execute(noncanonical)
    with pytest.raises((TypeError, ValueError)):
        deserializer.execute(duplicate)
    with pytest.raises((TypeError, ValueError)):
        deserializer.execute(unknown)
    with pytest.raises((TypeError, ValueError)):
        deserializer.execute(missing)
    with pytest.raises((TypeError, ValueError)):
        deserializer.execute(wrong_type)


def test_artifact__resolved_wire__round_trips_without_source_bindings() -> None:
    """Evidence ID: software-verification.harness-configuration.phase1.resolved-wire

    Requirement: Resolved canonical JSON round trips the effective configuration and
    excludes source bindings and snapshot identity from configuration equality.

    Acceptance: Exact round trip preserves equality and the wire contains neither
    binding nor snapshot members.
    """
    result = resolve(b'{"futurePiField":1,"subagents":{"agentOverrides":{}}}')
    assert result.status == "resolved"
    assert result.configuration is not None
    payload = api.HarnessConfigurationJsonSerializer().execute(result.configuration)
    replay = api.HarnessConfigurationJsonDeserializer().execute(payload)
    assert replay == result.configuration
    assert b"source_bindings" not in payload
    assert b"snapshot_identity" not in payload


def test_artifact__resolution__binds_exact_bytes_and_fails_closed() -> None:
    """Evidence ID: software-verification.harness-configuration.phase1.resolution

    Requirement: Resolution orders source then Pi bindings, hashes exact supplied
    bytes, preserves Pi open consumed-subset behavior, deterministically identifies a
    valid snapshot, and returns no configuration for invalid or mismatched inputs.

    Acceptance: Roles and SHA-256 digests are exact, repeated resolution is equal, and
    malformed Pi JSON or a mismatched Pi path yields a closed failed result.
    """
    pi_payload = b'{"theme":"pi-owned","subagents":{"agentOverrides":{}}}'
    result = resolve(pi_payload)
    assert result.status == "resolved"
    assert tuple(binding.role for binding in result.source_bindings) == (
        "harness_configuration_source",
        "pi_project_settings",
    )
    observed_digests = tuple(
        binding.content_identity.digest for binding in result.source_bindings
    )
    assert observed_digests == (
        hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        hashlib.sha256(pi_payload).hexdigest(),
    )
    assert result.snapshot_identity == api.SnapshotIdentity(
        1,
        "sha256",
        "5a97c2d21465e0346df98484341ed090063491b6f0a509cdcba9920999b5040f",
    )
    assert resolve(pi_payload) == result
    bad_pi = resolve(b"{")
    assert bad_pi.status == "failed"
    assert bad_pi.configuration is None and bad_pi.snapshot_identity is None
    mismatch = api.HarnessConfigurationResolver().execute(
        "harness/configuration.json",
        SOURCE_PATH.read_bytes(),
        ".pi/other.json",
        b"{}",
    )
    assert mismatch.status == "failed"
    assert mismatch.configuration is None and mismatch.findings


def test_artifact__validation__rejects_manifests_outside_configured_roots() -> None:
    """Evidence ID: software-verification.harness-configuration.phase1.validation

    Requirement: Cross-component validation requires each resource manifest to be
    lexically beneath its corresponding configured root.

    Acceptance: Canonical configuration has no findings; an outside generic manifest
    produces the stable compatibility finding and resolver failure behavior.
    """
    result = resolve()
    assert result.configuration is not None
    assert api.HarnessConfigurationValidator().execute(result.configuration) == ()
    configuration = result.configuration
    invalid = api.HarnessConfiguration(
        1,
        configuration.pi,
        configuration.human_review,
        configuration.persistence,
        configuration.python_conformance,
        api.HarnessResourceConfiguration(
            configuration.resources.project_profile_path,
            "other/resource-manifest.json",
            configuration.resources.generic_root,
            configuration.resources.local_manifest_path,
            configuration.resources.local_root,
        ),
        configuration.catalogs,
    )
    findings = api.HarnessConfigurationValidator().execute(invalid)
    assert tuple(finding.code for finding in findings) == (
        "HARNESS_CONFIGURATION.RESOURCE_MANIFEST_OUTSIDE_ROOT",
    )
