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
its immutable ``BlindAlignmentEncodedDocuments``. Filesystem resolution is supplied to
calculation, correlation, and verification requests rather than stored with encoded
bytes. The [row-041 document dossier](periodic1d/campaign/alignment/blind/encoded_documents/BlindAlignmentEncodedDocuments/index.md)
binds this split to exact retained-byte identities and scientific exclusions. Row 062
moves the complete family to `ksdft2effmass.periodic1d.campaign.alignment.blind`; its
[canonical family dossier](periodic1d/campaign/alignment/blind/index.md) maps source,
tests, Sphinx, provenance, numerical scaling, and limitations. The former underscored
route is removed without an alias. Maintained low-level records and Actionizers are
imported from their defining canonical modules and are not aggregated into the
supported public route. The inference core supports full-rank,
rank-deficient identified-sector, and explicitly reconciled rectangular
partial-isometry routes, with structured stops for rank, spin, subspace-angle,
conditioning, and energy-anchor boundaries. A separate verifier authenticates direct
and transitive sources and independently reconstructs all 34 retained records without
importing maintained calculation algorithms. The maintained blind-alignment software
and numerical-verification slice is therefore complete; this status makes no material
validation or uncertainty-quantification claim.

Independent-route reconciliation now has a maintained typed package slice. Its encoded
document owner stores exact input and retained-result bytes only, while distinct
calculation, retained-correlation, and verification requests own their absolute
filesystem roots. The [row-044 canonical dossier](periodic1d/campaign/reconciliation/route/encoded_documents/RouteReconciliationEncodedDocuments/index.md)
binds that split to exact retained-byte/checksum identities, routine and artifact-owned
evidence, the curated facade, and retired aggregate-route removal; row 066 separately
owns the source move to `periodic1d.campaign.reconciliation.route`. Its strict input
adapter and baseline loader authenticate the directly declared matched input, matched
result, and periodic parent. Separate Actionizers implement direct site-space and direct
folded-fiber extraction without invoking each other. The Workflow retains seven nominal
controls, four explicit mismatch outcomes, and four declared reconciliations without
silently changing parent, domain, weights, or map. Canonical correlation reproduces the
retained result identity, while a verifier that imports no maintained Workflow
reconstructs all 15 records independently. The row-044 dossier establishes software
ownership and content identity; it does not by itself rerun or verify those numerics.

The finite-rank oracle now has encoded documents and a façade with explicit
operation-owned filesystem resolution: calculation and retained correlation receive an
absolute root argument, while independent verification uses a typed root-owning
request. The [row-043 canonical dossier](periodic1d/campaign/oracle/finite_rank/encoded_documents/FiniteRankOracleEncodedDocuments/index.md)
binds that split to exact retained-byte identities, owned tests, supported routes, and
scientific exclusions; row 064 separately owns the source move to
`periodic1d.campaign.oracle.finite_rank`. Strict version-one input adaptation,
three-source authentication, separate Bloch-resolvent and site-space numerical routes,
canonical retained correlation, and an independent verifier cover 20 rank-one sweep
records plus four special controls. Degenerate states use equal-rank projectors, and
unequal rank remains an explicit stop. This named bounded analytical route is not a
generic oracle engine or production qualification mechanism.

Separated continuum refinement now has encoded documents and a façade with explicit
operation-owned filesystem resolution: correlation receives an absolute root argument,
while independent verification uses a typed root-owning request. The
[row-042 canonical dossier](periodic1d/campaign/refinement/continuum/encoded_documents/ContinuumRefinementEncodedDocuments/index.md)
binds that split to exact retained-byte identities, owned tests, supported routes, and
scientific exclusions; row 063 separately owns the source move to
`periodic1d.campaign.refinement.continuum`. Strict version-one input adaptation,
three-source authentication, distinct continuum-mesh,
continuum-domain, lattice-supercell, lattice-scale, and profile-family operations,
canonical retained correlation, and an independent verifier for all 31 records. The
verifier imports no maintained Workflow or construction Actionizer. It preserves the
retained bounded conclusion: the tested lattice-scale sequence has a persistent pass,
but neither profile-width family establishes a profile-defined continuum crossover
over the tested width domain. The five-capability software-integration chain is
complete; this status is not an asymptotic theorem or scientific validation claim.

## Package ownership

Campaign families move individually to the canonical application-specific surface:

```text
ksdft2effmass.periodic1d.campaign
```

Blind alignment is canonical at `periodic1d.campaign.alignment.blind`; the unmatched
families remain under `ksdft2effmass.campaigns.periodic_1d.defects` until their assigned
migration rows. The existing `periodic_1d` package remains the provisional owner of
reusable periodic-parent
records, calculations, and controlled toy models. Reusable models demonstrated by
the defect campaigns belong under `periodic_1d/model/toy_defects/`; examples include
finite hopping parents, primitive fibers, twisted supercells, controlled basis
scrambling, Gaussian onsite defects, and later finite-rank or continuum comparators.
The shared basis-scrambling constructor supplies explicitly oriented
reference-to-candidate and candidate-to-reference maps to both matched extraction and
blind-alignment baseline adaptation. These models expose typed
state, request, Action, and Result objects without retaining phase labels, campaign
thresholds, provenance paths, or acceptance policy.

Reusable finite-periodic geometry and represented operator mechanics remain with
their existing solid-state and operator owners. The `defects` package owns only
research-monograph campaign records, exact version-one adaptation, orchestration,
campaign policy, retained-result correlation, and independent campaign
verification. Campaign Workflows consume toy-model Actions rather than owning
competing numerical constructions.

The intended internal capability groups are:

```text
periodic1d/campaign/
  extraction/matched/
  alignment/blind/
  reconciliation/route/
  oracle/finite_rank/
  refinement/continuum/
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
routes. New maintained tests and integrations import each family's defining canonical or
transitional modules; matched-extraction and blind-alignment tests mirror
`ksdft2effmass.periodic1d.campaign.extraction.matched` and
`ksdft2effmass.periodic1d.campaign.alignment.blind`, respectively. No top-level `ksdft2effmass`
re-export, CLI, dependency, or shared ProjectKoios extraction is introduced by this
integration.

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
