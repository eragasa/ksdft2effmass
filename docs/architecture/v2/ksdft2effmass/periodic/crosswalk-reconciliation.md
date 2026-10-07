# Periodic crosswalk reconciliation ledger

## Purpose and status semantics

This ledger reconciles all 73 `PERIODIC-XWALK-*` rows against the owning phase pages.
It separates source implementation from the newer scientist-facing documentation and
evidence gate. A historical `Implemented` disposition is not promoted to fully
`Complete` until its documentation dossier and current validation have been audited.

| Implementation status | Meaning |
|---|---|
| `Implemented` | The source disposition recorded by the owning migration phase is present. |
| `Pending` | The target disposition has not been implemented. |
| `Blocked` | Implementation requires metadata, scientific authority, or a contract that cannot be inferred safely. |

| Documentation status | Meaning |
|---|---|
| `Ready for gate` | Applicable source docstrings, tests, Sphinx, and canonical architecture mappings have been reconciled; current validation remains the final gate. |
| `Audit required` | Earlier implementation predates the current completion dossier and must be inspected before the row is called complete. |
| `Blocker documented` | The unavailable information and prohibited inference are documented, but no implemented terminal disposition exists. |
| `Not implemented` | Documentation must be completed with the future implementation rather than describing a nonexistent contract as current. |

## Row ledger

| ID | Implementation | Documentation | Owner and next gate |
|---|---|---|---|
| `PERIODIC-XWALK-001` | Implemented | Ready for gate | `periodic.model`; validate nominal-role source, tests, API, and canonical architecture pages. |
| `PERIODIC-XWALK-002` | Implemented | Ready for gate | `periodic.model`; validate the nominal root and its scientific-category exclusions. |
| `PERIODIC-XWALK-003` | Implemented | Ready for gate | `periodic.model`; validate exact 1D membership and override rejection. |
| `PERIODIC-XWALK-004` | Implemented | Ready for gate | `periodic.model`; validate exact 2D membership and override rejection. |
| `PERIODIC-XWALK-005` | Implemented | Ready for gate | `periodic.model`; validate exact 3D membership and override rejection. |
| `PERIODIC-XWALK-006` | Implemented | Ready for gate | `periodic.model`; validate 1D defect parent-identity boundary. |
| `PERIODIC-XWALK-007` | Implemented | Ready for gate | `periodic.model`; validate 2D defect parent-identity boundary. |
| `PERIODIC-XWALK-008` | Implemented | Ready for gate | `periodic.model`; validate 3D defect parent-identity boundary. |
| `PERIODIC-XWALK-009` | Implemented | Ready for gate | `periodic.catalog`; validate catalog invariants and short delegated `__post_init__`. Phase-6 catalog consumption remains a separate program gate. |
| `PERIODIC-XWALK-010` | Implemented | Ready for gate | Phase 7; cosine-parent equation, nominal identity, API, documented tests, and canonical architecture dossier are reconciled. |
| `PERIODIC-XWALK-011` | Implemented | Ready for gate | Phase 5; finite-hopping parent identity, blocks, units, short invariant entry point, documented tests, and canonical pages are reconciled. |
| `PERIODIC-XWALK-012` | Implemented | Ready for gate | Phase 7; scalar-hopping defect parentage, potential/operator distinction, compatibility boundary, documented tests, and canonical pages are reconciled. |
| `PERIODIC-XWALK-013` | Pending | Not implemented | Phase 5; split Gaussian perturbation data from a parent-qualified nominal defect model. |
| `PERIODIC-XWALK-014` | Implemented | Ready for gate | Phase 5; coefficient data, complete transform representation, truncation, and fit routes have separate typed and documented dossiers. |
| `PERIODIC-XWALK-015` | Pending | Not implemented | Phase 5; keep reusable scalar hopping data independent and add an explicit ksdft scientific effective-model composition where demonstrated. |
| `PERIODIC-XWALK-016` | Implemented | Ready for gate | Phase 7; the finite plane-wave representation definition, represented-result boundary, equations, documented tests, and canonical pages are reconciled. |
| `PERIODIC-XWALK-017` | Implemented | Ready for gate | Phase 5; the Fourier potential component, complete parent law, identity/unit boundaries, documented tests, and canonical pages are reconciled. |
| `PERIODIC-XWALK-018` | Implemented | Ready for gate | Phase 5; the basis-scrambling definition rename, short invariant entry points, Action/map direction, documented tests, retired-name check, and canonical pages are reconciled. |
| `PERIODIC-XWALK-019` | Implemented | Ready for gate | Phases 5 and 7; parent-qualified one- and two-dimensional selected-band definitions, ordering, failure semantics, tests, and canonical pages are reconciled. |
| `PERIODIC-XWALK-020` | Implemented | Ready for gate | Phase 5; retained-band group identity, delegated ordering/rank, tests, and canonical ownership are reconciled; encoded-document byte preservation remains with rows 038 and 056. |
| `PERIODIC-XWALK-021` | Implemented | Ready for gate | Phase 5; the mathematical retained-space versus orthogonal spectral embedding boundary, dimensional tests, and canonical pages are reconciled. |
| `PERIODIC-XWALK-022` | Implemented | Ready for gate | Phase 5 plus band-frame decision; the retained-space versus gauge-frame boundary, endpoint sewing, frame-content digest scope, short validation entry point, tests, and canonical pages are reconciled. |
| `PERIODIC-XWALK-023` | Implemented | Ready for gate | Phase 5; authenticated replay adoption, untruncated versus finite parentage, retained space/operator, frame and complete representation, distinct truncation/fit routes, allowances, retained evidence, documented tests, and canonical `periodic1d.campaign` pages are reconciled. The current underscored source namespace remains transitional pending row 058 and will receive no alias. |
| `PERIODIC-XWALK-024` | Implemented | Ready for gate | Phase 5; finite-parent composite exact operators, smooth reciprocal and smooth/rough hopping forms, basis/gauge/energy/content identities, explicitly unavailable frame/projector/rough-reciprocal data, documented tests, and canonical `periodic1d.campaign` and `periodic1d.representations` pages are reconciled. The current underscored source namespace remains transitional pending row 059 and will receive no alias. |
| `PERIODIC-XWALK-025` | Implemented | Ready for gate | Phase 5; the exact composite source result remains owner of isolation, Wilson, gauge, range, route, represented diagnostics, and artifact identities; unavailable arrays and separate scientific adoption are explicit in canonical `periodic1d.campaign` pages and documented tests. |
| `PERIODIC-XWALK-026` | Implemented | Ready for gate | Phase 5; role-neutral reciprocal samples, short delegated invariants, operation-local projection roles, and explicit retained-operator bindings are reconciled in canonical `solidstate` and `periodic1d.representations` pages and documented tests. |
| `PERIODIC-XWALK-027` | Implemented | Ready for gate | Phase 5; generic finite represented compression, Action/result ownership, invariant-restriction versus Ritz versus downfolding boundaries, unit/dimension tests, and canonical operator pages are reconciled. |
| `PERIODIC-XWALK-028` | Implemented | Ready for gate | Phases 5 and 7; the general immutable dense represented record, state-space/basis/geometry/energy/provenance metadata, non-Hermitian scope, separate Actions, class-facet tests, and canonical operator pages are reconciled. |
| `PERIODIC-XWALK-029` | Implemented | Ready for gate | Phase 5; the specialized sparse scalar finite-periodic representation, shape/twist/gauge/basis/unit/energy/provenance contract, PhysKit dependency direction, short delegated invariants, documented tests, and canonical `solidstate` pages are reconciled. |
| `PERIODIC-XWALK-030` | Blocked | Blocker documented | Phase 5; requires explicit cell vectors, ordered state labels, and structured provenance for lossless replacement. |
| `PERIODIC-XWALK-031` | Blocked | Blocker documented | Phase 5; requires a parent-qualified request with stable parent-model, operator, and state-space identities. |
| `PERIODIC-XWALK-032` | Blocked | Blocker documented | Phase 5; requires the same parent identities while preserving half-open grid and Bloch-seam conventions. |
| `PERIODIC-XWALK-033` | Implemented | Ready for gate | Phase 7; general 2D plane-wave definition/request/Action/result ownership, PhysKit geometry, units, reduced-coordinate and basis ordering, transfer convention, duality evidence, documented software/numerical tests, and canonical pages are reconciled. |
| `PERIODIC-XWALK-034` | Implemented | Ready for gate | Phase 7; the cosine request/Action/result adapter preserves exact parent/request identity and duality evidence while delegating the only plane-wave assembly algorithm; documented analytic and negative tests and canonical pages are reconciled. |
| `PERIODIC-XWALK-035` | Implemented | Ready for gate | Phase 7; the authorized reusable finite-difference basis/model/request/Action/result contract makes coordinate geometry, Euclidean normalization, grid order, directed seams, unit, kinetic scale, energy reference, represented identities, immutable samples, provenance, binary64 range failures, and dense-resource behavior explicit; the cosine adapter delegates the only assembly algorithm and exact matrix-preservation, class-facet invariant/range tests, analytic-entry evidence, Sphinx, link, and canonical-page gates pass. |
| `PERIODIC-XWALK-036` | Implemented | Ready for gate | Phase 7; exact adapter compatibility, basis-column-distinct sampling, proper-rectangular versus square-unitary map branches, directional basis order, intrinsic `T^dagger H_fd T` transport correlation, signed difference, unit/shape/range failures, all diagnostics, Action/Result boundary, documented software/numerical evidence, specification, Sphinx, and canonical architecture pages are reconciled. |
| `PERIODIC-XWALK-037` | Implemented | Audit required | Phase 3; audit isolated-band encoded-document rename and exact-byte preservation. |
| `PERIODIC-XWALK-038` | Implemented | Audit required | Phase 3; audit composite encoded-document rename and exact-byte preservation. |
| `PERIODIC-XWALK-039` | Implemented | Audit required | Phase 3; audit reduction-challenge terminology and exact-byte preservation. |
| `PERIODIC-XWALK-040` | Implemented | Audit required | Phase 3; audit Wannier90 encoded/native-artifact split and identity preservation. |
| `PERIODIC-XWALK-041` | Implemented | Audit required | Phase 3; audit blind-alignment bytes versus request-owned repository location. |
| `PERIODIC-XWALK-042` | Implemented | Audit required | Phase 3; audit continuum-refinement bytes versus request-owned repository location. |
| `PERIODIC-XWALK-043` | Implemented | Audit required | Phase 3; audit finite-rank-oracle bytes versus request-owned repository location. |
| `PERIODIC-XWALK-044` | Implemented | Audit required | Phase 3; audit route-reconciliation bytes versus request-owned repository location. |
| `PERIODIC-XWALK-045` | Implemented | Audit required | Phase 3; audit encoded-result kind, serializer, retired names, and byte/digest preservation. |
| `PERIODIC-XWALK-046` | Implemented | Audit required | Phase 3; audit 2D isolated-band encoded-document rename. |
| `PERIODIC-XWALK-047` | Implemented | Audit required | Phase 3; audit 2D composite encoded-document rename. |
| `PERIODIC-XWALK-048` | Implemented | Audit required | Phase 3; audit 2D topological encoded-document rename. |
| `PERIODIC-XWALK-049` | Implemented | Audit required | Phase 3; audit phase-sweep encoded-document rename. |
| `PERIODIC-XWALK-050` | Implemented | Audit required | Phase 3; audit balanced-Wannier90 encoded-document rename. |
| `PERIODIC-XWALK-051` | Implemented | Audit required | Phase 3; audit Wannier90-study encoded-document rename. |
| `PERIODIC-XWALK-052` | Implemented | Audit required | Phase 3; audit optimizer-basin encoded-document rename. |
| `PERIODIC-XWALK-053` | Implemented | Audit required | Phase 3; audit optimizer-reanalysis encoded-document rename. |
| `PERIODIC-XWALK-054` | Implemented | Audit required | Phase 3; audit optimizer-regression encoded-document rename. |
| `PERIODIC-XWALK-055` | Implemented | Audit required | Phase 3; audit optimizer-standalone encoded-document rename. |
| `PERIODIC-XWALK-056` | Implemented | Audit required | Phase 3; audit existing isolated-band result-document ownership. |
| `PERIODIC-XWALK-057` | Implemented | Audit required | Phase 3; audit existing defect result-document ownership and paths. |
| `PERIODIC-XWALK-058` | Pending | Not implemented | Phase 5; move the isolated-band campaign family to canonical 1D campaign ownership. |
| `PERIODIC-XWALK-059` | Pending | Not implemented | Phase 5; move the composite campaign family with explicit retention objects. |
| `PERIODIC-XWALK-060` | Pending | Not implemented | Phase 5; rename/move the reduction-challenge campaign while preserving wire identities. |
| `PERIODIC-XWALK-061` | Pending | Not implemented | Phase 5; move the 1D Wannier90 campaign behind integration-owned native artifacts. |
| `PERIODIC-XWALK-062` | Pending | Not implemented | Phase 5; move the blind-alignment family while keeping alignment Actions separate. |
| `PERIODIC-XWALK-063` | Pending | Not implemented | Phase 5; move continuum refinement with explicit continuum/lattice embedding. |
| `PERIODIC-XWALK-064` | Pending | Not implemented | Phase 5; move the finite-rank-oracle family without redefining general retention. |
| `PERIODIC-XWALK-065` | Pending | Not implemented | Phase 5; move matched extraction only after row 030 supplies a lossless represented-operator route. |
| `PERIODIC-XWALK-066` | Pending | Not implemented | Phase 5; move route reconciliation with explicit route identities and compatibility prerequisites. |
| `PERIODIC-XWALK-067` | Pending | Not implemented | Phase 7; decompose the 2D isolated-band campaign and replace encoded-model terminology. |
| `PERIODIC-XWALK-068` | Pending | Not implemented | Phase 7; introduce typed scientific results before retiring the composite adapter. |
| `PERIODIC-XWALK-069` | Pending | Not implemented | Phase 7; decompose topological observations without treating them as expected-result oracles. |
| `PERIODIC-XWALK-070` | Pending | Not implemented | Phase 7; decompose the phase sweep with explicit unavailable outcomes. |
| `PERIODIC-XWALK-071` | Pending | Not implemented | Phase 7; move 2D Wannier90 campaigns behind integration-owned native adapters. |
| `PERIODIC-XWALK-072` | Pending | Not implemented | Phase 7; decompose optimizer campaigns while retaining campaign-owned optimization policy. |
| `PERIODIC-XWALK-073` | Pending | Not implemented | Phase 8; remove `Periodic2DCampaign` only after all ten concrete consumers are independent. |

## Reconciled totals

| Status | Count | Rows |
|---|---:|---|
| Implemented dispositions | 52 | `001–012`, `014`, `016–029`, `033–057` |
| Blocked dispositions | 3 | `030–032` |
| Pending dispositions | 18 | `013`, `015`, `058–073` |
| Documentation ready for current gate | 31 | `001–012`, `014`, `016–029`, `033–036` |
| Earlier implementation requiring dossier audit | 21 | `037–057` |

The totals describe migration state only. They do not establish scientific validation or
completion of phase 6.

## Non-row program gate

Phase 6 remains pending even though row 009's catalog DataObject is implemented. The
program still requires an explicit immutable catalog snapshot populated only with
migrated toy models and one campaign that consumes that snapshot while representing
incompatible or unavailable observations explicitly.
