# H2 — Generic Python harness implementation

Status: blocked at pending `H2-HC01` after the single consolidated correction cycle exposed an accepted H1/H3 manifest-relational-validity contract conflict; no final acceptance, commit, push, or successor activation

## Objective

Implement only the accepted generic Python harness contract under `python/src/ksdft2effmass/harness/pi/`. H2 creates no project-specific Python under `python/src/ksdft2effmass/harness/pi/local/`; H4 owns that entire local Python boundary.

## Activation and prerequisite

`H3:human_accepted` is satisfied through resolved `H3-HC01`. The human PI
separately activated H2 on 2026-08-04 in the instruction titled "Activate and
execute H2 under its existing accepted task, H1 contract, H3 resources,
ownership, review, and validation requirements". Activation is retained at
`.pi/evidence/pi-harness-incubation/H2/activation.json`. The required version-2
ownership manifest is `.pi/evidence/pi-harness-incubation/H2/task-ownership.json`
and must validate before any implementation, test, documentation, or evidence
writer edits. Accepted H1 remains the transitive public contract and accepted H3
resources remain read-only authoritative inputs. This activation authorizes H2
only and does not activate H4, H5, or P2.

## Planned boundaries

Generic code receives project profiles and resource roots explicitly. It must not depend on CPN classes, SNAKES, Quantum ESPRESSO, Wannier90, periodic-electronic-structure objects, P0--P11 identities, implicit `.pi` discovery, the current working directory, or unsupplied repository-relative paths. Internal generic imports remain relative and the public API exposes only accepted records/actions/results.

## Evidence

`class_owned` and `artifact_owned` software verification, with agreement and
direction represented as artifact relation metadata; explicit schemas/fixtures
where accepted; static dependency and leakage checks; path-confinement cases;
public imports; typing/linting; documentation; and independent review.
`ValidationIssue` class-owned evidence must cover a regular-file diagnostic
path, a directory-tree ownership-scope diagnostic path, `None`, and rejection of
absolute, traversal, non-NFC, malformed, control, and Windows/platform-specific
forms. Artifact-owned evidence must cover diagnostic-path ordering, unchanged
specialized path meanings, accepted H3 schema/fixture agreement, and canonical
JSON/intended Rust round trips. Legacy terminology remains only explicit
project-local compatibility input. Numerical
verification is required only for actual numerical algorithms.

## Exclusions

No generic textual-resource extraction owned by H3, no skill retirement/cutover, no package publication, no P2 work, and no scientific execution.

## Sequence rule

H2 follows accepted H3 and must not overlap H3. It implements the accepted
generic Python contract against the generic and local textual resource
identities established by H3.

## Current protected conflict

The initial implementation, independent tests, documentation, validation, and
three independent reviews entered the accepted single consolidated correction
cycle. That cycle exposed a protected conflict between accepted H1/H3 inputs:
strict `ResourceReference`/`ResourceManifest` construction and deserialization
reject duplicate resource identities/paths and self-dependencies before a
manifest object exists, while `ValidateResourceManifest` and accepted H3
resource-resolution oracles require those states to reach the action and produce
capability-specific `PIH.RESOURCE.*` findings. No H2-only change can satisfy both
without changing an accepted public contract or accepted H3 resource.

`.pi/checkpoints/H2-HC01-manifest-relational-validity-boundary.json` owns the
human decision. H2 is blocked there with provisional source, tests,
documentation, review findings, and correction evidence retained. The final H2
acceptance checkpoint was not created; the H2 boundary was not committed or
pushed.

## Stop

H2 concludes only at separate final human acceptance after the protected
conflict is resolved and all required gates and reviews pass. Accepted H2 would
satisfy H4's prerequisite but would not activate H4; H4 requires its own separate
human authorization.
