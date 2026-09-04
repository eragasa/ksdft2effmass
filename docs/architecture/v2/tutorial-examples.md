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

Synthetic fixtures may verify isolated software or numerical mechanics, but they may
not stand in for calculated data when a tutorial-derived architecture probe claims
calculator, stage, continuation, native-output, diagnostic, or failure behavior. Such
a claim requires identified output from an actual explicitly authorized invocation,
with exact input, executable, pseudopotential, attempt, streams, native outputs, and
postprocessing provenance. Without that evidence, the behavior remains proposed or
unobserved.

## Runtime layout

Each execution writes beneath exactly one isolated run root. The root may be the
backend's ignored `run/` directory for a lightweight local example or an external run
root selected by an exact execution preflight when native state should remain outside
the repository. Maintained records use a portable run identity and never commit the
external root's absolute machine path.

A run root normally separates these roles:

```text
<run-root>/
  input/
  pseudo/
  streams/
  work/
  results/
  records/
```

Backend-specific directory names such as `input-source/` or separate `stdout/` and
`stderr/` directories are permitted when their roles remain explicit. Inputs and
external dependencies are staged and checked by identity; process streams remain
separate; `work/` contains calculator-native mutable state; `results/` contains
postprocessed local results; and `records/` contains compact execution and processing
records. These are runtime roles rather than mandatory public Python objects or
persisted Workflow
records. Generated content remains ignored or external in both layouts.

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
The simulator therefore has a one-to-many native-output boundary. This single-stage
observation did not by itself require replacing the flat preprocessing → simulation →
postprocessing CPN candidate. The paired silicon flow below supplies the first
cross-backend continuation observation.

## Observed paired silicon SCF-to-bands flow

The authorized paired silicon tutorial executed the same logical SCF-to-fixed-density-
bands dependency with two different native topologies:

| Logical role | Quantum ESPRESSO 7.5 | ABINIT 10.8.3 |
|---|---|---|
| SCF density | One `pw.x` process | Dataset 1 inside one `abinit` process |
| Density continuation | `si.save` cell, positions, and charge density read by a later process | `getden2=-1` reads dataset 1's density inside the same process |
| Fixed-density bands | A second `pw.x` process | Dataset 2 inside the original process |
| Backend postprocessing | A third `bands.x` process reads XML and wavefunctions | No second calculator process; project postprocessing reads `.abo` and NetCDF |
| Represented spectrum | Final QEXSD and `bands.x` files | Dataset-2 GSR/EIG NetCDF |
| Diagnostic delivery | Process stderr contained IEEE flag notices | Warnings appeared in the stdout log while process stderr was empty |

All three QE processes and the one ABINIT process exited 0. QE reported SCF
convergence, and ABINIT reported dataset-1 energy convergence. Those facts remain
separate from fixed-density band convergence: ABINIT warned that its two buffer bands
might not satisfy the same tolerance as the six non-buffer bands.

The represented outputs also require semantic interpretation rather than generic
presence checks. The final QE bands-mode QEXSD replaced the SCF QEXSD and exposed a
`0.0` total-energy field that is not the earlier SCF energy. ABINIT's dataset-2 GSR
repeated the dataset-1 SCF energy and represented unavailable forces with
`9.9999999999e99` sentinels. A field's presence and numeric type therefore do not
establish that the quantity was evaluated in that stage.

## Provisional CPN consequences

The concrete pair supports the following constraints on a later generic CPN design;
it does not itself accept a public contract:

- retain preprocessing → scientific execution → result extraction as a useful outer
  envelope;
- do not equate one operating-system process, one calculator dataset, one native file,
  or one scientific stage with one another;
- let Workflow control own an ordered, possibly nested dependency graph of scientific
  Task operations while backend adapters only stage, invoke, and parse each bound Task;
- represent QE SCF, NSCF, and DOS as separate reusable Task definitions and separate
  run-scoped CPN Task instances, each with its own activation, attempt, grant, process
  observation, result ingress, and failure boundary;
- pass continuation through admitted ResultObjects and exact immutable native-state
  identities rather than permitting a downstream Task to discover or mutate an
  upstream Task's workspace;
- allow one bound Task to report calculator-native internal structure, such as ABINIT's
  two datasets in one invocation, without transferring Workflow dependency-state
  ownership to the adapter or fabricating a CPN transition between atomic native steps;
- carry native continuation state as an explicit produced-and-consumed role, whether
  the dependency occurs within one Task or between Tasks, even when its binary arrays
  remain opaque to the generic layer;
- keep process completion, calculator-reported convergence, continuation satisfaction,
  postprocessor completion, represented-result availability, and diagnostics as
  separate facts;
- collect diagnostics from backend-defined channels rather than treating process
  stderr as complete; and
- let backend-specific postprocessing be optional and composable rather than forcing
  every backend through a `bands.x`-like process.

The flat three-phase candidate therefore remains suitable as an outer composition but
is insufficient as the only internal topology when stage-specific failure,
continuation, or restart behavior must be represented. The observed candidate is a
hierarchical composition: a Workflow-owned outer envelope and scientific-execution
subgraph compose backend-specific Task operations, while calculator adapters realize
those operations and expose represented scientific results alongside calculator-native
state and diagnostics.

The human subsequently selected the bounded internal vertical slice recorded in the
[DFT simulation CPN service decision](ksdft2effmass/workflows/dft-simulation-cpn-service-decision.md).
That slice privately fixes only the first SCF-to-fixed-density-bands transition names,
closed QE/ABINIT operation variants, effect-free retained-result replay, and
fail-closed comparison probe. The later DOS probe composed and executed independent
reusable SCF, NSCF, and DOS CPN Task instances rather than adding a monolithic
SCF-to-DOS Task. Its compact calculated QE 7.5 observation is materialized under
`examples/tutorials/silicon-dos/`; full native state and process artifacts remain in
the identified external run. Stable public token fields, general failure semantics,
general effectful dispatch, and persistence remain undecided.

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
QE backend contains the migrated portable input-construction example; its ABINIT
backend now links to the SCF dataset observed within the paired bands flow without
fabricating a portable input. `examples/tutorials/silicon-bands/` is the first
calculated paired-backend workflow observation. Runtime-retention rules keep both
backend-local and preflight-declared external run trees out of maintained examples.
`examples/tutorials/silicon-dos/` is the first calculated three-Task QE workflow
observation with identity-verified immutable state copies between independent CPN Task
instances. Additional tutorials are materialized only as their campaign work proceeds.
