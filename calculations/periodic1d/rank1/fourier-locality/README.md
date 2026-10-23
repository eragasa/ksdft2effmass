# Periodic 1-D rank-one single-band Fourier locality

**Status:** pre-execution calculation design; no implemented model, run, result, or evidence package.

This calculation root is reserved for the model-family-compatible rank-one null control in the periodic multiband program. It will test scalar Fourier interpolation, hopping-support truncation, and spectral consequences using conventions compatible with the rank-two and higher-rank controlled calculations.

For a scalar represented Hamiltonian, phase conjugation is operator-trivial:

\[
U(k)^\dagger H(k)U(k)=H(k), \qquad U(k)\in U(1).
\]

The calculation therefore cannot exhibit gauge-induced represented-operator locality. Its scientific role is to establish the scalar Fourier/locality baseline and the boundary at which nontrivial internal gauge effects first become possible.

## Surfaces

- [`protocol.md`](protocol.md) records the pre-execution compatibility and evidence contract.
- [`simulations/`](simulations/README.md) will own inputs, execution, runs, and experiment verification after those contracts exist.
- [`analysis/`](analysis/README.md) will own verified-input analysis, analysis verification, and plots.
- [`technical-report/`](technical-report/technical_report.tex) contains the current calculation-facing design note.

No stage scripts, input files, generated results, schemas, or run directories are created yet.

## Relationship to Mathieu1D

The retained [`calculations/mathieu1d/`](../../../mathieu1d/) package remains a separate periodic-potential and single-band Fourier-reduction benchmark. It is not renamed, replaced, or treated as the rank-one specialization of this controlled model family.

## Program context

The cross-rank plan and current evidence map are maintained under [`calculations/periodic/multiband/`](../../../periodic/multiband/).
