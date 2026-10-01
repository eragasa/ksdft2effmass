# Periodic-1D defect campaign integration

## Status and authority

This page defines the authorized software-integration boundary for the five
completed synthetic periodic-1D defect capabilities retained under
`calculations/research-monograph/`. It does not alter their scientific
protocols, version-one wire documents, calculated results, figures, checksums,
or human-acceptance records. Those retained calculation directories remain the
authoritative evidence sources for their exact inputs and outputs.

The integration is software work. It may establish agreement with documented
software and numerical contracts, but it does not establish silicon behavior,
material validation, transferability, an asymptotic continuum theorem, or
uncertainty quantification. No Quantum ESPRESSO, Wannier90, remote, or
production calculation is authorized by this page.

## Five-capability chain

Historical phase letters identify provenance only. Supported software names use
the scientific capability.

| Historical phase | Scientific capability | Retained owner |
|---|---|---|
| A | Matched known-map extraction | `impurity-defect-1d/` |
| B | Blind alignment and identified-sector extraction | `impurity-defect-1d-blind-alignment/` |
| C | Independent real-space and Bloch-fiber route reconciliation | `impurity-defect-1d-independent-route/` |
| D | Finite-rank resolvent oracle | `impurity-defect-1d-analytical-oracle/` |
| E | Separated continuum refinement | `impurity-defect-1d-continuum-refinement/` |

The dependency order is A, B, C, D, E. Phase D also consumes the retained Phase
C result identity, and Phase E consumes retained Phase A and D identities plus the
isolated periodic-parent identity. These dependencies identify evidence inputs; they
do not authorize one phase to rewrite another phase's artifacts.

## Integration status

The matched known-map capability has a maintained typed package slice, canonical
version-one serializer, explicit parent authentication, compatibility gate,
structured workflow result, and independent retained-result verifier. Its focused
normal and optimized-runtime checks correlate the scientific payload with the
retained Phase-A artifact while preserving distinct implementation provenance.

Blind-alignment integration has begun with immutable version-one input records, a
strict closed input deserializer, authenticated adaptation of the matched-extraction
baseline, a constructor that separates inference-visible observations from hidden
post hoc truth, immutable observation, policy, request, and result records, an
observation-only inference Actionizer, a separate post hoc evaluator, complete typed
version-one result records, strict result decoding, canonical result encoding,
identity-only retained-result correlation, and complete campaign composition. The
package boundary exports only the encapsulating ``BlindAlignmentCampaign`` façade and
its immutable ``BlindAlignmentCampaignModel``; maintained low-level records and
Actionizers are imported from their defining modules and are not aggregated into the
supported public route. The inference core supports full-rank,
rank-deficient identified-sector, and explicitly reconciled rectangular
partial-isometry routes, with structured stops for rank, spin, subspace-angle,
conditioning, and energy-anchor boundaries. A separate verifier authenticates direct
and transitive sources and independently reconstructs all 34 retained records without
importing maintained calculation algorithms. The maintained blind-alignment software
and numerical-verification slice is therefore complete; this status makes no material
validation or uncertainty-quantification claim.

Independent-route reconciliation now has a maintained typed package slice. Its
encapsulating model and façade own exact retained-wire state; its strict input adapter
and baseline loader authenticate the matched input, matched result, and periodic parent;
and separate Actionizers implement direct site-space and direct folded-fiber
extraction without invoking each other. The Workflow retains seven nominal controls,
four explicit mismatch outcomes, and four declared reconciliations without silently
changing parent, domain, weights, or map. Canonical correlation reproduces the retained
result identity, while a verifier that imports no maintained Workflow reconstructs all
15 records independently.

The finite-rank oracle now has an encapsulated model and façade, strict version-one
input adaptation, three-source authentication, separate Bloch-resolvent and site-space
numerical routes, canonical retained correlation, and an independent verifier for 20
rank-one sweep records plus four special controls. Degenerate states use equal-rank
projectors, and unequal rank remains an explicit stop.

Separated continuum refinement now has an encapsulated model and façade, strict
version-one input adaptation, three-source authentication, distinct continuum-mesh,
continuum-domain, lattice-supercell, lattice-scale, and profile-family operations,
canonical retained correlation, and an independent verifier for all 31 records. The
verifier imports no maintained Workflow or construction Actionizer. It preserves the
retained bounded conclusion: the tested lattice-scale sequence has a persistent pass,
but neither profile-width family establishes a profile-defined continuum crossover
over the tested width domain. The five-capability software-integration chain is
complete; this status is not an asymptotic theorem or scientific validation claim.

## Package ownership

The integrated campaign belongs under the existing application-specific
surface:

```text
ksdft2effmass.campaigns.periodic_1d.defects
```

The existing `periodic_1d` package remains the owner of reusable periodic-parent
records, calculations, and controlled toy models. Reusable models demonstrated by
the defect campaigns belong under `periodic_1d/model/toy_defects/`; examples include
finite hopping parents, primitive fibers, twisted supercells, controlled basis
scrambling, Gaussian onsite defects, and later finite-rank or continuum comparators.
The shared basis-scrambling constructor supplies explicitly oriented
reference-to-candidate and candidate-to-reference maps to both matched extraction and
blind-alignment baseline adaptation. These models expose typed
state and Actionizer requests and results without retaining phase labels, campaign
thresholds, provenance paths, or acceptance policy.

Reusable finite-periodic geometry and represented operator mechanics remain with
their existing solid-state and operator owners. The `defects` package owns only
research-monograph campaign records, exact version-one adaptation, orchestration,
campaign policy, retained-result correlation, and independent campaign
verification. Campaign workflows consume toy-model Actionizers rather than owning
competing numerical constructions.

The intended internal capability groups are:

```text
defects/
  matched_extraction/
  blind_alignment/
  route_reconciliation/
  finite_rank_oracle/
  continuum_refinement/
```

A group may be split into records, serializers, actions, workflows, and
verification modules when its demonstrated behavior requires those owners.
Generic helpers, untyped dictionaries beyond the closed JSON boundary, and
module-level behavioral functions are prohibited. Immutable DataObjects own
state and intrinsic invariants; serializers own wire mechanics; ActionObjects
own comparison, construction, inference, and verification; Workflows own only
genuine multi-step campaign composition.

## Compatibility and import policy

The retained version-one JSON documents are fixed compatibility inputs. New
deserializers must reject unsupported schema versions, booleans where numbers
are required, numeric strings, nonfinite values, incomplete records, and
incompatible represented spaces. Existing field names, sign conventions,
units, tolerances, ordering, and structured stopping outcomes must not be
silently normalized or reinterpreted.

Historical calculation-local implementations remain frozen and import no new
package code. They are provenance-bound evidence, not supported execution
routes. New maintained tests and integrations import defining modules beneath
`ksdft2effmass.campaigns.periodic_1d.defects`. No top-level
`ksdft2effmass` re-export, CLI, dependency, or shared ProjectKoios extraction is
introduced by this integration.

## Evidence-preserving migration

Each capability follows the same bounded sequence:

1. identify its immutable retained input, result, source identities, and exact
   version-one contract;
2. introduce typed records and serializer or deserializer actions;
3. extract the demonstrated calculation or inference actions without importing
   calculation-local runner code;
4. implement an independent verifier that does not import the production
   construction algorithm;
5. correlate the package result with the retained artifact without rewriting
   that artifact; and
6. document the defining-module import route and evidence limitation.

Reading and hashing retained artifacts is allowed. Overwriting, regenerating,
reformatting, or relabelling them is forbidden. A newly calculated result must
use a new output path and retained provenance; compatibility with a historical
result does not transfer that result's acceptance status.

## Completion criteria

A capability is integrated only when all of the following hold:

- its input and result records are closed and strictly typed;
- version-one decoding and encoding behavior is explicit where applicable;
- production and independent-verification algorithms remain separate;
- structured incompatibility and stopping outcomes are preserved;
- maintained software-verification tests cover positive and negative contracts;
- applicable numerical-verification tests use explicit tolerances and identify
  their bounded synthetic claim;
- retained artifact identities and values are unchanged;
- focused Ruff, formatting, mypy, pytest, optimized-runtime, and checksum checks
  pass; and
- documentation states that the capability is synthetic verification rather
  than material validation.

The full chain is complete only after all five capabilities meet these criteria.
Partial integration must be reported by capability and must not be described as
completion of the chain.
