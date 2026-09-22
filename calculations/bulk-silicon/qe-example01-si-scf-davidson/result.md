# QE example01 silicon SCF Davidson smoke test

**Status:** Human-accepted successful tutorial smoke-test reproduction under the claim boundary below.

The one authorized local, single-process Quantum ESPRESSO 7.2 calculation exited with status 0 and emitted `JOB DONE.`. SCF convergence was reported after 6 iterations at a total energy of `-15.84452726 Ry`. The bundled QE example reference reports `-15.84452726 Ry` after 6 iterations; these values agree at the printed precision, without requiring output-byte equality.

The exact observed unresolved runtime warning was: `Note: The following floating-point exceptions are signalling: IEEE_INVALID_FLAG IEEE_DIVIDE_BY_ZERO IEEE_OVERFLOW_FLAG IEEE_UNDERFLOW_FLAG`. It is described as neither harmless nor a calculation failure; diagnosis is deferred unless the flags recur in later calculations. Raw stdout, stderr, and the 544 KiB post-run scratch tree remain outside Git under `/Users/eugene/projects/q-e-qe-7.2/PW/examples/example01/results` and `/Users/eugene/projects/q-e-qe-7.2/tempdir`; their identities and locations are recorded in `execution-provenance.json`.

This result does not establish production convergence, numerical verification, scientific validation, uncertainty quantification, Stage 02 acceptance, or authorization for any successor.

## Accepted claim

> Quantum ESPRESSO 7.2 reproduced the selected official example01 silicon Davidson SCF result using the identified legacy pseudopotential, with retained compact provenance and externally retained native artifacts.

This acceptance does not establish production convergence, pseudopotential suitability for production, numerical verification, scientific validation, uncertainty quantification, Stage 02 acceptance, or transferability beyond the selected tutorial.
