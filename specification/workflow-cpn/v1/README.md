# Backend-neutral CPN contract schema, version 1

This directory retains the retired version-1 language-neutral field names, enum
spellings, tagged expression values, routing-token envelope, scoped outcomes,
complete multiset markings, net definitions, firing records, and structured errors
for historical P1 audit. Schemas use JSON Schema draft 2020-12 and reject unknown
fields. The former `ksdft2effmass.workflows.cpn` executable Python reference is
retired; these files are retained specifications, not a supported Python import or a
serializer/persistence repository. The live generic API is
`ksdft2effmass.petrinet.colored` and is intentionally not record- or schema-equal to
this routing-oriented contract.

`cpn-contract.schema.json` contains shared definitions. The net, marking,
firing, validation, executable-result, and error schemas are narrow entry
points. Arrays representing sets use unique items where JSON Schema can enforce
this. A `string_sequence` instead preserves declared order and duplicates so
`bound_token_ids` can represent two read variables bound to the same token;
its individual strings remain nonempty. Declared ordering also remains semantic
for patterns, templates, guards, and bindings.

JSON Schema cannot establish graph references, complete place sets, global token
identity, enabledness, or output-ID novelty. Those relational rules belonged to the
retired `CpnDefinitionValidator`, `CpnMarkingValidator`, and `TransitionFirer`
runtime; the invalid-fixture README retains the historical expected layer.

Under the retained version-1 contract, duplicate
`FiringRequest.output_token_ids` are an intrinsic identifier error and were rejected
before firing. The retired `TransitionFirer` represented `output_id_collision` for a
new request identity already present in the marking. Result-object relations such as
matching transition IDs and successor revision were constructor invariants in the
former Python reference; JSON Schema cannot compare sibling values, so any historical
consumer must enforce those relations independently.

The fixtures are synthetic software-verification examples. They contain no DFT,
Wannier, material, numerical-verification, scientific-validation, or uncertainty-
quantification evidence. Version 1 does not define persistence, SNAKES mapping,
scientific payload objects, external execution, identity generation, or Rust
implementation. A Rust implementation should map frozen Python DataObjects to
validated immutable structs, `StrEnum` values to exhaustive serialized enums,
tuples to validated owned vectors, optionals to `Option`, and structured Python
exceptions to an exhaustive error result. Tagged `integer` values map to signed Rust `i64`. Every version-1
expression-visible nonnegative control field—including marking and prior
revisions, schema and payload-schema versions, iteration indices, and
corresponding routing values—is no greater than `9223372036854775807` and passes
through the same signed `i64` expression representation; version 1 has no
unsigned expression-value kind. Expression-visible payload schema versions
therefore admit the full nonnegative interval from zero through that maximum;
fixed contract and marking schema versions retain their separate version-1
constraints. Tagged `real`
values map to IEEE-754 binary64 Rust `f64`: the former Python reference accepted finite
exact built-in `int` or `float` values except `bool`, canonicalizes them to
built-in `float`, rejects conversion overflow and nonfinite results, and permits
binary64 round-to-nearest, ties-to-even conversion of large integer inputs.
The largest finite binary64 value is

$$
M = (2 - 2^{-52})2^{1023} = 2^{1024} - 2^{971}.
$$

General JSON number values are admitted through inclusive $\pm M$. Built-in
Python `int` values have a distinct exact conversion domain: conversion still
rounds to finite $\pm M$ through the inclusive integer endpoints

$$
L = 2^{1024} - 2^{970} - 1,
$$

so tagged `real` integer-valued JSON numbers are admitted through inclusive
$\pm L$. The schema represents the union with `anyOf`: an integer branch bounded
by $\pm L$ and a general-number branch bounded by $\pm M$. Thus $M+1$ is admitted
as an integer-valued `real` and rounds to $M$, while $\pm(L+1)$ is rejected
because built-in `float` conversion would overflow. The exact positive decimal
endpoints are

- $M = 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368$;
- $L = 179769313486231580793728971405303415079934132710037826936173778980444968292764750946649017977587207096330286416692887910946555547851940402630657488671505820681908902000708383676273854845817711531764475730270069855571366959622842914819860834936475292719074168444365510704342711559699508093042880177904174497791$.

This wire boundary does not require an admitted integer-valued `real` to be
exactly representable after canonicalization.

NaN and positive or negative infinity are outside the JSON instance model, and
version 1 defines no nonstandard spelling for them. Conformance requires strict
JSON parsing that rejects these nonfinite constants before schema validation;
they are never admitted tagged `real` wire values. If a JSON Schema API is given
host-language infinities directly, the finite schema bounds also reject them,
but that does not make them JSON. Schema implementations that coerce
arbitrary-precision JSON numbers to a narrower host numeric type may be unable
to enforce the exact decimal boundaries, so interoperability checks must use an
implementation that preserves enough numeric range for these `minimum` and
`maximum` comparisons.

Firing from revision
`9223372036854775807` returns the structured `revision_overflow` firing error
before successor construction and creates no successor.
