# Licence and Credits

Copyright © 2024 Bundesanstalt für Materialforschung und -prüfung (BAM)

This guidance document is published by the **Bundesanstalt für Materialforschung und -prüfung
(BAM)**. The development of the Digital Reference Material Document (DRMD) is partially funded and
supported by the [QI-Digital](https://www.qi-digital.de/) project.

## Licence of this guidance document

The text of this guidance document, its tables and diagrams, and the checklists (including the
PDF checklists) are licensed under the
[Creative Commons Attribution 4.0 International licence (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
You may share and adapt them for any purpose, provided that you give appropriate credit, provide a
link to the licence and indicate if changes were made. The licence gives no permission to suggest
that BAM endorses you or your use, and it does not license trademarks.

**How to credit.** For example:

> DRMD guidance document, © 2024 Bundesanstalt für Materialforschung und -prüfung (BAM),
> <https://punitharumilli.github.io/BestPracticeDocs/>, licensed under
> [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

If you changed the material, add that you did, for example "adapted from …".

The guidance document is provided as is, without warranty of any kind (Section 5 of the licence).

**Not covered by this licence:**

* the name and the logo of BAM;
* standards and other documents that are cited or briefly quoted, such as ISO 33401:2024,
  ISO 17034:2016 and the D-SI guide: they remain under the terms of their publishers;
* the data of the interactive schema tree and the third-party software listed below, which have
  their own licences;
* the code of this site, see the next section.

## Licence of the code of this site

The scripts, style sheets and page template of this site, the script and style sheet of the
interactive schema tree, the tool that generates its data (`tools/build_schema_tree.py`) and the
publishing workflow are licensed under the
[European Union Public Licence v1.2 (EUPL-1.2)](https://interoperable-europe.ec.europa.eu/collection/eupl/eupl-text-eupl-12).

## Data of the interactive schema tree

`schema_data/schema.json`, which the [Schema Interactive Tree](schema_tree.md) displays, is
generated from the DRMD schema and business rules (Copyright © 2024 BAM) and from the DCC and D-SI
schemas they use (Copyright © 2018–2024 Physikalisch-Technische Bundesanstalt, PTB). It contains
their annotations and is therefore licensed, like them, under the
[GNU Lesser General Public License, version 3](https://www.gnu.org/licenses/lgpl-3.0.html).

## Changes and suggestions

BAM maintains this guidance document. If you find an error or would like a change, please write
to [drmd@bam.de](mailto:drmd@bam.de) or open an issue in the repository of this site. BAM reviews
each request and publishes the change here, so that everyone works with the same guidance.

## Third-party software

The site uses the following open-source software. Each is used under its own licence, whose text
is linked or reproduced below.

| Component | Used for | Licence |
|---|---|---|
| [Material for MkDocs](https://github.com/squidfunk/mkdocs-material) 9.7.7 | Design, navigation and search of the site; the page template of this site is adapted from its template | MIT, text below |
| [Mermaid](https://github.com/mermaid-js/mermaid) 11.16.1 | Diagrams | MIT, [licence](assets/js/licenses/mermaid-LICENSE.txt) |
| [D3](https://github.com/d3/d3) 7.9.0 | Interactive schema tree | ISC, [licence](assets/js/licenses/d3-LICENSE.txt) |
| [Inter](https://github.com/rsms/inter) 4.0 | Typeface of the text | SIL Open Font License 1.1, [licence](assets/fonts/Inter-LICENSE.txt) |
| [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono) | Typeface of code | SIL Open Font License 1.1, [licence](assets/fonts/JetBrainsMono-LICENSE.txt) |

Material for MkDocs builds the following components into the scripts and icons of the site:

| Component | Licence |
|---|---|
| [RxJS](https://github.com/ReactiveX/rxjs) 7.8.2 | Apache License 2.0, Copyright (c) 2015-2018 Google, Inc., Netflix, Inc., Microsoft Corp. and contributors, [licence](assets/js/licenses/Apache-2.0.txt) |
| [clipboard.js](https://github.com/zenorocha/clipboard.js) 2.0.11, with [good-listener](https://github.com/zenorocha/good-listener) 1.2.2, [select](https://github.com/zenorocha/select) 1.1.2, [delegate](https://github.com/zenorocha/delegate) 3.2.0 (MIT, by Zeno Rocha) and [tiny-emitter](https://github.com/scottcorgan/tiny-emitter) 2.1.0 | MIT, text below |
| [escape-html](https://github.com/component/escape-html) 1.0.3 | MIT, text below |
| [focus-visible](https://github.com/WICG/focus-visible) 5.2.1 | W3C Software and Document License, [licence](assets/js/licenses/W3C-20150513.txt) |
| [tslib](https://github.com/microsoft/tslib) 2.7.0 | 0BSD, text below |
| [Lunr](https://github.com/olivernn/lunr.js) 2.3.9 | MIT, text below |
| [lunr-languages](https://github.com/MihaiValentin/lunr-languages) 1.14.0 | Mozilla Public License 1.1, [licence](assets/js/licenses/MPL-1.1.txt); the source code is available at the link |
| [Material Design Icons](https://github.com/Templarian/MaterialDesign-SVG) 7.4.47 | Pictogrammers Free License: icons under the Apache License 2.0, [licence](assets/js/licenses/Apache-2.0.txt) |

??? note "Licence texts: Material for MkDocs, clipboard.js, tiny-emitter, escape-html, Lunr, tslib"

    **Material for MkDocs 9.7.7**

    ```text
    Copyright (c) 2016-2025 Martin Donath <martin.donath@squidfunk.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.
    ```

    **clipboard.js 2.0.11**

    ```text
    MIT License

    Copyright (c) Zeno Rocha

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    ```

    **tiny-emitter 2.1.0**

    ```text
    The MIT License (MIT)

    Copyright (c) 2017 Scott Corgan

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    ```

    **escape-html 1.0.3**

    ```text
    (The MIT License)

    Copyright (c) 2012-2013 TJ Holowaychuk
    Copyright (c) 2015 Andreas Lubbe
    Copyright (c) 2015 Tiancheng "Timothy" Gu

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    'Software'), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    ```

    **Lunr 2.3.9**

    ```text
    Copyright (C) 2013 by Oliver Nightingale

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    ```

    **tslib 2.7.0**

    ```text
    Copyright (c) Microsoft Corporation.

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
    REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
    AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
    INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
    LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
    OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
    PERFORMANCE OF THIS SOFTWARE.
    ```
