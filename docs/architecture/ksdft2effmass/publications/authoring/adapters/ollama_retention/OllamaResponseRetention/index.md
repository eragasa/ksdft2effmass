# `OllamaResponseRetention`

`OllamaResponseRetention` is the ActionObject for bounded atomic response observability.
It publishes exact raw bytes before parse. Successful typed conversion produces parsed
metadata; any outer, generated, or typed contract rejection after successful outer
JSON decoding instead produces distinct stage-labelled excerpt-free rejection metadata.
Composition produces an ordinary terminal record, while an
inference exception produces a distinct exceptional terminal record without a response
or result identity. Every artifact is mode `0600`, publication is no-replace, and
metadata excludes target, evidence, and generated replacement excerpts.
