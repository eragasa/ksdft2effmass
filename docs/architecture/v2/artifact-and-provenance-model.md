# Artifact and provenance model

## ArtifactManifest

`ArtifactManifest` is the portable immutable inventory for artifacts produced,
consumed, or referenced by a scientific operation. Each entry separates content
identity from deployment location and records:

- stable artifact identity;
- checksum algorithm and digest;
- byte count;
- media or native format;
- semantic role;
- producer request and result identities;
- parent artifact identities;
- retention classification; and
- optional portable store reference.

Absolute user-specific paths, credentials, scheduler clients, process handles,
and open files are not portable manifest content.

## Lineage

Lineage connects scientific intent, `Campaign`, `CampaignRun`, `Simulation`,
execution request, `SimulationExecutionResult`, native artifacts, normalized
observations, `ScientificAnalysis`, and `ScientificDisposition`. Every edge is
explicit and identity-correlated. Exact byte identity does not imply scientific
compatibility, and compatible semantics do not imply identical bytes.

## Retention

Retention metadata describes expected handling but grants no deletion authority.
The target classifications distinguish at least:

- authoritative compact input or result;
- retained verification fixture;
- reconstructible scratch;
- externally retained native artifact; and
- publication candidate subject to separate authority.

Large wavefunctions, densities, restart trees, and dense matrices remain outside
Git. Compact manifests, exact inputs, checksums, software identities, settings,
and reproduction records remain version controlled.

## Result ownership

`SimulationExecutionResult` references mechanical stdout, stderr, generated
artifacts, resource observations, warnings, and native calculator metadata.
`ScientificAnalysis` references normalized observations and states algorithms,
units, tolerances, and findings. `ScientificDisposition` references the analyses
and authority supporting a conclusion. These records do not overwrite one
another.

## Publication and stores

Artifact publication is a bounded effect owned by the calculator executor or an
explicit artifact service composed with it. Publication verifies complete bytes
before returning identities. Portable logical stores resolve through explicit
configuration and confinement rules. A run-local copy is derived input, not the
source authority.

## Privacy and integrity

Environment capture is allowlisted and sanitized. Secrets, private keys, tokens,
restricted data, and unrestricted environment mappings are forbidden. Missing
or conflicting identity, lineage, or manifest closure produces a structured
failure and stops dependent CPN transitions.
