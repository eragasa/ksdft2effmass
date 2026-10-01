# `LocalManuscriptInferencePort`

`LocalManuscriptInferencePort` is a structural protocol with one `infer(request)`
method returning `ManuscriptInferenceResponse`. The protocol exposes no filesystem,
shell, database, browser, network, retrieval, bibliography, or publication method.
[`OllamaLoopbackManuscriptInferenceAdapter`](../../adapters/ollama/OllamaLoopbackManuscriptInferenceAdapter/index.md)
implements this port with a fixed model and bounded literal-loopback transport. The
protocol itself remains runtime-neutral and grants no capability to the model.
