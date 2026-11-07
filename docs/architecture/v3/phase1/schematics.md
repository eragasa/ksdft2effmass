# Phase 1 schematics

## Layering

```mermaid
flowchart TD
    records["existing operator metadata"] --> representations["operators.representations"]
    numerics["Project Koios Numerics"] --> representations
    representations --> transformations["operators.transformations"]
    transformations --> future["future operation-specific Actions"]

    future -. "not implemented in Phase 1" .-> evidence["evidence and decisions"]
```

## Object separation

```mermaid
flowchart LR
    operator["mathematical operator"] -. "represented by" .-> node["finite representation identity + field"]
    source["source representation identity"] --> edge["TransformationIdentity"]
    target["target representation identity"] --> edge
    edge -. "does not prove execution" .-> action["future transformation Action"]
```

## Documentation descent

```mermaid
flowchart TD
    phase["Phase 1 overview"] --> source["src mirror"]
    source --> package["package contract"]
    package --> module["module contract"]
    module --> type["public-type contract"]
```

Package-level schematics:

- [representations](../src/ksdft2effmass/operators/representations/schematics.md);
- [transformations](../src/ksdft2effmass/operators/transformations/schematics.md).
