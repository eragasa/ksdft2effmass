# Finding `<CAMPAIGN>-<PACKET>-F<NN>`

## Binding

| Field | Value |
|---|---|
| Campaign | `<campaign identifier>` |
| Packet | `<packet identifier>` |
| Candidate version | `<candidate identifier>` |
| Review pass | `<pass>` |
| Raised by | `<person or agent>` |
| Date raised | `<date>` |
| Affected sources | `<path:line and rendered page>` |
| Affected dependencies | `<packet or claim identifiers>` |

## Finding

**Disposition:** `<MUST_FIX/HUMAN_DECISION_REQUIRED/SAFE_TO_DEFER/NO_ACTION_REQUIRED>`

**Problem:** `<Plain-language description.>`

**Evidence:** `<Exact source, page, calculation record, command result, or
contract contradiction.>`

**Consequence:** `<What can happen if left unchanged.>`

**Next action:** `<Specific correction, decision, revisit condition, or none.>`

## Review and resolution

- Conflicting reviewer evidence: `<evidence or none>`
- Human decision record, if applicable: `<decision identifier or none>`
- Corrected in candidate: `<candidate identifier or not corrected>`
- Verification evidence: `<diff, command, source, or none>`
- Human redline confirmation: `<person, date, concrete answer, or pending>`
- Final disposition: `<disposition>`
- Closure date: `<date or open>`

Changing a disposition does not erase the original recommendation. Record the
change and its evidence here.
