# H3 — Skills and textual-resource extraction

Status: blocked by accepted H1; inactive and no extraction or retirement authorized

## Objective

Create accepted generic operational skills and textual resources under `harness/pi/`, with project profiles/extensions under `harness/local/`, without copying project-specific task IDs, evidence prefixes, scientific semantics, or repository paths into the generic layer.

## Prerequisite

`H1:human_accepted`, plus a validated task-ownership manifest with explicit
resource/profile paths and separate implementation, documentation, test, and
review ownership. H3 requires its own separate activation; accepted H1 does not
activate H3.

## Planned scope

Subject to H1 approval, extract only classified generic skills, directly referenced one-level resources, templates, schemas, manifests, and parameterized validators. Project-local profiles supply marker names, evidence-ID namespaces, paths, and scientific/task extensions. Resource identities require kind, version, stable identifier, dependencies, and content identity where required.

## Evidence

Resource-manifest validation; missing/duplicate/incompatible resource cases; reference resolution; explicit-profile use; project-leakage checks; software/numerical evidence-classification behavior; independent oracle and ownership review; documentation and integration review.

## Exclusions

No generic Python implementation owned by H2, no silent skill retirement, no replacement of authoritative `.pi` runtime state, no package publication, no P2 work, and no scientific execution.

## Sequence rule

H3 precedes H2 and must not overlap H2. It establishes the accepted generic and
local textual resource identities that H2 consumes.

## Stop

H3 concludes at separate human acceptance. Accepted H3 satisfies H2's task
prerequisite but does not activate H2; H2 requires its own separate human
authorization.
