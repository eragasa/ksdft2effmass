# One-dimensional periodic reduction exercise

## Current status

This directory contains calculated illustrative **isolated-band and direct
composite-band slices** of Appendix G. The isolated-band study covers
independent plane-wave and finite-difference parent refinement, exact structural
and Mathieu checks, direct parallel-transport localization, hopping
reconstruction, finite-range truncation, withheld-mesh tests, and
direct-versus-mediated route agreement. Its adversarial suite sweeps potential
amplitude, reciprocal mesh density, the first eight bands, modified potential
shapes, random input gauges, and altered direct-fit objectives.

The separate composite mini-paper treats bands 0--1 and 2--3 using polar
transport, overlap singular values, Wilson-loop phases, controlled $U(2)$ gauge
attacks, explicit alignment, matrix-valued hoppings, smooth-versus-rough gauge
locality, and direct-versus-mediated block reduction. New in-memory calculations of
these demonstrated channels use the public
`Periodic1DCompositeBandCalculationWorkflow`. Its typed result retains parent fibers,
source and transported frame provenance, gauge attacks, projectors, Wilson spectra,
complete smooth/rough block hoppings, and separate truncation, training, withheld,
Hermiticity, and direct-route diagnostics. It reads no retained result and performs no
filesystem discovery or external execution.

The independent Wannier90 comparison followed a retained sequence of bounded
attempts. `search_shells = 130` repaired the initial anisotropic-mesh
preprocessing failure, but 500-iteration runs and a low-pair 5000-iteration
extension remained nonconverged. Read-only diagnosis identified Wannier90's
documented preconditioner as the smallest objective-preserving remedy. Fresh
runs adding only `precond = true` then satisfied the unchanged $10^{-12}$ spread
criterion at iterations 69 and 4176. The failed attempts, diagnosis, converged
execution, and verified result remain separate records. The converged result is
specific to this synthetic interface and is not semiconductor validation or
transferability evidence.

For new execution-independent interface preparation, use the public
`Wannier90InterfacePreparationWorkflow` under
`ksdft2effmass.integration.wannier90`. It deterministically writes the demonstrated
`.win`, `.eig`, `.amn`, and `.mmn` subset from typed caller-supplied records, compares
`.win` and parsed `.nnkp` reciprocal points under an explicit tolerance, and requires
exact ordered `.mmn` header agreement with parsed `.nnkp` data. It does not
construct projections or overlaps, discover files, or execute Wannier90. The
historical `prepare_wannier90.py` remains frozen as a provenance owner and is
deprecated for new execution.

## Historical reproduction record

The commands below document the authenticated historical adapters and retained result
provenance. Those scripts are frozen and deprecated for new execution as stated in
`DEPRECATION.md`; the commands are not current execution authorization. New software
integration must use the public package Workflows.

From `python/`:

```bash
uv run python \
  ../calculations/research-monograph/periodic-1d/run_experiment.py \
  --input ../calculations/research-monograph/periodic-1d/input.json \
  --output ../calculations/research-monograph/periodic-1d/result.json

uv run python \
  ../calculations/research-monograph/periodic-1d/verify_result.py \
  ../calculations/research-monograph/periodic-1d/result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-1d/plot_result.py \
  ../calculations/research-monograph/periodic-1d/result.json \
  --output ../calculations/research-monograph/periodic-1d/summary.png

uv run python \
  ../calculations/research-monograph/periodic-1d/run_stress.py \
  --input ../calculations/research-monograph/periodic-1d/stress-input.json \
  --output ../calculations/research-monograph/periodic-1d/stress-result.json

uv run python \
  ../calculations/research-monograph/periodic-1d/verify_stress.py \
  ../calculations/research-monograph/periodic-1d/stress-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-1d/plot_stress.py \
  ../calculations/research-monograph/periodic-1d/stress-result.json \
  --output ../calculations/research-monograph/periodic-1d/stress-summary.png

uv run python \
  ../calculations/research-monograph/periodic-1d/run_composite.py \
  --input ../calculations/research-monograph/periodic-1d/composite-input.json \
  --output ../calculations/research-monograph/periodic-1d/composite-result.json

uv run python \
  ../calculations/research-monograph/periodic-1d/verify_composite.py \
  ../calculations/research-monograph/periodic-1d/composite-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-1d/plot_composite.py \
  ../calculations/research-monograph/periodic-1d/composite-result.json \
  --output ../calculations/research-monograph/periodic-1d/composite-summary.png

uv run python \
  ../calculations/research-monograph/periodic-1d/extract_wannier90.py \
  --input ../calculations/research-monograph/periodic-1d/composite-input.json \
  --workdir "${WANNIER90_RUN_ROOT}" \
  --output ../calculations/research-monograph/periodic-1d/wannier90-result.json

uv run python \
  ../calculations/research-monograph/periodic-1d/verify_wannier90.py \
  ../calculations/research-monograph/periodic-1d/wannier90-result.json

uv run python \
  ../calculations/research-monograph/periodic-1d/verify_wannier90.py \
  ../calculations/research-monograph/periodic-1d/wannier90-preconditioned-result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-1d/plot_wannier90.py \
  ../calculations/research-monograph/periodic-1d/wannier90-preconditioned-result.json \
  --composite ../calculations/research-monograph/periodic-1d/composite-result.json \
  --output ../calculations/research-monograph/periodic-1d/wannier90-preconditioned-summary.png
```

The largest finite-difference matrix is $255\times255$; the nominal and stress
experiments each execute locally in well under a minute on a laptop. `protocol.md` defines the state
spaces, controls, and claim boundary. `report.md` is the self-contained
provisional isolated-band mini-paper, including abstract, methods, verification,
results, discussion, limitations, and reproduction. `composite-report.md` is
the corresponding direct composite-band mini-paper. `SHA256SUMS` identifies the
retained files.

## Evidence boundary

Passing checks establish numerical verification for the frozen cosine model.
They do not establish semiconductor validation, uncertainty quantification,
production localization, or transferability to silicon. The reduced model
approximates a represented isolated-band dispersion, not the scalar potential.
