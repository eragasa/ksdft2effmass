# Direct run-script template

## Reference boundary

Every Periodic1D study follows the direct module-scope pattern already implemented by
`calculations/piab1d/` and `calculations/qho1d/`:

```text
run_01_calculation.py → run_02_verification.py → run_03_render.py
```

The target is similar sequencing and failure behavior, not copied scientific content.
Each study imports its own typed configuration, analyzer, result, verifier, verification,
visualization data, and visualizer classes.

## Rules shared by all three scripts

Each script:

- begins with a Python shebang, one stage-specific module docstring, and
  `from __future__ import annotations`;
- executes direct composition at module scope;
- contains no function or class definition, Workflow, `main()`, argument parser,
  `import json`, `.tolist()`, registry, or generic execution engine;
- declares the calculation family, execution identifier, evidence status, and claim
  boundary in Python source;
- resolves every path from `Path(__file__).resolve()`;
- uses `TypedJsonValueCodec` only for typed metadata mappings and model-owned
  `to_json()`/`from_json()` boundaries for scientific records;
- rejects existing final and incomplete-stage destinations before calculation;
- hashes the exact bytes it reads or writes rather than a reserialized mapping;
- records its own source digest and applicable implementation-source digests;
- fails with a nonzero process status on any exception; and
- performs no sealing, publication decision, remote execution, or external calculator
  invocation.

No shared script helper is introduced merely to shorten these adapters. Repeated path and
stage mechanics remain explicit unless an independently reviewed action object acquires a
real maintained caller outside one script.

## `run_01_calculation.py`

The calculation script follows this ordered template.

### 1. Authored declarations

Declare:

- `EXECUTION_ID` and `CALCULATION_FAMILY`;
- evidence status and a bounded claim statement;
- one concrete typed configuration constructed from Python values; and
- any study-specific exact enum selections required by that configuration.

JSON is an output representation, not authored scientific input.

### 2. Paths and no-overwrite gate

Resolve repository, calculation, execution, and temporary execution paths. Reject both:

```text
executions/<execution-id>/
executions/.<execution-id>.incomplete/
```

before invoking the analyzer.

### 3. Typed calculation

Instantiate one concrete family analyzer and call its direct operation with the typed
configuration and required calculation metadata. Reuse one parent solve or eigensystem
for every channel that refers to the same finite case.

Serialize:

- `inputs/configuration.json` from the typed configuration; and
- `results/result.json` from the typed family result.

Immediately reconstruct each typed record from its bytes when the record boundary does
not already guarantee round-trip admission. Hash those exact bytes.

### 4. Execution record

Write canonical `execution.json` containing at least:

- schema version, calculation family, and execution identifier;
- local deterministic execution kind and UTC creation time;
- completed, failed, or incomplete outcome;
- evidence status and claim boundary;
- relative configuration and result paths plus SHA-256 digests;
- result schema;
- required numerical route declarations;
- script and analyzer source locators and digests;
- runtime versions; and
- `sealed: false`.

Write the complete initial package beneath the incomplete directory, then expose it with
one same-filesystem rename. Never create the final execution directory first and fill it
incrementally.

## `run_02_verification.py`

The verification script follows this ordered template.

### 1. Paths and stage gate

Resolve the selected execution, exact input and result paths, final verification
directory, and `.verification.incomplete`. Reject an existing final or incomplete
verification directory. Require the completed calculation artifacts.

### 2. Correlation checks

Decode `execution.json` as a typed metadata mapping and check:

- execution identifier and calculation family;
- completed calculation outcome;
- declared configuration and result paths;
- configuration and result schema declarations;
- required numerical-route declarations; and
- SHA-256 digests of the exact configuration and result bytes.

Do not trust a success label inside the result.

### 3. Byte-owning verification

Pass the exact immutable result bytes to the concrete verifier:

```text
FamilyVerifier(result_wire=result_bytes).result()
```

The verifier reconstructs the typed result from those same bytes, independently checks
the declared finite operations, derives the authenticated visualization projection, and
calculates the subject and projection digests internally. The script does not supply a
projection digest.

### 4. Verification record

Write one canonical `verification/verification.json` containing:

- schema version and family-specific verification schema;
- calculation family and execution identifier;
- a plain-language independent route;
- the typed verification aggregate;
- typed visualization data;
- comparison count or another closed family inventory;
- claim boundary;
- exact result digest; and
- script digest.

Write through `.verification.incomplete` and rename it to `verification/`. If the typed
aggregate does not pass, retain the completed verification record when required by the
evidence policy and then exit nonzero with operation-named failures.

## `run_03_render.py`

The rendering script follows this ordered template.

### 1. Paths and stage gate

Resolve result, verification, final figures, temporary figures, authored report, final
execution report, and temporary report paths. Reject any existing final or incomplete
rendering destination. Require calculation, verification, and authored report inputs.

### 2. Authentication

Read exact result and verification bytes. Check:

- execution identifier and calculation family;
- result digest recorded by verification;
- verifier-owned subject digest;
- passing typed verification; and
- typed visualization projection admission.

Re-run the concrete byte-owning verifier from the exact result bytes and admit the
stored aggregate and projection only when their canonical bytes equal the independently
recomputed pair. Render the recomputed pair, not the merely decoded stored values. This
rejects an omitted or altered comparison without maintaining a second hard-coded list of
all dynamically named observations.

Construct the concrete family visualizer from the admitted projection data and passing
verification. No plotting begins before these checks pass.

### 3. Closed rendering

Call the visualizer and require exact set equality between produced plot enum members and
the declared plot inventory. The selected `native_only` inventory contains the study's
one baseline PNG. `native_plus_certificate` contains that baseline plus exactly one
certificate-obligation PNG backed by an admitted checker result.

Write every PNG behind `.figures.incomplete`. Copy only declared report source,
bibliography, style, and authenticated figure files into the temporary report directory.
Do not calculate scientific values, read unauthenticated CSV files, or import a producer
script.

### 4. Rendering record and publication

Write canonical `rendering.json` containing:

- rendering schema, execution identifier, and completed outcome;
- result and verification paths plus exact digests;
- every PNG filename, media type, and digest;
- every admitted report file and digest;
- script and concrete visualizer source locators and digests;
- Python, NumPy, Matplotlib, and backend versions; and
- a bounded presentation-only claim statement.

Publish the completed report and figure directories only after every file and digest has
been written. No incomplete path remains after success.

## Study-specific class bindings

Mathieu1D has finalized the first concrete binding; its source contract is documented at
[`model_systems.mathieu1d`](../model_systems/mathieu1d/index.md). Implemented Periodic1D
slices use their exact public owners rather than a generic Periodic1D aggregate.

| Study | Configuration/analyzer/result prefix | Verification prefix | Visualization prefix |
|---|---|---|---|
| Mathieu1D | `Mathieu1d` | `Mathieu1d` | `Mathieu1d` |
| Compatible rank-one control | `Periodic1DFourierLocality` | `Periodic1DFourierLocality` | `Periodic1DFourierLocality` |
| Rank-two band equivalence | `Periodic1DRank2` | `Periodic1DRank2Calculation` | `Periodic1DRank2ParentFamily` |
| Rank-two composite alignment | `Periodic1DCompositeBandAlignment` | `Periodic1DCompositeBandAlignment` | `Periodic1DCompositeBandAlignment` |
| Confirmatory admissible sets | `Periodic1DConfirmatoryAdmissibleSet` | `Periodic1DConfirmatoryAdmissibleSet` | `Periodic1DConfirmatoryAdmissibleSet` |
| Scalar/direct demonstration | `Periodic1DScalarAdmissibleSet` | `Periodic1DScalarAdmissibleSet` | `Periodic1DScalarAdmissibleSet` |
| Threshold sensitivity | `Periodic1DThresholdSensitivity` | `Periodic1DThresholdSensitivity` | `Periodic1DThresholdSensitivity` |
| Higher-rank alignment | `Periodic1DHigherRankAlignment` | `Periodic1DHigherRankAlignment` | `Periodic1DHigherRankAlignment` |

Each prefix expands only into classes the study needs, such as `Configuration`,
`Analyzer`, `CalculationResult`, `Verifier`, `Verification`, `VisualizationData`,
`VisualizationPlotEnum`, and `Visualizer`. Plot, subplot, figure, and renderer class names
follow their concrete data-to-mark or composition responsibility rather than a mechanical
name template.

## Calculation-root bindings

Existing selected roots are:

| Study | Calculation root |
|---|---|
| Mathieu1D | `calculations/mathieu1d/` |
| Compatible rank-one control | `calculations/periodic1d/rank1/fourier-locality/` |
| Rank-two band equivalence | `calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/` |
| Rank-two composite alignment | `calculations/periodic1d/rank2/composite-band-alignment-locality/` |
| Higher-rank alignment | `calculations/periodic1d/rankN/composite-band-alignment-locality/` |

The three admissible-set calculation roots are selected only after the Phase 0 inventory
reconciles historical paths and current consumers. This document does not create
placeholder directories or conflate them with the rank-two band-equivalence root.

## Required script tests

Every implemented study adds one cohesive integration-test class establishing:

1. AST-level absence of functions, classes, Workflow, parser, custom JSON, and `.tolist()`
   in all three scripts;
2. a fresh copied calculate → verify → render execution using only the installed package
   and declared calculation resources;
3. exact configuration/result correlation and byte-owning verification;
4. rejection of modified result, verification, projection, or plot inventory values;
5. non-overwrite behavior for every final and incomplete stage path;
6. atomic publication with no surviving incomplete path after success;
7. exact expected baseline and optional certificate filenames and digests; and
8. explicit failed-verification behavior with no published figures.

Tests establish script and finite numerical behavior only. They do not retain a new
execution, seal evidence, or establish scientific validity.
