Agent control plane
===================

The agent control plane records how humans and agents coordinate work in the
repository. It is operational guidance, not a scientific specification.

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

Public validation surfaces
--------------------------

Scientific invariants, conventions, transformations, approximations, and wire
formats require public documentation and independently executable validation
surfaces when they become part of the software contract. Examples include public
schemas, valid and invalid fixtures, object tests, Sphinx documentation, and
integration review. Private methods may mechanically implement public rules, but
must not hide scientific semantics.

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
