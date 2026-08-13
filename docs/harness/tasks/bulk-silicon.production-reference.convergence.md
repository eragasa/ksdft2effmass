<!-- Generated from SQLite control state; do not edit. -->
# Plane-wave and Brillouin-zone convergence

[Task index](index.md) · [Previous](./bulk-silicon.production-reference.md) · [Next](./bulk-silicon.production-reference.lattice-reference.md)

## Status

`deferred`: awaiting_scientific_harness_reimplementation: Direct bootstrap execution completed through 18 pw.x invocations governed by the development harness. The retained observations are bootstrap scientific-harness development evidence, not a canonical scientific CampaignRun or accepted production convergence evidence. Scientific interpretation is not accepted, canonical scientific-harness execution is deferred, and additional execution is unauthorized.

## Objective

Verify the frozen production pseudopotential identity and compatibility, then design, execute when separately authorized, and analyze staged wavefunction-cutoff and SCF Monkhorst--Pack convergence with a bounded cutoff--mesh coupling cross-check.

## Parent and prerequisites

- Parent: `bulk-silicon.production-reference`
- External prerequisite: `production_execution_authorization`

## Authority references

- calculations/bulk-silicon/production-convergence-preflight/bootstrap-execution-disposition.json
- docs/computational/bulk-silicon-production-convergence-design.md
- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation series plus numerical verification; the current phase authorizes design only.
- Preflight owns controlled acquisition from only the frozen exact PseudoDojo URL, atomic publication to the portable user_opt installation without repository redistribution, exact compressed and decompressed byte and metadata verification, license/citation recording, selected pw.x identity inspection without invocation, and later QE--Wannier90 interface compatibility checks. Acquisition and static verification are complete; pw.x readability remains an execution-time check and pw2wannier90.x remains later scope.
- Cutoff execution, when separately authorized, varies E_cut^psi over the finite conventional candidate sequence 30, 36, 42, 48, 54, and 60 Ry with E_cut^rho=4 E_cut^psi while holding the provisional structure, exact pseudopotential, shifted 8^3 SCF mesh, occupations, diagonalization, mixing, SCF threshold, symmetry, and one-process execution fixed.
- SCF-mesh execution, when separately authorized, varies the systematically refined but non-nested shifted-even Monkhorst--Pack candidates 6^3, 8^3, 10^3, and 12^3 at the provisional 48 Ry PseudoDojo high-hint setting, with the 48 Ry/8^3 case deterministically reused from the cutoff scan. Later four-corner inputs remain parameterized until E_*, K_*, E_+, and K_+ are known.
- Retain total energy per atom, pressure or stress, SCF iteration count, final code-reported convergence estimate, wall time, observable disk use, warnings, and explicitly limited fixed-point band-edge diagnostics; retain identities, tables, residuals, rejected settings, cross-checks, and diagnostic plot data.
- One bounded human acceptance may select provisional cutoff and SCF-mesh settings for later EOS work; a material EOS geometry change can require a bounded recheck.
- Before any such scientific disposition, the canonical scientific campaign must be reimplemented and separately authorized through the deterministic scientific harness; the retained direct bootstrap execution is fixture evidence only.

## Completion criteria

- Frozen authority metadata, local availability, byte-identity verification, executable identity, runtime UPF readability, later interface compatibility, numerical convergence, and scientific validation remain separately classified. Static byte/metadata and executable identity checks pass; any later readability, identity, or compatibility discrepancy stops execution.
- Each primary table changes one controlled variable, applies the revised 0.05 kbar stress criterion and the 1 meV criterion only to fixed-point energies and gaps, and retains finite-setting comparisons without claiming an infinite-basis limit or effective-mass convergence.
- The accepted provisional cutoff and SCF mesh pass the staged studies, both required one-axis guards, the mixed higher-cutoff/denser-mesh corner, and the observable-specific mixed-difference rule, or unresolved coupling is reported for a separately approved expanded design.
- The human explicitly accepts or rejects the bounded provisional settings before lattice/EOS refinement; production lattice acceptance, production SCF, path, valley, Wannier, and physical-validation work remain outside this Task.

## Exclusions

- The completed protected-execution authorization covered exactly the committed direct-bootstrap 9-SCF and 9-NSCF execution. No retry, input revision, Wannier90 execution, four-corner follow-on, or other scientific executable is authorized; pseudopotential commit and redistribution remain prohibited.
- No canonical scientific CampaignRun exists. The direct bootstrap observations do not establish deterministic scientific-harness execution, production convergence, numerical-verification acceptance, scientific-validation acceptance, or a ScientificDisposition.
- No final cutoff, mesh, or lattice constant is selected. Canonical scientific-harness execution and scientific interpretation remain deferred pending reimplementation and separate authorization.
- No production lattice/EOS acceptance, production SCF execution, symmetry-path bands, valley effective masses, Wannierization, plotting implementation, production scientific Python, physical validation, or uncertainty quantification is owned here.
- Successful execution, agreement with the finest retained setting, or a diagnostic plot does not establish scientific validation or agreement with the infinite-basis limit.

## Historical source

No archived source.
