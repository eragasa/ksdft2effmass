# Research-monograph results projection

**Status:** Implemented repository-local application projection.

## Responsibility

`ksdft2effmass.campaigns.research_monograph.results_projection` constructs a
rebuildable SQLite projection of retained files under
`calculations/research-monograph/`. It owns navigation records, safe artifact
locators, bounded text previews, scalar JSON observations, and checksum-manifest
observations for read-only presentation consumers.

It does not own or execute scientific calculations, verifiers, plotting scripts,
Quantum ESPRESSO, or Wannier90. It does not reinterpret a retained result, establish
scientific validity, or convert a checksum match into an acceptance decision. The
retained source files and their manifests remain authoritative.

## Components

| Component | Responsibility |
| --- | --- |
| `ResearchResultsProjectionRequest` | Identifies the repository root and derived SQLite destination. |
| `ResearchResultsProjectionRebuilder` | Scans accepted repository-local calculation artifacts, builds a complete temporary database, validates it, and atomically replaces the destination. |
| `ResearchResultsProjectionResult` | Returns the completed database path, SHA-256 identity, and table row counts. |

The public Action boundary separates the rebuild operation from its immutable request
and result records. Source-artifact and scalar-walk records remain implementation
internals.

## Storage contract

Schema version 1 is identified by SQLite `application_id = 1263748178` and
`user_version = 1`. It provides:

- `calculations` for direct retained calculation packages;
- `artifacts` for recursively retained files and their media/display properties;
- `runs` for valid retained JSON result documents;
- `scalar_observations` for bounded scalar JSON leaves;
- `manifest_observations` for independent expected-versus-observed byte identities;
- `presentation_artifacts` and `run_results` read-only views; and
- `projection_metadata` for schema and path semantics.

A `runs` row means only that a valid retained result document is available. It does
not claim that an execution occurred in the current environment or that the result is
verified, accepted, converged, or suitable for publication.

All source locators are POSIX paths relative to the supplied repository root. Absolute
paths, parent traversal, and symbolic-link artifacts are not admitted. Text previews
are bounded and explicitly marked when truncated. Consumers resolve complete content
against an explicitly known repository root and must recheck containment.

The default generated database is ignored local state at
`ui/analysis/build/results.sqlite`. The builder uses a same-directory temporary file,
SQLite integrity and foreign-key checks, path-safety checks, an atomic replacement,
and directory synchronization. A long-lived reader must reopen its read-only
connection to observe a replacement generation.

## Verification and operator entry point

Implementation:
`python/src/ksdft2effmass/campaigns/research_monograph/results_projection.py`.

Focused software verification:
`python/tests/software_verification/ksdft2effmass/campaigns/research_monograph/test__ResearchResultsProjection.py`.

Repository-local build and consumer guidance: `ui/analysis/README.md`.
