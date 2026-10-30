# DRMD Guidance Document

The published guidance for the **Digital Reference Material Document (DRMD)**, an XML format for
reference material certificates and product information sheets, aligned with **ISO 33401:2024**.

This repository holds the documentation site only. The schema itself, its validation rules and
its worked examples live in the companion **schema** repository.

**Published site:** https://punitharumilli.github.io/BestPracticeDocs/

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
├── LICENSE                        CC BY 4.0, the licence of the text (see "Licence" below)
├── LICENSES/                      EUPL-1.2 (code) and LGPL-3.0 / GPL-3.0 (schema tree data)
├── CONTRIBUTING.md                how to report an error or ask for a change
├── mkdocs.yml                     site configuration and navigation
├── requirements.txt               build dependencies, every package pinned
├── overrides/main.html            theme override: BAM logo in the sidebar
├── tools/
│   └── build_schema_tree.py       regenerates the interactive tree data from the schema
└── docs/
    ├── index.md                   introduction, severity model
    ├── architecture.md            the six containers, namespaces, dependencies
    ├── administrative_data.md     … one chapter per part of the schema
    ├── iso_mapping.md             ISO 33401:2024 Table 1, row by row
    ├── checklists.md              per-role implementation checklists
    ├── licence.md                 licence of text, code and data; third-party software
    ├── schema_tree.md             the interactive D3 schema explorer
    ├── schema_data/schema.json    generated, do not edit by hand
    └── assets/                    logo, styles, scripts, fonts, downloadable checklists
```

## Privacy and security

The site loads nothing from other servers: the fonts (Inter, JetBrains Mono), the diagram library
(Mermaid 11.16.1) and the library of the schema tree (D3 7.9.0) are served from `docs/assets`.
Reading the guide therefore sends no visitor data to Google Fonts, unpkg or any other service, and
no code from another server runs on the site.

The language menu offers a German machine translation by Google Translate. It opens the current page
on Google's translation address (translate.goog) only when a reader chooses **Deutsch**; nothing
from Google is loaded into the site itself, and no cookie is set.

The build installs only the exact package versions in `requirements.txt` (tested with Python 3.13),
and each GitHub Action in the workflow is pinned to a reviewed commit.

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

## Changes and contributions

BAM maintains the guidance document. If you find an error or need a change, please tell us instead
of publishing a changed copy: open an issue in this repository or write to
[drmd@bam.de](mailto:drmd@bam.de). BAM reviews each request and publishes the change on the site,
so that everyone works with the same guidance. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Copyright (c) 2024 Bundesanstalt für Materialforschung und -prüfung (BAM)

| What | Licence |
|---|---|
| The text of the guidance document, its tables and diagrams, and the checklists (`docs/*.md`, `docs/assets/pdfs/`) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), see [`LICENSE`](LICENSE) |
| The code: the page template (`overrides/`), the scripts and style sheets (`docs/assets/js/translate.js`, `docs/assets/css/`), the script and style sheet embedded in `docs/schema_tree.md`, `tools/build_schema_tree.py` and the workflow in `.github/` | EUPL v1.2, see [`LICENSES/EUPL-1.2.txt`](LICENSES/EUPL-1.2.txt) |
| `docs/schema_data/schema.json`, generated from the DRMD schema and rules (BAM) and from the DCC and D-SI schemas (Physikalisch-Technische Bundesanstalt, PTB), whose annotations it contains | GNU LGPL v3, see [`LICENSES/LGPL-3.0.txt`](LICENSES/LGPL-3.0.txt) and [`LICENSES/GPL-3.0.txt`](LICENSES/GPL-3.0.txt) |
| Fonts, Mermaid, D3 (`docs/assets/fonts/`, `docs/assets/js/`) | Their own licences, in the files next to them; see `docs/licence.md` |
| The BAM name and logo (`docs/assets/BAM_Logo_RGB.jpg`) | Not licensed; they belong to BAM |

CC BY 4.0 lets anyone share and adapt the text, provided they credit BAM, link to the licence and
say if they changed it; it gives no right to suggest that BAM endorses them. How to credit, the
licences of the site's third-party software and their texts are on the page
[Licence & Credits](docs/licence.md), which is also part of the published site.

The development of the Digital Reference Material Document (DRMD) is partially funded and
supported by the [QI-Digital](https://www.qi-digital.de/) project.
