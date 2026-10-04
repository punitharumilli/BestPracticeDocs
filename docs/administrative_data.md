# Administrative Data

The **Administrative Data** block (`administrativeData`) is the structural backbone of every DRMD document. It serves as the **"digital container"** for the material, ensuring that any software, analytical instrument, or regulatory body can verify the document's authenticity, identify its producer, and confirm its valid lifespan, all **before** processing any technical measurement data.


## Structure at a Glance

```mermaid
graph TD
    AD["administrativeData"]
    CD["coreData"]
    RMP["referenceMaterialProducer"]
    RP["respPersons"]

    AD --> CD
    AD --> RMP
    AD --> RP

    CD --> TOD["titleOfTheDocument"]
    CD --> UID["uniqueIdentifier"]
    CD --> DV["documentVersion"]
    CD --> DI["documentIdentifiers"]
    CD --> VAL["validity"]

    RMP --> NAME1["name"]
    RMP --> CONT["contact"]
    RMP --> CS["cryptElectronicSeal"]
    RMP --> CSig["cryptElectronicSignature"]
    RMP --> CTS["cryptElectronicTimeStamp"]
    RMP --> OI["organizationIdentifiers"]

    RP --> RP1["respPerson"]
    RP1 --> PERSON["person"]
    RP1 --> DESC["description"]
    RP1 --> ROLE["role"]
    RP1 --> MS["mainSigner"]

    style AD fill:#e8eaf6,color:#000,stroke:#283593
    style CD fill:#c5cae9,color:#000,stroke:#3949ab
    style RMP fill:#c5cae9,color:#000,stroke:#3949ab
    style RP fill:#c5cae9,color:#000,stroke:#3949ab
```

The three pillars are:

| Pillar | Path | Type | Required |
|--------|------|------|----------|
| **Core Data** | `coreData` | `drmd:coreDataType` | Mandatory |
| **Reference Material Producer** | `referenceMaterialProducer` | `drmd:referenceMaterialProducerType` | Mandatory |
| **Responsible Persons** | `respPersons` | `dcc:respPersonListType` | CRM: Mandatory / PIS: Optional |

!!! warning "Dual Validation Required"
    The DRMD schema uses a **dual-profile architecture**. The XSD defines the structure, but profile-specific mandatory requirements (e.g., `respPersons` for CRM documents) are enforced by the companion **Schematron business rules** (`drmd-business-rules.sch`). Full compliance requires passing **both** validations.


## 3.1 Core Data (`coreData`)

The `coreData` pillar contains the primary metadata that identifies the document and its legal status. Think of it as the document's **passport**.

```mermaid
graph LR
    CD["coreData"] --> TOD["titleOfTheDocument<br/><i>drmd:titleOfDocumentType</i>"]
    CD --> UID["uniqueIdentifier<br/><i>dcc:notEmptyStringType</i>"]
    CD --> DV["documentVersion<br/><i>dcc:notEmptyStringType</i>"]
    CD --> DI["documentIdentifiers<br/><i>drmd:documentIdentifierListType</i>"]
    CD --> VAL["validity<br/><i>drmd:ValidityType</i>"]

    style CD fill:#e8eaf6,color:#000,stroke:#3f51b5
    style TOD fill:#e8eaf6,stroke:#3f51b5
    style UID fill:#e8eaf6,stroke:#3f51b5
    style DV fill:#e8eaf6,stroke:#3f51b5
    style DI fill:#e8eaf6,stroke:#3f51b5
    style VAL fill:#e8eaf6,stroke:#3f51b5
```


### 3.1.1 Title of the Document (`titleOfTheDocument`)

| Property | Value |
|----------|-------|
| **Path** | `.../coreData/drmd:titleOfTheDocument` |
| **Type** | `drmd:titleOfDocumentType` (restricts `xs:string`) |
| **Cardinality** | **Required** `[1..1]` |
| **Enumerations** | `referenceMaterialCertificate`, `productInformationSheet` |

**Purpose:** A mandatory classification that defines the **metrological level** of the document. It tells analytical instrument software how to weigh the data contained within.

???+ info "Understanding the Two Document Profiles"

    The `titleOfTheDocument` value drives the entire validation behavior of the DRMD. Choosing the wrong profile can lead to validation failures or, worse, incorrect interpretation of measurement data.

    === "referenceMaterialCertificate (CRM)"

        - Identifies a **Certified Reference Material** per ISO 33401:2024
        - Values are **certified** with full traceability and uncertainty budgets
        - Downstream data systems treat properties as suitable for **calibration**
        - **Additional mandatory requirements** are activated via Schematron:
            - `respPersons` with approving officer (RMC-010)
            - `metrologicalTraceability` statement (RMC-001)
            - At least one `properties` block with `@isCertified="true"` (RMC-002)
            - Material `description` (RMC-011)

    === "productInformationSheet"

        - Identifies an informative **Reference Material** per ISO 33401:2024
        - Values are valid measurement results but **not certified**
        - Should **not** be used as a primary anchor for calibration
        - Fewer mandatory requirements, `respPersons` is optional
        - `@isCertified` MUST NOT be set to `"true"` (PIS-001)

**XML Examples:**

```xml
<!-- For a Certified Reference Material (CRM) -->
<drmd:titleOfTheDocument>referenceMaterialCertificate</drmd:titleOfTheDocument>

<!-- For an informative Reference Material (RM) -->
<drmd:titleOfTheDocument>productInformationSheet</drmd:titleOfTheDocument>
```

!!! danger "Schematron Rule: DRMD-001"
    Every DRMD document **MUST** declare a `titleOfTheDocument` in `coreData`, specifying either `referenceMaterialCertificate` or `productInformationSheet`. Severity: **Error**, document is non-compliant without this element.


### 3.1.2 Unique Identifier (`uniqueIdentifier`)

| Property | Value |
|----------|-------|
| **Path** | `.../coreData/drmd:uniqueIdentifier` |
| **Type** | `dcc:notEmptyStringType` |
| **Cardinality** | **Required** `[1..1]` |

**Purpose:** A mandatory string identifying **this document instance**. It prevents identifier
collisions across systems and lets a LIMS tell one revision from another.

!!! danger "This is the document's identifier, not the material's"
    ISO 33401:2024, 5.2.3 requires the unique identifier **of the RM**, a product code, normally
    with a batch or lot number. That is a different thing, it lives in
    `materials/material/materialIdentifiers`, and rule **DRMD-016** requires it.

    They cannot be the same field: one document may cover several materials, and one material is
    described by successive document revisions. Putting the product code here and nothing in
    `materialIdentifiers` leaves ISO 5.2.3 unsatisfied.

!!! tip "Best Practice"
    Use a **UUID v4**. If the document is revised or re-issued, generate a **new** UUID, never
    reuse one across revisions. The material identifiers, by contrast, stay the same, because the
    material has not changed.

```xml
<drmd:uniqueIdentifier>84d58aee-4f81-460f-993e-a594ce3a8d60</drmd:uniqueIdentifier>
```


### 3.1.3 Document Version (`documentVersion`)

| Property | Value |
|----------|-------|
| **Path** | `.../coreData/drmd:documentVersion` |
| **Type** | `dcc:notEmptyStringType` |
| **Cardinality** | **Required** `[1..1]` |

**Purpose:** A mandatory version string identifying the revision of this document, so that a
recipient can tell whether they hold the current one (ISO 33401:2024, §5.2.13).

!!! danger "Schematron Rule: DRMD-011"
    Every DRMD document **MUST** state a `documentVersion` (ISO 33401:2024, §5.2.13, Mandatory
    for both document profiles). Severity: **Error**. The XSD also requires the element; the rule
    exists so that a Schematron-only report covers ISO 33401:2024, Table 1 in full on its own.

A version number, an approval date, or both are acceptable. Whichever form you choose, the value
must change whenever the content changes.

```xml
<drmd:documentVersion>2.0</drmd:documentVersion>
```

```xml
<!-- An approval date is equally valid -->
<drmd:documentVersion>2026-03-14</drmd:documentVersion>
```

!!! tip "Do not confuse it with `@schemaVersion`"
    `@schemaVersion` on the root element says which **DRMD specification** the document follows
    (currently `1.0.0`). `documentVersion` says which revision of **this certificate's content**
    it is. They change for entirely different reasons.


### 3.1.4 Document Identifiers (`documentIdentifiers`)

| Property | Value |
|----------|-------|
| **Path** | `.../coreData/drmd:documentIdentifiers` |
| **Type** | `drmd:documentIdentifierListType` |
| **Cardinality** | **Optional** `[0..1]` |

**Purpose:** The digital **"Linkage Hub"** for the certificate, allowing it to be indexed and verified across different global and internal databases.

```mermaid
graph TD
    DI["documentIdentifiers"] --> DI1["documentIdentifier"]
    DI --> DI2["documentIdentifier"]

    DI1 --> S1["scheme: DOI"]
    DI1 --> V1["value: 10.1234/BAM.M308a.2026"]
    DI1 --> L1["link: https://doi.org/..."]

    DI2 --> S2["scheme: Internal_ERP"]
    DI2 --> V2["value: BATCH-2026-X99"]

    style DI fill:#e8eaf6,color:#000,stroke:#3f51b5
    style DI1 fill:#e3f2fd,stroke:#1565c0
    style DI2 fill:#e3f2fd,stroke:#1565c0
```

Each `documentIdentifier` contains:

| Child Element | Type | Required | Description |
|---------------|------|----------|-------------|
| `scheme` | `dcc:notEmptyStringType` | Yes | The naming system or authority (e.g., `"DOI"`, `"Internal_ERP"`) |
| `value` | `dcc:notEmptyStringType` | Yes | The actual unique code assigned by the authority |
| `link` | `xs:anyURI` | No | A URI/URL for immediate verification of origin |

**Technical Attributes:** `@id` (internal XML label), `@refId` (pointer to another ID), `@refType` (categorizes the nature, e.g., `basic_certificateIdentification`).

???+ example "Complete XML Example"

    ```xml
    <drmd:documentIdentifiers>
      <!-- Global DOI Identification -->
      <drmd:documentIdentifier id="ID_01" refType="basic_certificateIdentification">
        <drmd:scheme>DOI</drmd:scheme>
        <drmd:value>10.1234/BAM.M308a.2026</drmd:value>
        <drmd:link>https://doi.org/10.1234/BAM.M308a.2026</drmd:link>
      </drmd:documentIdentifier>

      <!-- Internal Business Tracking -->
      <drmd:documentIdentifier id="ID_02">
        <drmd:scheme>Internal_ERP</drmd:scheme>
        <drmd:value>BATCH-2026-X99</drmd:value>
      </drmd:documentIdentifier>
    </drmd:documentIdentifiers>
    ```


### 3.1.5 Validity (`validity`)

| Property | Value |
|----------|-------|
| **Path** | `.../coreData/drmd:validity` |
| **Type** | `drmd:ValidityType` |
| **Cardinality** | **Required** `[1..1]` |

**Purpose:** A mandatory **choice** that establishes the operational lifespan of the certificate. Producers must select **exactly one** of three methods. Instruments match this data block against real-time evaluation dates to automatically lock out expired materials.

!!! danger "Schematron Rule: DRMD-012"
    Every DRMD document **MUST** specify a validity period or condition (ISO 33401:2024, §5.2.8). Severity: **Error**.

```mermaid
graph TD
    VAL["validity<br/><i>Choose exactly one</i>"]
    ST["specificTime<br/><i>xs:date</i><br/>Fixed expiration"]
    TAD["timeAfterDispatch<br/><i>Relative validity</i>"]
    UR["untilRevoked<br/><i>xs:boolean, fixed=true</i><br/>Permanent"]

    VAL -->|Option 1| ST
    VAL -->|Option 2| TAD
    VAL -->|Option 3| UR

    TAD --> DD["dispatchDate<br/><i>xs:date [0..1]</i>"]
    TAD --> PER["period<br/><i>xs:duration [1..1]</i>"]

    style VAL fill:#e8eaf6,color:#000,stroke:#3f51b5
    style ST fill:#fff3e0,stroke:#ff9800
    style TAD fill:#e8f5e9,stroke:#4caf50
    style UR fill:#e3f2fd,stroke:#1565c0
```

=== "specificTime (Fixed Expiration)"

    A hard expiration date using the `YYYY-MM-DD` format. Provides a **"Hard Stop"** for safety, automated instruments compare this to the current date and **lock out** the material if expired.

    ```xml
    <drmd:validity>
      <drmd:specificTime>2040-12-31</drmd:specificTime>
    </drmd:validity>
    ```

=== "timeAfterDispatch (Relative Validity)"

    A dynamic duration defined by an optional `dispatchDate` and a mandatory ISO 8601 `period` (e.g., `P3Y` for 3 years). Accommodates materials where shelf-life only begins once shipped. Systems parse the period to **automatically calculate** a unique expiration date.

    !!! note "Policy Option"
        If DRMD's legal issuance is defined as the act of signing (not printing/dispatching), set `dispatchDate` to the date of the signing event. Only do this when signing time is explicitly your issuance time by regulation/process.

    ```xml
    <drmd:validity>
      <drmd:timeAfterDispatch>
        <drmd:dispatchDate>2026-04-20</drmd:dispatchDate>
        <drmd:period>P3Y2M</drmd:period> <!-- Valid for 3 years, 2 months -->
      </drmd:timeAfterDispatch>
    </drmd:validity>
    ```

=== "untilRevoked (Permanent Until Notice)"

    A boolean element fixed to the value `true`. Used for inherently stable materials that do not require a predetermined expiration date. The certificate remains active until a **revocation or updated version** is issued.

    ```xml
    <drmd:validity>
      <drmd:untilRevoked>true</drmd:untilRevoked>
    </drmd:validity>
    ```


## 3.2 Reference Material Producer (`referenceMaterialProducer`)

| Property | Value |
|----------|-------|
| **Path** | `.../administrativeData/drmd:referenceMaterialProducer` |
| **Type** | `drmd:referenceMaterialProducerType` |
| **Cardinality** | **Required** `[1..1]` |

This block identifies the organization **legally and operationally responsible** for producing (or issuing) the reference material and its documentation (e.g., BAM, NIST, IRMM).

!!! danger "Schematron Rule: DRMD-010"
    Every DRMD document **MUST** identify the `referenceMaterialProducer` (ISO 33401:2024, §5.2.5). Severity: **Error**.

```mermaid
graph TD
    RMP["referenceMaterialProducer"]
    NAME["name<br/><i>dcc:textType [1..1]</i>"]
    CONTACT["contact<br/><i>dcc:contactType [1..1]</i>"]
    SEAL["cryptElectronicSeal<br/><i>xs:boolean [0..1]</i>"]
    SIG["cryptElectronicSignature<br/><i>xs:boolean [0..1]</i>"]
    TS["cryptElectronicTimeStamp<br/><i>xs:boolean [0..1]</i>"]
    OI["organizationIdentifiers<br/><i>drmd:organizationIdentifierListType [0..1]</i>"]

    RMP --> NAME
    RMP --> CONTACT
    RMP --> SEAL
    RMP --> SIG
    RMP --> TS
    RMP --> OI

    CONTACT --> CN["name<br/><i>dcc:textType</i>"]
    CONTACT --> EM["eMail"]
    CONTACT --> PH["phone"]
    CONTACT --> FAX["fax"]
    CONTACT --> LN["link"]
    CONTACT --> LOC["location"]

    style RMP fill:#e8eaf6,color:#000,stroke:#3f51b5
    style NAME fill:#c5cae9,stroke:#3f51b5
    style CONTACT fill:#c5cae9,stroke:#3f51b5
    style SEAL fill:#e8eaf6,stroke:#9fa8da
    style SIG fill:#e8eaf6,stroke:#9fa8da
    style TS fill:#e8eaf6,stroke:#9fa8da
    style OI fill:#e8eaf6,stroke:#9fa8da
```

??? abstract "Who Uses This Block?"

    | Stakeholder | How They Use It |
    |-------------|----------------|
    | **RM Producer / Issuing Organization** | Provides authoritative identity; enables consistent re-use of metadata across many DRMDs |
    | **Laboratories / Customers** | Verifies the issuer and finds official contact details to confirm provenance |
    | **Software Developers** | Renders the "Producer block" consistently; uses identifiers as stable keys for deduplication |
    | **Machine / Instrument Manufacturers** | Links results to producer identity for QA workflows and LIMS integration |
    | **Auditors / Regulators** | Validates issuer identity and supports regulatory compliance |


### 3.2.1 Name

| Property | Value |
|----------|-------|
| **Path** | `.../referenceMaterialProducer/drmd:name` |
| **Type** | `dcc:textType` |
| **Cardinality** | **Required** `[1..1]` |

A multilingual "human-friendly" name of the producer. As a `dcc:textType`, it holds one or more `dcc:content` elements where the `@lang` attribute follows ISO-639-1.

!!! tip "Best Practices"
    - Provide at least one `dcc:content`
    - For international publications, provide multiple languages (e.g., `en`, `de`)
    - Use the official long form; avoid abbreviations unless included separately

```xml
<drmd:name>
  <dcc:content lang="en">Federal Institute for Materials Research and Testing (BAM)</dcc:content>
  <dcc:content lang="de">Bundesanstalt fuer Materialforschung und -pruefung (BAM)</dcc:content>
</drmd:name>
```


### 3.2.2 Contact

| Property | Value |
|----------|-------|
| **Path** | `.../referenceMaterialProducer/drmd:contact` |
| **Type** | `dcc:contactType` |
| **Cardinality** | **Required** `[1..1]` |

A structured contact block essential for requesting value clarifications, handling instructions, or additional documentation.

**Contact sub-elements:**

| Element | Type | Required | Notes |
|---------|------|----------|-------|
| `dcc:name` | `dcc:textType` | Yes | Department or team name |
| `dcc:eMail` | `dcc:notEmptyStringType` | No | Always provide at least email or phone |
| `dcc:phone` | `dcc:notEmptyStringType` | No | |
| `dcc:fax` | `dcc:notEmptyStringType` | No | Legacy, but schema-supported |
| `dcc:link` | `xs:anyURI` | No | Organization website |
| `dcc:location` | `dcc:locationType` | Yes | Postal address. `countryCode` (ISO 3166-1) recommended. See *Address elements* below. |

**Address elements (`dcc:location`).** `dcc:locationType` is a *repeatable choice*: each of its
elements is **optional**, may be repeated, and may appear in any order. The schema only requires
that at least one of them is present.

| Element | Typically given | Notes |
|---------|-----------------|-------|
| `dcc:street`, `dcc:streetNo` | Yes | |
| `dcc:postCode`, `dcc:city` | Yes | |
| `dcc:countryCode` | Yes | Two-letter ISO 3166-1 code, e.g. `DE` |
| `dcc:postOfficeBox` | Only where used | |
| `dcc:state` | Only where used | Federal state, province or region |
| `dcc:further` | Only where needed | Free text, e.g. building or room |
| `dcc:positionCoordinates` | Optional | Geographic coordinates, e.g. WGS84 |

!!! note "Reading the cardinality in the schema tree"
    Each address element *declares* `[1..1]` in `dcc.xsd`, but that applies each time the
    surrounding choice is used, and the choice may be used any number of times. The interactive
    schema tree therefore shows these elements as `[0..*]`.

???+ example "Complete Contact XML Example"

    ```xml
    <drmd:contact>
      <dcc:name>
        <dcc:content lang="en">BAM Sales / CRM</dcc:content>
      </dcc:name>
      <dcc:eMail>sales.crm@bam.de</dcc:eMail>
      <dcc:phone>+49 30 8104 2061</dcc:phone>
      <dcc:fax>+49 30 8104 72061</dcc:fax>
      <dcc:link>https://www.bam.de/</dcc:link>
      <dcc:location>
        <dcc:street>Richard-Willstaetter-Str.</dcc:street>
        <dcc:streetNo>11</dcc:streetNo>
        <dcc:postCode>12489</dcc:postCode>
        <dcc:city>Berlin</dcc:city>
        <dcc:countryCode>DE</dcc:countryCode>
        <dcc:positionCoordinates>
          <dcc:positionCoordinateSystem>WGS84</dcc:positionCoordinateSystem>
          <dcc:positionCoordinate1>
            <si:label>latitude</si:label>
            <si:value>52.4319</si:value>
            <si:unit>\degree</si:unit>
          </dcc:positionCoordinate1>
          <dcc:positionCoordinate2>
            <si:label>longitude</si:label>
            <si:value>13.5330</si:value>
            <si:unit>\degree</si:unit>
          </dcc:positionCoordinate2>
        </dcc:positionCoordinates>
      </dcc:location>
    </drmd:contact>
    ```


### 3.2.3 descriptionData (Optional Attachment)

| Property | Value |
|----------|-------|
| **Path** | `.../contact/dcc:descriptionData` |
| **Type** | `dcc:byteDataType` |
| **Cardinality** | **Optional** `[0..1]` |

Used to attach small binary artifacts such as a **vCard** (`text/vcard`) or an organization **logo** (PNG/SVG).

```xml
<dcc:descriptionData>
  <dcc:fileName>producer-contact.vcf</dcc:fileName>
  <dcc:mimeType>text/vcard</dcc:mimeType>
  <dcc:dataBase64>BASE64_ENCODED_BYTES_HERE==</dcc:dataBase64>
</dcc:descriptionData>
```


### 3.2.4 Cryptographic Capability Flags (Optional Booleans)

These flags are **capability / policy hints**, not proofs. They help consumers know what to expect from the producer's trust infrastructure.

| Element | Type | Meaning |
|---------|------|---------|
| `cryptElectronicSeal` | `xs:boolean` | Organization-level sealing (often for automated issuing) |
| `cryptElectronicSignature` | `xs:boolean` | Person-based signing workflows |
| `cryptElectronicTimeStamp` | `xs:boolean` | Time-stamping services used for long-term validity |

??? abstract "Who Uses These Flags?"

    | Stakeholder | Usage |
    |-------------|-------|
    | **Producers** | Declare available trust mechanisms |
    | **Consumers** | Decide if additional manual verification is needed |
    | **Software Developers** | Decide whether to show validation UI and "digitally signed" expectations |

!!! tip "Best Practice"
    Use `true`/`false` explicitly only when you are confident. **Omit the element** if unknown rather than guessing.

```xml
<drmd:cryptElectronicSeal>true</drmd:cryptElectronicSeal>
<drmd:cryptElectronicSignature>false</drmd:cryptElectronicSignature>
<drmd:cryptElectronicTimeStamp>true</drmd:cryptElectronicTimeStamp>
```


### 3.2.5 Organization Identifiers (Optional List)

| Property | Value |
|----------|-------|
| **Path** | `.../referenceMaterialProducer/drmd:organizationIdentifiers` |
| **Type** | `drmd:organizationIdentifierListType` |
| **Cardinality** | **Optional** `[0..1]` |

A mechanism to assign **stable external identifiers** to the organization, enabling unambiguous machine linking across global systems.

Each `organizationIdentifier` contains: `scheme` (Required), `value` (Required), `link` (Optional), plus `@id`, `@refId`, `@refType` attributes.

**Recommended Schemes:**

| Scheme | Description | Example |
|--------|-------------|---------|
| `ROR` | Research Organization Registry | `02h2x7d13` |
| `VAT` | EU VAT Number | `DE123456789` |
| `LEI` | Legal Entity Identifier | `529900T8BM49AURSDO55` |
| National registers | Company register or authority IDs | none |

!!! tip "Best Practices"
    - Prefer globally resolvable IDs (e.g., ROR + link)
    - Use `link` whenever there is a canonical resolver URL
    - Keep the `scheme` short and stable; do not use long prose

???+ example "Organization Identifiers XML"

    ```xml
    <drmd:organizationIdentifiers>
      <drmd:organizationIdentifier>
        <drmd:scheme>ROR</drmd:scheme>
        <drmd:value>02h2x7d13</drmd:value>
        <drmd:link>https://ror.org/02h2x7d13</drmd:link>
      </drmd:organizationIdentifier>

      <drmd:organizationIdentifier>
        <drmd:scheme>VAT</drmd:scheme>
        <drmd:value>DE123456789</drmd:value>
      </drmd:organizationIdentifier>
    </drmd:organizationIdentifiers>
    ```


## 3.3 Responsible Persons (`respPersons`)

| Property | Value |
|----------|-------|
| **Path** | `.../administrativeData/drmd:respPersons` |
| **Type** | `dcc:respPersonListType` (imported from DCC schema) |
| **Cardinality** | CRM: **Mandatory** / ProductInformationSheet: **Optional** `[0..1]` |

The **Responsible Persons** block records the human (or organizational) accountability for the DRMD: who prepared it, who approved it, and who is authorized to perform electronic signatures.

!!! danger "Schematron Rules: RMC-010 and RMC-012"
    ISO 33401:2024, §5.3.5 requires the **name and function** of the officer representing the RM
    producer and accepting responsibility for the contents of the certificate. Both halves are
    required, and two rules cover them:

    * **RMC-010** (Error): a Reference Material Certificate MUST have a `respPersons` list.
    * **RMC-012** (Error): at least one `dcc:respPerson` in it MUST state a `dcc:role`, which is
      the officer's function. `dcc:role` is optional in the DCC schema, so without this rule a
      certificate could name someone with no indication of their authority to approve it.

    Neither rule applies to `productInformationSheet` documents, where §5.3.5 is Optional.

    The NOTE to §5.3.5 allows the officer's name to be the name of the responsible organisation,
    so a role naming the unit rather than a personal job title, `Head of Division, Inorganic
    Reference Materials`, satisfies the requirement.

```mermaid
graph TD
    RP["respPersons<br/><i>dcc:respPersonListType</i>"]
    RP1["respPerson<br/><i>@id, @refId, @refType</i>"]
    RP2["respPerson<br/><i>@id, @refId, @refType</i>"]

    RP --> RP1
    RP --> RP2

    RP1 --> P1["person<br/><i>dcc:contactNotStrictType</i>"]
    RP1 --> D1["description<br/><i>dcc:richContentType</i>"]
    RP1 --> R1["role<br/><i>dcc:notEmptyStringType</i>"]
    RP1 --> MS1["mainSigner<br/><i>xs:boolean</i>"]
    RP1 --> CS1["cryptElectronicSeal"]
    RP1 --> CSig1["cryptElectronicSignature"]
    RP1 --> CTS1["cryptElectronicTimeStamp"]

    P1 --> PN["name"]
    P1 --> PE["eMail"]
    P1 --> PP["phone"]
    P1 --> PL["link"]

    style RP fill:#e8eaf6,color:#000,stroke:#3f51b5
    style RP1 fill:#c5cae9,stroke:#3f51b5
    style RP2 fill:#c5cae9,stroke:#3f51b5
    style P1 fill:#e8eaf6,stroke:#9fa8da
```

??? abstract "Who Uses This Block?"

    | Stakeholder | Usage |
    |-------------|-------|
    | **RM Producer** | Internal governance, traceability of approvals, auditability, and responsibility assignment |
    | **Regulators / Accreditation Bodies / Auditors** | Clear accountability and roles |
    | **Software Developers / Platform Operators** | Consistent identity anchors (`@id`) and re-use via references (`@refId`) across sections |
    | **Downstream Users (Labs, Customers)** | Know who approved/certified the DRMD and how to reach them |


### 3.3.1 Responsible Person Entry (`respPerson`)

Each `dcc:respPerson` entry captures **who is responsible** and optionally **what role they play**.

**Attributes (identity & linking):**

| Attribute | Type | Purpose |
|-----------|------|---------|
| `@id` | `xs:ID` | Unique identifier within the XML document (e.g., `respPerson_1`) |
| `@refId` | `xs:IDREFS` | References IDs defined elsewhere to avoid duplication |
| `@refType` | `dcc:refTypesType` | Classifies the reference relationship |

**Child Elements:**

| Element | Type | Required | Description |
|---------|------|----------|-------------|
| `dcc:person` | `dcc:contactNotStrictType` | **Yes** | Identity and contact data (location is optional) |
| `dcc:description` | `dcc:richContentType` | No | Human-readable responsibilities, expertise, department |
| `dcc:role` | `dcc:notEmptyStringType` | Optional in DCC; **required on at least one person in a certificate** (RMC-012) | The person's function, e.g. `"Head of Division, Inorganic Reference Materials"` |
| `dcc:mainSigner` | `xs:boolean` | No | Flags the primary signer among multiple persons |
| `dcc:cryptElectronicSeal` | `xs:boolean` | No | Workflow hint: sealing capability |
| `dcc:cryptElectronicSignature` | `xs:boolean` | No | Workflow hint: signing capability |
| `dcc:cryptElectronicTimeStamp` | `xs:boolean` | No | Workflow hint: timestamping capability |

!!! tip "Best Practice"
    If you have a signing workflow, set exactly **one** `mainSigner=true`. Always set `@id` so other elements can reference the person consistently.


### 3.3.2 Person Details (`dcc:person`)

The `dcc:person` element uses type `dcc:contactNotStrictType`, meaning **location is optional** (unlike `dcc:contactType` where location is required).

| Element | Type | Required | Notes |
|---------|------|----------|-------|
| `dcc:name` | `dcc:textType` | **Yes** | Multilingual structured text |
| `dcc:eMail` | `dcc:notEmptyStringType` | No | Email contact |
| `dcc:phone` | `dcc:notEmptyStringType` | No | Phone contact |
| `dcc:fax` | `dcc:notEmptyStringType` | No | Fax (legacy, supported) |
| `dcc:link` | `xs:anyURI` | No | ORCID page, institutional directory, etc. |
| `dcc:location` | `dcc:locationType` | No | Optional address/affiliation |
| `dcc:descriptionData` | `dcc:byteDataType` | No | Binary attachment (vCard, mandate PDF, etc.) |


### 3.3.3 Complete Responsible Persons Example

???+ example "Full XML Example with Two Responsible Persons"

    ```xml
    <drmd:respPersons>
      <!-- Primary Approving Officer -->
      <dcc:respPerson id="respPerson_1" refType="basic_certificateIdentification">
        <dcc:person>
          <dcc:name>
            <dcc:content lang="en">Dr. F. Emmerling</dcc:content>
          </dcc:name>
          <dcc:eMail>f.emmerling@example.org</dcc:eMail>
          <dcc:phone>+49 30 8104 0000</dcc:phone>
          <dcc:link>https://www.example.org/staff/emmerling</dcc:link>
        </dcc:person>
        <dcc:description>
          <dcc:content lang="en">Analytical Chemistry; Reference Materials</dcc:content>
        </dcc:description>
        <dcc:role>Head of Department 1</dcc:role>
        <dcc:mainSigner>true</dcc:mainSigner>
        <dcc:cryptElectronicSeal>true</dcc:cryptElectronicSeal>
        <dcc:cryptElectronicSignature>true</dcc:cryptElectronicSignature>
        <dcc:cryptElectronicTimeStamp>true</dcc:cryptElectronicTimeStamp>
      </dcc:respPerson>

      <!-- Secondary Technical Reviewer -->
      <dcc:respPerson id="respPerson_2"
                      refId="respPerson_1"
                      refType="basic_certificateIdentification">
        <dcc:person>
          <dcc:name>
            <dcc:content lang="en">Dr. S. Recknagel</dcc:content>
          </dcc:name>
          <dcc:eMail>sebastian.recknagel@example.org</dcc:eMail>
          <dcc:phone>+49 30 8104 1160</dcc:phone>
        </dcc:person>
        <dcc:description>
          <dcc:content lang="en">Specialist in Inorganic Reference Materials</dcc:content>
        </dcc:description>
        <dcc:role>Head of Division 1.6</dcc:role>
        <dcc:mainSigner>false</dcc:mainSigner>
        <dcc:cryptElectronicSignature>true</dcc:cryptElectronicSignature>
        <dcc:cryptElectronicTimeStamp>true</dcc:cryptElectronicTimeStamp>
      </dcc:respPerson>
    </drmd:respPersons>
    ```


## Business Rules Summary

The following Schematron business rules apply specifically to the **Administrative Data** block. Full compliance requires passing both XSD and Schematron validation.

| Rule ID | Scope | Severity | Description |
|---------|-------|----------|-------------|
| **DRMD-001** | All documents | Error | Must declare `titleOfTheDocument` |
| **DRMD-010** | All documents | Error | Must identify `referenceMaterialProducer` |
| **DRMD-012** | All documents | Error | Must specify a `validity` period or condition |
| **DRMD-011** | All documents | Error | Must state a `documentVersion` |
| **RMC-010** | CRM only | Error | Must list `respPersons`, naming the approving officer |
| **RMC-012** | CRM only | Error | At least one responsible person must state a function (`dcc:role`) |

!!! info "Validation Pipeline"
    ```
    Step 1: Validate against drmd.xsd         → Structural validation
    Step 2: Validate against drmd-business-rules.sch → Business rule validation
    Both steps MUST pass for a document to be considered fully compliant.
    ```


## Complete Administrative Data Example

??? example "Full administrativeData Block (Click to Expand)"

    ```xml
    <drmd:administrativeData>
      <!-- === Core Data === -->
      <drmd:coreData>
        <drmd:titleOfTheDocument>referenceMaterialCertificate</drmd:titleOfTheDocument>
        <drmd:uniqueIdentifier>84d58aee-4f81-460f-993e-a594ce3a8d60</drmd:uniqueIdentifier>
        <drmd:documentVersion>1.0.0</drmd:documentVersion>

        <drmd:documentIdentifiers>
          <drmd:documentIdentifier id="ID_01" refType="basic_certificateIdentification">
            <drmd:scheme>DOI</drmd:scheme>
            <drmd:value>10.1234/BAM.M308a.2026</drmd:value>
            <drmd:link>https://doi.org/10.1234/BAM.M308a.2026</drmd:link>
          </drmd:documentIdentifier>
        </drmd:documentIdentifiers>

        <drmd:validity>
          <drmd:untilRevoked>true</drmd:untilRevoked>
        </drmd:validity>
      </drmd:coreData>

      <!-- === Reference Material Producer === -->
      <drmd:referenceMaterialProducer>
        <drmd:name>
          <dcc:content lang="en">Federal Institute for Materials Research and Testing (BAM)</dcc:content>
          <dcc:content lang="de">Bundesanstalt fuer Materialforschung und -pruefung (BAM)</dcc:content>
        </drmd:name>

        <drmd:contact>
          <dcc:name>
            <dcc:content lang="en">BAM Sales / CRM</dcc:content>
          </dcc:name>
          <dcc:eMail>sales.crm@bam.de</dcc:eMail>
          <dcc:phone>+49 30 8104 2061</dcc:phone>
          <dcc:link>https://www.bam.de/</dcc:link>
          <dcc:location>
            <dcc:street>Richard-Willstaetter-Str.</dcc:street>
            <dcc:streetNo>11</dcc:streetNo>
            <dcc:postCode>12489</dcc:postCode>
            <dcc:city>Berlin</dcc:city>
            <dcc:countryCode>DE</dcc:countryCode>
          </dcc:location>
        </drmd:contact>

        <drmd:cryptElectronicSeal>true</drmd:cryptElectronicSeal>
        <drmd:cryptElectronicSignature>false</drmd:cryptElectronicSignature>
        <drmd:cryptElectronicTimeStamp>true</drmd:cryptElectronicTimeStamp>

        <drmd:organizationIdentifiers>
          <drmd:organizationIdentifier>
            <drmd:scheme>ROR</drmd:scheme>
            <drmd:value>02h2x7d13</drmd:value>
            <drmd:link>https://ror.org/02h2x7d13</drmd:link>
          </drmd:organizationIdentifier>
        </drmd:organizationIdentifiers>
      </drmd:referenceMaterialProducer>

      <!-- === Responsible Persons === -->
      <drmd:respPersons>
        <dcc:respPerson id="respPerson_1" refType="basic_certificateIdentification">
          <dcc:person>
            <dcc:name>
              <dcc:content lang="en">Dr. F. Emmerling</dcc:content>
            </dcc:name>
            <dcc:eMail>f.emmerling@example.org</dcc:eMail>
          </dcc:person>
          <dcc:role>Head of Department 1</dcc:role>
          <dcc:mainSigner>true</dcc:mainSigner>
        </dcc:respPerson>
      </drmd:respPersons>
    </drmd:administrativeData>
    ```
