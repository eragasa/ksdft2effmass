# `ksdft2effmass.simulations.quantumespresso`

`ksdft2effmass.simulations.quantumespresso` owns project-specific Quantum ESPRESSO
simulation composition above generic Workflow, toolchain, pseudopotential, and
QE-native integration contracts.

The bundled-example run identity maps an exact simulation Task identity, QE release,
and explicit whole-second UTC creation time to a portable Workflow run identity and a
deterministic relative external-workspace hierarchy. It performs no clock access,
filesystem mutation, or execution.

The supported execution-composition surface is `QuantumEspressoExecutionRequest`,
`QuantumEspressoPlanner`, and `QuantumEspressoExecution`. The request names one exact
dated schema-v2 JSON manifest. The accepted identity is
`quantum-espresso-execution-manifest:v2.20260921T155105Z`; the integer major version
remains `2`, and unknown dated v2 identities fail closed. The manifest controls run
identity, exact source identities, integration destinations, resource limits,
environment additions, native-output extraction candidates, and complete local
execution-plan correlation identities. The planner now constructs an inert
`LocalQuantumEspressoExecutionPlan` but not its classifier-dependent executor. The
manifest also names one canonical
development decision as evidence and embeds
one generic `ScientificExecutionAuthorityReference` containing the externally issued
grant revision, authority snapshot, and grant-state identities. The decision identity
is not a grant, and decoding does not issue or authenticate authority. The planner
constructs an effect-free correlated plan and exposes no direct path to QE-native
preparation, staging, or process entry. Its internal direct-execution Workflow rejects
invocation before filesystem mutation. A separate internal application ActionObject
binds the complete generic `SimulationDispatchControlWorkflow` lifecycle to only
`LocalQuantumEspressoExecutor` as its effect port. The generic Workflow persists the
reservation, persists the separately authorized claim, repeats claim authorization,
wins durable dispatch entry, and only then invokes the executor.
`QuantumEspressoDispatchAssembler` loads one exact content- and idempotency-bound
predecessor revision, requires replay equality, checks a separately supplied Task
activation and unused/reserved authority requests against the local plan, and returns
an inert lifecycle request. It performs no commit or effect and does not infer
authority from manifest correlations. `QuantumEspressoLocalExecutorAssembler`
constructs the complete native executor from that exact plan and an explicitly
supplied matching diagnostic catalog without preparing, staging, or entering a
process. `QuantumEspressoProtectedDispatchWorkflow` connects both assemblies to the
generic persisted reservation, claim, immediate reauthorization, and dispatch-entry
lifecycle without dependency discovery or fallback. Its effect-free `preflight`
requires replay equality, checks supplied authority for both phases, and composes the
executor in memory. Readiness grants no authority and the separate execution call
repeats current persisted assembly and lifecycle checks. The manifest CLI does not yet
supply external activation/authority inputs or select a repository, so non-plan mode
remains blocked. Software verification traverses persisted reservation, claim,
immediate reauthorization, dispatch entry, the local executor, confirmed
reconciliation, immutable result and native-output admission, obligation disposition,
generic CPN result firing, and replay-equal terminal successor commit with a
deterministic fixture only. This is not a QE calculation or production-authority
claim. Retry requires a new operation, attempt, obligation, and grant. The
real-QE diagnostic catalog is limited to `pw` 7.2, the exact completion marker, and a
fail-closed policy that leaves every nonempty stderr line—including the retained IEEE
notice—unresolved; it makes no convergence or scientific-validity claim. Completed
schema-v1 manifests remain
unaltered historical provenance and are not accepted for new planning.

The OpenBLAS comparator build planner binds the proposed QE 7.2 profile to generic
execution-free native build planning. It performs no build, installation, discovery,
or dependency adoption.

The pseudopotential adapter admits only cataloged UPF2 artifacts for the accepted
native QE branch and retains the backend-neutral source-entry identity, independent
UPF2 SHA-256, filename, and content-addressed path. It performs no byte verification,
QE parser smoke test, staging, invocation, cross-format comparison, or scientific
acceptance.
