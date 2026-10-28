# Mathieu1D direct finite-reduction protocol

## Scientific question

For the finite scalar Mathieu Hamiltonian

\[
H(k)=-\frac{d^2}{dx^2}+0.5\cos x,
\]

how accurately do declared plane-wave and periodic finite-difference representations
resolve the sampled parent spectrum, and how does a finite reciprocal inventory support
complete and range-truncated scalar hopping representations?

This protocol concerns finite represented calculations only. It does not establish a
continuum isolation certificate, uncertainty quantification, a universally adequate
hopping range, material validity, publication acceptance, evidence sealing, or release.

## Mathematical conventions

- period: \(a=2\pi\);
- reciprocal vector: \(G=1\);
- recoil energy: \(E_G=1\);
- fixed parent-model energy zero;
- reduced momentum: \(k/G\) on one centered reciprocal period;
- selected band: zero-based band 0;
- forward transform:

  \[
  t_R=N^{-1}\sum_j e^{-2\pi i R k_j/G}E(k_j);
  \]

- inverse interpolation:

  \[
  E(k)=\sum_R e^{+2\pi i R k/G}t_R.
  \]

The complete training inventory is a 64-point centered half-open mesh. The disjoint
257-point evaluation mesh is \(-1/2+(i+1/65)/257\). Evaluation coordinates cannot alter
coefficients, fitting weights, hopping ranges, or tolerances.

## Finite controls

- plane-wave cutoffs: `3, 5, 7, 9, 11`;
- finite plane-wave reference cutoff: `15`;
- production plane-wave cutoff: `11`;
- finite-difference points: `31, 63, 127, 255`;
- parent reduced momenta: `-1/2, -1/4, 0, 1/4, 1/2`;
- compared parent bands: lowest three ordered bands;
- hopping ranges: `0, 1, 2, 3, 4, 6, 8`;
- fitting weights: 64 positive unit weights;
- coordinate and Fourier-duality tolerance: `1e-14`;
- reconstruction, Hermiticity, Parseval, and imaginary tolerances: `1e-12`.

The sampled training and evaluation external gaps are diagnostics. Positive values on
these inventories are not a continuum spectral certificate.

## Direct lifecycle

1. `run_01_calculation.py` constructs typed configuration and result bytes through
   `Mathieu1dAnalyzer` and canonical numerical owners.
2. `run_02_verification.py` admits the exact result bytes, correlates the embedded
   configuration, independently reconstructs the finite formulas, and emits typed
   verification and visualization data.
3. `run_03_render.py` repeats independent admission, compares complete verification and
   projection bytes, renders the closed figure inventory, and copies the buildable
   technical-report snapshot.

The scripts refuse to overwrite a completed or incomplete stage. They do not import or
read predecessor code, schemas, results, figures, or run directories.

## Retained direct execution

`executions/direct-finite-reduction-n64/` is the only live execution. It is a local
deterministic Python calculation with recorded dirty-worktree qualification and remains
explicitly unsealed. Its result and verification SHA-256 values are:

- result: `83d25e824a0aedf085e77e86a998c02a17d4a51c320375b0bfb395986dae3fe6`;
- verification: `61553c16636efc39452706006dc480b827c2f2d04f3e318e02e3c2eec4f24664`.

Predecessor run artifacts are absent from the live tree.
