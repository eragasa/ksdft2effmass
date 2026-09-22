r"""Software verification of validation domain validators.

Evidence profile: routine

Bounded artifact scope: capability, resource, and source-level evidence catalog
validation over one immutable normalized Harness state.

Facet and represented meaning

The artifact verifies that each public domain validator reports its owned structural
closure defects without changing the supplied state.

Intrinsic and cross-object scope

This is an artifact-owned agreement check across the three catalog validators. State
composition, Task graph, selection, decision, authority, and conformance parsing are
excluded.

VVUQ and scientific exclusions

This is software verification only. It establishes no semantic evidence acceptance,
numerical verification, scientific validation, uncertainty quantification, protected
authority, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.harness import (
    HarnessCapabilityCatalog,
    HarnessCapabilityCatalogValidator,
    HarnessEvidenceCatalog,
    HarnessEvidenceCatalogValidator,
    HarnessResourceCatalog,
    HarnessResourceCatalogValidator,
    HarnessSourceIdentity,
    HarnessState,
    ValidationStatus,
)
from ksdft2effmass.harness.pi import ResourceManifest, ResourceReference

pytestmark = pytest.mark.software_verification


class TestHarnessValidationDomainValidators:
    """Own catalog-validator public-behavior agreement evidence."""

    @staticmethod
    def replace_capabilities(
        state: HarnessState, capabilities: HarnessCapabilityCatalog
    ) -> HarnessState:
        """Rebuild a state with one explicit capability catalog."""
        return HarnessState.create(
            source_snapshot_identity=state.source_snapshot_identity,
            normalization_version=state.normalization_version,
            tasks=state.tasks,
            selection=state.selection,
            decisions=state.decisions,
            capabilities=capabilities,
            resources=state.resources,
            evidence=state.evidence,
            provenance=state.provenance,
        )

    @staticmethod
    def replace_resources(
        state: HarnessState, resources: HarnessResourceCatalog
    ) -> HarnessState:
        """Rebuild a state with one explicit resource catalog."""
        return HarnessState.create(
            source_snapshot_identity=state.source_snapshot_identity,
            normalization_version=state.normalization_version,
            tasks=state.tasks,
            selection=state.selection,
            decisions=state.decisions,
            capabilities=state.capabilities,
            resources=resources,
            evidence=state.evidence,
            provenance=state.provenance,
        )

    @staticmethod
    def replace_evidence(
        state: HarnessState, evidence: HarnessEvidenceCatalog
    ) -> HarnessState:
        """Rebuild a state with one explicit evidence-source catalog."""
        return HarnessState.create(
            source_snapshot_identity=state.source_snapshot_identity,
            normalization_version=state.normalization_version,
            tasks=state.tasks,
            selection=state.selection,
            decisions=state.decisions,
            capabilities=state.capabilities,
            resources=state.resources,
            evidence=evidence,
            provenance=state.provenance,
        )

    @pytest.mark.parametrize(
        "validator",
        (
            pytest.param(HarnessCapabilityCatalogValidator(), id="capability_catalog"),
            pytest.param(HarnessResourceCatalogValidator(), id="resource_catalog"),
            pytest.param(HarnessEvidenceCatalogValidator(), id="evidence_catalog"),
        ),
    )
    def test_method__execute__accepts_consistent_catalogs(
        self,
        normalized_harness_state: HarnessState,
        validator: HarnessCapabilityCatalogValidator
        | HarnessResourceCatalogValidator
        | HarnessEvidenceCatalogValidator,
    ) -> None:
        """Evidence ID: software-verification.harness.domain-validation.pass

        Requirement: Each domain validator accepts the complete consistent normalized
        catalog owned by its rules.

        Acceptance: Every semantic validator partition returns completed nonblocking
        ``pass`` with no findings.
        """
        result = validator.execute(normalized_harness_state)

        assert result.status is ValidationStatus.PASS
        assert not result.findings
        assert not result.blocking

    def test_method__execute__reports_absent_agent_selected_skill(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.capability-validation.closure

        Requirement: Every agent-selected skill must occur in the normalized
        capability catalog.

        Acceptance: Replacing the agent selection with an absent skill returns exactly
        ``SELECTED_SKILL_MISSING``.
        """
        catalog = normalized_harness_state.capabilities
        agent = replace(
            catalog.agent_definitions[0],
            selected_skills=("absent-skill",),
        )
        changed = HarnessCapabilityCatalog.create(
            model_version=1,
            normalization_version=normalized_harness_state.normalization_version,
            capabilities=catalog.capabilities,
            agent_definitions=(agent,),
        )
        state = self.replace_capabilities(normalized_harness_state, changed)

        result = HarnessCapabilityCatalogValidator().execute(state)

        assert tuple(finding.code for finding in result.findings) == (
            "HV.CAPABILITY.SELECTED_SKILL_MISSING",
        )

    def test_method__execute__reports_resource_layer_and_dependency_defects(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.resource-validation.closure

        Requirement: A local manifest names an existing base and every resource
        dependency occurs in the complete catalog.

        Acceptance: An absent base and absent dependency return exactly the two
        rule-specific findings with the resource path retained.
        """
        original = normalized_harness_state.resources.resources[0].resources[0]
        local_resource = ResourceReference(
            original.schema_version,
            "local-entry",
            original.resource_kind,
            original.format_version,
            "local/entry.md",
            original.content_identity,
            ("absent-resource",),
        )
        local_manifest = ResourceManifest(
            1,
            "local-resources",
            1,
            "local",
            "absent-base",
            (local_resource,),
        )
        changed = HarnessResourceCatalog.create(
            model_version=1,
            normalization_version=normalized_harness_state.normalization_version,
            resources=(local_manifest,),
        )
        state = self.replace_resources(normalized_harness_state, changed)

        result = HarnessResourceCatalogValidator().execute(state)

        assert tuple(finding.code for finding in result.findings) == (
            "HV.RESOURCE.DEPENDENCY_MISSING",
            "HV.RESOURCE.BASE_MISSING",
        )
        assert result.affected_paths == ("local/entry.md",)

    def test_method__execute__rejects_local_manifest_as_base(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.resource-validation.layering

        Requirement: Every local manifest extends a generic manifest rather than a
        second local overlay.

        Acceptance: A local manifest extending another valid local manifest returns
        exactly one ``BASE_NOT_GENERIC`` finding.
        """
        generic = normalized_harness_state.resources.resources[0]
        template = generic.resources[0]
        local_a = ResourceManifest(
            1,
            "local-a",
            1,
            "local",
            generic.manifest_id,
            (
                replace(
                    template,
                    resource_id="local-a-entry",
                    path="local/a.md",
                ),
            ),
        )
        local_b = ResourceManifest(
            1,
            "local-b",
            1,
            "local",
            local_a.manifest_id,
            (
                replace(
                    template,
                    resource_id="local-b-entry",
                    path="local/b.md",
                ),
            ),
        )
        changed = HarnessResourceCatalog.create(
            model_version=1,
            normalization_version=normalized_harness_state.normalization_version,
            resources=(local_a, local_b, generic),
        )
        state = self.replace_resources(normalized_harness_state, changed)

        result = HarnessResourceCatalogValidator().execute(state)

        assert tuple(finding.code for finding in result.findings) == (
            "HV.RESOURCE.BASE_NOT_GENERIC",
        )

    def test_method__execute__reports_duplicate_evidence_source_closure(
        self, normalized_harness_state: HarnessState
    ) -> None:
        """Evidence ID: software-verification.harness.evidence-validation.closure

        Requirement: Evidence source paths and exact source identities are unique
        within the normalized source-level catalog.

        Acceptance: Duplicating one exact source and identity returns exactly the path
        and source-identity findings without parsing evidence semantics.
        """
        catalog = normalized_harness_state.evidence
        source = catalog.evidence[0]
        identity: HarnessSourceIdentity = catalog.source_identities[0]
        changed = HarnessEvidenceCatalog.create(
            model_version=1,
            normalization_version=normalized_harness_state.normalization_version,
            evidence=(source, source),
            source_identities=(identity, identity),
        )
        state = self.replace_evidence(normalized_harness_state, changed)

        result = HarnessEvidenceCatalogValidator().execute(state)

        assert tuple(finding.code for finding in result.findings) == (
            "HV.EVIDENCE.DUPLICATE_PATH",
            "HV.EVIDENCE.DUPLICATE_SOURCE_IDENTITY",
        )
        assert "ownership" in result.claim_boundary
