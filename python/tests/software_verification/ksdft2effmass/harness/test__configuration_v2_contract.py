r"""Software verification of the current Harness configuration contract.

Evidence profile: routine

Bounded artifact scope: schema-2 Harness configuration values and wire, plus
independently versioned resolution, identity and validation contracts.

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

import pytest

import ksdft2effmass.harness as api

pytestmark = pytest.mark.software_verification
REPO_ROOT = Path(__file__).resolve().parents[5]
SOURCE_PATH = REPO_ROOT / "harness/configuration.json"


class TestHarnessConfigurationContract:
    """Own the current configuration composition and resolution artifact."""

    def load_source(self) -> api.HarnessConfigurationSource:
        """Evidence ID: Owns no identifier; supports the module's evidence owners.

        Requirement: Load the exact checked-in source through the public deserializer.

        Acceptance: Return the decoded immutable source or propagate a setup failure.
        """
        return api.HarnessConfigurationSourceJsonDeserializer().execute(
            SOURCE_PATH.read_bytes()
        )

    def resolve(
        self,
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

    def test_artifact__data_objects__are_frozen_and_reject_noncanonical_values(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness-configuration.phase1.data-objects

        Requirement: Public configuration values are frozen/slotted and reject Boolean
        versions, mutable or unsorted roots, duplicate paths, and external paths.

        Acceptance: Mutation and every representative invalid partition raise the exact
        contract error family.
        """
        source = self.load_source()
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
                source.catalogs.task_catalog,
                ["agents"],  # type: ignore[arg-type]
                ("checkpoints",),
                ("skills",),
            )
        with pytest.raises(ValueError, match="sorted"):
            api.HarnessCatalogConfiguration(
                source.catalogs.task_catalog, ("z", "a"), ("checkpoints",), ("skills",)
            )
        with pytest.raises(ValueError, match="root-relative"):
            api.HumanReviewConfiguration("/tmp/reviews", None)

    def test_artifact__source_wire__is_canonical_strict_and_round_trips(self) -> None:
        """Evidence ID: software-verification.harness-configuration.phase1.source-wire

        Requirement: The checked-in authoring document is exact two-space canonical JSON
        with ordered members, literal Unicode and one final LF. Noncanonical,
        duplicate, unknown, missing and wrong-type payloads are rejected.

        Acceptance: Serialization reproduces checked-in bytes exactly and each malformed
        representative raises ``TypeError`` or ``ValueError``.
        """
        payload = SOURCE_PATH.read_bytes()
        source = self.load_source()
        assert api.HarnessConfigurationSourceJsonSerializer().execute(source) == payload
        assert payload.endswith(b"\n") and not payload.endswith(b"\n\n")
        noncanonical = payload.replace(
            b'  "schema_version": 2,\n', b' "schema_version": 2,\n'
        )
        duplicate = payload.replace(
            b'  "schema_version": 2,\n',
            b'  "schema_version": 2,\n  "schema_version": 2,\n',
        )
        unknown = payload.replace(
            b'  "pi_settings_path":', b'  "unknown": 0,\n  "pi_settings_path":'
        )
        missing = payload.replace(b'  "schema_version": 2,\n', b"")
        wrong_type = payload.replace(
            b'  "schema_version": 2,', b'  "schema_version": true,'
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

    def test_artifact__resolved_wire__round_trips_without_source_bindings(self) -> None:
        """Evidence ID: software-verification.harness-configuration.phase1.resolved-wire

        Requirement: Resolved canonical JSON round trips the effective configuration and
        excludes source bindings and snapshot identity from configuration equality.

        Acceptance: Exact round trip preserves equality and the wire contains neither
        binding nor snapshot members.
        """
        result = self.resolve(b'{"futurePiField":1,"subagents":{"agentOverrides":{}}}')
        assert result.status == "resolved"
        assert result.configuration is not None
        payload = api.HarnessConfigurationJsonSerializer().execute(result.configuration)
        replay = api.HarnessConfigurationJsonDeserializer().execute(payload)
        assert replay == result.configuration
        assert b"source_bindings" not in payload
        assert b"snapshot_identity" not in payload

    def test_artifact__resolution__binds_exact_bytes_and_fails_closed(self) -> None:
        """Evidence ID: software-verification.harness-configuration.phase1.resolution

        Requirement: Resolution orders source then Pi bindings, hashes supplied
        sources, preserves Pi open consumed-subset behavior, deterministically
        identifies a valid snapshot, and fails closed on invalid or mismatched input.

        Acceptance: Source roles and SHA-256 digests agree with independent hashes;
        repeated resolution is equal. Malformed Pi JSON or a mismatched Pi path yields
        a closed failure.
        """
        pi_payload = b'{"theme":"pi-owned","subagents":{"agentOverrides":{}}}'
        result = self.resolve(pi_payload)
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
        assert result.snapshot_identity is not None
        assert result.snapshot_identity.algorithm == "sha256"
        assert self.resolve(pi_payload) == result
        bad_pi = self.resolve(b"{")
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

    def test_artifact__validation__rejects_manifests_outside_configured_roots(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness-configuration.phase1.validation

        Requirement: Cross-component validation requires each resource manifest to be
        lexically beneath its corresponding configured root.

        Acceptance: Canonical configuration has no findings; an outside generic manifest
        produces the stable compatibility finding and resolver failure behavior.
        """
        result = self.resolve()
        assert result.configuration is not None
        assert api.HarnessConfigurationValidator().execute(result.configuration) == ()
        configuration = result.configuration
        invalid = api.HarnessConfiguration(
            2,
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
