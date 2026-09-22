# Quantum ESPRESSO nickel collinear spin bands

**Status:** one authorized QE 7.5 four-stage attempt completed; calculated tutorial observation retained.

The proposed Workflow has four sequentially constrained calculator stages:

1. `pw.x` SCF with `nspin=2` and `starting_magnetization(1)=0.7`;
2. `pw.x` bands over the source-defined FCC path;
3. `bands.x` selecting `spin_component=1`; and
4. `bands.x` selecting `spin_component=2`.

The two postprocessing stages are independent siblings after the bands result exists.
Each stage receives its own workspace, streams, snapshots, process record, and result
status. Native state crosses stage boundaries only through identity-checked copies; no
stages share a mutable `outdir`.

The exact source identities, operational input identities, pseudopotential metadata
and license boundary, resource envelope, output plan, and stopping rules are recorded
in the [nickel preflight](../../../../docs/computational/nickel-spin-bands-preflight.md).
Human response `A` resolved checkpoint `QE-NICKEL-SPIN-BANDS-RUN-HC01` before
execution.

All four local one-process stages returned zero, contained `JOB DONE.`, remained within
the authorized envelopes, and used identity-checked native-state copies. The SCF stage
reported convergence in 13 iterations. The bands stage produced 71 path points and 10
bands for each collinear spin component. Both `bands.x` outputs agree with their QEXSD
spin-component eigenvalues to the expected 0.001-eV output rounding.

The compact retained record is
[`expected/qe75-calculated-observation.json`](expected/qe75-calculated-observation.json),
SHA-256 `4ab87fc9b88ca3feafc7ee6f719239e01d50ca03ce7d7048d3fe7cb3ec6e8a5f`.
Raw streams, operational inputs, pseudopotential bytes, native state, and calculator
artifacts remain in the external run
`qe-7.5-nickel-spin-bands-20260908T091550Z` and are not committed.

The retained values are calculated tutorial observations only. They do not
scientifically validate nickel magnetization, exchange splitting, bands, or Fermi
surface behavior.
