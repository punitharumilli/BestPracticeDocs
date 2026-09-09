# Materials

The **Materials** block (`materials`) is the authoritative catalogue of the physical reference material(s) that a DRMD document describes. It answers, in a machine-readable way:

- **What** material(s) exist in this document (names, descriptions).
- **How** they are classified (optional, repeatable material classes).
- **How** they are identified externally (IDs such as BAM/CRM code, batch/lot, ROR, internal IDs).
- **What** sample amount(s) are relevant for using the material (e.g., minimum sample size; optional additional item quantities).

## Structure at a Glance

```mermaid
graph TD
    MAT["materials<br/><i>drmd:materialListType [1..1]</i>"]
    M["material<br/><i>drmd:materialType [1..∞]</i>"]

    MAT --> M

    M --> NAME["name<br/><i>dcc:textType [1..1]</i>"]
    M --> DESC["description<br/><i>dcc:richContentType [0..1]</i>"]
    M --> MC["materialClass<br/><i>drmd:materialClassType [0..∞]</i>"]
    M --> MSS["minimumSampleSize<br/><i>dcc:itemQuantityListType [0..1]</i>"]
    M --> IQ["itemQuantities<br/><i>dcc:itemQuantityListType [0..1]</i>"]
    M --> MID["materialIdentifiers<br/><i>drmd:materialIdentifierListType [0..1]</i>"]

    MC --> REF["reference [1..1]"]
    MC --> CID["classID [1..1]"]
    MC --> LNK1["link [0..1]"]

    MID --> MI["materialIdentifier<br/><i>drmd:identifierType [1..∞]</i>"]
    MI --> SCH["scheme [1..1]"]
    MI --> VAL["value [1..1]"]
    MI --> LNK2["link [0..1]"]

    style MAT fill:#e8eaf6,color:#000,stroke:#283593
    style M fill:#c5cae9,color:#000,stroke:#3949ab
    style NAME fill:#e8eaf6,stroke:#3f51b5
    style DESC fill:#e8eaf6,stroke:#3f51b5
    style MC fill:#e8eaf6,stroke:#3f51b5
    style MSS fill:#e8eaf6,stroke:#3f51b5
    style IQ fill:#e8eaf6,stroke:#3f51b5
    style MID fill:#e8eaf6,stroke:#3f51b5
    style REF fill:#e3f2fd,stroke:#1565c0
    style CID fill:#e3f2fd,stroke:#1565c0
    style LNK1 fill:#e3f2fd,stroke:#1565c0
    style MI fill:#c5cae9,stroke:#3949ab
    style SCH fill:#e3f2fd,stroke:#1565c0
    style VAL fill:#e3f2fd,stroke:#1565c0
    style LNK2 fill:#e3f2fd,stroke:#1565c0
```

The six child elements of each `material` entry are:

| Child Element | Type | Required | Description |
|---------------|------|----------|-------------|
| **name** | `dcc:textType` | Mandatory | Human-readable product name |
| **description** | `dcc:richContentType` | CRM: Mandatory / ProductInformationSheet: Optional | Physical form, composition, matrix information |
| **materialClass** | `drmd:materialClassType` | Optional (repeatable) | Classification taxonomy assignment |
| **minimumSampleSize** | `dcc:itemQuantityListType` | Mandatory whenever applicable | Minimum quantity for valid use |
| **itemQuantities** | `dcc:itemQuantityListType` | Optional | Additional physical descriptors |
| **materialIdentifiers** | `drmd:materialIdentifierListType` | **Mandatory** (ISO 5.2.3) | The unique identifier of the RM itself |

!!! warning "Dual Validation Required"
    The DRMD schema uses a **dual-profile architecture**. The XSD defines the structure, but profile-specific mandatory requirements (e.g., `description` being mandatory for CRM documents) are enforced by the companion **Schematron business rules** (`drmd-business-rules.sch`). Full compliance requires passing **both** validations.

## 4.1 Purpose and Use

??? abstract "Who Uses This Block?"

    | Stakeholder | How They Use the Materials Block |
    |-------------|-------------------------------|
    | **Reference Material Producer (RMP)** | Publishes the canonical product identity (name + identifiers) and how to handle it (sample size). Ensures traceability between digital document and physical packaging/labels, catalog entries, and internal inventory systems. |
    | **Laboratories / End Users** | Know exactly which material the certified values apply to (especially crucial when there are multiple materials, lots, forms). Determine minimum sample size to plan method suitability, sample preparation, and replicate strategy. |
    | **Instrument / Machine Manufacturers** | Can ingest standardized material metadata to preconfigure methods. Map "material name/identifier" to internal instrument libraries. Display correct sample requirements and warnings in UI. |
    | **Software Developers / LIMS / ELN** | Use `materials/material/materialIdentifiers` to match DRMD content to database entities (product tables, lots, customer inventory). Use DCC quantity structures to reuse existing parsing/validation for numeric values and units. |
    | **Regulators / Auditors** | Verify the document refers to a clearly identified material, and the declared minimum sample size and identifiers are consistent with external references and packaging. |

!!! tip "Handling Multiple Materials"
    When a DRMD contains multiple `drmd:material` entries, the identifiers declared in `/drmd:materials/drmd:material/materialIdentifiers` should be treated as the **canonical keys** for linking downstream information. In the next chapter (Properties), software can use these material identifiers as stable references (e.g., via `@id`/`@refId` patterns) to associate each set of properties with the correct material.

## 4.2 Materials List

| Property | Value |
|----------|-------|
| **Element** | `drmd:materials` |
| **Path** | `/drmd:digitalReferenceMaterialDocument/drmd:materials` |
| **Type** | `drmd:materialListType` |
| **Cardinality** | **Required** `[1..1]` at root |
| **Contents** | One or more `drmd:material` |

**Purpose:** The top-level container that holds the catalogue of all physical reference materials covered by this DRMD document.

!!! tip "Best Practices"
    - Include **exactly one** `drmd:material` when the DRMD is for a single CRM/RM product.
    - Use **multiple** `drmd:material` entries when:
        - The DRMD certifies multiple distinct materials.
        - The product is a kit with distinct components.
        - Variants/forms are treated as separate "materials" with separate sample size constraints or identifiers.
    - Keep identifiers **stable across releases**; if you revise the document, avoid changing identifiers unless the material itself changes.

```xml
<drmd:materials>
  <drmd:material>
    <!-- ... material details ... -->
  </drmd:material>
</drmd:materials>
```

!!! danger "Schematron Rule: DRMD-002"
    Every DRMD document **MUST** contain at least one `material` entry in the materials catalogue (ISO 33401:2024, §5.2.4). Severity: **Error**. the document is non-compliant without at least one material.

## 4.3 Material Entry (`material`)

| Property | Value |
|----------|-------|
| **Element** | `drmd:material` |
| **Path** | `/drmd:digitalReferenceMaterialDocument/drmd:materials/drmd:material` |
| **Type** | `drmd:materialType` |
| **Cardinality** | `[1..∞]` within `drmd:materials` |

**Purpose:** Each `material` element represents a single physical reference material. It encapsulates everything needed to identify, describe, classify, and quantify the material.

```mermaid
graph LR
    M["material"] --> NAME["name<br/><i>Required</i>"]
    M --> DESC["description<br/><i>CRM: Required</i>"]
    M --> MC["materialClass<br/><i>0..∞</i>"]
    M --> MSS["minimumSampleSize<br/><i>Conditional</i>"]
    M --> IQ["itemQuantities<br/><i>Optional</i>"]
    M --> MID["materialIdentifiers<br/><i>Optional</i>"]

    style M fill:#e8eaf6,color:#000,stroke:#3f51b5
    style NAME fill:#c5cae9,stroke:#3f51b5
    style DESC fill:#c5cae9,stroke:#3f51b5
    style MC fill:#e8eaf6,stroke:#9fa8da
    style MSS fill:#fff3e0,stroke:#ff9800
    style IQ fill:#e8eaf6,stroke:#9fa8da
    style MID fill:#e8eaf6,stroke:#9fa8da
```

### 4.3.1 Name (`name`)

| Property | Value |
|----------|-------|
| **Path** | `.../drmd:material/drmd:name` |
| **Type** | `dcc:textType` |
| **Cardinality** | **Required** `[1..1]` |

**Purpose:** The human-readable primary name of the material (e.g., "BAM-M308a", "AlZnMgCu1.5", "CRM XYZ-123").

??? abstract "Who Uses This Element?"

    | Stakeholder | How They Use It |
    |-------------|-----------------|
    | **Producer** | Public-facing product name |
    | **Lab** | Selection of correct material in procedures and reports |
    | **Software** | Display label and user selection (not a stable key, use identifiers for matching) |

!!! tip "Best Practices"
    - Provide at least one `dcc:content`.
    - If multilingual usage is expected, include multiple `dcc:content` entries with `@lang`.
    - Keep naming consistent with packaging/catalog.
    - Keep the "material name" short; put extended marketing/narrative into `drmd:description`.

```xml
<drmd:name>
  <dcc:content lang="en">Aluminium Alloy Disk</dcc:content>
  <dcc:content lang="de">Aluminiumscheibe (Legierung)</dcc:content>
</drmd:name>
```

!!! danger "Schematron Rule: DRMD-007"
    Every material entry **MUST** include a `name` element (ISO 33401:2024, §5.2.4). Severity: **Error**.

### 4.3.2 Description (`description`)

| Property | Value |
|----------|-------|
| **Path** | `.../drmd:material/drmd:description` |
| **Type** | `dcc:richContentType` |
| **Cardinality** | CRM: **Mandatory** / ProductInformationSheet: **Optional** `[0..1]` |

**Purpose:** Structured descriptive content including narrative text, attachments, and formulas. Typically used for form factor, composition notes, packaging form, and hazards summary pointers.

!!! tip "Best Practices"
    - Use description to capture: physical form, dimensions, matrix, appearance, preparation hints.
    - Keep long legal/health & safety statements in `drmd:statements` (not here), but you may reference them.
    - Use `dcc:content` for narrative.
    - Use `dcc:file` for images/spec sheets only when needed (otherwise keep DRMD lean).
    - Keep units/numerical constraints in `itemQuantities` or results sections rather than burying them only in narrative text.

=== "Text-only Example"

    ```xml
    <drmd:description>
      <dcc:name>
        <dcc:content lang="en">Material description</dcc:content>
      </dcc:name>
      <dcc:content lang="en">
        The reference material is provided as discs
        (approx. 65 mm diameter, 30 mm height).
        Intended for establishing/checking calibration
        of spark OES and XRF methods for similar matrices.
      </dcc:content>
    </drmd:description>
    ```

=== "With Attachment"

    ```xml
    <drmd:description>
      <dcc:content lang="en">See the attached technical drawing
        for geometry and tolerances.</dcc:content>
      <dcc:file>
        <dcc:fileName>BAM-M308a-drawing.pdf</dcc:fileName>
        <dcc:mimeType>application/pdf</dcc:mimeType>
        <dcc:dataBase64>BASE64_PDF_BYTES_HERE==</dcc:dataBase64>
      </dcc:file>
    </drmd:description>
    ```

!!! danger "Schematron Rule: RMC-011"
    Reference Material Certificates **MUST** include a description for each material (ISO 33401:2024, §5.3.2). Severity: **Error**. This rule does **not** apply to `productInformationSheet` documents, but a description is still recommended (PIS-005, Severity: **Warning**).

## 4.4 Material Classification (`materialClass`)

| Property | Value |
|----------|-------|
| **Path** | `.../drmd:material/drmd:materialClass` |
| **Type** | `drmd:materialClassType` |
| **Cardinality** | **Optional**, repeatable `[0..∞]` |

**Purpose:** A classification entry that ties the material to a classification scheme and a class identifier within that scheme.

```mermaid
graph LR
    MC["materialClass"] --> REF["reference<br/><i>Required</i>"]
    MC --> CID["classID<br/><i>Required</i>"]
    MC --> LNK["link<br/><i>Optional</i>"]

    style MC fill:#e8eaf6,color:#000,stroke:#3f51b5
    style REF fill:#c5cae9,stroke:#3f51b5
    style CID fill:#c5cae9,stroke:#3f51b5
    style LNK fill:#e8eaf6,stroke:#9fa8da
```

| Child Element | Type | Required | Description |
|---------------|------|----------|-------------|
| **reference** | `dcc:notEmptyStringType` | Yes | Names the classification scheme (e.g., ISO, UNS, InternalCatalog, ECHA) |
| **classID** | `dcc:notEmptyStringType` | Yes | The code within that scheme |
| **link** | `xs:anyURI` | No | A resolvable URL to the scheme definition |

**Technical Attributes:** `@id` (xs:ID), `@refId` (xs:IDREFS), `@refType` (drmd:refTypesType), all optional.

??? abstract "Who Uses This Element?"

    | Stakeholder | How They Use It |
    |-------------|-----------------|
    | **Producer** | Align product with internal classification or external taxonomy |
    | **Labs** | Group/filter materials by matrix/type (e.g., alloy class, soil class) |
    | **Manufacturers/Software** | Enable automated method suggestions or UI filters by class |

!!! tip "Best Practices"
    - Use `reference` for the scheme name (e.g., ISO, UNS, InternalCatalog, ECHA).
    - Use `classID` for the scheme's code.
    - Provide `link` when the scheme/class is resolvable online.

```xml
<drmd:materialClass id="mc-1">
  <drmd:reference>ISO 12103-1</drmd:reference>
  <drmd:classID>A2 Fine Test Dust</drmd:classID>
  <drmd:link>https://www.iso.org/standard/30109.html</drmd:link>
</drmd:materialClass>
```

## 4.5 Sample Size and Quantities

### 4.5.1 Minimum Sample Size (`minimumSampleSize`)

| Property | Value |
|----------|-------|
| **Path** | `.../drmd:material/drmd:minimumSampleSize` |
| **Type** | `dcc:itemQuantityListType` |
| **Cardinality** | **Mandatory whenever applicable** `[0..1]` |

**Purpose:** The minimum quantity of sample needed to use the material as intended. Often depends on the method family; if so, use multiple `dcc:itemQuantity` entries with names/descriptions inside the quantity structure.

??? abstract "Who Uses This Element?"

    | Stakeholder | How They Use It |
    |-------------|-----------------|
    | **Labs** | Compliance with certified use conditions; planning sample prep |
    | **Producer** | Communicate minimum amount for valid use |
    | **Software / Instruments** | Warnings if planned sample mass/volume is below minimum |

!!! tip "Best Practices"
    - Use `si:real` for numeric sample size + unit (e.g., 0.2 g).
    - If multiple minima exist (e.g., OES vs wet chemistry), provide multiple `dcc:itemQuantity` entries and differentiate using the quantity's name/description.

=== "Simple Minimum Sample Mass"

    ```xml
    <drmd:minimumSampleSize>
      <dcc:itemQuantity>
        <si:real>
          <si:label>Minimum sample mass for wet chemical analysis</si:label>
          <si:value>0.2</si:value>
          <si:unit>\gram</si:unit>
        </si:real>
      </dcc:itemQuantity>
    </drmd:minimumSampleSize>
    ```

=== "With Uncertainty"

    ```xml
    <drmd:minimumSampleSize>
      <dcc:itemQuantity>
        <si:real>
          <si:label>Minimum sample mass</si:label>
          <si:value>0.200</si:value>
          <si:unit>\gram</si:unit>
          <si:measurementUncertaintyUnivariate>
            <si:expandedMU>
              <si:valueExpandedMU>0.005</si:valueExpandedMU>
              <si:coverageFactor>2</si:coverageFactor>
              <si:coverageProbability>0.95</si:coverageProbability>
              <si:distribution>normal</si:distribution>
            </si:expandedMU>
          </si:measurementUncertaintyUnivariate>
        </si:real>
      </dcc:itemQuantity>
    </drmd:minimumSampleSize>
    ```

!!! danger "Schematron Rule: DRMD-008"
    Each material entry **MUST** specify a `minimumSampleSize` whenever applicable to ensure representative sampling for homogeneity (ISO 33401:2024, §5.2.7). Severity: **Conditional Error**, absence may be valid if not applicable to the specific material, but absence of this field when a minimum sample size exists constitutes a violation.

### 4.5.2 Item Quantities (`itemQuantities`)

| Property | Value |
|----------|-------|
| **Path** | `.../drmd:material/drmd:itemQuantities` |
| **Type** | `dcc:itemQuantityListType` |
| **Cardinality** | **Optional** `[0..1]` |

**Purpose:** Additional quantities describing the material item (not necessarily "minimum"), such as nominal item mass, dimensions (diameter/height), number of units in package, or storage temperature limits.

!!! tip "Best Practices"
    - Use this for quantitative descriptors of the material item/package.
    - Avoid duplicating general statements that belong in `drmd:statements`.

=== "Dimensions + Mass"

    ```xml
    <drmd:itemQuantities>
      <dcc:itemQuantity>
        <si:real>
          <si:label>Diameter</si:label>
          <si:value>65</si:value>
          <si:unit>\milli\metre</si:unit>
        </si:real>
      </dcc:itemQuantity>
      <dcc:itemQuantity>
        <si:real>
          <si:label>Height</si:label>
          <si:value>30</si:value>
          <si:unit>\milli\metre</si:unit>
        </si:real>
      </dcc:itemQuantity>
      <dcc:itemQuantity>
        <si:real>
          <si:label>Approximate mass</si:label>
          <si:value>250</si:value>
          <si:unit>\gram</si:unit>
        </si:real>
      </dcc:itemQuantity>
    </drmd:itemQuantities>
    ```

=== "Non-numeric Quantity"

    ```xml
    <drmd:itemQuantities>
      <dcc:itemQuantity>
        <dcc:noQuantity>
          <dcc:content lang="en">Item quantity not specified
            (varies by batch/packaging).</dcc:content>
        </dcc:noQuantity>
      </dcc:itemQuantity>
    </drmd:itemQuantities>
    ```

## 4.6 Primitive Quantity Type (Deep Dive)

The `dcc:primitiveQuantityType` is the foundational container for every single quantitative statement in a DRMD. It is used inside both `minimumSampleSize` and `itemQuantities`. Understanding its structure is key to producing valid, interoperable data.

```mermaid
graph TD
    PQ["dcc:primitiveQuantityType"]
    PQ --> N["dcc:name<br/><i>Optional</i>"]
    PQ --> D["dcc:description<br/><i>Optional</i>"]
    PQ --> CHOICE{{"Choice (exactly 1)"}}

    CHOICE --> A["si:real<br/><i>Number + Unit</i>"]
    CHOICE --> B["dcc:noQuantity<br/><i>Structured placeholder</i>"]
    CHOICE --> C["si:realListXMLList<br/><i>List of numbers</i>"]
    CHOICE --> D2["dcc:charsXMLList<br/><i>Token list</i>"]
    CHOICE --> E["si:hybrid<br/><i>Advanced</i>"]
    CHOICE --> F["si:complex<br/><i>Rare</i>"]
    CHOICE --> G["si:constant<br/><i>Rare</i>"]
    CHOICE --> H["si:complexListXMLList<br/><i>Rare</i>"]

    style PQ fill:#e8eaf6,color:#000,stroke:#283593
    style N fill:#e3f2fd,stroke:#1565c0
    style D fill:#e3f2fd,stroke:#1565c0
    style CHOICE fill:#fff3e0,color:#000,stroke:#ff9800
    style A fill:#e8f5e9,stroke:#4caf50
    style B fill:#e8f5e9,stroke:#4caf50
    style C fill:#e8f5e9,stroke:#4caf50
    style D2 fill:#e8f5e9,stroke:#4caf50
    style E fill:#e8eaf6,stroke:#9fa8da
    style F fill:#e8eaf6,stroke:#9fa8da
    style G fill:#e8eaf6,stroke:#9fa8da
    style H fill:#e8eaf6,stroke:#9fa8da
```

!!! tip "Best Practices"
    - Provide `dcc:name` whenever a list contains multiple quantities (humans and software need labels).
    - **Default to Option A** (`si:real`) for numeric + unit (highest interoperability).
    - Use Option C (`si:realListXMLList`) only when your ecosystem supports list parsing; otherwise model multiple `dcc:itemQuantity` entries each with `si:real`.
    - Use Option B (`dcc:noQuantity`) only when numeric is truly not applicable.
    - Use `dcc:charsXMLList` for controlled vocabulary / token lists, not for numbers.
    - Treat `si:hybrid`, `si:complex`, `si:constant`, `si:complexListXMLList` as advanced/rare options.

### 4.6.1 Option A (`si:real`)

Use when you have **one number with one unit**. This is the most common and interoperable option.

```xml
<dcc:itemQuantity>
  <dcc:name><dcc:content lang="en">Minimum sample size</dcc:content></dcc:name>
  <si:real>
    <si:value>0.2</si:value>
    <si:unit>\gram</si:unit>
  </si:real>
</dcc:itemQuantity>
```

### 4.6.2 Option B (`dcc:noQuantity`)

Use when the value is **intentionally not numeric**, but you want a structured placeholder and explanation.

```xml
<dcc:itemQuantity>
  <dcc:name><dcc:content lang="en">Minimum sample size</dcc:content></dcc:name>
  <dcc:noQuantity>
    <dcc:content lang="en">Not specified; depends on method.</dcc:content>
  </dcc:noQuantity>
</dcc:itemQuantity>
```

### 4.6.3 Option C (`si:realListXMLList`)

Use when one "quantity" is naturally a **list of numbers**.

!!! danger "These elements do not repeat"
    `si:valueXMLList` and `si:unitXMLList` each appear **once** and hold a whitespace-separated
    list. Writing one element per value is invalid. The lists must be the same length, so that
    value and unit line up position by position.

```xml
<dcc:itemQuantity>
  <dcc:name><dcc:content lang="en">Recommended test portions</dcc:content></dcc:name>
  <si:realListXMLList>
    <si:valueXMLList>0.1 0.2 0.5</si:valueXMLList>
    <si:unitXMLList>\gram \gram \gram</si:unitXMLList>
  </si:realListXMLList>
</dcc:itemQuantity>
```

In most cases three separate `dcc:itemQuantity` entries, each with its own `si:real` and its own
`dcc:name`, are easier for a consumer to handle and easier for a person to read. Reach for the
list form only when the numbers genuinely belong to one quantity, replicates, a time series, a
calibration curve.

### 4.6.4 Option D (`dcc:charsXMLList`)

Use when the "quantity" is best represented as a **list of tokens/strings** (not numeric), e.g., categorical values, codes, labels.

```xml
<dcc:itemQuantity>
  <dcc:name><dcc:content lang="en">Applicable methods</dcc:content></dcc:name>
  <dcc:charsXMLList>ICP-OES XRF OES</dcc:charsXMLList>
</dcc:itemQuantity>
```

### 4.6.5 Options E, H (Advanced/Rare)

These options exist for specialized use cases:

| Option | Element | When to Use |
|--------|---------|-------------|
| **E** | `si:hybrid` | When you need a hybrid representation, typically when a plain double is insufficient |
| **F** | `si:complex` | When the quantity is genuinely complex-valued (real + imaginary) |
| **G** | `si:constant` | When you need to represent a constant quantity as defined by the SI schema |
| **H** | `si:complexListXMLList` | When you need a list of complex numbers in compact list form |

## 4.7 Material Identifiers

Material Identifiers provide the canonical, **machine-actionable keys** that identify a reference material across producers, lots and batches, catalogues and downstream systems. Unlike free-text names, identifiers are intended to be **stable** and suitable for indexing, deduplication, traceability and cross-document linking.

!!! danger "This is where ISO 33401:2024, 5.2.3 is satisfied, and it is mandatory"
    ISO 33401:2024, 5.2.3 requires the RM document to carry **the unique identifier of the RM**,
    for both certificates and product information sheets. The standard describes it as a
    combination of a product code and a batch number, `NMIJ CRM 7305-a`, `ERM-AC110`,
    `NIST SRM 41`, distinguishable from any other RM issued by the same producer. Rule
    **DRMD-016** enforces it as a hard error.

    **`coreData/uniqueIdentifier` does not satisfy this requirement.** That element identifies the
    *document*. One document can cover several materials, and one material is described by
    successive document revisions, so the two are not interchangeable. Using the document
    identifier for 5.2.3 is a genuine compliance gap, not a stylistic choice.

    Give at least a product-level identifier. Where units are produced in batches, add the batch
    or lot number as a second identifier. Where each unit is individually characterised, ISO
    33401:2024, 5.2.3 asks for an additional identifier such as a serial number for that unit,
    so add it as a third.

!!! warning "Match the label exactly"
    ISO 33401:2024, Clause 6 requires the container label to allow the right RM document to be
    identified, using the unique RM identifier of 5.2.3. That string is the only link between the
    physical unit in someone's hand and this digital document.

    Copy it **byte for byte**, case, punctuation, separators, leading zeros. Normalising it on
    one side (upper-casing it, stripping a hyphen, trimming a leading zero) silently breaks the
    match, and the failure only shows up later, in someone else's system.

```mermaid
graph LR
    MID["materialIdentifiers"] --> MI1["materialIdentifier #1"]
    MID --> MI2["materialIdentifier #2"]
    MID --> MIN["materialIdentifier #n"]

    MI1 --> S1["scheme: BAM"]
    MI1 --> V1["value: M308a"]
    MI1 --> L1["link: https://www.bam.de/"]

    MI2 --> S2["scheme: Lot"]
    MI2 --> V2["value: L2024-Q3-001"]

    style MID fill:#e8eaf6,color:#000,stroke:#283593
    style MI1 fill:#c5cae9,color:#000,stroke:#3949ab
    style MI2 fill:#c5cae9,color:#000,stroke:#3949ab
    style MIN fill:#c5cae9,color:#000,stroke:#3949ab
    style S1 fill:#e3f2fd,stroke:#1565c0
    style V1 fill:#e3f2fd,stroke:#1565c0
    style L1 fill:#e3f2fd,stroke:#1565c0
    style S2 fill:#e3f2fd,stroke:#1565c0
    style V2 fill:#e3f2fd,stroke:#1565c0
```

### 4.7.1 Material Identifiers List

| Property | Value |
|----------|-------|
| **Path** | `.../drmd:material/drmd:materialIdentifiers` |
| **Type** | `drmd:materialIdentifierListType` |
| **Cardinality** | `[0..1]` in the XSD, but **required** by rule DRMD-016 |

!!! tip "Best Practices"
    - Provide this list whenever the material must be uniquely tracked (almost always recommended).
    - Include at least one **product-level identifier** (e.g., catalog/material code) and one **lot/batch-level identifier** when the DRMD is specific to a batch/production run.
    - Keep identifiers exactly as printed on packaging/certificate (case, punctuation, separators).
    - Prefer persistent/resolvable identifier schemes (DOI, Handle, official producer page) whenever possible.

### 4.7.2 Material Identifier Entry

| Property | Value |
|----------|-------|
| **Path** | `.../materialIdentifiers/drmd:materialIdentifier` |
| **Type** | `drmd:identifierType` |
| **Cardinality** | `[1..∞]` within the list |

Each `drmd:materialIdentifier` is one identifier instance, expressed as a **scheme + value** pair, optionally with a link.

| Child Element | Type | Required | Description |
|---------------|------|----------|-------------|
| **scheme** | `dcc:notEmptyStringType` | Yes | Names the identifier system / namespace / issuing authority |
| **value** | `dcc:notEmptyStringType` | Yes | The identifier string itself |
| **link** | `xs:anyURI` | No | A resolvable URL for the identifier |

!!! note "Recommended Scheme Values"
    Use a controlled set of scheme names across your organization to avoid duplicates:

    | Scheme | Category | Example Value |
    |--------|----------|---------------|
    | `BAM`, `NIST`, `ERM`, `LGC` | Producer-specific | `M308a`, `SRM-610` |
    | `ERP`, `SAP`, `InternalMaterialID` | Internal enterprise | `MAT-2024-001` |
    | `CatalogNo`, `GTIN` | Commercial | `7640114565019` |
    | `Lot`, `Batch` | Batch identifiers | `L2024-Q3-001` |
    | `DOI`, `Handle`, `URL` | Persistent identifiers | `10.1234/bam-m308a` |

### 4.7.3 Attributes

These attributes exist on each `drmd:materialIdentifier` and are useful for internal cross-references, merges, and structured linking patterns.

| Attribute | Type | Description |
|-----------|------|-------------|
| `@id` | `xs:ID` | Defines an internal XML identifier for this node. Use when you want to reference this exact element via `@refId` or want stable anchors for processing pipelines. |
| `@refId` | `xs:IDREFS` | One or more references to `@id` values elsewhere in the document. Supports internal linking such as mapping identifiers or connecting imported/legacy IDs to canonical ones. |
| `@refType` | `drmd:refTypesType` | Classifies the purpose/type of the reference. Enumeration values: `basic_certificateIdentification`, `basic_measuredValue`. Use only when you have a clear internal convention. |

### 4.7.4 Multi-Material Scenario

When a DRMD contains **multiple `drmd:material` entries** (e.g., different lots, different physical forms), the identifiers declared under `/drmd:materials/drmd:material/materialIdentifiers` should be treated as the canonical keys for linking downstream information.

```mermaid
graph TD
    MATS["materials"]
    M1["material #1<br/><i>Disc Form</i>"]
    M2["material #2<br/><i>Powder Form</i>"]

    MATS --> M1
    MATS --> M2

    M1 --> ID1["scheme: BAM<br/>value: M308a-disc"]
    M2 --> ID2["scheme: BAM<br/>value: M308a-powder"]

    ID1 -.->|"@refId links to"| PROPS1["Properties Block A<br/><i>Certified values for disc</i>"]
    ID2 -.->|"@refId links to"| PROPS2["Properties Block B<br/><i>Certified values for powder</i>"]

    style MATS fill:#e8eaf6,color:#000,stroke:#283593
    style M1 fill:#c5cae9,color:#000,stroke:#3949ab
    style M2 fill:#c5cae9,color:#000,stroke:#3949ab
    style ID1 fill:#e3f2fd,stroke:#1565c0
    style ID2 fill:#e3f2fd,stroke:#1565c0
    style PROPS1 fill:#e8f5e9,stroke:#4caf50
    style PROPS2 fill:#e8f5e9,stroke:#4caf50
```

!!! tip "Implementation Options"
    - **XML-native approach:** Assign `@id` on a chosen identifier element and reference it using `@refId` patterns where the schema permits.
    - **Database approach:** Map `(scheme, value)` pairs into normalized keys and use them as foreign keys across imported DRMD content.

???+ example "Complete Material Identifier Example"

    ```xml
    <drmd:materialIdentifiers>
      <drmd:materialIdentifier id="matid_m308a"
          refType="basic_certificateIdentification">
        <drmd:scheme>BAM</drmd:scheme>
        <drmd:value>M308a</drmd:value>
        <drmd:link>https://www.bam.de/</drmd:link>
      </drmd:materialIdentifier>
    </drmd:materialIdentifiers>
    ```

## Business Rules Summary

The following Schematron rules directly govern the Materials section:

| Rule ID | Scope | Severity | Description |
|---------|-------|----------|-------------|
| **DRMD-002** | All documents | Error | Every DRMD **MUST** contain at least one `material` entry (ISO 33401:2024, §5.2.4) |
| **DRMD-007** | All documents | Error | Every `material` entry **MUST** include a `name` element (ISO 33401:2024, §5.2.4) |
| **DRMD-008** | All documents | Conditional Error | Each `material` **MUST** specify `minimumSampleSize` whenever applicable (ISO 33401:2024, §5.2.7) |
| **DRMD-016** | All documents | Error | Every `material` **MUST** carry at least one `materialIdentifier`, the unique identifier of the RM (ISO 33401:2024, §5.2.3) |
| **RMC-011** | CRM only | Error | Reference Material Certificates **MUST** include a `description` for each material (ISO 33401:2024, §5.3.2) |
| **PIS-005** | ProductInformationSheet only | Warning | Product Information Sheets **SHOULD** include a `description` for each material |

```mermaid
graph LR
    DOC["DRMD Document"]
    DOC -->|"DRMD-002"| MAT["At least 1 material"]
    MAT -->|"DRMD-007"| NAME["name required"]
    MAT -->|"DRMD-008"| MSS["minimumSampleSize<br/><i>when applicable</i>"]
    MAT -->|"RMC-011<br/><i>CRM only</i>"| DESC["description required"]
    MAT -.->|"PIS-005<br/><i>PIS only</i>"| DESC2["description recommended"]

    style DOC fill:#e8eaf6,color:#000,stroke:#283593
    style MAT fill:#c5cae9,color:#000,stroke:#3949ab
    style NAME fill:#ffebee,color:#000,stroke:#f44336
    style MSS fill:#fff3e0,color:#000,stroke:#ff9800
    style DESC fill:#ffebee,color:#000,stroke:#f44336
    style DESC2 fill:#e8f5e9,color:#000,stroke:#4caf50
```

## Complete Material Example

??? example "Full materials Block (Click to Expand)"

    ```xml
    <drmd:materials>
      <drmd:material>
        <!-- Name (required) -->
        <drmd:name>
          <dcc:content lang="en">Aluminium Alloy Disk BAM-M308a</dcc:content>
          <dcc:content lang="de">Aluminiumlegierung Scheibe BAM-M308a</dcc:content>
        </drmd:name>

        <!-- Description (mandatory for CRM) -->
        <drmd:description>
          <dcc:name>
            <dcc:content lang="en">Material description</dcc:content>
          </dcc:name>
          <dcc:content lang="en">
            The reference material is provided as discs
            (approx. 65 mm diameter, 30 mm height).
            Intended for establishing/checking calibration
            of spark OES and XRF methods for similar matrices.
          </dcc:content>
        </drmd:description>

        <!-- Classification (optional, repeatable) -->
        <drmd:materialClass id="mc-1">
          <drmd:reference>ISO 12103-1</drmd:reference>
          <drmd:classID>A2 Fine Test Dust</drmd:classID>
          <drmd:link>https://www.iso.org/standard/30109.html</drmd:link>
        </drmd:materialClass>

        <!-- Minimum Sample Size (mandatory whenever applicable) -->
        <drmd:minimumSampleSize>
          <dcc:itemQuantity>
            <si:real>
              <si:label>Minimum sample mass for wet chemical analysis</si:label>
              <si:value>0.2</si:value>
              <si:unit>\gram</si:unit>
            </si:real>
          </dcc:itemQuantity>
        </drmd:minimumSampleSize>

        <!-- Item Quantities (optional) -->
        <drmd:itemQuantities>
          <dcc:itemQuantity>
            <si:real>
              <si:label>Diameter</si:label>
              <si:value>65</si:value>
              <si:unit>\milli\metre</si:unit>
            </si:real>
          </dcc:itemQuantity>
          <dcc:itemQuantity>
            <si:real>
              <si:label>Height</si:label>
              <si:value>30</si:value>
              <si:unit>\milli\metre</si:unit>
            </si:real>
          </dcc:itemQuantity>
          <dcc:itemQuantity>
            <si:real>
              <si:label>Approximate mass</si:label>
              <si:value>250</si:value>
              <si:unit>\gram</si:unit>
            </si:real>
          </dcc:itemQuantity>
        </drmd:itemQuantities>

        <!-- Material Identifiers (optional) -->
        <drmd:materialIdentifiers>
          <drmd:materialIdentifier id="matid_m308a"
              refType="basic_certificateIdentification">
            <drmd:scheme>BAM</drmd:scheme>
            <drmd:value>M308a</drmd:value>
            <drmd:link>https://www.bam.de/</drmd:link>
          </drmd:materialIdentifier>
          <drmd:materialIdentifier>
            <drmd:scheme>Lot</drmd:scheme>
            <drmd:value>L2024-Q3-001</drmd:value>
          </drmd:materialIdentifier>
        </drmd:materialIdentifiers>
      </drmd:material>
    </drmd:materials>
    ```
