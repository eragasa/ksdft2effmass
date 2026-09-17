# Synthetic blind-alignment protocol

## Status and scope

This is a deterministic **synthetic test-data** experiment. It verifies a declared inverse-alignment and subtraction procedure on represented operators inherited from the accepted one-dimensional defect benchmark. It is not a silicon calculation, DFT result, production Wannierization, scientific validation, transferability study, uncertainty quantification, or public API.

The known-map benchmark remains separate. Here the inference action receives only declared observations; the authored translation, orbital map, spin-frame map, scalar energy shift, and planted defect are withheld until post hoc evaluation.

## Frozen sources

`input.json` records SHA-256 identities for:

- `calculations/research-monograph/impurity-defect-1d/input.json`;
- `calculations/research-monograph/impurity-defect-1d/result.json`; and
- the parent periodic composite result transitively identified by the defect input.

The baseline loader verifies these identities before constructing observations. The inherited pristine represented operator is the 16-cell, two-orbital composite parent folded at the declared reduced supercell momentum. The spinor case uses its explicit spin lift. The planted onsite orbital and spin-mixing defects are reconstructed from the accepted compact blocks rather than imported from executable code.

## Information visible to inference

For each nominal case the alignment action receives:

1. the reference and candidate represented Hamiltonians;
2. an authored anchor cross-covariance from candidate coordinates to reference coordinates;
3. retained-subspace overlap singular information;
4. a declared exterior energy-anchor projector;
5. reference and candidate spin counts; and
6. whether partial alignment is admissible.

It does **not** receive the authored coordinate map, scalar energy shift, planted impurity operator, or any oracle error metric.

The frozen information contract states that the full anchor cross-covariance is available as an authored matrix; site-anchor and orbital labels are available only on its ordered reference rows; reference spin-frame labels are available while the candidate rotation remains hidden; and the exterior energy projector is available while the scalar shift remains hidden. Candidate site, orbital, and spin correspondences must therefore be inferred through the cross-covariance rather than supplied as a map.

The anchor record is an authored synthetic observable. It is not claimed to be an overlap computed by an independent electronic-structure route.

## Inference rule

Let $C$ be the anchor cross-covariance and let

$$
C=L\Sigma R^\dagger
$$

be its singular-value decomposition. Singular values larger than $10^{-10}$ define the identifiable anchor sector. The inferred partial isometry is

$$
\widehat U=L_rR_r^\dagger,
$$

with reference projector $P=\widehat U\widehat U^\dagger$. Full alignment requires rank equal to the represented dimension. Partial alignment is permitted only in the declared gauge-equivalent case.

Inference stops if:

- reference and candidate represented ranks differ;
- spin counts differ;
- the largest retained-subspace principal angle exceeds $0.35$ rad;
- no anchor direction survives the rank tolerance;
- the surviving anchor condition number exceeds $10^6$;
- rank is deficient when partial alignment is not declared; or
- the exterior energy-anchor rank is less than four.

The exterior rank is evaluated from singular values above the same $10^{-10}$ numerical-rank tolerance, rather than by comparing a floating-point trace directly with the integer threshold. The trace remains the averaging weight in the shift estimator.

For an admissible observation, the scalar energy shift is estimated only from the aligned exterior sector. With aligned candidate operator $\widehat H_d=\widehat U H_d\widehat U^\dagger$ and pristine operator $H_0$, the extracted represented operator is

$$
\widehat V=P\widehat H_dP-\widehat\delta P-PH_0P.
$$

## Success and equivalence rules

A full-rank map is compared with the authored map after quotienting one global complex phase. This phase is the sole full-rank gauge equivalence declared here.

For rank-deficient anchors, only $P\widehat U$ and $P\widehat V P$ are identified. The complement is explicitly non-identifiable. Two unitary completions are therefore compared in both the full represented space and the compressed identified sector. A large full-space disagreement with numerical-noise compressed disagreement is the intended degeneracy control, not a failed fit.

The following errors remain separate:

- phase-quotiented alignment-map Frobenius defect;
- scalar energy-shift error;
- represented extraction Frobenius defect;
- onsite model-class residual;
- active-sector eigenvalue defect; and
- lowest-active-state fidelity.

No one metric is substituted for another.

## Controls

The frozen suite contains:

- exact spinless and spinor full-rank cases;
- a well-conditioned unitary anchor-noise sweep from $0$ to $10^{-2}$ rad;
- a 16-of-32-dimensional undercomplete, gauge-equivalent control; and
- structured stops for ill-conditioning, incompatible retained subspaces, unequal rank, incompatible spin space, and an insufficient exterior energy anchor.

The noise sweep is a controlled sensitivity experiment, not UQ. The stopping thresholds are protocol settings for these synthetic controls and are not proposed material acceptance thresholds.

## Debugging the stopping boundaries

The original five negative controls remain unchanged. Frozen neighboring probes diagnose what information is missing and which explicit declaration makes a comparison admissible:

1. A fixed additive anchor perturbation of spectral norm $10^{-10}$ is applied while the smallest singular value is decreased. Map and extraction errors grow before the condition number crosses $10^6$; cases above that limit retain only the structured stop.
2. One retained-subspace principal direction is swept through $0.35$ rad. The $0.34$ rad case remains admissible and the $0.36$ rad case stops.
3. The unequal-rank case remains invalid as a full comparison. A separate declared $32\times31$ rectangular partial isometry identifies a 31-dimensional common sector. Because its zero target is completely degenerate, an individual lowest-state fidelity is undefined; the full lowest-eigenspace projector is compared instead.
4. The spin mismatch remains invalid directly. An explicit spin lift constructs a common spinor space. The retained spin-mixing defect has a nonzero spin-independent restriction residual, so lossless restriction to the spinless space is unavailable.
5. Exterior energy-anchor ranks zero through three stop, while ranks four and above identify the shift. Four is a protocol robustness requirement for this synthetic suite, not a universal mathematical threshold.

These probes diagnose the stopping rules; they do not silently coerce incompatible observations, weaken the frozen thresholds, or claim material tolerances.

## Independent verification

`verify_result.py` does not import `run_experiment.py`. It independently:

- verifies source and script identities;
- reconstructs the pristine and planted represented operators;
- reconstructs the hidden coordinate maps solely for post hoc checking;
- implements its own SVD/polar inference and energy-reference estimate;
- recalculates all retained nominal metrics and matrix digests;
- reconstructs the gauge-completion contrast;
- verifies every structured stop; and
- checks the declared information boundary and limitations.

Agreement establishes software and numerical verification only under this synthetic protocol.

## Reproduction

From `python/`:

```bash
uv run python ../calculations/research-monograph/impurity-defect-1d-blind-alignment/run_experiment.py \
  --input ../calculations/research-monograph/impurity-defect-1d-blind-alignment/input.json \
  --output ../calculations/research-monograph/impurity-defect-1d-blind-alignment/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-blind-alignment/verify_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-blind-alignment/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-blind-alignment/plot_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-blind-alignment/result.json \
  --output ../calculations/research-monograph/impurity-defect-1d-blind-alignment/summary.png \
  --diagnostics-output ../calculations/research-monograph/impurity-defect-1d-blind-alignment/diagnostics.png
```

Run `sha256sum -c SHA256SUMS` from the calculation directory after the catalog has been generated.
