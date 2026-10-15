# Experiment execution structure

## Baseline

The maintained source baseline is the existing publication-independent periodic-1D
experiment package:

```text
experiments/periodic-reduction/single-band-fourier-reduction/periodic1d/
├── pyproject.toml
├── uv.lock
├── README.md
├── src/single_band_fourier_reduction/
│   ├── __init__.py
│   ├── definition.py
│   ├── experiment.py
│   └── results.py
└── tests/
    └── test__SingleBandFourierReductionExperiment.py
```

The periodic-1D execution path is an in-process typed composition:

```text
immutable definition
        |
        v
Experiment.execute(definition)
        |
        v
immutable result
```

The constrained periodic-1D model-adequacy package adds `verify.py`, with an independent
result verifier that does not call the experiment Action. The hopping-shell hierarchy
needs that additional verification leg.

There is no nested `experiment/` or `execution/` directory. `experiment.py` is the
module that owns the experiment Action, matching the existing experiment packages.

## Selected package structure

Once the remaining controls and source contracts close, the isotropic periodic-2D
package will use:

```text
experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/
├── pyproject.toml
├── uv.lock
├── README.md
├── protocol.md
├── orbit-support-inventory.md
├── execution-structure.md
├── src/hopping_shell_hierarchy/
│   ├── __init__.py
│   ├── definition.py
│   ├── experiment.py
│   ├── results.py
│   ├── verify.py
│   └── serialization.py
└── tests/
    ├── test__HoppingShellHierarchyExperiment.py
    ├── test__HoppingShellHierarchyResultVerifier.py
    └── test__HoppingShellHierarchySerialization.py
```

The source directory is not created until the definition, result, verifier, and schema
contracts are ready. This page selects the module boundaries; it does not create empty
implementation placeholders.

## Execution graph

```text
strict input document
        |
        v
serialization.py decoder
        |
        v
HoppingShellHierarchyDefinition
        |
        +------------------------------+
        |                              |
        v                              v
HoppingShellHierarchyExperiment       HoppingShellHierarchyResultVerifier
        |                              ^
        v                              |
HoppingShellHierarchyResult ----------+
        |
        v
serialization.py encoder
        |
        v
strict result document
```

The producer and verifier receive the same immutable definition. The verifier also
receives the immutable result but does not call `HoppingShellHierarchyExperiment`, use
its private functions, or treat its dispositions as an oracle.

## Module responsibilities

### `definition.py`

Owns the immutable experiment definition and exact scientific controls:

- family/version correlation supplied by the caller;
- copied compact parent data and donor digests;
- lattice, Fourier, unit, and energy-reference conventions;
- exact operation, orbit, member, multiplicity, and support inventories;
- coefficient box, weights, thresholds, metric, resolution, and sample roles;
- numerical and conservative-arithmetic policies; and
- exact owner method identities.

It performs strict structural validation without file I/O, fitting, minimization,
certificate construction, or result-dependent inference.

### `experiment.py`

Owns one cohesive Action, `HoppingShellHierarchyExperiment`, following
`SingleBandFourierReductionExperiment` and `ConstrainedAdmissibleSetsExperiment`.
Its `execute(definition)` method:

1. reconstructs and checks the selected parent projection;
2. constructs the exact orbit features and class masks;
3. calls reviewed PhysKit, Numerics, and Optimization capabilities directly;
4. constructs channel quadratics in the experiment's scientific coordinates;
5. obtains minima, witnesses, feasible pairs, and certificate evidence;
6. evaluates evaluation, withheld, and locality channels only after decisive controls are fixed; and
7. returns one immutable correlated result.

It performs no file I/O, ambient discovery, plotting, report generation, external
calculator execution, protocol mutation, or retained-evidence sealing. It contains no
pass-through solver facade and no duplicate generic numerical kernel.

### `results.py`

Owns immutable experiment-specific records:

- projected-parent diagnostics;
- per-channel quadratic correlation;
- per-support-class evidence and disposition;
- common-witness, feasible-pair, and owner-certificate correlation;
- evaluation, withheld, and locality diagnostics;
- hierarchy conclusion; and
- explicit limitations and bounded nonclaims where represented as structured fields.

Constructors enforce local and cross-record invariants. They do not solve optimization
problems, infer missing evidence, or repair malformed data.

### `verify.py`

Owns `HoppingShellHierarchyResultVerifier` and its immutable verification result. The
verifier independently reconstructs decisive relationships from the definition and
result:

- donor and projection correlation;
- operations, orbits, ordering, multiplicities, and support prefixes;
- spectral/operator features and direct residual losses;
- box minima and channel nonemptiness evidence;
- every common witness and feasible pair;
- support endpoints, metric dual norms, conservative lower bounds, and certificate
  premises;
- evidence/disposition and minimum-class logic; and
- evaluation, withheld, and locality role isolation.

It does not call the producer Action or reuse producer-private feature construction. It
may use reviewed owner validation and arithmetic contracts when those contracts are
the objects being verified, but producer solver status is never its oracle.

### `serialization.py`

Owns strict canonical input, result, and verification codecs. It transports scientific
state but does not construct models, run the experiment, choose defaults, infer
identities, alter dispositions, or repair certificate evidence. Missing and unknown
fields fail closed.

Exact serializer class names and schema IDs remain open until the wire contracts are
selected.

## Test structure

Like the existing experiment packages, each test module groups one cohesive behavior
under one `Test...` class.

- `TestHoppingShellHierarchyExperiment` covers deterministic composition, owner calls,
  role isolation, and result correlations.
- `TestHoppingShellHierarchyResultVerifier` covers independent reconstruction,
  producer-import exclusion, and adversarial evidence mutations.
- `TestHoppingShellHierarchySerialization` covers strict fields, canonical round trips,
  schema rejection, and byte stability.

Owner numerical algorithms are qualified in their owner repositories. Experiment tests
verify scientific binding and direct owner consumption rather than duplicate those
algorithm suites.

## Retained execution correspondence

A future retained run will preserve the useful periodic-1D evidence sequence:

```text
input + protocol freeze
        -> typed experiment execution
        -> canonical result
        -> independent verification
        -> figure data / figure / report
        -> software and source provenance
        -> checksum catalog
```

Those wire artifacts and entry-point scripts are not source-package modules and are not
specified as a new nested execution framework here. Their exact paths, version/run
layout, schema IDs, and retention rules remain part of the still-open evidence policy.
The eventual entry points must only decode files, call the typed package objects, encode
results, and derive presentation artifacts; scientific behavior remains in the modules
above.

## Current status

The package layout and typed execution graph are selected. Source creation remains
blocked on the open scientific controls, completed owner capabilities, strict wire
contracts, and mirrored module/class architecture. This page authorizes no source
skeleton, immutable version, retained run, experiment execution, commit, or push.
