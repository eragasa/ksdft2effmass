# Accepted-S1 parent DFT band path

## Purpose

This authorized calculation supplies the conventional parent-DFT band diagram requested
for the `Ragasa2026icmsep` working manuscript. It does not connect the separate 408-point
valley/Hessian inventory as if that inventory were a band path.

## Calculation

Exactly one local Quantum ESPRESSO 7.5 `pw.x` invocation was executed with no retry:

- accepted relaxed structure: `Si.PrimitiveUnitCell.RightHanded.RelaxedS1`;
- fixed density from an isolated copy of the authenticated accepted-S1 K10 parent SCF;
- SSSP 1.3.0 PBE-efficiency silicon ultrasoft pseudopotential;
- wavefunction/density cutoffs: 42/336 Ry;
- 20 Kohn--Sham bands;
- `nosym=.true.` and `noinv=.true.` to preserve the declared order;
- 241 unique ordered points, with 81 points per segment including endpoints, on
  `L-Gamma-X-Gamma`; and
- one local process and one OpenMP thread.

The invocation completed with return code zero and `JOB DONE` in 46.41 seconds wall
time. QE emitted the same four IEEE flag classes retained for earlier successful parent
occurrences. No unconverged-eigenvalue message or explicit calculator error was found.

`disk_io='none'` suppressed path-wavefunction output and left the copied SCF QEXSD
unchanged. Therefore the band eigenvalues are parsed from retained `pw.out`; the copied
QEXSD is labeled as inherited SCF provenance and is not used as a band result. Printed
band energies have QE's retained four-decimal-eV precision.

## Diagram and path diagnostics

The figure displays the lowest 12 of the 20 computed parent bands and overlays the ten
bands of the authenticated full `C6-B20-W21` Wannier source. Both use their native common
energy reference; the plot subtracts the parent path VBM and applies no fitted source
shift.

On this sampled path:

- parent path gap: `0.6114 eV`;
- source path gap: `0.6904587348708153 eV`.

These are sampled-path diagnostics, not new global-extremum estimates. The previously
retained optimized values remain the owners of the parent and source indirect gaps.

## Claim boundary

This is a scalar-relativistic PBE Kohn--Sham band path. It is not an experimental or
quasiparticle spectrum, a convergence study, an independent reconstruction, or evidence
that the Wannier source is adequate for silicon. The overlay visualizes the already
reported source/parent discrepancy without defining a common DFT/Wannier operator
subtraction.

## Retained files

- `authorization.json` and `preflight.json` — execution authority and frozen settings;
- `input/path.json` and `input/pw.in` — ordered path and exact calculator input;
- `run_campaign.py` — single-invocation producer;
- `occurrence/` — input, streams, execution record, and inherited SCF QEXSD;
- `analyze_and_plot.py` — no-calculator parser and renderer;
- `result/band-data.json` — plotted coordinates, parent spectra, source spectra, and
  path-only diagnostics;
- `figures/parent-dft-band-diagram.pdf` and `.png` — retained diagram.

Large mutable calculator state remains under the authenticated external occurrence root
recorded in `result/external-root.json`.
