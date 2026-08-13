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

**Status:** the accepted v1 physical and numerical specifications freeze the
PBE/PseudoDojo standard-table ONCV bulk-Si branch and exact Si artifact
metadata. The complete authority/provenance confirmation boundary is planned by
[`bulk-silicon.production-reference.pseudopotential-selection`](../../harness/tasks/bulk-silicon.production-reference.pseudopotential-selection.json)
and documented in the
[bulk-silicon production program](bulk-silicon-production-program.md). That Task
is blocked under its inactive parent.

The earlier preference recorded here for evaluating SSSP Efficiency and
Precision is not current production authority and does not override
[`PhysicalSpecification-v1`](../../specification/ksdft2Effmass.physical-specification.v1.md)
or
[`NumericalSpecification-v1`](../../specification/ksdft2Effmass.numerical-specification.v1.md).
A no-download candidate-family metadata comparison is non-authoritative and may
only identify whether a separately authorized revision of those owning
specifications should be considered. It cannot select, substitute, or override
the frozen pseudopotential.

Before production use, the authoritative branch must explicitly fix or confirm:

- the exchange-correlation functional and pseudopotential family/release;
- NC, ultrasoft, or PAW form and applicable charge-density cutoff behavior;
- scalar-relativistic or fully relativistic treatment;
- Si valence configuration and nonlinear-core-correction status;
- exact source URL, filename, size, SHA-256 identity, license, and citations;
- compatibility with the selected Quantum ESPRESSO and Wannier90 interface;
- later compatible P and B family requirements without silently selecting their
  branch-specific artifacts; and
- the production convergence studies required by the accepted numerical
  specification.

Tutorial results obtained with `Si.pz-vbc.UPF` must not be assumed comparable
with results obtained from an SSSP pseudopotential. Changing a pseudopotential
changes the represented Hamiltonian and may change total energies, band
energies, equilibrium geometry, cutoff requirements, convergence behavior, and
scientifically meaningful comparison boundaries.

Authority/provenance confirmation must complete before production convergence
studies, bulk-silicon reference calculations, or doped-system comparisons. The
planned Task creates no checkpoint, is blocked under an inactive parent, and
authorizes no download, installation, comparison calculation, selection, or
substitution.

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
