# `ollama_retention` implementation

```mermaid
flowchart TD
    Temp["complete fsynced 0600 temp file"] --> Link["atomic hard-link publication"]
    Existing["existing final name"] -->|"FileExistsError"| Stop["never replace"]
    Link --> Final["0600 final artifact"]
    Final --> Directory["fsynced 0700 directory"]
```

`OllamaResponseRetention` accepts a local directory selected by runtime composition.
Production composition uses ignored `.pi/cache/evidence-authoring/runtime`; tests use
framework-isolated temporary directories. Response bytes must contain 1 to 65,536
bytes and use the exact inference-request identity grammar. Complete temporary bytes
are fsynced and atomically published with a hard link, so an existing final artifact
is never replaced. Files are mode `0600`; the retention directory is mode `0700`.

The raw artifact contains exact local service bytes. Parsed metadata separately records
raw path name/digest/count, model name/digest, inference request/response/implementation
IDs, replacement-text digest and character count, request-owned citation/evidence
mappings, gap IDs, and the exact warning tuple—never replacement, target, or evidence
text. When decoded JSON is rejected during typed construction, a distinct
`decoded-rejection` record binds the request, model, and raw digest to generated keys,
content and replacement digests/counts, exact warnings, stage, and stable error
code/type/message. It is not a parsed response.

Ordinary terminal metadata records the authoring outcome, issues,
response/result/proposal IDs, and `NOT_EVALUATED` acceptance. Inference exceptions
instead produce `exceptional-terminal` metadata naming retained raw/decoded/parsed
artifacts while setting response, result, and outcome identities to null. It is not a
`ManuscriptAuthoringResult`. All metadata uses canonical unversioned record types and
omits `schema_version`. Retention grants no manuscript, bibliography, publication,
remote-network, or retry capability.
