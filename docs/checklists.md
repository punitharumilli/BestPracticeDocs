# Implementation Checklists

Four checklists, one per role. Work through the one that applies to you before publishing,
shipping or signing off.

Everything here is checkable. Where a validation rule covers an item, its identifier is given, so
you can trace a tick back to a line in a validation report. Where nothing checks it automatically,
the item says so, those are the ones that need a person.

!!! tip "Run the validator first"
    ```bash
    pip install lxml
    python tools/validate.py my-document.xml --json report.json
    ```
    It reports everything marked with a rule identifier below. The checklists then cover what the
    tools cannot see.

Downloadable PDF versions are linked in each section.

---

## 16.1 Reference Material Producer

Everything a published DRMD must satisfy.

[Download Producer PDF](assets/pdfs/producer_checklist.pdf){ .md-button .md-button--primary }

### A. Document identity

- [ ] The root element carries `@schemaVersion` (currently `1.0.0`).
- [ ] `titleOfTheDocument` is the correct type. A certificate that is not certified is worse than
      no certificate. **(DRMD-001)**
- [ ] `uniqueIdentifier` is a new UUID for this revision, never reused from a previous one.
- [ ] `documentVersion` is stated, and it changed when the content changed. **(DRMD-011)**
- [ ] `validity` uses exactly one of the three forms, and the choice matches how the material
      actually degrades. **(DRMD-012)**
- [ ] Producer `name`, `contact` and a structured `location` are present. **(DRMD-010)**
- [ ] For a certificate: `respPersons` names the approving officer **(RMC-010)** and at least one
      person states a `dcc:role`, which is their function. **(RMC-012)**

### B. The material

- [ ] Every material has a `name`. **(DRMD-007)**
- [ ] Every material has at least one `materialIdentifier`, the unique identifier of the RM
      itself, not the document. **(DRMD-016)**
- [ ] Where units are batched, the batch or lot number is a second identifier.
- [ ] **The identifier matches the container label byte for byte**, case, punctuation,
      separators. *Nothing checks this. It is the only link between the physical unit and this
      document.*
- [ ] `minimumSampleSize` is stated, or the document says why it does not apply. **(DRMD-008)**
- [ ] For a certificate: every material has a `description`. **(RMC-011)**

### C. The data

- [ ] Every `properties` block declares `@isCertified` explicitly, rather than relying on the
      default. A reader should not have to know the default.
- [ ] A certificate has at least one block with `@isCertified="true"`. **(RMC-002)**
- [ ] A product information sheet has **no** block with `@isCertified="true"`. **(PIS-001, PIS-003)**
- [ ] Every certified value carries an uncertainty. **(RMC-006 … RMC-009)**
- [ ] Inside `si:expandedMU`, both `coverageFactor` and `coverageProbability` are present.
      D-SI requires both, and omitting one is an XSD error.
- [ ] The meaning of the uncertainty is stated once, in the `properties` description: what it
      covers, and at what coverage factor.
- [ ] Every unit is a D-SI string, `\gram`, not `g`; `\milli\gram\kilo\gram\tothe{-1}`, not
      `mg/kg`. *Nothing checks this: `si:unit` is an unrestricted string.*
- [ ] Any unit D-SI cannot express is reported through `si:hybrid` with an SI-encoded sibling, and
      defined with `dcc:nonSIUnit` and `dcc:nonSIDefinition`.
- [ ] Every certified value carries an `si:quantityTypeQUDT`.
- [ ] Every analyte row carries a `propertyIdentifier` (CAS, InChI, or a documented scheme).
- [ ] `procedures` are documented, or the document says why they do not apply. **(DRMD-014)**
- [ ] No `NaN` appears in any certified value.

### D. The statements

- [ ] `intendedUse` says what the material is for **and what it is not for**. **(DRMD-004)**
- [ ] `storageInformation` gives actionable conditions, not "store appropriately". **(DRMD-005)**
- [ ] `instructionsForHandlingAndUse` covers preparation, and states that the certified values
      apply only at or above the minimum sample size. **(DRMD-006)**
- [ ] `commutability` is stated, or the document says it was not assessed. **(DRMD-013)**
- [ ] For a certificate: `metrologicalTraceability` names the reference the values are traceable
      to, not just the word "traceable". **(RMC-001)**
- [ ] `healthAndSafetyInformation` is present, including whether a safety data sheet exists.
      **(DRMD-015)**

### E. Before you publish

- [ ] `python tools/validate.py` reports no error and no conditional error.
- [ ] Every warning has been considered and consciously accepted.
- [ ] No text field contains a placeholder, `TBD`, `XXX`, `lorem ipsum`, or an empty
      `dcc:content`. *Nothing checks this.*
- [ ] Where a PDF is embedded, it is the same revision as the XML.
- [ ] The document is signed **after** it is final, and not edited afterwards.

---

## 16.2 Software and LIMS developers

[Download Software PDF](assets/pdfs/software_checklist.pdf){ .md-button .md-button--primary }

### A. Parsing

- [ ] Elements are matched by namespace URI **plus local name**, never by prefix.
- [ ] The DRMD namespace is handled as the URN `urn:drmd:schema`, and nothing tries to fetch it.
- [ ] External entity resolution and DTD loading are **disabled** (XXE protection).
- [ ] Document size and entity expansion are capped before parsing, not after.
- [ ] Unknown optional elements are ignored rather than causing a failure, so a minor version
      increment does not break the importer.
- [ ] The major version in `@schemaVersion` is checked, and an unknown major version is refused
      rather than parsed optimistically.

### B. Validation

- [ ] XSD validation resolves imports from the local `supporting/` bundle via `catalog.xml`,
      not from the network.
- [ ] Schematron validation runs after XSD validation, and both must pass.
- [ ] The pipeline branches on the Schematron `@role`: `error` and `conditional-error` block,
      `warning` does not.
- [ ] A conditional error is surfaced to a person as a question, *does this apply?*, not as a
      flat rejection.
- [ ] Rule identifiers are stored with each finding, so a report stays readable later.
- [ ] D-SI unit strings are checked with your own regular expression. **No layer of DRMD
      validation does this.**

### C. Data handling

- [ ] Quantity extraction handles all payload types: `si:real`, `si:realListXMLList`, `si:hybrid`,
      `si:complex`, `si:constant`, `dcc:noQuantity`, `dcc:charsXMLList`.
- [ ] For `si:hybrid`, the SI-encoded sibling is used for calculation and the non-SI sibling for
      display.
- [ ] `si:realListXMLList` is parsed as whitespace-separated lists, and mismatched list lengths
      are reported rather than silently truncated.
- [ ] Values are stored at full precision. Rounding happens at display time only.
- [ ] Certified and non-certified values are kept distinct in the data model, and a non-certified
      value can never be presented as certified.
- [ ] Language selection falls back predictably, and the user can see which language they are
      reading.
- [ ] Deduplication uses `materialIdentifiers` for materials and `uniqueIdentifier` for documents.
      *These are different indexes, see [Cross-references](cross_references.md).*

---

## 16.3 Instrument vendors

[Download Instrument PDF](assets/pdfs/instrument_checklist.pdf){ .md-button .md-button--primary }

### A. Ingestion

- [ ] Materials map to the internal library by `materialIdentifiers`, not by name.
- [ ] Only blocks with `@isCertified="true"` are used for calibration.
- [ ] Analytes map through `propertyIdentifier`; where an `si:quantityTypeQUDT` is present, it is
      used to confirm the quantity kind matches what the instrument expects.
- [ ] A value whose unit cannot be parsed as D-SI is refused, not guessed at.

### B. Operational safety

- [ ] `minimumSampleSize` is shown, and a planned test portion below it raises a warning.
- [ ] `validity` is checked against the current date, and an expired material is blocked from
      calibration use.
- [ ] Storage and handling instructions are shown to the operator before use.
- [ ] A material with no certified block cannot be selected as a calibration standard.

### C. Trust

- [ ] For Profile C, signatures are verified cryptographically, not merely checked for presence.
- [ ] The embedded PDF is reachable from the UI, so an operator can see the human-readable form.
- [ ] A failed signature verification is surfaced clearly and is not silently ignored.

---

## 16.4 Auditors and assessors

[Download Auditor PDF](assets/pdfs/auditor_checklist.pdf){ .md-button .md-button--primary }

### A. Conformance evidence

- [ ] A validation report exists for the document, showing no error and no conditional error.
- [ ] Every ISO 33401:2024, Table 1 row can be traced to an element, see the
      [ISO 33401:2024 Conformance Map](iso_mapping.md).
- [ ] Where a conditional requirement was treated as not applicable, the justification is recorded
     , ideally in the document, and in the producer's quality records either way.

### B. Governance

- [ ] `titleOfTheDocument` matches what the material actually is.
- [ ] The approving officer is named **and their function is stated**. **(RMC-010, RMC-012)**
- [ ] The version and identifier scheme make revisions traceable: a revised document has a new
      `uniqueIdentifier` and a changed `documentVersion`, while the material identifiers stayed
      the same.

### C. Measurement quality

- [ ] Certified values are clearly distinguished from indicative ones, by `@isCertified` **and**
      by the block name a person will read.
- [ ] The traceability statement names the reference the values are traceable to, and how.
- [ ] The uncertainty statement says what the uncertainty covers, not just the coverage factor.
- [ ] The measurement procedures are identified well enough to be repeated.

### D. The physical unit

- [ ] The identifier on the container label matches `materialIdentifiers` exactly.
- [ ] The label does not carry certified or indicative property values (ISO 33401:2024, Clause 6),
      so the material cannot be used without the document having been read.
- [ ] The label is legible and intact, and can be expected to stay so for the period of validity.
