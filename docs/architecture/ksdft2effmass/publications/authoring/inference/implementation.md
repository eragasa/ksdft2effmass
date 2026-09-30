# `inference` implementation

```mermaid
flowchart LR
    Contracts["contracts.py"] --> Inference["inference.py"]
    ProposedCitation["proposal.ProposedCitation"] --> Inference
    Inference --> Author["author.py"]
```

The protocol exposes only `infer(ManuscriptInferenceRequest) ->
ManuscriptInferenceResponse`. Records impose hard size, identity, uniqueness, and
ordering bounds. Concrete runtime selection, process isolation, timeout, cancellation,
model identity, and structured-output parsing remain deferred.
