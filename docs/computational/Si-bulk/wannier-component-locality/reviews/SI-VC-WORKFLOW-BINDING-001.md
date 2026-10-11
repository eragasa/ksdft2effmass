# SI-VC workflow-binding exact-digest review 001

## Record metadata

| Field | Value |
|---|---|
| Review ID | `SI-VC-WORKFLOW-BINDING-001` |
| Record status | Complete technical design review |
| Review scope | Exact-digest owner/provider/consumer architecture consistency |
| Review outcome | `NO_BLOCKING_FINDINGS` |
| Operator request | `NONE` |
| Implementation readiness | Not established; retained blockers remain |
| Scientific acceptance | Not assessed or granted |
| Execution authorization | Not granted |
| Record revision | Git commit containing this file |

This record binds one immutable cross-repository design candidate without placing
reciprocal future digests inside the owner, consumer, or provider documents. It
records technical design consistency only. It is not contract acceptance,
implementation evidence, migration approval, dependency authorization,
calculator authority, scientific validation, publication approval, or release
approval.

## Definition of done

The bounded review asked whether the exact retained owner, consumer, lineage,
and provider documents agree on:

- canonical CPN identity layers and `Cpn*` vocabulary;
- bounded control records, field projection, record construction, and the frozen
  SNAKES expression-translation route;
- flat parent and child topology ownership without copied child topology;
- child-export, plan, run, occurrence, attempt, terminal, companion, and delivery
  correlation;
- provider candidacy versus Si-VC acceptance;
- exact bounded cancellation and reconciliation containment;
- staging-receipt identity, acyclic receipt ordering, and the pre-dispatch
  receipt barrier;
- unchanged-Slice-A-first replay and effect-free pure CPN replay;
- quiescence with no unresolved child, attempt, process, cancellation,
  companion-production, delivery, ambiguity, invalid evidence, or partial
  application; and
- non-authorization and evidence-boundary language.

The review did not ask whether any prospective API exists or whether the design
has been implemented, executed, numerically verified, scientifically validated,
or accepted for production.

## Exact candidate

| Owner | Repository path | Git commit | SHA-256 | Lines | Bytes |
|---|---|---|---|---:|---:|
| Generic Workflow | `docs/contracts/workflow-cpn-bindings.md` | `9ec0944dad3af1706edf01101e443e244da22ef5` | `e6428a8b0d8a47d4f9a6596300fe5ccc65bb16c12e1cc8ffe64884720bd513c2` | 1387 | 74593 |
| Si-VC consumer profile | `docs/computational/Si-bulk/wannier-component-locality/workflow-binding.md` | `9ac2363908fca665fef29b5add5a334a69d98180` | `e3496191b7299b2bdba11ba3ca4679a0eb80a421bd076eac1a7a8fdc3344dd06` | 618 | 32110 |
| Si-VC lineage contract | `docs/computational/Si-bulk/wannier-component-locality/scf-saved-state-lineage.md` | `9ac2363908fca665fef29b5add5a334a69d98180` | `639daaf0a6a316b269f556e5a5aae35ce11c7a38f7c265b1178e25a98ef6313c` | 545 | 25971 |
| Simulations provider | `docs/architecture/projectkoios/simulations/workflows/pw_dft_scf/cpn/provider-binding.md` | `b6995de15dd44067c55d9055735d26b11b80e712` | `adfa47ba9007e3b08b02d219bf5d7b29de28a48531876c79559a510fc5484858` | 941 | 50979 |

Repository ownership remains separate:

- Generic Workflow owns the first document;
- `ksdft2effmass` owns the two Si-VC documents and this review record; and
- `projectkoios-simulations` owns the provider document.

The digest graph is intentionally one-way: the consumer binds the already-derived
owner identity, the provider binds the already-derived owner and consumer
identities, and this later review record binds all four documents. No candidate
document embeds its own digest or the future digest of a downstream document.

## Resolved review findings

### Finding 1 — exact candidate and vocabulary

**Disposition: NO_ACTION_REQUIRED**

Superseded owner, provider, and consumer digests are no longer presented as the
current tranche. The consumer uses `CpnDefinitionIdentity`; historical reviews
remain attributable only to their historical bytes. The exact candidate is the
table above.

### Finding 2 — terminal companion and child-export correlation

**Disposition: NO_ACTION_REQUIRED**

The owner defines classification-specific primary and companion requirements,
canonical ordering, correlation, durable delivery, replay, ambiguity, and
quiescence. The provider candidate contains exact `child_export_identity`; the
consumer accepted-parent contract copies and verifies it. Wrong-export and
tamper vectors fail closed.

### Finding 3 — cancellation capability

**Disposition: NO_ACTION_REQUIRED**

The unchanged SCF child declares no cancellation port, no definition-declared
cancelled terminal classification, and no in-net cancellation. The documents
agree on `CONFIRMED_NOT_APPLIED` operational containment and processing of
`CONFIRMED_APPLIED` through existing event ports. No cancellation token or
parent scientific firing is fabricated.

### Finding 4 — control-record and expression closure

**Disposition: NO_ACTION_REQUIRED**

The owner contract defines bounded immutable control records and the closed
`LITERAL`, `VARIABLE`, `FIELD_PROJECTION`, and
`CONTROL_RECORD_CONSTRUCTOR` expression grammar. The provider selects a
version-pinned `str(Expression)` surface, Python 3.14 evaluation-mode AST parser,
closed node/operator/attribute/constructor whitelist, and deterministic lowering
route. The current scalar shadow kernel is explicitly nonconforming and no
implementation capability is claimed.

### Finding 5 — staging-receipt identity

**Disposition: NO_ACTION_REQUIRED**

The consumer lineage contract derives the staging-receipt payload identity as its
exact prefix plus lowercase SHA-256 of canonical receipt bytes, excludes that
identity from the payload, keeps it distinct from the later six-field Workflow
reference, and requires stable/changed-byte, codec, assembly, admission, and
replay verification.

### Finding 6 — exact companion role

**Disposition: NO_ACTION_REQUIRED**

Consumer and provider use the same evidence role:
`qe-pw-scf-saved-state-candidate-reference`. Success requires exactly one such
post-terminal companion at signed ordinal `0`; known failure declares an empty
companion tuple and zero total.

## Checks and review evidence

The orchestrating review independently reproduced all four SHA-256 values,
line counts, byte counts, and Git commit identities. It also checked:

- every relative link in the four candidate documents resolves;
- no superseded review-target digest remains in the candidate;
- the digest dependency graph is one-way and acyclic;
- exact owner, primary-consumer, lineage, and companion-role values embedded by
  the provider equal the retained upstream bytes;
- `git diff --check` or committed-diff checks pass for each focused change;
- each owner, consumer, lineage, and provider commit contains only its declared
  documentation path or paths; and
- the provider documentation-contract checks report 11 passing tests.

Independent owner-side and provider-side exact-digest reviews both reported
`NO_BLOCKING_FINDINGS` for this final candidate. Reviewer agreement is technical
evidence, not human acceptance or execution authority.

## Retained implementation blockers

The following remain outside this design-consistency outcome and must be resolved
before nested implementation can claim readiness:

1. an immutable path-free saved-state artifact-set contract and complete
   Workflow-correlated path-free success-evidence projection;
2. separately authorized implementation of the canonical control-record,
   parser/lowering, exporter, execution-profile, payload-codec, and runtime
   contracts;
3. generated and independently verified canonical definition, plan, export,
   fixture, and golden-parity bytes;
4. later runtime segments for protected effects, attempt-bound authority,
   persistence, ambiguity, reconciliation, cancellation, companion production,
   delivery, staging, replay, and quiescence; and
5. separately authorized dependency changes, migration, protected calculator
   execution, merge, release, or publication.

A failed or absent implementation is not converted into design inconsistency,
and design consistency is not implementation evidence.

## Change invalidation

Any byte change to one of the four candidate documents, or any changed owner,
consumer, provider, source-topology, SNAKES, schema, codec, parser, grammar,
mapper, correlation, cancellation, staging, replay, or quiescence contract,
invalidates this exact-digest outcome for the changed bytes. A successor review
must retain a new candidate table and must not silently inherit this outcome.

**ReviewOutcome: NO_BLOCKING_FINDINGS**

The exact retained documents are internally aligned for the bounded architecture
design scope.

**OperatorRequest: NONE**

No further human decision is required to record this technical outcome. Any
implementation, dependency change, push, merge, protected execution, release,
or publication requires its own applicable authorization.
