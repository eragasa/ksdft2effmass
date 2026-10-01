# `OllamaLoopbackManuscriptInferenceAdapter`

`OllamaLoopbackManuscriptInferenceAdapter` is the concrete local-inference ActionObject.
It accepts only `ManuscriptInferenceRequest`, verifies the exact installed
`qwen3.5:9b` model digest, performs one bounded no-tools chat request on literal IPv4
loopback, strictly parses candidate text and warning output, combines it only with
request-owned citation/evidence/marker lineage, and returns
`ManuscriptInferenceResponse`. The service port is bounded and configurable only to
support local deployment and synthetic protocol verification; host, model, digest,
paths, timeouts, generation limits, and no-remote/no-tools policy are fixed.

The class requires `OllamaResponseRetention`: exact raw bytes are retained before
parse, decoded typed-contract rejection is retained before re-raise, and parsed
metadata is retained before a typed return. It does not retrieve evidence, launch a
service, expose tools, modify manuscript or bibliography content, retry, or confer
scientific or human acceptance.
