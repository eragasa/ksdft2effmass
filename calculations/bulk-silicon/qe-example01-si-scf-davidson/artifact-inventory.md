# QE example01 artifact inventory

**Status:** Observed artifact inventory for the human-accepted tutorial smoke test. No calculation was rerun, and no native artifact was changed, relocated, or committed.

## Main findings

- `tempdir/silicon.save/data-file-schema.xml` is the compact structured QEXSD 23.03.10 record containing the cell, atomic positions and species, reciprocal lattice, ten k-points, four eigenvalues and occupations at each k-point, FFT grids, total energy, and exit status. `tempdir/silicon.xml` is byte-identical redundant output.
- `tempdir/silicon.save/wfc1.dat` through `wfc10.dat` are native unformatted binary wavefunction-coefficient files for the ten irreducible k-points. Observed headers report one spin channel, four bands, and k-point-specific plane-wave dimensions.
- `tempdir/silicon.save/charge-density.dat` is the native binary self-consistent charge-density artifact.
- `tempdir/silicon.save/Si.pz-vbc.UPF` is byte-identical to the selected tutorial pseudopotential.
- Stdout uniquely retains the human-readable iteration history, estimated accuracy, convergence statement, timing/call details, and `JOB DONE.` marker. Stderr contains the exact unresolved IEEE warning already recorded with the accepted simulation.

## Producer attribution and path identity

- PWSCF 7.2 produced `data-file-schema.xml`, `silicon.xml`, `wfc*.dat`, `charge-density.dat`, the save-directory pseudopotential copy, and stdout.
- Stderr belongs to the executed PWSCF process and linked numerical runtime; the IEEE warning text is not attributed more narrowly.
- QE 7.2 `PW/examples/example01/run_example` produced the sanitized SCF input, while the authorized execution wrapper produced the start/end time, wall-time, and exit-status sidecars.
- The `ksdft2effmass` tutorial-capture workflow at repository revision `c6ed673686c9ddd6a756bf47e080af4ffbff4520` produced the compact execution-provenance and result records.
- The downloaded `Si.pz-vbc.UPF` is attributed to the Quantum ESPRESSO original pseudopotential library. The available provenance does not identify a pseudopotential author or generation version, and PWSCF 7.2 is not claimed to have generated it.
- Missing optional artifacts have no producer. Their notes identify the expected producer if they were generated.

Repository-maintained compact artifacts use canonical repository-relative identities under `calculations/bulk-silicon/qe-example01-si-scf-davidson/`. Absolute paths are retained for external calculation artifacts. The execution provenance separately retains observed execution-time paths.

## Retention

The sanitized input, execution provenance, result note, this inventory, and this review are retained compactly in Git. Raw stdout/stderr and the complete 544 KiB post-run scratch tree remain external under `/Users/eugene/projects/q-e-qe-7.2/`. Wavefunctions, charge density, restart metadata, and native pseudopotential copy are not committed. No artifact was deleted or marked safe for deletion by this inventory.

## Candidate extraction inputs

A metadata/spectral periodic-record extraction can begin from `silicon.save/data-file-schema.xml` plus the compact run, executable, input, and pseudopotential provenance. Wavefunction-bearing extraction additionally needs all ten `wfc*.dat` files; density-bearing extraction needs `charge-density.dat`. Stdout remains the source for iteration, convergence, and timing observations not represented equivalently in XML.

No separate eigenvalue sidecar, HDF5 wavefunction file, band output, or post-processed charge-density export was observed. Those absences apply only to this authorized SCF execution.

See [`artifact-inventory.json`](artifact-inventory.json) for exact paths, sizes, SHA-256 identities, formats, completeness, roles, and retention dispositions for every observed or explicitly missing artifact. This inventory defines no generalized artifact framework, extraction schema, DataObject, scientific validation, or successor authorization.
