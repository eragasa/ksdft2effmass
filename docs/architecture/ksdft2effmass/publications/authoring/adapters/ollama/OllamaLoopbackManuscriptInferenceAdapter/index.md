# `OllamaLoopbackManuscriptInferenceAdapter`

`OllamaLoopbackManuscriptInferenceAdapter` is the concrete local-inference ActionObject.
It accepts only `ManuscriptInferenceRequest`, verifies the exact installed
`qwen3.5:9b` model digest, performs one bounded no-tools chat request on literal IPv4
loopback, strictly parses structured output, and returns
`ManuscriptInferenceResponse`. The service port is bounded and configurable only to
support local deployment and synthetic protocol verification; host, model, digest,
paths, timeouts, generation limits, and no-remote/no-tools policy are fixed.

The class requires `OllamaResponseRetention`: exact raw bytes are retained before
parse and parsed metadata before return. It does not retrieve evidence, launch a
service, expose tools, modify manuscript or bibliography content, retry, or confer
scientific or human acceptance.
