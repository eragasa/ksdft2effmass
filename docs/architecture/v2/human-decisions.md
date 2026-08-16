# Human decisions

This page defines the prospective, unimplemented Architecture v2 contract for explicit human-decision inputs. Record processing is deterministic. A harness can wait for an explicit external response without treating response timing as a selection mechanism.

## Domain separation

Development decisions and scientific decisions are two domain-separated systems. They have no common nominal checkpoint base, shared aggregate, or shared repository. Neither family can authorize or mutate the other. Their records preserve what a human declared; they do not themselves grant authority, authorize protected execution, approve a scientific disposition, or establish acceptance or scientific validity.

| Domain | Records and action | Aggregate and persistence |
|---|---|---|
| Development | One immutable `DevelopmentDecision` model, with unresolved and resolved variants/revisions | `HarnessState` and development persistence |
| Scientific | `ScientificDecisionRequest`, `ScientificDecisionResolution`, and `ScientificDecisionRecorder` | Request and resolution records in `WorkflowRun` and workflow persistence |

A separate grant may reference the decision that justified it when needed. The decision need not reciprocally reference the grant. Development authority remains separate from scientific execution and disposition authority.

## Development decisions

`DevelopmentDecision` covers human-owned development architecture, dependencies, scope, protected repository operations, review, and acceptance. An unresolved variant preserves the exact request, question, offered options, declared scope, source identity, and authority identity. A resolved variant or successor revision additionally preserves the verbatim response and one normalized declared outcome when the response matches unambiguously. It records predecessor and supersession identities where applicable.

An ambiguous response, no matching response, or conflicting response does not resolve the decision. A pending decision blocks only its declared development transition and scope. Silence, elapsed time, passing checks, or reviewer agreement is not a response. Histories are immutable and append-only: correction creates a predecessor/supersession revision rather than mutating an earlier record.

No additional development request, resolution, obligation, result class, or decision-specific public ActionObject is part of this v2 contract. `HarnessState` contains `DevelopmentDecision` values directly as one immutable canonically ordered sequence; each value owns its intrinsic field and variant invariants, while normalization and `HarnessStateValidator` own cross-record identity uniqueness, references, and canonical ordering. `DevelopmentDecision` remains within the complete `HarnessState`; `HarnessStateRepository` commits a supplied validated state revision and neither interprets a response nor creates a decision.

## Scientific decisions

`ScientificDecisionRequest` is an immutable `WorkflowRun` record. It preserves the exact request, question, offered options, declared scope, affected Workflow, Task, run, and transition identities, and the authority and source identities for the requested response. Together with the identified Workflow definition, it identifies exactly one decision-ingress transition, its selected binding inputs, and the resolution-to-generic-value mapping. The unresolved request itself pauses only the affected workflow branch. It does not require a decision Task, TaskActivation, attempt, obligation, checkpoint scheduler, prompt service, registry, catalog, or plugin system.

`ScientificDecisionResolution` is an immutable `ResultObject`. It preserves the exact request identity, verbatim response, exactly one normalized declared outcome, provenance, and predecessor and supersession identities where applicable.

`ScientificDecisionRecorder` is the sole named new scientific-decision `ActionObject`. It receives the exact predecessor `WorkflowRun` and revision, the exact request, the explicit verbatim response, and the request-identified decision-ingress transition and selected-binding inputs. It correlates the response to the request and validates source and authority identities and one unambiguous option match. It then constructs `ScientificDecisionResolution`, asks the existing effect-free `ColoredPetriNetWorkflowAdapter` to map that supplied resolution through the request-identified mapping into the generic external-output-value binding, obtains pure generic firing for the exact decision-ingress transition, constructs the complete scientific-decision-origin `WorkflowTransitionRecord` and `WorkflowRun` successor transaction, and submits that transaction to `WorkflowRunRepository`.

Only a successful atomic commit returns the recorded `ScientificDecisionResolution`. Ambiguity, no match, conflict, pure-firing failure, or persistence failure produces no resolution or generic token. The repository only checks and commits the supplied validated unit; it does not interpret a response or create either record. Exact error and wire representations remain deferred. This v2 contract prohibits another public scientific-decision ActionObject or result-wrapper type.

## Workflow token flow and replay

After successful recording, the exact typed `ScientificDecisionResolution` is available as a `ResultObject` and its scientific-decision-origin transition is already part of the committed ordered history. The effect-free `ColoredPetriNetWorkflowAdapter` maps the supplied resolution value for the exact request-identified decision-ingress transition; it does not prompt, interpret or record a decision, create authority, or construct the workflow record. No Task, TaskActivation, or attempt exists for this transition. `ksdft2effmass.petrinet.colored` remains unaware of humans, checkpoints, decisions, workflow, and authority.

Replay consumes the recorded resolution and never prompts again. If the resolution is absent or the supplied response was ambiguous, unmatched, or conflicting, the affected branch remains blocked and replay produces no resolution or token. Scientific request and resolution histories are immutable and append-only within `WorkflowRun`; correction uses predecessor and supersession identities.

## Status and deferred details

This is a prospective documentation contract, not an implemented capability or implementation authorization. Exact public fields, error representations, and wire encodings remain deferred; another public scientific-decision result type is prohibited. This page grants no development authority, protected-execution authority, scientific-disposition authority, acceptance, calculation, software or numerical verification, scientific validation, or uncertainty-quantification claim.
