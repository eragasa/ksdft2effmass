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
locality, and direct-versus-mediated block reduction.

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
construct projections or overlaps, discover files, or execute Wannier90.
`prepare_wannier90.py` remains an in-development campaign adapter and provenance
owner; new software integrations use the public Workflow.

## Deterministic isolated-band replay

The authorized replay retained
`replay/isolated-band-v1/artifacts.json` without replacing `input.json`,
`result.json`, or the historical producer. The replay used only repository-local
Python, NumPy, and SciPy. It reproduced `result.json` byte for byte and retained the
previously missing 64-point rank-one parallel-transport frame, a digest of projectors
reconstructed as $P(k)=u(k)u(k)^\dagger$, all 64 complete hopping coefficients, and
separate truncated and directly fitted coefficients for every declared range.

The replay artifact authenticates the frozen input, retained result, historical
producer, replay producer, frame, reconstructed projector path, and every coefficient
inventory with SHA-256. The typed replay object also retains the exact immutable
campaign definition and result supplied at authentication; adoption rejects later
same-identifier replacements. The dense projector path is intentionally not duplicated
because it is deterministically reconstructed from the retained frame.
`verify_replay.py` authenticates those identities and independently checks frame
orthonormality, projector reconstruction, complete Fourier reconstruction,
truncation, and direct least-squares fitting without rerunning the parent eigensolve.
The replay command refuses an existing output with different bytes and leaves an
identical existing output untouched.

Typed adoption keeps the untruncated Fourier Hamiltonian distinct from the finite
plane-wave parent representation used by the replay. That representation has cutoff
$P=11$, ordered ambient dimension 23, and the retained 64-point reciprocal mesh. The
selected lowest-band space and its retained operator descend from this finite
operator, not directly from the untruncated parent state space. The retained operator
is an exact invariant restriction only within that declared finite Galerkin
representation. A separate discretization record preserves the historical comparison
of its first three bands at $k=-0.5,-0.25,0,0.25,0.5$ against the separately identified
finite $P=15$ reference. The recorded maximum difference,
$2.954581024283698\times10^{-14}E_G$, is one finite-cutoff observation. The retained
sequence is nonmonotone at the $10^{-14}E_G$ scale, so this value must not be treated as
a rigorous bound on error against the untruncated parent, a convergence proof,
validation, or UQ.

Typed scientific adoption accepts `absolute_tolerance: float | None = None`. An
explicit built-in `float` is a common absolute allowance for energy-valued full-mesh
reconstruction and coefficient-route comparisons in dimensionless reciprocal-energy
units. `None` calculates a distinct allowance for each such comparison as binary64
machine epsilon times the comparison dimension times the greater of one and the
applicable reference norm. Reconstruction uses source sample count and maximum
source-matrix Frobenius norm; coefficient comparison uses block count and the L2
aggregation of reference-block Frobenius norms. Reciprocal-coordinate agreement always
uses an independently calculated allowance based on coordinate count and the maximum
of one, reciprocal-period magnitude, and maximum coordinate magnitude. The typed
results retain the resolved allowances and replay comparisons. Frame orthonormality
separately uses a
binary64 roundoff allowance scaled by the 23-dimensional ambient plane-wave basis.
These allowances are software/numerical comparison policy, not rigorous forward-error
bounds, scientific-validation criteria, or uncertainty quantification.

## Reproduction

From `python/`:

```bash
uv run python \
  ../calculations/research-monograph/periodic-1d/run_experiment.py \
  --input ../calculations/research-monograph/periodic-1d/input.json \
  --output ../calculations/research-monograph/periodic-1d/result.json

uv run python \
  ../calculations/research-monograph/periodic-1d/verify_result.py \
  ../calculations/research-monograph/periodic-1d/result.json

uv run python \
  ../calculations/research-monograph/periodic-1d/replay_isolated_band.py \
  --input ../calculations/research-monograph/periodic-1d/input.json \
  --reference-result ../calculations/research-monograph/periodic-1d/result.json \
  --output ../calculations/research-monograph/periodic-1d/replay/isolated-band-v1/artifacts.json

uv run python \
  ../calculations/research-monograph/periodic-1d/verify_replay.py \
  --input ../calculations/research-monograph/periodic-1d/input.json \
  --reference-result ../calculations/research-monograph/periodic-1d/result.json \
  --artifact ../calculations/research-monograph/periodic-1d/replay/isolated-band-v1/artifacts.json

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

The retained-result DataObjects encapsulate immutable version-one models and delegate
to separate correlation and verification Actionizers. The verifier Actionizers
independently reconstruct the channels identified in
`protocol.md`. Transported-frame, localization-density, and several composite-gauge
source arrays were not retained in the historical result. The authorized isolated-band
replay sidecar now retains its rank-one frame and effective-model coefficient routes;
the composite frame/gauge omissions remain. Accordingly, composite overlap, Wilson,
localization, alignment, rough-gauge, and withheld diagnostics remain calculated producer values
with software and structural checks rather than independently reconstructed numerical
evidence. The Wannier90 integration DataObject can correlate retained controls without
native artifacts; native Wilson verification additionally requires complete explicit
artifact groups. Neither Actionizer reruns Wannier90.

Passing checks establish bounded numerical verification only for the reconstructable
channels of the frozen cosine model. They do not establish semiconductor validation,
uncertainty quantification, production localization, or transferability to silicon.
The reduced model approximates a represented isolated-band dispersion, not the scalar
potential.
