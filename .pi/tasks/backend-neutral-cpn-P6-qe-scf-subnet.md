# P6 — QE semantic adapter and SCF-validation subnet

Status: blocked by accepted P3, P4, and P5

## Objective

Implement separate `QuantumEspressoInputMapper` and `QuantumEspressoResultAdapter` ownership plus the CPN places/transitions for capability verification, authorization, request/result recording, parsing/adaptation to `PeriodicElectronicStructureDataset`, SCF convergence, and accepted periodic parent construction.

Process completion, parsing, convergence, numerical acceptance, and scientific validation remain distinct tokens. Failure and retry require structured failure and explicit retry authorization. Preserves E and remaining F content.

Completion requires implementation, tests, documentation, independent review, parent verification, and human acceptance.