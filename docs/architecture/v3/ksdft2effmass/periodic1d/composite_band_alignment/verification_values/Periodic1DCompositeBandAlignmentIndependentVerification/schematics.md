# Schematic

```mermaid
flowchart LR
    O[operation names] --> M[immutable comparison mapping]
    C[maximum-error comparisons] --> M
    M --> R[per-operation pass results]
```
