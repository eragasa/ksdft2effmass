# `LocalManuscriptInferencePort`

`LocalManuscriptInferencePort` is a structural protocol with one `infer(request)`
method returning `ManuscriptInferenceResponse`. The protocol exposes no filesystem,
shell, database, browser, network, retrieval, bibliography, or publication method.
Concrete local runtime composition and process isolation are deferred.
