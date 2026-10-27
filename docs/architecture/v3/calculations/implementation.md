# Calculation package implementation

## Scope

This document defines the maintained filesystem and execution lifecycle for calculation
packages under `calculations/`. It applies to new packages and prospective migrations.
It does not rewrite historical calculation bytes, embedded identities, checksum
catalogs, or provenance paths.

A calculation family, an execution, an evidence package, a schema revision, a software
release, and an arXiv manuscript revision are distinct identities. Passing calculation
or verification stages does not establish scientific validation, human acceptance,
publication, or release.

For the `calculations/` tree, this Architecture v3 page is authoritative. Architecture
v2 calculation and experiment records remain useful historical design and migration
context, but any requirement there to assign a pre-publication scientific `.vN` does
not govern new calculation packages.

## Publication-version boundary

Before a corresponding arXiv manuscript revision is posted, a calculation uses its
stable family identity and explicit execution identities. It receives no scientific
`.vN` or publication-version identity. Creating another execution does not create a
version.

When an arXiv revision is posted, the publication owner records a manifest that maps
that revision to one exact sealed execution and evidence-package digest. The
publication manifest may identify the posted revision as `v1`, `v2`, and so on. It does
not rename the calculation family or rewrite the execution package. A later arXiv
revision may bind a different execution. Publication manifests remain with the
publication owner rather than beneath the calculation package.

JSON schema revisions, serializer revisions, Workflow revisions, dependency versions,
and software release tags remain separate technical identities where applicable. They
must not be presented as calculation-publication or arXiv versions.

Historical records that already contain `.vN` identities remain exact provenance.
They are not renamed, silently reclassified, or used as the naming template for new
pre-arXiv executions.

## Target layout

A maintained calculation package uses this target shape:

```text
calculations/<name>/
├── README.md
├── protocol.md
├── evidence-policy.md
├── inputs/
├── schemas/
├── technical_report/
│   └── technical_report.tex
├── run_01_calculation.py
├── run_02_verification.py
├── run_03_render.py
├── run_04_seal.py
├── verify_package.py
└── executions/
    └── <execution-id>/
        ├── execution.json
        ├── inputs/
        ├── schemas/
        ├── results/
        ├── verification/
        ├── figures/
        ├── technical_report/
        │   └── technical_report.tex
        ├── provenance.json
        ├── source.sha256
        ├── SHA256SUMS
        └── evidence-package-identity.txt
```

The root `inputs/` and `schemas/` directories contain the active authored contracts.
The root `technical_report/technical_report.tex` is the maintained calculation-facing
report source. An execution package contains exact copies of every input and schema used
for that execution and an execution-bound technical report source. Later edits to the
authored copies cannot change the meaning of a retained execution.

Report-local bibliography, style, and static-asset files may accompany
`technical_report.tex` when declared by the package. A compiled PDF is a generated
artifact and is not retained evidence unless the execution contract explicitly admits
and checksums it.

A package may have multiple named result or verification documents when its protocol
contains multiple prespecified channels. Their dependencies are explicit. For example,
a derived decomposition result that consumes a residual result records the exact
consumed result digest rather than relying on a shared directory or filename. Optional
artifacts are declared by the protocol; absence must not be silently treated as
success.

## Execution identity and outcome

The calculation-family identity names the durable scientific question and method
boundary. An execution identity names one concrete calculation attempt or
execution-free materialization under that family. It contains no `.vN` component
before publication freeze.

`execution.json` is immutable after creation and records at least:

- the calculation-family and execution identities;
- the execution kind and exact requested stage inventory;
- creation time in UTC;
- `completed`, `failed`, or `incomplete` execution outcome;
- input and schema identities;
- the local-only, external-calculator, remote, or execution-free boundary; and
- a claim boundary.

`development` and `candidate` are human lifecycle dispositions, not execution
outcomes. Promoting an execution from development consideration to candidate status is
recorded separately by reference to the sealed evidence-package digest. It does not
mutate `execution.json` or any sealed package byte. Candidate status does not establish
scientific acceptance or authorize publication.

## Staged entry points

Maintained calculation entry points resolve paths from their own location, terminate
with failure on an exception, and refuse to overwrite an artifact owned by their stage.
They are executable composition scripts, not importable source modules. The scripts
contain direct module-scope composition and remain outside package API discovery and
test collection. Reusable scientific behavior remains in `python/src/ksdft2effmass/`
or its reviewed dependency owner.

### `run_01_calculation.py`

The calculation stage:

- reads explicit authored inputs and schemas;
- authenticates required dependencies and authority before any protected effect;
- creates one new execution directory with no-overwrite semantics;
- writes exact execution input and schema copies;
- performs only the calculation defined by the protocol;
- writes result and initial provenance records; and
- records failure or incompleteness without reporting success when a required action
  fails.

It does not render publication figures, make human acceptance decisions, assign a
publication version, or seal the package.

### `run_02_verification.py`

The independent-verification stage:

- reads an existing unsealed execution;
- verifies input/result correlation;
- reconstructs decisive checks through the declared independent route without calling
  the producer action;
- writes machine-readable verification records under `verification/`; and
- refuses to overwrite an existing verification record.

A verifier does not treat serialized success labels as oracles. Verification failure
is retained when required by the evidence policy; it is not converted into a successful
execution.

### `run_03_render.py`

The rendering stage:

- reads only authenticated results and completed verification records;
- writes declared figures and the execution-bound
  `technical_report/technical_report.tex`;
- preserves the distinction between primary outcomes, controls, diagnostics, and
  refinement checks; and
- refuses to overwrite an existing rendering.

Figures and prose are derived presentation artifacts, not additional scientific
evidence classes.

### Implemented PIAB1D direct lifecycle

The PIAB1D successor implements `run_01_calculation.py`,
`run_02_verification.py`, and `run_03_render.py` as a direct
calculate → verify → render chain. It does not implement a Workflow, registry, generic
execution engine, nested execution graph, argument parser, or JSON-authored scientific
input.

Calculation writes one typed `Piab1dCalculationResult` through an incomplete-stage
path. Verification decodes that result, independently reconstructs all reference
families, derives and authenticates visualization data, and writes a 79-comparison
aggregate through `.verification.incomplete`. Rendering accepts only the passing
aggregate bound to the exact result and projection digests, generates the closed
13-figure inventory, and publishes through `.figures.incomplete`.

The complete source architecture is documented at
[`ksdft2effmass.model_systems.piab1d`](../ksdft2effmass/model_systems/piab1d/index.md).
The retained flat PIAB1D artifacts remain historical. Successor execution retention,
checksum updates, sealing, and evidence promotion remain separate authorized actions.

### Prospective Periodic1D direct lifecycles

The [Periodic1D Architecture v3 plan](../ksdft2effmass/periodic1d/index.md) applies the
same direct calculate → verify → render behavior to eight separate studies: Mathieu1D,
the compatible rank-one null control, rank-two band-equivalence locality, rank-two
composite alignment, confirmatory constrained admissible sets, the minimal scalar/direct
admissible-set demonstration, post-hoc threshold sensitivity, and higher-rank composite
alignment. These are separate calculation records, not stages or versions of one
universal Periodic1D execution.

Each selected family receives concrete typed records, a byte-owning independent
verifier, an authenticated family-specific visualization projection, and its own closed
rendering inventory. Shared mechanics do not imply shared scientific inputs, result
wires, tolerances, evidence policies, or claims. No direct Periodic1D successor is
claimed implemented by this prospective section.

### `run_04_seal.py`

The seal stage is the sole writer of the final checksum catalog and evidence-package
identity. It:

1. checks that every protocol-required stage and artifact is present;
2. checks canonical serialization and exact schema validity;
3. binds exact source, repository, dependency, runtime, input, result, verification,
   rendering, and claim-boundary identities;
4. writes `source.sha256` and `provenance.json` before the final manifest;
5. writes `SHA256SUMS` over every admitted package file except the manifest and its
   nonrecursive identity file; and
6. writes `evidence-package-identity.txt` as the declared digest of the exact
   `SHA256SUMS` bytes.

The seal stage refuses an already sealed directory. No execution-package byte changes
after sealing. A partially written seal is an incomplete package and cannot be
represented as sealed evidence.

A dirty worktree must not be represented as its base commit. Provenance records the
base revision, dirty state, and exact in-scope source-byte identities. A digest proves
byte identity only; it does not establish producer causality, scientific validity, or
availability of unhashed source bytes.

### `verify_package.py`

Package verification is read-only. It verifies the evidence-package identity, every
manifest entry, canonical documents, schemas, cross-document identities, provenance,
and the recorded verification disposition. It performs no calculation, rendering,
sealing, acceptance, publication, or repair.

Package verification establishes package integrity under its declared checks. It does
not establish material validity, convergence beyond the protocol, scientific
acceptance, or publication status.

## Failure, retention, and authority

A failed or incomplete execution may be retained when the package evidence policy
requires attempt history. Its outcome and missing stages remain explicit. It must not
be promoted by omitting failure records or by copying successful artifacts from a
different execution without an exact declared dependency.

This structure grants no authority for production Quantum ESPRESSO or Wannier90
execution, remote or cluster computation, destructive data operations, dependency
changes, evidence promotion, publication, release, or DOI activity. Those actions
retain their separate authorization and human-decision boundaries.

## Migration

Existing flat, publication-labelled, or historically versioned packages migrate only
through an explicit alias and provenance crosswalk. Migration preserves exact old paths
at their repository revision, content identities, checksums, execution meaning, and
publication references. A new layout may wrap or supersede historical records; it must
not relabel a collection of independent historical outputs as one atomic execution
without evidence that establishes that relationship.

Removal of historical calculation data from the maintained tip requires explicit human
authorization. Until then, a successor layout is added non-destructively and prior
records remain available under their established locators.
