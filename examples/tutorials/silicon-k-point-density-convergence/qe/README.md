# Quantum ESPRESSO k-point-density convergence

**Status:** one exact four-point QE 7.5 attempt completed under resolved protected-execution checkpoint `QE-SILICON-KPOINT-DENSITY-CONVERGENCE-RUN-HC01`.

The tutorial contains four independent `pw.x` SCF points using shifted cubic
Monkhorst--Pack meshes: `2x2x2`, `4x4x4`, `6x6x6`, and `8x8x8`. Every other
represented scientific setting remained fixed. Each point used its own isolated
runtime workspace, streams, snapshots, process record, native-state identity, and
result status.

The result table retains mesh and shift, full-grid count, reciprocal primitive-cell
volume, full-grid point density, observed irreducible count, total energy when
available, process and calculator status, diagnostics, and runtime. No PWTK installation
or invocation is planned.

The exact operational inputs and generated state remain in the external run identified
by the [silicon k-point-density preflight](../../../../docs/computational/silicon-k-point-density-convergence-preflight.md).
They are not maintained here because upstream redistribution terms are unresolved.

The compact calculated observation is retained at
[`expected/qe75-calculated-observation.json`](expected/qe75-calculated-observation.json).
The authoritative total-energy table is:

| Mesh | Full count | Density (Bohr$^3$) | Irreducible count | Total energy (Ry) | QE SCF iterations | Process result |
|---|---:|---:|---:|---:|---:|---|
| `2x2x2` | 8 | 8.708281770947195 | 2 | -15.84001476 | 4 | exit 0; `JOB DONE.` |
| `4x4x4` | 64 | 69.66625416757756 | 10 | -15.85199753 | 4 | exit 0; `JOB DONE.` |
| `6x6x6` | 216 | 235.12360781557425 | 28 | -15.85219772 | 4 | exit 0; `JOB DONE.` |
| `8x8x8` | 512 | 557.3300333406205 | 60 | -15.85220459 | 4 | exit 0; `JOB DONE.` |

Every shift is `(1,1,1)`. QEXSD 25.05.21 reported exit status 0 for every point,
retained the same irreducible counts, and reported Hartree energies agreeing with the
printed Rydberg energies after unit conversion at the retained precision. The
represented total energy is successively lower across this finite ordered sequence;
no tolerance or mesh-selection rule was applied.

Every stderr stream contains the same 139-byte floating-point exception note; it is
retained as an uncharacterized diagnostic rather than classified as harmless or fatal.
Sampled resident-memory observations ranged from 35,600 to 42,368 KiB and may
underestimate instantaneous maxima.

These passing tutorial points do not select a production mesh, establish
Brillouin-zone integration convergence, provide numerical verification, or establish
scientific validation or acceptance.
