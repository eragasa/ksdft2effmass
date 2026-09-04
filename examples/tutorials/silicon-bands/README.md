# Silicon SCF-to-bands tutorial

This concept pairs Quantum ESPRESSO and ABINIT realizations of the same
computational objective:

1. construct a self-consistent density for two-atom diamond silicon;
2. continue from that native density state;
3. evaluate eight fixed-density Kohn-Sham bands on an
   L–$\Gamma$–X–$\Gamma$ path topology; and
4. expose the represented band spectrum for scientific postprocessing.

The pairing establishes workflow correspondence, not numerical equivalence.
The backends retain their native pseudopotentials, lattice constants, cutoffs,
k-point discretizations, coordinate conventions, and convergence semantics.
Energies and eigenvalues must not be compared without a separately specified
alignment and verification procedure.

## Calculated tutorial observations

One exact, single-shot execution was authorized and completed on 2026-09-02:

| Backend | Native realization | Result |
|---|---|---|
| Quantum ESPRESSO 7.5 | `pw.x` SCF → `pw.x` bands → `bands.x` | all three exits 0; SCF convergence reported; 72 points × 8 bands |
| ABINIT 10.8.3 | one `abinit` process, SCF dataset 1 → fixed-density dataset 2 | exit 0; dataset-1 energy convergence reported; 39 points × 8 bands |

The compact records are:

- [paired workflow observation](expected/paired-workflow-observation.json);
- [Quantum ESPRESSO observation](qe/expected/qe75-calculated-observation.json); and
- [ABINIT observation](abinit/expected/abinit1083-calculated-observation.json).

These are calculated tutorial observations, not production results, numerical
verification, scientific validation, or acceptance. Native QEXSD, NetCDF,
density, wavefunction, and complete band files remain outside Git.

## Architectural observation

The logical SCF-to-bands dependency required two `pw.x` processes in Quantum
ESPRESSO but two datasets inside one ABINIT process. Quantum ESPRESSO then
required an additional `bands.x` postprocessor, whereas the ABINIT result was
read directly by project postprocessing. A generic workflow therefore cannot
identify a scientific stage with an operating-system process. Native
continuation state and optional backend-specific postprocessing must remain
explicit.

## Internal CPN architecture probe

The deterministic internal probe reads the two compact observations, adapts each
backend into separate logical SCF and fixed-density-bands values, replays both
through the same effect-free CPN, and applies an explicit fail-closed comparison
specification:

```bash
PYTHONPATH=python/src python3 \
  examples/tutorials/silicon-bands/scripts/compare_retained_observations.py
```

The expected report is
[`expected/internal-cpn-architecture-probe.json`](expected/internal-cpn-architecture-probe.json).
Both logical workflows replay successfully. The ABINIT values preserve one shared
native process-observation identity while the QE values preserve distinct SCF and
bands process-observation identities. Workflow shape is compatible, but numerical
comparison is rejected because the required grid, settings, pseudopotential, energy
alignment, and complete committed spectra are unavailable or incompatible.

The probe invokes no scientific executable, reads no external native run state, and
provides software-orchestration evidence only. Its private Python contracts remain
revisable under the
[DFT simulation CPN service decision](../../../docs/architecture/v2/ksdft2effmass/workflows/dft-simulation-cpn-service-decision.md).

See
[the execution preflight](../../../docs/computational/paired-silicon-scf-bands-preflight.md)
for exact settings, identities, authorization bounds, and retained-output
policy.
