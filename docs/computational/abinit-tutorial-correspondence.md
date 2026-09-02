# ABINIT basic tutorials and Quantum ESPRESSO correspondence

**Status:** Proposed tutorial-task mapping. ABINIT 10.8.3 is installed with its
Wannier90 3.1.0 connector enabled under separate resolved checkpoints, but no tutorial
input acquisition, pseudopotential selection, or scientific executable invocation is
authorized by this document.

The official [ABINIT tutorial overview](https://docs.abinit.org/tutorial/) states
that basic tutorials 1--4 form a sequential introductory unit. The first bounded
ABINIT campaign therefore represents those four tutorials rather than immediately
creating executable Tasks for every advanced ABINIT topic.

Maintained examples use the concept-first paired layout defined by
[cross-backend tutorial examples](../architecture/v2/tutorial-examples.md). One
upstream ABINIT tutorial may populate several project tutorials when it combines
several computational concepts. Each project tutorial contains both `qe/` and
`abinit/` status directories; this pairing expresses a shared learning objective,
not numerical equivalence.

## Correspondence

| ABINIT Task | Project tutorial path(s) | Official tutorial scope | Closest existing QE Task correspondence | Interpretation |
|---|---|---|---|---|
| `abinit.tutorials.basic1-h2` | `hydrogen-molecule-scf/abinit`, `hydrogen-molecule-structure/abinit`, `hydrogen-molecule-density/abinit` | H2 SCF, geometry, density, atomization, multidataset input | No direct counterpart | The paired QE directories begin as `planned`; unrelated silicon workflows are not treated as the same tutorial. |
| `abinit.tutorials.basic2-h2-convergence` | `h2-convergence/abinit` | H2 cutoff and supercell convergence; LDA/GGA comparison | No same-material QE Task; `quantumespresso.simulations.convergence-silicon` is methodological context only | The material, finite-cell error, pseudopotential, observables, and XC comparison differ. |
| `abinit.tutorials.basic3-silicon` | `silicon-scf/abinit`, `silicon-convergence/abinit`, `silicon-structure-optimization/abinit`, `silicon-bands/abinit` | Silicon total energy, k-point convergence, lattice parameter, Kohn--Sham bands | `quantumespresso.simulations.scf-silicon`, `quantumespresso.simulations.convergence-silicon`, `quantumespresso.simulations.structure-optimization-silicon`, `quantumespresso.simulations.bands-silicon` | Strong workflow correspondence. It does not imply equal inputs or numerically comparable results. |
| `abinit.tutorials.basic4-aluminum` | `aluminum-metal/abinit`, `aluminum-smearing-convergence/abinit`, `aluminum-surface/abinit` | Metallic aluminum, k-point/smearing convergence, lattice parameter, surface slabs | `quantumespresso.simulations.aluminum-metal`, `quantumespresso.simulations.smearing-convergence-aluminum` | Strong bulk-metal workflow correspondence. The paired QE surface directory begins as `planned` because no campaign Task currently owns it. |

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

The exact first-stage H$_2$ SCF candidate and its authorized calculated observation are
documented in the [ABINIT basic1 stage-1 preflight and outcome](abinit-basic1-stage1-preflight.md).
The proposed same-simulation continuation is the [paired ABINIT and QE silicon
SCF-and-bands preflight](paired-silicon-scf-bands-preflight.md), which selects basic3
`tbase3_5.abi` and the corresponding QE workflow and awaits an exact protected-execution
decision. The previously staged ABINIT basic1 stage-2 H$_2$ scan was rejected as a pair
for QE silicon bands and was not executed. Other campaign Tasks remain inactive or
blocked. The completed local installations are documented in
[ABINIT 10.8.3 local installation](abinit-10.8.3-installation.md) and [Wannier90 3.1.0
local installation](wannier90-3.1.0-installation.md); neither authorizes a tutorial
execution. Before any run, record the exact executable, version, tutorial
inputs, pseudopotentials and reuse terms, expected scale, output locations, and
resource estimate, then obtain the applicable protected-execution authorization. Runtime output remains beneath the backend-local ignored `run/` tree. Maintained
ABINIT examples commit only portable reusable input, useful scripts, instructions,
and small test-consumed fixtures under the architecture commit boundary; routine
stdout/stderr, wavefunctions, densities, NetCDF results, and restart files remain
uncommitted.

Advanced ABINIT tutorials, including PAW, DFPT, electron--phonon, GW, BSE, DMFT,
TDDFT, MULTIBINIT, and advanced parallelism, are not activated or represented as
near-term executable work by this bounded mapping.
