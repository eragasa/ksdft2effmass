# Human intake: explicit successor selection

The authoritative Task-local record is [`harness.simplification.control.successor-selection.json`](harness.simplification.control.successor-selection.json). This intake records the requested future work but does not select or activate a successor.

When its prerequisites are complete, this Task provides a bounded durable selection boundary for the next harness-simplification Task. Eligibility, ordering, documentation, reviewer agreement, and completed predecessor work do not authorize activation. One exact successor may be activated only after an unambiguous current human selection and an agreeing chain/Task state update.
