# Quantum ESPRESSO diagnostic outcome and retry decision

The diagnostic, admission, and retry semantics selected here remain accepted. The
later [package-ownership decision](quantum-espresso-package-ownership-decision.md)
supersedes only this page's original placement of QE ResultObject contracts: those
concrete contracts now belong to `ksdft2effmass.integration.quantum_espresso` and
satisfy the backend-neutral `ksdft2effmass.calculators.dft.pw` port.

## Problem

Quantum ESPRESSO communicates completion, warnings, convergence information, and
fatal errors through calculator-defined content that may appear on stdout, stderr,
or native output artifacts. Process exit status and stream choice do not by
themselves establish calculator success. The integration and Workflow architecture
must preserve those independent observations, represent expected calculator failures
without exceptions, and support a later retry only after the reported problem has an
explicit resolution.

The material architecture choice is where QE-specific diagnostic classification
belongs and how its result controls immutable result ingress, CPN state, resolution,
and retry dispatch.

## Observed current behavior

**Implemented fact.** `QuantumEspressoPwResult` and
`QuantumEspressoBandsResult` are immutable operation-specific ResultObjects carrying
mechanical process, diagnostic, native-output, and artifact identities without
convergence or acceptance claims
([QE calculator architecture](quantum-espresso.md)).

**Observed fact.** Generic dispatch is closed as `confirmed`, `rejected`, or
`indeterminate`. Confirmed alone carries a concrete ResultObject, while retry creates
new activation, operation, attempt, request, obligation, and grant identities
([identity, version, and failure contracts](../../identity-version-and-failure-contracts.md)).

**Observed fact.** Retained tutorial observations show that successful QE processes
can emit notices on stderr and that a fatal `c_bands` error can appear on stdout with
a secondary `MPI_ABORT` diagnostic on stderr. The cross-backend architecture already
requires diagnostics to be collected from backend-defined channels rather than
assuming stderr is complete
([cross-backend tutorial examples](../../tutorial-examples.md)).

**Implemented fact.** The active QE integration Task assigns and implements separate
stdout/stderr capture and project failure mapping in
`ksdft2effmass.integration.quantum_espresso`
(`harness/tasks/quantumespresso.simulations.integration.json`).

**Inference.** Process termination, calculator-reported outcome, diagnostic
disposition, native-artifact availability, dependency admission, and scientific
acceptance must remain separate facts. A single success Boolean or exception-first
interface would erase distinctions required by the observed workflows.

## Decision requirements

**Accepted requirement.** Capture stdout and stderr independently, retain their exact
content identities, and preserve ordering within each stream without inventing a
total order across streams.

**Accepted requirement.** Apply QE-specific, executable- and version-bound diagnostic
classification to every calculator-defined diagnostic channel required by the
operation contract. Nonempty stderr alone is neither success nor failure.

**Accepted requirement.** A determinately captured calculator-reported failure is a
typed immutable result. Exceptions and rejected or indeterminate dispatch outcomes
are reserved for integration failures such as spawn, confinement, identity, capture,
or reconciliation failure.

**Accepted requirement.** Unknown, contradictory, or unsupported diagnostics remain
explicitly unresolved and cannot satisfy a downstream dependency.

**Accepted requirement.** Workflow control owns dependency gating and retry control;
the QE integration owns native parsing, diagnostic classification, and calculator
failure mapping.

**Accepted requirement.** Retry is never a mutation or erasure of the failed attempt.
It requires an explicit resolution, new attempt identities, and fresh execution
authority. No diagnostic silently changes an input, setting, executable, or retry
policy.

**Accepted requirement.** A diagnostic reclassification that establishes the
original completed result as admissible permits admission reevaluation without
rerunning QE. A correction to execution context, input, executable configuration, or
scientific settings requires a new execution attempt with exact new identities.

**Human choice resolved.** The human accepted Option A below and clarified that the
Workflow's CPN must represent resolution-gated retry control while the scientific
execution effect remains outside the generic CPN kernel.

## Option A

**Conceptual model**
Each operation-specific QE ResultObject contains distinct process, native-calculator,
diagnostic, artifact, and continuation-state observations. A Workflow-owned CPN
branch represents recovery-required, resolution-admitted, retry-eligible, and
terminal outcomes without performing the external effect.

**Authority**
The architecture fixes fail-closed dependency admission. A version-bound integration
classifier supplies QE-specific diagnostic meaning but grants neither execution
authority nor scientific acceptance. Every new effect requires a fresh applicable
execution grant.

**Ownership/dependency**
Integration-owned immutable QE output contracts satisfy the generic
`ksdft2effmass.calculators.dft.pw` structural port. The integration-owned diagnostic
classifier is an ActionObject. Application composition maps the calculator result to
Workflow-owned generic CPN values; the generic Workflow and CPN packages do not parse
QE text or import the integration package.

**Runtime/dispatch**
The executor captures exact streams, applies the bound diagnostic classifier, and
returns one operation-specific result. Determinate capture of a QE failure is a
confirmed dispatch with a calculator-failure result. The CPN records the failure and
requires an admitted resolution before retry becomes eligible. Workflow control then
creates and authorizes a new dispatch outside the effect-free CPN kernel.

**Implementation status**
The process and operation-output contracts, classification over both stream artifacts,
and deterministic fixtures for successful stderr notices, stdout fatal errors,
secondary stderr diagnostics, and unresolved diagnostics are implemented. Explicit
CPN recovery and resolution-gated retry remain Workflow-owned and are not executed by
the integration.

**Reversibility**
Raw stream and classifier identities remain available. Reclassification produces a
new derived result or assessment without mutating the original attempt. A retried
execution retains and references its failed predecessor while using new identities.

**Failures**
Known calculator failures and unresolved diagnostics are typed results and are not
continuation-eligible. Spawn, confinement, identity, capture, and reconciliation
failures remain rejected or indeterminate dispatch outcomes as applicable. Retry has
an explicit abandon or exhaustion path and no direct failure-to-execution back edge.

**Complexity**
Moderate: one calculator result per attempt, a versioned classifier, and explicit CPN
recovery transitions.

**Maintenance**
Requires a bounded QE program/version diagnostic catalog and exact software-
verification fixtures. Unsupported messages remain unresolved rather than falling
through a permissive default.

**Context-window consequences**
Compact typed diagnostic records and stream identities can guide agents and reviewers
without placing complete native outputs in prompts or maintained prose.

**Future compatibility**
Additional QE executables and versions can add closed classifiers while retaining the
same Workflow recovery semantics. Scheduler or remote execution support can remain a
separate future boundary.

**Advantage**
Keeps QE semantics at the anti-corruption boundary, preserves one Task attempt to one
typed result, and gives the Workflow an explicit auditable retry loop.

**Risk**
An overly broad signature could misclassify output. Exact version binding,
fail-closed unknown handling, and retained raw stream identities are mandatory
mitigations.

## Option B

**Conceptual model**
The executor first returns a purely mechanical QE output. A separate mandatory
integration diagnostic-analysis operation consumes that admitted output and returns a
second diagnostic-assessment ResultObject before the Workflow can continue or retry.

**Authority**
The diagnostic analyzer owns classification; Workflow control owns the assessment
join, resolution state, and fresh execution authority.

**Ownership/dependency**
Mechanical execution and diagnostic analysis are separate integration ActionObjects.
Workflow composition persists both result identities and their dependency.

**Runtime/dispatch**
Every QE Task is followed by a deterministic diagnostic-analysis stage. The CPN waits
for that assessment before selecting continuation, resolution, retry, or terminal
failure.

**Migration**
Preserve after-ingress parsing, then add another result family, transition, persistence
record, replay step, and join for every QE operation.

**Reversibility**
A new classifier can reassess retained streams without changing or rerunning the
original QE Task.

**Failures**
Execution capture failures remain dispatch failures. Calculator failures and
unresolved diagnostics are represented by the second result and block the join.

**Complexity**
High because each calculator Task gains another mandatory result-production and
history step.

**Maintenance**
The separation is explicit, but every Workflow must compose the diagnostic assessment
correctly and consistently.

**Context-window consequences**
Additional result, transition, and correlation records increase retained review
context.

**Future compatibility**
Supports independent evolution and replay of diagnostic classifiers.

**Advantage**
Provides the clearest standalone reclassification history.

**Risk**
Makes essential calculator failure recognition look like optional postprocessing and
complicates the reusable one-Task execution model.

## Option C

**Conceptual model**
The QE integration extracts lossless native diagnostic records without disposition.
Each application or Workflow supplies an explicit immutable policy that maps them to
nonblocking, fatal, or unresolved outcomes and controls recovery.

**Authority**
The supplied Workflow/application policy controls disposition. The integration owns
only extraction.

**Ownership/dependency**
Calculator-layer diagnostic records cross into application composition, which applies
an exact policy. Different Workflows may bind different policy identities.

**Runtime/dispatch**
Captured diagnostics and the selected policy are evaluated together. Missing policy
coverage blocks continuation and retry pending resolution.

**Migration**
Add policy DataObjects, policy identities, evaluators, persistence and replay
bindings, and per-Workflow configuration.

**Reversibility**
The same output can be evaluated under a later policy while retaining every prior
interpretation.

**Failures**
Policy mismatch, unsupported version, or unmatched diagnostics are unresolved.
Calculator failures remain typed results rather than exceptions.

**Complexity**
Highest because policy selection becomes part of every dispatch and replay closure.

**Maintenance**
Flexible but susceptible to duplicated or inconsistent QE policies across Workflows.

**Context-window consequences**
Review requires the captured output, extracted diagnostics, selected policy, and
Workflow-specific disposition.

**Future compatibility**
Supports different operational risk profiles but permits identical QE output to
receive different interpretations.

**Advantage**
Maximizes configurability and policy provenance.

**Risk**
Moves QE-specific operational meaning above the anti-corruption boundary and conflicts
with the current assignment of failure mapping to the integration.

## Three-option comparison

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| QE semantic owner | Integration | Integration | Workflow/application policy |
| Calculator results per attempt | One | Mechanical output plus assessment | Output plus policy evaluation |
| CPN recovery representation | Directly from typed result | After mandatory assessment join | After policy evaluation |
| Workflow complexity | Moderate | High | Highest |
| Reclassification | New derived assessment | Native separate operation | New policy evaluation |
| Failure-mapping locality | Strong | Strong but delayed | Distributed |
| Interpretation consistency | Strong | Strong | Policy-dependent |
| Existing architecture fit | Strongest overall | Preserves after-ingress parser placement | Requires broader policy architecture |

## Recommendation

**Accepted recommendation: Option A.**

The operation-specific QE ResultObject retains independent process,
calculator-reported, diagnostic, artifact, and native-state facts rather than one
undifferentiated success flag. The integration-owned diagnostic classifier consumes
both exact stream artifacts under an explicit QE executable/version and classifier
version. Known nonblocking diagnostics, known fatal diagnostics, and unresolved
messages remain distinguishable; the current decision does not classify any specific
observed message as harmless.

Confirmed dispatch means that the effect and its outputs were determinately captured,
not that QE succeeded. `TaskResultIngester` may therefore correlate and retain a typed
calculator-failure result. Application composition maps only an explicitly
continuation-eligible result to the generic value that can satisfy a downstream Task
gate.

Retry control is part of the Workflow-owned CPN definition, but retry execution is
not part of the effect-free CPN kernel. The conceptual flow is:

```text
attempt result
  |-- continuation eligible --------------------------> downstream gate
  `-- calculator failed or diagnostic unresolved ----> recovery required
                                                         |
                                              explicit resolution admitted
                                                         |
                         +-------------------------------+------------------+
                         |                                                  |
               reevaluate original result                            retry eligible
               without QE execution                                       |
                                                              new authorized dispatch
                         |
                  abandon or terminal failure remains available
```

A resolution only enables the applicable transition. It does not invoke QE, reuse an
execution grant, erase an attempt, or silently change settings. A retried effect uses
new activation, operation, attempt, request, obligation, and grant identities. The
failed result and resolution dependency remain in ordered Workflow history. An
explicit bound or terminal abandon path prevents an uncontrolled retry loop.

The accepted ownership decomposition is:

| Surface | Owner and role |
|---|---|
| Process and diagnostic observations | Immutable calculator DataObjects/ResultObject components with intrinsic field invariants only |
| QE diagnostic classification | Integration-owned ActionObject over exact streams and explicit program/version inputs |
| Operation-specific QE output | QE integration-owned immutable ResultObject satisfying the generic plane-wave structural port |
| Calculator-result to CPN-value mapping | Application composition adapter preserving exact result and classifier identities |
| Recovery and retry topology | Workflow-owned reusable CPN composition |
| Retry dispatch | Workflow service after selection, new identity construction, and fresh authorization |
| Stream/result persistence | Separately owned serializers and repositories; no persistence methods on the records |

## Deferred questions

- The initial public in-memory class names and fields and integration-private local
  serializers are implemented by the authorized integration Task. Durable public wire
  tokens and serializers remain deferred.
- The deterministic-fixture diagnostic catalog is implemented. An initial supported
  real-QE executable/version diagnostic catalog remains deferred.
- The observed 139-byte floating-point notice remains uncharacterized; this decision
  does not mark it nonblocking.
- The exact domain record used to establish an operational versus scientific
  resolution remains deferred. It must reuse the applicable accepted human-decision
  boundary rather than introduce an unapproved generic resolution hierarchy.
- The exact retry bound and abandonment policy are Workflow-definition inputs, not
  integration defaults.
- Scheduler adapters, remote execution, and automatic setting repair remain excluded.
- Scientific convergence, validation, acceptance, and uncertainty claims remain
  outside diagnostic classification and retry control.

## Human decision required

Resolved. The human accepted **Option A — integration-classified,
diagnostic-bearing QE results with Workflow-owned CPN recovery state and explicit
resolution-gated retries**. This decision does not activate implementation, authorize
QE execution, approve any diagnostic signature, or grant retry execution authority.
