# H2 — Generic Python harness implementation

Status: closed as human-accepted PASS at resolved `H2-HC02`; no successor activation

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

## Resolved protected boundary and authorized correction

The initial implementation, independent tests, documentation, validation, and
three independent reviews exposed a protected conflict between accepted H1/H3
inputs. The human PI resolved `H2-HC01` as Option A on 2026-08-05 after the
pending conflict boundary was recovered and pushed at
`7f8c3d781bff535dd355d47ad0172d0b5f35bee1`.

The bounded correction keeps field presence, exact semantic types, enum/scalar
and lexical-path rules, immutable tuple storage, field-local uniqueness,
canonical ordering, and generic/local layer shape intrinsic to version-1 record
construction and deserialization. It moves relational manifest validity to
`ValidateResourceManifest`, including duplicate entry IDs/paths, self-edges,
missing dependencies, dependency cycles, generic-to-local edges, incompatible
kind/format, generic/local mismatch, and forbidden local replacement. A
structurally valid candidate manifest may therefore construct and deserialize
without being accepted, authorized, resolvable, or capability-valid.

The correction may reconcile only directly affected H1 contract evidence, H3
schemas/fixtures/oracles/manifests/handoff/validator/docs/checksums, H2
source/tests/docs/evidence, remaining deterministic H2 hygiene, declared
validation, and one integrated focused re-review by the existing independent
reviewers. It adds no interface or contract version. H4, H5, P2, local Python,
SQLite, dependencies/locks, live-skill cutover, CPN/scientific code, protected
execution, and unrelated work remain outside scope.

## Final acceptance boundary

The resolved Option-A correction, H2 implementation, independent tests,
documentation, retained evidence, integrated review and deterministic finding
closure, final verification, and checksums were accepted by the human PI as
PASS at resolved `.pi/checkpoints/H2-HC02-final-acceptance.json` on
2026-08-05. H2 is closed.

H2 acceptance satisfies H4's prerequisite but does not activate H4. H4 requires
its own separate human authorization. No additional review/correction loop,
H4/H5/P2 activation, project-local cutover, SQLite work, protected or external
execution, scientific execution, publication, or release work is authorized by
this acceptance.
