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

Human checkpoints
-----------------

Human checkpoints are mandatory for scientific meaning, mathematical
conventions, public API decisions, serialization compatibility, architecture,
backward compatibility, project scope, acceptance of unresolved validation
failures, and final task acceptance. Agent summaries and passing checks do not
replace human acceptance records.

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

The ``choose-next-task`` skill is designed to work without chat history. It
reconstructs state from ``AGENTS.md``, task records, chains, skills, agents,
source, tests, specifications, documentation, integration-review evidence, and
version-control status. Graphify may accelerate broad topology questions, but
any graph-derived conclusion must be verified against authoritative files before
it affects a recommendation.

Final human authority
---------------------

Agents may recommend, implement approved changes, run checks, and report risks.
The human PI remains final authority for scientific and architectural meaning and
for final acceptance.
