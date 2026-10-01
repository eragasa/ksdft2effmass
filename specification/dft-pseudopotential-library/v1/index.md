# DFT Pseudopotential Library Specification v1

## Status and authority

**Status:** Accepted human scientific and public-contract decision

**Accepted:** 2026-09-21

**Scope:** pseudopotential family selection, external storage, compact metadata
catalog, and native ABINIT/Quantum ESPRESSO representation boundaries

This specification records the human acceptance of the current PseudoDojo
recommendation. It supersedes only the pseudopotential-family, source-table, release,
and future-artifact-selection provisions of
[`PhysicalSpecification-v1`](../../ksdft2Effmass.physical-specification.v1.md) and
[`NumericalSpecification-v1`](../../ksdft2Effmass.numerical-specification.v1.md).
Those documents continue to govern their unaffected physical and numerical decisions.
Their previously pinned PseudoDojo v0.4.1 Si UPF remains the exact identity of the
historical calculations that used it; this decision does not relabel those bytes or
results as v0.5/stringent evidence.

The accepted decision selects source-library branches. Exact B, Si, and P native-file
URLs, compressed and uncompressed sizes, and SHA-256 identities remain pending local
acquisition and verification. No artifact is accepted merely from a filename, table
label, database row, or successful calculator exit.

## Adversarial assessment incorporated into the decision

The following challenges were applied before defining the storage and software
contract:

1. **There is no universally best pseudopotential.** “Best” is conditional on the
   exchange-correlation approximation, relativistic branch, target observable,
   cutoff, and calculator implementation. The decision therefore fixes explicit
   branches and still requires observable-specific convergence.
2. **A library entry is not a file identity.** PseudoDojo PSP8 and UPF2 files may
   derive from one selected source entry but have different bytes and parser paths.
   They receive independent complete SHA-256 identities. A shared source-entry ID is
   not evidence of identical finite Hamiltonians.
3. **A database can amplify bad metadata.** Catalog insertion therefore requires an
   already-local regular file at its content-addressed path and checks byte size and
   complete SHA-256 before recording it. The database stores no payload blob and does
   not select a scientific branch.
4. **Mutable aliases undermine provenance.** The authoritative hierarchy contains no
   `latest` or `current` directory. Human-friendly calculator views are explicitly
   non-authoritative.
5. **Format convenience can erase backend differences.** ABINIT composition uses the
   selected PSP8 representation; Quantum ESPRESSO composition uses the selected UPF2
   representation. ABINIT's ability to parse some UPF files does not replace this
   native paired-representation decision.
6. **Changing the family invalidates inherited convergence.** Earlier cutoff,
   geometry, band, or effective-mass observations made with the v0.4.1 or legacy QE
   files remain observations of those parent models. They cannot establish convergence
   for the v0.5/stringent branch.
7. **The scalar branch is insufficient for final B acceptor claims.** The scalar
   B/Si/P family is the common baseline, while final B:Si SOC work uses a separately
   identified fully relativistic family with a matching fully relativistic Si host.
8. **The source site's standard and stringent table metadata are not hashes.** The
   current B, Si, and P scalar tables report equal cutoff/test metadata, but the
   selected stringent files must still be acquired and independently identified.

## Accepted scientific branches

| Use | Family and release | XC | Relativity | Accuracy table | ABINIT | Quantum ESPRESSO |
|---|---|---|---|---|---|---|
| Primary common B/Si/P baseline | PseudoDojo ONCVPSP v0.5 | PBE | Scalar-relativistic | Stringent | PSP8 | UPF2 |
| Final B:Si acceptor/SOC branch | PseudoDojo ONCVPSP v0.4 | PBE | Fully relativistic | Stringent | PSP8 | UPF2 |
| QE-only comparison, when separately authorized | SSSP v2.0 Precision | PBE | Per selected SSSP entry | Precision | Not the common baseline | Native SSSP UPF |

The scalar branch uses norm-conserving B $2s^2 2p^1$, Si $3s^2 3p^2$, and P
$3s^2 3p^3$ source entries. The fully relativistic branch must use compatible
fully relativistic Si and B entries; a scalar host must not be subtracted from or
presented as aligned with a fully relativistic doped operator.

PseudoDojo currently identifies v0.5 as its scalar-relativistic PBE release and offers
both PSP8 and UPF formats. Its site notes that the v0.5 element updates are PBE-only;
LDA and PBEsol work therefore remains on v0.4.1 unless a later accepted specification
changes that boundary. ABINIT's official pseudopotential page recommends PseudoDojo
norm-conserving sets. Quantum ESPRESSO's pseudopotential guidance lists PseudoDojo and
SSSP; SSSP is retained only as a QE-specific comparator because its curated table may
mix source families and pseudopotential formalisms.

## Source cutoff hints and convergence boundary

The PseudoDojo v0.5 PBE scalar-relativistic tables currently report:

| Element | Low | Normal | High |
|---|---:|---:|---:|
| B | 34 Ha | 38 Ha | 44 Ha |
| Si | 14 Ha | 18 Ha | 24 Ha |
| P | 18 Ha | 22 Ha | 28 Ha |

For a mixed scalar B/Si/P calculation, B supplies the largest current hint:
38 Ha (76 Ry) normal and 44 Ha (88 Ry) high. These are source-library starting
points, not calculated project results or final settings. Wavefunction and
charge-density cutoffs must be converged for the declared observable and fixed
pseudopotential identities. Parent-model, numerical/discretization, and
model-reduction errors remain separate.

## External filesystem layout

Callers supply one explicit absolute root. The accepted local root is:

```text
/Users/eugene/opt/pseudopotentials/
├── artifacts/
│   └── sha256/
│       └── <first-two-hex>/
│           └── <complete-64-hex-digest>/
│               └── <original-native-filename>
├── manifests/
│   └── sets/
│       └── <immutable-set-identity>.json
├── catalog/
│   └── pseudopotentials-v1.sqlite3
├── views/
│   ├── quantumespresso/
│   └── abinit/
└── incoming/
```

The content-addressed artifact path and complete digest are authoritative for local
bytes. Set manifests contain compact identities and citations. Calculator views are
non-authoritative convenience surfaces and must resolve to cataloged artifacts before
run staging. `incoming/` is mutable staging; nothing there is accepted or available to
scientific runs by location alone.

Each calculation copies the verified exact file into its isolated run workspace and
records the source-entry identity, native format, filename, complete SHA-256, byte
size, and staged path. Calculations do not point directly to source-tree pseudo
directories, the mutable incoming area, or an unverified calculator view.

## Catalog schema v1

The SQLite database is a compact local metadata catalog, not a scientific-results
database and not a payload store. Schema v1 has:

- `catalog_metadata`: exact schema version;
- `source_entries`: family, release, XC, table tier, element, formalism,
  relativistic treatment, valence count, and optional Hartree cutoff hints; and
- `artifacts`: complete uncompressed SHA-256, source-entry foreign key, native
  format, original basename, byte size, HTTPS source URL, and canonical path relative
  to the library root.

The catalog allows one artifact for each source-entry/native-format pair. Public
recording is insert-only and idempotent for an exact repetition. Conflicting source
metadata, digest metadata, or source-entry/format pairs are rejected. Public
resolution reconstructs typed immutable records but deliberately does not imply that
current local bytes still match; current-byte verification is a separate operation.

Schema conformance, a digest match, a shared source-entry identity, backend format
admission, and successful execution establish only their respective software or
provenance facts. None establishes cross-format numerical agreement, production
convergence, scientific validation, uncertainty quantification, or authorization to
run a calculator.

## Software ownership

| Surface | Owner |
|---|---|
| Generic source entries, artifact identities, layout, catalog, and byte verification | `ksdft2effmass.simulations.dft` |
| UPF2 admission and QE-native composition reference | `ksdft2effmass.simulations.quantumespresso` |
| PSP8 admission and ABINIT-native composition reference | `ksdft2effmass.simulations.abinit` |
| Native parser and process mechanics | Applicable integration package |
| Scientific selection and convergence | This or a later accepted specification plus retained calculation evidence |

`ksdft2effmass.simulations` is not a convenience re-export namespace. Supported
imports are curated at the explicit `simulations.dft`,
`simulations.quantumespresso`, and `simulations.abinit` boundaries.

## Deferred work

This decision and schema do not download, decompress, copy, convert, or publish any
pseudopotential artifact. A later bounded acquisition operation must retain source
responses, distinguish compressed and uncompressed identities, inspect embedded
metadata, install by atomic promotion, produce set manifests, and record exact B, Si,
and P artifact identities. Calculator smoke tests and cross-format numerical
comparisons require separate execution preflights and authorization.
