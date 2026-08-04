Agent control plane
===================

The agent control plane records how humans and agents coordinate work in the
repository. It is operational guidance, not a scientific specification.

Current operator-record status
------------------------------

The operator-record validation-correction task was accepted and closed on
2026-08-03, and no operator-record corrective task is active. The periodic
KS/GKS electronic-structure and Quantum ESPRESSO architecture was approved on
2026-08-03 and is recorded in
``.pi/tasks/backend-neutral-kohn-sham-qe-architecture.md``,
``docs/architecture/kohn-sham-dft-quantum-espresso.md``, and
``docs/architecture/periodic-electronic-structure-integration.md``. Its
scientific object and adapter boundaries remain approved as prospectively
corrected. The never-launched
A--H linear workflow sequence is prospectively superseded by the project-owned
Colored Petri Net architecture and P0--P11 task program recorded in
``.pi/tasks/backend-neutral-cpn-workflow-architecture.md``. The human PI granted
final acceptance through ``CPN-HC01`` on 2026-08-03, and the architecture task
is closed. The human PI accepted bounded P0 as ``CONDITIONAL_PASS`` through
resolved ``P0-HC01`` on 2026-08-03 and closed it. Bounded P0A
packaging/configuration closed as human-accepted ``PASS``. P1 is the active
production-contract task and is blocked at unresolved ``P1-HC01`` for its
version-1 numeric wire contract. P2--P11 remain blocked, and no production
QE/ABINIT/Wannier execution is authorized.
Basis/state-space alignment remains a G01b work item, not a prerequisite of
G01a or G02, and is not active.

Authority and roles
-------------------

The root ``AGENTS.md`` is the authoritative repository instruction file. It
records scientific-integrity policy, architecture policy, validation policy,
branch and release constraints, and human authority. Repository-local pi control
files live under ``.pi/``. In the validated project environment, both Codex and
pi discover repository-local skills under ``.agents/skills/``. pi additionally
discovers pi-specific skills under ``.pi/skills/``. A project skill may shadow a
same-named global pi skill. Codex configuration or hooks belong under
``.codex/`` only when explicitly approved.

``.pi/tasks/`` contains durable task and decision records. ``.pi/skills/``
contains pi-specific skills with no shared equivalent. ``.pi/agents/`` and
``.pi/chains/`` describe pi subagents and chains. ``.agents/skills/`` contains
shared repository-local agent skills such as the manually installed Graphify
skill.

Decision classes and human checkpoints
--------------------------------------

The control plane separates three decision classes.

``deterministic_agent_correction``
   The task is already approved, the correction remains in scope, authoritative
   policy uniquely determines the correction, and no scientific meaning, public
   contract, external transmission, destructive action, or materially different
   defensible option remains. The agent records an agent-resolved corrective
   finding, corrects, revalidates, and continues without a human checkpoint.

``standing_delegated_decision``
   A durable human policy already resolves the choice. The agent cites that
   standing decision, acts, records the action, revalidates, and continues.

``genuine_human_decision``
   A checkpoint is required only when at least two materially different
   defensible options remain and the choice affects scientific meaning,
   physical or mathematical conventions, public API or serialization contracts,
   authoritative schemas, project scope, publication claims, external data
   transmission, privacy, dependencies or licensing, destructive or
   difficult-to-reverse actions, ownership conflicts, institutional or
   regulatory interpretation, resource-intensive computation, or conflicting
   authoritative instructions.

Human checkpoints are stored as JSON under ``.pi/checkpoints/`` and validated by
``.pi/checkpoints/checkpoint.schema.json``. They preserve the decision-bearing
human message, necessary context, normalized decision, consequences, and evidence
paths, but not complete chat transcripts. When the current human message answers
an unresolved checkpoint, the shared ``resolve-human-checkpoint`` skill records
and normalizes the decision, updates task and episode records, marks the
checkpoint resolved, identifies the authorized scope, resumes the blocked task,
reruns validation, and reports the result. Special phrases such as "record this
decision" or "resume" are not required. A bare "yes" resolves only one pending
checkpoint with one proposed approval.

Agent summaries and passing checks do not replace final human acceptance records,
but final-acceptance recordkeeping is administrative once the human gives
acceptance: the agent records acceptance, updates the case register, episode, and
active task, runs closeout validation, closes the task, and stops before starting
another task.

DataObject, ActionObject, and ResultObject policy
-------------------------------------------------

New or substantially refactored scientific software follows the repository
DataObject/ActionObject policy. DataObjects own represented data and intrinsic
invariants. ActionObjects own transformations, analyses, serialization, and
validation procedures. ResultObjects make operation outputs explicit. Production
Workflow objects are introduced only for genuine reusable scientific or
computational sequences; technical integrations do not require artificial
Workflow objects.

VVUQ evidence classes
---------------------

The control plane distinguishes software verification, numerical verification,
scientific validation, and uncertainty quantification. Software verification is
evidence that code satisfies its documented software contract. Numerical
verification is evidence that numerical algorithms implement or approximate the
stated mathematics. Scientific validation requires independent physical
reference evidence and a declared intended use. Uncertainty quantification
requires explicit uncertainty sources and propagation.

Agents must not classify constructor or schema rejection as scientific
validation. Passing software-verification or numerical-verification tests must
not be reported as scientific validation or UQ. When scientific validation or UQ
has not been performed, reports state that absence explicitly.

Public validation surfaces
--------------------------

Scientific invariants, conventions, transformations, approximations, and wire
formats require public documentation and independently executable validation
surfaces when they become part of the software contract. Examples include public
source docstrings, public schemas, valid and invalid fixtures, object tests,
Sphinx documentation, and integration review. Private methods may mechanically
implement public rules, but must not hide scientific semantics. Maintained-source
completion gates include complete public and private source documentation,
meaningful local-state comments, source/Sphinx synchronization, mathematical
symbol-to-field-name mapping, Python-version consistency, and read-only
documentation review with no unresolved material findings.

Graphify role
-------------

Graphify is optional repository intelligence. It can help agents understand
package topology, locate related objects and tests, inspect dependency or impact
questions, and support next-task candidate discovery. Its outputs are derived
and may be stale or incomplete. Graphify cannot approve architecture, establish
scientific validity, launch implementation work, or supersede human decisions,
task records, specifications, source, tests, fixtures, or human-reviewed
documentation.

Remote semantic processing, API-key configuration, hooks, global skill changes,
and committing generated graph artifacts require explicit human approval.
Generated ``graphify-out/`` artifacts are locally persistent and ignored unless a
curated report receives separate human review.

New-session state reconstruction
--------------------------------

Every new agent session must first inspect unresolved checkpoints under
``.pi/checkpoints/``, active accepted tasks, and the latest durable human
decisions. If the current human message resolves a persisted checkpoint, the
session records the decision and resumes the authorized incomplete work without
requiring the human to paste the previous checkpoint report. If a checkpoint was
already resolved, the decision is not requested again. If work was interrupted
after resolution, the session resumes from the recorded authorized step.

The ``choose-next-task`` skill is designed to work without chat history. It is
invoked only when no task or checkpoint remains active and the human asks for a
planning transition. It reconstructs state from ``AGENTS.md``, checkpoint and
task records, chains, skills, agents, source, tests, specifications,
documentation, integration-review evidence, and version-control status. Graphify
may accelerate broad topology questions, but any graph-derived conclusion must
be verified against authoritative files before it affects a recommendation.

Colored Petri Net workflow control
-----------------------------------

Static chain/task prerequisites remain useful planning and launch controls, but
they are not the scientific workflow state. The prospective scientific and
computational workflow is a stateful project-owned Colored Petri Net with typed
multiset markings, pure guards, request/result boundaries, failure/retry paths,
provenance lineage, and accepted marking predicates. SNAKES is the selected
candidate engine behind an adapter; neutral scientific objects and durable
markings remain project-owned.

Task-ownership launch preflight
-------------------------------

Every production task must record task-specific writers and independent
reviewers before implementation starts. The controlling chain names a
machine-readable ownership manifest and runs
``python .pi/task-ownership/validate_task_ownership.py --task <TASK_ID>`` as a
fail-closed launch preflight. Missing declarations, missing agent records,
overlapping writer scopes, combined writer/reviewer ownership, or an invalid
completion validator block launch.

Version 1 retains the P1 public-object inventory, exact test-module rule,
classified exceptions, non-class package/schema gate owner, and string command
for compatibility. Version 2 is generic, uses a structured completion-command
argument vector bound to the declared validator path, and does not impose P1
object kinds or filenames.

A version-2 task may opt into the exact ``evidence-branches-v1`` profile by
naming a validated repository-relative branch matrix and a correction-cycle
limit of one. Its structured authorization binds the same durable task record as
the manifest, a stable decision ID present in that record, and the exact profile.
Activation requires at least two branches and either multiple writer roles or a
deterministic/protected-checkpoint split. Every validation stage declares its
writer, command, requirements, and owned evidence; exactly one referenced
completion stage matches the manifest completion command and validator path.
Version-2 agent records establish agent identity and writer/read-only role, while
structured manifest paths establish ownership.

The matrix is authorization and ownership input, not an execution log or an
orchestration engine. Dispatchers batch all branches assigned to each writer
role, then request one consolidated independent review. They may run one
consolidated correction cycle and must escalate unresolved findings rather than
create an iterative writer/reviewer loop. This optional profile is not required
for ordinary tasks.

A launch-preflight pass establishes control-plane ownership only; it does not
establish implementation correctness, scientific validity, or human acceptance.
A direct tool or agent call can technically bypass the validator, but remains
unauthorized and supplies no preflight evidence.

Chain behavior
--------------

When a chain creates a genuine human checkpoint, the task waits in a durable
pending state. After a human response is received, the same parent task uses the
checkpoint-resolution policy to record the decision, clear the checkpoint, resume
work, route deterministic corrections, request read-only integration review, and
perform final verification. Deliberately failing commands must not be used merely
to simulate a human checkpoint unless the execution system technically requires
one; a durable pending checkpoint is sufficient.

Final human authority
---------------------

Agents may recommend, implement approved changes, run checks, and report risks.
The human PI remains final authority for scientific and architectural meaning and
for final acceptance.
