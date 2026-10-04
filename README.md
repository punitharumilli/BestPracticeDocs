# DRMD Guidance Document

The published guidance for the **Digital Reference Material Document (DRMD)**, an XML format for
reference material certificates and product information sheets, aligned with **ISO 33401:2024**.

This repository holds the documentation site only. The schema itself, its validation rules and
its worked examples live in the companion **schema** repository.

**Published site:** https://punitharumilli.github.io/DRMD_Schema/

## Building locally

```bash
pip install -r requirements.txt
mkdocs serve          # live preview at http://127.0.0.1:8000
mkdocs build          # writes the static site to site/
```

`mkdocs.yml` sets `strict: true`, so a broken internal link or a missing nav entry fails the
build rather than being published.

## Structure

```
best-practice/
├── mkdocs.yml                     site configuration and navigation
├── requirements.txt               pinned build dependencies
├── overrides/main.html            theme override: BAM logo in the sidebar
├── tools/
│   └── build_schema_tree.py       regenerates the interactive tree data from the schema
└── docs/
    ├── index.md                   introduction, severity model
    ├── architecture.md            the six containers, namespaces, dependencies
    ├── administrative_data.md     … one chapter per part of the schema
    ├── iso_mapping.md             ISO 33401:2024 Table 1, row by row
    ├── checklists.md              per-role implementation checklists
    ├── schema_tree.md             the interactive D3 schema explorer
    ├── schema_data/schema.json    generated, do not edit by hand
    └── assets/                    logo, styles, scripts, downloadable checklists
```

## Keeping the site in step with the schema

`docs/schema_data/schema.json` drives the interactive schema tree. It is **generated** from
`drmd.xsd` and `drmd-business-rules.sch`, and is committed so that the site builds without the
schema repository present.

After any change to the schema, regenerate it and commit the result:

```bash
python tools/build_schema_tree.py --schema-dir ../schema
```

The script needs only `lxml`. It reads the XSD files as XML, so no XSD processor and no network
access are required.

When a validation rule is added, changed or retired, three places in this repository also need
updating, and none of them are generated:

1. `docs/validation_rules.md`, the complete rule catalogue.
2. `docs/iso_mapping.md`, the ISO 33401:2024 Table 1 mapping.
3. The `Business Rules Summary` table in whichever chapter covers that part of the schema.

## Licence

Copyright (c) 2024 Bundesanstalt für Materialforschung und -prüfung (BAM).
Documentation licensed under the GNU Lesser General Public License v3.0, in line with the schema.
The development of the Digital Reference Material Document (DRMD) is partially funded and
supported by the QI-Digital project.
