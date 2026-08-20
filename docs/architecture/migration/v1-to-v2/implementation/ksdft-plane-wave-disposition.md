# Plane-wave record field disposition

## Status and identity

This page records the deterministic field-by-field owner disposition for
`migration.v2.ksdft.plane-wave-disposition`. It uses the completed periodic and
Kohn--Sham contract results and the accepted v2 package ownership boundaries.

The schema-version-1 aggregate, serializer, retained JSON, and current public
imports remain compatibility surfaces until all consumers cut over. This result
does not define a v2 wire, accept a neutral plane-wave representation contract,
or authorize implementation in downstream owner packages.

## Aggregate disposition

| Current field | Retain now | Future owner or disposition | Cutover consequence |
|---|---|---|---|
| `schema_version` | `ksdft.pw` schema-v1 wire | No domain owner | Legacy adapter consumes it; separated values do not copy it. |
| `structure` | Aggregate reference | `periodic` | Adapter emits or reuses `PeriodicStructure`. |
| `reciprocal_lattice` | Aggregate reference | `periodic` | Adapter emits or reuses `ReciprocalLattice`; compatibility stays explicit. |
| `k_point_sampling` | Aggregate reference | `periodic` | Adapter emits or reuses `KPointSampling`. |
| `spectrum` | Aggregate reference | `ksdft` | Adapter emits or reuses `KohnShamSpectralObservations`. |
| `total_energy` | Aggregate reference | `ksdft` | Adapter emits or reuses `TotalEnergyObservation`. |
| `plane_wave` | Entire v1 object | `integration.quantumespresso` extracted/native result | Do not move the current class wholesale into neutral `ksdft`. |
| `provenance` | Entire v1 object | Split among Workflow artifact provenance, calculator identity, and integration adaptation | Do not copy the class directly into a v2 manifest. |
| `exit_status` | Aggregate field | `calculators.ProcessObservation` | Integration correlates it with calculator output/process evidence. |

`KohnShamPlaneWaveCalculationRecord` remains only as the schema-v1 compatibility
aggregate and retires after every consumer migrates. Its validator remains at
legacy construction and serialization boundaries during cutover. Future QEXSD
adaptation owns admission across separated owner outputs without creating a
permanent `ksdft -> periodic` dependency.

## Plane-wave metadata disposition

No current `PlaneWaveRepresentationMetadata` field is representation-neutral
under the accepted v2 `ksdft` contract.

| Field | Future owner | Required preservation | Deferred choice |
|---|---|---|---|
| `representation` | `integration.quantumespresso` extracted-result discriminator | Preserve `plane_wave` for legacy adaptation. | Neutral representation taxonomy. |
| `fft_grid` | Integration-native QEXSD observation | Preserve positive triplet and source meaning. | Cross-backend normalized FFT semantics. |
| `fft_smooth` | Integration-native QEXSD observation | Preserve its distinction from `fft_grid`. | Compatible concepts in other backends. |
| `fft_box` | Integration-native QEXSD observation | Preserve its QEXSD meaning. | Compatible concepts in other backends. |
| `basis_identity` | Integration extraction availability | Preserve `not_represented`; invent no identity. | Neutral basis-identity contract. |
| `retained_subspace` | Integration extraction availability | Preserve `no_retained_subspace`. | Future reduced-subspace contract. |
| `gauge` | Integration extraction availability | Preserve `not_represented`. | Neutral gauge contract. |
| `phase_convention` | Integration extraction availability | Preserve `not_represented`. | Neutral phase-convention contract. |

## Provenance disposition

The current `ArtifactProvenance` object is insufficient for a closed v2 producer
variant: it lacks an artifact identity, explicit checksum algorithm,
provenance-variant identity/version, evidence and claim-boundary identities, and
producer-attempt correlation. Migration must not fabricate them.

| Field | Future owner | Cutover rule | Deferred choice |
|---|---|---|---|
| `source_path` | Integration source resolver; optional Workflow portable reference | Keep the absolute path local; never place it in a portable manifest. | Portable native-output reference. |
| `source_sha256` | Workflow content identity/manifest | Represent algorithm=`SHA-256` and digest explicitly and verify bytes. | Algorithm-agility contract. |
| `source_byte_count` | Workflow artifact manifest | Preserve exact count and correlate with observed bytes. | None. |
| `source_format` | Workflow native/media-format identity interpreted by integration | Preserve `QEXSD`; integration selects the parser. | Exact format identity wire. |
| `source_format_version` | Integration QEXSD contract, optionally referenced by manifest | Preserve exact version; do not treat it as application version. | Version identity wire. |
| `producing_application` | Calculator executable identity or Workflow producer evidence | A string alone does not establish represented lineage. | Retained-artifact producer variant. |
| `producing_application_version` | Same split as `producing_application` | Preserve known value or explicit absence; do not infer. | Same producer variant. |
| `transformation` | Identified integration adaptation policy referenced by Workflow lineage | Preserve legacy text as history; replace authority with a versioned policy identity when defined. | Adaptation-policy identity and wire. |

## Schema-version-1 field inventory

Every schema-v1 field remains accepted through the compatibility serializer only.
The root grouping fields and `schema_version` have no permanent domain owner.

### Periodic geometry and sampling

| Schema path | Future owner | Preservation rule |
|---|---|---|
| `structure.direct_lattice.vectors` | `periodic` | Preserve order and values. |
| `structure.direct_lattice.unit_system` | `periodic` | Preserve `hartree_atomic`. |
| `structure.direct_lattice.dimension` | `periodic` | Preserve `length`. |
| `structure.direct_lattice.unit` | `periodic` | Preserve `bohr`. |
| `structure.direct_lattice.coordinate_convention` | `periodic` | Preserve `cartesian`. |
| `structure.direct_lattice.vector_order` | `periodic` | Preserve explicit ordering. |
| `structure.species[].name` | `periodic` | Preserve species identifier. |
| `structure.species[].mass` | `periodic` | Preserve numeric value. |
| `structure.species[].mass_dimension` | `periodic` | Preserve `mass`. |
| `structure.species[].mass_unit` | `periodic` | Preserve explicit unit. |
| `structure.species[].pseudopotential_label` | `periodic` | Preserve represented label; it proves no artifact equivalence. |
| `structure.sites[].index` | `periodic` | Preserve one-based source order. |
| `structure.sites[].species_name` | `periodic` | Preserve reference. |
| `structure.sites[].coordinates` | `periodic` | Preserve values. |
| `structure.sites[].coordinate_convention` | `periodic` | Preserve `cartesian`. |
| `structure.sites[].coordinate_dimension` | `periodic` | Preserve `length`. |
| `structure.sites[].coordinate_unit` | `periodic` | Preserve `bohr`. |
| `reciprocal_lattice.raw_coefficients` | `periodic` | Preserve source order. |
| `reciprocal_lattice.raw_dimension` | `periodic` | Preserve `dimensionless`. |
| `reciprocal_lattice.raw_coordinate_convention` | `periodic` | Preserve `cartesian`. |
| `reciprocal_lattice.scale_convention` | `periodic` | Preserve `2pi_over_alat`. |
| `reciprocal_lattice.scale_alat` | `periodic` | Preserve positive scale. |
| `reciprocal_lattice.scale_alat_unit` | `periodic` | Preserve `bohr`. |
| `reciprocal_lattice.incorporates_two_pi` | `periodic` | Preserve `true`. |
| `reciprocal_lattice.physical_vectors` | `periodic` | Preserve exact represented values. |
| `reciprocal_lattice.physical_dimension` | `periodic` | Preserve `inverse_length`. |
| `reciprocal_lattice.physical_unit` | `periodic` | Preserve `bohr^-1`. |
| `reciprocal_lattice.physical_coordinate_convention` | `periodic` | Preserve `cartesian`. |
| `reciprocal_lattice.duality_absolute_tolerance` | Legacy serializer/adaptation policy | Preserve and enforce; create no intrinsic periodic field. |
| `k_point_sampling.raw_coordinates` | `periodic` | Preserve order. |
| `k_point_sampling.raw_dimension` | `periodic` | Preserve `dimensionless`. |
| `k_point_sampling.coordinate_convention` | `periodic` | Preserve `cartesian`. |
| `k_point_sampling.scale_convention` | `periodic` | Preserve `2pi_over_alat`. |
| `k_point_sampling.scale_alat` | `periodic` | Preserve and compare with reciprocal scale. |
| `k_point_sampling.scale_alat_unit` | `periodic` | Preserve `bohr`. |
| `k_point_sampling.incorporates_two_pi` | `periodic` | Preserve `true`. |
| `k_point_sampling.physical_coordinates` | `periodic` | Preserve represented values. |
| `k_point_sampling.physical_dimension` | `periodic` | Preserve `inverse_length`. |
| `k_point_sampling.physical_unit` | `periodic` | Preserve `bohr^-1`. |
| `k_point_sampling.weights` | `periodic` | Preserve order and values. |
| `k_point_sampling.weight_normalization` | `periodic` | Preserve explicit normalization or availability. |

### Kohn--Sham observations

| Schema path | Future owner | Preservation rule |
|---|---|---|
| `spectrum.eigenvalues` | `ksdft` | Preserve rows and order. |
| `spectrum.eigenvalue_unit` | `ksdft` | Preserve `hartree`. |
| `spectrum.occupations` | `ksdft` | Preserve rows or explicit `null`. |
| `spectrum.band_count` | `ksdft` | Preserve explicit count. |
| `spectrum.spin_channel_availability` | `ksdft` | Preserve `no_spin_resolved_arrays`. |
| `spectrum.energy_reference_availability` | `ksdft` | Preserve `not_represented`. |
| `total_energy.value` | `ksdft` | Preserve exact represented value. |
| `total_energy.unit` | `ksdft` | Preserve `hartree`. |
| `total_energy.reference_availability` | `ksdft` | Preserve `not_represented`. |

Every `plane_wave.*` and `provenance.*` path follows its complete table above.
Root `exit_status` becomes calculator process observation. Root `structure`,
`reciprocal_lattice`, `k_point_sampling`, `spectrum`, `total_energy`,
`plane_wave`, and `provenance` are legacy grouping envelopes.

## Cutover order and gates

1. Keep schema v1, retained JSON, serializer, and current imports stable.
2. Migrate QEXSD native parsing without introducing a replacement aggregate.
3. Establish Workflow artifact provenance and calculator contracts before full
   adaptation.
4. Adapt parsed QEXSD into separate periodic values, Kohn--Sham observations,
   integration-native plane-wave extraction results, calculator process
   observations, and Workflow provenance references.
5. Retain the legacy serializer as compatibility oracle for canonical JSON,
   duplicate-key rejection, direct--reciprocal duality, scale agreement,
   sampled-point count agreement, and configured tolerance equality.
6. Retire `ksdft.pw` only after all imports, retained-fixture checks, QEXSD
   construction, schema consumers, and documentation migrate.

No new v2 domain code may depend on the legacy aggregate.

## Deferred human-owned decisions

This disposition is deterministic under existing authority. Two future choices
remain deferred and are not selected here:

- whether representation-specific plane-wave fields warrant a neutral public
  contract; and
- the exact v2 public wire formats and compatibility guarantees.

Either requires separate human authorization when a downstream Task actually
needs it.
