# Security & Trust Model

The trust model ensures that technical data (values, units, uncertainties) remains authentic and entirely unaltered from the moment of issuance by the Reference Material Producer (RMP) to the moment of automated consumption by an analytical instrument or Laboratory Information Management System (LIMS).

Structural validation and the business rules establish that a document *says the right things*.
They say nothing about whether it came from who it claims to, or whether anyone changed it in
transit. That is what this chapter covers, layer 3 of the
[three validation layers](validation_rules.md).

!!! warning "XSD validation is not signature verification"
    DRMD imports the complete W3C XML Signature schema, so XSD validation does check that a
    `ds:Signature` block is structurally well formed. It cannot recompute a digest or check a
    certificate chain. A document can be fully XSD-valid and carry a signature that does not
    verify at all, for example because the content was edited after signing. Never report
    "signed and valid" on the strength of schema validation.

---

## 14.1 Trust Store & Certificate Governance

Digital signatures (as defined in Chapter 8) are only as strong as the cryptographic infrastructure supporting them.

- **Trust Anchors:** Consumers (laboratories and software applications) must maintain a "Trust Store" of authorized Root Certificates from recognized Reference Material Producers (e.g., BAM, NIST, ERM).
- **Identity Verification:** RMPs should use organizational certificates (Electronic Seals) issued by Qualified Trust Service Providers (TSPs) to ensure the signature is legally linked to the institution, not just an individual.
- **Public Key Distribution:** Producers should publish their public keys or certificate fingerprints on official, secure websites (HTTPS) to allow software vendors to pre-configure trust.
- **Revocation Checks:** Software implementations should periodically check Certificate Revocation Lists (CRL) or use Online Certificate Status Protocol (OCSP) to ensure a producer's signing key hasn't been compromised.

---

## 14.2 Handling Embedded Documents

The DRMD schema allows embedding binary files like PDFs and images within the `drmd:document` element. Because these are "untrusted" data streams traversing the network, they require strict security processing.

!!! warning "Strict Payload Processing"
    Failure to properly sanitize embedded Base64 documents can result in malware execution or Denial-of-Service (DoS) attacks via memory exhaustion.

### Security Implementation Rules
1. **Size Limits:** To prevent "XML bomb" or memory exhaustion attacks, parsers should enforce a maximum size for `dcc:dataBase64` elements (e.g., a hard limit of 50 MB).
2. **Malware scanning:** scan extracted attachments before they are opened or written to disk. Treat every embedded file as untrusted input, whatever the document's signature says: a validly signed document can still embed a hostile attachment.
3. **MIME-Type Whitelisting:** Systems should only process a restricted list of safe formats (e.g., `application/pdf`, `image/png`, `image/jpeg`). Executable files (e.g., `.exe`, `.bat`, `.js`) MUST be outright rejected.
4. **Content Consistency:** Software should verify that the `dcc:fileName` extension matches the declared `dcc:mimeType` to prevent "extension spoofing".

---

## 14.3 Transport & Storage Integrity

Even with a digital signature present, the operational environment must protect the DRMD from accidental or malicious corruption during its lifecycle.

- **Secure Transport:** DRMDs should always be exchanged over encrypted channels (e.g., HTTPS, SFTP, or TLS-encrypted API calls).
- **Storage Immutability:** Once a DRMD is imported into a LIMS or instrument library, it should be marked as **Read-Only**. Any changes to the data must require the issuance of a new DRMD with a completely new `uniqueIdentifier`.
- **Hashing for Quick Verification:** Systems should generate and store a cryptographic hash (e.g., SHA-256) of the entire DRMD file upon import. This allows for rapid integrity checks without performing a full, expensive XMLDSig verification every time the file is accessed.
- **Audit trail requirements:** log every security-relevant event in a local audit trail for regulatory review: signature verification success and failure, certificate expiry warnings, and attachment extractions.

---

## 14.4 Summary of Security Responsibilities

Security is a shared responsibility across the entire supply chain. 

| Stakeholder | Primary Responsibility |
|-------------|------------------------|
| **Reference Material Producer** | Signs the document with a valid, non-expired organizational seal. Securely distributes their public keys. |
| **Software Developer** | Implements automated signature validation, strict XML parsing, and attachment malware scanning. |
| **Laboratory (End User)** | Maintains the local trust store and reviews system audit logs for any signature failures. |
| **Auditor** | Verifies that the digital "Chain of Trust" is intact, logged, and policy-compliant. |
