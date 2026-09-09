# ISO 33401:2024 Conformance Map

**ISO 33401:2024**, *Reference materials: Contents of certificates, labels and accompanying
documentation*, is the standard DRMD implements. Its Table 1 lists every item of information a
product information sheet or a reference material certificate must contain, and at which
requirement level.

This chapter is the audit trail: for each row of Table 1, where the information lives in a DRMD
document, and what enforces it. Use it to answer the question an assessor will ask, *show me
where this requirement is met.*

!!! info "How this standard relates to the others"
    **ISO 33401:2024** replaced ISO Guide 31:2015 and is complementary to **ISO 17034:2016**,
    *General requirements for the competence of reference material producers*. ISO 17034 governs
    how a producer works; ISO 33401 governs what the resulting document says. ISO 33401 also
    references **ISO Guide 35:2017** (characterisation, homogeneity and stability) and
    **ISO/IEC Guide 98-3**, the GUM, for the expression of measurement uncertainty.

---

## Requirement levels

ISO 33401:2024, Table 1 uses four levels, and DRMD maps each to a Schematron severity so that a
validation report can be read against the standard directly.

| ISO level | Schematron `role` | Meaning |
|---|---|---|
| Mandatory | `error` | Required without exception |
| Mandatory whenever applicable | `conditional-error` | Required if it applies to this material; the producer judges applicability |
| Recommended | `warning` | Not required, but expected in a good document |
| Optional | *(no rule)* | Accepted when present, never flagged when absent |

---

## Table 1, row by row

Columns follow ISO 33401:2024, Table 1: **PIS** is the product information sheet, **RMC** is the
RM certificate.

### 5.2 (Information required in the RM document (both types))

| # | Requirement | PIS | RMC | Where it lives in DRMD | Enforced by |
|---|---|---|---|---|---|
| 5.2.2 | Title of the document | Mandatory | Mandatory | `administrativeData/coreData/titleOfTheDocument` | XSD enumeration + **DRMD-001** |
| 5.2.3 | Unique identifier of the RM | Mandatory | Mandatory | `materials/material/materialIdentifiers/materialIdentifier` | **DRMD-016** (error) |
| 5.2.4 | Name of the RM | Mandatory | Mandatory | `materials/material/name` | XSD + **DRMD-002**, **DRMD-007** |
| 5.2.5 | Name and contact details of the RM producer | Mandatory | Mandatory | `administrativeData/referenceMaterialProducer` (`name`, `contact`) | XSD + **DRMD-010** |
| 5.2.6 | Intended use | Mandatory | Mandatory | `statements/intendedUse` | XSD + **DRMD-004** |
| 5.2.7 | Minimum sample size | Mandatory whenever applicable | Mandatory whenever applicable | `materials/material/minimumSampleSize` | **DRMD-008** (conditional-error) |
| 5.2.8 | Period of validity | Mandatory | Mandatory | `administrativeData/coreData/validity` | XSD + **DRMD-012** |
| 5.2.9 | Commutability | Mandatory whenever applicable | Mandatory whenever applicable | `statements/commutability` | **DRMD-013** (conditional-error) |
| 5.2.10 | Storage information | Mandatory | Mandatory | `statements/storageInformation` | XSD + **DRMD-005** |
| 5.2.11 | Instructions for handling and use | Mandatory | Mandatory | `statements/instructionsForHandlingAndUse` | XSD + **DRMD-006** |
| 5.2.12 | Document components | Mandatory | Mandatory | The XML document itself, see the note below | Satisfied structurally |
| 5.2.13 | Document version | Mandatory | Mandatory | `administrativeData/coreData/documentVersion` | XSD + **DRMD-011** |
| 5.2.14 | Measurement procedures for operationally defined measurands | Mandatory whenever applicable | Mandatory whenever applicable | `propertiesList/properties/procedures` | **DRMD-014** (conditional-error) |
| 5.2.15 | Property of interest | Mandatory | Mandatory | `propertiesList/properties/results/result` | **DRMD-003**, **DRMD-009** |

### 5.3 (Information required in an RM certificate)

These are the rows where the two document types differ. They are what makes a certificate a
certificate.

| # | Requirement | PIS | RMC | Where it lives in DRMD | Enforced by |
|---|---|---|---|---|---|
| 5.3.2 | Description of the material | Recommended | **Mandatory** | `materials/material/description` | **RMC-011** (error) / **PIS-005** (warning) |
| 5.3.3 | Property value and associated uncertainty | Optional | **Mandatory** | `properties[@isCertified='true']` with `si:measurementUncertaintyUnivariate` on each value | **RMC-002**, **RMC-006** … **RMC-009** |
| 5.3.4 | Metrological traceability | Optional | **Mandatory** | `statements/metrologicalTraceability` | **RMC-001** (error) |
| 5.3.5 | Name and function of the RM producer's approving officer | Optional | **Mandatory** | `administrativeData/respPersons/dcc:respPerson`, `dcc:person/dcc:name` for the name, `dcc:role` for the function | **RMC-010** (name) + **RMC-012** (function) |

### 5.4 (Other useful information)

| # | Requirement | PIS | RMC | Where it lives in DRMD | Enforced by |
|---|---|---|---|---|---|
| 5.4.2 | Measurement procedures for non-operationally defined measurands | Recommended | Recommended | `propertiesList/properties/procedures` | **RMC-005** (warning); also covered by **DRMD-014** |
| 5.4.3 | Health and safety information | Recommended | Recommended | `statements/healthAndSafetyInformation` | **DRMD-015** (warning) |
| 5.4.4 | Subcontractors | Optional | Optional | `statements/subcontractors` | XSD element, no rule |
| 5.4.5 | Indicative values | Optional | Optional | A `properties` block with `isCertified` false or omitted | XSD structure, no rule |
| 5.4.6 | Legal notice | Optional | Optional | `statements/legalNotice` | XSD element, no rule |
| 5.4.7 | Reference to a certification report | Optional | Optional | `statements/referenceToCertificationReport` | XSD element, no rule |

---

## Three rows that need explaining

### 5.2.3 (the identifier of the RM is not the identifier of the document)

This is the requirement most often mapped to the wrong element.

`coreData/uniqueIdentifier` identifies **the document**. ISO 33401:2024, 5.2.3 asks for the
unique identifier of **the reference material**: "a combination of a product code and a batch
number", such as `NMIJ CRM 7305-a` or `ERM-AC110`, distinguishable from any other RM issued by
the same producer.

They cannot be the same field, because one document may cover several materials, and one material
is described by successive document revisions. In DRMD the RM identifier is
`material/materialIdentifiers`, and **DRMD-016** requires it.

```xml
<drmd:materialIdentifiers>
  <drmd:materialIdentifier id="matid_product">
    <drmd:scheme>ProductCode</drmd:scheme>
    <drmd:value>EXA-1a</drmd:value>
  </drmd:materialIdentifier>
  <drmd:materialIdentifier id="matid_batch">
    <drmd:scheme>Batch</drmd:scheme>
    <drmd:value>2026-03-017</drmd:value>
  </drmd:materialIdentifier>
</drmd:materialIdentifiers>
```

ISO 33401:2024, 5.2.3 also asks that where each unit is individually characterised, the document
carry an additional identifier such as a serial number for that unit. Add it as a further
`materialIdentifier` with its own scheme.

### 5.2.12 (document components)

ISO 33401:2024 requires that an RM document be arranged so that all its components are
recognisable as part of the whole, and that the end is clearly marked. The example given in the
standard is a page number and a total page count.

A DRMD instance meets this by being what it is: a single well-formed XML document with exactly
one root element. Its start and end are explicit, and every component is inside it by
construction. `@schemaVersion` states which specification the components follow,
`documentVersion` states which revision of the content they belong to, and `uniqueIdentifier`
binds them all to one instance.

No Schematron rule exists for 5.2.12, because an assertion that always holds would only add noise
to every validation report. Two things are still worth doing:

* Where you also publish a human-readable rendition, embed it in `drmd:document` or reference it
  from `statements/referenceToCertificationReport`, so the two forms travel together.
* Where a PDF is generated from a DRMD, apply 5.2.12 to that PDF in the ordinary way, page
  numbering with a total, and a clear end marker.

### 5.3.5 (the function, not only the name)

ISO 33401:2024, 5.3.5 asks for "the name **and function** of an officer representing the RM
producer and accepting responsibility for the contents of the certificate". Both halves are
required.

`dcc:respPerson` provides both: `dcc:person/dcc:name` for the name, which the DCC schema already
makes mandatory, and `dcc:role` for the function, which it does not. **RMC-012** requires at
least one responsible person in a certificate to state a `dcc:role`.

The NOTE to 5.3.5 allows the officer's name to be the name of the responsible organisation, so a
role such as `Head of Division, Inorganic Reference Materials`, naming the unit rather than a
job title, satisfies the requirement.

---

## Clause 6 (Labels)

ISO 33401:2024, Clause 6 governs the **physical label** on the container of an individual RM unit.
It is not a data field, so it is out of scope for the schema, but it is squarely in scope for a
producer, and it depends on getting 5.2.3 right.

Clause 6 requires the label to:

* be securely attached, and to stay legible and intact under the defined storage and handling
  conditions for the whole period of validity;
* allow the appropriate RM document to be identified, **by the unique RM identifier of 5.2.3**;
* include the name of the RM and the producer where space allows;
* carry health, safety, environmental and transport information where appropriate.

Clause 6 also advises that **neither certified nor indicative property values should appear on the
label**, so that the material cannot be used without the RM document having been read.

The practical consequence for DRMD: the identifier printed on the label and the value in
`material/materialIdentifiers` must be **byte-identical**, including case, punctuation and
separators. That string is the only link between the physical unit in someone's hand and the
digital document, and normalising it on one side breaks the match.

---

## Requirements that are deliberately absent

Some ISO 17034 requirements describe how a producer operates rather than what a document says:
production planning, production control, distribution, management of non-conforming work,
handling of complaints. They are audited against the producer's quality system, not against a
DRMD instance, and no element or rule corresponds to them.

Similarly, ISO 33401:2024 does not require DRMD to check whether a value is *correct*. No schema
can. Validation establishes that the document says what the standard requires it to say; the
truth of the values rests on the producer's competence under ISO 17034.

---

## Self-assessment

Before publishing, run the validator and read the report against the table above.

```bash
python tools/validate.py my-document.xml --json report.json
```

| Report shows | Table 1 status |
|---|---|
| No findings | Every mandatory and recommended item is present |
| Warnings only | Compliant. Recommended items are missing, 5.4.2, 5.4.3 |
| Conditional errors | Decide, per material, whether each applies. If it does, add it. If not, say so in the document. |
| Any hard error | Not compliant with ISO 33401:2024, Table 1. Do not publish. |

The [Implementation Checklists](checklists.md) turn this into a per-role list you can work
through.
