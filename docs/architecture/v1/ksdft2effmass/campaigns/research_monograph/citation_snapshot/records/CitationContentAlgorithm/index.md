# `CitationContentAlgorithm`

Public closed enum for exact source-content digest algorithms. The owner contract
accepts only `sha256`; adding another value would change public content-identity
semantics and requires synchronized implementation, replay, tests, and documentation.
