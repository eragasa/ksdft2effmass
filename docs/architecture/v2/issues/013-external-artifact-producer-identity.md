# V2-ISSUE-013: Producer identity for external input artifacts

**Severity:** Medium

**Scope:** Artifact manifests and lineage

## Conflict

`ArtifactManifest` covers produced, consumed, and referenced artifacts but requires producer request and result identities. External pseudopotentials, imported fixtures, human-authored compact inputs, and other pre-existing artifacts may have no represented workflow request or result producer.

## Affected contracts

- `workflow/artifact-and-provenance-model.md` — *ArtifactManifest*
- `workflow/simulation-model.md` — required external artifacts
- `identity-version-and-failure-contracts.md` — producer correlation

## Required resolution

Represent producer provenance as a closed variant, including workflow-produced, externally acquired, retained fixture, human-authored, transformed, and explicitly bounded unknown-legacy provenance where applicable. Do not fabricate request or result identities.

## Acceptance condition

Every artifact role has unambiguous lineage semantics, and absence of a represented workflow producer is explicit rather than null or invented provenance.
