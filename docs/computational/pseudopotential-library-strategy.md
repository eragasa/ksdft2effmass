# Pseudopotential Library Strategy

## Purpose

Historical tutorial reproduction and production pseudopotential selection are
separate decisions. A file retained to reproduce an upstream example does not
become a production project input by inheritance.

## Tutorial reproduction

The active Quantum ESPRESSO `PW/examples/example01` silicon SCF reproduction
uses exactly `Si.pz-vbc.UPF` obtained from:

<https://pseudopotentials.quantum-espresso.org/upf_files/Si.pz-vbc.UPF>

The selected bytes have SHA-256
`e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217`
and a size of 74,552 bytes. The UPF declares silicon, a norm-conserving
pseudopotential, the Perdew–Zunger local-density approximation, and a
nonrelativistic treatment. This legacy Quantum ESPRESSO example dependency is
retained only to reproduce the official silicon reference calculation. It must
not silently become the production pseudopotential for `ksdft2effmass`.

The compact acquisition and execution provenance is recorded with the
[Davidson SCF tutorial result](../../calculations/bulk-silicon/qe-example01-si-scf-davidson/execution-provenance.json).

## Production calculations

**Status:** deferred pending tutorial completion and a separate
scientific/numerical decision.

Production bulk-silicon and impurity calculations must later select one
coherent, pinned pseudopotential family. The preferred candidate for evaluation
is a specific release of the Standard Solid-State Pseudopotentials (SSSP)
library, comparing at least SSSP Efficiency and SSSP Precision.

Before production use, a human decision must fix:

- the SSSP release and version;
- the Efficiency or Precision protocol;
- the exchange-correlation functional;
- the Si, P, and B pseudopotential identities;
- recommended wavefunction and charge-density cutoffs;
- relativistic treatment;
- source URLs, file sizes, and SHA-256 identities;
- licensing and citation metadata;
- compatibility with the selected Quantum ESPRESSO version; and
- any convergence study required before production use.

Tutorial results obtained with `Si.pz-vbc.UPF` must not be assumed comparable
with results obtained from an SSSP pseudopotential. Changing a pseudopotential
changes the represented Hamiltonian and may change total energies, band
energies, equilibrium geometry, cutoff requirements, convergence behavior, and
scientifically meaningful comparison boundaries.

Selection must occur before production convergence studies, bulk-silicon
reference calculations, or doped-system comparisons. A future Task should be
created only when production pseudopotential evaluation is ready to begin; this
note creates neither a Task nor a checkpoint.

## External storage and repository provenance

A suitable external layout is:

```text
/Users/eugene/projects/pseudopotentials/
├── qe-legacy-examples/
│   └── Si.pz-vbc.UPF
└── sssp/
    ├── efficiency/
    └── precision/
```

Complete pseudopotential libraries must remain outside Git. The repository
should retain only compact provenance: library name and version, source URL,
selected filenames, SHA-256 identities, relevant metadata, citations, external
storage location, and acquisition or reproduction instructions.

This policy does not authorize SSSP download, pseudopotential installation or
substitution, production calculation, convergence testing, dependency changes,
schema or database changes, CPN work, or successor activation.
