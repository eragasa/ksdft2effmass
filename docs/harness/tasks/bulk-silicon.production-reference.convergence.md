<!-- Generated from SQLite control state; do not edit. -->
# Plane-wave and Brillouin-zone convergence

[Task index](index.md) · [Previous](./bulk-silicon.production-reference.md) · [Next](./bulk-silicon.production-reference.lattice-reference.md)

## Status

`active`: awaiting_human_parameter_selection: Design is active, but pseudopotential-byte verification and every scientific execution remain blocked pending explicit human disposition and later protected-execution authorization.

## Objective

Verify the frozen production pseudopotential identity and compatibility, then design, execute when separately authorized, and analyze staged wavefunction-cutoff and SCF Monkhorst--Pack convergence with a bounded cutoff--mesh coupling cross-check.

## Parent and prerequisites

- Parent: `bulk-silicon.production-reference`
- External prerequisite: `production_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-convergence-design.md
- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation series plus numerical verification; the current phase authorizes design only.
- Preflight owns exact comparison of the supplied local Si pseudopotential bytes and metadata with the frozen PseudoDojo PBE standard-table ONCV scalar-relativistic authority, plus QE and later QE--Wannier90 interface compatibility checks; missing bytes are reported and are not downloaded under the current authority.
- Cutoff execution, when separately authorized, varies E_cut^psi over the accepted ordered sequence with explicit E_cut^rho while holding the provisional structure, pseudopotential, SCF mesh, occupations, diagonalization, mixing, SCF threshold, symmetry, and processor count fixed.
- SCF-mesh execution, when separately authorized, varies only the accepted uniform Monkhorst--Pack dimensions and shifts at the provisionally selected cutoff, followed by a bounded four-corner check at the selected and next-higher cutoff and mesh rather than a full Cartesian grid unless coupling is material.
- Retain total energy per atom, pressure or stress, SCF iteration count, final code-reported convergence estimate, wall time, observable disk use, warnings, and explicitly limited fixed-point band-edge diagnostics; retain identities, tables, residuals, rejected settings, cross-checks, and diagnostic plot data.
- One bounded human acceptance may select provisional cutoff and SCF-mesh settings for later EOS work; a material EOS geometry change can require a bounded recheck.

## Completion criteria

- Frozen authority metadata, local availability, byte-identity verification, executable/interface compatibility, and scientific validation remain separately classified; any identity or compatibility discrepancy stops execution.
- Each primary table changes one controlled variable, uses the accepted observable-specific criteria, and retains the highest-resolution comparison without claiming an infinite-basis limit.
- The accepted provisional cutoff and SCF mesh pass the staged studies, both required one-axis guards, the mixed higher-cutoff/denser-mesh corner, and the observable-specific mixed-difference rule, or unresolved coupling is reported for a separately approved expanded design.
- The human explicitly accepts or rejects the bounded provisional settings before lattice/EOS refinement; production lattice acceptance, production SCF, path, valley, Wannier, and physical-validation work remain outside this Task.

## Exclusions

- The current awaiting_human_parameter_selection phase runs no Quantum ESPRESSO, Wannier90, or other scientific executable and downloads no pseudopotential.
- No final cutoff, mesh, lattice constant, resource campaign, or numerical result is selected before the human responds.
- No production lattice/EOS acceptance, production SCF execution, symmetry-path bands, valley effective masses, Wannierization, plotting implementation, production scientific Python, physical validation, or uncertainty quantification is owned here.
- Successful execution, agreement with the finest retained setting, or a diagnostic plot does not establish scientific validation or agreement with the infinite-basis limit.

## Historical source

No archived source.
