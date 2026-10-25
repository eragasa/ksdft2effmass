# Simulations

This directory is the owner for future bulk-silicon simulation inputs, authorized
execution records, compact outputs, and experiment verification. It currently contains
no runnable production stage and no production result.

## Existing predecessor

The completed direct bootstrap remains at
[`calculations/bulk-silicon/production-convergence-preflight/`](../../../bulk-silicon/production-convergence-preflight/).
It contains nine SCF and nine linked diagnostic NSCF executions. Its inputs, compact
records, checksums, external-run identities, and embedded repository paths remain under
that historical owner.

## Admission rule for a successor

A simulation version may be added here only after it has:

1. an accepted physical branch and lattice source;
2. exact executable and pseudopotential identities;
3. frozen inputs, numerical settings, warning policy, and stop policy;
4. a declared external workspace and compact-artifact policy;
5. expected runtime and resource bounds;
6. explicit authorization for the bounded QE or Wannier90 execution; and
7. an independent experiment-verification contract.

No empty stage scripts are provided. A stage is created only when its input, output,
failure, provenance, and verification contracts exist.

## Intended sequence

The expected simulation families are parent-setting qualification, conduction-valley
characterization, Wannier construction/qualification, and prospectively declared
sensitivity controls. They remain distinct versions; a later stage may consume only a
verified predecessor and must not overwrite it.
