# ABINIT

## Deferred role

ABINIT is the planned secondary conformance backend for software verification of
the neutral periodic input/output abstractions and bounded cross-backend
numerical verification. Quantum ESPRESSO remains the initial production
backend.

ABINIT is **planned**, **deferred**, **not installed**, **not software
verified**, **not numerically verified**, and **not scientifically validated**
in this project. It is not an oracle, a mandatory duplicate of each QE run, an
initial complete Wannier pipeline, or a replacement for experimental or future
all-electron validation.

## First prospective slice

After the first accepted end-to-end dopant result, a separately approved task
may consider:

- tutorial-derived semilocal SCF parser cases;
- one periodic silicon case;
- mapping from the common neutral periodic specification;
- deterministic ABINIT input serialization;
- output parsing and neutral dataset adaptation;
- capability reporting;
- selected paired QE–ABINIT numerical comparisons.

No ABINIT dependency, production module, fixture, test, or execution is
authorized by the current architecture correction. A production QE run does not
require a simultaneous ABINIT run.

See [cross-backend verification](cross-backend-verification.md) and the
[periodic integration architecture](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/architecture/periodic-electronic-structure-integration.md).
