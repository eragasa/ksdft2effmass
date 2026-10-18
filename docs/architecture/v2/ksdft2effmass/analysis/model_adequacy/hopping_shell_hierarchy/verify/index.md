# `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.verify`

## Purpose and status

Prospective independent typed-result verifier for HSH-1. No source module exists.

## Prospective public contract inventory

- [`Periodic2DHoppingShellHierarchyVerificationResult`](Periodic2DHoppingShellHierarchyVerificationResult/index.md) — immutable bounded defect and premise summary.
- [`Periodic2DHoppingShellHierarchyResultVerifier`](Periodic2DHoppingShellHierarchyResultVerifier/index.md) — ActionObject that independently reconstructs the result from a definition and typed hierarchy result.

## Represented verification

The verifier reconstructs source projection, orbit coverage, shell masks, channel
quadratics, bounded minima and nonemptiness, feasible points, common witnesses, fixed
metric, support bounds, distance intervals, hierarchy logic, and withheld diagnostics.
It reports bounded numerical defects and exact Boolean premise outcomes; it does not
return scientific acceptance.

## Invariants and failure behavior

Verification tolerances must be finite and strictly positive. A verification result can
pass only when every decisive premise is checked and every maximum defect lies within
its named tolerance. Missing checks cannot be represented as a pass. Invalid typed
inputs fail rather than being coerced.

## Dependencies and neighboring owners

The verifier may share low-level NumPy/SciPy kernels and periodic conventions with the
producer. It may read the stored center, canonical matrix entries, minimum, and backend
selection from the HSH wrapper's exact-pinned Optimization facade only as claimed values
for comparison. Its
verification logic must not call the shared primitive constructor, `squared_loss`, or
`root_loss`. Instead, it independently validates dimensions, finiteness, symmetry, and
positive curvature and independently reconstructs direct and completed-square values.
It must not call `Periodic2DHoppingShellHierarchyCalculator.execute()` or trust stored
quadratic/certificate scalars. The standalone retained verifier adds wire,
configuration, source-file, and manifest checks without importing producer modules.

## Class navigation

- [`Periodic2DHoppingShellHierarchyVerificationResult`](Periodic2DHoppingShellHierarchyVerificationResult/index.md)
- [`Periodic2DHoppingShellHierarchyResultVerifier`](Periodic2DHoppingShellHierarchyResultVerifier/index.md)

## Prospective code mapping

| Planned path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/verify.py` | Module | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.verify` | Independent typed reconstruction |

## Test mapping

Planned direct and adversarial checks are listed in [testing](../testing.md). No verifier
test currently exists.

## Sphinx mapping

No Sphinx page exists. The intended page is
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Verifier is not implemented | None |
| Numerical verification | Not evaluated | No independent reconstruction run | None |
| Scientific validation | Not evaluated | Verification is not validation | None |
| Uncertainty quantification | Not evaluated | No uncertainty model | None |
| Human acceptance | Not evaluated | Verifier cannot accept a result | None |

## Limitations and deviations

The verifier will remain numerically dependent on some common libraries and conventions.
Its exact interval/outward-rounding backend is unresolved.
