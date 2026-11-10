# Diamond Slater--Koster implementation boundary

## Source layout

- `geometry.py` owns the concrete FCC primitive cell, descriptive diamond-center
  identifiers, shell representatives, and their composition into PhysKit spatial-basis
  and directed-bond records.
- `parameters.py` owns KSD's concrete onsite and first-/second-neighbor grouping,
  stable fifteen-value order, electron-volt admission, and composition into PhysKit
  seven-channel integral records. The omitted first-neighbor channels are supplied as
  explicit zeros rather than inferred.
- `model.py` owns the KSD model definition, onsite block, shell inventory, represented
  basis correlation, and evaluation wrapper. It delegates two-center construction,
  generated Hermitian reverses, ordinary-cell assembly, cell-gauge Bloch evaluation,
  and orbital-center gauge construction directly to PhysKit.
- `serialization.py` owns the concrete model-definition wire and records the PhysKit
  mechanics owner without serializing a fit or scientific disposition.

The public records and model are frozen, slotted, and keyword-only. Public numeric
boundaries reject booleans, numeric strings, wrong shapes, and nonfinite values.

## Dependency direction

```text
KSD diamond geometry and shell policy
KSD concrete parameter grouping and onsite terms
KSD represented-basis and wire correlation
                    |
                    v
Project Koios PhysKit Slater--Koster mechanics
Project Koios PhysKit block-hopping Bloch evaluation
Project Koios PhysKit orbital-center gauge construction
```

The reusable layer does not import KSD. KSD does not retain copied reusable hopping or
assembly implementations. The `calculations/` predecessor is not an import provider,
compatibility package, or fallback path.

## Deliberate exclusions

The implementation does not own fitting, residual construction, sample selection,
weighting, alignment admission, evidence interpretation, model selection, or
scientific acceptance. It does not add heteropolar bonds, spin, spin--orbit coupling,
$f$ orbitals, overlap matrices, or generalized eigenproblems.
