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
- semantic cross-checks against the authenticated S30, S105, and immutable S110 JSON,
  with legacy S110 `A`/`B` labels confined to an explicit positional correlation into
  the descriptive diamond-center identifiers;
- complete parser-facade and matrix-convention source authentication;
- deterministic human-readable progress reporting; and
- the CSD0/CSD1 producer action.

The scientific request remains with its owner at
[`../../analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json`](../../analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json).
The direct entrypoint remains beside that request and imports this package explicitly.
It requires a nonexistent output root and creates artifacts exclusively; existing output
roots are rejected before source processing. There is no compatibility module at the
former flat implementation path.

## Migration boundary

This is an incubation package, not a supported repository library. A later review must
separate reusable finite-rank overlap diagnostics from silicon-specific source binding,
threshold policy, evidence comparison, artifact persistence, and scientific
interpretation before moving any behavior into `python/src/ksdft2effmass/`.

The current producer does not import `run_definition_fit.py`, but it implements only the
projector-rank reconstruction subset of CSD1. The separately implemented verifier,
higher-precision sensitivity extension, symmetry-related deficient-point inventory, and
CSD2 symmetry attribution remain absent. No retained execution, evidence promotion, fit,
Quantum ESPRESSO run, or Wannier90 run is authorized by this package.

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
