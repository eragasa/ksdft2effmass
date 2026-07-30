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

The repository is organized as a language-neutral scientific project with
separate Python and Rust implementations.

Use the following language roots:

    python/
    rust/

Do not place language implementations under `src/python/` or `src/rust/`.
Each language should retain its conventional project structure:

    python/src/ksdft2effmass/
    rust/crates/

Python is the initial and reference implementation. It is used for scientific
workflows, analysis, validation, visualization, and rapid development.

Rust may be used first for measured performance bottlenecks and may later
develop into a complete implementation of the computational model.

Language-independent scientific definitions belong under:

    specification/

Shared numerical fixtures and expected results belong under:

    fixtures/

The specification must define:

- operators and state spaces;
- units and physical conventions;
- array shapes and index ordering;
- scalar and complex data types;
- energy and gauge conventions;
- serialization schemas;
- validation metrics;
- numerical tolerances.

The Python and Rust implementations must conform to the same scientific
specification. Neither implementation may silently introduce different
physical definitions or conventions.

Before introducing a Rust implementation of an existing Python component:

1. retain a correct Python reference implementation;
2. define shared fixtures and expected results;
3. identify the required numerical tolerances;
4. add cross-language conformance tests;
5. document any intentional algorithmic differences.

For performance acceleration, profile a representative Python workload before
moving a kernel to Rust. Do not rewrite operations already performed
efficiently by BLAS, LAPACK, NumPy, or SciPy without a measured reason.

A Rust component must provide:

- tests against shared fixtures;
- comparison with the Python reference;
- documented inputs and outputs;
- explicit ownership and memory-layout assumptions;
- benchmarks when performance is part of its justification.

Prefer safe Rust. Any `unsafe` code must be localized, documented, tested, and
justified.

PyO3 and Maturin may be used when exposing Rust kernels through Python. They
are not required for a standalone Rust implementation.

Python and Rust may expose language-appropriate public APIs. Their syntax may
differ, but their scientific meaning, serialized data, and validation behavior
must remain compatible.

### DataObject/ActionObject programming model

Apply this policy to new code and code undergoing substantial refactoring. Do
not launch repository-wide mechanical rewrites of unrelated stable modules.

DataObjects represent scientific state, metadata, configuration, or results.
They should normally be `@dataclass(frozen=True, slots=True)`. They may own
explicit fields, intrinsic constructor validation, canonicalization of their own
data, exact value equality, and trivial derived properties. They must not own
serialization workflows, numerical analysis policies, basis alignment, unit
conversion, file I/O, orchestration, or operations that produce conceptually new
objects.

ActionObjects perform explicit transformations, analyses, validation procedures,
or external representations. They own numerical or algorithmic policy, accept
DataObjects as inputs, return a DataObject or explicit ResultObject, avoid
hidden mutation and global state, and expose a clear domain verb such as
`execute()`, `encode()`, or `decode()`.

A Workflow is a concrete ActionObject that encapsulates a reusable,
scientifically or computationally meaningful sequence of actions. Workflow
inputs and outputs must be explicit DataObjects or ResultObjects; dependencies
must be explicit; Workflows must not rely on hidden global state. Do not
introduce a generic Workflow base class unless multiple existing workflows
require a real shared interface. Do not treat every integration test as a
Workflow, and do not create production Workflow objects solely to provide an
owner for tests.

The standard computational form is:

```text
DataObject --ActionObject--> DataObject or ResultObject
```

Do not create abstract `DataObject` or `ActionObject` base classes. Prefer
concrete types and composition. Introduce protocols only after multiple real
implementations share a required interface.

Ownership rule:

- data invariant -> method or constructor validation on the owning DataObject;
- numerical operation -> method on the corresponding ActionObject;
- serialization rule -> method on the serializer ActionObject;
- operation output -> explicit ResultObject;
- genuinely domain-independent mathematics -> a free function only when it has
  no natural object owner.

Do not create generic dumping grounds such as `utils.py`, `helpers.py`,
`common.py`, or `misc.py`. "No dangling helper functions" means every
nontrivial operation needs an explicit and documented domain owner; it does not
mean that every mathematical function must be wrapped artificially in a class.

New architecture must remain translatable to Rust using structs for DataObjects
and ResultObjects, structs with `impl` blocks for ActionObjects, constructors
returning `Result` for validated construction, composition rather than
inheritance, explicit ownership and immutable borrowing, deterministic versioned
serialization, fixed serialized field names, explicit error cases, no dynamic
attributes or monkey patching, and no implicit workflow state. Python and Rust
need not share source code, but they must share an intelligible data model,
operation boundaries, and wire-format specification.

### Pi control plane for operator-record work

Repository-local pi skills live under `.pi/skills/`; project subagents and
chains live under `.pi/agents/` and `.pi/chains/`. The root `AGENTS.md` remains
the authoritative global architectural policy. Focused skills and task files may
add narrower instructions but must not contradict this file.

Use the repository-local `choose-next-task` skill as a read-only planning
transition after human final acceptance of a task, when the user explicitly asks
what is next, or when a chain completes and the parent needs to propose the next
task. The skill reconstructs state from repository evidence, recommends exactly
one next task, and then stops for human selection. Do not make it a mandatory
completion gate, and do not use it to create or launch work automatically.

Every completed task record should leave enough durable repository evidence for
`choose-next-task` to operate in a new session. A completion handoff should
identify the objective, final status, human acceptance, artifacts produced,
public API or scientific result, validation evidence, known limitations,
unresolved decisions, dependencies now satisfied, and explicitly deferred work.
The handoff describes state only; it must not recommend or launch the next task.

### Graphify repository-intelligence policy

Graphify is an optional, read-only repository-analysis aid for broad topology,
dependency, impact, navigation, and candidate-task questions. It is not
mandatory for ordinary tasks and must not be an automatic side effect of every
agent run. Generated graphs may be incomplete or stale; every material conclusion
from Graphify must be verified against authoritative repository files. Graphify
cannot approve architecture, establish scientific validity, launch implementation
work, record human decisions, or supersede accepted task records, source, tests,
specifications, fixtures, or human-reviewed documentation.

In the validated project environment, both Codex and pi discover
repository-local skills under `.agents/skills/`. pi additionally discovers
pi-specific skills under `.pi/skills/`. A project skill may shadow a same-named
global pi skill. The shared repository-local Graphify skill lives under
`.agents/skills/graphify/` and intentionally takes precedence over the global pi
fallback because it is versioned with the repository and subject to repository
policy. Do not retain a duplicate project-local pi Graphify routing workflow
under `.pi/skills/`.

Remote semantic processing, API-key configuration, Codex hooks, git hooks,
global skill modification, or generated graph artifacts committed to version
control each require a new explicit human approval. Generated Graphify outputs
under `graphify-out/` are locally persistent, generated, and ignored. A curated
`GRAPH_REPORT.md` may be committed only after separate human review, and no
generated report becomes an architectural decision record automatically. Human
intervention remains mandatory when instructions, evidence, authority, external
processing, hook behavior, or generated-file ownership conflict.

For the operator-record refactor, repository evidence establishes the Python
project root as `python/`, the Python source root as `python/src/`, the operator
package as `python/src/ksdft2effmass/operators/`, and the test root as
`python/tests/`. Object tests must mirror the public package hierarchy under
`python/tests/ksdft2effmass/<package>/test__<ObjectName>.py`; operator-record
object tests therefore live under
`python/tests/ksdft2effmass/operators/test__<ObjectName>.py`. Tests for genuine
production Workflow objects live under
`python/tests/ksdft2effmass/workflows/test__<WorkflowName>.py`. Technical
integration tests that are not domain workflows live under
`python/tests/ksdft2effmass/integration/test__<IntegrationName>.py`. If future
package-discovery, layout, import, test, or Sphinx evidence conflicts with this,
pause for human decision instead of choosing a source root silently.

The intended operator-package structure is:

```text
python/src/ksdft2effmass/operators/
├── __init__.py
├── records.py
├── hermiticity.py
└── serialization.py
```

Architectural decisions for that work:

- `StateSpace`, `Basis`, `Geometry`, `EnergyReference`, and `OperatorRecord` are
  DataObjects; `HermiticityResult` is a ResultObject; `HermiticityAnalyzer` and
  `OperatorRecordJsonSerializer` are ActionObjects.
- `OperatorRecord` contains represented data only.
- Hermiticity tolerance belongs to `HermiticityAnalyzer`.
- Hermiticity results are returned as `HermiticityResult`.
- Serialization belongs to `OperatorRecordJsonSerializer`.
- Schema-version and complex-matrix mechanics belong to the serializer.
- Geometry validation belongs to `Geometry`.
- State-space validation belongs to `StateSpace`.
- Exact equality belongs to the DataObject.
- Approximate or physically aligned comparison is a separate future ActionObject.
- The public API is exported from `ksdft2effmass.operators`.
- Sphinx documentation and tests are required parts of completion.
- Do not create an `OperatorRecordWorkflow` for `construct -> Hermiticity
  analysis -> serialize -> deserialize`; those operations remain owned by
  `OperatorRecord`, `HermiticityAnalyzer`, and `OperatorRecordJsonSerializer`.

Hermiticity is measured by

$$
\varepsilon_{\mathrm H}
=
\max_{i,j}
\left|
H_{ij}-H_{ji}^{*}
\right|,
$$

with acceptance under analyzer tolerance $\tau$ when

$$
\varepsilon_{\mathrm H}\leq\tau.
$$

Future delegated operator-record work must follow this order: control-plane
contract, public schema and validation fixtures, production implementation,
tests, documentation, read-only integration review, parent verification, and
human final acceptance. Public scientific semantics, independent validation
surfaces, strict JSON serializer/deserializer contracts, public versioned
schemas, valid and invalid golden fixtures, no cross-object private-method
calls, private methods only for owned mechanical implementation, deterministic
serialization, explicit human intervention for compatibility discoveries,
source documentation as part of implementation, Sphinx documentation as part of
completion, and integration review after combined-tree validation are required.
Implementation, tests, and documentation must not all begin simultaneously in a
shared worktree. Tests and documentation may be designed from the approved
public contract, but they must not run validation against partially written
production modules. Use non-overlapping file ownership when agents run
concurrently; serialize overlapping edits explicitly; require subagents to
report files changed, commands run, and unresolved issues; reserve final
integration and verification for pi; preserve existing user changes; and avoid
unrelated cleanup.

The human PI is final authority for scientific meaning, mathematical
conventions, public API decisions, serialization compatibility, architectural
boundaries, backward compatibility, project scope, acceptance of unresolved
validation failures, and final acceptance. A timeout, unavailable human, or
absent response leaves human checkpoints blocked; do not assume approval.

Completion gates for this refactor are unit tests, formatter, linter, static
type checker, Sphinx build with warnings treated as errors, public-import smoke
test, JSON round-trip test, architecture review, and a clean check for obsolete
imports and dangling helpers.

## Repository structure

Python and Rust are separate implementations under the repository-level
directories:

    python/
    rust/

Language-independent scientific definitions belong under `specification/`.
Shared numerical fixtures belong under `fixtures/`.

The canonical repository structure and directory responsibilities are defined
in [`docs/architecture/repository-layout.md`](docs/architecture/repository-layout.md).
Do not introduce a competing source-tree layout.

## Testing and validation

Inspect `pyproject.toml`, existing workflows, and the test directory before
choosing development commands. Use the repository's established tools rather
than introducing replacements without justification.

Run the cheapest relevant checks first.

Tests should cover applicable invariants such as:

- dimensions and shapes;
- Hermiticity;
- projector identities;
- unitary or isometric transformations;
- basis-change consistency;
- failure on incompatible state spaces;
- deterministic serialization and provenance.

Use explicit numerical tolerances and explain what they measure.

Do not update expected values merely to make a failing test pass. Determine
whether the implementation, fixture, numerical method, or reference value is
incorrect.

Unit tests and scientific validation are different:

- unit tests verify implementation behavior;
- scientific validation compares the model with an appropriate physical or
  computational reference.

Do not describe test coverage as scientific validation.

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

## Working procedure

For each task:

1. Read the relevant files and any more specific `AGENTS.md`.
2. Inspect the current branch and working-tree state.
3. Preserve unrelated user changes.
4. Identify the smallest change that satisfies the request.
5. Implement the change without expanding its scientific scope.
6. Run the relevant inexpensive checks.
7. Report:
   - files changed;
   - checks performed;
   - assumptions introduced;
   - unresolved limitations;
   - scientific or expensive validations not performed.

Do not commit, push, merge, tag, publish, or submit external jobs unless
explicitly requested.

## Definition of done

A task is complete when:

- the requested change is implemented;
- relevant checks pass;
- affected documentation is consistent;
- user work outside the task remains unchanged;
- assumptions and limitations are reported;
- no unsupported scientific claim has been introduced.
