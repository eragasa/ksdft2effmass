EnergyReference verification evidence
=====================================

Scope and represented DataObject
--------------------------------

``EnergyReference`` is the frozen, slotted metadata DataObject used by
``OperatorRecord`` to identify an energy reference. It stores exactly:

.. code-block:: text

   zero: str
   unit: str

``zero`` is a textual identifier for the energy-origin convention, for example
``"explicit zero"`` or ``"valence-band maximum"``. It is not a numerical energy
offset. ``unit`` is a textual energy-unit label, for example ``"eV"`` or
``"hartree"``. The object stores no ``value``, ``offset``, ``energy_offset``, or
``reference_energy`` field and accepts no corresponding constructor argument.

Construction and intrinsic invariants
-------------------------------------

Both fields accept Python ``str`` instances and are retained unchanged. This
includes exact case, spacing, punctuation, hyphenation, and any ``str`` subclass
identity. There is no canonicalization: construction performs no trimming, case
folding, vocabulary lookup, alias resolution, unit normalization, dimensional
analysis, unit conversion, or interpretation of the zero convention.

Wrong semantic types—including ``None``, Booleans, integers, floats, bytes, and
arbitrary objects—raise ``TypeError`` independently for each field. Values are
not passed through ``str()``. A correctly typed empty string raises ``ValueError``.
Because no trimming occurs, a whitespace-only string is nonempty and remains
accepted metadata under the current contract. This boundary validates only
textual metadata structure; it does not validate whether a label is recognized
or physically appropriate.

The object is frozen and slotted. ``zero`` and ``unit`` cannot be reassigned,
arbitrary dynamic attributes cannot be added, and instances have no per-instance
``__dict__``. Equality is exact structural equality across both stored fields.
It is case-, punctuation-, spacing-, and spelling-sensitive. Exact equality
therefore expresses metadata identity, not physical equivalence between two
energy references. Hash behavior is not assigned by this evidence surface.

Ownership boundaries
--------------------

``EnergyReference`` owns only its two intrinsic nonempty-string invariants and
exact value semantics. It does not align energy zeros, compare references,
normalize or convert units, apply an energy shift, or determine physical
equivalence. Exact record-to-record energy-unit and zero-convention compatibility
belongs to ``OperatorRecordCompatibilityAnalyzer``.

``EnergyReference`` exposes no standalone ``serialize``, ``deserialize``,
``to_json``, ``from_json``, ``to_dict``, or ``from_dict`` API. Its nested
schema-version-1 JSON representation belongs exclusively to
``OperatorRecordJsonSerializer``. Serializer malformed-payload tests—including
the historical forbidden ``energy_reference.value`` field—remain on that
ActionObject's evidence surface and are not duplicated here.

Software-verification traceability
----------------------------------

The target software-verification facets own one executable test for each stable
evidence identifier:

* ``test__EnergyReference__construction.py``:

  * ``SV-ER-001`` — public construction and exact stored-field mapping;
  * ``SV-ER-002`` — exact preservation of the zero-convention string;
  * ``SV-ER-003`` — exact preservation of the energy-unit string;
  * ``SV-ER-004`` — numerical-offset constructor and stored-state exclusion;
  * ``SV-ER-005`` — absence of standalone serialization APIs.

* ``test__EnergyReference__invariants.py``:

  * ``SV-ER-006`` — invalid ``zero`` semantic-type rejection;
  * ``SV-ER-007`` — empty ``zero`` rejection;
  * ``SV-ER-008`` — invalid ``unit`` semantic-type rejection;
  * ``SV-ER-009`` — empty ``unit`` rejection.

* ``test__EnergyReference__value_semantics.py``:

  * ``SV-ER-010`` — frozen and slotted stored state;
  * ``SV-ER-011`` — exact structural equality;
  * ``SV-ER-012`` — field-sensitive and case-sensitive inequality.

These tests use only the ``software_verification`` marker. Synthetic metadata are
passed directly to the public constructor; no DFT, Wannier, experimental, or
impurity calculation supplies the values. A pass means the Python object
satisfies its documented construction, invariant, ownership, error-taxonomy,
immutability, and equality contracts. A failure may indicate an implementation
regression, documentation mismatch, or evidence defect requiring investigation;
it does not by itself establish a physical-model error or scientific invalidity.

VVUQ and cross-language status
------------------------------

``EnergyReference`` owns no numerical algorithm, so numerical verification is
not applicable to this migration and no numerical-verification identifier is
assigned. The software evidence does not establish that an energy-origin
convention or unit is suitable for a declared scientific use, that two labels are
physically equivalent, or that a represented Hamiltonian has a correct energy
reference.

Scientific validation has not been performed. Uncertainty quantification has not
been performed. A two-string validated struct is conceptually portable to Rust,
but no Rust implementation or Python/Rust conformance evidence has been
performed or demonstrated.
