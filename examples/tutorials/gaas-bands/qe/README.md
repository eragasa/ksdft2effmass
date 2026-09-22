# Quantum ESPRESSO GaAs non-SOC bands

**Status:** one authorized QE 7.5 attempt completed with an admitted SCF result, a calculator-reported bands-stage failure, and unattempted dependent postprocessing.

The proposed smallest Workflow has three sequential calculator stages:

1. `pw.x` SCF for the source-recorded two-atom zinc-blende cell;
2. `pw.x` bands over the source-defined path; and
3. `bands.x` with symmetry classification enabled.

Each stage receives its own workspace, streams, snapshots, process record, and result
status. Native state crosses stage boundaries only through content-identity-checked
copies; no stages share a mutable `outdir`.

The source's GaAs `vc-relax` branch is explicitly deferred because the downstream
source input already fixes `celldm(1)=10.861462` Bohr and no geometry-propagation policy
is authorized. The NSCF branch is explicitly deferred because the source states that
it is needed only for density of states.

Exact source identities, operational-input identities, two official PSlibrary
pseudopotential identities, GPL-2.0-or-later boundary, resource envelope, output plan,
and stopping rules are recorded in the
[GaAs bands preflight](../../../../docs/computational/gaas-bands-preflight.md).
Human response `A` resolved checkpoint `QE-GAAS-BANDS-RUN-HC01` before execution.

The SCF stage returned zero, contained `JOB DONE.`, and reported convergence in 27
iterations. Its admitted native state crossed into the bands stage with exact content
identity. The bands stage generated a 91-point path and then returned 1 after nine
`c_bands` eigenvalue-nonconvergence diagnostics and the QE error `too many bands are
not converged`. It did not emit `JOB DONE.` or a bands QEXSD result. Under the
authorized no-retry policy, `bands.x` was explicitly unattempted because its predecessor
was not admitted. All attempted stages remained within the resource envelopes.

The compact retained record is
[`expected/qe75-calculated-observation.json`](expected/qe75-calculated-observation.json),
SHA-256 `5670b50067599e1725fd7d9872cc0a21065f679cbe025d9aacd03a7224049c21`.
Raw streams, operational inputs, pseudopotential bytes, native state, and calculator
artifacts remain in the external run `qe-7.5-gaas-bands-20260911T004955Z` and are not
committed.

This failure is a calculated tutorial and Workflow observation. It does not
scientifically validate GaAs bands or provide an aligned numerical SOC comparator.
