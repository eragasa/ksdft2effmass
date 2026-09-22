# Nickel collinear spin bands

**Status:** one authorized Quantum ESPRESSO 7.5 Workflow attempt completed with a retained calculated tutorial observation; ABINIT realization not implemented.

## Learning objective

This tutorial probes how a generic calculator and Workflow interface must represent a
collinear spin-polarized metal calculation followed by a band-path calculation and two
spin-selective postprocessing stages.

The Quantum ESPRESSO realization belongs to
`quantumespresso.simulations.pranab_das.spin-bands-nickel`. It must preserve the distinction
between the collinear spin model (`nspin=2`), an initial magnetization seed,
calculator-reported final magnetization, spin-labeled eigenvalue channels, and the two
`bands.x` selections `spin_component=1` and `spin_component=2`.

Nickel is a learning-only system outside the project's supported material scope. Any
calculated result is software-workflow evidence, not a validated nickel band structure
or magnetic prediction.

## Backends

- [`qe/`](qe/) — exact QE 7.5 four-stage attempt complete; calculated tutorial observation retained.
- [`abinit/`](abinit/) — correspondence placeholder only; no implementation or execution is authorized.
