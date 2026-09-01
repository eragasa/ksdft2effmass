# ABINIT basic tutorials and Quantum ESPRESSO correspondence

**Status:** Proposed tutorial-task mapping. No ABINIT installation, dependency,
input acquisition, pseudopotential selection, or executable invocation is authorized
by this document.

The official [ABINIT tutorial overview](https://docs.abinit.org/tutorial/) states
that basic tutorials 1--4 form a sequential introductory unit. The first bounded
ABINIT campaign therefore represents those four tutorials rather than immediately
creating executable Tasks for every advanced ABINIT topic.

## Correspondence

| ABINIT Task | Official tutorial scope | Closest existing QE Task correspondence | Interpretation |
|---|---|---|---|
| `abinit.tutorials.basic1-h2` | H2 SCF, geometry, density, atomization, multidataset input | No direct counterpart | QE structure-optimization and density workflows exercise related mechanics, but no existing QE Task uses the same H2 system and claim. |
| `abinit.tutorials.basic2-h2-convergence` | H2 cutoff and supercell convergence; LDA/GGA comparison | `quantumespresso.simulations.convergence-silicon` | Methodological correspondence only. The material, finite-cell error, pseudopotential, observables, and XC comparison differ. |
| `abinit.tutorials.basic3-silicon` | Silicon total energy, k-point convergence, lattice parameter, Kohn--Sham bands | `quantumespresso.simulations.scf-silicon`, `quantumespresso.simulations.convergence-silicon`, `quantumespresso.simulations.structure-optimization-silicon`, `quantumespresso.simulations.bands-silicon` | Strong workflow correspondence. It does not imply equal inputs or numerically comparable results. |
| `abinit.tutorials.basic4-aluminum` | Metallic aluminum, k-point/smearing convergence, lattice parameter, surface slabs | `quantumespresso.simulations.aluminum-metal`, `quantumespresso.simulations.smearing-convergence-aluminum` | Strong bulk-metal workflow correspondence. No existing QE campaign Task corresponds to the aluminum-surface branch. |

## Comparison boundary

Correspondence means that two tutorials exercise related computational stages or
observables. It does not establish equivalent physical models, pseudopotentials,
exchange-correlation settings, structures, units, k-point conventions, convergence
criteria, energy references, or scientific claims. Any paired numerical comparison
requires separately aligned inputs and a declared numerical-verification contract.

The ABINIT tutorials report illustrative or tutorial reference values. Those values
must not become project acceptance tolerances merely because a corresponding QE Task
exists.

## Execution boundary

All Tasks are inactive or blocked. Planning and source inspection do not authorize
ABINIT installation or execution. Before any run, record the exact executable,
version, tutorial inputs, pseudopotentials and reuse terms, expected scale, output
locations, and resource estimate, then obtain the applicable protected-execution
authorization. Large native outputs remain outside Git.

Advanced ABINIT tutorials, including PAW, DFPT, electron--phonon, GW, BSE, DMFT,
TDDFT, MULTIBINIT, and advanced parallelism, are not activated or represented as
near-term executable work by this bounded mapping.
