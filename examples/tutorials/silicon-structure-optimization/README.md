# Silicon structure-optimization tutorial

This tutorial concept represents variable-cell optimization of a two-atom diamond
silicon cell while holding both atomic positions fixed. It is a prerequisite selected
for the separate silicon SCF-to-NSCF-to-DOS tutorial Workflow.

## Backend status

| Backend | Status | Scope |
|---|---|---|
| [Quantum ESPRESSO](qe/README.md) | Calculated tutorial observation | One authorized QE 7.5 `pw.x` variable-cell-relaxation Task completed. |
| [ABINIT](abinit/README.md) | Proposed | No corresponding ABINIT calculation or portable example has been selected. |

The backend directories share a computational concept only. They do not establish
aligned inputs, pseudopotentials, numerical equivalence, scientific validation, or an
accepted project geometry.

Human decision `QE-SILICON-DOS-GEOMETRY-HC01` selected the calculated QEXSD-derived
`10.207479550732002` Bohr geometry for the separate tutorial DOS Workflow. That
bounded selection does not promote the geometry to a project lattice reference.
