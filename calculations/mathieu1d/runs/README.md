# Run index

All directories are immutable no-overwrite local synthetic executions of experiment
version `v1`. None used an external calculator or remote resource.

| Run identity suffix | Disposition |
|---|---|
| `run-20261014T183028Z` | Non-publication development execution retained from initial serializer/verifier integration |
| `run-20261014T183603Z` | Non-publication development execution retained from strict-schema integration |
| `run-20261014T183721Z` | Non-publication development execution superseded after typed-boundary and installed-dependency-provenance review |
| `run-20261014T184707Z` | Publication-facing execution after typed script checks and authenticated installed VCS dependency checks |

Publication manifests must resolve the publication-facing run by its complete run ID and
post-execution evidence-package digest. Development executions are retained rather than
deleted; they are not live publication evidence.
