# Isotropic 2-D schematics

## Scientific flow

The experiment projects one retained finite parent into a square-symmetric target and
compares nested candidate classes in one maximal space.

- Projection occurs before class reduction.
- Both channels consume the same target and coordinates.
- Evaluation occurs after decisive evidence is fixed.

```mermaid
flowchart LR
    source["retained scalar 2-D parent"] --> checks["Hermiticity and D4 checks"]
    checks --> target["exact real orbit target"]
    target --> spectral["spectral channel"]
    target --> operator["operator channel"]
    hierarchy["nested support masks"] --> spectral
    hierarchy --> operator
    spectral --> evidence["witness / lower bound / unresolved"]
    operator --> evidence
    evidence --> evaluation["evaluation / withheld / locality diagnostics"]
```

## Implementation flow

The package mirrors the existing periodic-1D experiments. There is no nested
`experiment/` or `execution/` source package.

- `definition.py` owns the immutable definition.
- `experiment.py` owns the in-process Action.
- `results.py` owns immutable result records.
- `verify.py` independently reconstructs decisive evidence without calling the Action.
- `serialization.py` transports rather than interprets input, result, and verification documents.

```mermaid
flowchart TB
    document["strict input document"] --> decoder["serialization.py decoder"]
    decoder --> definition["HoppingShellHierarchyDefinition"]
    definition --> action["HoppingShellHierarchyExperiment.execute"]
    action --> result["HoppingShellHierarchyResult"]
    definition --> verifier["HoppingShellHierarchyResultVerifier"]
    result --> verifier
    result --> encoder["serialization.py encoder"]
    verifier --> verification["bounded verification result"]
```
