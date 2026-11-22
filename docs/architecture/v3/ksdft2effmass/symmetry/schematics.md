# Symmetry schematics

**Prospective design.** The concepts below are responsibilities, not committed Python
class names, supported imports, schemas, or implemented capabilities.

## Object separation

```text
physical operation / declared group law
                |
                v
identified source and target spaces, bases, metrics and conventions
                |
                v
supplied represented action (linear or explicitly semilinear)
                |
                +--> group-law and metric-preservation checks
                |
                v
selected subspaces and full-column-rank frames
                |
                +--> leakage / invariance diagnostics
                |
                v
qualified induced representation
                |
                +--> operator covariance / intertwiner diagnostics
                |
                v
qualified character data --> isotypic projectors and sector dimensions
```

A geometric operation is not its matrix on electronic states. A represented action is
not automatically a symmetry of a Hamiltonian. A compressed action is not automatically
a representation on the compressed space. Equal dimensions establish none of these
identifications.

## Necessary contracts

| Concept | Required information |
|---|---|
| Operation/group | Explicit identity, composition and inverses; geometric and fractional-translation data when applicable; linearity and any representation factor-system conventions |
| Represented action | Domain/codomain, ordered bases, metric, matrix, action direction, linear/antilinear character and source of the action |
| Reciprocal-space action | Source/target momentum, reciprocal representative and any boundary sewing, Bloch/gauge convention and translation phases |
| Subspace | Ambient identity, selection and frame, induced metric, rank/conditioning information and closure evidence |
| Representation | Qualified action family and declared composition law, not merely a list of square matrices |
| Sector data | Applicable group and representation class, authenticated irreducible characters/dimensions, projector and residual evidence |

Use existing space, operator and PhysKit value contracts where applicable; do not create
a parallel state-space hierarchy. Keep physical operators distinct from their finite
representations, as required by the
[retained-space architecture](../../../v2/ksdft2effmass/periodic/retained-spaces-and-operators.md).
Which concrete types can serve these boundaries remains an implementation-design task;
a future PhysKit core cannot import KSD-owned space or campaign types.

## Native-data boundary

```text
retained native payloads + explicit source bindings
  -> Simulations-owned decoding/extraction
  -> action matrices + metric/phase/basis/space conventions and uncertainty
  -> reusable symmetry mathematics
  -> calculation-owned scientific interpretation and admission
```

Native file existence, a successful parse or a matching checksum does not establish the
physical meaning of an action. The core must not read QE/Wannier files, discover a
replacement source, choose a pseudopotential, or infer a representation from orbital
names. Missing extraction support is distinct from mathematical non-invariance and
from proof that retained data are fundamentally insufficient.

## Outcome separation

Report constructed values and residuals separately from their qualification. Distinguish
invalid or incompatible inputs, unsupported representation classes, unavailable source
actions, resolved leakage, and numerically inconclusive checks. A caller supplies the
scientifically justified uncertainty/tolerance policy; residual size alone is not a
universal acceptance decision. No symmetry result grants calculation authority, passes
a campaign gate, or selects a successor model.

Return to [index](index.md); see [numerics](numerics.md) and [science](science.md).
