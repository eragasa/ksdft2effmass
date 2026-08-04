# H3 — Skills and textual-resource extraction

Status: blocked by accepted H1; no extraction or retirement authorized

## Objective

Create accepted generic operational skills and textual resources under `harness/pi/`, with project profiles/extensions under `harness/local/`, without copying project-specific task IDs, evidence prefixes, scientific semantics, or repository paths into the generic layer.

## Prerequisite

`H1:human_accepted`, plus a validated task-ownership manifest with paths disjoint from H2 and separate review ownership.

## Planned scope

Subject to H1 approval, extract only classified generic skills, directly referenced one-level resources, templates, schemas, manifests, and parameterized validators. Project-local profiles supply marker names, evidence-ID namespaces, paths, and scientific/task extensions. Resource identities require kind, version, stable identifier, dependencies, and content identity where required.

## Evidence

Resource-manifest validation; missing/duplicate/incompatible resource cases; reference resolution; explicit-profile use; project-leakage checks; software/numerical evidence-classification behavior; independent oracle and ownership review; documentation and integration review.

## Exclusions

No generic Python implementation owned by H2, no silent skill retirement, no replacement of authoritative `.pi` runtime state, no package publication, no P2 work, and no scientific execution.

## Concurrency rule

H3 may overlap H2 only after accepted H1 and validated non-overlapping manifests prove safe concurrency. Otherwise it runs sequentially.

## Stop

H3 concludes at separate human acceptance. Acceptance alone does not activate H4 until H2 is also accepted.
