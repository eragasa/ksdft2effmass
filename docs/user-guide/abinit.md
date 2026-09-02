# ABINIT

## Installed but unqualified role

ABINIT is the installed secondary tutorial and prospective conformance backend for
software verification of neutral periodic input/output abstractions and separately
authorized bounded cross-backend numerical verification. Quantum ESPRESSO remains the
initial production backend.

ABINIT 10.8.3 is **installed** and has passed version/build-information probes. It is
**not qualified by a scientific-input software test, numerically verified, or
scientifically validated** in this project. It is not an oracle, a mandatory duplicate
of each QE run, an initial complete Wannier pipeline, or a replacement for experimental
or future all-electron validation.

## First prospective slice

The separately controlled basic1--basic4 tutorial campaign may consider:

- tutorial-derived semilocal SCF parser cases;
- one periodic silicon case;
- mapping from the common neutral periodic specification;
- deterministic ABINIT input serialization;
- output parsing and neutral dataset adaptation;
- capability reporting;
- selected paired QE–ABINIT numerical comparisons.

The installation record does not authorize tutorial input acquisition,
pseudopotential selection, ABINIT test-suite execution, or a scientific calculation.
A production QE run does not require a simultaneous ABINIT run.

See the [ABINIT 10.8.3 installation
record](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/computational/abinit-10.8.3-installation.md),
[cross-backend verification](cross-backend-verification.md), and the [implemented
Architecture v1 snapshot](../architecture/v1/index.md).
