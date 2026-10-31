# Conduction-frozen gauge-sensitivity diagnostic

## Purpose

This execution-free analysis compares the blocked 500- and 1000-iteration
conduction-frozen Wannier90 outputs. It tests whether failure of the strict
Wannierisation convergence gate has a material effect on finite-representation spectra,
conduction-edge diagnostics, and Hamiltonian locality.

No Quantum ESPRESSO or Wannier90 process is invoked. Both inputs remain blocked
diagnostic operators rather than accepted Hamiltonians.

## Declared comparison

The analysis uses:

- the complete native `_hr.dat` representatives and Wigner--Seitz degeneracies;
- the authenticated parent EIG table at the 64 source points;
- the accepted relaxed direct lattice;
- exact source-mesh reconstruction on the ordered `4 x 4 x 4` mesh;
- a deterministic Gamma-origin `41 x 41 x 41` finite-representation comparison grid;
- ordered eigenvalues, comparing candidate indices 3--10 with parent conduction bands
  5--12 at source points;
- a diagnostic conduction-edge union containing points within `0.5 eV` of either
  candidate's dense-grid minimum;
- deterministic local minimization from the 20 lowest dense-grid starts;
- Cartesian finite-difference Hessians at `0.001`, `0.002`, `0.005`, and
  `0.010 inverse angstrom`, with `0.002 inverse angstrom` designated the primary
  curvature diagnostic; and
- pair-symmetric physical-radius tail and finite-compression diagnostics at every
  represented lattice-radius shell.

The curvature-derived mass values are sensitivity diagnostics for the two finite
interpolants. They are not validated silicon effective masses: there is no withheld QE
path, valley-identity acceptance, mesh-convergence result, or accepted Wannier operator.

## Interpretation

Direct matrix subtraction between the two `_hr.dat` operators is forbidden because
their Wannier gauges are not aligned. Comparisons use ordered spectral observations and
within-candidate tail norms. Dense finite-representation evaluation is not independent
first-principles validation.

This is an exploratory diagnostic authorized after both failed localization
occurrences were observed. It has no prospective scientific acceptance threshold and
must not be relabelled as confirmatory evidence.

Run with the maintained ProjectKoios worktree on `PYTHONPATH`:

```text
python run_analysis.py
```

The script writes `gauge-sensitivity-result.json` and authenticates every consumed
artifact by byte count and SHA-256 before analysis.

## Findings

The two blocked operators agree at the 64 construction points to the precision of the
native `_hr.dat` representation: their maximum conduction-eigenvalue difference is
`1.43e-5 eV`, and each reconstructs the frozen parent conduction bands within
`1.22e-5 eV`.

That agreement does not extend between construction points:

- across the `41^3` finite-representation grid, the conduction-band difference has
  `0.240 eV` RMS and `1.433 eV` maximum magnitude;
- in the `0.5 eV` conduction-edge union, the lowest-band difference has `0.252 eV` RMS
  and `1.003 eV` maximum magnitude;
- the optimized diagnostic minima are `6.3104 eV` and `6.4986 eV` in the native energy
  reference and occur at different fractional reciprocal coordinates;
- at the 500-iteration minimum, the 1000-iteration interpolant is `0.6573 eV` higher;
  and
- the primary curvature-derived mass-ratio triplets change from approximately
  `(0.916, 0.223, 0.151)` to `(0.558, 0.308, 0.119)`.

The curvature estimates are internally stable over the tested finite-difference steps,
but they are not validated effective masses. Locality diagnostics also remain
candidate-dependent: for example, truncation after the first nonzero lattice shell has
a dense-grid direct-operator error of `4.02 eV` versus `4.94 eV`.

## Disposition

The iteration sensitivity is consequential for interpolation, valley location,
curvature, and compression. The strict Wannierisation failure cannot be treated as an
innocuous stopping-criterion technicality, and neither diagnostic operator is suitable
for observable-based acceptance. Further iteration-only extension is not supported.
A later candidate should revise the target space or projection strategy, with a narrow
conduction-edge frozen window preferred over freezing all eight conduction bands.

Result SHA-256:
`dbe6198640b4901be4753aa1360866b4f45f8b3667d4f2a06d000f3520c76076`.
