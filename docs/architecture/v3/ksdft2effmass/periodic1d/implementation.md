# Implementation plan

## Current boundary

Phase 1 is implemented outside the retained-generation package:
[`model_systems.mathieu1d`](../model_systems/mathieu1d/index.md) owns the direct typed
Mathieu1D vertical slice and `calculations/mathieu1d/` owns its direct scripts and sole
live unsealed execution.

Phase 2 is also implemented. `periodic1d.fourier_locality` owns the direct rank-one
configuration, analyzer, result, byte-owning independent verifier, authenticated
visualization projection, and closed renderer. The former `isolated_band/` source,
Fourier toy-parent record, aggregate predecessor test, exports, and Sphinx page were removed
after direct replacement and explicit authorization.

The installed package now has this mixed migration state:

```text
periodic1d/
├── model.py
├── fourier_locality/       # implemented direct lifecycle
├── multiband_alignment/    # predecessor retained for Phase 3
└── admissible_sets/         # predecessor retained for Phase 4
```

The two remaining predecessor children have frozen definitions and results, a producer,
a serializer, and an independent numerical verifier. Those real supported contracts
predate the direct architecture in four important respects:

1. result serializers are family-local rather than shared typed-record boundaries;
2. verifiers accept reconstructed result objects rather than owning original wire bytes;
3. no authenticated typed visualization projection binds verification to rendering; and
4. historical publication-oriented compositions are not yet direct calculation-root
   calculate → verify → render successors.

The rewrite replaces these remaining boundaries family by family. It does not wrap them
in a compatibility facade or retain two maintained implementations indefinitely.

## Target source shape

The target is behavioral, not a mandate that every family contain identical files.
Expected cohesive children are:

```text
ksdft2effmass/
├── model_systems/
│   ├── periodic_1d/                 # finite parent/fiber representations
│   └── mathieu1d/                   # concrete Mathieu1D vertical slice
└── periodic1d/
    ├── model.py                     # controlled parent models still used by callers
    ├── fourier_locality/            # reusable scalar reduction/locality behavior
    ├── composite_band_alignment/    # alignment and block-locality behavior
    ├── band_equivalence_locality/   # equivalence/locality analysis
    └── admissible_sets/             # constrained-set composition
```

A child exists only when a maintained calculation needs it. No empty marker base,
registry, solver facade, serializer facade, or generic `Periodic1DResult` is introduced.
The exact source name is fixed in the implementation slice that inventories its callers;
this plan does not create aliases from the historical child names.

## Model-owned typed records

Each implemented family owns concrete records with its own fields and wire layout:

- a Python-authored configuration containing physical, finite-representation, sampling,
  gauge/alignment, fitting, and diagnostic choices that actually apply to that family;
- operation-named result sections that store authoritative scientific values once;
- one typed root result that enforces cross-section state-space, shape, ordering, unit,
  energy-reference, and correlation invariants;
- operation-named verification components with explicit tolerances; and
- a typed visualization projection containing only authenticated values required by a
  closed rendering inventory.

Successor records use `BaseTypedRecord` and the shared typed-value codec for canonical
JSON representation. Concrete records implement typed mappings rather than custom NumPy
transport. Canonical bytes make serialization reproducible; they do not make binary64
payloads exact mathematical values. SHA-256 remains verifier and provenance behavior,
never serializer behavior.

The rewrite does not force scalar, rank-two, admissible-set, and higher-rank values into
one data-transfer object. Shared result sections are used only when their mathematical
meaning, units, and invariants are identical.

## Analysis composition

Production analyzers are concrete actions. They may compose canonical low-level owners,
but they do not hide them behind a periodic solver facade.

A scalar Fourier-locality analyzer may compose:

1. a declared finite parent representation;
2. an ordered scalar band selection;
3. complete reciprocal-to-cell Fourier transformation;
4. separately requested truncation or fitting routes; and
5. training, withheld-evaluation, Parseval, bandwidth, curvature, and locality
   diagnostics.

A composite analyzer additionally owns the declared retained frame, sewing, alignment,
projection, block transform, and block-Hermiticity composition. An admissible-set
analyzer consumes typed upstream values and declared threshold policy; it does not
recompute a hidden alternative upstream calculation or subclass its analyzer.

One expensive solve or eigensystem per declared finite case supplies every downstream
channel that refers to that case. Different representations or refinement axes remain
separate cases rather than being pooled as repeated estimates of one value.

## Byte-owning independent verification

Each successor verifier uses the same admission rule as PIAB1D, QHO1D, and Mathieu1D:

1. require the exact result wire as built-in immutable `bytes`;
2. hash those exact bytes internally;
3. deserialize the same bytes into the model-owned typed result;
4. reconstruct decisive values without invoking the production analyzer;
5. derive the typed visualization projection from independently admitted values;
6. hash the projection's canonical typed JSON bytes internally; and
7. return operation-named verification components and one model-owned aggregate.

A verifier may consume canonical low-level numerical libraries, but it must take a route
independent of the producer composition. For example, production may use canonical
hopping-transform actions while verification evaluates the finite Fourier sums directly.
Shared NumPy/SciPy and binary64 behavior are disclosed limitations, not an independent
physical oracle.

`BaseModelAnalysisVerifier` and `BaseModelAnalysisVerification` may be reused when their
existing behavior is exactly applicable. They do not select periodic references,
tolerances, comparison inventories, gauges, fitting routes, or scientific dispositions.

## Authenticated rendering

Each family defines its own closed plot enumeration and typed visualization data.
Rendering proceeds only when:

- the aggregate verification passes;
- the supplied result digest equals the verifier-owned subject digest;
- the supplied projection digest equals the verifier-derived projection digest; and
- the renderer inventory exactly equals the declared plot inventory.

Model-specific plot actions own data-to-mark relations, subplot actions own axis-local
composition, figure actions own layout, and the common renderer owns PNG encoding and
container admission. The calculation script publishes through an incomplete directory
and atomically exposes only the complete rendering inventory.

No figure reads unauthenticated CSV, imports a producer script, or calculates a new
scientific value that is absent from the authenticated projection. The temporary
[visualization migration plan](visualization.md) defines eight baseline PNGs, one per
study, until each inventory is implemented by concrete classes in its source owner. A
study adds exactly one certificate-obligation PNG only when its declared
`native_plus_certificate` inventory is backed by an admitted certificate export and
checker result; no placeholder is rendered.

## Direct calculation roots

Each scientific family receives its own calculation root and direct stages:

```text
run_01_calculation.py → run_02_verification.py → run_03_render.py
```

The [direct run-script template](direct-scripts.md) is derived from the implemented
PIAB1D, QHO1D, and Mathieu1D adapters. The scripts resolve paths from their own location, execute at
module scope, contain no functions, Workflow, `main()`, parser, custom JSON transport, or
`.tolist()`, refuse to overwrite final or incomplete stage paths, authenticate exact
bytes between stages, and retain incomplete or failed outcomes honestly. Reusable
behavior remains in `python/src/ksdft2effmass/`.

The initial rewrite may retain unsealed executions with an explicit `UNSEALED.md`, as
PIAB1D, QHO1D, and Mathieu1D do. `run_04_seal.py`, package verification, evidence promotion, and
retained execution creation remain separate reviewed and authorized scopes.

## Predecessor disposition

The [Phase 0 inventory](phase-0-inventory.md) selects complete replacement. The former
M1 imports, class layouts, serializer API, schema-v1 runtime surface, and sole direct test
consumer were removed after the Phase 2 replacement gate and explicit authorization;
exact recovery is recorded in the calculation-owned retirement record. Current M2--M3
predecessors remain supported only until their own specified finite calculations,
authenticated plot-data channels, and consumer migrations pass unchanged comparison
gates and receive separate removal authorization.

Historical result and artifact bytes remain unchanged and recoverable from exact Git
objects for provenance. The new runtime neither decodes those packages nor imports,
copies, wraps, subclasses, or executes a calculation `workflow/` directory. There is no
deprecation shim, wildcard re-export, compatibility module, or calculation-local
duplicate source tree. Supported callers move directly to the selected owner.

## Optional formal-certificate export

Formal checking is a separate proposition-specific layer after the native family result
and its independent numerical verification. KSD owns a compact export containing exact
rationals or documented outward rational intervals bound to the native result digest.
Formal owns the exact proposition and checker-soundness theorem. The export is never a
replacement for the native result, and raw binary64 values are never reclassified as
exact.

The [formal-method boundary](formal.md) defines the fail-closed request and checker-result
obligations. No formal certificate is required merely to complete the direct
calculate → verify → render rewrite, and no current checked runtime certificate exists.
