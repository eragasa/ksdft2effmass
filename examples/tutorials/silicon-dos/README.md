# Silicon density-of-states tutorial

This tutorial represents one Quantum ESPRESSO silicon SCF-to-NSCF-to-DOS Workflow.
SCF, NSCF, and DOS were executed as three independent reusable CPN Task instances
with separate activations, attempts, execution grants, private workspaces, process
observations, result ingresses, and CPN firings.

## Backend status

| Backend | Status | Scope |
|---|---|---|
| [Quantum ESPRESSO](qe/README.md) | Calculated tutorial observation | One authorized QE 7.5 three-Task Workflow completed without retry. |
| [ABINIT](abinit/README.md) | Deferred | No ABINIT DOS realization or cross-backend comparison is claimed here. |

The selected `10.207479550732002` Bohr geometry came from the separately retained QE
structure-optimization tutorial ResultObject. Its use here does not promote it to a
project lattice reference. The calculated DOS is likewise not a project reference,
scientific validation result, or evidence of QE--ABINIT equivalence.
