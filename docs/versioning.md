# Versioning & Backward Compatibility

Managing changes effectively prevents **"digital decay"**, where older certificates become unreadable by newer software, or newer certificates are suddenly rejected by legacy laboratory instruments.

This chapter defines the semantic versioning logic of the DRMD schema and the operational rules for updating certificates.

---

## 15.1 Breaking vs. Non-Breaking Changes

The DRMD follows strict semantic versioning logic to signal the impact of schema updates to developers.

| Change Type | Version Increment | Description |
|-------------|-------------------|-------------|
| **Breaking** | **Major** (e.g. `1.x` to `2.x`) | Renaming or removing an element, or changing a data type. Parsers need migration. |
| **Non-breaking** | **Minor** (e.g. `1.0.0` to `1.1.0`) | Adding optional elements or identifier schemes, and tightening conformance rules to match ISO 33401. Existing parsers keep working, though a document that passed before may now report a finding. |
| **Correction** | **Patch** (e.g. `1.0.0` to `1.0.1`) | Corrections to documentation and annotations. No change to the content model. |

The version applies to the specification as a whole: `drmd.xsd` and `drmd-business-rules.sch` carry the same number and are released together. The current version is **1.0.0**, the first release.

---

## 15.2 Handling Unknown Schema Versions

Software **MUST** implement version checking by inspecting the `@schemaVersion` attribute on the `drmd:digitalReferenceMaterialDocument` root element.

```mermaid
graph TD
    IN["Incoming DRMD<br/>@schemaVersion"]
    
    IN --> CHECK{Compare to<br/>Supported Version}
    
    CHECK -->|Major Version is Higher| MAJOR["STOP Processing<br/><i>(Breaking Changes Expected)</i>"]
    CHECK -->|Minor/Patch is Higher| MINOR["Attempt to Parse<br/><i>(Backward Compatible)</i>"]
    CHECK -->|Version is Lower/Equal| EQUAL["Parse Normally"]

    MINOR --> LENIENT["<b>Lenient Mode (Archival)</b><br/>Read available data, ignore unknown fields."]
    MINOR --> STRICT["<b>Strict Mode (Calibration)</b><br/>Enforce 100% schema compliance."]

    style IN fill:#e8eaf6,color:#000,stroke:#283593
    style CHECK fill:#c5cae9,color:#000,stroke:#3949ab
    style MAJOR fill:#ffebee,color:#000,stroke:#f44336
    style MINOR fill:#e3f2fd,color:#000,stroke:#1565c0
    style EQUAL fill:#e8f5e9,color:#000,stroke:#4caf50
    style LENIENT fill:#f5f5f5,stroke:#9e9e9e
    style STRICT fill:#f5f5f5,stroke:#9e9e9e
```

### Strict vs. Lenient Parsing Modes
It is highly recommended that parsers offer two modes:
- A **lenient mode** for archival viewing (reading whatever is possible, ignoring unknown optional fields added in minor updates).
- A **strict mode** for automated machine calibration (ensuring 100% schema compliance before trusting the values).

---

## 15.3 Migration Guidance

When a Reference Material Producer (RMP) updates a certificate or migrates to a new DRMD schema, the following operational rules apply:

1. **Document Re-issuance:** Any change to the technical content (e.g., a revised certified value) requires a completely new `uniqueIdentifier` (UUID) to be issued. You cannot quietly patch certified data.
2. **Stable Identifiers:** Even if a document is updated to a new version, the `materialIdentifiers` (like a batch number or catalog ID) SHOULD remain completely unchanged to maintain the link to the physical material.
3. **Upgrading Stored DRMDs:** When migrating a database of old DRMDs to a new schema version, software SHOULD preserve the original XML and the original digital signature as a "record of origin" before generating the transformed version.

---

## 15.4 Deprecation Policy

Fields or identifier schemes that are no longer recommended (e.g., an outdated unit string format or a decommissioned database link) will enter a strict "Deprecation" phase.

- **Warning Period:** a deprecated field stays in the schema for at least one minor version cycle and raises a `warning` during Schematron validation.
- **Removal:** Fields will only be actively removed in Major version updates.
- **Replacement:** Official documentation MUST provide a clear mapping from the deprecated field to the new recommended field to assist developers in updating their parsers.

---

## 15.5 Summary for Stakeholders

| Stakeholder | Best Practice |
|-------------|---------------|
| **Producers** | Always use the latest patch version for stability; never reuse a UUID for a modified document. |
| **Developers** | Implement "Future-Proof" parsing that gracefully ignores unknown optional elements in minor version updates. |
| **Laboratories** | Ensure your LIMS can store multiple versions of a certificate to maintain a complete, unbroken audit trail. |
