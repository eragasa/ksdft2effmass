---
title: "Measuring the Harness: Telemetry for Deterministic Agentic Software Engineering"
author: "Eugene Joseph M. Ragasa"
affiliation: "De La Salle University, Taft Campus"
status: "Research proposal"
---

# Measuring the Harness: Telemetry for Deterministic Agentic Software Engineering

## Abstract

Large-language-model agents can perform substantial software-engineering work, but their practical efficiency is often limited by process instability rather than coding ability. Agentic workflows may repeatedly reconstruct repository state, generate malformed shell commands, dispatch redundant reviewers, load excessive historical context, execute duplicated validation, and produce control-plane artifacts whose cost is disproportionate to the underlying change. These behaviors are usually discussed anecdotally because agentic development harnesses rarely expose a measurement model for their own operation.

This project proposes an event-based telemetry framework for evaluating the determinism, efficiency, recoverability, and human burden of agentic software-engineering harnesses. The framework represents harness activity as an append-only sequence of immutable telemetry events covering task execution, delegation, command invocation, validation, review, correction, state reconstruction, human intervention, and completion. Deterministic ActionObjects transform these observations into run summaries and comparisons, while a local SQLite adapter provides queryable persistence without making the database itself an authority for project state.

The empirical study will combine repeated controlled tasks with matched natural software-development tasks performed under successive harness configurations. A run will count as a verified resolution only when it satisfies a task-specific verification floor. Primary outcomes will characterize verified-resolution probability, active harness time, computational and monetary cost, human burden, and process amplification. Diagnostic measures will include duplicate agent dispatch, maintained-command coverage, ad hoc shell use, correction cycles, context consumption, and durable-state recovery. The study distinguishes software verification of the telemetry implementation from empirical validation of claims about harness effectiveness. It does not assume that more process is better; instead, it tests whether explicit object boundaries, maintained commands, durable state, and constrained delegation produce measurable improvements over prose-driven orchestration.

The expected contribution is a reproducible measurement framework for agentic software engineering, together with evidence concerning which forms of harness structure improve reliability and which merely introduce process ceremony.

## 1. Motivation

The decreasing cost of generating code shifts the software-engineering bottleneck from syntax production toward judgment, coordination, verification, and state management. An agent may generate a technically plausible implementation quickly while consuming substantially more time reconstructing context, assembling shell commands, coordinating reviewers, updating control records, and repeating validation.

This creates a distinction between two forms of productivity:

1. **local code productivity**, describing how quickly an agent produces a candidate change; and
2. **system-level development productivity**, describing how efficiently the complete workflow produces a correct, reviewable, recoverable, and accepted change.

Agentic harnesses attempt to improve system-level productivity by introducing durable tasks, specialized agents, reusable skills, deterministic tools, validation gates, and human checkpoints. These structures may improve reliability, but they may also create excessive process ceremony. Without telemetry, it is difficult to distinguish productive governance from overhead.

Examples of observable harness friction include:

- multiple equivalent subagent assignments;
- repeated or nested reviews;
- malformed generated shell pipelines;
- broad repository searches when an authoritative command exists;
- repeated validation with identical inputs;
- excessive loading of historical evidence;
- failure to reconstruct state from durable records;
- unnecessary human clarification;
- large control-plane diffs for small implementation changes;
- long finalization phases after the implementation already passes focused checks.

The central premise of this proposal is that these phenomena can be measured as properties of an executable development process.

## 2. Research problem

Current evaluations of coding agents commonly emphasize benchmark completion, generated-code correctness, pass rates, or model cost. These outcomes do not fully characterize an agentic development harness operating over a persistent research-software repository.

A harness is not merely a code generator. It is a control system that:

- reconstructs project state;
- selects work;
- assigns authority;
- dispatches agents;
- invokes tools;
- validates results;
- requests human decisions;
- records durable state;
- recovers from interruption;
- determines when work should stop.

The research problem is therefore:

> How can the efficiency, determinism, recoverability, and human burden of an agentic software-engineering harness be measured from its observable execution?

A related engineering problem is:

> Which harness structures convert repeated language-model judgment into reliable executable operations, and which structures merely relocate complexity into process artifacts?

## 3. Central hypothesis

The primary hypothesis is:

> Replacing prose-reconstructed operations with explicit DataObjects, deterministic ActionObjects, maintained commands, durable state, and bounded delegation will reduce duplicate work and human process intervention without reducing software correctness.

This hypothesis is decomposed into measurable claims.

### H1: Command determinism

Maintained commands and ActionObjects will reduce:

- ad hoc shell-command frequency;
- malformed commands;
- repeated command execution;
- broad repository searches;
- command-output volume.

### H2: Delegation efficiency

Durable role definitions and bounded dispatch will reduce:

- duplicate subagent assignments;
- nested delegation;
- unused subagent results;
- review repetition;
- agent waiting time.

### H3: State recoverability

Explicit task, run, and handoff records will reduce:

- context-reconstruction attempts;
- session-memory dependence;
- inter-session communication;
- recovery time;
- missing-state blocks.

### H4: Proportional process

Simplified skills and control records will reduce:

- control-plane amplification;
- review-to-change ratio;
- correction cycles caused by process misunderstandings;
- time between passing implementation checks and task completion.

### H5: Preserved correctness

Reductions in process overhead will not increase:

- introduced software defects;
- failed focused validation;
- scope violations;
- unsupported scientific claims;
- unrelated-work mutations.

### H6: Resource proportionality

Harness improvements that reduce elapsed time will not do so solely by consuming disproportionate model or computational resources. Candidate configurations will therefore be evaluated jointly in terms of:

- input, output, and tool-result tokens where observable;
- model and tool cost;
- parallel agent activity;
- verified-resolution probability;
- active harness time;
- human process burden.

## 4. Research questions

### RQ1

Which telemetry events are sufficient to reconstruct the operational history of an agentic software-engineering task?

### RQ2

Does replacing generated shell fragments with maintained ActionObjects and commands reduce command failure and repetition?

### RQ3

Does limiting delegation to demonstrably useful context isolation, specialization, independence, or parallelism reduce duplicate dispatch without weakening review quality?

### RQ4

Do durable task and handoff records improve continuation across sessions?

### RQ5

How much of total task time is attributable to implementation, validation, review, correction, state reconstruction, human waiting, and control-plane maintenance?

### RQ6

Which process metrics distinguish useful verification from unproductive ceremony?

### RQ7

Can harness efficiency improve while software-verification outcomes remain unchanged or improve?

### RQ8

Do reductions in elapsed time remain improvements after accounting for model-token consumption, monetary cost, parallel agent activity, and unsuccessful runs?

## 5. Conceptual model

A harness execution is modeled as a run

$$
\mathcal R
=
\left(
\mathcal T,
\mathcal A,
\mathcal C,
\mathcal V,
\mathcal H,
\mathcal O
\right),
$$

where:

- $\mathcal T$ is the durable task state;
- $\mathcal A$ is the sequence of agent actions and delegations;
- $\mathcal C$ is the sequence of tool and command invocations;
- $\mathcal V$ is the validation and review history;
- $\mathcal H$ is the sequence of human interventions;
- $\mathcal O$ is the final outcome.

The observable run is represented as an ordered event sequence

$$
\mathcal E_{\mathcal R}
=
(e_0,e_1,\ldots,e_{N-1}).
$$

Each event records a stable run identity, event type, actor, task identity, parent event, timestamp, duration where available, operation identity, status, and bounded metadata.

Metrics are deterministic functions of the event sequence:

$$
\mathbf m_{\mathcal R}
=
\mathcal S(\mathcal E_{\mathcal R}),
$$

where $\mathcal S$ is a run-summarization ActionObject.

For a single matched pair, two runs may be compared descriptively through

$$
\Delta\mathbf m
=
\mathbf m_{\mathrm{candidate}}
-
\mathbf m_{\mathrm{baseline}}.
$$

This comparison is meaningful only when task class, repository state, environment, validation requirements, and expected output are sufficiently comparable. Inferential analysis will operate over repeated controlled runs or matched task groups rather than treating a single run difference as evidence of a harness effect.

Harness performance is treated as a vector rather than collapsed into a single score:

$$
\mathbf p_{\mathcal R}
=
\left(
G_{\mathcal R},
T_{\mathrm{active}},
C_{\mathrm{task}},
B_{\mathrm{human}},
A_{\mathrm{control}}
\right),
$$

where:

- $G_{\mathcal R}$ indicates whether the run achieved a verified resolution;
- $T_{\mathrm{active}}$ is elapsed time excluding intervals blocked solely on human response;
- $C_{\mathrm{task}}$ is the observed computational and monetary cost;
- $B_{\mathrm{human}}$ is the measured human process burden;
- $A_{\mathrm{control}}$ is control-plane amplification.

A candidate configuration is a Pareto improvement when it improves at least one of these outcomes without worsening the remaining outcomes within the prespecified uncertainty and equivalence bounds.

## 6. Software architecture

### 6.1 Telemetry events as DataObjects

A telemetry event is immutable observed state:

```python
@dataclass(frozen=True, slots=True)
class HarnessTelemetryEvent:
    event_id: str
    run_id: str
    task_id: str | None
    parent_event_id: str | None
    agent_role: str
    event_type: HarnessTelemetryEventType
    occurred_at: str
    duration_ms: int | None
    status: str | None
    operation: str | None
    operation_identity: str | None
    input_bytes: int | None
    output_bytes: int | None
    input_tokens: int | None
    output_tokens: int | None
    tool_result_tokens: int | None
    cost_microunits: int | None
    cost_currency: str | None
    metadata: tuple[tuple[str, str], ...]
```

The event owns only intrinsic field invariants. It does not infer whether an operation was useful, correct, or efficient.

### 6.2 Summaries as ResultObjects

```python
@dataclass(frozen=True, slots=True)
class HarnessRunSummary:
    run_id: str
    outcome: str
    elapsed_ms: int
    dispatch_count: int
    duplicate_dispatch_count: int
    command_count: int
    maintained_command_count: int
    malformed_command_count: int
    correction_cycle_count: int
    human_intervention_count: int
    validation_count: int
    verification_eligible: bool
    verified_resolution: bool
    total_tokens: int | None
    total_cost_microunits: int | None
    cost_currency: str | None
    metrics: tuple[tuple[str, float], ...]
```

A summary is a ResultObject and therefore semantically a DataObject. It stores derived results without performing analysis itself.

### 6.3 Analysis as ActionObjects

```python
class RecordHarnessTelemetry:
    def execute(...) -> HarnessTelemetryRecordResult:
        ...
```

```python
class SummarizeHarnessRun:
    def execute(
        self,
        events: tuple[HarnessTelemetryEvent, ...],
    ) -> HarnessRunSummary:
        ...
```

```python
class CompareHarnessRuns:
    def execute(
        self,
        baseline: HarnessRunSummary,
        candidate: HarnessRunSummary,
    ) -> HarnessRunComparisonResult:
        ...
```

The comparison action calculates differences but does not decide whether the candidate harness should be accepted.

### 6.4 SQLite adapter

Raw telemetry will be stored in a local append-only SQLite database:

```text
.pi/runtime/harness-telemetry.sqlite3
```

The database will not be committed to version control and will not replace task, chain, checkpoint, or source authority.

A minimal event table is:

```sql
CREATE TABLE telemetry_event (
    event_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    task_id TEXT,
    parent_event_id TEXT,
    agent_role TEXT NOT NULL,
    event_type TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    duration_ms INTEGER,
    status TEXT,
    operation TEXT,
    operation_identity TEXT,
    input_bytes INTEGER,
    output_bytes INTEGER,
    input_tokens INTEGER,
    output_tokens INTEGER,
    tool_result_tokens INTEGER,
    cost_microunits INTEGER,
    cost_currency TEXT,
    metadata_json TEXT NOT NULL
);
```

Token and cost fields are nullable because historical artifacts and some runtimes do not expose reliable resource observations. Monetary values are stored as integer microunits with an explicit currency code rather than binary floating-point values.

SQLite provides persistence and querying. It does not determine authorization, task completion, software correctness, or human acceptance.

## 7. Telemetry domains

### 7.1 Temporal behavior

The study will measure:

- total elapsed time;
- active execution time;
- validation time;
- review time;
- correction time;
- human-wait time;
- agent-wait time;
- recovery time;
- time to first useful change;
- time to first passing focused check;
- implementation-to-closeout time.

Run time will be classified into mutually exclusive states:

$$
\begin{aligned}
T_{\mathrm{elapsed}}
={}&
T_{\mathrm{implementation}}
+T_{\mathrm{validation}}
+T_{\mathrm{review}}
+T_{\mathrm{control}}\\
&+T_{\mathrm{closeout}}
+T_{\mathrm{recovery}}
+T_{\mathrm{agent\ wait}}
+T_{\mathrm{human\ wait}}.
\end{aligned}
$$

An interval must be assigned to exactly one state. Human-wait time therefore cannot simultaneously be counted as review, control, or closeout time.

Active harness time is

$$
T_{\mathrm{active}}
=
T_{\mathrm{elapsed}}
-
T_{\mathrm{human\ wait}}.
$$

Two process-ceremony fractions will be reported:

$$
f_{\mathrm{ceremony,wall}}
=
\frac{
T_{\mathrm{control}}
+
T_{\mathrm{review}}
+
T_{\mathrm{closeout}}
}{
T_{\mathrm{elapsed}}
},
$$

and

$$
f_{\mathrm{ceremony,active}}
=
\frac{
T_{\mathrm{control}}
+
T_{\mathrm{review}}
+
T_{\mathrm{closeout}}
}{
T_{\mathrm{active}}
}.
$$

These measures must be interpreted with task class: public-contract or scientific work may legitimately require more review than a routine refactor. Neither fraction alone establishes that an activity is waste. Review and control activity will be classified as ceremony only when it produces neither a product-state change nor new assurance, authorization, recovery, or decision evidence.

### 7.2 Delegation behavior

The study will measure:

- total dispatches;
- unique dispatches;
- duplicate dispatches;
- writer, reviewer, and advisory assignments;
- redispatches;
- nested dispatches;
- cancelled or timed-out dispatches;
- unused returned results;
- incomplete handoffs;
- integration conflicts.

Dispatch efficiency is

$$
\eta_{\mathrm{dispatch}}
=
\frac{
N_{\mathrm{unique\ dispatches}}
}{
N_{\mathrm{total\ dispatches}}
}.
$$

### 7.3 Command behavior

The study will measure:

- total commands;
- maintained-command calls;
- ad hoc shell commands;
- inline Python and heredoc commands;
- broad repository searches;
- malformed commands;
- failed commands;
- repeated commands;
- retried commands;
- command duration;
- output bytes loaded into context.

Maintained-command coverage is

$$
\eta_{\mathrm{command}}
=
\frac{
N_{\mathrm{maintained\ command\ calls}}
}{
N_{\mathrm{total\ command\ calls}}
}.
$$

### 7.4 Context behavior

Where runtime hooks expose the required observations, the study will measure:

- input and output tokens;
- tool-result tokens;
- peak context utilization;
- duplicated context;
- historical-record context;
- skill and agent-prompt context;
- context reconstruction frequency;
- truncated outputs.

These metrics will be marked unavailable rather than estimated when the runtime does not expose reliable token information.

For contemporaneously instrumented runs, total observed task cost is

$$
C_{\mathrm{task}}
=
C_{\mathrm{input}}
+
C_{\mathrm{output}}
+
C_{\mathrm{tool}}
+
C_{\mathrm{compute}}.
$$

For a matched baseline and candidate using comparable models and pricing records, token amplification is

$$
A_{\mathrm{token}}
=
\frac{
N_{\mathrm{tokens,candidate}}
}{
\max\left(1,N_{\mathrm{tokens,baseline}}\right)
}.
$$

Token amplification will not be interpreted across configurations with materially different token accounting, model families, or unavailable runtime observations.

### 7.5 Change and scope behavior

The study will measure:

- unique files read and modified;
- source, test, documentation, evidence, and control-plane files changed;
- lines added and removed;
- files edited repeatedly;
- unrelated paths touched;
- unauthorized write attempts;
- reverted edits;
- residual temporary files.

File-count control-plane amplification is

$$
A_{\mathrm{control}}
=
\frac{
N_{\mathrm{control\ files\ changed}}
}{
\max(1,N_{\mathrm{source+test\ files\ changed}})
}.
$$

Net-diff amplification is

$$
A_{\mathrm{control,net}}
=
\frac{
L_{\mathrm{control}}^{+}
+
L_{\mathrm{control}}^{-}
}{
\max\left(
1,
L_{\mathrm{source+test}}^{+}
+
L_{\mathrm{source+test}}^{-}
\right)
},
$$

where $L^{+}$ and $L^{-}$ are added and removed lines in the delivered diff. Cumulative churn amplification is

$$
A_{\mathrm{control,churn}}
=
\frac{
\sum_e B_{\mathrm{control},e}
}{
\max\left(
1,
\sum_e B_{\mathrm{source+test},e}
\right)
},
$$

where $B_{x,e}$ is the number of bytes modified by edit event $e$. Net amplification measures delivered control-plane surface, whereas churn amplification measures the operational effort expended producing it. None of these metrics implies that control-plane changes are unnecessary; each identifies runs requiring qualitative inspection.

### 7.6 Validation and review behavior

The study will measure:

- distinct validation invocations;
- duplicate validation;
- focused and full test counts;
- introduced, pre-existing, environmental, and flaky failures;
- validation time;
- material review findings;
- duplicate or inapplicable findings;
- correction passes;
- review loops;
- reviewer independence;
- finding disposition.

### 7.7 State recovery

The study will measure:

- state-reconstruction attempts;
- successful durable reconstruction;
- missing-artifact blocks;
- session-memory fallback;
- inter-session recovery attempts;
- handoff-based continuation;
- stale-record conflicts;
- manifest drift;
- recovery time;
- lost-work events.

Recovery efficiency is

$$
\eta_{\mathrm{recovery}}
=
\frac{
N_{\mathrm{successful\ durable\ recoveries}}
}{
N_{\mathrm{recovery\ attempts}}
}.
$$

### 7.8 Human burden

The study will measure:

- genuine human decisions;
- clarification questions;
- avoidable clarification questions;
- human corrections;
- prompt restarts;
- process-friction interventions;
- technical or scientific interventions;
- human messages per task;
- decision latency;
- human-review surface.

The objective is not to eliminate human involvement. The desired outcome is to concentrate human effort on scientific meaning, architecture, authorization, and acceptance rather than recoverable operational details.

## 8. Primary outcome measures

To avoid an unmanageable analysis, the primary evaluation will use five outcome families:

1. **Verified resolution:** verification-floor eligibility, verified-resolution rate, and final acceptance outcome.
2. **Time:** total elapsed time, active harness time, and time from first passing focused validation to completion.
3. **Resource cost:** total tokens and monetary cost per run where contemporaneous runtime observations are available.
4. **Human burden:** human corrections, process-friction interventions, genuine human decisions, and human-review surface.
5. **Process proportionality:** active ceremony fraction, net control-plane amplification, and cumulative control-plane churn.

Cost per verified resolution is defined over a set of runs as

$$
C_{\mathrm{verified\ resolution}}
=
\frac{
\sum_{r=1}^{N} C_r
}{
N_{\mathrm{verified,accepted}}
}.
$$

The numerator includes unsuccessful and verification-ineligible runs. This prevents a configuration from appearing inexpensive by failing early or omitting required verification. If no run reaches verified acceptance, the cost per verified resolution is undefined and the zero-success outcome is reported directly.

Token and monetary-cost measures are conditionally primary: they are primary for contemporaneously instrumented runs with complete and comparable runtime accounting, and explicitly unavailable otherwise.

Secondary diagnostic measures include dispatch counts, duplicate dispatch ratio, returned-result utilization, maintained-command coverage, ad hoc shell ratio, malformed and repeated command counts, command-output volume, correction cycles, review loops, reconstruction attempts, and durable-recovery success. These explain why a primary outcome changed but do not replace the primary outcomes.

## 9. Experimental design

### 9.1 Study design

The project will use a staged within-repository comparison.

Each experimental unit is a bounded software-engineering task. Tasks will be grouped by class:

- routine software correction;
- public-contract implementation;
- test-evidence migration;
- harness maintenance;
- documentation synchronization;
- read-only architecture decision.

Runs will be compared across harness configurations:

| Configuration | Description |
|---|---|
| Baseline | Historical prose-heavy agents and generated command reconstruction |
| Intermediate | Durable agents and simplified skills |
| Candidate | Durable agents, simplified skills, maintained ActionObjects, explicit telemetry, and bounded delegation |

### 9.2 Matched tasks

Where possible, comparison tasks will be matched by:

- task class;
- number of owned files;
- expected implementation size;
- validation surface;
- public-contract significance;
- requirement for human decisions;
- repository cleanliness;
- model and runtime configuration.

The same defect should not be solved twice with leaked knowledge. Instead, structurally comparable tasks or controlled synthetic tasks will be used.

### 9.3 Controlled repeated tasks

Synthetic or seeded repository fixtures will be reset to an identical starting revision and executed independently under each harness configuration. Each run will use:

- an isolated repository snapshot;
- a fresh agent session;
- a fixed model and runtime configuration within the comparison;
- the same task specification and verification floor;
- no cross-run handoff or solution artifact;
- randomized or counterbalanced configuration order where feasible.

The pilot will target at least five independent repetitions per controlled task and configuration when resource limits permit. If fewer repetitions are feasible, the study will label the result exploratory and use it primarily to estimate trajectory variance rather than to support a configuration-effect claim.

For task instance $i$, configuration $c$, and repetition $r$, the analysis model is

$$
m_{icr}
=
\mu
+
\alpha_c
+
\beta_i
+
(\alpha\beta)_{ic}
+
\varepsilon_{icr},
$$

where $\alpha_c$ is the configuration effect, $\beta_i$ is task-instance difficulty, $(\alpha\beta)_{ic}$ is their interaction, and $\varepsilon_{icr}$ contains run-to-run trajectory variation.

### 9.4 Natural repository tasks

Real repository defects and feature tasks will not ordinarily be repeated after their solutions become known. They will instead be analyzed as matched groups of structurally comparable tasks. Configuration assignment will be randomized or counterbalanced where operationally possible, and the analysis will record:

- prior agent and human exposure to the task class;
- repository revision and cleanliness;
- model and runtime identity;
- task and validation surface;
- human-decision requirements;
- contemporaneous versus reconstructed telemetry.

These observations will support a matched observational analysis and will not be represented as equivalent to repeated controlled trials.

### 9.5 Controlled pilot task classes

Initial pilot tasks should include:

1. one DataObject invariant correction;
2. one ActionObject implementation;
3. one class-owned test correction;
4. one artifact-owned integration test;
5. one resource-manifest update;
6. one documentation-only synchronization;
7. one task-state reconstruction after a fresh session;
8. one bounded writer-plus-reviewer workflow.

### 9.6 Verification-floor gate

Each task instance $i$ will declare a required validation set before execution:

$$
\mathcal V_i^{\mathrm{req}}
=
\{v_{i1},v_{i2},\ldots,v_{ik}\}.
$$

Verification eligibility is

$$
G_i
=
\prod_{v\in\mathcal V_i^{\mathrm{req}}}
\mathbb I[v=\mathrm{PASS}].
$$

A run is a verified resolution only when $G_i=1$ and its prespecified scope, artifact, and acceptance requirements are satisfied. A run with $G_i=0$ remains in the dataset as an unsuccessful or verification-ineligible outcome. Its time, tokens, monetary cost, commands, and human burden remain part of configuration-level resource accounting, but it is excluded from duration summaries conditioned on verified success.

### 9.7 Baseline reconstruction

Historical runs may provide incomplete telemetry. They will be classified as:

- `contemporaneously instrumented`;
- `reconstructed from durable artifacts`;
- `partially reconstructed`;
- `unavailable`.

Reconstructed observations must not be represented as equivalent to contemporaneous runtime telemetry.

## 10. Analysis plan

### 10.1 Descriptive analysis

For each run, report:

- task class;
- starting and ending revisions;
- final outcome;
- verification-floor status;
- verified-resolution status;
- primary telemetry metrics;
- missing observations;
- material anomalies.

At the configuration level, report verified-resolution counts and proportions before reporting time or cost conditioned on success. Distributions will be reported using medians and interquartile ranges because task durations, token use, costs, and command counts are likely to be skewed. Resource totals will include unsuccessful runs.

### 10.2 Paired or matched comparison

For descriptive matched task pairs, calculate

$$
\Delta m_i
=
m_{i,\mathrm{candidate}}
-
m_{i,\mathrm{baseline}},
$$

for each metric $m_i$.

Relative change is

$$
\delta_i
=
\frac{
m_{i,\mathrm{candidate}}
-
m_{i,\mathrm{baseline}}
}{
\max(\epsilon,m_{i,\mathrm{baseline}})
},
$$

where $\epsilon$ prevents division by zero and must be reported.

Single-pair deltas will not be treated as estimates of a general configuration effect. Controlled repeated tasks will be analyzed using the task, configuration, interaction, and repetition structure defined in Section 9.3. Natural tasks will be analyzed separately using task-class matching and recorded covariates.

### 10.3 Uncertainty

With sufficient task repetitions, uncertainty will be estimated using:

- bootstrap confidence intervals for median differences;
- interval estimates for verified-resolution proportions;
- within-task estimates of stochastic trajectory variation;
- sensitivity analysis across task classes;
- separate reporting of wall-clock and active harness time;
- separate analysis for contemporaneous and reconstructed telemetry;
- separate analysis for complete and unavailable token or cost observations;
- robustness checks excluding outlier tasks.

The study will avoid strong causal claims if assignments are not randomized. The empirical analysis will report the joint outcome vector rather than construct an arbitrary scalar ranking. Pareto comparisons will be accompanied by uncertainty intervals and prespecified equivalence bounds.

### 10.4 Qualitative analysis

Quantitative metrics will be supplemented by coded failure modes:

- duplicate delegation;
- command reconstruction;
- stale-state use;
- manifest drift;
- excessive review;
- unsupported validation claim;
- ownership conflict;
- human correction;
- missing durable handoff.

This qualitative layer is necessary because low command count can reflect either efficiency or inadequate verification.

## 11. Verification, validation, and uncertainty boundaries

### 11.1 Software verification

Software verification will establish that:

- event DataObjects enforce their contracts;
- SQLite recording is lossless for represented fields;
- event ordering is deterministic;
- summaries reproduce analytically expected counts;
- duplicate-operation identities are detected;
- CLI and API results agree;
- explicit roots and paths are respected;
- private or sensitive payloads are not stored by default.

### 11.2 Numerical verification

Numerical verification will apply to derived metrics and aggregations. Controlled event sequences will provide exact analytical expected values for:

- durations;
- mutually exclusive time-state partitions;
- counts;
- ratios;
- duplicate rates;
- maintained-command coverage;
- correction cycles;
- net and churn control-plane amplification;
- token and monetary-cost aggregation;
- verification-floor eligibility;
- cost per verified resolution.

### 11.3 Empirical validation

Empirical validation will test whether the metrics correspond to observed harness behavior across real development tasks.

For example:

- duplicate-dispatch metrics should identify known repeated assignments;
- malformed-command counts should identify known shell failures;
- recovery metrics should distinguish successful durable reconstruction from session-memory dependence;
- ceremony metrics should identify long closeout phases;
- cost metrics should include unsuccessful and verification-ineligible runs;
- verification-floor outcomes should identify runs that skipped required validation.

### 11.4 Uncertainty quantification

Uncertainty arises from:

- variation in task difficulty;
- stochastic model behavior;
- finite repetitions within controlled task instances;
- incomplete runtime instrumentation;
- historical reconstruction;
- human response latency;
- differences in repository state;
- evolving harness versions.

These sources will be recorded and, where possible, separated rather than collapsed into a single performance score.

## 12. Privacy and research integrity

The telemetry system will not store by default:

- human prompt text;
- model response text;
- command output;
- file contents;
- credentials;
- environment variables;
- unpublished scientific data;
- personal communications.

It will store:

- event identities;
- operation categories;
- normalized operation hashes;
- durations;
- statuses;
- byte or token counts;
- bounded structured metadata.

The study will not represent telemetry as proof of:

- software correctness;
- scientific validity;
- model intelligence;
- general agent superiority;
- causal performance improvement without an appropriate design.

## 13. Expected contributions

The project is expected to produce:

1. an immutable telemetry event contract for agentic development;
2. a deterministic ActionObject architecture for event recording and summarization;
3. a local SQLite telemetry adapter;
4. a taxonomy of agentic software-process friction;
5. reproducible efficiency and determinism metrics;
6. a matched-task evaluation protocol;
7. empirical evidence concerning maintained tools versus prose-generated commands;
8. empirical evidence concerning bounded versus excessive delegation;
9. a verification-gated protocol for resource-aware harness comparison;
10. design guidance for human-in-the-loop scientific-software harnesses.

## 14. Risks and limitations

### 14.1 Hawthorne effect

Agents operating under telemetry may behave differently because instrumentation is present.

### 14.2 Task heterogeneity

Software tasks differ in difficulty, making direct comparison challenging.

### 14.3 Model stochasticity

Identical prompts may produce different behavior. Controlled repeated tasks will estimate this trajectory variance; natural repository tasks will not be treated as exact repetitions.

### 14.4 Incomplete runtime access

Repository-level instrumentation cannot observe every model call, token, or tool event unless the Pi runtime exposes hooks.

### 14.5 Metric gaming

An agent could reduce command count, elapsed time, or token use by skipping necessary verification. The prespecified verification-floor gate prevents such runs from being counted as verified resolutions. Their resource consumption and failure outcomes remain in the dataset rather than being discarded or replaced by an arbitrary penalty multiplier.

### 14.6 Historical-data quality

Past runs may be reconstructable only partially and must be labeled accordingly.

### 14.7 Repository specificity

Initial results will arise from one scientific-software repository and may not generalize immediately to other domains.

## 15. Work plan

### Phase 1: Telemetry contract

- Audit runtime hooks for model calls, tokens, costs, tool calls, agent dispatch, and context observations.
- Define event vocabulary.
- Define event, summary, and comparison DataObjects.
- Define ActionObject boundaries.
- Define privacy and explicit-input rules.
- Create controlled canonical fixtures.

### Phase 2: Local instrumentation

- Implement SQLite storage.
- Implement deterministic recording.
- Implement run summarization.
- Add task, command, validation, review, correction, and handoff events.
- Add a read-only summary CLI.

### Phase 3: Software and numerical verification

- Verify record invariants.
- Verify storage round trips.
- Verify aggregation using synthetic event sequences.
- Verify deterministic ordering and duplicate detection.
- Verify privacy exclusions.

### Phase 4: Pilot evaluation

- Execute repeated controlled development tasks from isolated repository snapshots.
- Compare baseline and simplified harness behavior.
- Estimate stochastic trajectory variance.
- Evaluate telemetry completeness.
- Refine metric definitions.

### Phase 5: Runtime integration

- Implement the model-call, token, cost, tool-call, agent-dispatch, and context hooks found to be reliable during the Phase 1 audit.
- Mark unsupported observations unavailable rather than estimating them.
- Preserve separation between repository state and runtime observations.

### Phase 6: Empirical study

- Execute a larger matched natural-task set with randomized or counterbalanced assignment where possible.
- Analyze primary and secondary metrics.
- Perform uncertainty and sensitivity analysis.
- Document qualitative failure modes.

### Phase 7: Publication and extraction

- Extract the generic telemetry layer into the reusable harness package.
- Publish the event schema, metric definitions, and analysis protocol.
- Prepare a paper on telemetry-guided deterministic agentic software engineering.

## 16. Proposed schedule

| Period | Work |
|---|---|
| Weeks 1–2 | Runtime-hook audit; event and metric contract |
| Weeks 3–4 | SQLite adapter and summary actions |
| Weeks 5–6 | Software and numerical verification |
| Weeks 7–8 | Controlled pilot tasks |
| Weeks 9–10 | Runtime instrumentation and refinement |
| Weeks 11–14 | Matched-task empirical study |
| Weeks 15–16 | Analysis, documentation, and manuscript draft |

## 17. Success criteria

The project will be considered successful if it produces:

- deterministic event recording;
- reproducible run summaries;
- no default storage of sensitive payloads;
- reliable identification of duplicate dispatch and malformed-command events;
- reliable separation of maintained and ad hoc commands;
- correct verification-floor classification;
- resource accounting that includes unsuccessful runs;
- empirical estimates of repeated-run trajectory variance;
- successful fresh-session reconstruction from durable state;
- measurable comparisons across matched tasks;
- no degradation in required software-verification outcomes;
- a documented account of which harness structures reduce friction.

A candidate harness improvement will be considered practically useful when it improves verified-resolution probability, active time, resource cost, human burden, or process proportionality without materially worsening the remaining outcomes or increasing defects, scope violations, or unsupported claims. Prespecified uncertainty and equivalence bounds will determine whether an apparent change is material.

## 18. Anticipated publishable claim

The strongest defensible initial claim is not that one harness is universally superior. It is:

> Agentic software-engineering process overhead can be represented as an observable event system, and harness configurations can be compared as verification-gated, multi-objective systems whose outcomes include resolution probability, active time, resource cost, state recoverability, and human process burden.

A stronger causal claim should be deferred until sufficient matched or randomized task evidence exists.

## 19. Proposed title alternatives

- **Measuring the Harness: Telemetry for Deterministic Agentic Software Engineering**
- **From Process Ceremony to Executable Control: An Event-Based Evaluation of Coding-Agent Harnesses**
- **Telemetry-Guided Design of Human-in-the-Loop Software-Engineering Agents**
- **Observable Agentic Development: Measuring Delegation, Determinism, and Process Overhead**
- **When Code Is Cheap, Measure the Process: Telemetry for Agentic Software Engineering**
