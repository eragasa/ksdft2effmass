# Vogl 1983 LCAO `sp3s*` control

This calculation-local package implements the nearest-neighbor, spinless,
non-SOC `sp3s*` pseudo-Hamiltonian of Vogl, Hjalmarson, and Dow (1983).
It is an empirical LCAO/tight-binding development control for the planned
silicon ten-orbital hierarchy; it is not a DFT or Wannier model.

## Contents

- `table1.json`: accepted transcription of all 16 compounds and 13 parameters
  from Vogl Table 1, in eV;
- `vogl1983_lcao_sp3sstar/`: typed table access and the ten-band Bloch model;
- `tests/`: table, basis, structure-factor, Hermiticity, periodicity, input,
  and silicon symmetry-point controls.

The Table 1 JSON SHA-256 is
`77d1766661d76778239a13e45e701c892c2ee4db0f74c43fb21df292da60ef27`.

## Model contract

The basis is

```text
(s_a, px_a, py_a, pz_a, s*_a, s_c, px_c, py_c, pz_c, s*_c)
```

where `a` and `c` denote the anion and cation sublattices. The model returns a
read-only `10 x 10` complex Hermitian matrix in eV. Its dimensionless Cartesian
wavevector is defined by

```text
k = (2*pi/a_L) q.
```

The excited-state `s*`--`s*` transfer is structurally zero, as specified by the
model; it is not a fourteenth Table 1 parameter.

## Paper-to-code reading order

For a direct crosswalk from Vogl et al. to the implementation, read:

1. `Vogl1983BasisIndex` for the published anion-then-cation basis;
2. `Vogl1983StructureFactors` for the named equation (6) values
   $(g_0,g_1,g_2,g_3)$;
3. `Vogl1983HamiltonianBlocks` for the named $D_a$, $T(\mathbf{k})$, and $D_c$
   blocks and the published orbital-row and orbital-column pattern; and
4. `Vogl1983LcaoSp3sStarModel` for compound selection, block construction,
   assembly, and diagonalization.

[`source-audit.md`](source-audit.md) maps every Table 1 symbol to its Python
field and records the exact source and transcription boundary.

## Use

From this directory:

```python
from pathlib import Path

from vogl1983_lcao_sp3sstar import Vogl1983LcaoSp3sStarModel, Vogl1983Table1

table = Vogl1983Table1.from_json(Path("table1.json"))
silicon = Vogl1983LcaoSp3sStarModel.from_table(table, "Si")
energies_ev = silicon.band_energies((0.0, 0.0, 0.0))
```

The control can test basis ordering, phase conventions, Hermiticity,
reciprocal periodicity, band ordering, and later reduction machinery. It does
not establish QE/Wannier agreement, convergence, model adequacy, or material
validation.

## Source

P. Vogl, H. P. Hjalmarson, and J. D. Dow, “A semi-empirical tight-binding
theory of the electronic structure of semiconductors,” *Journal of Physics and
Chemistry of Solids* **44** (1983), 365--378,
[doi:10.1016/0022-3697(83)90064-1](https://doi.org/10.1016/0022-3697(83)90064-1).

See [source-audit.md](source-audit.md) for the inspected source and transcription
identities.
