# Human decisions

This page defines the Architecture v2 contract for explicit human-decision inputs. The public development-decision records, strict canonical wire, source provenance, and one-way legacy adaptation are implemented under `ksdft2effmass.harness`; their composition into the future complete `HarnessState` remains prospective. Scientific-decision records and recording remain prospective. Record processing is deterministic. A harness can wait for an explicit external response without treating response timing as a selection mechanism.

## Domain separation

Development decisions and scientific decisions are two domain-separated systems. They have no common nominal checkpoint base, shared aggregate, or shared repository. Neither family can authorize or mutate the other. Their records preserve what a human declared; they do not themselves grant authority, authorize protected execution, or establish scientific acceptance or validity.

| Domain | Records and action | Aggregate and persistence |
|---|---|---|
| Development | One immutable `DevelopmentDecision` model, with unresolved and resolved variants/revisions | `HarnessState` and development persistence |
| Scientific | `ScientificDecisionRequest`, `ScientificDecisionResolution`, and `ScientificDecisionRecorder` | Request and resolution records in `WorkflowRun` and workflow persistence |

A separate grant may reference the decision that justified it when needed. The decision need not reciprocally reference the grant. Development authority remains separate from scientific execution authority.

## Development decisions

`DevelopmentDecision` covers human-owned development architecture, dependencies, scope, protected repository operations, review, and acceptance. An unresolved variant preserves the exact request, question, offered options, declared scope, source identity, and authority identity. A resolved variant or successor revision additionally preserves the verbatim response and one normalized declared outcome when the response matches unambiguously. It records predecessor and supersession identities where applicable.

An ambiguous response, no matching response, or conflicting response does not resolve the decision. A pending decision blocks only its declared development transition and scope. Silence, elapsed time, passing checks, or reviewer agreement is not a response. Histories are immutable and append-only: correction creates a predecessor/supersession revision rather than mutating an earlier record.

No additional development request, resolution, obligation, result class, or decision-specific public ActionObject is part of this v2 contract. `HarnessState` contains `DevelopmentDecision` values directly as one immutable canonically ordered sequence; each value owns its intrinsic field and variant invariants, while normalization and `HarnessStateValidator` own cross-record identity uniqueness, references, and canonical ordering. `DevelopmentDecision` remains within the complete `HarnessState`; `HarnessStateAtomicRepository` invokes its bound transaction validator and serializer on the exact supplied candidate, binds the resulting bytes and identities, and commits only after those checks. It neither interprets a response nor creates a decision.

## Scientific decisions

`ScientificDecisionRequest` is an immutable `WorkflowRun` record. It preserves the exact request, question, offered options, declared scope, affected Workflow, Task, run, and transition identities, and the authority and source identities for the requested response. Together with the identified Workflow definition, it identifies exactly one decision-ingress transition, its selected binding inputs, and the resolution-to-generic-value mapping. The unresolved request itself pauses only the affected workflow branch. It does not require a decision Task, TaskActivation, attempt, obligation, checkpoint scheduler, prompt service, registry, catalog, or plugin system.

`ScientificDecisionResolution` is an immutable `ResultObject`. It preserves the exact request identity, verbatim response, exactly one normalized declared outcome, direct response-source and authority-context identities, its closed scientific-decision-ingress producer provenance, and predecessor and supersession identities where applicable.

`ScientificDecisionRecorder` is the sole named new scientific-decision `ActionObject`. It is invoked only through an application-owned trusted boundary that has already identified the response source and authority context. The recorder receives the exact predecessor `WorkflowRun` and revision, the exact request, the explicit verbatim response, those direct trusted-boundary identities, any boundary receipt reference that is actually available, and the request-identified decision-ingress transition and selected-binding inputs. It does not authenticate a raw transport message or require a separate response-snapshot, verifier, registry, or receipt subsystem. It requires the supplied source and authority-context identities to satisfy the request, rejects an unavailable required identity, and validates one unambiguous option match. It then constructs `ScientificDecisionResolution`, asks the existing effect-free `ColoredPetriNetWorkflowAdapter` to map that supplied resolution through the request-identified mapping into the generic external-output-value binding, obtains pure generic firing for the exact decision-ingress transition, constructs the complete scientific-decision-origin `WorkflowTransitionRecord` and `WorkflowRun` successor transaction, and submits that transaction to `WorkflowRunRepository`.

Only a successful atomic commit returns the recorded `ScientificDecisionResolution`. Ambiguity, no match, source or authority mismatch, stale correction predecessor, pure-firing failure, or persistence failure produces no resolution or generic token. `WorkflowRunAtomicRepository` invokes its bound transaction validator and serializer on the exact supplied candidate and commits only the identity-bound bytes; it does not interpret a response or create either record. Exact authentication mechanisms, trusted-boundary integration, error forms, and wire representations remain deferred. This v2 contract prohibits another public scientific-decision ActionObject or result-wrapper type.

## Workflow token flow and replay

After successful recording, the exact typed `ScientificDecisionResolution` is available as a `ResultObject` and its scientific-decision-origin transition is already part of the committed ordered history. The effect-free `ColoredPetriNetWorkflowAdapter` maps the supplied resolution value for the exact request-identified decision-ingress transition; it does not prompt, authenticate, interpret or record a decision, create authority, or construct the workflow record. No Task, TaskActivation, or attempt exists for this transition. `ksdft2effmass.petrinet.colored` remains unaware of humans, checkpoints, decisions, workflow, and authority.

The marking carries exactly one decision-state token for the request at this boundary: initially unresolved, then containing the one effective resolution. A correction is another invocation through the same trusted boundary. It identifies the exact effective predecessor resolution, creates one immutable successor that names and supersedes that predecessor, and atomically fires the request-identified ingress transition by consuming the predecessor decision-state token and producing the successor token. Downstream transitions read rather than consume the effective decision token. A stale predecessor or competing correction conflicts and produces no successor. Exact idempotent replay of the same bound commit returns its original committed revision; reuse of that idempotency identity with different response, evidence, resolution, or bytes conflicts.

Replay consumes the committed ordered records and never prompts or reauthenticates. It reproduces the initial resolution token, every historical read, and each later consume-and-replace correction, so the reconstructed current marking contains exactly the recorded effective successor. Earlier resolutions and transitions that read them remain immutable history: correction changes future effective decision state but does not erase, reinterpret, compensate, or authorize reversal of downstream work. If the resolution is absent or the supplied response is ambiguous, unmatched, conflicting, or untrusted at the application boundary, the affected branch remains blocked and replay produces no resolution token.

## Implementation and deferred details

The implemented development surface is `DevelopmentDecision`,
`DevelopmentDecisionOption`, `DevelopmentDecisionSourceProvenance`, and
`DevelopmentDecisionSerializer`, exported from `ksdft2effmass.harness`. Its version-1
wire requires explicit nulls, exact source-byte provenance, and append-only successor
references. Aggregate loading, canonical sequence normalization, cross-record closure,
and persistence remain with the future `HarnessState` compiler, validator, and
repository.

For scientific decisions, exact public fields, trusted-boundary authentication
integration, optional receipt representation, error representations, and wire
encodings remain deferred; another public scientific-decision result type is
prohibited.
