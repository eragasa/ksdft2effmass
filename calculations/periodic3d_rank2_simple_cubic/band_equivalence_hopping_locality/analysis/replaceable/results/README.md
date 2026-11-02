# Simple-cubic bounded nominal calculation

Status: **replaceable diagnostics; not retained evidence or scientific validation**.

The canonical JSON outputs are intentionally excluded from source integration. Rerun
[`run_nominal_calculation.py`](../../../run_nominal_calculation.py) to recreate
replaceable artifacts. The bounded request uses an `8 x 8 x 8` construction mesh, shifted
`17 x 17 x 17` evaluation mesh, parent scales `0` and `1`, amplitudes `0`, `pi/8`, and
`pi/4`, complete cubic shells through squared radius `9`, and provisional band thresholds
`1e-3` and `1e-5`.

The historical bounded run reported independent verification passing with maximum stored
identity defect about `6.0e-15`. Its rotated endpoint remained unresolved at the sampled
shell cap, as required by the fail-closed policy. Those values are historical replaceable
development observations; they were not rerun by the context migration and are not
retained execution evidence.

The maintained action stores typed parent/subspace, frame, alignment, Fourier,
Hermiticity, interpolation, truncation, total-error, Parseval, resource, shell, and
first-passing channels without materializing a dense global Hamiltonian. It does not
establish convergence or publication evidence.
