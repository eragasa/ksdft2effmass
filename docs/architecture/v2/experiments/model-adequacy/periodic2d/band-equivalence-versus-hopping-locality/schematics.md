# Schematics

```mermaid
flowchart TD
    P[Kronecker cell-orbital parent<br/>C^N tensor C^N tensor C^4]
    P -->|Centered tensor Fourier transform| B[Direct sum of four-state Bloch fibers]
    B -->|Complete spectra and qualified periodic frame| H[Retained rank-two Bloch Hamiltonian]
    H --> REF[Reference field]
    H -->|Full momentum-dependent gauge U(q)| CMP[Band-equivalent comparison field]
    REF -->|Inverse tensor Fourier transform| HR[Reference Wannier/TB blocks]
    CMP -->|Inverse tensor Fourier transform| HC[Comparison Wannier/TB blocks]
    HR --> COV[Covariant nonlocal alignment check]
    HC --> COV
    HR --> GLO[Cell-local global SO(2) residual]
    HC --> GLO
    GLO --> NYQ[Two-line Nyquist conversion]
    NYQ --> SH[Complete square-orbit truncations]
    SH --> EV[Disjoint-mesh evaluation]
    EV --> OUT[First-passing shell and block-count inflation]
```

Parent--retained reconstruction, covariant representation, restricted alignment,
conversion, interpolation, truncation, and total consequences remain separate. An
eigenvalue array never enters a Hamiltonian subtraction.
