# `RetainedLocalManuscriptAuthoringRun`

`RetainedLocalManuscriptAuthoringRun` is the Workflow for one observable local
composition. It preserves the sole semantic authoring path, requires the concrete
retained loopback adapter, and publishes separate terminal metadata after the author
returns. If inference raises, it publishes an exceptional terminal record without a
response/result identity and then re-raises. It neither retries nor changes any warning,
mismatch, proposal, or acceptance outcome.
