# Common-space diagnostics incubation package

`common_space.diagnostics` contains calculation-owned diagnostic composition that is
being separated from the C6-B20-W21 Slater--Koster entrypoint before any reviewed
migration of reusable behavior.

## Current public surface

The package deliberately exports:

- immutable request and result records;
- strict development-request decoding, repository-path confinement, and source
  authentication;
- the exact atomic-to-projection basis transformation;
- the native-format singular-value uncertainty bound;
- full-grid rank and normalized principal-angle diagnostics;
- nominal minimum-direction atomic and grouped orbital weights at every deficient point;
- semantic cross-checks against the authenticated S30, S105, and immutable S110 JSON,
  with legacy S110 `A`/`B` labels confined to an explicit positional correlation into
  the descriptive diamond-center identifiers;
- complete parser-facade and matrix-convention source authentication;
- deterministic human-readable progress reporting; and
- the CSD0/CSD1 producer action.

Each `KPointDiagnosis` now carries `minimum_direction_atomic_weights`: ten nominal
squared SVD-vector magnitudes in the result's declared atomic basis order when the
point is deficient, or an empty tuple when it is full rank. The separately aggregated
`minimum_direction_group_weights_s_p_s_star` wire field uses coordinates `(0,5)`,
`(1,2,3,6,7,8)`, and `(4,9)`. These are dimensionless numerical diagnostics, not
certified intervals or a unique orbital diagnosis when several directions are
unresolved. They are trial-coordinate weights, not orbital populations or charges.
Floating normalization is not asserted to be exact. The existing Gamma
mapping and its frozen comparison are preserved; no weights are copied from Gamma
to another point. Serialization makes detached lists from immutable tuple fields.
Historical S30/S105/S110 bytes are unchanged. The separately authorized
[retained producer checkpoint](../../analysis/common-space-producer/) now contains a
new 216-point reconstruction; it is not independent verification.

The scientific request remains with its owner at
[`../../analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json`](../../analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json).
The direct entrypoint remains beside that request and imports this package explicitly.
It requires a nonexistent output root and creates artifacts exclusively; existing output
roots are rejected before source processing. There is no compatibility module at the
former flat implementation path.

The AMN boundary uses the pinned provider's constructor-owned
`Wannier90TrialOrbitalOverlapParser(payload=...).parse()` and explicit
`trial_orbital_count`. The unretained development request binds the current provider
module bytes; historical S30, S105, and S110 identities are unchanged. Synthetic
native-file tests exercise the real provider parsers and require a different trial
count to fail before rank reconstruction. They are not retained silicon calculations.

Retained `execute()` now requires the exact adopted source declaration, binds all 16
source paths, authenticates the shared seven-module native boundary and exact ordered
coordinate presentations, and supplies the geometric construction-index inventory.
Its direct entrypoint requires `--source-declaration`. Synthetic tests must explicitly
select `CommonSpaceReviewScope.synthetic`; that route cannot consume a retained
source declaration and produces neither retained-source associations nor completion
receipts. The scope enum is a trust context, never execution authority.

The producer's human-readable and JSON continuation reports require independent
CSD1-V verification before CSD2. Reproducing the old rank gate
must not be reported as permission to skip those missing stages. The prospective
precision amendment makes higher arithmetic precision conditional on unresolved
arithmetic bounds or plausibly arithmetic route disagreement after source/software
checks; a decisive independently checked result needs no extra precision artifact.

## Migration boundary

This is an incubation package, not a supported repository library. A later review must
separate reusable finite-rank overlap diagnostics from silicon-specific source binding,
threshold policy, evidence comparison, artifact persistence, and scientific
interpretation before moving any behavior into `python/src/ksdft2effmass/`.

The producer does not import `run_definition_fit.py`. Its numeric `producer_scope`
remains `projector-rank-reconstruction-subset` in the original schema; complete
producer delivery additionally includes the separately retained geometric index
inventory and actual completion evidence. This is not electronic symmetry analysis. The separately implemented
[`verification/`](../verification/) package now contains declared native-byte
correlation, shared provider parsing, independent exact overlap reconstruction,
Gram-rank and input-error bounds, deficient-direction and unitary controls, complete-grid
composition, exclusive numerical output, and subsequent producer comparison. Only
synthetic tests and a separately authorized [retained CSD1-V run](../../analysis/common-space-verification/)
have exercised its numerical verification. The complete real source bundle now
authenticates, and all 216 independent Gram results correlate with the original producer
under the declared source/uncertainty contract. This does not establish a CSD2 electronic
symmetry action or physical validation. No unconditional higher-precision
sensitivity record is required; unresolved arithmetic or disagreement still stops
progression under the conditional precision policy. The independent
adapter consumes the actual producer JSON after independent computation and correlates
its sources, conventions, threshold, point inventory, and reported weights. That does
not establish completed scientific prerequisites, retained verification, symmetry
attribution, material validation, or scientific acceptance. No retained execution,
evidence promotion, fit, Quantum ESPRESSO run, or Wannier90 run follows from these checks.

## Development checks

From the repository root:

```console
PYTHONPATH=calculations/Si/bulk python/.venv/bin/pytest -q \
  calculations/Si/bulk/common_space/diagnostics/tests
python/.venv/bin/ruff check --config calculations/.ruff.toml \
  calculations/Si/bulk/common_space/diagnostics
python/.venv/bin/ruff format --check --config calculations/.ruff.toml \
  calculations/Si/bulk/common_space/diagnostics
```
