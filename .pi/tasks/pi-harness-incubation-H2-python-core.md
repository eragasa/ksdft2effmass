# H2 — Generic Python harness implementation

Status: blocked by accepted H1; no implementation authorized

## Objective

Implement only the accepted generic Python harness contract under `python/src/ksdft2effmass/harness/pi/`, with project-specific Python adapters isolated under `python/src/ksdft2effmass/harness/pi/local/` only where the accepted H1 ownership plan assigns them to H2.

## Prerequisite

`H1:human_accepted`, plus a validated task-ownership manifest naming separate implementation, test, documentation, and independent review owners.

## Planned boundaries

Generic code receives project profiles and resource roots explicitly. It must not depend on CPN classes, SNAKES, Quantum ESPRESSO, Wannier90, periodic-electronic-structure objects, P0--P11 identities, implicit `.pi` discovery, the current working directory, or unsupplied repository-relative paths. Internal generic imports remain relative and the public API exposes only accepted records/actions/results.

## Evidence

Class-owned and boundary-owned software verification, explicit schemas/fixtures where accepted, static dependency and leakage checks, path-confinement cases, public imports, typing/linting, documentation, and independent review. Numerical verification is required only for actual numerical algorithms.

## Exclusions

No generic textual-resource extraction owned by H3, no skill retirement/cutover, no package publication, no P2 work, and no scientific execution.

## Concurrency rule

H2 may overlap H3 only after accepted H1 defines non-overlapping path ownership and both tasks have independently validated ownership manifests. Otherwise the controlling chain runs them sequentially.

## Stop

H2 concludes at separate human acceptance. Acceptance alone does not activate H4 until H3 is also accepted.
