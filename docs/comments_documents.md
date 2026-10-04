# Comments and Documents

The **Comments and Documents** chapter covers two optional, document-level add-ons that exist at the root of the DRMD structure. They apply to the DRMD as a whole, rather than being nested inside Materials or Properties:

- **`comment`**: A simple free-text note field intended for short, non-structured remarks about the DRMD instance.
- **`document`**: A repeatable, embedded binary file container. It is typically used to attach a PDF rendition of the RM document directly inside the XML, and can also hold other documents.

## Structure at a Glance

Both of these elements sit directly under the `digitalReferenceMaterialDocument` root.

```mermaid
graph TD
    ROOT["digitalReferenceMaterialDocument<br/><i>Root</i>"]
    
    ROOT --> C["comment<br/><i>xs:string [0..1]</i>"]
    ROOT --> D["document<br/><i>dcc:byteDataType [0..*]</i>"]
    
    D --> FNAME["fileName<br/><i>Required</i>"]
    D --> MTYPE["mimeType<br/><i>Required</i>"]
    D --> B64["dataBase64<br/><i>Required</i>"]
    D --> NAME["name<br/><i>Optional</i>"]
    D --> DESC["description<br/><i>Optional</i>"]

    style ROOT fill:#e8eaf6,color:#000,stroke:#283593
    style C fill:#f5f5f5,color:#000,stroke:#9e9e9e
    style D fill:#c5cae9,color:#000,stroke:#3949ab
    style FNAME fill:#e3f2fd,stroke:#1565c0
    style MTYPE fill:#e3f2fd,stroke:#1565c0
    style B64 fill:#e3f2fd,stroke:#1565c0
    style NAME fill:#e8eaf6,stroke:#3f51b5
    style DESC fill:#e8eaf6,stroke:#3f51b5
```

!!! note "Validation Context"
    Because these elements are fundamentally optional and act as supplementary metadata, there are no strict Schematron business rules that mandate their presence in either the CRM or PIS document profiles. 

---

## 7.1 Purpose and Use

| Stakeholder | How They Use Comments and Documents |
|-------------|-------------------------------------|
| **Reference Material Producer (RMP)** | Uses `document` to deliver a human-readable official PDF alongside the machine-readable XML in a single package. Uses `comment` for brief editorial or operational notes. |
| **Laboratories / End Users** | Can store one single artifact (the XML file) while still having access to the official PDF without needing a separate download. Use `comment` for quick notes in archives (e.g., "Imported into LIMS on [Date]"). |
| **Instrument / Machine Manufacturers** | Usually ignore `document` for calculations, but may display it as a "View Certificate PDF" button. May show `comment` in UI logs or debug screens. |
| **Software Developers / LIMS** | `document` provides a canonical embedded file to store, checksum, and present to users. `comment` is parsed as a simple string for operational notes. |
| **Regulators / Auditors** | `document` provides the signed/issued PDF representation as evidence, stored together with the structured XML data. |

---

## 7.2 Comment (`comment`)

| Property | Value |
|----------|-------|
| **Path** | `/drmd:digitalReferenceMaterialDocument/drmd:comment` |
| **Schema Type** | `xs:string` |
| **Cardinality** | **Optional** `[0..1]` |

A short, document-level free-text note. 

!!! warning "Limitations"
    Unlike `dcc:textType` or `dcc:richContentType`, the `comment` field is **not multilingual** and **does not support attachments**. 

!!! tip "Best Practices"
    - Keep it short and non-normative (e.g., import notes, processing notes).
    - **Do not** put required guidance here (intended use, storage, and handling belong in the `Statements` chapter).
    - **Do not** put machine-relevant identifiers here (use identifier lists in the proper chapters).
    - **Do not** use this for legally relevant statements.

### 7.2.1 Example

```xml
<drmd:comment>
  Imported into LIMS on 2026-05-07. PDF attachment included as drmd:document.
</drmd:comment>
```

---

## 7.3 Document (`document`)

| Property | Value |
|----------|-------|
| **Path** | `/drmd:digitalReferenceMaterialDocument/drmd:document` |
| **Schema Type** | `dcc:byteDataType` |
| **Cardinality** | **Optional, repeatable** `[0..*]` |

An embedded file container, most commonly used to include a PDF version of the RM document (certificate or product information sheet) in Base64 encoding. This is a **document-level attachment** (applies to the whole DRMD), in contrast to attachments embedded inside specific statement fields via `dcc:richContentType`.

The element may be repeated. It can also be used for embedding documents other than the RM document, or for several documents, for example the certificate in two languages, or the certification report.

### 7.3.1 Structure

Inside `drmd:document`, the following sequence of elements is used:

The elements form a **sequence** and must appear in this order:

| # | Element | Required | Description |
|---|---------|----------|-------------|
| 1 | **name** | No | Multilingual label for the embedded document |
| 2 | **description** | No | Short description of what the embedded file represents |
| 3 | **fileName** | Yes | Original or recommended file name (e.g. `EXA-1a-certificate.pdf`). The extension must match the MIME type. |
| 4 | **mimeType** | Yes | Media type (e.g. `application/pdf`). Use a registered MIME type. |
| 5 | **dataBase64** | Yes | The file bytes, base64-encoded. Embed the exact bytes of the authoritative document. |

Putting `fileName` before `name` is a common mistake and fails XSD validation with a message
about an unexpected element, which does not obviously point at ordering.

**Optional attributes on `drmd:document`:**
- `@id`: Recommended if you reference the embedded document elsewhere via `@refId`.
- `@refId`: References other IDs (if you use a linking convention).
- `@refType`: Only if you have a consistent internal meaning.

!!! tip "Best Practices"
    - Use this element to embed the **official human-readable representation** (usually a PDF).
    - When you embed more than one document, put the official RM document **first** and give **every** document a `name` (and, if useful, a `description`) that says what it is, so that software and readers can tell the official rendition apart from the other files.
    - Where a supplementary document belongs to one statement (for example an SDS with `healthAndSafetyInformation`, or a drawing with the material `description`), attaching it there as a `dcc:file` keeps it next to the text it supports.
    - Ensure the embedded PDF **matches the content and version** of the XML to avoid mismatched revisions.
    - **Consider size/performance:** Base64 encoding increases file size. If the PDF is extremely large, some ecosystems prefer external linking instead of embedding.

### 7.3.2 Example

```xml
<drmd:document id="doc_pdf_certificate">
  <dcc:name>
    <dcc:content lang="en">Certificate PDF</dcc:content>
    <dcc:content lang="de">Zertifikat (PDF)</dcc:content>
  </dcc:name>
  <dcc:description>
    <dcc:content lang="en">
      Human-readable PDF rendition of this DRMD instance.
    </dcc:content>
  </dcc:description>
  <dcc:fileName>BAM-M308a-certificate.pdf</dcc:fileName>
  <dcc:mimeType>application/pdf</dcc:mimeType>
  <dcc:dataBase64>JVBERi0xLjQKJcTl8uXrp...BASE64_BYTES_HERE...==</dcc:dataBase64>
</drmd:document>
```
