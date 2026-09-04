# Strict Python conformance migration

## Status and authority

**Status: authorized planning; implementation remains staged by existing Tasks.** The
current human instruction selects strict typing, explicit callable ownership,
class-owned pytest collection, repository-local test resources, and cost-bounded
artifact handling as project policy. `AGENTS.md` and
`docs/development/source-documentation.rst` own the project rules. This page maps
those rules onto existing canonical Tasks; it creates no new Task identity and does
not activate a successor.

The migration changes software structure and verification policy only. It establishes
no numerical verification, scientific validation, uncertainty quantification,
protected-execution authority, release status, or human acceptance.

## Target state

Every maintained Python module and test module satisfies the following project-local
conditions:

- precise concrete types, closed unions, protocols, and type parameters replace
  `Any`, `cast(Any, ...)`, erased containers, and generic `object` boundaries;
- encoded data has an exact representation type and a typed conversion into closed
  domain records;
- software values are not classified as trusted or untrusted by origin;
- every non-entry-point callable belongs to an explicit class owner;
- every collected pytest case belongs to an explicit `Test...` owner class, with
  setup, assertion, and fixture helpers owned as methods;
- only exact language-, packaging-, or framework-required hooks remain at module
  scope, and those hooks perform typed adaptation only;
- authored test-support resources reside beneath `python/tests/**/resources/`; and
- large text and binary artifacts are passed by blob marker, attachment reference, or
  path plus content identity and are inspected through structured metadata or bounded
  ranges.

These are project-local restrictions. Generic harness parsing may represent broader
Python syntax, but the project profile applies the stricter policy. Existing violations
are migration inputs, not compatibility promises or exceptions.

## Stages and existing Task owners

| Stage | Existing Task owner | Planned result |
|---|---|---|
| 0. Policy and agent alignment | `migration.v2` and `migration.v2.pi.agents` | Record the project rules and assign later descriptor/source/test enforcement without claiming that current code already conforms. |
| 1. Typed validation foundation | `migration.v2.harness.validation` | Supply strictly typed closed validation results needed by conformance reporting without introducing `Any`, generic `object`, or dangling helpers. |
| 2. Project conformance enforcement | `migration.v2.harness.conformance` | Parse class-owned pytest methods and helpers, reject prohibited module-level callables, detect prohibited typing forms, enforce test-resource placement, and report exact project-profile findings without rewriting source. |
| 3. Inward package migration | `migration.v2.periodic`, `migration.v2.ksdft`, `migration.v2.operators-ownership`, `migration.v2.persistence`, and `migration.v2.petrinet.colored` | Migrate foundational records, serializers, operations, and their tests while preserving accepted scientific, numerical, public, and wire contracts. |
| 4. Analysis pilot | `migration.v2.analysis.implementation-verification` | Convert the private aligned-band comparison slice and its periodic inputs/tests first, then verify the exact synthetic oracle and fail-closed behavior under the strict rules. |
| 5. Composed domain migration | `migration.v2.workflows.contract-verification` and `migration.v2.calculators.contract-verification` | Migrate Workflow and calculator composition only after inward owners and conformance enforcement are available. |
| 6. Outer-boundary migration | `migration.v2.integration.quantumespresso.verification`, `migration.v2.campaigns.definitions`, `migration.v2.application.verification`, and `migration.v2.pi.agents.verification` | Migrate integrations, definitions, application composition, and verify that every enabled project agent applies the root rules, all without external scientific execution. |
| 7. Aggregate completion | `migration.v2` | Require zero unresolved project-profile strict-conformance findings over the maintained source/test inventory before aggregate closeout. |

Parent relationships remain containment only. Added Task prerequisites name actual
migration gates; they do not imply source-package imports or grant implementation
authority.

## Enforcement sequence

`migration.v2.harness.conformance` introduces enforcement in this order:

1. extend parser facts to retain enclosing test-class identity, method decorators,
   method documentation, helper ownership, and exact module-level hooks;
2. add controlled positive and negative fixtures for class-owned tests, owned helper
   methods, prohibited top-level tests/helpers, `Any`, `cast(Any, ...)`, generic
   `object` annotations, erased containers, and misplaced authored resources;
3. apply the strict prohibitions through the project profile rather than silently
   changing generic policy behavior;
4. preserve stable evidence identifiers while changing only callable ownership;
5. report existing violations fail-closed without automatically editing them; and
6. synchronize the maintained module inventory and control projections only after the
   exact candidate source state passes structural validation.

The parser must not infer semantic ownership from a class name alone. Explicit test
ownership metadata remains authoritative, and class structure supplies callable
placement rather than scientific meaning or acceptance.

## Typing gates

Typing migration proceeds from narrow to broad:

1. changed source and tests pass targeted mypy with no new `Any`, generic `object`, or
   erased-container flow;
2. each migrated package passes its complete configured mypy scope;
3. cross-package verification Tasks pass their composed typed interfaces; and
4. `migration.v2` aggregate closeout enables and passes the repository-wide strict
   gate.

Do not enable a repository-wide flag merely to create thousands of undifferentiated
failures, and do not suppress a package wholesale. Negative runtime-type evidence may
use only the narrowest code-specific suppression at the exact intentionally invalid
call. The case data remains a closed union, and production signatures are never
widened for a test.

## Callable migration

For each migrated module:

1. assign every intrinsic check to its DataObject or ResultObject;
2. assign policy, transformation, comparison, validation, serialization, and I/O
   adaptation to the applicable ActionObject or adapter;
3. move mechanical helpers to private, static, class, or instance methods of that
   owner;
4. retain a module-level callable only for an exact framework or packaging hook and
   document that owner; and
5. group pytest methods and their helpers under the narrowest explicit `Test...`
   class without changing evidence identifiers or test meaning.

A class must own coherent behavior; migration must not create nominal utility classes
or hide scientific policy merely to eliminate a free function.

## Resources and large artifacts

Authored ownership files, compact fixtures, parser cases, and other test-support inputs
move beneath the applicable `python/tests/**/resources/` directory. Runtime scratch
continues to use framework-provided isolated temporary paths and is never treated as a
maintained input.

Large text and binary files are not copied into tests, prompts, logs, or review prose.
Tests and agents use blob markers, attachment references, or path-plus-content-identity
records and inspect only the required structured metadata or bounded ranges.

## Verification and closeout

Each stage runs the cheapest affected structural and typing checks first, followed by
its Task-owned focused tests, package tests, Harness validation, projection checking,
and documentation build where applicable. Full-suite pytest is an integration gate,
not a substitute for strict typing or callable-ownership checks.

A stage closes only when its exact Task criteria and prerequisites are satisfied. No
stage may weaken typing, add blanket ignores, move scientific behavior to a utility
owner, renumber unchanged evidence, fabricate provenance, or activate the next stage
automatically.

## Rollback and limitations

Before aggregate cutover, rollback restores the last accepted module structure and
project-profile enforcement revision without changing scientific contracts, wire
versions, or evidence meaning. The migration may expose pre-existing typing or
ownership defects; those findings remain explicit and do not justify a compatibility
alias or suppression.

The plan does not yet claim that current source or tests conform. It authorizes bounded
migration through the named existing Tasks only; implementation and administrative
closeout remain separately governed by each Task.
