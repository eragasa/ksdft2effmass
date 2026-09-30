# `OllamaResponseRetention`

`OllamaResponseRetention` is the ActionObject for bounded atomic response observability.
It publishes exact raw bytes before parse, parsed metadata after successful typed
conversion, and terminal metadata after composition. Every artifact is mode `0600`,
publication is no-replace, and metadata excludes target/evidence excerpts and generated
replacement text.
