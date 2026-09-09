# Introduction & Overview

Welcome to the **Best Practice Guidelines** for the **Digital Reference Material Document (DRMD)**.

This guide provides comprehensive instructions for machine manufacturers, reference material producers, and software developers to ensure consistent, interoperable, and automated handling of DRMD certificates across different platforms.

<style>
.drmd-acronym-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin: 30px 0;
    align-items: flex-start;
}
.drmd-column {
    display: flex;
    flex-direction: column;
}
.drmd-letter-heading {
    border-bottom: 2px solid #000;
    padding-bottom: 8px;
    margin-bottom: 15px;
    display: flex;
    align-items: baseline;
    justify-content: center;
    white-space: nowrap;
}
.drmd-big-letter {
    font-size: 2.8rem;
    font-weight: 800;
    color: #d32f2f;
    line-height: 0.85;
}
.drmd-rest-word {
    font-size: 1.2rem;
    font-weight: 700;
    color: #000;
    margin-left: 2px;
}
.drmd-desc {
    font-size: 0.9rem;
    line-height: 1.5;
    color: #333;
    text-align: justify;
}
@media (max-width: 768px) {
    .drmd-acronym-container {
        grid-template-columns: 1fr;
        gap: 25px;
    }
}
</style>

<div class="drmd-acronym-container">
    <div class="drmd-column">
        <div class="drmd-letter-heading">
            <span class="drmd-big-letter">D</span><span class="drmd-rest-word">igital</span>
        </div>
        <div class="drmd-desc">
            The term Digital represents our process of converting standard PDF formats into fully machine-readable formats for automated data processing.
        </div>
    </div>
    <div class="drmd-column">
        <div class="drmd-letter-heading">
            <span class="drmd-big-letter">R</span><span class="drmd-rest-word">eference</span>
            <span class="drmd-big-letter" style="margin-left: 12px;">M</span><span class="drmd-rest-word">aterial</span>
        </div>
        <div class="drmd-desc">
            The Reference Material forms the core engine of this project, acting as the foundational source of truth for all data verification.
        </div>
    </div>
    <div class="drmd-column">
        <div class="drmd-letter-heading">
            <span class="drmd-big-letter">D</span><span class="drmd-rest-word">ocument</span>
        </div>
        <div class="drmd-desc">
            The Document signifies the final structured layout specifically designed to output Certified Reference Materials (CRM) and Product Information Sheets.
        </div>
    </div>
</div>
!!! info "What is the DRMD?"
    The DRMD is a standardised XML format for the documentation that accompanies a reference material. Its content follows **ISO 33401:2024**, *Reference materials: Contents of certificates, labels and accompanying documentation*, which is the standard that says what an RM certificate and a product information sheet must contain.

    ISO 33401:2024 is complementary to **ISO 17034:2016**, *General requirements for the competence of reference material producers*: ISO 17034 governs how a producer works, ISO 33401 governs what the resulting document says. Two further standards are referenced where they apply: **ISO Guide 35:2017** for characterisation, homogeneity and stability, and **ISO/IEC Guide 98-3 (GUM)** for the expression of measurement uncertainty.

## The DRMD Ecosystem

The DRMD schema transforms static PDF certificates into a machine-readable ecosystem. By moving to structured data, it enables:

- **Automated parsing** without manual data entry.
- **Seamless LIMS integration** for analytical laboratories.
- **Standardized data exchange** between producers and end-users.
- **Regulatory compliance** through structured traceability and uncertainty data.

### How it works

```mermaid
graph LR
    %% Styles
    classDef producer fill:#e3f2fd,stroke:#0288d1,stroke-width:2px;
    classDef schema fill:#f3e5f5,stroke:#e65100,stroke-width:2px;
    classDef user fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

    P[RM Producer]:::producer -->|Generates XML| XSD[(DRMD Schema &<br>Schematron Validation)]:::schema
    XSD -->|Validates & Ingests| U[LIMS & Instruments]:::user
```

## Target Audience

This best practice guide is designed for multiple stakeholders across the quality infrastructure:

=== "Machine Manufacturers & Software"
    Developers of LIMS, ELN, and analytical instrument software who need to confidently import, parse, and process DRMD certificates.

=== "Reference Material Producers"
    Organizations certified according to ISO 17034 who generate and distribute DRMD certificates. This guide ensures your output achieves maximum interoperability.

=== "End-Users & Laboratories"
    Quality control departments and calibration facilities that load DRMD certificates into their systems and require a deep understanding of the certificate structure.

=== "Auditors & Regulators"
    Quality Assurance personnel responsible for verifying data integrity, cryptographic signatures, and maintaining audit trails for compliance.

---

## The four-tier severity model

An XML Schema can check that a document is well formed and structurally complete. It cannot say *"if this is a certificate, then metrological traceability is required"*. XSD 1.0 has no way to make one requirement depend on the value of another element. That conditional logic lives in the companion **Schematron** file, `drmd-business-rules.sch`.

Each rule carries a severity that maps directly onto an ISO 33401:2024 requirement level, so a validation report can be read against the standard without interpretation.

!!! failure "Hard error, `role="error"`"
    **ISO level: Mandatory.** The document is non-compliant and must fail conformance validation. Example: a certificate without a `metrologicalTraceability` statement (RMC-001), or a material with no identifier of its own (DRMD-016).

!!! warning "Conditional error, `role="conditional-error"`"
    **ISO level: Mandatory whenever applicable.** Required if the requirement applies to *this* material. Where it genuinely does not apply, absence is acceptable, and it is the producer, not the validator, who makes that judgement. Example: `minimumSampleSize` (DRMD-008), `commutability` (DRMD-013).

!!! tip "Warning, `role="warning"`"
    **ISO level: Recommended.** The document is compliant. The element is recommended and makes the document more useful. Example: `healthAndSafetyInformation` (DRMD-015).

!!! note "No rule"
    **ISO level: Optional.** Accepted when present, never flagged when absent. Example: `legalNotice`, `subcontractors`.

`conditional-error` is a custom role. The Schematron specification allows any string in `@role`, and standard processors report it as an ordinary failed assertion. A validation pipeline must read the `role` attribute and classify accordingly: a tool that treats every failed assertion as a hard error will wrongly reject documents where a conditional requirement genuinely does not apply.

---

## How to read this guide

In the following chapters, we will break down the DRMD schema into its **Six Core Containers**, providing you with best-practice examples, XML snippets, and strict rules for implementation:

1. **Administrative Data**
2. **Materials**
3. **Properties List**
4. **Statements**
5. **Comments & Documents**
6. **Digital Signature**

Click **Next** below to start with the schema overview and architecture.

---

## Where things live

| Repository | Holds |
|---|---|
| **Schema** | `drmd.xsd`, `drmd-business-rules.sch`, the vendored supporting schemas, worked examples, the rule test suite, and the validation tools. |
| **Best practice** (this site) | These guidelines, the interactive schema tree, and the implementation checklists. |

The current specification version is **1.0.0**, the first release.
