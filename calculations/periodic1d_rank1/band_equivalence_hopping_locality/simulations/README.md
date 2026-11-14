# Simulations

This documentation surface records the deterministic in-process calculation boundary.
Architecture v3 places the three direct stage scripts at the calculation root and any
future retained package under `executions/`; it does not create a nested simulation
workflow.

The scalar parent and finite controls are frozen in the calculation-root decision
records. The typed analyzer, independent byte-owning verifier, authenticated projection,
closed renderer, and direct calculate → verify → render adapters are implemented. No
retained execution directory has been produced, and creating one requires separate
execution authorization and provenance review.
