# H2 — Generic Python harness implementation

Status: blocked by accepted H3; inactive and no implementation authorized

## Objective

Implement only the accepted generic Python harness contract under `python/src/ksdft2effmass/harness/pi/`. H2 creates no project-specific Python under `python/src/ksdft2effmass/harness/pi/local/`; H4 owns that entire local Python boundary.

## Prerequisite

`H3:human_accepted`, plus a validated task-ownership manifest naming separate
implementation, test, documentation, and independent review owners. Accepted
H1 remains a transitive prerequisite through H3. H2 requires its own separate
activation; accepted H3 does not activate H2.

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

## Stop

H2 concludes at separate human acceptance. Accepted H2 satisfies H4's task
prerequisite but does not activate H4; H4 requires its own separate human
authorization.
