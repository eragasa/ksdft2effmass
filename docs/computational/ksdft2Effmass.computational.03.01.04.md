back_to: [[ksdft2Effmass.computational.03]]
# Task 03.01.04: Run the Wannier-compatible uniform-grid NSCF child and QE–Wannier bridge

## Status

`Blocked`

## Objective

Produce the immutable native and bridge artifact set required by the approved Wannier-interface specification without assigning the unknown uniform grid to G02.

## Prerequisites

- accepted [[ksdft2Effmass.computational.03.01.03|03.01.03]] Wannier-interface specification;
- accepted G02 SCF parent manifest;
- approved production-environment checkpoint recording the machine or cluster, QE/Wannier executable identities, exact pseudopotential artifact, resources, working and artifact roots, runtime estimate, retained outputs, and data-transfer policy.

Every prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- accepted G02 SCF parent density and manifest;
- approved retained bands, projections, outer/inner windows, and uniform grid;
- exact QE and Wannier90 interface inputs;
- typed artifact identities and locations resolved for the authorized environment.

## Procedure

1. Construct the uniform-grid NSCF child specification from the approved Stage 03 interface specification.
2. Record explicit lineage to the accepted G02 SCF parent manifest.
3. Execute the authorized QE NSCF calculation without changing the accepted scientific or numerical choices.
4. Run `wannier90.x -pp` to produce `.nnkp` and `pw2wannier90.x` to produce `.amn`, `.mmn`, `.eig`, and any separately approved optional interface files.
5. Seal, checksum, classify, and retain the required native and bridge artifacts. For every wavefunction-like artifact, record its representation (for example auxiliary pseudo or PAW-reconstructed); for projector, augmentation, Wannier-overlap, and Wannier-projection products, record semantic role and availability separately. Record execution completion and interface consistency separately from scientific acceptance.

## Outputs

Primary output:

```text
Wannier interface artifact set
```

It contains typed immutable references to the uniform-grid QE wavefunctions and `.save` data, `.nnkp`, `.amn`, `.mmn`, `.eig`, and approved optional bridge artifacts. It does not embed those large payloads in Git or the compact `PeriodicElectronicStructureDataset`.

## Acceptance Criteria

- the child manifest references the accepted G02 SCF parent manifest;
- k-point, band, spin, pseudopotential, prefix/outdir, and neighbor-list compatibility checks pass;
- every required artifact is sealed and checksum verified;
- every wavefunction-like artifact declares its representation, and every projector/augmentation/Wannier matrix product declares its semantic role and availability;
- process completion, bridge consistency, and later Wannier/scientific validation remain distinct states;
- failed, interrupted, partial, or mismatched outputs are not accepted downstream;
- no unapproved resource, pseudopotential, storage, or transfer choice is introduced.

## Unlocks

- [[ksdft2Effmass.computational.03.02.01|03.02.01]]

## Failure Conditions

The task fails if authorization is absent, parent lineage is missing, native or bridge artifacts are incomplete or mismatched, a checksum fails, or an unresolved execution/interface failure is propagated as accepted input.

## Computational Record

- run identifier:
- G02 parent manifest:
- code and executable versions:
- pseudopotential artifact:
- resource authorization:
- input manifest:
- output manifest:
- interface validation record:
- completion date:
