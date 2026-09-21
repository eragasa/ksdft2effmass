# Pseudopotential library strategy

## Current decision

The authoritative decision is
[`DFT Pseudopotential Library Specification v1`](../../specification/dft-pseudopotential-library/v1/index.md).
It accepts the following future production branches:

- PseudoDojo ONCVPSP v0.5, PBE, scalar-relativistic, stringent table for the
  common B/Si/P baseline;
- PSP8 native representations for ABINIT and UPF2 native representations for
  Quantum ESPRESSO, related by one source-entry identity but independently hashed;
- PseudoDojo ONCVPSP v0.4, PBE, fully relativistic, stringent table with matched Si
  and B entries for final B:Si spin-orbit calculations; and
- SSSP PBE Precision v2.0 only as a separately authorized QE-specific comparison,
  not as the common ABINIT/QE baseline.

This decision supersedes the future-production selection of the older PseudoDojo
v0.4.1 standard-table Si branch. It does not change the identity or interpretation of
historical calculations that already used that artifact.

Exact selected B, Si, and P files have not yet been acquired into the new library.
Their complete native-file SHA-256 identities, sizes, embedded metadata, and exact
source URLs remain pending. A source-table label or database row is not a substitute
for those identities.

## Adversarial safeguards

The storage and catalog design assumes that metadata can be wrong, aliases can drift,
and nominally matched formats can produce backend-specific behavior. It therefore:

- stores native payloads by complete uncompressed SHA-256 rather than filename;
- keeps payloads outside SQLite and outside Git;
- permits no authoritative `latest` or `current` alias;
- distinguishes a PseudoDojo source entry from each PSP8, UPF2, or other file;
- verifies size and complete SHA-256 before catalog insertion;
- treats calculator views as non-authoritative;
- requires current-byte verification again before run staging;
- does not infer PSP8/UPF2 numerical equivalence from common provenance; and
- does not inherit cutoff or observable convergence across a pseudopotential change.

The PseudoDojo low, normal, and high hints remain starting guidance. For the common
scalar B/Si/P branch, B currently supplies the largest hints: 38 Ha/76 Ry normal and
44 Ha/88 Ry high. These are not calculated project convergence results.

## External storage

The accepted local root is explicit and is never inferred from an ambient home
directory:

```text
/Users/eugene/opt/pseudopotentials/
├── artifacts/sha256/<first-two-hex>/<complete-digest>/<filename>
├── manifests/sets/<immutable-set-identity>.json
├── catalog/pseudopotentials-v1.sqlite3
├── views/
│   ├── quantumespresso/
│   └── abinit/
└── incoming/
```

`artifacts/` is the authoritative local byte store. `manifests/` retains compact set
composition and source provenance. `catalog/` is a typed local inventory. `views/`
provides optional backend-oriented names but no independent identity. `incoming/` is
mutable acquisition staging and is never a scientific input by location alone.

Each scientific run copies verified artifacts into its isolated workspace and records
source entry, native format, complete SHA-256, byte size, and staged path. Runs do not
consume source-tree pseudopotential directories, `incoming/`, or mutable aliases.

## Software boundaries

- `ksdft2effmass.simulations.dft` owns generic source entries, native artifact
  metadata, content-addressed paths, schema-v1 catalog behavior, and local-byte
  verification.
- `ksdft2effmass.simulations.quantumespresso` owns UPF2 admission into QE simulation
  composition.
- `ksdft2effmass.simulations.abinit` owns PSP8 admission into ABINIT simulation
  composition.
- Integration packages continue to own native parser, input, and process mechanics.
- Scientific specifications own family selection and convergence meaning.

The root `ksdft2effmass.simulations` package intentionally re-exports none of these
contracts; callers use one explicit domain route.

## Tutorial reproduction remains separate

The Quantum ESPRESSO `PW/examples/example01` silicon reproduction uses exactly the
legacy `Si.pz-vbc.UPF` obtained from:

<https://pseudopotentials.quantum-espresso.org/upf_files/Si.pz-vbc.UPF>

Its SHA-256 is
`e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217`
and its size is 74,552 bytes. It declares a norm-conserving, nonrelativistic
Perdew--Zunger LDA silicon pseudopotential. It remains an identified tutorial
artifact and must not become a production input by inheritance.

Likewise, the completed paired ABINIT tutorial used a separately identified
PseudoDojo PW-LDA PSP8 artifact. Tutorial pairing established workflow shape, not a
common pseudopotential parent or cross-backend numerical comparison.

## Acquisition and execution boundary

The empty layout and database authorize no download, decompression, conversion,
calculator invocation, convergence study, or production claim. A bounded acquisition
operation must verify source responses, compressed and uncompressed identities,
embedded metadata, native-format pairing, and atomic installation before catalog
recording. Any calculator smoke test or scientific comparison remains protected
execution requiring its own preflight and authorization.
