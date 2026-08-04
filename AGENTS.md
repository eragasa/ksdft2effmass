# AGENTS.md

## Project

`ksdft2effmass` is open-source research software for constructing and
validating reduced semiconductor Hamiltonians from first-principles
Kohn-Sham DFT calculations.

The initial application is substitutional phosphorus and boron in silicon. The
project investigates when an atomistic impurity Hamiltonian can be replaced by
a reduced lattice or continuum effective-mass model.

Read `README.md` and the files relevant to the requested task before making
changes. Mathematical definitions and computational dependencies belong in the
versioned research documents; do not introduce competing conventions here.

## Scope

The active program includes:

- bulk-silicon reference calculations;
- projected and Wannier Hamiltonians;
- tight-binding reductions;
- alignment of pristine and doped representations;
- impurity-operator extraction;
- lattice and continuum reductions;
- validation metrics and provenance.

Quantum ESPRESSO and Wannier90 remain responsible for the underlying
electronic-structure and Wannier calculations. Do not reimplement DFT or
Wannier localization in this package unless explicitly requested.

Do not expand a task into phonons, electron-phonon coupling, machine learning,
device simulation, or another material system without explicit authorization.

## Branches and releases

Active development occurs on `dev`.

The `main` branch contains the latest reviewed snapshot associated with a
conference, paper, or other formal research output.

Unless explicitly requested, do not:

- merge `dev` into `main`;
- push directly to `main`;
- create, move, or delete version tags;
- create a GitHub Release;
- publish a package;
- archive software or data;
- update a DOI;
- describe development work as reviewed or released.

Only signed semantic-version tags of the form

    vMAJOR.MINOR.PATCH

identify reviewed research-software releases.

Development branches, intermediate commits, pull requests, automated builds,
and continuous-integration artifacts are provisional.

## Scientific integrity

Never fabricate or silently infer:

- numerical results;
- completed calculations;
- convergence claims;
- validation results;
- literature values;
- references;
- quotations;
- DOIs;
- software capabilities.

Clearly distinguish among:

- calculated results;
- literature values;
- expected behavior;
- illustrative examples;
- synthetic test data;
- placeholders;
- proposed work.

Do not present a successful program execution as evidence of scientific
correctness.

Track these error sources separately:

- parent-model error;
- numerical or discretization error;
- model-reduction error.

Do not combine them into one error unless the mathematical relation and
compatible error definitions have been established.

## Mathematical conventions

Preserve the notation and definitions in the versioned mathematical
specification.

In particular:

- distinguish an operator from its finite matrix representation;
- state the domain and codomain when they matter;
- do not subtract operators acting on unidentified state spaces;
- align pristine and doped bases before direct matrix subtraction;
- make energy-zero and gauge conventions explicit;
- distinguish projection, disentanglement, basis transformation, and
  truncation;
- do not describe Wannierization alone as a low-rank approximation;
- do not identify Kohn-Sham eigenvalues with the complete many-body excitation
  spectrum.

If an existing convention is unclear or inconsistent, report the ambiguity
instead of silently selecting a new convention.

## Numerical calculations

Do not submit remote, cluster, cloud, or HPC jobs without explicit
authorization.

Before starting a potentially expensive calculation, report:

- the executable to be used;
- the input system;
- the expected computational scale;
- the anticipated outputs;
- the approximate runtime or resource requirement, when known.

Do not silently:

- replace pseudopotentials;
- change exchange-correlation approximations;
- change energy cutoffs or meshes;
- alter convergence tolerances;
- change crystal structures;
- change Wannier windows or projections;
- change energy-alignment conventions.

Such changes modify the scientific specification and must be documented.

## Data and provenance

Do not commit large electronic-structure outputs to Git.

Keep large wavefunction, density, restart, scratch, and dense matrix files
outside the repository. Version-control their:

- input files;
- manifests;
- checksums;
- software versions;
- physical and numerical settings;
- compact validation summaries;
- reproduction scripts.

Do not delete calculation data unless the exact target is known and deletion
has been explicitly requested.

Never expose credentials, access tokens, private keys, scheduler secrets, or
restricted data in code, logs, documentation, or commits.

## Software architecture

Keep language implementations conventional and separate. The current Python
source root is `python/src/ksdft2effmass/`; use `rust/crates/` if Rust crates are
introduced. Language-independent definitions belong in `specification/`; use
`fixtures/` when shared numerical fixtures are introduced. Follow
`docs/architecture/repository-layout.md`; do not create a competing source-tree
layout.

Python is the initial reference implementation. Language-independent operators,
state spaces, units, conventions, shapes, types, wire formats, metrics, and
tolerances belong in `specification/`; shared numerical cases belong in
`fixtures/`. Python and Rust APIs may differ syntactically but must preserve the
same scientific meaning, serialized data, and validation behavior.

Before implementing an existing Python component in Rust, retain the Python
reference, define shared expected results and tolerances, add cross-language
conformance tests, and document intentional algorithmic differences. Profile a
representative workload before moving performance code; do not rewrite efficient
NumPy/SciPy or BLAS/LAPACK operations without evidence. Rust components must
document ownership and memory-layout assumptions and include benchmarks when
performance is their justification. Prefer safe Rust; localize, justify,
document, and test any `unsafe` code.

### DataObject/ActionObject programming model

Apply this model to new code and substantial refactors, not unrelated stable
modules. Load `.pi/skills/design-data-action-objects/SKILL.md`; its referenced
architecture document owns the detailed rules.

Use concrete, composed objects without abstract DataObject or ActionObject base
classes:

```text
DataObject --ActionObject--> DataObject or ResultObject
```

- DataObjects own represented state, intrinsic invariants, canonicalization,
  exact value semantics, and trivial derived properties.
- ActionObjects own transformations, numerical policy, validation procedures,
  serialization, file or external boundaries, and orchestration.
- ResultObjects represent explicit operation outcomes.
- Workflows are concrete ActionObjects only for reusable scientific or
  computational sequences; do not invent them to own tests.

Keep nontrivial behavior with its domain owner; do not create generic utility
modules or hide policy in module-level validators. Maintained data and results
must be operationally immutable. Public numeric APIs must reject booleans and
numeric strings, document accepted scalar types and overflow behavior, and use
explicit units. Runtime behavior, typing, documentation, tests, schemas, and
Rust mappings must agree. New public models must remain translatable to concrete
Rust structs with explicit errors and deterministic versioned wire formats.

### Pi control plane and active-program snapshot

Repository control files live under `.agents/skills/` and `.pi/`; this file
owns global policy, while narrower skills and task records may add compatible
requirements. Mutable state is owned by the controlling chain, active task,
unresolved checkpoints, and latest durable human decisions—not by this
snapshot.

At this snapshot, P1, the bounded EVIDENCE-DOC-1 maintenance task, and harness
H0 are closed as human-accepted `PASS`. H1 alone is active after resolved
`H1-HC01` Option B for exactly one bounded `DiagnosticPath` contract correction
and return to final human acceptance; no implementation is authorized. The
remaining harness sequence is H3 -> H2 -> H4. After accepted H4, P2 and optional H5 each require their own
separate explicit human activation; H5 is not a P2 prerequisite. P2 requires
accepted P1, accepted H4, and explicit P2 activation. H3--H5, P2--P11, and all
production or scientific execution remain blocked.
Verify this against both `.pi/chains/backend-neutral-kohn-sham-qe.chain.json`
and `.pi/chains/pi-harness-incubation.chain.json` at session start and update
stale prose rather than following it. Read
`docs/architecture/colored-petri-net-workflows.md` and
`docs/architecture/periodic-electronic-structure-integration.md` before related
work. Architecture records define boundaries but do not authorize task launch or
execution.

At session start, inspect unresolved checkpoints, the controlling chain, the
active task, and latest durable human decisions. If the current human message
resolves a persisted checkpoint, follow
`.agents/skills/resolve-human-checkpoint/SKILL.md`, record the decision, resume
only authorized work, and revalidate. Never infer approval from silence or a
timeout.

Use `.pi/skills/choose-next-task/SKILL.md` only when no task or checkpoint remains
active and the human asks what is next. It is read-only, recommends exactly one
task, and must not create or launch work. Harness H0 is closed; H1 alone is
active only for the bounded contract correction recorded by resolved
`H1-HC01`. Do not infer implementation or successor activation from the
prospective pages under `docs/harness/`.

Decision handling and closeout procedures are defined in
`docs/development/agent-control-plane.rst`. In summary, agents may apply a
uniquely required in-scope deterministic correction or a standing durable human
decision. Pause for a genuine human decision when materially different options
affect scientific meaning, public contracts, scope, dependencies, external data
or execution, destructive actions, ownership, or acceptance. A checkpoint block
must be a validated commit pushed to the task branch before waiting for the
human. After an unambiguous resolution, record and validate the decision, commit
and push that resolution boundary, and only then resume authorized work. Apply
the same validated commit-and-push boundary whenever the human explicitly
accepts a coherent incremental change. Final acceptance must be recorded
durably, followed by closeout validation; stop before starting a successor task.

The human PI remains final authority for scientific meaning, mathematical and
physical conventions, public APIs and serialization contracts, backward
compatibility, architecture and project scope, acceptance of unresolved
validation failures, external or resource-intensive execution, and final
acceptance. Silence, timeout, or unavailability never implies approval.

### Repository skills and Graphify

Skills are agent capabilities, never scientific CPN guards or transitions.
Follow the applicable repository-local `SKILL.md`; deterministic commands own
software-gate pass/fail, reviewers own findings, parent verification checks
evidence completeness, and humans own protected decisions and acceptance.

Graphify is optional and read-only. Use
`.agents/skills/graphify/SKILL.md` only for an explicit Graphify request or a
broad topology, dependency, or impact question. Verify every material conclusion
against authoritative files. Graphify cannot approve architecture, establish
scientific validity, launch work, or record human decisions. Remote processing,
API-key configuration, hooks, global skill changes, or committing generated
outputs requires explicit human approval.

### Operator-record subsystem

The maintained Python package is `python/src/ksdft2effmass/operators/`; its
software- and numerical-verification evidence is under the corresponding VVUQ
subtrees of `python/tests/`. Historical layouts remain historical and must not be
recreated.

For operator-record work, load `.pi/skills/develop-operator-records/SKILL.md` and
follow its architecture reference, the active task record, and the maintained
pages under `docs/verification/`. Those records own the object inventory,
package decomposition, dependency direction, Hermiticity definition, comparison
semantics, serialization contract, detailed gates, and deferred alignment work.
Do not silently change those conventions or treat exact represented comparison
as basis, gauge, energy-zero, unit, geometry, or physical alignment.

## Testing and validation

Inspect `pyproject.toml`, existing workflows, and the relevant test tree before
choosing commands. Use established tools, run the cheapest relevant checks
first, and do not change expected values merely to obtain a pass. Diagnose
whether the implementation, fixture, method, or reference is wrong.

Keep VVUQ evidence classes distinct:

- software verification checks the documented software contract;
- numerical verification checks implementation of stated mathematics;
- scientific validation compares a model with independent reference evidence
  for a declared use;
- uncertainty quantification identifies and propagates uncertainty sources.

Constructor, schema, invariant, and deterministic tolerance checks do not by
themselves establish scientific validation or UQ. Report absent evidence
explicitly. Use explicit tolerances and state what they measure.

Place evidence under the corresponding subtree of `python/tests/` and migrate
only an approved object or subsystem at a time. Maintained migrated tests require
stable evidence identifiers, explicit requirements and oracles, acceptance and
failure interpretation, limitations, and correct evidence-class markers. Load
`.pi/skills/document-research-python/SKILL.md` and its shared test-evidence
reference for the unified class-owned and artifact-owned documentation grammar;
operator-record work additionally follows `.pi/skills/develop-operator-records/SKILL.md`.
Follow `docs/verification/testing-and-evidence.rst` for hierarchy, module
documentation, numerical-case, controlled-fault, and review requirements.

## Documentation

Use Markdown with LaTeX mathematics:

- inline mathematics: `$...$`;
- display mathematics: `$$...$$`.

Define symbols when introduced. Distinguish among:

1. the physical model;
2. the mathematical operator;
3. the numerical representation;
4. the software implementation.

Use direct technical prose. Avoid promotional language and unsupported claims.

### Source documentation standard

Maintained first-party Python must be auditable from source documentation.
Modules, public APIs, dataclass fields, private implementation owners, and
scientifically meaningful local state must document purpose, scope, units,
assumptions, invariants, canonicalization, equations, and validation boundaries
where applicable. Comments explain meaning, not assignments.

Use `TypeError` for wrong semantic types and `ValueError` for violated
invariants. Document accepted scalar types and canonicalization; do not accept
booleans as numbers or silently convert numeric strings unless the public
contract explicitly authorizes it.

Source, tests, schemas, fixtures, examples, and Sphinx pages must agree. Complete
warnings-as-errors documentation builds and read-only documentation review for
maintained-source tasks. Do not use Sphinx `:undoc-members:` to conceal missing
source documentation. Follow `docs/development/source-documentation.rst` for the
operational standard.

Verify references against primary sources before adding them.

Research plans, expected results, and proposed calculations must remain
visibly distinct from completed findings.

## AI-assisted work

Treat all agent-generated code, prose, equations, and analysis as provisional.

Do not describe AI-assisted work as reviewed, validated, or release-ready
unless the user explicitly authorizes a formal release.

When uncertainty remains:

- state the uncertainty;
- identify the assumption;
- identify what must be checked;
- avoid inventing a convenient answer.

## Task launch and ownership

Before any production-task implementation begins or resumes:

1. identify the active task from durable chain, task, checkpoint, and human-
   decision records;
2. require the controlling chain to name a task-ownership manifest;
3. require separate named implementation, test, and documentation writers and
   at least one independent read-only reviewer;
4. require each writer's path scope to be explicit and non-overlapping;
5. require a deterministic completion validator bound to its declared path;
6. for a version-1 manifest, additionally require the P1 compatibility inventory,
   exact test-module rule, dedicated object kinds, classified exceptions, and
   non-class package/schema gate owner;
7. run

   ```bash
   python .pi/task-ownership/validate_task_ownership.py --task <TASK_ID>
   ```

   and stop without editing if it fails.

Do not route production work to a generic or operator-specific agent unless the
validated manifest names that agent and its record explicitly covers the assigned
paths. Do not let one writer own both production source and tests. Writers must
run sequentially in a shared worktree, and tests must not validate partially
written production modules.

A test-layout rule is task-specific. Do not infer that one subsystem's facet
layout or `test__ClassName.py` convention applies to another subsystem. The
version-1 validator retains those P1 conventions only for compatibility; generic
version-2 validation does not impose them. The declared completion validator must
pass before independent review; reviewers must reject missing or incomplete
ownership evidence rather than attempting to repair the test architecture
retrospectively.

A version-2 task may opt into the exact `evidence-branches-v1` profile and its
approved branch matrix; the profile is not mandatory for ordinary tasks. The
matrix binds a durable authorization decision, activates only for at least two
branches with multiple writers or a deterministic/protected split, and declares
writer-owned validation stages with exactly one manifest-bound completion stage.
Version-2 agent records establish identity and writer/read-only role; structured
manifest paths establish ownership. For an enabled profile, consume the matrix
without recording execution results in it, batch all branches assigned to each
writer role, perform one consolidated review, allow one consolidated correction
cycle, and escalate remaining findings instead of spawning another loop. The
validator does not execute or dispatch branches.

This preflight establishes control-plane ownership only. It does not establish
implementation correctness, numerical verification, scientific validation,
uncertainty quantification, or human acceptance. A direct tool or subagent call
that technically bypasses the preflight remains unauthorized.

## Working procedure

For each task:

1. Read the relevant files and any more specific `AGENTS.md`.
2. Inspect unresolved checkpoints, the active task, latest durable human
   decisions, the current branch, and the working-tree state.
3. For production work, pass the task-launch and ownership preflight above.
4. Preserve unrelated user changes.
5. Identify the smallest change that satisfies the request.
6. Implement the change without expanding its scientific scope.
7. Run the cheapest relevant checks first, followed by all affected completion
   gates.
8. Report:
   - files changed;
   - checks performed;
   - assumptions introduced;
   - unresolved limitations;
   - scientific or expensive validations not performed.

Do not merge, tag, publish, submit external jobs, or otherwise perform an
external or release action unless explicitly requested. Commits and pushes to
the active task branch are additionally authorized—and required—at durable human
decision boundaries: before waiting at a genuine checkpoint, after recording its
resolution, and after explicit human acceptance of a coherent incremental
change. Include only validated, in-scope state; never mix unrelated or unaccepted
work into the boundary commit. Do not amend or rewrite a pushed decision-boundary
commit. Roll back by revert or by branching from the accepted commit; do not
reset shared history or force-push without explicit human approval. Direct
pushes to `main` remain prohibited.

## Definition of done

A task is complete when:

- the requested change is implemented;
- relevant checks pass;
- affected documentation is consistent;
- user work outside the task remains unchanged;
- assumptions and limitations are reported;
- no unsupported scientific claim has been introduced.
