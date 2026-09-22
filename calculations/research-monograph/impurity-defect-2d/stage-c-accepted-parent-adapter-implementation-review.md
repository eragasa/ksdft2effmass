# Stage C accepted-parent adapter implementation review

## Review boundary

This adversarial review covers only the HC15 execution-free adapter,
authorization/provenance contracts, independent verifier, maintained authored
fixtures and tests, and the HC16 native-root binding. It reviewed
`run_stage_c_parent.py`, `verify_stage_c_parent.py`, both closed schemas, both new
authored resources, the Stage C test module, and synchronized protocol/preflight
records. It did not open accepted periodic, Stage A, or Stage B contents through
the adapter, execute accepted parents, populate the external native root, create
accepted-parent output, invoke the plotter on accepted evidence, or activate
Stage D.

## Procedural deviations and human dispositions

During parent identity checking after the correction handoff, the parent ran
`sha256sum` over the five accepted input files before an attempt journal existed.
This was an accepted-parent byte read and is not represented as though no such
read occurred. It performed no JSON parsing or semantic inspection, scientific
computation, output creation, external-root access or mutation, or information
gain beyond the already-frozen digests. All five observed digests matched the
previously recorded immutable identities.

Human response preserved verbatim: `recommendation authorized`.

Normalized disposition:
`RECORD_PARENT_PREJOURNAL_FIVE_INPUT_SHA256SUM_AS_PROCEDURAL_DEVIATION`.
The deviation is retained as a process-boundary violation, not accepted Stage C
evidence. It did not consume or authorize HC17 because no HC17 executable
authorization or attempt journal existed.

During subsequent HC17 preparation, the worker mistakenly ran aggregate
`SHA256SUMS`. That command byte-read and re-hashed only `stage-a-result.json`,
`stage-b-result.json`, and `stage-c-design.json` before attempt consumption. It
performed no semantic parsing, scientific computation, executable authorization,
attempt consumption, accepted-result creation, or external-root access, and all
three checks matched frozen identities. Its ordinary `OK` stdout was redirected
to transient `/tmp/stage-c-hc17-checksums.log`; this was not a repository or
Stage C result, but is stated explicitly rather than hidden.

Second human response preserved verbatim: `recommendation authorized`.

Second normalized disposition:
`RECORD_WORKER_PREJOURNAL_THREE_INPUT_AGGREGATE_SHA256SUMS_AS_PROCEDURAL_DEVIATION`.
This second deviation also did not resolve, authorize, or consume HC17. The
accurate boundary statement after both deviations is: accepted-input byte reads
occurred, but no semantic accepted-parent read and no Stage C execution occurred.

The corrected preparation rule now prohibits every pre-attempt aggregate
checksum check whose catalog contains an accepted input. Preparation checks use
an explicit safe-file allowlist excluding all five accepted inputs; only the
protected Workflow may validate their identities after STARTED consumes the
attempt. Its package-specific catalog contains only newly retained Stage C
products.

Definition of done: authored records traverse the same adapter intended for a
future accepted run; all execution authority and provenance is closed and
fail-before-read; the independent verifier does not import runner code; future
authority, native storage, compact outputs, resources, and one-attempt behavior
are frozen; maintained software-verification checks pass; and no accepted output
exists.

## Frozen identities

The future HC17 authorization must bind these implementation identities:

| Role | SHA-256 |
|---|---|
| `run_stage_c_parent.py` | `8e9a603d56b685079db8e818e61545fc1275e5ce3b5900823a2c0c86f1472210` |
| `verify_stage_c_parent.py` | `93ceb1e3f3a623b19495e0e18dfeaf8c69c437965e75035366e1d383ea64727b` |
| `plot_stage_c_parent.py` | `21489a1bc9fec08e6c7c2c87d9394b0f69c2e7b520bbda3ce15e3b580730669e` |
| `stage-c-result.schema.json` | `e4a58d8df7825a9231ee3aaf312909ffa78c0ca8225b4b71299466985abc2188` |
| `stage-c-execution-authorization.schema.json` | `4cd64bb18d8e345b5d5a8589def4da960619848afbbce061a66f97867fcc8b82` |

Authored review-input identities are:

| Role | SHA-256 |
|---|---|
| five-record adapter fixture | `f23183cd0e041e1278f18bbedabfebc1fe0c9b4b6e42bb2ad3c61ae05a38ca38` |
| nonexecuting authorization fixture | `a26fd668a1b0567142e01b9016466374e64330fe65bdc1921dc19459e5e21ec5` |
| Stage C execution-contract tests | `4532be265151a6203da4400b1218842976ebe9c4004b302a8b41ba5a31a2b206` |

The later protected boundary is frozen as:

- checkpoint `RM-IMPURITY-DEFECT-2D-STAGE-C-ACCEPTED-PARENT-EXECUTION-HC17` at
  `.pi/checkpoints/research-monograph-impurity-defect-2d-stage-c-accepted-parent-execution.json`;
- authorization identity
  `research-monograph.impurity-defect-2d.stage-c.accepted-parent-execution.hc17.v1`
  at `stage-c-accepted-parent-execution-authorization.json`;
- repository root `/Users/eugene/worktrees/ksdft2effmass-calculations`, Git
  revision `9def2718ee763faf2060eb692739600485de5c72`, and machine `minerva`;
- external native simulation root `/Users/eugene/projects/ksdft2effmass`; and
- the seven compact repository outputs named in the implementation plan.

Neither future authority file nor any accepted-parent output exists.

## Adversarial findings and corrections

### Adapter momentum ordering

Disposition: `NO_ACTION_REQUIRED`

Problem: The first authored adapter attempt used a monotonically centered
momentum list, which did not match the inverse-Fourier array convention and
therefore broke the retained $D_2$ control.

Evidence: The authored adapter stopped before retained evidence; changing the
mesh to `numpy.fft.fftfreq(15)` restored the independently checked transform
ordering. The final authored adapter and independent verifier pass all criteria.

Consequence: Resolved. Leaving the original ordering would have made the future
adapter mathematically incompatible with the frozen Fourier convention.

Next action: None.

### Durable one-attempt consumption

Disposition: `NO_ACTION_REQUIRED`

Problem: Parent review found that the first implementation checked for absent
outputs but created only the result near the end. A parser, invariant, or process
failure before serialization therefore left no consumed-attempt evidence and
allowed the same authority to be invoked again.

Evidence: The corrected protected Workflow completes authority preflight without
reading accepted-parent contents, then exclusively creates an append-only attempt
journal before accepted-input hashing. STARTED alone consumes the attempt. Every
ordinary Python success/failure appends a terminal event with chained start-event
identity and output or error identities. Any later invocation fails exclusive
creation before source conversion. Authored success and parser-failure tests
prove byte-preserving no retry.

Consequence: Resolved. A favorable rerun is unavailable even when no result was
created; abnormal process termination can leave STARTED, which remains consumed.

Next action: None.

### Complete protected-operation ownership

Disposition: `NO_ACTION_REQUIRED`

Problem: Parent review found no producer for the complete authorized package:
the runner produced only a result, verification wrote stdout, report/manifest
producers were absent, and the plotter rejected accepted-parent results.

Evidence: The corrected authorization binds eleven ordered operations and the
workflow implementation identity. One typed Workflow now owns exclusive result
serialization, captured independent verification log, accepted-capable SVG,
report, native evidence manifest, package-specific checksum catalog, and terminal
attempt finalization. Its authored sandbox mode produces and checksum-verifies
all seven artifacts without accepted inputs.

Consequence: Resolved. HC17 can bind one complete operation rather than unrelated
manual commands or missing producers.

Next action: None.

### Atomic retained-output creation

Disposition: `NO_ACTION_REQUIRED`

Problem: Parent review found check-then-write races in JSON serialization and SVG
plotting that could replace a target created after the preliminary existence
check.

Evidence: Result serialization uses binary exclusive creation; SVG uses text
exclusive creation; verification log, report, manifest, checksum catalog, and
attempt start use the same exclusive writer. Tests preserve existing sentinel
bytes and preserve every byte of a completed package on a second invocation.

Consequence: Resolved. A concurrent or preexisting target causes retained
failure rather than replacement.

Next action: None.

### Authority identity and output ambiguity

Disposition: `NO_ACTION_REQUIRED`

Problem: A draft allowed any repository-contained authorization path and any
checkpoint path with a matching decision, leaving the future authority identity
less specific than the requested protected boundary.

Evidence: The final runner, verifier, and schemas freeze the HC17 checkpoint
path, authorization path and identity, ordered twelve-artifact and eleven-
operation inventories, seven compact outputs, canonical repository root and Git revision,
machine, exact native root, and
resource envelope before accepted reads.

Consequence: Resolved. A later authorization cannot substitute another retained
path or silently redirect compact outputs.

Next action: None.

### Native-storage separation

Disposition: `NO_ACTION_REQUIRED`

Problem: The initial adapter draft bound only repository output paths and did
not represent the later human storage decision.

Evidence: HC16 preserves `recommendation authorized` and the instruction
`storage for all simulations should be in ~/projects/ksdft2effmass`. The final
authorization and result provenance bind the expanded root
`/Users/eugene/projects/ksdft2effmass`; accepted execution would use it as the
process working root. Compact result/provenance records remain separately bound
under repository `calculations/**`. No current command entered or populated the
external root.

Consequence: Resolved. Native simulation storage and compact version-controlled
records are not conflated.

Next action: None.

### Independent provenance reconstruction

Disposition: `NO_ACTION_REQUIRED`

Problem: An early verifier draft checked only the count of authored adapter input
identities and incompletely rebound future result provenance.

Evidence: The final verifier independently hashes all five embedded authored
records, reconstructs both parents without importing the runner, checks every
route and fit using QR, and in dormant accepted mode rebinds checkpoint,
authorization, repository root and Git revision, machine, native root, artifact identities, output
paths, attempt policy, evidence status, and result input provenance.

Consequence: Resolved. A result cannot pass by retaining the right inventory
size with different source identities.

Next action: None.

### Runtime and peak-memory enforcement

Disposition: `SAFE_TO_DEFER`

Problem: The 600-second runtime and 2-GiB peak-memory values are observed and
checked only after the numerical evaluation; they are not proactive wall-clock
or operating-system memory limits.

Evidence: `AcceptedParentStageCExecutionWorkflow` evaluates first, obtains
`resource.getrusage` observations, and then applies the declared comparisons.
The output-size limit is enforced before terminal success, but there is no timer
or process memory sandbox.

Consequence: A runaway future calculation would not be proactively terminated at
600 seconds or 2 GiB by this implementation. The bounded authored workload is far
below both declarations, but that observation is not hard enforcement.

Next action: HC17 must state this limitation exactly. Revisit only if the human
requires proactive hard limits; that would require separate implementation and
review before changing the claim.

### Accepted-record semantic observation

Disposition: `SAFE_TO_DEFER`

Problem: By design, the adapter has not semantically opened the real accepted
records; compatibility is established from owning source contracts, frozen
hashes, and authored records rather than an observed accepted run.

Evidence: HC15 explicitly forbids real parent reads through the new path. The
five-record authored fixture exercises the expected closed fields and exact
scientific constants. Runtime hash and identity validation precedes those future
semantic reads.

Consequence: A separately authorized HC17 attempt could still retain a fail-
closed parser or invariant failure if an accepted record differs from its owning
contract. Such a failure would consume the single attempt and would not justify
a retry.

Next action: Revisit only within a separately resolved HC17 execution boundary;
retain any failure without favorable rerun. This limitation does not block the
current execution-free definition of done.

## Verification evidence

- Ruff passed for runner, verifier, plotter, and the Stage C maintained test module.
- Strict mypy passed for the same four Python files.
- The cohesive artifact-owned module reports **28 passed**.
- Python evidence conformance reports one artifact-owned module, 28 unique test
  owners, and `PASS`.
- Both Draft 2020-12 schemas accept their authored records in maintained tests.
- Final complete authored operation retained seven files totaling 2,224,320
  bytes, including a 2,211,718-byte JSON result, in 3.88 seconds with
  103,759,872 bytes maximum resident set size. Its journal retains STARTED then
  terminal SUCCESS, and its package checksum catalog verifies all five finalized
  products.
- Independent adapter reconstruction reports `PASS`, no runner import, no normal
  equations, and maximum scalar difference
  $2.741586977772928\times10^{-15}E_G$.
- A separate authored parser-failure operation retains STARTED then terminal
  FAILURE; a valid retry at the same package path fails without changing bytes.
- The frozen accepted-parent attempt journal, result, verification log, SVG,
  report, manifest, package checksum catalog, HC17 checkpoint, and execution-
  authorization record are absent.

These checks establish software behavior for authored synthetic records only.
They do not establish accepted-parent execution, scientific validation,
uncertainty quantification, material transfer, publication readiness, or human
acceptance.

## Outcome

The parent correction pass initially reported `CHANGES_REQUIRED`. Its three
`MUST_FIX` findings—durable attempt consumption, complete package ownership, and
atomic retained-output creation—are closed by the corrections and authored
success/failure evidence above. The post-computation resource-limit behavior is
retained as `SAFE_TO_DEFER` and must be explicit in HC17.

Review outcome: `NO_BLOCKING_FINDINGS`

Operator request: `AUTHORIZATION_REQUIRED`

Recommendation: Keep the repository paused at the exact unresolved HC17
protected-execution question. Recommend one attempt only if its exact preflight
remains satisfied and the human explicitly authorizes it with the post-computation
runtime/memory limitation understood. The pending checkpoint itself authorizes no
accepted-input read, execution, external-root access, retry, verifier or plotter
invocation on accepted evidence, Stage D activation, commit, push, or merge.
