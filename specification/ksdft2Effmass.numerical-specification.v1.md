# Numerical Specification v1

Task: `ksdft2Effmass.computational.01.01.02`
Artifact: `NumericalSpecification-v1`
Status: `Passed`
Scope: protocol-freezing artifact for the pristine bulk-silicon pilot supporting `G02`--`G04` and active paper `P01`.

This document freezes the numerical **protocols** and provenance requirements used by downstream calculations. It does not require production executables to be available in the editing environment and does not require final converged cutoffs, $k$-meshes, lattice constants, band gaps, effective masses, or Wannier windows. Those values are outputs of later convergence and validation tasks and must not be silently inferred here.

## Inputs

- Physical parent problem: [`PhysicalSpecification-v1`](ksdft2Effmass.physical-specification.v1.md).
- Active-paper boundary: bulk silicon only; no dopants, continuum reductions, charged-defect branches, or projector searches are introduced into `P01` by this numerical specification.
- Current family/release/table authority: [DFT Pseudopotential Library Specification v1](dft-pseudopotential-library/v1/index.md). It supersedes the earlier standard-table source selection; exact current native-file identities remain pending.
- The 2026-07-28 standard-table inspection is retained below as a historical identity, not as a v0.5 artifact.

## Software-stack provenance protocol

Production executables are not acceptance prerequisites for this task. They are provenance fields that must be recorded by the downstream task that first uses each executable.

| Component | Frozen protocol | Downstream provenance record | Status |
|---|---|---|---|
| Python package | Use repository package `ksdft2effmass`, Python `3.14` as declared in `python/pyproject.toml`. | Python executable path, Python version, package commit, installed dependency versions, and relevant test command output. | Frozen |
| Numerical Python libraries | Use NumPy `>=2.3,<3` and SciPy `>=1.18,<2` as declared in `python/pyproject.toml`. | Exact installed versions in each run manifest. | Frozen |
| Development checks | Use the repository-declared development tools when an implementation artifact is accepted. | Exact `pytest`, `ruff`, `mypy`, and coverage-tool versions when used. | Frozen |
| Quantum ESPRESSO SCF/NSCF/relaxation | Use `pw.x` for bulk SCF, NSCF, band-path, and lattice-optimization tasks. | `pw.x --version`, executable path, module/container name, MPI/OpenMP settings, compile/build provenance when available, and run command. | Frozen provenance protocol |
| Quantum ESPRESSO to Wannier90 interface | Use `pw2wannier90.x` for QE-to-Wannier90 conversion. The `pw.x`, `pw2wannier90.x`, and `wannier90.x` records must be mutually compatible: same QE installation for `pw.x`/`pw2wannier90.x`, matching file-format expectations, and a successful interface smoke test before accepted Wannier production. | `pw2wannier90.x --version` or QE version banner, executable path, associated `pw.x` path/version, conversion input, output checksums, and interface smoke-test result. | Frozen provenance protocol |
| Wannier90 | Use `wannier90.x` for Wannier construction. | `wannier90.x --version`, executable path, module/container name, build provenance when available, and run command. | Frozen provenance protocol |
| Rust | Optional until a task explicitly depends on Rust. | `rustc --version`, `cargo --version`, and build flags for accepted Rust artifacts. | Deferred |

## Bulk pseudopotential protocol

### Current source-library selection

The common B/Si/P baseline is **PseudoDojo ONCVPSP v0.5, PBE, scalar-relativistic,
stringent**. Quantum ESPRESSO uses UPF2; ABINIT uses the separately identified PSP8
representation. The source entry may be shared, but its native representations have
different exact byte identities and do not establish cross-code numerical agreement.

The accepted library specification records these starting hints for silicon:

| Element | Low | Normal | High |
|---|---:|---:|---:|
| Si | 14 Ha / 28 Ry | 18 Ha / 36 Ry | 24 Ha / 48 Ry |

These are source-library recommendations, not accepted project cutoffs. Exact native-file
URLs, byte counts, complete SHA-256 identities, local set membership, and current-byte
verification remain pending before use. No historical `Si.upf` hash is substituted for
the selected v0.5 stringent artifact.

The exact P and B artifacts are selected and verified by `06.01.01` and `07.01.01`
within their approved branches. Final B:Si acceptor/SOC work uses the separate PseudoDojo
v0.4 PBE fully relativistic stringent branch with a matching Si host; it does not reuse
the scalar pilot as its spinor reference.

### Historical artifact identity — not the current release

The original inspection recorded this standard-table URL:

```text
https://www.pseudo-dojo.org/pseudos/nc-sr-04_pbe_standard/Si.upf.gz
```

Its metadata labels and byte identities are preserved as originally recorded:

| Element | File | PseudoDojo table | PseudoDojo version | Type | Relativistic flag | Valence electrons | Normal hint (Ha) | High hint (Ha) | SHA-256 of downloaded `.upf.gz` | SHA-256 of decompressed `.upf` | Status |
|---|---|---|---|---|---|---:|---:|---:|---|---|---|
| Si | `Si.upf.gz` | `nc-sr-04_pbe_standard` | `1.0` | NC | scalar | 4 | 18 | 24 | `bfbd01ccd4b67584dcf19a490a76e9b688c25026775ce2f4a4b6a13f900dad81` | `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282` | Historical identity only |

The retained SSSP 1.3.0 PBE Efficiency silicon parent is another distinct historical
development source. Its `42/336 Ry` observations, structure, and Wannier outputs are not
v0.5/stringent convergence evidence. Neither that retained source nor the separately
authorized SSSP v2.0 Precision comparison replaces the approved common baseline.

## Plane-wave cutoff refinement rules

Cutoff convergence is a protocol, not a completed value in this artifact.

1. Keep the physical branch, exact pseudopotential bytes, lattice parameter, occupation convention, and $k$-mesh fixed while varying a cutoff coordinate.
2. Start from the selected PseudoDojo silicon normal/high hints, `ecutwfc = 36 Ry` and `48 Ry`, as recommendations only.
3. Freeze a monotone candidate sequence that brackets and extends those hints, for example `30, 36, 42, 48, 54, 60 Ry`; an execution preflight must declare any justified narrower or wider sequence before execution.
4. `ecutrho = 4 * ecutwfc` is an initial norm-conserving screening trial, not an accepted density cutoff. A wavefunction-cutoff qualification axis holds the density cutoff at one prospectively frozen sufficiently conservative value.
5. Refine the density cutoff independently at fixed wavefunction cutoff, including a higher guard. Ratios such as `4, 6, 8` describe starting candidates, not transferable accepted settings.
6. Change only one controlled variable per convergence table; coupled screening scans do not replace the separate axes. Retain prospectively declared mixed cutoff/mesh corner controls where required.
7. Select the smallest cutoff pair satisfying all declared convergence tolerances for the target bulk observables, then retain one higher setting on each relevant axis as a guard calculation when computationally affordable.
8. Record rejected values and the observable that rejected them; do not update accepted values merely to make later tests pass.

## $k$-mesh refinement rules

Bulk Brillouin-zone sampling is split into separate meshes for SCF density convergence, high-symmetry band paths, valley-local sampling, and effective-mass fitting. A dense path calculation must not be treated as a substitute for a converged SCF integration mesh.

1. Use uniform Monkhorst--Pack meshes for primitive-cell SCF convergence.
2. Preserve symmetry-compatible offsets for the selected cell convention; record whether the mesh is Gamma-centered or shifted.
3. Refine the SCF mesh monotonically, for example `6x6x6`, `8x8x8`, `10x10x10`, `12x12x12`, and continue until the target observables are stable.
4. Select the smallest SCF mesh satisfying all declared tolerances and record at least one finer comparison if feasible.
5. Use independently specified non-self-consistent sampling for path, valley, and mass tasks, all generated from the accepted SCF density.

## Separate bulk sampling protocols

| Protocol | Purpose | Frozen rule | Accepted value supplied by |
|---|---|---|---|
| SCF mesh | Converge charge density and total energy for the primitive bulk parent. | Uniform Monkhorst--Pack sequence with one-variable-at-a-time refinement and fixed occupation convention. | `02.01.03` |
| Band-path sampling | Report high-symmetry band structure and withheld path points. | Run NSCF/bands calculations on an explicitly listed path after SCF convergence. Record path labels, reciprocal-coordinate convention, point density per segment, band indexing rule, and withheld-point list before fitting. | `02.02.01`/`02.02.02` |
| Valley sampling | Locate the conduction valley along the selected $\Gamma$--$X$-type direction for the non-SOC bulk pilot. | Use a one-dimensional NSCF refinement around the coarse path minimum. Fit or interpolate only within a recorded local interval; report the fractional path coordinate and uncertainty from refinement. | `02.02.02` |
| Effective-mass sampling | Estimate longitudinal and transverse electron effective masses. | Use local NSCF stencils around the selected conduction minimum. Record Cartesian/reciprocal axes, finite-difference or polynomial order, stencil radii, units, and stability under at least one smaller stencil. | `02.02.02` |
| Wannier interface sampling | Provide QE outputs suitable for Wannier90. | Use an explicit uniform grid compatible with `pw2wannier90.x` and the selected Wannier task. Record whether the grid is the same as, coarser than, or finer than the converged SCF mesh. | `03.01.01`--`03.02.01` |

## Bulk-lattice optimization procedure

The production lattice constant is not accepted here; the procedure for obtaining it is frozen here.

1. Use the frozen physical branch: pristine diamond-structure Si, PBE, scalar-relativistic, non-SOC, non-spin-polarized, and the selected Si PseudoDojo pseudopotential.
2. Use primitive two-atom diamond Si cells for the primary equation-of-state series. Conventional cubic coordinates may be used only as a documented coordinate representation.
3. Before the final lattice optimization, use cutoff and SCF $k$-mesh settings at least as strict as the currently accepted convergence settings for total energy and stress.
4. Generate a symmetric volume or lattice-constant grid around the expected PBE equilibrium. The initial grid must include at least seven points and span both compressed and expanded cells; a typical starting span is approximately $\pm 3\%$ in lattice constant.
5. At each grid point, keep the diamond internal coordinate fixed by symmetry and run an SCF calculation with identical numerical settings.
6. Fit an equation of state or an explicitly stated polynomial in a local interval around the minimum. Record the fit form, included points, excluded points, and residuals.
7. Refine the grid around the fitted minimum until the equilibrium lattice constant changes by less than `1e-4 Å` under the refinement or until the residual uncertainty is larger, in which case report the larger uncertainty.
8. Verify the final candidate by either a variable-cell relaxation constrained to the diamond symmetry or an additional energy/stress calculation at the fitted lattice constant.
9. Freeze the accepted lattice constant for downstream bulk and compatible supercell lattice vectors. Treat the experimental lattice constant only as an external validation branch.
10. Record all energies per primitive cell and per atom, units, stress conventions, and conversion factors.

## Downstream numerical-convergence tolerances

The following tolerances are frozen acceptance rules for downstream numerical convergence; they are not completed results of this task.

| Observable | Numerical-convergence tolerance | Notes |
|---|---:|---|
| Total energy per Si atom | `1e-5 Ry/atom` between successive accepted settings | Used for numerical stability, not as the sole physics acceptance test. |
| Equilibrium lattice constant | `1e-4 Å` or the larger fitted uncertainty | Applies to the lattice optimization refinement. |
| Indirect Kohn--Sham gap | `1 meV` between successive accepted settings | Parent-model PBE gap error is tracked separately and is not a numerical error. |
| Conduction-valley position along the selected high-symmetry line | `0.002` in fractional path coordinate | Coordinate convention must be recorded with the path. |
| Longitudinal electron effective mass | `0.5%` relative change | Fit window and finite-difference stencil must be recorded. |
| Transverse electron effective mass | `0.5%` relative change | Fit window and finite-difference stencil must be recorded. |
| Withheld-point band energies for the selected bulk validation set | `1 meV` maximum absolute change at fixed band/path labeling | Withheld set is selected before fitting or reduction. |

These tolerances test numerical stability relative to the selected Kohn--Sham parent. They are not scientific validation against experiment.

## Controlled regression record

| Reference | Candidate | Metric | Tolerance | Result |
|---|---|---|---|---|
| Historical Si URL and SHA-256 identities listed above | Original standard-table download and decompression record | Exact compressed and decompressed SHA-256 identities | Exact string equality | Historical passed record; not repeated by this reconciliation |
| Accepted pseudopotential-library specification | Current family, release, relativity, table, and native-format declarations | Consistent source-library selection without reusing historical artifact identities | Exact declared branch | Selection specified; exact current artifact admission remains pending |
| Protocol scope requested by PI | This artifact | No requirement for production executables or final converged numerical values at `01.01.02` | Protocol-only acceptance | Passed |

The historical regression records the earlier artifact identity only. The current
source-library selection does not claim a new download, current-byte verification,
catalog admission, completed convergence, or validation of any electronic-structure
result.

## Explicit non-results

- No Quantum ESPRESSO calculation was run.
- No Wannier90 calculation was run.
- No production executable version is accepted here.
- No lattice constant, band gap, effective mass, converged cutoff, converged $k$-mesh, or Wannier window is reported.
- Exact current Si, P, and B artifact identities and qualification remain downstream requirements; the common family/release/table and separate final B:Si SOC branch are already selected.
