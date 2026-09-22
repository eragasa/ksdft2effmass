# Quantum ESPRESSO realization

Checkpoint `QE-SILICON-DOS-RUN-HC01` authorized one Quantum ESPRESSO 7.5
SCF-to-NSCF-to-DOS actual-data probe. The Workflow completed once without retry using
three separately activated and granted CPN Task instances:

1. `pw.x` SCF with a 50 Ry cutoff, 8 bands, and an unshifted $8\times8\times8$ mesh;
2. `pw.x` NSCF with 8 bands, tetrahedron occupations, and an unshifted
   $12\times12\times12$ mesh, consuming an identity-verified immutable SCF-state
   copy; and
3. `dos.x` over $[-9,16]$ eV, consuming an identity-verified immutable NSCF-state
   copy.

Both `pw.x` inputs used the selected QEXSD-derived
`celldm(1)=10.207479550732002` Bohr geometry. The pinned NSCF omission of `nosym` was
preserved.

All three processes exited with status 0 and printed `JOB DONE.`. QE reported SCF
convergence in six iterations, 29 irreducible SCF k-points, 72 irreducible NSCF
k-points using the tetrahedron method, and 8 Kohn--Sham states in both `pw.x` Tasks.
The DOS process reported `Tetrahedra used` and produced an identified 82,588-byte
`si_dos.dat` artifact. Its 2,501 finite three-column data rows span −9 to 16 eV with a
0.01 eV step. The file header reports a Fermi energy of 6.642 eV.

The compact calculated observation is
[qe75-calculated-observation.json](expected/qe75-calculated-observation.json). The full
streams, snapshots, native states, state-copy manifests, and DOS artifact remain in the
identified external run. Source inputs and the pseudopotential are not redistributed
here.

This is one calculated tutorial observation. It does not establish production
convergence, pseudopotential suitability, an accepted project geometry, a project
reference DOS, numerical verification, scientific validation, uncertainty
quantification, QE--ABINIT equivalence, or a complete many-body excitation spectrum.
See the
[exact preflight](../../../../docs/computational/silicon-scf-nscf-dos-preflight.md).
