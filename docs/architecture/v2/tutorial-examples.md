# Cross-backend tutorial examples

## Status and purpose

This page records the human-selected repository architecture for maintained
computational tutorial examples. Project tutorials are organized by computational
concept first and calculator backend second:

```text
examples/tutorials/<tutorial-id>/qe/
examples/tutorials/<tutorial-id>/abinit/
```

A project tutorial is not automatically identical to one upstream tutorial page. An
upstream QE or ABINIT tutorial may be decomposed across several project tutorials so
that each directory has one bounded learning objective. Conversely, one project
tutorial may cite more than one upstream source when the relationship is explicit and
reuse terms permit it.

The layout does not authorize installation, dependency changes, input acquisition,
pseudopotential selection, or executable invocation. Tutorial results remain
illustrative software-workflow observations unless a separate verification or
validation contract says otherwise.

## Directory contract

A materialized tutorial has this shape:

```text
examples/tutorials/<tutorial-id>/
  README.md
  qe/
    README.md
    input/
    scripts/
    expected/
    run/
  abinit/
    README.md
    input/
    scripts/
    expected/
    run/
```

`<tutorial-id>` is a stable lowercase kebab-case identity describing the system and
operation, such as `silicon-scf` or `aluminum-smearing-convergence`. It does not encode
execution order, backend, Task status, or scientific acceptance.

The tutorial-level `README.md` owns:

- the learning objective and physical system;
- the preprocessing, simulation, and postprocessing stages;
- the relationship between the QE and ABINIT realizations;
- comparisons that are permitted and comparisons that remain unsupported; and
- the implementation status of each backend.

Each backend `README.md` owns backend-specific executable roles, input conventions,
required external data, local run instructions, expected output roles, upstream
sources and reuse status, and limitations. A backend directory always contains a
README once the project tutorial is materialized. When implementation is unavailable,
that README states `planned`, `blocked`, or `not applicable`; it does not contain
fabricated input or expected output.

`input/` contains portable, sanitized, legally reusable inputs maintained by this
project. `scripts/` contains input construction or result-reading examples that do not
hide scientific settings. `expected/` is optional and contains only small curated
fixtures consumed by a deterministic software example or test. `run/` is local,
generated, and ignored by Git.

Directories with no maintained file are not created merely to reserve names. The
paired backend directories are created together when a tutorial is first materialized,
with an explicit status README for an unavailable backend.

## Commit boundary

The following material may be committed:

- tutorial and backend README files;
- portable sanitized input files authored by this project or reusable under verified
  source terms;
- deterministic input-generation and postprocessing scripts;
- tests that do not invoke scientific executables;
- small curated fixtures required by those tests, with their synthetic, tutorial, or
  calculated status stated explicitly; and
- compact expected observations only when their source, units, interpretation, and
  non-validation boundary are explicit.

The following material is not committed by default:

- `run/` trees, scratch directories, restart state, caches, or temporary files;
- routine raw stdout and stderr;
- QE `.save/`, `wfc*.dat`, charge-density files, or generated QEXSD;
- ABINIT wavefunction, density, NetCDF result, restart, or temporary files;
- pseudopotentials unless redistribution terms are verified and repository retention
  has a demonstrated need;
- executables, machine-local configuration, absolute local paths, scheduler state, or
  credentials;
- generated plots unless a reviewed documentation page directly consumes them; or
- copied upstream tutorial files whose reuse terms are unresolved.

A small native output may be promoted into `expected/` only when a maintained test or
example consumes its content. Promotion is an explicit fixture decision, not an
automatic consequence of a successful run. File listing or checksum collection alone
does not make runtime output a maintained example.

## Runtime layout

Each backend writes only beneath its ignored `run/` directory:

```text
run/
  input/
  stdout/
  stderr/
  work/
  results/
```

`input/` is the staged execution input, `stdout/` and `stderr/` retain separate process
streams, `work/` contains calculator-native mutable state, and `results/` contains
postprocessed local results. These are runtime roles rather than mandatory public
Python objects or persisted Workflow records.

A tutorial may demonstrate a three-phase colored-Petri-net composition:
preprocessing constructs a prepared run, simulation invokes the external executable
under separate authority, and postprocessing consumes the complete native result.
The example directory supplies concrete inputs and scripts; it does not own generic
CPN mechanics, execution authority, Task state, or Workflow persistence.

## Cross-backend comparison boundary

The paired directory expresses a shared learning objective, not numerical equivalence.
QE and ABINIT inputs may differ in pseudopotential representation, exchange-correlation
implementation, basis conventions, cutoffs, sampling, geometry, units, convergence
behavior, and output semantics.

A backend-neutral comparison requires a separate explicit alignment contract covering
at least structure, pseudopotential meaning, functional, basis and cutoff policy,
$k$-point sampling, units, energy reference, and the compared observable. Until then,
paired examples may compare workflow shape and software behavior only.

## Observed ABINIT single-stage flow

The authorized ABINIT basic1 stage-1 run materialized one concrete instance of the
three runtime roles without introducing generic Workflow or artifact objects:

- preprocessing staged one exact input and one pseudopotential by identity;
- simulation produced separate process streams plus one main `.abo` result, three
  NetCDF result views, and native density, wavefunction, derivative-database,
  eigenvalue, and band-plot files; and
- postprocessing joined the `.abo`, stdout log, GSR NetCDF, and EIG NetCDF content to
  report completion, input-tolerance convergence, energy, forces, eigenvalues, and
  diagnostics while leaving native continuation state external.

Two output details are architecturally relevant. First, ABINIT delivered a scientific
warning in its stdout log while the process stderr stream was empty; postprocessing
cannot treat stderr as the complete diagnostic channel. Second, GSR and EIG NetCDF
contained directly useful named numerical arrays, whereas density and wavefunction
files retained an operational continuation role without requiring immediate decoding.
The simulator therefore has a one-to-many native-output boundary, but this single-stage
observation does not yet require replacing the flat preprocessing → simulation →
postprocessing CPN candidate. Multi-stage branch and join behavior remains to be
observed before selecting the general topology.

## Task and campaign relationship

Canonical campaign Tasks remain under `harness/tasks/`. Computational campaign pages
map each backend Task to one or more project tutorial directories. Task activation,
blocking, execution authorization, outcome, or acceptance is never inferred from the
presence of an example directory.

QE campaign Tasks use `examples/tutorials/<tutorial-id>/qe/`; ABINIT campaign Tasks use
`examples/tutorials/<tutorial-id>/abinit/`. A campaign Task may populate several
project tutorials when an upstream tutorial combines several computational concepts.
The opposite backend directory remains an explicit planned, blocked, implemented, or
not-applicable peer.

## Initial implementation

`examples/tutorials/silicon-scf/` is the initial materialized project tutorial. Its
QE backend contains the migrated portable input-construction example, its ABINIT
backend records the planned and blocked status without fabricated input, and
repository ignore rules cover backend-local run trees and principal native outputs.
Additional tutorials are materialized only as their campaign work proceeds.
