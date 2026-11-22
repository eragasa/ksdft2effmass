# Silicon source-association review

**ReviewOutcome: REVIEW_INCONCLUSIVE**  
**OperatorRequest: DECISION_REQUIRED**

The dossier is defensible as a candid, stopped association report. **Creating the canonical reviewed-state source assertion is not supported now under the existing contract.** Shared native band/gauge lineage supports the finite-band coefficient association; it does not establish equality of the executed and nominal physical geometries.

Scope: read-only review of `calculations/Si/bulk/analysis/wannier-window-remedy/source-associations.md`, identified by the supplied SHA-256 `e25c91f03f733ab52254213b629310e8688b9358c139229b435f417b2a71e2d0`. That digest was not independently recomputed.

All repository paths below are relative to `calculations/Si/bulk/`.

## Finding: geometry identification remains unresolved

**Disposition: HUMAN_DECISION_REQUIRED**

**Problem:** The evidence establishes a common native computational occurrence, but not the exact geometry association required by the present source-admission contract.

**Evidence:**

- `analysis/c6-b20-w21-untruncated-characterization/characterization-result.json:5–22` declares nonzero direct-basis entries `2.7345910468201033 Å`.
- `simulations/evidence/wannier-localization/run-001/input/silicon.win:21–26` presents those entries as `2.734591046820 Å`.
- The executed NSCF input, `simulations/evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20/input/pw.in:27–30`, instead specifies `2.73459105 Å`.
- Its retained external `run/tmp/system.save/data-file-schema.xml:365–377` records the output cell as `5.167628147352816 bohr`. QE reference `Modules/constants.f90:38` supplies the stated Bohr radius. The reported `3.1798967903284847e-9 Å` residual is a parent observation, not my recomputation.
- `research-protocol/controlled-reduction-protocol-hopping-first.tex:319–345` requires explicit, exact geometry/conventions and stops on a missing or unequal identity member.
- `common_space/verification/native_inputs.py:107–119` explicitly treats geometry labels as opaque declarations; `source_admission.py:135–138,210–220` cannot establish their scientific truth by serialization.

QE reference `PP/src/pw2wannier90.f90:1510–1531,1654–1665` checks lattice compatibility with `eps6` and constructs projection centers using native `at`. Successful conversion therefore explains compatibility, not exact equality with S30/WIN metadata.

**Consequence:** A canonical assertion could incorrectly identify nominal geometry with the actual parent geometry. Fractional/index correspondence would then be overstated as exact physical Cartesian-wavevector correspondence.

**Smallest next action:** Retain the stopped dossier. Before assertion creation, the scientific owner must choose between:

1. retaining the current identity rule and leaving admission stopped; or
2. separately authorizing an explicit clarification/amendment that distinguishes the actual native parent geometry from nominal S30/Wannier metadata and defines the permitted serialization identification, including coordinate presentations.

**Recommendation:** Keep admission stopped pending that explicit decision. Neither the discrepancy’s smallness, more arithmetic, nor an opaque geometry label resolves it. Calculator reruns are not automatically required.

## Correct and supported

- **Occurrence lineage:** I cross-read the converter result/input, localization input manifest, execution record and external inventory, plus S30/S110 source entries. Their declared AMN/EIG/NNKP and U/U_dis/HR identities correlate. This supports common native band-index/gauge origin—not merely matching spectra. S30’s “full source” is the ten-dimensional untruncated Wannier operator, not the complete KS space. S105 explicitly retains its support (`analysis/c6-b20-w21-spatial-truncation-disposition/spatial-truncation-disposition.json:52–63`).

- **Ultrasoft metric:** The retained UPF header declares scalar-relativistic USPP, not PAW; XML output agrees. QE reference `compute_amn` applies `s_psi` to the trials before the scalar conjugate-transpose product (`PP/src/pw2wannier90.f90:5132–5225`). Thus `A=<ψ|S|g>` is the appropriate declared interpretation. In an S-orthonormal parent-band coefficient frame, `W†C` needs no additional S factor. This does not certify solver orthonormality or all-electron populations.

- **Projection and spin conventions:** Native NNKP projection records (`silicon.nnkp:237–259`) agree with the stated eight hybrids followed by two additional radial-s trials. Wannier90’s `doc/user_guide/projections.tex:339–349` supports the half-Hadamard transformation. Coordinate unitarity does not imply orthonormal raw trial columns. XML spin flags, WIN `spinors=false`, and converter `spin_component='none'` support one scalar orbital block, not a doubled spinor basis.

- **Point presentation and row packing:** The dossier properly distinguishes decimal coordinate presentations from physical wavevectors. I checked the parent inspection logic: it compares explicit ordered presentations, checks ordered EIG energies above `-6 eV`, and checks zero U_dis tails. Wannier90 `src/disentangle.F90:699–722,1019–1026` supports the resulting first-row identification; `:240–245` zeros unused rows. **Conditional on the reported checks**, no row-offset expansion is needed for this occurrence. I did not independently reproduce the full-grid checks.

- **Reference and uncertainty:** QE `write_band` writes `et*rytoev` without the proposed energy shifts. AMN formatting and Wannier90 `src/plot.F90:1661–1680` support the stated decimal quanta. Nearest rounding and correspondence between these reference sources and historical executable builds remain assumptions, correctly disclosed at dossier lines 176–184. The printing/parsing model does not bound geometry rendering, DFT, solver, localization or reduction errors.

No unsupported completion or source-to-build attestation claim was found. The parent scratch’s reported 438 saved-state checks, 464 identities, extrema and residuals remain **parent observations**, not independent verification by this review.

## Limits and disposition

I inspected the bounded working-tree inventory, relevant protocol delta, named contracts, retained declarations/native excerpts, reference source, and parent scratch logic/output. I did not run commands, hashes, tests, calculators, producer, verifier or replay; inspect wavefunction contents or withheld402 values; change settings; or edit files.

Producer reconstruction, point-inventory evidence and a truthful completion receipt remain separate outstanding prerequisites (`source_admission.py:256–294`). This review establishes neither completed CSD0/CSD1-V, scientific validation, human acceptance, CSD3 selection nor execution permission.

**Merge verdict: OK with notes — retain the stopped dossier; do not create the canonical source assertion yet.**