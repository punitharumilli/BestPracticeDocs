# Parsing & Data Extraction Guide

This chapter provides implementation guidance for software developers, such as those building LIMS (Laboratory Information Management Systems), ELNs (Electronic Lab Notebooks), or analytical instrument software, who need to parse DRMD documents reliably and extract data for automated workflows.

Because the DRMD schema is built upon DCC and SI namespaces, and supports multilingual text and optional attachments, a robust parser must be designed to handle these variables gracefully.

---

## 13.1 Namespace Handling & Parser Configuration

### 13.1.1 Prefix-Independence (Critical)
XML prefixes are not significant and can change depending on how the document was generated. **Your code MUST match elements by Namespace URI + Local Name, never by prefix string.**

| Prefix commonly used | Namespace URI |
|-----------|-----------------|
| `drmd` | `urn:drmd:schema` |
| `dcc` | `https://ptb.de/dcc` |
| `si` | `https://ptb.de/si` |
| `qudt` | `http://qudt.org/vocab/` |
| `ds` | `http://www.w3.org/2000/09/xmldsig#` |

!!! warning "The DRMD namespace is a URN and is not resolvable"
    It is `urn:drmd:schema`, not an `https://` address. Nothing is served there. Do not attempt
    to dereference it, and do not treat a failure to fetch it as an error.

### 13.1.2 Recommended Parser Configuration
- Use a fully namespace-aware XML parser.
- **Disable external entity resolution** (XXE protection) and DTD loading. A DRMD document never
  needs either, and leaving them on exposes you to entity-expansion and file-disclosure attacks.
- **Set a limit on expansion and document size** before parsing, not after.
- If you validate structurally, resolve schema imports from the offline bundle in the schema
  repository's `supporting/` folder via its `catalog.xml`. Fetching schemas from the network at
  validation time is both a availability risk and a reproducibility risk: an upstream revision can
  change what counts as valid between two runs.

```bash
export XML_CATALOG_FILES=/path/to/schema/catalog.xml
```

---

## 13.2 Data Normalization Strategies

### 13.2.1 Multilingual Text Fallback (`dcc:textType`)
Many strings appear as `dcc:content` with an optional `@lang` attribute (ISO 639-1). Implement the following fallback algorithm for UI display:

1. If the application requests a specific language (e.g. `en`), select all `dcc:content[@lang='en']`.
2. If none match, look for `dcc:content` elements without a `@lang` attribute and treat them as
   the default.
3. If still none match, use the first available `dcc:content` regardless of language, and show
   the user which language they are reading.

Never silently render a German statement to an English-speaking user as though it were English.
Handling instructions and safety information are exactly the fields where a language mismatch
causes harm.

### 13.2.2 Identifier Normalization
When extracting `(scheme, value)` identifier pairs:
- Trim all whitespace.
- Normalize the `scheme` spelling (e.g., lowercasing).
- **Keep raw values unchanged** (as some identifier values are case-sensitive).

### 13.2.3 Numeric Precision
Store extracted values as high-precision numeric types (double or decimal). **Do not round values upon import.** Preserve the original lexical form to ensure round-trip integrity, and apply rounding logic only at the UI/display layer.

---

## 13.3 The Quantity Extraction Algorithm

The `drmd:quantity` element can carry its payload in several different XML types. A robust parser should implement a unified algorithm to extract the value, unit, and uncertainty based on the provided choice.

```mermaid
graph TD
    Q["Extract drmd:quantity"]
    
    Q --> CHK{Determine Payload Type}
    
    CHK -->|si:real| S_REAL["Extract:<br/>1. si:value<br/>2. si:unit<br/>3. si:measurementUncertaintyUnivariate"]
    CHK -->|si:realListXMLList| S_LIST["Extract:<br/>1. si:valueXMLList<br/>2. si:unitXMLList"]
    CHK -->|dcc:noQuantity| N_QUANT["Extract text from:<br/>dcc:content<br/><i>(Treat as non-numeric)</i>"]
    CHK -->|dcc:charsXMLList| C_LIST["Extract space-separated string"]
    
    S_REAL --> ID["Extract propertyIdentifiers (Scheme/Value)"]
    S_LIST --> ID
    N_QUANT --> ID
    C_LIST --> ID
    
    style Q fill:#e8eaf6,color:#000,stroke:#283593
    style CHK fill:#c5cae9,color:#000,stroke:#3949ab
    style S_REAL fill:#e3f2fd,color:#000,stroke:#1565c0
    style S_LIST fill:#e3f2fd,color:#000,stroke:#1565c0
    style N_QUANT fill:#e3f2fd,color:#000,stroke:#1565c0
    style C_LIST fill:#e3f2fd,color:#000,stroke:#1565c0
    style ID fill:#9fa8da,color:#000,stroke:#303f9f
```

!!! tip "Getting Certified Values"
    To query for certified values, filter your XPath to only include quantities descending from:
    `/drmd:digitalReferenceMaterialDocument/drmd:propertiesList/drmd:properties[@isCertified='true']`

---

## 13.4 Recommended Internal Object Model

When parsing the DRMD XML into your software's backend, it is highly recommended to map the XML structure into a simplified internal object model consisting of a few core entities.

```mermaid
classDiagram
    DRMDDocument "1" *-- "many" Material
    DRMDDocument "1" *-- "many" MaterialPropertySet
    MaterialPropertySet "1" *-- "many" Result
    Result "1" *-- "many" Quantity
    Quantity "1" *-- "many" Identifier

    class DRMDDocument {
        +String schemaVersion
        +CoreData coreData
        +Producer producer
        +List statements
        +List signatures
    }
    
    class Material {
        +String name
        +String description
        +Quantity minimumSampleSize
        +List identifiers
    }
    
    class MaterialPropertySet {
        +String name
        +Boolean isCertified
        +List procedures
    }
    
    class Result {
        +String name
    }
    
    class Quantity {
        +String payloadType
        +Float value
        +String unit
        +Uncertainty uncertainty
    }
    
    class Identifier {
        +String scheme
        +String value
        +String link
    }
```
