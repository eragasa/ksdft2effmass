# QE example01 silicon SCF Davidson smoke test

**Status:** Calculated tutorial smoke-test observation; not production validation or scientific acceptance.

The one authorized local, single-process Quantum ESPRESSO 7.2 calculation exited with status 0 and emitted `JOB DONE.`. SCF convergence was reported after 6 iterations at a total energy of `-15.84452726 Ry`. The bundled QE example reference reports `-15.84452726 Ry` after 6 iterations; these values agree at the printed precision, without requiring output-byte equality.

The output stderr reported signalling IEEE invalid, divide-by-zero, overflow, and underflow flags. No QE error was reported, and the calculation completed. Raw stdout, stderr, and the 544 KiB post-run scratch tree remain outside Git under `/Users/eugene/projects/q-e-qe-7.2/PW/examples/example01/results` and `/Users/eugene/projects/q-e-qe-7.2/tempdir`; their identities and locations are recorded in `execution-provenance.json`.

This result does not establish production convergence, numerical verification, scientific validation, uncertainty quantification, Stage 02 acceptance, or authorization for any successor.
