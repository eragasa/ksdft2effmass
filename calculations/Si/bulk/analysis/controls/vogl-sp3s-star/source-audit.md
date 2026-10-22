# Vogl 1983 source audit

## Primary source

- P. Vogl, H. P. Hjalmarson, and J. D. Dow, “A semi-empirical tight-binding
  theory of the electronic structure of semiconductors,” *Journal of Physics
  and Chemistry of Solids* 44 (1983), 365--378.
- DOI: [`10.1016/0022-3697(83)90064-1`](https://doi.org/10.1016/0022-3697(83)90064-1).
- Retrieved PDF SHA-256:
  `3bee3702162b8d2a60543cdbfbb7ff188770b69e2af104f998ef68ba472e7c39`.
- Relevant locations: Hamiltonian on printed page 367; structure factors,
  parameter definitions, and Table 1 on printed page 368.

The source defines a nearest-neighbor empirical pseudo-Hamiltonian in a
symmetrically orthogonalized quasi-atomic basis. It is not a first-principles
Hamiltonian.

## Table 1

The accepted calculation-owned transcription is [table1.json](table1.json). It
contains the printed 16 compounds, 13 ordered parameters, and 208 values in eV.
Its SHA-256 is
`77d1766661d76778239a13e45e701c892c2ee4db0f74c43fb21df292da60ef27`.

Source bindings retained in that document include:

- source-page identity:
  `reading-page-location:sha256:4c07fcbb9be5ae8ab54addd7a44639764dfcd072b48fc217551b4218fd48bf26`;
- 600-dpi Table 1 region identity:
  `rendered-region:sha256:18f643e41995809242c1f701295c8277dc33f7467194b2c1e5ffbc9ef13f96f4`;
- source-backed transcription SHA-256:
  `f984bb23335002765b1b65083f794e29edb44b7159990defc5ef29fd61eb8173`.

The operator accepted the rendered Table 1 values on 2026-10-22. The five
values that differed from the inspected external notebook were resolved in
favor of the printed Vogl table:

| Compound | Parameter | Accepted Vogl value | Notebook value |
|---|---|---:|---:|
| AlAs | `E(s,a)` | -7.5273 | -7.5270 |
| AlSb | `E(s*,a)` | 6.7607 | 6.7606 |
| AlSb | `V(s,s)` | -5.6448 | -5.6488 |
| GaP | `E(s,a)` | -8.1124 | -8.1224 |
| GaP | `V(s*a,pc)` | 4.6541 | 4.6451 |

## Independent implementation boundary

The package `vogl1983_lcao_sp3sstar` is an independent implementation of the
model equations and accepted table. No notebook source code was copied. The
notebook remains only a historical cross-check and is not a software or
scientific authority.

The implementation fixes the basis order, eV unit, reduced-wavevector
convention, structural zero couplings, and Hermitian block construction. Tests
cover the full table inventory, silicon parameter row, analytic structure
factors, matrix Hermiticity, silicon Gamma spectrum, reciprocal periodicity,
and invalid inputs.

## Paper-to-code crosswalk

The code preserves the paper's anion (`a`) and cation (`c`) notation rather than
introducing implementation-only orbital names:

| Published object | Calculation-local implementation |
|---|---|
| Ten-orbital anion-then-cation basis | `Vogl1983BasisIndex` |
| $\mathbf{k}=(2\pi/a_L)\mathbf{q}$ input convention | `Vogl1983StructureFactors.from_reduced_wavevector` and the model class docstring |
| Equation (6), named $(g_0,g_1,g_2,g_3)$ record | `Vogl1983StructureFactors` |
| Diagonal $(s,p_x,p_y,p_z,s^*)$ sublattice blocks | `Vogl1983HamiltonianBlocks._onsite_block` |
| Published anion-to-cation block $T(\mathbf{k})$ | `Vogl1983HamiltonianBlocks._anion_to_cation_hopping_block` |
| Named $D_a$, $T(\mathbf{k})$, and $D_c$ record | `Vogl1983HamiltonianBlocks` |
| Full $10\times10$ Hermitian block matrix | `Vogl1983HamiltonianBlocks.assemble` and `Vogl1983LcaoSp3sStarModel.hamiltonian` |
| Ascending finite-matrix eigenvalues | `Vogl1983LcaoSp3sStarModel.band_energies` |
| Accepted printed parameters | `Vogl1983Table1Parameters`, `Vogl1983Table1`, and `table1.json` |

The 13 Python parameter fields are direct ASCII transliterations of the Table 1
symbols:

| Table 1 symbol | Python field | Table 1 symbol | Python field |
|---|---|---|---|
| $E(s,a)$ | `e_s_a` | $E(p,a)$ | `e_p_a` |
| $E(s,c)$ | `e_s_c` | $E(p,c)$ | `e_p_c` |
| $E(s^*,a)$ | `e_s_star_a` | $E(s^*,c)$ | `e_s_star_c` |
| $V(s,s)$ | `v_s_s` | $V(x,x)$ | `v_x_x` |
| $V(x,y)$ | `v_x_y` | $V(s_a,p_c)$ | `v_s_a_p_c` |
| $V(s_c,p_a)$ | `v_s_c_p_a` | $V(s_a^*,p_c)$ | `v_s_star_a_p_c` |
| $V(p_a,s_c^*)$ | `v_p_a_s_star_c` |  |  |

The immutable structure-factor and Hamiltonian-block records expose the paper's
intermediate mathematical objects without requiring callers to unpack anonymous
arrays. The hopping-block source keeps the published orbital order visible in its
row and column comments. A direct analytic test reconstructs equation (6) from
the four tetrahedral bond phases, and named block and entry tests check onsite,
hopping-sign, and structural-zero slots against the published parameter names.
These tests establish implementation behavior only.

This model is an empirical development control. It does not validate Quantum
ESPRESSO, Wannier90, the planned reduced hierarchy, or material predictions.
