# Human decisions

This page defines the Architecture v2 contract for explicit scientific-decision
inputs. A decision record preserves what a human declared; it does not itself grant
authority, authorize protected execution, or establish scientific acceptance or
validity. Silence, elapsed time, process success, passing checks, and reviewer
agreement are not human responses.

## Scientific decisions

`ScientificDecisionRequest` is an immutable `WorkflowRun` record. It preserves the
exact request, question, offered options, declared scope, affected Workflow, Task,
run, and transition identities, and the source and authority-context identities
required for the response. Together with the identified Workflow definition, it
identifies one decision-ingress transition, its selected binding inputs, and the
resolution-to-generic-value mapping. An unresolved request pauses only the affected
workflow branch.

`ScientificDecisionResolution` is an immutable `ResultObject`. It preserves the
request identity, verbatim response, one unambiguous normalized outcome, direct
response-source and authority-context identities, scientific-decision-ingress
provenance, and predecessor and supersession identities where applicable.

The prospective `ScientificDecisionRecorder` is the sole scientific-decision
`ActionObject`. An application-owned response-source boundary supplies the exact
predecessor `WorkflowRun` and revision, request, verbatim response, source and
authority-context identities, any available boundary receipt reference, and the
request-identified transition inputs. The recorder rejects ambiguity, no match,
identity mismatch, stale correction, firing failure, and persistence failure. Only
a successful atomic commit returns a recorded resolution.

## Workflow token flow and replay

After successful recording, the typed resolution is available as a `ResultObject`
and its scientific-decision-origin transition is part of committed ordered history.
The effect-free `ColoredPetriNetWorkflowAdapter` maps the supplied value for the
request-identified transition; it does not prompt, authenticate, interpret, record,
or authorize a decision. `ksdft2effmass.petrinet.colored` remains unaware of human
decisions and authority.

A correction names and supersedes the exact effective predecessor resolution. The
request-identified transition consumes the predecessor decision-state token and
produces the successor token atomically. A stale predecessor or competing correction
produces no successor. Replay consumes committed ordered records without prompting
or reauthentication and reconstructs the recorded effective decision state without
erasing earlier history.

Exact response-source integration, optional receipt representation, public error
forms, and wire encodings remain deferred where their owning Workflow contracts do
not already define them.
