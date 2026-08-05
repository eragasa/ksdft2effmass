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

## Research scope

The program includes:

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

## Authority and repository state

Apply repository instructions in this order:

1. the current human instruction and durable human decisions;
2. accepted scientific and public contracts;
3. this root file and any applicable scoped `AGENTS.md`;
4. the active chain, task, checkpoint, and ownership records;
5. applicable skills and procedural documentation;
6. derived reports and historical evidence.

A lower-level record may add compatible detail but may not silently override a
higher-level decision. Historical evidence records what happened; it does not
govern current work. Architecture and planning records define boundaries but do
not by themselves authorize task launch or execution.

Do not store mutable task status in this file. At session start, reconstruct the
state from authoritative records in this order:

1. inspect unresolved records under `.pi/checkpoints/`;
2. inspect the controlling record under `.pi/chains/`;
3. inspect the task records referenced by that chain and any checkpoint;
4. inspect the latest durable human decisions; and
5. treat those records as authoritative over summaries and documentation.

If the current human message resolves a persisted checkpoint, follow
`.agents/skills/resolve-human-checkpoint/SKILL.md`. Never infer approval from
silence, timeout, an agent report, or a passing check. Use
`.pi/skills/recommend-next-task/SKILL.md` only when no task or checkpoint remains
active and the human asks what comes next; it is read-only and cannot launch
work.

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
- make basis, gauge, and energy-reference conventions explicit;
- distinguish projection, disentanglement, basis transformation, and
  truncation;
- do not describe Wannierization alone as a low-rank approximation;
- do not identify Kohn-Sham eigenvalues with the complete many-body excitation
  spectrum.

If an existing convention is unclear or inconsistent, report the ambiguity
instead of silently selecting a new convention.

## Numerical calculations and protected execution

Do not submit remote, cluster, cloud, or HPC jobs without explicit human
authorization and the applicable durable checkpoint.

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

QE or Wannier90 production execution; HPC, cloud, or remote jobs; destructive
operations; external data transmission; dependency or licensing decisions;
merges to `main`; tags, releases, publication, and DOI actions are protected.
They require explicit human authorization and the applicable durable checkpoint.

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
`fixtures/` for shared numerical fixtures. Follow
`docs/architecture/repository-layout.md`; do not create a competing source-tree
layout.

Python is the initial reference implementation. Python and Rust agreement is
required only for explicitly language-independent specifications, shared wire
formats, components approved for Rust implementation, or contracts whose active
task requires cross-language conformance. Before implementing an existing
Python component in Rust, retain the Python reference, define shared expected
results and tolerances, add cross-language conformance tests, and document
intentional algorithmic differences. Python-only internal objects require
conventional Python typing and tests, not speculative Rust design.

Profile a representative workload before moving performance code; do not rewrite
efficient NumPy/SciPy or BLAS/LAPACK operations without evidence. Rust
components must document ownership and memory-layout assumptions and include
benchmarks when performance is their justification. Prefer safe Rust; localize,
justify, document, and test any `unsafe` code.

Apply the DataObject/ActionObject programming model to new scientific object
models and substantial refactors, not unrelated stable modules. Its detailed
object-ownership and portability rules are owned by
`.pi/skills/design-data-action-objects/SKILL.md` and its architecture reference.

Keep nontrivial behavior with its domain owner; do not create generic utility
modules or hide scientific policy in module-level validators. Maintained data
and results must be operationally immutable. Public numeric APIs must reject
booleans and numeric strings unless the accepted contract states otherwise,
document accepted scalar types and overflow behavior, and use explicit units.
Runtime behavior, typing, documentation, tests, and applicable schemas or
cross-language contracts must agree.

## Process classes

Choose controls according to the highest-risk applicable class. An active,
accepted task may impose compatible additional controls.

### Routine software work

Examples include internal helpers, local refactors, documentation corrections,
ordinary unit tests, non-public validators, and deterministic bug fixes under an
accepted contract.

Normally require bounded scope, implementation, relevant tests, affected
documentation, and one review when materially useful. They do not automatically
require a task-ownership manifest; separate source, test, and documentation
writers; evidence identifiers; class-per-file tests; retained checksum catalogs;
human checkpoints; Rust mappings; VVUQ analysis; or multiple review rounds.

### Public-contract and persistence work

Examples include public APIs, schemas, serialized records, durable marking
formats, file or SQLite repository boundaries, and compatibility or migration
behavior.

Require an explicit contract, schema or fixture agreement where applicable,
software-verification tests, and compatibility review. A human decision is
required only when materially different defensible choices remain at a protected
boundary.

### Scientific or numerical work

Examples include mathematical algorithms, numerical approximations, convergence
procedures, physical-model comparisons, and scientific acceptance metrics.

Require only the evidence classes applicable to the claims made:

- software verification checks the documented software contract;
- numerical verification checks implementation or approximation of stated
  mathematics;
- scientific validation compares a model with independent reference evidence
  for a declared use;
- uncertainty quantification identifies and propagates uncertainty sources.

Do not demand or claim scientific validation or uncertainty quantification when
the task makes no corresponding scientific claim. Keep parent-model, numerical,
and model-reduction errors distinct.

### Protected execution and release work

This class covers the protected actions identified under **Numerical
calculations and protected execution**. It requires explicit human authorization
and the applicable durable checkpoint. Passing tests, review, or agent agreement
does not supply that authority.

## Human decisions and checkpoints

The human PI remains final authority for scientific meaning; mathematical and
physical conventions; public APIs and serialization contracts; backward
compatibility; architecture and project scope; dependencies and licensing;
acceptance of unresolved validation failures; external or resource-intensive
execution; destructive actions; releases and publication; and final acceptance.

Create a human checkpoint only when at least two materially different defensible
options remain and the choice affects a protected boundary. Do not create one
for deterministic corrections fixed by an accepted contract, routine
implementation details, formatting, mechanical synchronization, expected test
failures during development, or administrative closeout after explicit human
acceptance. When only one contract-consistent correction exists, apply it, test
it, record it concisely, and continue.

Checkpoint resolution, durable decision-boundary commits, and resumption are
owned by `.agents/skills/resolve-human-checkpoint/SKILL.md` and
`docs/development/agent-control-plane.rst`; do not duplicate their mechanics in
task instructions. A checkpoint cannot expand the scope authorized by its
higher-level task or human decision.

## Ownership and review

Explicit, non-overlapping writer ownership is required when multiple agents
write concurrently, protected source and independent verification must be
separated, an accepted task explicitly requires a manifest, or conflicting or
high-risk path ownership exists. Otherwise, one agent may implement code, tests,
and documentation for ordinary bounded work.

When a manifest is required, follow `.pi/task-ownership/README.md` and run its
validator before covered work begins. A passing task-ownership validator
establishes authorization and path separation only; it does not establish
implementation correctness, numerical verification, scientific validity, or
human acceptance.

The default managed-task flow is:

```text
implementation
→ relevant validation
→ one consolidated independent review
→ at most one consolidated correction pass
→ final verification
→ human acceptance when required
```

If material disagreement remains after the correction pass, stop and report the
unresolved decision. Do not create an unbounded writer, reviewer, or checkpoint
loop.

## Testing and retained evidence

Inspect `pyproject.toml`, existing workflows, and the relevant test tree before
choosing commands. Use established tools, run the cheapest relevant checks
first, and do not change expected values merely to obtain a pass. Diagnose
whether the implementation, fixture, method, or reference is wrong.

Ordinary unit and integration tests need clear names and assertions. They do not
automatically require stable evidence identifiers; complete
Requirement/Method/Oracle/Acceptance/Interpretation/Limitations sections; one
class per file; or class-owned and artifact-owned classification.

Those conventions apply when an accepted task explicitly declares tests to be
maintained verification evidence. Their detailed grammar is owned by
`.pi/skills/document-python-research-software/references/test-evidence-documentation.md`;
subsystem-specific placement and evidence rules belong in the applicable skill,
task, specification, or `docs/verification/` page.

Constructor, schema, invariant, and deterministic tolerance checks do not by
themselves establish scientific validation or uncertainty quantification. Use
explicit tolerances and state what they measure. Report absent evidence only
when it is relevant to the task or claims.

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
Verify references against primary sources before adding them. Research plans,
expected results, and proposed calculations must remain visibly distinct from
completed findings.

Public APIs, scientific meanings, mathematical algorithms, units, assumptions,
serialized formats, and non-obvious invariants require complete documentation.
Private mechanical helpers and obvious local variables require concise
documentation only when it improves understanding; do not add repetitive
docstrings or comments that merely restate assignments or types.

Use `TypeError` for wrong semantic types and `ValueError` for violated
invariants. Source, tests, schemas, fixtures, examples, and Sphinx pages must
agree where they describe the same contract. Follow
`docs/development/source-documentation.rst` for detailed, risk-proportional
source-documentation procedure.

## Repository procedures and subsystem rules

Keep stable global rules in this file. Detailed mechanics remain with their
owners:

- checkpoint resolution: `.agents/skills/resolve-human-checkpoint/SKILL.md`;
- test-evidence grammar:
  `.pi/skills/document-python-research-software/references/test-evidence-documentation.md`;
- DataObject/ActionObject design:
  `.pi/skills/design-data-action-objects/SKILL.md`;
- task-ownership schemas and validation: `.pi/task-ownership/README.md`;
- subsystem rules: applicable scoped task, skill, specification, architecture,
  and verification files;
- mutable state: chain, task, checkpoint, and durable human-decision records.

Skills are capabilities, not scientific guards or transitions. Deterministic
commands establish only their declared software gates; reviewers report
findings; humans own protected decisions and acceptance.

Graphify is optional and read-only. Use `.agents/skills/graphify/SKILL.md` only
for an explicit Graphify request or a broad topology, dependency, or impact
question. Verify material conclusions against authoritative files. Graphify
cannot approve architecture, establish scientific validity, launch work, or
record human decisions. Remote processing, API-key configuration, hooks, global
skill changes, or committing generated outputs requires explicit human
approval.

Operator-record work follows `.pi/skills/develop-operator-records/SKILL.md` and
its referenced maintained architecture and verification records. Do not treat
exact represented comparison as basis, gauge, energy-zero, unit, geometry, or
physical alignment.

## AI-assisted work

Treat all agent-generated code, prose, equations, and analysis as provisional.

Do not describe AI-assisted work as reviewed, validated, or release-ready unless
the human explicitly authorizes that statement.

When uncertainty remains, state the uncertainty, identify the assumption and
what must be checked, and avoid inventing a convenient answer.

## Working procedure

For each task:

1. Read the relevant files and any more specific `AGENTS.md`.
2. Reconstruct repository state from the authoritative records and inspect the
   current branch and working tree.
3. Classify the work and apply proportional controls plus any accepted
   task-specific requirements.
4. Preserve unrelated user changes.
5. Make the smallest change that satisfies the request without expanding
   scientific scope.
6. Run the cheapest relevant checks followed by affected completion gates.
7. Report changed files, checks, assumptions, unresolved limitations, and any
   scientific or expensive validation not performed when relevant.

Do not merge, tag, publish, submit external jobs, or perform another protected
or release action without explicit human authorization. Commit and push only
when requested or when required by an applicable durable decision-boundary
procedure. Include only validated, in-scope state; never mix unrelated or
unaccepted work into a boundary commit. Do not amend or rewrite a pushed
decision-boundary commit. Do not reset shared history or force-push without
explicit human approval.

## Definition of done

A task is complete when:

- the requested change is implemented;
- relevant checks pass;
- affected documentation is consistent;
- unrelated user work remains unchanged;
- assumptions and limitations are reported; and
- no unsupported scientific claim has been introduced.
