Agent control plane
===================

This page describes optional coordination for repository work. It is operational
guidance, not a scientific specification and not a prerequisite for ordinary
development.

Default: direct work
--------------------

An explicit human request authorizes ordinary bounded work directly. The agent reads
the relevant files, inspects the branch and working tree, makes the requested change,
runs proportionate checks, and reports the result.

Direct work does not require:

* a Harness Task or chain activation;
* checkpoint discovery or closeout;
* an ownership manifest;
* a mission, run record, handoff record, or completion packet;
* a retained evidence inventory;
* an independent reviewer or correction round; or
* a separate human-acceptance record.

The absence of those records is not a blocker. Historical records do not govern new
work unless the human request or a directly applicable durable decision selects them.

Managed work
------------

Use the managed control plane only when the human explicitly selects a Task or chain,
a directly applicable unresolved checkpoint exists, concurrent writers need path
ownership, or a protected action needs a durable decision record.

In that mode, inspect only the named chain, Task, checkpoint, ownership, workspace,
and handoff records. Do not recursively reconstruct unrelated project history. A
managed record may add compatible constraints but cannot override current human
instruction, accepted scientific contracts, or repository safety policy.

Human decisions
---------------

Ask for a human decision only when at least two materially different defensible
options remain and the choice affects scientific meaning, a public contract, project
scope, dependencies or licensing, external data transmission, destructive action,
protected computation, release, or another human-owned boundary.

Do not create checkpoints for deterministic corrections, formatting, ordinary test
failures, routine implementation choices, or administrative closeout. When a current
human response answers an existing unresolved checkpoint, use the
``resolve-human-checkpoint`` skill. Silence, elapsed time, passing checks, or reviewer
agreement never resolves a decision.

A checkpoint record is required for protected actions when root policy identifies an
applicable durable checkpoint, and when another decision must remain durable for later
managed work. It does not automatically require a case register, episode update, or
successor activation. A human-authorized managed administrative closeout does require
its exact validated commit and configured-upstream push under the Git boundary below;
no separate commit-and-push request is needed.

Ownership and delegation
------------------------

One writer may change source, tests, and documentation for ordinary bounded work.
Use an ownership manifest only for concurrent writers, a real path conflict, required
implementation/verification separation, or an explicitly managed Task.

A delegated writer reports its workspace, base and resulting state, changed paths,
checks, and unresolved risks. Persist a formal handoff only when later integration or
managed policy needs it. Reviewers remain read-only and cannot grant human acceptance
or protected authority.

Validation, review, and evidence
--------------------------------

Validation is proportional to the claim:

* routine changes use relevant unit, lint, type, or documentation checks;
* public contracts use appropriate compatibility and software-verification checks;
* numerical algorithms use numerical verification when making a mathematical claim;
* scientific validation and uncertainty quantification are required only for claims
  that need them.

Independent review is optional and risk-based. There is no mandatory
implementation-review-correction loop for ordinary work. Retained evidence records,
stable evidence identifiers, exhaustive prose, and generated inventories are used
only when an explicit claim-bearing evidence contract requires them.

A passing software check establishes only its stated software condition. It does not
establish scientific correctness, protected authority, release status, or human
acceptance.

Current technical harness surfaces
-----------------------------------

Process simplification does not remove or redefine implemented software contracts.
The project-local public package is ``ksdft2effmass.harness.pi.local``. It retains
explicit-root context composition, operational adapters, the project-local Task model,
and deterministic repository validation. Projection synchronization and checking are
private implementation behind the maintained ``harness_projection.py`` command.
A private canonical Python-conformance input resolver selects configured test modules,
the profile, and the predecessor map once. Repository validation consumes that
selection directly, while projection input construction composes it with the remaining
control inputs; projection code is not source authority for conformance.

The private synchronizer remains the sole publisher of maintained SQLite, SQL, the
projection manifest, and owned projections. The private check action reconstructs the
same candidate without publication and compares integrity, foreign keys, schema,
normalized content, SQL, manifest, and projections. Raw SQLite hashes are diagnostic.

``HarnessValidator`` returns the six ordered checks ``python_conformance``, ``resources``,
``task_graph``, ``checkpoints``, ``skills``, and ``control_state``. It does not execute
pytest, Ruff, mypy, or Sphinx. Its maintained renderer is
``python3 -m ksdft2effmass.harness.cli validate-harness --repository-root <ABSOLUTE_REPOSITORY_ROOT>``;
PASS or WARN returns zero, expected FAIL returns one, invalid input returns two, and an
unexpected command-boundary error returns three.

The generic and local resource manifests and ``ksdft2effmass.profile.v2`` retain their
implemented identities and dependency direction. The maintained resource command is
``python3 -m ksdft2effmass.harness.cli validate-local-harness-resources`` with explicit repository,
resource-root, profile, and manifest paths. Resource validation does not select or
activate work.

Project agent descriptors have a separate read-only structural check::

   python3 -m ksdft2effmass.harness.cli validate-agent-definitions \
     --repository-root <ABSOLUTE_REPOSITORY_ROOT> \
     --agent-root <ABSOLUTE_REPOSITORY_ROOT>/.pi/agents \
     --settings <ABSOLUTE_REPOSITORY_ROOT>/.pi/settings.json \
     --skill-root <ABSOLUTE_REPOSITORY_ROOT>/.pi/skills \
     --skill-root <ABSOLUTE_REPOSITORY_ROOT>/.agents/skills \
     --allowed-external-override gpt-pro

The check covers flat frontmatter structure, filename and runtime-name agreement,
tool-role compatibility, selected-skill availability, and stale disabled overrides.
It does not sandbox ``bash``, evaluate prompt quality, discover user-global agents,
measure runtime performance, or grant authority or acceptance.

Git and publication
-------------------

Do not stage, commit, or push unrelated or unaccepted work. Direct work requires an
explicit commit-and-push request. For managed work, explicit human authorization of
administrative closeout includes one commit containing only the validated accepted
boundary, a push to the current non-protected branch's already configured upstream,
and verification that local and remote commit identities agree. Closeout remains
incomplete if the push or identity check fails; retain and report the local commit
without amending, resetting, force-pushing, creating an upstream, or choosing another
remote. Closeout does not activate a successor.

Never rewrite shared history, force-push, merge to ``main``, tag, release, publish, or
archive without explicit human authorization and any applicable protected-action
safeguard.

Protected and scientific boundaries
------------------------------------

Process simplification does not relax scientific integrity or protected-action rules.
Do not fabricate calculations, validation, references, or capabilities. Preserve the
applicable specification, basis, gauge, units, geometry, and provenance conventions.
Production electronic-structure execution, external computation, destructive data
operations, dependency or licensing decisions, external data transmission, and
release actions still require explicit human authorization and the applicable durable
checkpoint required by root policy.

Historical records
------------------

Existing Tasks, chains, checkpoints, ownership files, reports, and evidence remain
historical or opt-in managed records. They need not be rewritten merely because direct
work is now the default, and they do not create new authority by their presence.
