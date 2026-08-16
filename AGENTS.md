# AGENTS.md

## Project

`ksdft2effmass` is open-source research software for constructing and
evaluating reduced semiconductor Hamiltonians from first-principles Kohn-Sham
DFT calculations.

The initial application is substitutional phosphorus and boron in silicon. The
project investigates when an atomistic impurity Hamiltonian can be replaced by
a reduced lattice or continuum effective-mass model.

Read `README.md` when general project context is needed, and inspect the files
relevant to the requested task before making changes. Keep authoritative
definitions and dependencies in their owning surfaces:

| Subject | Authoritative location |
|---|---|
| Physical and mathematical definitions | Applicable versioned files under `specification/` |
| Scientific assumptions | `docs/research/` |
| Computational workflow dependencies | `docs/computational/` |
| Python software dependencies | `python/pyproject.toml` |
| Resolved Python dependency versions | `python/uv.lock` |

Do not define or override these contracts in this file.

## Research scope

The authorized research and software scope includes the areas listed below.
Inclusion defines project scope only; it does not mean that a capability is
implemented, scientifically validated, or authorized for execution:

- bulk-silicon reference calculations;
- projected and Wannier Hamiltonians;
- tight-binding reductions;
- alignment of pristine and doped representations;
- impurity-operator extraction;
- lattice and continuum reductions; and
- validation metrics and provenance.

The underlying electronic-structure and Wannier calculations remain outside
this package:

- Quantum ESPRESSO is responsible for electronic-structure calculations; and
- Wannier90 is responsible for Wannier localization.

Do not reimplement DFT or Wannier localization in this package, or expand a task
into phonons, electron-phonon coupling, machine learning, device simulation, or
another material system, without explicit human authorization and an applicable
durable task.

## Authority and repository state

Apply instructions and durable records in the following order. A lower level may
add compatible detail but may not override a higher level.

| Precedence | Authority |
|---|---|
| 1 | Current unambiguous human instruction |
| 2 | Applicable durable human decisions and resolved checkpoints |
| 3 | Accepted scientific specifications and public contracts |
| 4 | This root file and applicable scoped `AGENTS.md` files |
| 5 | Active chain, task, ownership, and authorized workspace records |
| 6 | Applicable skills and procedural documentation |
| 7 | Derived reports, retained evidence, and historical records |

An unresolved checkpoint is a pending human decision boundary, not a resolved
decision. Historical evidence records what happened but does not govern current
work. Architecture and planning records define boundaries but do not themselves
authorize task activation or execution.

Do not store mutable task status in this file. A controlling chain is current
selection and control state, not an append-only event log: keep one current
phase summary, do not append resolved phase narratives, and place resolved
architecture, decisions, and evidence in their owning normative, checkpoint, or
evidence records without duplicating them in the chain.

At session start, reconstruct only the state relevant to the requested task:

1. inspect unresolved checkpoint records under `.pi/checkpoints/`;
2. inspect the current branch, checkout, and working-tree state;
3. identify the applicable controlling chain from the human request and durable
   chain state rather than assuming one from filename or recency;
4. inspect the tasks and ownership records referenced by that chain or an
   unresolved checkpoint;
5. inspect applicable resolved checkpoints and other durable human decisions;
6. inspect any authorized worktree, mission, run, or handoff artifacts referenced
   by the controlling records; and
7. if required authority or state is missing or conflicting, report the exact
   blocker and stop.

If the current human message unambiguously resolves a persisted checkpoint,
follow `.agents/skills/resolve-human-checkpoint/SKILL.md`. Never infer approval
from silence, timeout, an agent report, reviewer agreement, or a passing check.

Use `.pi/skills/recommend-next-task/SKILL.md` only when no task or checkpoint
remains active and the human asks what comes next. It is read-only and cannot
activate or launch work.

## Branches and releases

| Branch | Meaning |
|---|---|
| `dev` | Active development; changes and results are provisional |
| `main` | Latest reviewed snapshot associated with a conference, paper, or other formal research output |

Do not perform any of the following without explicit human authorization and the
applicable durable checkpoint:

- merge `dev` into `main`;
- push directly to `main`;
- create, move, or delete version tags;
- create a GitHub Release;
- publish a package;
- archive software or data; or
- update a DOI.

Do not describe development branches, intermediate commits, pull requests,
automated builds, or continuous-integration artifacts as reviewed or released.

Only signed semantic-version tags of the form `vMAJOR.MINOR.PATCH` identify
reviewed research-software releases.

## Scientific integrity

Never fabricate or present unsupported claims about:

- numerical results;
- completed calculations;
- convergence;
- validation;
- literature values;
- references, quotations, or DOIs; or
- software capabilities.

Label the status of scientific and numerical material explicitly:

| Status | Required interpretation |
|---|---|
| Calculated result | Produced by an identified calculation with retained provenance |
| Literature value | Taken from an identified and verified source |
| Expected behavior | A prediction or expectation, not an observation |
| Illustrative example | Explanatory only, not research evidence |
| Synthetic test data | Constructed for testing, not calculated physical data |
| Placeholder | Incomplete material awaiting authoritative content |
| Proposed work | Planned but not completed |

Do not treat successful execution, passing software tests, or reviewer agreement
as evidence of scientific correctness or validation.

Track parent-model error, numerical or discretization error, and model-reduction
error separately. Do not combine them unless their mathematical relationship and
compatible error definitions have been established in the owning specification.

## Mathematical conventions

Preserve the notation and definitions in the applicable versioned files under
`specification/`.

In particular:

- distinguish a physical model, mathematical operator, and finite matrix
  representation;
- identify relevant state spaces and state the domain and codomain when they
  matter;
- do not subtract operators acting on unidentified or unaligned state spaces;
- align pristine and doped bases before direct matrix subtraction;
- make basis, gauge, energy-reference, unit, and geometry conventions explicit;
- distinguish projection, disentanglement, basis transformation, and
  truncation;
- do not describe Wannierization alone as a low-rank approximation; and
- do not identify Kohn-Sham eigenvalues with the complete many-body excitation
  spectrum.

If an owning specification is unclear or inconsistent, report the exact
ambiguity rather than selecting a convention by preference or implementation
convenience. Stop when that ambiguity materially blocks the requested work.

## Numerical calculations and protected execution

The following actions are protected and require explicit human authorization and
the applicable durable checkpoint:

| Protected action | Examples |
|---|---|
| Production electronic-structure execution | Quantum ESPRESSO or Wannier90 production calculations |
| External computation | Remote, cluster, cloud, or HPC jobs |
| Destructive operation | Deleting calculation data or rewriting repository history |
| External data transmission | Sending calculation, private, restricted, or unpublished project data outside approved repository remotes or services |
| Dependency or licensing decision | Adding, replacing, or relicensing a dependency |
| Release or publication action | Actions governed by **Branches and releases** |

Before starting an authorized potentially expensive calculation, report:

- the executable;
- the input system;
- the expected computational scale;
- the anticipated outputs; and
- the approximate runtime and resource requirements, when known.

Do not start if the active authorization does not cover the reported execution
or resource use.

Do not change the following scientific settings unless the owning specification
or an explicitly authorized durable task permits the change:

- pseudopotentials;
- exchange-correlation approximations;
- energy cutoffs or meshes;
- convergence tolerances;
- crystal structures;
- Wannier windows or projections; or
- energy-alignment conventions.

When a change is authorized, record the previous and new settings, the authority
for the change, and the affected provenance or specification.

## Data and provenance

Do not commit large electronic-structure outputs to Git. Keep wavefunction,
density, restart, scratch, and dense-matrix files outside the repository.

Retain compact, version-controlled reproduction and provenance records:

- sanitized calculation input files;
- manifests identifying external data and artifacts;
- checksums with their algorithms;
- software names and versions;
- physical and numerical settings;
- reproduction scripts; and
- compact calculation-status or validation summaries with their evidentiary
  status stated explicitly.

Do not delete, move, or overwrite calculation data unless the exact target and
impact are known and the action has explicit human authorization and the
applicable durable checkpoint.

Never include credentials, access tokens, private keys, scheduler secrets,
private data, or restricted data in source code, inputs, logs, documentation,
manifests, or commits.

## Software architecture

Follow `docs/architecture/v1/index.md` and use the current or approved
prospective ownership surfaces:

| Surface | Location and role |
|---|---|
| Current Python reference implementation | `python/src/ksdft2effmass/` |
| Rust crates, when authorized and introduced | `rust/crates/` |
| Current language-independent definitions | `specification/` |
| Shared numerical fixtures, when authorized and introduced | `fixtures/` |

Do not create a competing source-tree layout.

Python is the initial reference implementation. Require Python and Rust agreement
only for language-independent specifications, shared wire formats, approved Rust
components, or an active cross-language contract.

An authorized Rust port must retain the Python reference, define shared expected
results and tolerances, add conformance tests, and document intentional
algorithmic differences. Do not create speculative Rust designs for Python-only
internals.

Profile a representative workload before moving performance-sensitive code, and
do not replace NumPy, SciPy, BLAS, or LAPACK operations without evidence.
Performance-motivated Rust must document ownership and memory layout, include
representative benchmarks, prefer safe Rust, and localize, justify, document, and
test any `unsafe` code.

Apply the DataObject/ActionObject model before adding scientific object models,
changing public object boundaries or nontrivial data-model behavior, or
performing substantial object-model refactors. Do not apply it to unrelated
stable modules. Follow `.pi/skills/design-data-action-objects/SKILL.md` and its
referenced architecture.

Keep nontrivial behavior with its domain owner. Do not create generic utility
modules or hide scientific policy in module-level validators. Maintained data
and results must be operationally immutable.

Public numeric APIs must:

- reject booleans and numeric strings unless the accepted contract explicitly
  permits them;
- document accepted scalar types, units, and overflow behavior; and
- keep runtime behavior, typing, documentation, tests, and applicable schemas or
  cross-language contracts consistent.

## Process classes

Classify work by the highest-risk applicable class. Controls are cumulative when
more than one class applies. An active, authorized task may impose compatible
additional controls but may not waive higher-authority requirements.

### Routine software work

Examples include internal helpers, local refactors, documentation corrections,
ordinary unit tests, non-public validators, and deterministic bug fixes under an
accepted contract.

Normally require bounded scope, the requested change, relevant tests, affected
documentation, and one review when materially useful.

Routine classification alone does not require ownership manifests or writer
splits, maintained-evidence conventions, retained checksum catalogs, human
checkpoints, Rust mappings, scientific validation, uncertainty quantification,
or multiple review rounds.

### Public-contract and persistence work

Examples include public APIs, schemas, serialized records, durable marking
formats, file or SQLite repository boundaries, and compatibility or migration
behavior.

Require an explicit contract, schema or fixture agreement where applicable,
software-verification tests, and compatibility review. Require a human decision
only when materially different defensible choices remain at a human-owned or
protected boundary.

### Scientific or numerical work

Examples include mathematical algorithms, numerical approximations, convergence
procedures, physical-model comparisons, and scientific acceptance metrics.

Require only the evidence classes applicable to the claims made:

| Evidence class | What it establishes |
|---|---|
| Software verification | Agreement with the documented software contract |
| Numerical verification | Agreement with, or controlled approximation of, the stated mathematics |
| Scientific validation | Comparison with independent reference evidence for a declared use |
| Uncertainty quantification | Identification and propagation of relevant uncertainty sources |

Do not demand or claim scientific validation or uncertainty quantification when
the task makes no corresponding claim. Keep parent-model, numerical, and
model-reduction errors distinct.

### Protected execution and release work

This class covers the protected actions identified under **Numerical
calculations and protected execution**. It requires explicit human authorization
and the applicable durable checkpoint. Passing tests, review, or agent agreement
does not provide that authority.

## Human decisions and checkpoints

The human PI retains final authority over:

| Boundary | Examples |
|---|---|
| Scientific meaning | Mathematical and physical conventions, model interpretation, acceptance metrics |
| Public contracts | Public APIs, serialization, schemas, and backward compatibility |
| Architecture and scope | System boundaries, project scope, and materially different architectural choices |
| Dependencies and licensing | Dependency selection, replacement, and license acceptance |
| Evidence disposition | Acceptance of unresolved verification or validation failures |
| Protected action | External or resource-intensive execution, destructive operations, release, and publication |
| Completion | Final human acceptance when required |

Create a human checkpoint only when:

1. at least two materially different defensible options remain;
2. the choice affects a human-owned or protected boundary; and
3. existing authority does not already determine the answer.

Do not manufacture alternatives to force a checkpoint. Do not create one for
deterministic corrections fixed by an accepted contract, routine implementation
details, formatting, mechanical synchronization, expected development failures,
or administrative closeout after explicit human acceptance.

When only one contract-consistent correction exists, apply it, test it, record
it concisely, and continue within the active authorization.

Checkpoint resolution, durable decision-boundary commits, and resumption are
owned by `.agents/skills/resolve-human-checkpoint/SKILL.md` and
`docs/development/agent-control-plane.rst`. Do not duplicate their mechanics in
task instructions. A checkpoint cannot activate work or expand scope beyond its
controlling task and human authority.

## Ownership and review

Require explicit, non-overlapping ownership when:

- multiple agents write concurrently;
- implementation and independent verification ownership must be separated;
- an authorized task requires an ownership manifest; or
- conflicting or high-risk path ownership exists.

Otherwise, one agent may implement source, tests, and documentation for ordinary
bounded work.

Use separate authorized workspaces for concurrent writers and assign one writer
per covered path. Keep reviewers read-only with respect to the reviewed scope.
A reviewer reports findings but does not mutate the subject, resolve human-owned
decisions, or provide human acceptance.

When a manifest is required, follow `.pi/task-ownership/README.md` and run its
validator before covered work begins. A passing validator establishes that the
declared assignment and path separation are structurally valid within the
controlling task. It does not activate the task, expand authority, or establish
implementation correctness, numerical verification, scientific validation, or
human acceptance.

A delegated writer working outside the parent checkout must provide a durable
handoff identifying:

- the task and run;
- the workspace;
- the base and resulting revision or uncommitted state;
- changed paths;
- validation performed; and
- unresolved findings or risks.

The parent must verify the handoff against authoritative repository state before
integration or continuation.

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
unresolved decision. Do not create an unbounded writer, reviewer, correction, or
checkpoint loop.

## Testing and retained evidence

Testing responsibility follows the active task. When a manifest is required,
assignments must agree with its validated ownership:

| Work | Responsible agent or skill |
|---|---|
| Ordinary tests not requiring separate ownership | Current authorized writer |
| Maintained Python test evidence | Writer assigned by the active task or ownership manifest; use `.pi/agents/ksdft2effmass-tests.md` when selected |
| Maintained-evidence procedure | `.pi/skills/develop-python-test-evidence/SKILL.md` |
| Domain-specific operator evidence | `.pi/skills/develop-operator-records/SKILL.md` when applicable |
| DataObject/ActionObject domain constraints | `.pi/skills/design-data-action-objects/SKILL.md` when applicable |
| Independent semantic and compatibility review | Read-only reviewer assigned by the task or ownership manifest |
| Scientific validation or uncertainty quantification | Separate human authorization and declared evidence classification under the test-evidence skill |

Before selecting test commands, inspect `python/pyproject.toml`, configured test
tooling, the relevant test tree, and task-specific completion gates. Run
the cheapest affected checks first, followed by broader required checks.

Do not change expected values, weaken tolerances, add skips, or remove tests
merely to obtain a pass. Diagnose whether the implementation, fixture, method,
contract, or reference is wrong.

Ordinary unit and integration tests require clear names, relevant assertions,
and explicit tolerances where applicable. They do not automatically require
maintained evidence identifiers, full evidence prose, class-per-file structure,
or class-owned or artifact-owned classification.

For maintained Python test evidence, the assigned writer must load
`.pi/skills/develop-python-test-evidence/SKILL.md` and its complete reference.
That skill owns invocation profiles, evidence structure, migration, validation,
review boundaries, and reporting.

A passing test establishes only its stated requirement and acceptance rule under
the recorded conditions. Structural results establish only their declared
checks; semantic, scientific, and human conclusions remain separate.

## Documentation

Documentation responsibility follows the active task. When a manifest is
required, assignments must agree with its validated ownership:

| Work | Responsible agent or skill |
|---|---|
| Routine documentation accompanying implementation | Current authorized writer |
| Maintained narrative and Sphinx documentation | Writer assigned by the active task or ownership manifest; use `.pi/agents/ksdft2effmass-documentation.md` when selected |
| Public Python API, concept, serialization, and Sphinx procedure | `.pi/skills/document-python-research-software/SKILL.md` |
| Python source docstrings | Implementation owner unless explicitly transferred |
| Maintained test-evidence documentation | Task-assigned test writer using `.pi/skills/develop-python-test-evidence/SKILL.md` |
| Operator-record documentation | `.pi/skills/develop-operator-records/SKILL.md` when applicable |
| Independent documentation review | Read-only reviewer assigned by the task or ownership manifest |

Documentation authority does not authorize source behavior, tests, fixtures,
dependencies, scientific meaning, public-contract changes, or human acceptance.

For public Python APIs, serialization contracts, concepts, or Sphinx integration,
load `.pi/skills/document-python-research-software/SKILL.md` and follow
`docs/development/source-documentation.rst`. Use the required profile, explicit
authorized paths, and immutable input identities.

Use reStructuredText (`.rst`) for Sphinx documentation and Markdown (`.md`) for
all other maintained prose. In Markdown, use `$...$` for inline mathematics and
`$$...$$` for display mathematics; in reStructuredText, use the established
Sphinx syntax. Do not duplicate maintained content across formats or convert it
without explicit authorization.

Define symbols when introduced and distinguish the physical model, mathematical
operator, numerical representation, and software implementation. Use direct
technical prose, verify references against primary sources, and keep plans and
expected results distinct from completed findings.

Document public APIs and scientific contracts completely as required by the
owning skill and standard. Use supported public imports and keep source, tests,
schemas, fixtures, examples, API pages, and concept pages consistent.

Document private mechanical helpers and obvious local state only when useful;
do not restate assignments or types. Use `TypeError` for wrong semantic types
and `ValueError` for invariant violations by values of the correct type.

Run applicable Sphinx builds with warnings as errors, and do not retain generated
output.

## Repository procedures and subsystem rules

Keep stable repository-wide policy in this file. Detailed procedures remain with
their owning records:

| Concern | Owning procedure |
|---|---|
| Checkpoint resolution | `.agents/skills/resolve-human-checkpoint/SKILL.md` |
| Task ownership and validation | `.pi/task-ownership/README.md` |
| DataObject/ActionObject design | `.pi/skills/design-data-action-objects/SKILL.md` |
| Operator records | `.pi/skills/develop-operator-records/SKILL.md` |
| Next-task recommendation | `.pi/skills/recommend-next-task/SKILL.md` |
| Bounded inspection of one exact selected task | `.pi/skills/inspect-task-state/SKILL.md` |
| Explicitly requested Graphify use | `.agents/skills/graphify/SKILL.md` |

Task- and subsystem-specific rules belong in the applicable task, skill,
specification, architecture, verification, or scoped instruction file. Mutable
workflow state belongs in chain, task, checkpoint, ownership, mission, run, and
handoff records rather than this file.

An agent definition supplies the task role; a skill supplies the procedure.
Neither activates work, expands authorized paths or claims, permits protected
action, or provides human acceptance. A deterministic command establishes only
its declared software gate. Reviewers report findings; humans own protected
decisions and acceptance.

### Graphify

Use Graphify only when the human explicitly requests it; never trigger it for an
ordinary topology, dependency, impact, navigation, or next-task question. Follow
`.agents/skills/graphify/SKILL.md`, use only the validated local executable, and
never auto-install, upgrade, discover a fallback, rebuild, or select a semantic
backend.

Verify Graphify conclusions against authoritative files. Graphify cannot approve
architecture, establish scientific validity, activate work, or record human
decisions. Remote processing, API-key configuration, hooks, global skill
changes, or committing generated output requires explicit human authorization
and any applicable protected-action checkpoint.

### Operator records

For operator-record work, follow
`.pi/skills/develop-operator-records/SKILL.md` and its referenced architecture
and verification records.

Exact represented comparison does not by itself establish basis, gauge,
energy-zero, unit, geometry, or physical alignment.

## AI-assisted work

Treat agent-generated code, prose, equations, analysis, tests, and documentation
as provisional. Apply the same verification, review, evidence, and
human-acceptance requirements as for any other work.

When uncertainty remains, state the uncertainty, assumptions, missing evidence,
and required checks. Do not invent a convenient answer or convert expected
behavior into a completed finding.

## Working procedure

For each task:

1. reconstruct the applicable authority and durable state;
2. identify the requested outcome, process class, protected boundaries, and
   ownership requirements;
3. read the relevant files, applicable scoped `AGENTS.md`, and owning skills or
   procedures;
4. inspect the current branch, checkout, and uncommitted changes before editing;
5. perform the work directly unless authorized delegation is materially useful;
6. make the smallest in-scope change and preserve unrelated user work;
7. complete the applicable validation, review, correction, and final-verification
   gates; and
8. report changed paths, checks, assumptions, unresolved limitations, and any
   relevant scientific or expensive validation not performed.

If required authority, ownership, inputs, or durable state are missing or
conflicting, report the exact blocker and stop.

Do not perform protected execution or release actions without explicit human
authorization and the applicable durable checkpoint.

Commit and push only when requested by the current human instruction or required
by an applicable durable decision-boundary procedure. Include only validated,
in-scope state; do not stage or commit unrelated or unaccepted work.

Do not amend or rewrite a pushed decision-boundary commit. Do not reset shared
history or force-push without explicit human authorization and the applicable
durable checkpoint.

## Definition of done

Work is complete only when:

- the requested outcome is delivered within the authorized scope;
- required task, ownership, checkpoint, evidence, and handoff records are
  consistent with the resulting state;
- required checks pass or have an explicitly authorized disposition;
- required review and any permitted correction pass are complete;
- affected source, contracts, tests, schemas, fixtures, and documentation are
  consistent;
- unrelated user work remains unchanged;
- assumptions, residual risks, and limitations are reported; and
- no unsupported scientific claim or unauthorized protected action has been
  introduced.

When human acceptance is required, distinguish “work complete and pending human
acceptance” from “task closed and human-accepted.” Do not claim the latter until
the applicable durable decision is resolved.
