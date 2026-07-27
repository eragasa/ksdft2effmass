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
