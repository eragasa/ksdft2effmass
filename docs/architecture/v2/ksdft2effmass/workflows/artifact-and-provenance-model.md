# Artifact and provenance model

## ArtifactManifest

`ArtifactManifest` is the portable immutable inventory for artifacts produced, consumed, or referenced by a scientific operation. Each entry records stable artifact identity; checksum algorithm and digest; byte count; media or native format; semantic role; parent artifact identities; retention classification; optional portable store reference; and exactly one immutable tagged `ArtifactProducerProvenance` variant. The tag is mandatory: null, absent, multiple, contradictory, or inferred producer provenance rejects manifest closure.

Absolute user-specific paths, credentials, scheduler clients, process handles, and open files are not portable manifest content.

## Closed producer-provenance variants

All variants share artifact identity, observed `ContentIdentity`, checksum algorithm/digest, byte count, provenance-variant identity/version, and evidence/claim-boundary identities. Shared identities must agree with the enclosing manifest entry and observed bytes. Fields listed for another variant are prohibited rather than ignored.

| Variant | Required fields | Prohibited or bounded fields |
|---|---|---|
| `RepresentedWorkflowProducer` | Exact applicable `WorkflowIdentity`, `WorkflowRunIdentity`, producing `TaskInstanceIdentity`, `TaskActivationIdentity`, `AttemptIdentity`, produced `ResultObjectIdentity`, exact result/artifact relation, and content identity | No external-observation, fixture-import, human-authorship, or unknown-legacy fields; applicable Workflow/Task identities may not be omitted or invented |
| `ExternalSourceObservation` | Authoritative external producer identity; producer attempt identity; exact externally produced artifact and/or result identity; source-observation identity and revision/time when known; observation method/receipt; observed content identity; explicit limitations/claim boundary | Workflow, WorkflowRun, Task-instance, and TaskActivation identities may be unavailable only when the producer is genuinely outside a Workflow; none may be fabricated, and the authoritative external producer/attempt/artifact-or-result identities remain mandatory |
| `ImportedRetainedFixture` | Fixture identity/revision, source identity/reference, import identity/receipt, retained source/content/checksum/provenance identities, and evidence classification | No fabricated workflow producer; import does not upgrade the retained source's evidence or claim status |
| `HumanAuthoredCompactInput` | Compact-input identity/revision, identified author or authorship authority, source/review identity as applicable, authorship record, and content identity | No fabricated workflow run/request/result; authorship is not calculator execution or scientific validation |
| `UnknownLegacyProducer` | Nonempty reason, identities/references for every item of known evidence, explicit limitations, bounded claim status, and claim boundary | No inferred or fabricated producer identity; it may not claim more than known evidence or be upgraded by inference |

A field described as applicable is governed by the selected variant's versioned contract, not caller preference. `RepresentedWorkflowProducer` requires the exact applicable Workflow, WorkflowRun, producing Task instance, TaskActivation, attempt, and produced ResultObject identities. An `ExternalSourceObservation` for a genuine non-Workflow producer explicitly records Workflow/run/task/activation identities as unavailable while still requiring authoritative external producer identity, producer attempt, and exact artifact and/or result identity. External observations identify what source was observed and which bytes were observed without pretending that source participated in this Workflow. Imported fixtures preserve their fixture, source, checksum, content, and provenance identities. Human-authored compact inputs record actual identified authorship without inventing execution. Unknown legacy provenance remains explicitly limited.

Missing required fields, inapplicable populated fields, contradictory identities, checksum/content mismatch, or an unclosed evidence reference rejects the manifest. A correction creates a new immutable manifest revision with predecessor/supersession identity; it never rewrites history, fills unknowns by inference, or fabricates provenance.

## Lineage

For `RepresentedWorkflowProducer`, lineage connects `Workflow`, `WorkflowRun`, identified colored-Petri-net selection, `TaskActivation`, the exact producing Task instance, exact execution grant/snapshot where applicable, the exactly correlated immutable `ResultObject`, native artifact resolution, mechanically faithful parser records, normalization policy/version, `NormalizedObservationSet`, and `ScientificAnalysis`. Every edge is explicit and identity-correlated.

The other producer variants enter lineage at their declared source, fixture, authorship, or legacy evidence boundary. They need not and must not be rewritten as `WorkflowRun` history. Downstream consumption references the exact manifest entry and producer-provenance variant. Exact byte identity does not imply scientific compatibility, and compatible semantics do not imply identical bytes. Pseudopotentials, canonical native input bytes, and other exact external inputs remain content-identified manifest entries with their actual closed producer provenance. A concrete calculator input references those entries directly rather than reconstructing them from generic tags.

Shared labels, nominal methods, elements, cutoffs, or settings across calculators do not establish equivalence. PAW, ultrasoft, and norm-conserving assets; valence/core choices; generation settings; exchange-correlation compatibility; relativistic treatment; projector construction; recommended cutoffs; and file formats remain exact represented inputs. Any cross-calculator or model equivalence is a separately evidenced comparison or validation claim, not a property conferred by artifact identification or resolution.

Normalization starts only after reconciliation confirms the dispatch envelope and `TaskResultIngester` admits and commits the returned concrete ResultObject, or after an external/imported/human-authored/legacy input has passed its applicable manifest and intake contracts. For QE the mechanical path starts from admitted calculator-owned `QuantumEspressoOutput` → integration-owned native artifact resolver → integration-owned `QuantumEspressoOutputParser` and/or `QuantumEspressoXsdDocumentParser` → integration-owned `QuantumEspressoObservationAdapter` → workflow-owned `NormalizedObservationSet` → `ScientificAnalyzer`; neither raw process state nor a native record bypasses that order.

## Existing calculations and no-recalculation migration

Existing calculation artifacts remain retained under their actual evidence class as `ExternalSourceObservation`, `ImportedRetainedFixture`, or, when provenance is incomplete, `UnknownLegacyProducer`. Entries use actually available checksums, software/settings records, provenance records, and explicit limitations. Architecture v2 migration and manifest conformance do not require rerunning an existing calculation, rewriting it as a `WorkflowRun`, or inventing workflow identities merely to retain, import, compare, or continue using it within its declared evidence class. A prospective `QuantumEspressoInput` can reference existing exact QE input bytes and pseudopotential artifacts under their actual identities and provenance without rendering, conversion, registration, rerun, or evidence reclassification. The implemented `QePwInputFile` and `QePwInputFileWriter` represent and write grouped native input only; they do not define or duplicate provenance records.

A future new execution is optional, separately tasked, protected, and subject to exact authority; it is not a migration completion condition. Historical/bootstrap artifacts are not elevated to a calculated canonical Workflow result or stronger scientific evidence without supporting provenance.

## Retention

Retention metadata describes expected handling but grants no deletion authority. The target classifications distinguish at least authoritative compact input or result, retained verification fixture, reconstructible scratch, externally retained native artifact, and publication candidate subject to separate authority.

Large wavefunctions, densities, restart trees, and dense matrices remain outside Git. Compact manifests, exact inputs, available checksums, software identities, settings, provenance records, and explicit limitations remain version controlled where permitted.

## Result ownership

A concrete Task returns its concrete immutable `ResultObject`; `QuantumEspressoSimulationTask` returns `QuantumEspressoOutput`. The ResultObject carries its exact type-specific mechanical observations and references generated artifacts. Its represented producer provenance binds the exact applicable Workflow, WorkflowRun, producing Task instance, TaskActivation, attempt, and produced ResultObject identities. Exactly one confirmed dispatch envelope correlates that returned ResultObject to one request, activation, attempt, executor, grant, and obligation.

A no-Task `ScientificDecisionResolution` is not an artifact and does not use `ArtifactProducerProvenance`. Its closed `RepresentedScientificDecisionIngressProducer` ResultObject-provenance variant instead binds the exact Workflow, WorkflowRun, `ScientificDecisionRequest`, scientific-decision-origin transition, recorder implementation/version, direct trusted-boundary response-source and authority-context, and produced resolution identities. Task instance, TaskActivation, attempt, and Task result-production identities are prohibited. Any available trusted-boundary receipt is retained only as direct supporting evidence; Architecture v2 requires no standalone response snapshot, verifier, receipt store, or registration subsystem.

`ScientificAnalysis` references the exact workflow-owned normalized-observation set and states algorithms, units, tolerances, findings, limitations, evidence, and claim boundary. Human-reviewed scientific conclusions remain in applicable research records citing exact analysis and provenance identities; they are not WorkflowRun disposition state.

## Native outputs and extraction

An external calculator writes native output files in its exact execution workspace or configured external output location as part of the calculator effect. Workflow result ingress does not publish, copy, relocate, or register those files in a second artifact store. The confirmed calculator ResultObject and `ArtifactManifest` retain their exact identities, locations or portable references where applicable, content identities, producer provenance, and observed limitations.

After dispatch reconciliation, workflow control constructs the candidate generic `TaskInvocationOutcome` correlated to the exact specialized outcome. For confirmed work, `TaskResultIngester` consumes the confirmed `SimulationDispatchOutcome` and candidate generic outcome, validates their request/Task-instance/TaskActivation/attempt/executor/ResultObject correlations, and atomically admits the concrete ResultObject, manifest references, generic outcome, and result transition.

Extraction is a separate read-only transformation over identified native outputs. The Workflow definition supplies an immutable versioned extraction specification identifying the requested native sources and record families. Integration-owned artifact resolvers and parsers read those exact files and return closed extracted records or structured unavailable/rejected/indeterminate outcomes. They never infer an absent output, mutate the native files, or turn extraction into artifact publication. A later requirement to copy or transfer native files would be a separately authorized artifact-transfer contract, not implicit result ingress.

## Privacy and integrity

Environment capture is allowlisted and sanitized. Secrets, private keys, tokens, restricted data, and unrestricted environment mappings are forbidden. Missing, conflicting, inapplicable, or unclosed identity, lineage, producer-provenance, or manifest fields produce a structured failure and stop dependent colored-Petri-net transitions.

## Deferred implementation details

- Exact extraction-specification and extracted-record wire forms.
- Canonical portable native-output reference representation.
- Retention-classification vocabulary and lifecycle transitions.
- Access control for restricted or unpublished native outputs.
- Content-identity algorithm agility and very-large-artifact verification.
