# Periodic scientific-model hierarchy

## Represented meaning

The scientific hierarchy classifies physical and mathematical periodic models. It is
separate from campaign execution, finite represented operators, serialized campaign
documents, and retained calculation results. In particular, nominal model membership
does not establish that two finite matrices act on compatible state spaces.

The target hierarchy is closed and nominal so missing or malformed inheritance cannot
be accepted through structural coincidence:

```text
PeriodicModel
├── Periodic1DModel
│   ├── concrete parent models
│   └── Periodic1DDefectModel
├── Periodic2DModel
│   ├── concrete parent models, including GrapheneReferenceModel
│   └── Periodic2DDefectModel
└── Periodic3DModel
    ├── concrete parent models, including SiliconReferenceModel
    └── Periodic3DDefectModel
```

The foundation classes in this tree are implemented and publicly exported from
`ksdft2effmass.periodic`. `PeriodicModelRole` supplies the exact `TOY` and
`MATERIAL_REFERENCE` values. Concrete graphene, silicon, and migrated toy-model classes
remain proposed work; the foundation does not authorize empty concrete placeholders.

## Dimensional identity

Every concrete periodic model inherits one exact built-in spatial dimension from the
`Periodic1DModel`, `Periodic2DModel`, or `Periodic3DModel` branch. The final dimension
property and runtime subclass check reject attempts to replace that identity. Booleans,
numeric strings, NumPy scalar substitutes, and other coercible values are not valid
dimensions.

Dimensional membership describes the modeled periodic coordinates. It does not imply
that equal-dimensional models share lattice geometry, basis ordering, Hilbert space,
energy reference, units, gauge, boundary conditions, discretization, or reduction
method.

## Parent and defect models

A dimension-specific defect model is also a model in that same dimensional family.
It implements the required `parent_model_id` property and represents the additional
state needed to define the defect. Applicable records must make geometry, unit,
energy-reference, and represented-space alignment prerequisites explicit.

A defect label alone never authorizes operator subtraction. Pristine and defect
operators may be differenced only after an owning compatibility or alignment Action
establishes a common state space and conventions.

## Toy and material-reference roles

Toy versus material-reference status is orthogonal to dimension and defect status.
It is an exact closed model-role value rather than a second inheritance lattice. This
avoids multiple-inheritance combinations such as separate toy-defect base classes for
every dimension.

- A **toy model** is a controlled model used to isolate mathematical, numerical, or
  software behavior. Its results are not material evidence.
- A **material-reference model** represents an explicitly specified material model.
  The label does not imply experimental truth, scientific validation, or complete
  many-body excitation physics.

Graphene is the target two-dimensional material-reference family. Bulk silicon is the
target three-dimensional material-reference family. Their physical assumptions,
structures, Hamiltonians, numerical settings, and validation evidence require
separate authoritative specifications and research documentation.

## Dependency boundary

The model hierarchy may depend on approved reusable geometry, units, quantities, and
model-intrinsic records. Reusable lattice mathematics remains in Project Koios PhysKit
where its accepted contract applies. Ksdft-specific material identity, reduction
policy, provenance, and comparison prerequisites remain in this repository.

Scientific model modules must not import campaign packages, calculation scripts,
retained result serializers, campaign tolerances, or campaign acceptance decisions.
