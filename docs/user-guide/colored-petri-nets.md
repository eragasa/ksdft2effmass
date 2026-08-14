# Colored Petri Nets

The project workflow is a Colored Petri Net (CPN) with typed token colors and multiset markings. See the [implemented Architecture v1 CPN description](../architecture/v1/workflow/scientific-workflow-and-cpn-model.md) for the mathematical definition and ownership rules.

## P1 version-1 numeric inputs

Use `ContractValueKind.INTEGER` for expression integers. Its value must be an
exact built-in Python `int`, not `bool`, in the signed i64 interval
$[-2^{63},2^{63}-1]$. There is no unsigned `ContractValue` kind.

Use `ContractValueKind.REAL` for expression real numbers. It accepts only finite
exact built-in Python `int` or `float` values except `bool` and stores a built-in
IEEE-754 binary64 `float`. Integer conversion uses round-to-nearest,
ties-to-even, and may round a large integer-valued input. Let
$M=(2-2^{-52})2^{1023}=2^{1024}-2^{971}$ be the maximum finite binary64 value.
General noninteger number values are bounded inclusively by $\pm M$. Built-in
Python `int` values and integer-valued JSON `real` inputs may exceed $M$ and are
admitted through the exact inclusive endpoints
$\pm L$, where $L=2^{1024}-2^{970}-1$. Thus $M+1$ is admitted and rounds to
$M$, but $\pm(L+1)$ overflows or fails schema validation and is rejected.
Conversion overflow and nonfinite inputs or results raise `ValueError`. Strict
JSON input excludes `NaN`, `Infinity`, and `-Infinity`. Passing an in-memory
Python `nan` directly to `jsonschema` does not make it a permitted wire value,
even if the validator's ordered-bound behavior admits it. The intended Rust
mappings are `i64` for `INTEGER` and `f64` for `REAL`.

Every expression-visible nonnegative P1 version-1 control—including marking and
prior revisions, `iteration_index`, and `payload_schema_version`—must be in
$[0,2^{63}-1]$ and remains representable in Rust `i64`. Firing at the maximum
marking revision raises structured `CpnErrorCode.REVISION_OVERFLOW` before a
successor is constructed. This revision rule does not increment
`iteration_index`: the index is separate routing data that callers explicitly
supply or copy, and repeated values are valid.

P1 has no true u64 artifact-size field or unsigned expression value. P2 now
provisionally implements an explicit u64 artifact byte-size field, pending P2
acceptance; it does not change the P1 expression contract. `P1-HC01` Option A and `P1-HC02` Option B are
resolved. Final P1 acceptance was granted as Option A through `P1-HC03` on
2026-08-04, after reviews and parent verification; P1 is closed as
human-accepted `PASS`. P2 is active and provisional pending correction review,
replacement replay, parent verification, and human acceptance. H5 and P3--P11
remain inactive, and production or scientific execution remains unauthorized.

## Conceptual cpnpy reference supplied during architecture design

The following block is retained byte-for-byte as supplied in the human architecture-correction instruction dated 2026-08-03, normalized only as UTF-8 text without a trailing newline inside the fence. Its SHA-256 is `7e0b25a26bf648c5e1dc4cd96e1a4f2762195702312eac4ed489b3d825e90031`. It illustrates a possible CPN API style only. It has **not** been independently verified against the current `cpnpy` release, is not claimed executable, and is not the project's authoritative implementation.

```python
from cpnpy import CPN, Place, Transition, Arc, ColorSet

# 1. Initialize the Petri Net model
net = CPN()

# 2. Define your Color Sets (Token Types)
string_colorset = ColorSet("STRING")

# 3. Create Places (Every place requires a assigned color set)
p_input = Place(name="Input_Queue", colorset=string_colorset)
p_output = Place(name="Processed_Tasks", colorset=string_colorset)

net.add_place(p_input)
net.add_place(p_output)

# 4. Define Transitions with Guard Logic
# The guard allows only tasks starting with 'Priority' to pass
t_process = Transition(
    name="Process_Priority_Task",
    guard=lambda x: x.startswith("Priority")
)
net.add_transition(t_process)

# 5. Connect Elements via Arcs using variables
# Variable 'x' binds to the token value during execution
net.add_arc(Arc(source=p_input, target=t_process, expression="x"))
net.add_arc(Arc(source=t_process, target=p_output, expression="x"))

# 6. Add Initial Markings (Populate tokens)
p_input.add_token("Priority_Task_A")
p_input.add_token("Standard_Task_B")

# 7. Simulate and Fire
print("Initial Output Queue Tokens:", p_output.get_tokens())

# Find available transitions and fire them
enabled_transitions = net.get_enabled_transitions()
for t in enabled_transitions:
    print(f"Firing transition: {t.name}")
    net.fire(t)

print("Final Output Queue Tokens:", p_output.get_tokens())
```

Conceptually, the block shows:

- colored string tokens;
- places;
- transitions;
- guards;
- variable binding;
- markings;
- transition firing.

The example uses a lambda guard and live library objects. Those details are not approved for durable project persistence. Project guards must be represented by project-owned validated semantics, and durable state must store project token payloads rather than arbitrary callables or engine objects.

## Comparative references

`cpnpy` and SimPN remain comparative references only. They are not dependencies and do not reopen the approved SNAKES selection. P0 retained only the bounded comparison evidence needed to explain nonselection; any future comparison requires separate authorization and must remain factual.
