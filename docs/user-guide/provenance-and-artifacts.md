# Provenance and artifacts

Portable artifact identity is separate from deployment location.

```text
ArtifactReference
    artifact_id
    logical_path
    sha256
    byte_size
    format
    semantic_role
    retention_policy
    producer_manifest_id

ArtifactLocation
    artifact_id
    storage_uri
```

Checksums and sizes identify sealed content. Logical paths express role within a run or campaign. Storage URIs may change without changing scientific identity. A source URI is provenance metadata, not content identity.

Durable CPN tokens retain IDs for artifacts, manifests, tool installations, verification results, requests, results, and parent runs. They do not retain open files, subprocess handles, scheduler clients, credentials, mutable external-library instances, or SNAKES runtime objects.

Large densities, wavefunctions, QE `.save` trees, restart state, FFT grids, and Wannier bridge files remain external immutable artifacts. Retention metadata does not authorize deletion.

A comparison join requires compatible parent provenance and representation metadata. Two completed branch tokens alone are insufficient.
