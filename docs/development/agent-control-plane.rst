Agent control plane
===================

The agent control plane records how humans and agents coordinate work in the
repository. It is operational guidance, not a scientific specification.

Authority and roles
-------------------

Apply authority in this order: current human instruction and durable human
decisions; accepted scientific and public contracts; root and scoped
``AGENTS.md`` files; active chain, task, checkpoint, and ownership records;
applicable skills and procedural documentation; then derived reports and
historical evidence. Lower-level records may add compatible detail but may not
silently override higher authority. Historical evidence records what happened
and does not govern current work.

The root ``AGENTS.md`` owns stable repository policy. Mutable state belongs in
``.pi/chains/``, ``.pi/tasks/``, ``.pi/checkpoints/``, and durable human-decision
records rather than in constitutions or explanatory documentation. In the
validated project environment, both Codex and pi discover repository-local
skills under ``.agents/skills/``. pi additionally discovers pi-specific skills
under ``.pi/skills/``. A project skill may shadow a same-named global pi skill.
Codex configuration or hooks belong under ``.codex/`` only when explicitly
approved.

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

Durable Git decision boundaries
-------------------------------

A genuine human checkpoint is a version-control boundary, not merely a local JSON
state. Before presenting a blocking checkpoint, the agent completes the bounded
pre-checkpoint validation, commits the coherent task state together with the
pending checkpoint, and pushes that commit to the active task branch. The task
then waits. If commit or push fails, the agent reports the failure and remains
blocked; an unpushed local checkpoint is not a durable shared rollback anchor.

When the human answers unambiguously, the agent preserves the response, updates
the checkpoint and linked control records, and runs the resolution validation.
It then commits and pushes that resolution as a separate decision boundary before
resuming the newly authorized work. A human-accepted final checkpoint is handled
the same way before task closure is reported.

The same rule applies when the human incrementally clarifies and explicitly
accepts a coherent bounded change without creating a formal checkpoint. After
validation, that accepted increment receives its own commit and push before
unaccepted work continues. Routine discussion, progress narration, failed
experiments, and unaccepted work do not create decision-boundary commits.

Each boundary commit identifies the task and checkpoint or accepted increment.
It contains only validated in-scope state and excludes unrelated or unaccepted
changes. Once pushed, it is not amended, squashed away, rebased, or otherwise
rewritten. Restoration normally uses a revert commit or a new branch from the
accepted boundary; destructive reset or force-push requires explicit human
approval. These standing commit-and-push rules apply only to the active task
branch and do not authorize direct pushes to ``main``, merges, tags, releases, or
publication.

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
implement public rules, but must not hide scientific semantics. Documentation
and completion gates are proportional: public contracts, scientific or
numerical meaning, units, assumptions, serialization, and non-obvious invariants
require complete treatment; private mechanical helpers and obvious local state
need documentation only when it improves understanding.

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

Every new agent session reconstructs state by inspecting, in order, unresolved
checkpoint records, the controlling chain, the task records referenced by the
chain or checkpoints, and the latest durable human decisions. Those records are
authoritative over summaries and explanatory documentation. If the current
human message resolves a persisted checkpoint, the session records the decision
and resumes only the authorized incomplete work without requiring the human to
paste the previous checkpoint report. If a checkpoint was already resolved, the
decision is not requested again.

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

A machine-readable ownership manifest and fail-closed launch preflight are
required when an accepted task requires them, multiple agents write
concurrently, protected source and independent verification must be separated,
or conflicting or high-risk path ownership exists. Ordinary bounded work may
use one writer for source, tests, and documentation. When the control applies,
the controlling record names the manifest and runs
``python .pi/task-ownership/validate_task_ownership.py --task <TASK_ID>`` before
covered work starts; invalid declarations block only that manifest-governed
launch.

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
