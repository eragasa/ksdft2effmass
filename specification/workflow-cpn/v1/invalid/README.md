# Invalid fixture expectations

These synthetic fixtures are negative software-verification evidence only.

| Fixture | Rejection layer and expected result |
|---|---|
| `unknown-color.json` | Python definition validation: `unknown_color` and invalid initial marking consequences |
| `duplicate-token-id.json` | Python marking validation: `duplicate_token_id` |
| `wrong-place-set.json` | Python marking validation: `place_set_mismatch` |
| `unbound-guard-variable.json` | Python definition validation: `unbound_variable` |
| `invalid-outcome-terminality.json` | JSON Schema and Python `TokenOutcome` construction |
| `boolean-as-integer.json` | Python construction rejects Boolean-as-integer; JSON Schema alone follows JSON's Boolean/integer distinction |
| `nonfinite-real.json` | Strict JSON parsing rejects nonstandard `NaN`; Python `ContractValue` rejects nonfinite real values |
| `lambda-like-expression.json` | JSON Schema rejects the nondeclarative expression shape |
| `output-id-collision.json` | Schema-valid firing request; `TransitionFirer` rejects collision against a current marking |
| `unsupported-version.json` | JSON Schema and Python net construction reject version other than `1` |

Relational fixtures are intentionally permitted by structural schema where the
schema lacks the other object needed to decide the relation. Error codes, rather
than messages, are authoritative. No fixture bypasses object invariants to
fabricate an otherwise unreachable public state.
