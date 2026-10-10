# Conference Paper 1 isolated-band calculation package

## Status

This directory retains the completed controlled one-dimensional isolated-band
calculation for ICMSEP 2026 Conference Paper 1. `protocol-freeze.json` binds
`input.json` and `protocol.md` before confirmatory execution. The independent retained
verification passes.

This package is separate from the direct admissible-set demonstration in the parent
directory. It does not replace or rewrite the parent `result.json`, whose identity and
schema belong to that separate demonstration.

## Evidence role

The package provides controlled synthetic numerical evidence for:

- plane-wave parent-representation refinement;
- finite-difference refinement against the same declared finite parent reference;
- complete reciprocal-to-hopping Fourier reconstruction;
- symmetric finite-range hopping truncation;
- equal-weight direct fitting using the training mesh only;
- direct-fit versus Fourier-mediated route comparison;
- hopping Hermiticity and Parseval diagnostics;
- scalar bandwidth and zone-center-curvature diagnostics; and
- evaluation on a frozen staggered withheld mesh disjoint from training coordinates.

These channels support bounded statements about finite reconstruction, truncation,
route comparison, and withheld evaluation. They do not test multiband or nonidentity
alignment, gauge optimization, Wannier localization, two-dimensional shell locality,
material transferability, silicon, or uncertainty quantification.

The historical Mathieu, common-low-mode, weak-potential, and stress channels were not
recalculated and are not claims of this package.

## Maintained software boundary

The producer composes the canonical package:

```python
from ksdft2effmass.periodic1d import (
    Periodic1DIsolatedBandCalculationDefinition,
    Periodic1DIsolatedBandCalculator,
    Periodic1DIsolatedBandResultJsonSerializer,
    Periodic1DIsolatedBandResultVerifier,
)
```

The result serializer owns the distinct wire identity:

```text
ksdft2effmass.periodic1d.isolated-band-calculation-result.v1
```

It does not masquerade as the historical Appendix G result format. The retained
`verify_result.py` does not import `run.py`; it independently rebuilds the finite parent
matrices, spectra, Fourier blocks, truncations, fits, and diagnostics from the frozen
input. A passing verifier establishes bounded numerical consistency only, not
scientific acceptance or material validity.

## Retained files

```text
README.md
input.json
protocol.md
protocol-freeze.json
run.py
result.json
verify_result.py
verification.json
figure-data.csv
isolated-band-summary.png
report.md
software.json
source.sha256
SHA256SUMS
```

- `input.json` freezes the model, representations, sampling roles, ranges, and
  tolerances.
- `protocol.md` freezes mathematical conventions and the evidence boundary.
- `protocol-freeze.json` records the pre-execution input and protocol hashes.
- `run.py` is the thin producer and figure entry point.
- `result.json` is the deterministic schema-v1 typed result.
- `verify_result.py` is the independent retained-document parser and reconstruction
  entry point.
- `verification.json` records the passing independent reconstruction.
- `figure-data.csv` and `isolated-band-summary.png` derive from the retained result.
- `report.md` gives a bounded human-readable interpretation.
- `software.json` and `source.sha256` bind runtime and uncommitted source identities.
- `SHA256SUMS` seals the retained package.

## Reproduction

From this directory and the repository root environment:

```bash
../../../../../python/.venv/bin/python run.py
../../../../../python/.venv/bin/python verify_result.py
shasum -a 256 -c SHA256SUMS
```

Re-running `run.py` overwrites the derived result, figure data, and figure with values
from the frozen input. After any authorized rebuild, regenerate `software.json`,
`source.sha256`, and `SHA256SUMS`; do not claim identity with this retained package if
any sealed digest differs.

## Execution boundary

The retained work is an in-process synthetic numerical study. It invoked no Quantum
ESPRESSO, Wannier90, VASP, ABINIT, scheduler, remote compute, or private material data.
It does not authorize submission, publication, release, or a protected material
calculation.
