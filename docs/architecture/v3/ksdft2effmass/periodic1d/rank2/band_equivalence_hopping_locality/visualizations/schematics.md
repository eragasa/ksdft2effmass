# Schematic

```mermaid
flowchart TD
    A[authoritative analysis or calculation aggregate] --> P[retention-owned typed projection]
    B[canonical retained bytes] --> H[source SHA-256]
    H --> P
    P --> D[retention-authenticated projection digest]
    V[stored passing verification] --> G[visualization digest and type gate]
    D --> G
    G --> I{downstream closed plot inventory}
    I --> S[three single-parent PNGs]
    I --> F[three parent-family PNGs]
    I --> C[three refinement and truncation PNGs]
```
