---
document_id: ksdft2effmass.harness.002.001.005
task_id: harness-simplification.agents.project-architecture
parent: ksdft2effmass.harness.002.001.000
status: current
sphinx: excluded
---

# Simplify durable project roles

## Completed capability set

The bounded project-role simplification stage is complete. All five durable
project identities remain present, with unchanged access modes and lifecycle,
but their current records describe reusable capability and authority boundaries
rather than the history, file layout, commands, or procedure of a particular
task.

| Role | Access | Retained durable responsibility |
|---|---|---|
| [`ksdft2effmass-tests`](../../.pi/agents/ksdft2effmass-tests.md) | Writer | Independently check task-assigned accepted public contracts and documented invariants, use independent oracles when available, and classify software verification, numerical verification, scientific validation, and uncertainty quantification without overstating evidence. |
| [`ksdft2effmass-implementation`](../../.pi/agents/ksdft2effmass-implementation.md) | Writer | Implement accepted public contracts on explicitly assigned production-source paths while preserving APIs, serialization, compatibility, architecture, dependency direction, and applicable data/action boundaries. |
| [`ksdft2effmass-documentation`](../../.pi/agents/ksdft2effmass-documentation.md) | Writer | Maintain explicitly assigned project documentation consistently with accepted contracts, implemented behavior, authoritative conventions, supported public interfaces, and accurate claim status. |
| [`ksdft2effmass-integration-reviewer`](../../.pi/agents/ksdft2effmass-integration-reviewer.md) | Read-only | Independently review materially affected assigned surfaces and connecting interfaces, report exact material findings, and fail closed on authority, contract, ownership, evidence, or human-decision conflicts. |
| [`ksdft2effmass-architecture`](../../.pi/agents/ksdft2effmass-architecture.md) | Read-only by default | Provide proportionate project architecture analysis and human decision support for explicitly task-authorized work, remaining independent of implementation and human acceptance; write only narrow documentation or decision records under exact task ownership. |

Each role still requires an active authorized task and explicit path ownership or
review scope. Durable records own capability and stable boundaries; task and
ownership records supply paths, deliverables, permissions, validation, and any
supported subject skill. None may activate work, expand its assignment, choose
scientific meaning or a public contract, authorize protected execution, approve
its own work, or claim human acceptance.

## Architecture responsibility

The architecture role inspects only what is proportionate to the assigned
question. Depending on that question, relevant boundaries can include public
APIs, serialization, persistence, compatibility, dependency direction, external
systems, mathematical objects, and scientific representations. It separates
implemented behavior, proposed architecture, software verification, scientific
validation, and uncertainty quantification, and reports assumptions, risks,
questions, consequences, limitations, and any unresolved decision.

Read-only analysis is the default. Only an explicit task with exact ownership
may permit narrow documentation or decision-record writes; that exception does
not grant implementation, acceptance, or broader writing authority. When a
genuine human architecture choice exists, the role uses
`develop-architecture-decision` and presents exactly three materially distinct
defensible alternatives plus a reasoned recommendation without making the
decision. Deterministic, underspecified, unsuitable, and routine work does not
trigger an ADR or exactly-three-alternative requirement.

## Skill routing

Durable records retain only broadly reusable capability and boundary rules.
The architecture role now routes durably only to
`develop-architecture-decision`; its former universal OperatorRecord and CPN
specialization has been removed. Across the simplified project roles, a
subject-specific skill may be supplied only by an authorized task when routing
supports and requires it. An unsupported routing need is reported as a
limitation rather than solved by embedding permanent subject specialization.
Skill selection never expands task authority, path ownership, or review scope.

## Scope and remaining proposals

The five simplifications changed no agent identity, population total, historical
attribution, live-discovery behavior, harness execution behavior, tests,
retained evidence, scientific source, dependency, or protected-execution
authority. The architecture role remains read-only by default; its documented
narrow-write exception applies only under exact task ownership. Historical
records continue to identify work performed under their original assignments.
No executable was migrated in this task.

The executable-tool placement contract and validator migration pilot now have
durable Task records. Their current lifecycle, prerequisites, and successor
state belong to the
[harness-simplification chain](../../.pi/chains/harness-simplification.chain.json),
not this page; later work requires explicit activation. The accepted pilot scope
remained limited to one validator rather than a broad script migration. SQLite,
evidence-storage work, and later protected work remain outside this completed
project-role slice.

## Validation and rollback

Focused documentation validation checks exact front matter,
[harness.002.001.005](./ksdft2effmass.harness.002.001.005.md),
[harness.002.001.003](./ksdft2effmass.harness.002.001.003.md), relative links
across the four maintained pages, the unchanged inventory population totals,
the five project and five harness durable identities, absence of links to
nonexistent planned children, Sphinx exclusion, and whitespace errors. These
structural checks do not establish scientific validity or human acceptance.

Rollback of the final bounded slice restores the prior
`ksdft2effmass-architecture` record and any required capability registration,
then restores this page and the
[harness.001.005.000](./ksdft2effmass.harness.001.005.000.md) descriptions. It
does not undo the completed test, implementation, documentation, or
integration-review simplifications, rewrite historical agents or retained
evidence, or authorize any proposed successor.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [Create durable harness roles](ksdft2effmass.harness.002.001.004.md)
- **Next:** [Executable harness-tool placement contract](ksdft2effmass.harness.002.001.006.md)
