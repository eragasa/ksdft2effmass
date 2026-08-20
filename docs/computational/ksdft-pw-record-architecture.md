# Kohn–Sham plane-wave record architecture

## Status and scope

This maintained computational architecture records the selected implementation
for the human-accepted
[`bulk-silicon.records.periodic.extraction`](../../harness/tasks/bulk-silicon.records.periodic.extraction.json)
Task, now closed as `closed_human_accepted_pass`. The accepted claim is limited
to faithful semantic extraction of the retained QE 7.2 QEXSD 23.03.10 silicon
artifact through the documented ownership boundaries. The resulting plane-wave
Kohn--Sham record remains retained software-verification evidence; this status
does not establish production convergence, numerical verification, scientific
validation, uncertainty quantification, or acceptance as a production silicon
dataset.

## Former ownership problem

The former `ksdft2effmass.periodic` package combined QEXSD parsing, periodic
geometry, Kohn–Sham spectra, plane-wave FFT metadata, complete calculation
records, and serialization. It consequently mislabeled quantity-specific values
with the global QEXSD string “Hartree atomic units” and obscured reciprocal and
$k$-point scale conventions.

## Selected package boundaries

```mermaid
flowchart LR
    QE["io.quantum_espresso.qexsd<br/>QEXSD bytes and backend conventions"]
    PERIODIC["periodic<br/>lattices, structures, coordinates, k-points"]
    KSDFT["ksdft<br/>Kohn–Sham semantics"]
    PW["ksdft.pw<br/>plane-wave representation and calculation record"]

    QE -->|"constructs"| PW
    PW --> PERIODIC
    PW --> KSDFT
```

Canonical QEXSD source, native-document, and parser ownership is
`integration.quantumespresso.qexsd`. The historical
`io.quantum_espresso.qexsd` path forwards those objects for schema-version-1
compatibility and still owns the legacy aggregate adapter during migration.
Neither `periodic`, `ksdft`, nor `ksdft.pw` imports a Quantum ESPRESSO or QEXSD
module.

## Mechanical-to-semantic transformation

```text
explicit QEXSD bytes and source identity
→ QexsdDocumentParser
→ mechanically faithful QexsdDocument
→ ConstructQexsdKohnShamPlaneWaveRecord
→ KohnShamPlaneWaveCalculationRecord
```

`QexsdDocument` retains raw values, labels, and ordering. Canonical syntax parsing
and native records belong to `integration.quantumespresso.qexsd`.
`ConstructQexsdKohnShamPlaneWaveRecord` remains a legacy adapter that applies
source-backed backend conventions while the schema-version-1 serializer remains
with `ksdft.pw`. A later integration-adaptation Task owns separated outputs.

## Public-interface relocation

| Removed public interface | Defining replacement |
|---|---|
| `periodic.QexsdSource` | `integration.quantumespresso.qexsd.QexsdSource` |
| `periodic.QexsdDocument` | `integration.quantumespresso.qexsd.QexsdDocument` |
| `periodic.ParseQexsdDocument` | `integration.quantumespresso.qexsd.QexsdDocumentParser` |
| `periodic.PeriodicCalculationRecord` | `ksdft.pw.KohnShamPlaneWaveCalculationRecord` |
| `periodic.ConstructPeriodicCalculationRecord` | `io.quantum_espresso.qexsd.ConstructQexsdKohnShamPlaneWaveRecord` |
| `periodic.PeriodicCalculationRecordJsonSerializer` | `ksdft.pw.KohnShamPlaneWaveCalculationRecordJsonSerializer` |

No duplicate parser or native-record implementation remains. The accepted v1
``io.quantum_espresso.qexsd`` imports forward to the canonical classes, and the
historical ``ParseQexsdDocument`` name is a transitional identity alias for
``QexsdDocumentParser``. The old ``periodic`` imports remain absent.

## Units, dimensions, coordinates, and scales

The model distinguishes the QEXSD unit-system declaration from field-level
physical dimensions and concrete units. Direct vectors and Cartesian atomic
positions have length dimension and unit bohr. Raw reciprocal vectors and raw
Cartesian $k$ points are dimensionless coefficients. Their explicit scale is
`2pi_over_alat`, with `alat` in bohr and `incorporates_two_pi=true`; physical
values have inverse-length dimension and unit bohr$^{-1}$. Eigenvalues and total
energy use hartree. The retained weights are marked `sum_to_two`; unsupported
energy-reference, spin-array, basis, subspace, gauge, and phase conventions are
explicitly unavailable.

## Direct–reciprocal invariant

For source-ordered rows $A$ and $B_{\mathrm{raw}}$, the retained values satisfy
$A B_{\mathrm{raw}}^{\mathsf T}=10.2I$. QE 7.2 writes `bg` as Cartesian
coefficients in units of $2\pi/a_{\mathrm{lat}}`; therefore
$B_{\mathrm{physical}}=(2\pi/a_{\mathrm{lat}})B_{\mathrm{raw}}$ and the model
requires $A B_{\mathrm{physical}}^{\mathsf T}=2\pi I$. The deterministic
criterion is an absolute componentwise residual at most $10^{-12}$.

`ReciprocalLatticeCompatibilityValidator` owns this cross-object criterion.
`ReciprocalLattice` retains only intrinsic reciprocal state and exact raw-to-physical
scaling. The QEXSD construction and plane-wave serializer invoke the validator
explicitly.

## Aggregate Kohn--Sham compatibility

`KohnShamPlaneWaveCalculationRecord` is an immutable aggregate DataObject. Its
intrinsic constructor checks field types, schema version, exit-status range, and the
intrinsic validity already owned by each component. It does not own comparisons
between independently valid components.

`KohnShamPlaneWaveCalculationRecordValidator` owns exact agreement between the
reciprocal-lattice and $k$-point `alat` scales and between the sampled $k$-point count
and spectral row count. QEXSD construction and schema-version-1 serialization and
deserialization invoke this validator before returning or emitting a record. These
checks establish represented software compatibility only; they do not establish
sampling convergence or scientific validity.

## Source provenance ownership

QEXSD owns exact source bytes, path identity, raw labels, and backend
translation. The target record retains generic artifact identity and a concise
auditable transformation description; it does not own QEXSD parsing.

## Explicit non-decisions

This architecture adds no unit algebra, dimensional-analysis engine, protocol,
universal electronic-structure interface, solver abstraction, backend registry,
Architecture v2, telemetry, or repository-context machinery. It does not decide
energy alignment, physical band identity, convergence, validation, or UQ.

The useful design antecedents are pypospack commit
`21cdecaf3b05c87acc532d992be2c04d85bfbc22` and physkit commit
`bd5f657348acef131efe0e1618a5eb1641dfb893`: scale separated from dimensionless
shape, distinct direct and reciprocal lattices, $B=2\pi A^{-\mathsf T}$, and
quantity-specific units. Their mutable state, implicit units, filesystem-driven
simulation state, and incompletely typed arrays are not adopted.

## Migration status and links

The pre-acceptance interface and schema were replaced directly. Maintained
consumers use the new imports and retained identities:

- [retained record](../../calculations/bulk-silicon/qe-example01-si-scf-davidson/ksdft-plane-wave-calculation-record.json)
- [schema](../../specification/ksdft-plane-wave-calculation-record/v1/ksdft-plane-wave-calculation-record.schema.json)
- [API documentation](../api/periodic-records.rst)
- [v2 field disposition](../architecture/migration/v1-to-v2/implementation/ksdft-plane-wave-disposition.md)
- [concept documentation](../concepts/periodic-calculation-records.rst)
- [computational index](ksdft2effmass.computational.00.md)
