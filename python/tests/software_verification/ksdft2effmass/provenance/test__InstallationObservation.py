r"""Software verification of ``InstallationObservation``.

Facet and represented meaning

-----------------------------
This class-owned evidence verifies exact stored installation metadata, intrinsic
text and digest invariants, frozen state, equality, and the durable boundary.

Intrinsic and cross-object scope

--------------------------------
The sole SUT is ``InstallationObservation``. Public field declarations, literal
portable grammars, frozen-dataclass semantics, and independently chosen synthetic
values are exact oracles. Construction performs no I/O and emits no warnings.

VVUQ and scientific exclusions

------------------------------
Passing establishes only construction and immutable value semantics for an
already-observed installation record. It does not verify a digest against bytes,
execute a tool, or establish numerical verification, scientific validation, UQ,
physical correctness, portability, or cross-language agreement.
"""

from dataclasses import FrozenInstanceError, astuple, fields
from typing import Any

import pytest

from ksdft2effmass.provenance import InstallationObservation

SUT = InstallationObservation
pytestmark = pytest.mark.software_verification

IDENTIFIER_FIELDS = (
    "installation_id",
    "specification_id",
    "tool_id",
    "executable_or_package_id",
    "environment_record_id",
    "provenance_id",
)
PUBLIC_FIELDS = (
    "installation_id",
    "specification_id",
    "tool_id",
    "observed_version",
    "executable_or_package_id",
    "executable_sha256",
    "environment_record_id",
    "provenance_id",
)
FROZEN_FIELDS = (
    "installation_id",
    "specification_id",
    "tool_id",
    "observed_version",
    "executable_or_package_id",
    "executable_sha256",
    "environment_record_id",
    "provenance_id",
)
EQUALITY_FIELDS = (
    "installation_id",
    "specification_id",
    "tool_id",
    "observed_version",
    "executable_or_package_id",
    "executable_sha256",
    "environment_record_id",
    "provenance_id",
)


def make_installation_observation(**overrides: Any) -> InstallationObservation:
    """Evidence ID: Owns no identifier; supports InstallationObservation evidence in
    this module.

    Requirement: Tests need explicit valid synthetic baseline state with one-field
    overrides.

    Method: Build the eight public constructor arguments and replace only named
    overrides.

    Oracle: Literal valid values satisfy the accepted identifier, version, and digest
    contracts.

    Acceptance: Return direct SUT construction; perform no assertion, I/O, or
    normalization.

    Interpretation: Helper failure indicates invalid setup or constructor drift, not
    evidence.

    Limitations: The helper deliberately permits invalid typed overrides for rejection
    tests.
    """
    values: dict[str, Any] = {
        "installation_id": "install-1",
        "specification_id": "spec-1",
        "tool_id": "qe",
        "observed_version": "7.4",
        "executable_or_package_id": "pw.x",
        "executable_sha256": None,
        "environment_record_id": "env-1",
        "provenance_id": "prov-1",
    }
    values.update(overrides)
    return SUT(**values)


def test_constructor__field_mapping__stores_exact_values_order_and_builtin_types() -> (
    None
):
    """Evidence ID: SV-PROV-031

    Requirement: Construction stores eight public fields unchanged in their declared
    order and types.

    Method: Construct complete synthetic metadata with absent digest; inspect public
    state.

    Oracle: The accepted field sequence and literals fix exact values and built-in
    types.

    Acceptance: Names, values, and every built-in str/None type match; no coercion
    occurs.

    Interpretation: Failure identifies mapping, ordering, coercion, setup, or
    accepted-contract drift.

    Limitations: Values are synthetic and do not establish that an installation exists
    or executes.
    """
    record = make_installation_observation()
    assert tuple(field.name for field in fields(record)) == PUBLIC_FIELDS
    assert astuple(record) == (
        "install-1",
        "spec-1",
        "qe",
        "7.4",
        "pw.x",
        None,
        "env-1",
        "prov-1",
    )
    assert (
        type(record.installation_id),
        type(record.specification_id),
        type(record.tool_id),
        type(record.observed_version),
        type(record.executable_or_package_id),
        type(record.executable_sha256),
        type(record.environment_record_id),
        type(record.provenance_id),
    ) == (str, str, str, str, str, None.__class__, str, str)


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "installation_id", "alpha-1", id="installation_id_ordinary_identifier"
        ),
        pytest.param(
            "specification_id", "alpha-1", id="specification_id_ordinary_identifier"
        ),
        pytest.param("tool_id", "alpha-1", id="tool_id_ordinary_identifier"),
        pytest.param(
            "executable_or_package_id",
            "alpha-1",
            id="executable_or_package_id_ordinary_identifier",
        ),
        pytest.param(
            "environment_record_id",
            "alpha-1",
            id="environment_record_id_ordinary_identifier",
        ),
        pytest.param(
            "provenance_id", "alpha-1", id="provenance_id_ordinary_identifier"
        ),
        pytest.param("installation_id", "A", id="installation_id_minimum_length_1"),
        pytest.param("specification_id", "A", id="specification_id_minimum_length_1"),
        pytest.param("tool_id", "A", id="tool_id_minimum_length_1"),
        pytest.param(
            "executable_or_package_id",
            "A",
            id="executable_or_package_id_minimum_length_1",
        ),
        pytest.param(
            "environment_record_id", "A", id="environment_record_id_minimum_length_1"
        ),
        pytest.param("provenance_id", "A", id="provenance_id_minimum_length_1"),
        pytest.param(
            "installation_id", "A" * 128, id="installation_id_maximum_length_128"
        ),
        pytest.param(
            "specification_id", "A" * 128, id="specification_id_maximum_length_128"
        ),
        pytest.param("tool_id", "A" * 128, id="tool_id_maximum_length_128"),
        pytest.param(
            "executable_or_package_id",
            "A" * 128,
            id="executable_or_package_id_maximum_length_128",
        ),
        pytest.param(
            "environment_record_id",
            "A" * 128,
            id="environment_record_id_maximum_length_128",
        ),
        pytest.param("provenance_id", "A" * 128, id="provenance_id_maximum_length_128"),
    ],
)
def test_constructor__identifier_boundaries__accept_valid_partition(
    field_name: str, value: str
) -> None:
    """Evidence ID: SV-PROV-241

    Requirement: Each of six identifier fields accepts ordinary, length-one, and
    length-128 text.

    Method: Override one named field with one explicit valid lexical-length partition.

    Oracle: The grammar permits an alphanumeric lead and up to 127 permitted
    continuations.

    Acceptance: Construction succeeds and the selected built-in string is stored
    exactly.

    Interpretation: Failure identifies field-specific rejection, boundary, setup, or
    grammar drift.

    Limitations: Synthetic ASCII identifiers do not test external resolution or
    interoperability.
    """
    record = make_installation_observation(**{field_name: value})
    assert getattr(record, field_name) == value
    assert type(getattr(record, field_name)) is str


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("installation_id", id="installation_id_bytes_wrong_type"),
        pytest.param("specification_id", id="specification_id_bytes_wrong_type"),
        pytest.param("tool_id", id="tool_id_bytes_wrong_type"),
        pytest.param(
            "executable_or_package_id", id="executable_or_package_id_bytes_wrong_type"
        ),
        pytest.param(
            "environment_record_id", id="environment_record_id_bytes_wrong_type"
        ),
        pytest.param("provenance_id", id="provenance_id_bytes_wrong_type"),
    ],
)
def test_constructor__identifier_type__rejects_wrong_semantic_type(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-207

    Requirement: Each identifier field requires an exact built-in str and performs no
    coercion.

    Method: Supply bytes to one named identifier while every other field remains valid.

    Oracle: The accepted semantic type is built-in str; bytes is a distinct type.

    Acceptance: Every field partition raises exactly TypeError.

    Interpretation: Failure identifies coercion, validation-order, field-coverage, or
    contract drift.

    Limitations: Other wrong Python types and identifier value grammar are outside this
    partition.
    """
    with pytest.raises(TypeError):
        make_installation_observation(**{field_name: b"identifier"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("installation_id", id="installation_id_empty_identifier"),
        pytest.param("specification_id", id="specification_id_empty_identifier"),
        pytest.param("tool_id", id="tool_id_empty_identifier"),
        pytest.param(
            "executable_or_package_id", id="executable_or_package_id_empty_identifier"
        ),
        pytest.param(
            "environment_record_id", id="environment_record_id_empty_identifier"
        ),
        pytest.param("provenance_id", id="provenance_id_empty_identifier"),
    ],
)
def test_constructor__identifier_nonempty__rejects_empty_text(field_name: str) -> None:
    """Evidence ID: SV-PROV-242

    Requirement: Each identifier field rejects the empty built-in string.

    Method: Supply empty text to one named identifier with otherwise valid state.

    Oracle: The accepted identifier length is inclusively 1 through 128.

    Acceptance: Every field partition raises exactly ValueError.

    Interpretation: Failure identifies missing nonempty enforcement, field coverage, or
    contract drift.

    Limitations: Wrong types and nonempty malformed text are tested separately.
    """
    with pytest.raises(ValueError):
        make_installation_observation(**{field_name: ""})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("installation_id", id="installation_id_embedded_space"),
        pytest.param("specification_id", id="specification_id_embedded_space"),
        pytest.param("tool_id", id="tool_id_embedded_space"),
        pytest.param(
            "executable_or_package_id", id="executable_or_package_id_embedded_space"
        ),
        pytest.param(
            "environment_record_id", id="environment_record_id_embedded_space"
        ),
        pytest.param("provenance_id", id="provenance_id_embedded_space"),
    ],
)
def test_constructor__identifier_grammar__rejects_embedded_space(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-206

    Requirement: Each identifier field rejects an embedded ASCII space.

    Method: Supply ``bad id`` to one named field with otherwise valid state.

    Oracle: Space is absent from the accepted portable continuation character set.

    Acceptance: Every field partition raises exactly ValueError.

    Interpretation: Failure identifies grammar widening, field coverage, setup, or
    contract drift.

    Limitations: Leading-character, Unicode, and length partitions are tested
    separately.
    """
    with pytest.raises(ValueError):
        make_installation_observation(**{field_name: "bad id"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("installation_id", id="installation_id_invalid_leading_hyphen"),
        pytest.param("specification_id", id="specification_id_invalid_leading_hyphen"),
        pytest.param("tool_id", id="tool_id_invalid_leading_hyphen"),
        pytest.param(
            "executable_or_package_id",
            id="executable_or_package_id_invalid_leading_hyphen",
        ),
        pytest.param(
            "environment_record_id", id="environment_record_id_invalid_leading_hyphen"
        ),
        pytest.param("provenance_id", id="provenance_id_invalid_leading_hyphen"),
    ],
)
def test_constructor__identifier_leading_character__rejects_non_alphanumeric(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-243

    Requirement: Each identifier must begin with an ASCII alphanumeric character.

    Method: Supply a leading-hyphen identifier to one named field.

    Oracle: Hyphen is permitted only after the first grammar position.

    Acceptance: Every field partition raises exactly ValueError.

    Interpretation: Failure identifies leading-character grammar or field-specific
    enforcement drift.

    Limitations: This does not test all Unicode or punctuation characters.
    """
    with pytest.raises(ValueError):
        make_installation_observation(**{field_name: "-identifier"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("installation_id", id="installation_id_unicode_surrogate"),
        pytest.param("specification_id", id="specification_id_unicode_surrogate"),
        pytest.param("tool_id", id="tool_id_unicode_surrogate"),
        pytest.param(
            "executable_or_package_id", id="executable_or_package_id_unicode_surrogate"
        ),
        pytest.param(
            "environment_record_id", id="environment_record_id_unicode_surrogate"
        ),
        pytest.param("provenance_id", id="provenance_id_unicode_surrogate"),
    ],
)
def test_constructor__identifier_unicode__rejects_surrogate(field_name: str) -> None:
    """Evidence ID: SV-PROV-244

    Requirement: Each identifier field rejects Unicode surrogate code points.

    Method: Supply a string containing U+D800 to one named field.

    Oracle: The public Unicode invariant explicitly excludes the surrogate range.

    Acceptance: Every field partition raises exactly ValueError before grammar
    admission.

    Interpretation: Failure identifies unsafe Unicode admission, validation order, or
    contract drift.

    Limitations: NFC and portable ASCII grammar are separate partitions.
    """
    with pytest.raises(ValueError):
        make_installation_observation(**{field_name: "A\ud800"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("installation_id", id="installation_id_decomposed_non_nfc"),
        pytest.param("specification_id", id="specification_id_decomposed_non_nfc"),
        pytest.param("tool_id", id="tool_id_decomposed_non_nfc"),
        pytest.param(
            "executable_or_package_id", id="executable_or_package_id_decomposed_non_nfc"
        ),
        pytest.param(
            "environment_record_id", id="environment_record_id_decomposed_non_nfc"
        ),
        pytest.param("provenance_id", id="provenance_id_decomposed_non_nfc"),
    ],
)
def test_constructor__identifier_unicode__rejects_non_nfc(field_name: str) -> None:
    """Evidence ID: SV-PROV-245

    Requirement: Each identifier field rejects non-NFC text independently of portable
    grammar.

    Method: Supply decomposed ``A`` plus combining ring to one named field.

    Oracle: Unicode normalization maps the input to a different NFC string.

    Acceptance: Every field partition raises exactly ValueError at the public NFC
    boundary.

    Interpretation: Failure identifies normalization enforcement, ordering, or
    field-coverage drift.

    Limitations: The decomposed value is synthetic and would also fail the later ASCII
    grammar.
    """
    with pytest.raises(ValueError):
        make_installation_observation(**{field_name: "A\u030a"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("installation_id", id="installation_id_overlength_129"),
        pytest.param("specification_id", id="specification_id_overlength_129"),
        pytest.param("tool_id", id="tool_id_overlength_129"),
        pytest.param(
            "executable_or_package_id", id="executable_or_package_id_overlength_129"
        ),
        pytest.param(
            "environment_record_id", id="environment_record_id_overlength_129"
        ),
        pytest.param("provenance_id", id="provenance_id_overlength_129"),
    ],
)
def test_constructor__identifier_length__rejects_129_characters(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-246

    Requirement: Each identifier field rejects length 129 above the inclusive maximum
    128.

    Method: Supply 129 valid ASCII identifier characters to one named field.

    Oracle: The accepted grammar permits at most 128 characters.

    Acceptance: Every field partition raises exactly ValueError.

    Interpretation: Failure identifies an off-by-one bound, field coverage, or contract
    drift.

    Limitations: This is a lexical bound, not a filesystem or external-system limit.
    """
    with pytest.raises(ValueError):
        make_installation_observation(**{field_name: "A" * 129})


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("7.4", id="observed_version_ordinary_version"),
        pytest.param("1", id="observed_version_minimum_length_1"),
        pytest.param("A" * 64, id="observed_version_maximum_length_64"),
    ],
)
def test_constructor__observed_version_boundaries__accept_valid_text(
    value: str,
) -> None:
    """Evidence ID: SV-PROV-247

    Requirement: Observed version accepts ordinary, length-one, and length-64 portable
    text.

    Method: Construct with one explicit valid version length partition.

    Oracle: The version grammar permits an alphanumeric lead and 63 permitted
    continuations.

    Acceptance: The exact built-in string is stored without coercion or normalization.

    Interpretation: Failure identifies version grammar, boundary, setup, or storage
    drift.

    Limitations: Opaque text acceptance does not compare or interpret software versions.
    """
    record = make_installation_observation(observed_version=value)
    assert record.observed_version == value
    assert type(record.observed_version) is str


def test_constructor__observed_version_type__rejects_wrong_semantic_type() -> None:
    """Evidence ID: SV-PROV-248

    Requirement: Observed version requires exact built-in str and performs no coercion.

    Method: Supply bytes while every other constructor field remains valid.

    Oracle: Bytes is not the accepted built-in string semantic type.

    Acceptance: Construction raises exactly TypeError.

    Interpretation: Failure identifies accidental coercion or version type-contract
    drift.

    Limitations: Invalid string values are covered by separate partitions.
    """
    with pytest.raises(TypeError):
        make_installation_observation(observed_version=b"7.4")


def test_constructor__observed_version_nonempty__rejects_empty_text() -> None:
    """Evidence ID: SV-PROV-249

    Requirement: Observed version rejects empty text.

    Method: Construct with the empty built-in string and otherwise valid state.

    Oracle: The accepted version length is inclusively 1 through 64.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies missing nonempty enforcement or contract drift.

    Limitations: Wrong types and nonempty malformed versions are separate partitions.
    """
    with pytest.raises(ValueError):
        make_installation_observation(observed_version="")


def test_constructor__observed_version_leading_character__rejects_hyphen() -> None:
    """Evidence ID: SV-PROV-250

    Requirement: Observed version must begin with an ASCII alphanumeric character.

    Method: Construct with the otherwise plausible version ``-7.4``.

    Oracle: The accepted grammar excludes hyphen from the first position.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies leading-character grammar widening or contract
    drift.

    Limitations: This does not interpret semantic versioning.
    """
    with pytest.raises(ValueError):
        make_installation_observation(observed_version="-7.4")


def test_constructor__observed_version_character_set__rejects_slash() -> None:
    """Evidence ID: SV-PROV-251

    Requirement: Observed version rejects characters outside its portable continuation
    set.

    Method: Construct with an embedded slash after a valid leading character.

    Oracle: Slash is absent from ``[0-9A-Za-z._+-]``.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies character-set widening or contract drift.

    Limitations: This single representative does not enumerate every excluded character.
    """
    with pytest.raises(ValueError):
        make_installation_observation(observed_version="7/4")


def test_constructor__observed_version_unicode__rejects_surrogate() -> None:
    """Evidence ID: SV-PROV-252

    Requirement: Observed version rejects Unicode surrogate code points.

    Method: Construct with version text containing U+D800.

    Oracle: The public Unicode invariant excludes the surrogate range.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies unsafe Unicode admission or validation-order
    drift.

    Limitations: NFC and portable-character checks are separate requirements.
    """
    with pytest.raises(ValueError):
        make_installation_observation(observed_version="7\ud800")


def test_constructor__observed_version_unicode__rejects_non_nfc() -> None:
    """Evidence ID: SV-PROV-253

    Requirement: Observed version rejects non-NFC text.

    Method: Construct with decomposed ``A`` plus combining ring.

    Oracle: Unicode normalization changes the supplied text under NFC.

    Acceptance: Construction raises exactly ValueError at the NFC boundary.

    Interpretation: Failure identifies missing normalization enforcement or ordering
    drift.

    Limitations: The value would also fail the later portable-character grammar.
    """
    with pytest.raises(ValueError):
        make_installation_observation(observed_version="A\u030a")


def test_constructor__observed_version_length__rejects_65_characters() -> None:
    """Evidence ID: SV-PROV-254

    Requirement: Observed version rejects length 65 above the inclusive maximum 64.

    Method: Construct with 65 otherwise valid ASCII version characters.

    Oracle: The accepted lexical grammar permits at most 64 characters.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies an off-by-one bound or version-contract drift.

    Limitations: The bound is lexical and does not assess version meaning.
    """
    with pytest.raises(ValueError):
        make_installation_observation(observed_version="A" * 65)


@pytest.mark.parametrize(
    "digest",
    [
        pytest.param(None, id="executable_sha256_absent_digest"),
        pytest.param("a" * 64, id="executable_sha256_lowercase_64_hex"),
    ],
)
def test_constructor__executable_sha256_valid_states__preserves_value(
    digest: str | None,
) -> None:
    """Evidence ID: SV-PROV-033

    Requirement: Digest accepts absence or an exact lowercase 64-hex built-in string.

    Method: Construct one explicit optional-state partition.

    Oracle: None and 64 lowercase ``a`` characters are independently valid states.

    Acceptance: Construction stores the selected state exactly without coercion.

    Interpretation: Failure identifies optionality, grammar, storage, or setup drift.

    Limitations: No executable bytes are read, hashed, or compared.
    """
    record = make_installation_observation(executable_sha256=digest)
    assert record.executable_sha256 == digest
    assert type(record.executable_sha256) is type(digest)


def test_constructor__executable_sha256_type__rejects_wrong_semantic_type() -> None:
    """Evidence ID: SV-PROV-205

    Requirement: A present digest requires exact built-in str and is not coerced.

    Method: Supply integer one with otherwise valid constructor state.

    Oracle: The accepted present type is built-in str; integer is distinct.

    Acceptance: Construction raises exactly TypeError.

    Interpretation: Failure identifies accidental coercion or digest type-contract
    drift.

    Limitations: Invalid digest strings are separate partitions.
    """
    with pytest.raises(TypeError):
        make_installation_observation(executable_sha256=1)


def test_constructor__executable_sha256_nonempty__rejects_empty_text() -> None:
    """Evidence ID: SV-PROV-255

    Requirement: A present digest cannot be the empty string.

    Method: Construct with empty digest text and otherwise valid state.

    Oracle: A SHA-256 hexadecimal representation has exactly 64 characters.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies missing nonempty enforcement or digest-contract
    drift.

    Limitations: Other malformed digest strings are separate partitions.
    """
    with pytest.raises(ValueError):
        make_installation_observation(executable_sha256="")


@pytest.mark.parametrize(
    "digest",
    [
        pytest.param("A" * 64, id="executable_sha256_uppercase_hex"),
        pytest.param("g" * 64, id="executable_sha256_nonhex_character"),
        pytest.param("a" * 63, id="executable_sha256_short_length_63"),
        pytest.param("a" * 65, id="executable_sha256_long_length_65"),
    ],
)
def test_constructor__executable_sha256_grammar__rejects_malformed_text(
    digest: str,
) -> None:
    """Evidence ID: SV-PROV-256

    Requirement: A present digest must be exactly 64 lowercase hexadecimal characters.

    Method: Construct one uppercase, nonhex, short, or long malformed grammar partition.

    Oracle: The accepted literal regular language is exactly ``[0-9a-f]{64}``.

    Acceptance: Every partition raises exactly ValueError.

    Interpretation: Failure identifies digest grammar widening, length drift, or bad
    test data.

    Limitations: Unicode safety and NFC ordering are tested separately.
    """
    with pytest.raises(ValueError):
        make_installation_observation(executable_sha256=digest)


def test_constructor__executable_sha256_unicode__rejects_surrogate() -> None:
    """Evidence ID: SV-PROV-257

    Requirement: A present digest rejects Unicode surrogate code points.

    Method: Supply a 64-character string containing U+D800.

    Oracle: The public Unicode invariant excludes the surrogate range before SHA
    grammar.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies unsafe Unicode admission or validation-order
    drift.

    Limitations: This does not validate any real digest computation.
    """
    with pytest.raises(ValueError):
        make_installation_observation(executable_sha256="a" * 63 + "\ud800")


def test_constructor__executable_sha256_unicode__rejects_non_nfc() -> None:
    """Evidence ID: SV-PROV-258

    Requirement: A present digest rejects decomposed non-NFC text before SHA grammar
    admission.

    Method: Supply 62 lowercase hex characters followed by decomposed A-ring text.

    Oracle: NFC normalization changes the string, so the independent NFC check is
    reachable.

    Acceptance: Construction raises exactly ValueError at the public NFC boundary.

    Interpretation: Failure identifies missing NFC enforcement or validation-order
    drift.

    Limitations: The same text would also fail the later lowercase-hex grammar.
    """
    with pytest.raises(ValueError):
        make_installation_observation(executable_sha256="a" * 62 + "A\u030a")


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("installation_id", id="installation_id_frozen_reassignment"),
        pytest.param("specification_id", id="specification_id_frozen_reassignment"),
        pytest.param("tool_id", id="tool_id_frozen_reassignment"),
        pytest.param("observed_version", id="observed_version_frozen_reassignment"),
        pytest.param(
            "executable_or_package_id",
            id="executable_or_package_id_frozen_reassignment",
        ),
        pytest.param("executable_sha256", id="executable_sha256_frozen_reassignment"),
        pytest.param(
            "environment_record_id", id="environment_record_id_frozen_reassignment"
        ),
        pytest.param("provenance_id", id="provenance_id_frozen_reassignment"),
    ],
)
def test_field__frozen_reassignment__rejects_every_public_field(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-208

    Requirement: Every public installation field is frozen after construction.

    Method: Reassign one semantically identified public field on a valid record.

    Oracle: The accepted frozen-dataclass contract forbids all field reassignment.

    Acceptance: Every field partition raises exactly FrozenInstanceError.

    Interpretation: Failure identifies mutable public state or an incorrect field
    inventory.

    Limitations: This tests reassignment, not mutation of unrelated external objects.
    """
    record = make_installation_observation()
    with pytest.raises(FrozenInstanceError):
        setattr(record, field_name, getattr(record, field_name))


@pytest.mark.parametrize(
    ("field_name", "changed_value"),
    [
        pytest.param("installation_id", "install-2", id="installation_id_different"),
        pytest.param("specification_id", "spec-2", id="specification_id_different"),
        pytest.param("tool_id", "abinit", id="tool_id_different"),
        pytest.param("observed_version", "8.0", id="observed_version_different"),
        pytest.param(
            "executable_or_package_id", "ph.x", id="executable_or_package_id_different"
        ),
        pytest.param(
            "executable_sha256", "a" * 64, id="executable_sha256_absent_to_present"
        ),
        pytest.param(
            "environment_record_id", "env-2", id="environment_record_id_different"
        ),
        pytest.param("provenance_id", "prov-2", id="provenance_id_different"),
    ],
)
def test_method__eq__distinguishes_each_public_field(
    field_name: str, changed_value: str
) -> None:
    """Evidence ID: SV-PROV-209

    Requirement: Equality compares every public field, including absent versus present
    digest.

    Method: Compare a valid baseline with one record differing in exactly the named
    field.

    Oracle: Frozen dataclass equality is exact complete represented-state equality.

    Acceptance: Identical complete state is equal and the one-field change is unequal.

    Interpretation: Failure identifies omitted equality state, constructor setup, or
    contract drift.

    Limitations: Equality does not establish installation identity in an external
    registry.
    """
    baseline = make_installation_observation()
    assert baseline == make_installation_observation()
    assert baseline != make_installation_observation(**{field_name: changed_value})


def test_method__eq__distinguishes_present_from_absent_digest_in_both_directions() -> (
    None
):
    """Evidence ID: SV-PROV-259

    Requirement: Optional digest presence participates symmetrically in exact equality.

    Method: Compare valid absent- and present-digest records in both operand directions.

    Oracle: None and a lowercase digest are distinct represented states.

    Acceptance: Both comparisons are unequal.

    Interpretation: Failure identifies asymmetric or digest-omitting equality behavior.

    Limitations: No digest bytes or cryptographic equivalence are assessed.
    """
    absent = make_installation_observation()
    present = make_installation_observation(executable_sha256="a" * 64)
    assert absent != present
    assert present != absent


def test_method__eq__returns_unequal_for_unrelated_object() -> None:
    """Evidence ID: SV-PROV-260

    Requirement: InstallationObservation is unequal to an unrelated object.

    Method: Compare a valid record with a plain object using public equality.

    Oracle: Dataclass equality returns NotImplemented for another class, yielding false.

    Acceptance: The equality expression is exactly false.

    Interpretation: Failure identifies unexpected cross-type equality semantics or
    contract drift.

    Limitations: Equality against subclasses or proxies is not covered.
    """
    assert not (make_installation_observation() == object())


def test_field__capability_boundary__excludes_verification_status() -> None:
    """Evidence ID: SV-PROV-032

    Requirement: Installation metadata excludes capability verification identity and
    status.

    Method: Compare the exact public field inventory with capability-verification
    fields.

    Oracle: Capability observations belong to VerificationObservation, not this record.

    Acceptance: ``capability_id`` and ``status`` are both absent.

    Interpretation: Failure identifies a lifecycle-boundary or field-inventory defect.

    Limitations: This does not verify behavior of VerificationObservation.
    """
    assert set(PUBLIC_FIELDS).isdisjoint({"capability_id", "status"})


def test_field__durable_boundary__excludes_runtime_and_secret_state() -> None:
    """Evidence ID: SV-PROV-210

    Requirement: Durable installation metadata excludes results, secrets, handles, and
    services.

    Method: Compare the exact public inventory with explicit forbidden runtime-state
    names.

    Oracle: The accepted boundary excludes execution results, credentials, clients,
    processes,
    scheduler handles, open files, and mutable runtime services.

    Acceptance: The public field set is disjoint from every prohibited category
    representative.

    Interpretation: Failure identifies durable/runtime ownership leakage or inventory
    drift.

    Limitations: Name inspection cannot assess behavior hidden outside declared public
    fields.
    """
    assert set(PUBLIC_FIELDS).isdisjoint(
        {
            "capability_verification_status",
            "execution_result",
            "credentials",
            "client",
            "process",
            "scheduler_handle",
            "open_file",
            "mutable_runtime_service",
        }
    )
