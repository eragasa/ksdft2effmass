# ABINIT basic1 stage-1 execution preflight

## Status and claim boundary

This is a **proposed execution preflight**, not a calculated result or execution
authorization. It selects one exact upstream tutorial stage for a possible first ABINIT
scientific-input run. The run remains blocked by checkpoint `ABINIT-BASIC1-RUN-HC01`.

The first stage is intentionally narrower than the complete basic1 tutorial. It tests
the preprocessing → simulation → useful-output-processing path for one H$_2$
self-consistent-field input before considering the 21-dataset distance scan, geometry
optimization, density exercise, or atomization-energy stage.

## Exact selected identities

| Item | Selected identity |
|---|---|
| Executable | Connector-enabled ABINIT 10.8.3 development installation |
| Executable SHA-256 | `0f5b2ddc46a166271a5a61a0d618974cc8db1b3dfb7dbe13ebf4b04396b54e82` |
| Input | `${ABINIT_SOURCE_ROOT}/tests/tutorial/Input/tbase1_1.abi` |
| Input bytes | 3,634 |
| Input SHA-256 | `9b0669ce02e4312eb26f110aa0556338f567977062219f596dc12926fff0dd37` |
| Tutorial prose | `${ABINIT_SOURCE_ROOT}/doc/tutorial/base1.md` |
| Tutorial-prose SHA-256 | `82da087d1a1a147ba94c3c7da5b519c218ead374189fbd4c61430b6de0c58cc3` |
| Pseudopotential | `${ABINIT_SOURCE_ROOT}/tests/Pspdir/Psdj_nc_sr_04_pw_std_psp8/H.psp8` |
| Pseudopotential bytes | 75,139 |
| Pseudopotential SHA-256 | `af415463efe6cbd281cad1b3fda928016408ec401b0f2c671275fa8f19594983` |

The input and pseudopotential are already present in the verified official ABINIT 10.8.3
source archive. No additional tutorial or pseudopotential download is proposed.

## Reuse and redistribution boundary

The ABINIT archive `COPYING` states that most source and documentation use GPL-3.0,
but the exact tutorial input does not carry a file-specific license notice. Local
execution does not redistribute it; committing that upstream input into this
Apache-2.0 repository remains deferred pending a specific compatibility disposition.

The bundled directory README identifies the pseudopotential as PseudoDojo NC-SR v0.4,
Perdew--Wang LDA, standard accuracy, generated with ONCVPSP 3.3.0. The upstream [PseudoDojo repository](https://github.com/abinit/pseudo_dojo) states
that pseudopotential and generation-input files use CC BY 4.0. The proposed run stages an external copy with PseudoDojo attribution and
does not commit it.

## Input system and scientific settings

The proposed run preserves the upstream input byte-for-byte and therefore does not
select or change a project production setting.

| Setting | Upstream tutorial value |
|---|---|
| System | H$_2$ molecule; two hydrogen atoms |
| Cell | Orthogonal 10 × 10 × 10 Bohr box |
| Atomic positions | $(-0.7,0,0)$ and $(0.7,0,0)$ Bohr |
| Pseudopotential | PseudoDojo NC-SR v0.4 standard PSP8; PW LDA (`pspxc=-1012`) |
| Plane-wave cutoff | 10 Hartree |
| Sampling | One manually selected Gamma point |
| SCF limit | 10 steps |
| Stopping criterion | `toldfe = 1.0d-6` Hartree, satisfied twice consecutively |
| Molecular preconditioner | `diemac = 2.0` |
| Parallel scale | Direct serial invocation; no MPI launcher; upstream test metadata sets `max_nprocs = 1` |

The upstream ABINIT 10.5.8.2 reference reports two bands, a 30 × 30 × 30 FFT grid,
and 752 time-reversal-reduced plane waves. It reports completion after six SCF cycles,
0.4 seconds wall time, less than 8.712 MB estimated calculation memory, a roughly
0.025 MB wavefunction file, and a roughly 0.208 MB density file. These are **upstream
reference expectations**, not results from the installed ABINIT 10.8.3 executable and
not acceptance tolerances.

## Proposed isolated execution

The run root would be a new timestamped directory outside the repository beneath the
existing external run area. It would contain:

```text
input-source/       immutable copied source input
pseudo/             attributed staged PseudoDojo file in its expected subdirectory
work/               executable working directory and native outputs
streams/            separate stdout, stderr, and timing streams
records/            compact preflight, identity, extraction, and status summaries
```

The material command shape is:

```bash
cd work
ABI_PSPDIR=../pseudo abinit tbase1_1.abi \
  >../streams/stdout.txt \
  2>../streams/stderr.txt
```

The anticipated local scale is one CPU process, well under 100 MB memory, under 10 MB
new output, and under one minute wall time. These are conservative execution estimates;
the actual runtime and storage would be measured.

## Anticipated outputs and useful processing

The tutorial identifies the main `.abo` output, human-readable log stream, DDB, density,
eigenvalue, wavefunction, band-plot, GSR NetCDF, EIG NetCDF, and OUT NetCDF files. Exact
files remain an observed outcome rather than a fabricated inventory.

If authorized, postprocessing will:

1. preserve stdout, stderr, exit status, elapsed time, executable identity, exact input,
   pseudopotential identity, and before/after workspace snapshots separately;
2. extract from the `.abo` output the completion marker, warning/comment counts, SCF
   stopping status, iteration count, total energy, eigenvalues, forces, and reported
   memory/file estimates;
3. inspect GSR, EIG, and OUT NetCDF structure with the installed NetCDF 4.10.1 tools and
   extract scientifically named scalar/array content needed by the tutorial rather than
   treating the files only as hashes;
4. retain density and wavefunction files externally for native continuation or later
   authorized processing without committing them; and
5. label all observations as tutorial calculated results with exact provenance, not as
   production convergence, numerical verification, or scientific validation.

No comparison with Quantum ESPRESSO is proposed because the current QE campaign has no
same-system H$_2$ counterpart.
