# Quantum ESPRESSO local-execution implementation contract

## Status and scope

This page fixes the implementation-level contract for the active
`quantumespresso.simulations.integration` Task. It refines the accepted
[diagnostic outcome and retry decision](quantum-espresso-diagnostic-outcome-decision.md)
without changing its allocation of authority or scientific meaning.

The first implementation remains a revisable Python vertical slice, but the later
accepted [package-ownership decision](quantum-espresso-package-ownership-decision.md)
authorizes its demonstrated Python contracts as public package-level APIs. Generic
plane-wave DFT contracts are public from `ksdft2effmass.calculators.dft.pw`; all
QE-specific contracts and behavior are public from
`ksdft2effmass.integration.quantum_espresso`. Cross-language contracts and a durable
public wire format remain deferred until the slice has passed
its software-verification cases and review.

The implementation may invoke only deterministic test executables under this Task.
It does not authorize or invoke Quantum ESPRESSO, MPI launchers, schedulers, remote
services, or another scientific executable. It implements no automatic retry and no
Workflow CPN transition.

## Ownership and dependency direction

The canonical modules are:

| Module | Ownership |
|---|---|
| `ksdft2effmass.calculators.dft.pw` | Backend-neutral plane-wave DFT specification and binding vocabulary plus the structural calculator port |
| `ksdft2effmass.integration.quantum_espresso.contracts` | QE-specific immutable native inputs, executable bindings, process and diagnostic observations, closed concrete outcomes, and output ResultObjects |
| `ksdft2effmass.integration.quantum_espresso.diagnostics` | QE stream diagnostic signatures and the version-bound diagnostic-classifier ActionObject |
| `ksdft2effmass.integration.quantum_espresso.execution` | Read-only local preparation, confinement, source observation, supported-binding admission, and dry-run reporting |
| `ksdft2effmass.integration.quantum_espresso.effects` | Identity-rechecked staging, deterministic workspace snapshots, native-output candidate collection, and private terminal-record serialization and publication |
| `ksdft2effmass.integration.quantum_espresso.process` | One-attempt local process entry, bounded lifecycle handling, exact independent stream capture, and mechanical process observations |
| `ksdft2effmass.integration.quantum_espresso.outcomes` | Fail-closed cross-record compatibility checks and calculator-outcome precedence |

The backend-neutral calculator module imports only narrow Workflow identity and
ResultObject contracts it actually represents and imports no integration. The QE
integration modules may import generic calculator and Workflow contracts they adapt.
Generic Workflow and CPN modules import neither calculator nor integration modules.
Application composition adapts the concrete QE executor result to
`SimulationDispatchOutcome`; no runtime plugin registry, service locator, generic
integration base class, calculator-owned QE facade, or backend hierarchy is
introduced.

Nontrivial behavior belongs to the named ActionObjects below. DataObjects and
ResultObjects own only their intrinsic field and closed-variant invariants. They have
no filesystem, process, serialization, retry, or scientific-acceptance methods.

## Identity and scalar conventions

Private owner-local identities are frozen one-field records containing one nonempty
built-in `str`. Equal-looking identities of different nominal classes are not
interchangeable. The slice defines identities for:

- exact QE execution input;
- executable configuration;
- diagnostic classifier implementation/version;
- process observation;
- diagnostic observation and report;
- local preparation and attempt workspace;
- terminal record; and
- calculator output.

Exact byte identity uses the existing Workflow-owned `ArtifactContentIdentity` at an
actual artifact exchange boundary: algorithm `sha256`, 64 lowercase hexadecimal
digest characters, and an unsigned 64-bit byte count. The integration computes this
identity; generic plane-wave or concrete QE DataObjects only retain it.

All counts, byte offsets, exit codes, signal numbers, nanosecond durations, limits,
and resource observations are built-in `int` values and reject booleans and numeric
strings. Nonnegative counters use the inclusive unsigned 64-bit range. Timeouts and
resource ceilings use positive integral units rather than binary floating-point
seconds. Paths are exact `pathlib.Path` values only at the local integration boundary;
portable represented artifact names use parent-free relative POSIX text.

No maintained record contains credentials, environment secrets, unrestricted
environment dumps, or pseudopotential/native-state bytes.

## QE integration DataObjects

### `QuantumEspressoProgram`

A closed string enum initially distinguishes `pw` and `bands`. A separate closed
`QuantumEspressoExecutableKind` distinguishes `quantum_espresso` from
`deterministic_fixture`. A fixture executable is therefore never represented as a QE
binary or admitted as a calculated QE result, while its configured program role can
exercise `pw`- or `bands`-shaped integration behavior.

### `QuantumEspressoInputArtifactContent`

A closed union distinguishes `QuantumEspressoFileArtifactContent`, containing one
regular-file `ArtifactContentIdentity`, from
`QuantumEspressoTreeArtifactContent`, containing one immutable directory-tree manifest
identity plus its canonically ordered nonempty manifest-entry identities. File and
tree content are not interchangeable. The tree variant is permitted only for
predecessor native state in the initial slice.

### Input artifact variants

The closed `QuantumEspressoInputArtifact` union contains:

- `QuantumEspressoNativeInputArtifact` with regular-file content;
- `QuantumEspressoPseudopotentialArtifact` with regular-file content; and
- `QuantumEspressoPredecessorNativeStateArtifact` with directory-tree content, exact
  admitted predecessor ResultObject identity, and native-output manifest-entry
  identity.

Every frozen variant contains an owner-local artifact identity, exact content, and a
`QuantumEspressoArtifactDestination`. That destination is parent-free portable POSIX
text relative to the attempt workspace. No variant contains a source filesystem path.
Artifact identities and destinations are unique within one execution input.

### `QuantumEspressoExecutionInput`

A frozen record containing:

- execution-input identity;
- `QuantumEspressoProgram`;
- exactly one native-input artifact;
- a tuple of zero or more pseudopotential artifacts;
- a tuple of zero or more predecessor-native-state artifacts;
- exact Task-definition, Task-instance, activation, operation, and attempt identities;
  and
- input-contract version identity.

Artifact collections are tuples, unique by artifact identity and destination, and
canonically ordered by owner-local artifact identity. The object chooses no QE
variable, scientific default, pseudopotential, path root, executable, retry, or
resource setting.

### `QuantumEspressoExecutableConfiguration`

A frozen record containing:

- executable-configuration identity;
- represented QE program role;
- executable kind `quantum_espresso` or `deterministic_fixture`;
- executable content identity;
- exact supported program-version text, whose namespace must agree with executable
  kind;
- exact argument suffix as a built-in tuple of built-in strings;
- environment additions as a canonically ordered tuple of nonempty key/value pairs
  restricted to `OMP_NUM_THREADS`, `OMP_STACKSIZE`, `MKL_NUM_THREADS`,
  `OPENBLAS_NUM_THREADS`, and `VECLIB_MAXIMUM_THREADS`;
- classifier identity accepted for this executable/version; and
- configuration-contract version identity.

The concrete local binding separately supplies the absolute executable path. Shell
execution is prohibited. The first implementation accepts an empty argument suffix or
explicit non-shell arguments only and never inserts `mpirun`, `mpiexec`, PWTK, a
scheduler command, or an ambient command prefix. Environment additions are an
allowlisted exact tuple and cannot replace the complete inherited environment with an
unbounded dump.

## Local integration DataObjects

### `LocalQuantumEspressoArtifactSource`

A frozen record binding one `QuantumEspressoInputArtifact` to one absolute source
`Path`. Preparation requires a nonsymlink regular file for ordinary file roles or a
nonsymlink directory tree for predecessor native state. Every observed source byte
must agree with the declared content identity before staging. Directory-tree identity
uses the integration-local `qe-tree-manifest-v1` convention rather than concatenated
native bytes. Each descendant directory or regular file receives a deterministic
`qe-tree-entry-v1` identity from length-prefixed UTF-8 frames containing its type,
portable relative path, and, for files, SHA-256 identity and byte count. The manifest
identity frames the sorted entry-identity values. Symlinks and other entry types fail
closed. This convention is not the Workflow artifact-manifest wire format.

### `LocalQuantumEspressoExecutionLimits`

A frozen record containing positive integral:

- wall-time limit in milliseconds;
- termination-grace interval in milliseconds;
- minimum required free bytes;
- maximum created entry count;
- maximum created total bytes; and
- optional peak-resident-byte ceiling represented by a closed present/absent variant,
  not a sentinel.

These are operational ceilings, not scientific settings. A limit change creates a new
execution configuration and authorization input.

### `LocalQuantumEspressoSupportedExecutableBinding`

A frozen admission record containing the exact executable-configuration identity,
executable-content identity, program role, executable kind, program version, and
classifier identity accepted by one composed preparer. Preparation reconstructs this
complete value from the request configuration and requires exact allowlist membership
before filesystem observation. A matching self-declared program/version tuple cannot
substitute different executable bytes.

### `LocalQuantumEspressoExecutionPreparationRequest`

A frozen record containing:

- exact calculator execution input;
- exact executable configuration;
- absolute executable source path, its expected content identity, and a parent-free
  destination for the private staged executable copy;
- absolute authorized run root;
- one parent-free relative attempt-workspace name;
- exact artifact-source bindings;
- execution limits;
- exact stdout, stderr, before-snapshot, after-snapshot, terminal-record, work, and
  result destinations beneath that workspace; and
- the Workflow request, executor, destination, resource-scope, and authority-correlation
  identities that the later effect must match.

Every destination is explicit. Neither current working directory nor repository-root
search participates in construction or preparation.

### `LocalQuantumEspressoPreparedExecution`

A frozen successful preparation result containing the exact preparation request plus:

- canonical argv beginning with the private staged executable destination;
- canonical allowlisted environment additions;
- resolved root-confined destinations;
- executable and input-source identity observations;
- required/free-byte observation;
- preparation implementation/version identity; and
- preparation-result identity.

Preparation is read-only with respect to the attempt workspace: it hashes and checks
inputs but does not create directories, stage artifacts, open streams, or invoke a
process. The target workspace must not already exist. Dry-run reporting renders this
object and therefore cannot invoke or stage a scientific executable.

### `LocalQuantumEspressoPreparationFailure`

A closed preparation result containing a stable failure code, failed phase, expected
and observed sanitized conditions, related input or path identities, preparation
implementation identity, and explicit claim boundary. Codes initially cover invalid
confinement, unexpected symlink/type, missing source, source identity mismatch,
executable identity mismatch, existing workspace, insufficient free space, unsupported
program/version/classifier binding, and resource-limit invalidity.

Preparation failure creates no attempt workspace and is not retryable unless an
external owner explicitly resolves the reported condition.

## Process, diagnostic, and artifact observations

### `QuantumEspressoStreamObservation`

A frozen record containing channel `stdout` or `stderr`, one portable stream-artifact
reference, exact content identity, and captured byte count. The two channels are
always separate, even when one contains zero bytes.

### `QuantumEspressoProcessTermination`

A closed union:

- normal exit with one nonnegative process exit code;
- signal termination with one positive signal number; or
- timeout with the exact timeout and cleanup observations.

Normal exit code zero does not imply calculator success. Signal and timeout outcomes
are determinate only when the process lifecycle and both stream captures are closed.
If process state cannot be established after spawn, no process observation or
calculator output is constructed and dispatch adaptation is indeterminate.

### `QuantumEspressoProcessObservation`

A frozen record containing:

- process-observation identity;
- exact execution-input, executable-configuration, preparation, and attempt identities;
- canonical argv identity;
- termination variant;
- monotonic wall duration in nanoseconds;
- separate stdout and stderr observations;
- before- and after-workspace manifest identities;
- observed created-entry count and total bytes;
- closed optional peak-resident-byte observation; and
- process-observer implementation/version identity.

It contains no calculator convergence or diagnostic disposition.

### `QuantumEspressoDiagnosticObservation`

A frozen record identifies one diagnostic without inventing cross-stream order. It
contains:

- diagnostic-observation identity;
- source channel;
- zero-based half-open byte range within that exact stream;
- exact stream content identity;
- exact diagnostic-span content identity;
- classifier signature identity when recognized;
- closed disposition `nonblocking`, `fatal`, `secondary_fatal`, or `unresolved`;
- sanitized summary; and
- diagnostic claim boundary.

Within-stream observations are sorted by byte range. No total order is asserted
between stdout and stderr. Exact diagnostic text is preserved by the immutable stream
artifact plus byte range and span identity; persisted Workflow diagnostics use only
the sanitized summary and related artifact identities.

### `QuantumEspressoDiagnosticReport`

A frozen classifier result record contained by the later operation-specific
ResultObject and containing:

- report and classifier identities;
- exact executable configuration, executable-kind, program-role, and version
  identities;
- exact stdout and stderr content identities;
- ordered per-stream diagnostic observations;
- closed report kind `clear`, `fatal`, `unresolved`, or `contradictory`;
- known completion-marker observations; and
- classifier claim boundary.

`clear` permits zero or more recognized nonblocking observations and prohibits fatal or
unresolved observations. `fatal` requires at least one recognized fatal observation
and no unresolved or contradictory observation. Unsupported versions and every
unmatched diagnostic are `unresolved`. A fatal marker combined with inconsistent
process/completion facts is `contradictory`. There is no permissive fallback.

The observed 139-byte floating-point notice is not initially classified as
nonblocking. The deterministic verification fixture may use the exact text, but an
accepted signature entry is a separate explicit classifier-catalog change.

### `QuantumEspressoNativeOutputManifest`

A calculator-specific immutable candidate manifest containing exact output artifact
identities, roles, portable workspace-relative paths, content identities, and
symlink/type observations. The separately captured stdout and stderr artifacts are
mandatory entries, including a zero-byte stream; native scientific artifacts are
included only when observed. A confirmed failure result therefore still has the
nonempty manifest-entry set required by the Workflow dispatch contract. This candidate
is not the Workflow `ArtifactManifest`. Application composition may adapt verified
candidates into Workflow-owned manifest entries after confirmed dispatch and must
retain the source identities.

## Closed calculator outcome

`QuantumEspressoCalculatorOutcome` is a closed union contained by each
operation-specific output:

| Variant | Required observations | Continuation eligibility |
|---|---|---|
| `completed` | Normal exit zero, required completion marker, diagnostic report `clear`, required native artifacts present | Eligible for Task-specific admission evaluation; not automatically admitted |
| `calculator_failed` | Normal process exit plus report `fatal` with internally consistent QE fatal evidence | Never eligible |
| `process_failed` | Determinate nonzero exit with no unmatched diagnostic text and without a complete recognized QE fatal, signal termination, or timeout with closed capture | Never eligible |
| `diagnostic_unresolved` | Report `unresolved` or `contradictory`, including unknown text or inconsistent exit/completion facts | Never eligible pending explicit resolution |

The outcome is mechanical and calculator-reported. `completed` does not assert SCF
convergence, numerical convergence across settings, scientific validity, or human
acceptance. An operation-specific parser may retain a separate QE-reported convergence
observation when the operation contract requires it.

Outcome precedence is fail closed:

1. incomplete or uncertain spawn/lifecycle/capture/terminal-record state produces no
   calculator output and maps to rejected or indeterminate dispatch as applicable;
2. unresolved or contradictory diagnostics produce `diagnostic_unresolved`;
3. determinate abnormal termination produces `process_failed`;
4. internally consistent recognized fatal output produces `calculator_failed`; and
5. only consistent exit-zero, completion-marker, clear-diagnostic, and required-artifact
   closure produces `completed`.

## Operation-specific ResultObjects

The initial private slice does not introduce one universal simulation result. It
provides distinct `QuantumEspressoPwResult` and `QuantumEspressoBandsResult` wrappers
for the two configured QE program roles. Each wrapper owns its Workflow
`ResultObjectIdentity` and contract-version identity and contains one shared immutable
`QuantumEspressoOperationResultEvidence` value with:

- exact immutable `QuantumEspressoExecutionInput`, including its identity and complete
  represented Task-definition, Task-instance, activation, operation, and attempt
  producer correlations;
- `QuantumEspressoProcessObservation`;
- `QuantumEspressoDiagnosticReport`;
- one closed `QuantumEspressoCalculatorOutcome`;
- exact native-output manifest and entry identities;
- exact terminal-record identity.

Task-specific SCF, NSCF, bands, and DOS continuation predicates inspect the explicit
candidate roles fixed by their extraction specification; this slice does not infer an
operation kind from native input text. Failure and unresolved outcomes do not fabricate
required successful artifacts; the candidate manifest retains only artifacts actually
observed.

Cross-field consistency is intrinsic to the operation-specific ResultObject and is
validated during construction. Retryability is absent unless a future accepted
failure contract can determine it from explicit evidence. No ResultObject provides
`retry()`, filesystem access, serialization methods, or mutation.

## ActionObjects and effects

### `QuantumEspressoDiagnosticClassifier`

The integration-owned ActionObject consumes exact stdout and stderr bytes, their
content identities, the executable configuration, and its exact classifier catalog.
It returns `QuantumEspressoDiagnosticReport`. Wrong software types raise `TypeError`;
unsupported QE data produces an unresolved report rather than an exception.

Classifier catalogs are immutable code-owned versioned records in the initial slice,
not user-editable regex files or runtime plugins. Signatures are executable-kind,
program-role, and version specific, anchored to bounded structures, and covered by
exact positive and near-miss fixtures. Fixture catalogs and QE catalogs have distinct
identities; fixture success never claims observed QE compatibility.

### `QuantumEspressoCalculatorOutcomeResolver`

This integration-owned ActionObject consumes one exact process observation,
diagnostic report, native-output candidate manifest, and operation/version extraction
specification. It owns the cross-object precedence rules that produce one closed
`QuantumEspressoCalculatorOutcome`. Intrinsic record constructors do not infer
compatibility among independently valid process, diagnostic, and artifact records.
Unknown or contradictory combinations resolve only to
`QuantumEspressoDiagnosticUnresolvedOutcome`; the resolver never retries or changes an
input. An unresolved outcome may retain exact diagnostic-observation identities,
deterministic resolver-reason identities, or both. Reason identities cover
cross-record mismatch and missing completion evidence without fabricating a diagnostic
stream span.

### `LocalQuantumEspressoExecutionPreparer`

This integration-owned ActionObject consumes one preparation request and returns a
closed prepared or failed result. It owns path resolution, root confinement, exact
source/executable hashing, disk observation, and dry-run description. It performs no
mutation and no process invocation.

### `QuantumEspressoInputStager`

This integration-owned ActionObject runs only inside an already-authorized local
effect. It creates the previously absent attempt workspace, copies the exact admitted
executable to its private mode-0500 destination, stages each input source into its
private role, verifies every destination identity, and removes ordinary write access
from the workspace root and immutable executable/input/pseudopotential parents before
returning a closed staging result. Writable work, result, stream, and record
subdirectories remain explicit.
It rejects symlinks and path escape before copying. It never mutates or discovers a
predecessor workspace.

### `QuantumEspressoWorkspaceSnapshotter`

This integration-owned ActionObject produces deterministic before/after manifests of
the exact authorized workspace scope. Entry type, portable relative path, byte count,
and content identity are explicit. Unexpected symlinks, unsupported types, entry-count
or byte ceilings, and observation failure return closed snapshot failures.

### `QuantumEspressoWorkspaceSnapshotSerializer` and publisher

The serializer owns the private `qe-workspace-snapshot-v1` canonical JSON bytes. The
publisher verifies lineage, content identity, confinement, and transient two-entry/
two-byte-count workspace headroom, then uses same-directory atomic no-replace
publication at the exact prepared
before/after destination. These private records retain the manifests referenced by
the process observation and terminal record; they are not public persistence schemas.

### `QuantumEspressoNativeOutputCollector`

This integration-owned ActionObject consumes the closed after-snapshot and an explicit
operation/version extraction specification. It returns a verified
`QuantumEspressoNativeOutputManifest` or a closed collection failure. File presence
alone does not establish semantic availability.

### `QuantumEspressoTerminalRecordSerializer`

This integration-owned serializer owns one private version-1 canonical JSON terminal
record. The record contains only exact request/preparation/process/stream/snapshot/
diagnostic/output identities and closed status fields; large output bytes remain in
stream or native artifact files. It returns exact bytes and performs no filesystem
operation.

### `QuantumEspressoTerminalRecordPublisher`

This integration-owned ActionObject consumes exact serialized terminal-record bytes,
their identity, and the prepared absent destination. It first closes current workspace
usage and reserves the transient two-entry/two-byte-count headroom required by the
temporary file and hard link. It then writes a new temporary file beneath `records/`,
flushes and synchronizes it where supported, and performs one same-directory atomic
no-replace publication. It never overwrites a terminal record.
Failure before an observable terminal record maps to an integration failure or
indeterminate dispatch; it never fabricates a calculator result.

### `LocalQuantumEspressoProcessRunner`

This integration-owned external-effect ActionObject consumes an exact prepared and
identity-correlated staged execution plus distinct stream artifact identities. It
requires the workspace root and executable/input parents to remain non-writable,
rechecks the private mode-0500 executable copy and every staged input against the
closed before-snapshot, retains and rehashes opened executable and native-input
descriptors, opens stdout and stderr with no-replace semantics, and enters at most one
process with explicit argv, working directory, inherited environment-key allowlist,
and configuration-owned additions. The portable local implementation executes the
locked private executable pathname because Python on supported macOS exposes no
`fexecve`; the authority model permits no concurrent writer for an entered attempt and
makes no security claim against a malicious same-UID process that first changes file
modes. It actively samples aggregate workspace entry and byte
usage while the process is live, terminates the process group after an observed limit
violation, produces the after-snapshot before reading stream bodies, and never reads a
stream beyond the byte count admitted by that bounded snapshot. The aggregate monitor
is an operational fail-closed observer rather than an operating-system disk quota, so
an adversarial process may overshoot between samples; this integration makes no
hard-quota claim. A single monotonic deadline begins before process creation and is
checked before accepting a polled exit, so process-entry overhead and delayed polling
cannot produce an admitted over-limit normal exit. It records normal exit, signal
termination, or timeout only after process-group cleanup and both captures are closed. A known pre-entry failure is
rejected; lifecycle or capture uncertainty after entry is indeterminate. The initial
standard-library implementation fails closed
before entry when a finite peak-resident-memory limit is requested because it cannot
portably enforce and observe that ceiling.

### `LocalQuantumEspressoExecutor`

This integration-owned external-effect ActionObject owns one immutable
`LocalQuantumEspressoExecutionPlan` and consumes the complete Workflow effect request
supplied after Workflow claim authorization and dispatch-entry compare-and-swap. The
plan contains the read-only preparation request, extraction and stream bindings,
caller-supplied result and terminal identities, and exact expected run, versioned
grant authority reference, claim authorization, obligation, dispatch-entry state and
revision, outcome, and input identities. Before mutation the
executor independently verifies executor, request, Task definition and instance,
activation, operation, attempt, destination, resource, authorization, obligation,
grant, dispatch-entry, outcome, and Workflow input correlations. It then performs
exactly once:

1. re-run read-only preparation, create the isolated workspace, and stage its inputs;
2. serialize and atomically publish the private before-snapshot record;
3. open separate stdout and stderr targets;
4. spawn the exact executable with `shell=False`, explicit argv, explicit working
   directory, and allowlisted environment additions;
5. observe termination under the exact limits;
6. close and identity-check both stream artifacts;
7. produce, serialize, and atomically publish the private after-snapshot record;
8. classify diagnostics from both exact streams;
9. collect native artifact candidates;
10. construct the operation-specific output when all required observation boundaries
    are determinate; and
11. write the atomic terminal record.

It performs no retry. After process entry, inability to establish whether execution or
capture completed is indeterminate. A known pre-effect integration rejection contains
no calculator output. A determinate QE failure returns the typed operation-specific
ResultObject described above.

## Workflow admission and retry handoff

Application composition adapts one local execution result into the existing
Workflow-owned `SimulationDispatchOutcome`:

- determinate operation-specific output, including calculator/process failure and
  unresolved diagnostics, maps to `confirmed` with that ResultObject and the exact
  candidate native-output identities;
- pre-effect integration rejection maps to `rejected` with one structured
  `TaskInvocationFailure`; and
- post-entry uncertainty maps to `indeterminate` with the original reconciliation
  identities and no invented result.

Confirmed failure does not mean continuation admission. The Task-specific adapter maps
only an outcome satisfying the operation's continuation predicate to the generic CPN
external-output value used by a successor gate. Failed and unresolved outputs map to
the Workflow recovery branch when that later Workflow contract is implemented.

The current integration Task stops at this handoff. A later Workflow-owned contract
will fix exact recovery places and transition names. It must retain these accepted
semantics:

- failure or unresolved diagnostics produce recovery-required state;
- an explicit admitted resolution enables reevaluation, retry intent, or abandon;
- diagnostic reclassification may reevaluate the retained result without QE execution;
- corrective execution uses new activation, operation, attempt, request, obligation,
  and grant identities;
- the CPN remains effect-free and dispatch remains outside it; and
- every retry path has an explicit bound or abandon outcome.

## Initial private serialization boundary

The atomic local terminal record and before/after workspace-snapshot records receive
integration-private version-1 wires in this Task. Calculator DataObjects and
ResultObjects do not expose `to_json`, `from_json`, `to_dict`, or `from_dict`. Named
serializers own canonical field names, discrimination, version checks, and errors.

The terminal record is operational recovery evidence, not the durable WorkflowRun
aggregate and not a substitute for result ingress. Its private schema may be replaced
before public stabilization, but a written record is immutable; correction writes a
new identified record rather than overwriting the earlier terminal record.

## Software-verification contract

Maintained pytest inputs belong beneath
`python/tests/software_verification/ksdft2effmass/integration/quantum_espresso/resources/`.
They are synthetic executable and stream fixtures, not calculated physical data. Test
modules group every test beneath explicit `Test...` owner classes and follow the
maintained Python test-evidence procedure.

The minimum deterministic cases are:

1. dry-run preparation reports exact argv and confined destinations and performs no
   mutation or spawn;
2. successful fake process writes distinct stdout/stderr and returns completed only
   for a catalog-recognized nonblocking stderr fixture;
3. empty stderr remains a distinct zero-byte artifact;
4. fatal QE-shaped stdout plus recognized secondary stderr maps to
   calculator-failed;
5. unmatched stderr, unmatched stdout, and a near-miss signature map to unresolved;
6. contradictory exit/completion/fatal combinations map to unresolved;
7. nonzero exit without recognized QE fatal, signal termination, and closed timeout
   map to process-failed;
8. missing executable and pre-spawn identity mismatch are rejected without process
   entry;
9. post-entry stream, snapshot, or terminal-record uncertainty maps to indeterminate;
10. symlink, parent traversal, absolute portable destination, existing workspace,
    source mutation, entry-count ceiling, byte ceiling, and insufficient-space cases
    fail closed;
11. predecessor native state is copied into a new workspace and source/destination
    tree identities agree without source mutation;
12. operation-specific failure results fabricate no successful native artifact;
13. result-to-Workflow adaptation preserves all activation, attempt, grant,
    obligation, manifest, and result identities; and
14. no integration ActionObject retries, changes a scientific setting, invokes an MPI
    launcher, or constructs execution authority.

Passing these tests establishes only the documented software contract with synthetic
fixtures. It does not establish QE compatibility, numerical verification, scientific
validation, uncertainty quantification, physical correctness, production readiness,
or authorization for scientific execution.

## Implementation order and stop boundaries

Implementation proceeds in this order:

1. public generic plane-wave DFT specification, binding, and structural-port contracts plus public concrete QE execution contracts;
2. diagnostic classifier with synthetic exact and near-miss fixtures;
3. read-only local preparation and dry-run result;
4. staging, snapshots, process capture, artifact collection, and terminal serializer;
5. concrete local executor over deterministic test executables;
6. application adaptation to existing Workflow dispatch outcomes; and
7. focused tests, broader static checks, documentation synchronization, and independent
   read-only integration review.

Stop and return for human decision if implementation requires a stable public export,
a general retry framework, a scheduler/remote boundary, dependency addition, actual QE
execution, a new scientific setting or diagnostic disposition, or a change to the
accepted Workflow authority and dispatch contracts.
