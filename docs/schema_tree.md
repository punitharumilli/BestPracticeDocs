---
hide:
  - navigation
  - toc
---

# 🌳 Schema Interactive Tree

<style>
/* Aggressively hide MkDocs sidebars on this specific page */
.md-sidebar { display: none !important; }
.md-sidebar--primary { display: none !important; }
.md-sidebar--secondary { display: none !important; }

/* Force container to allow full width */
.md-main__inner { margin: 0 !important; max-width: 100% !important; }
.md-content { max-width: 100% !important; width: 100% !important; }

/* Three pane layout, using the container breakout trick */
.schema-explorer {
    display: flex;
    height: 85vh;
    width: 96vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -48vw;
    margin-right: -48vw;
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 8px;
    overflow: hidden;
    background: var(--md-default-bg-color);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Left Pane: Tree View */
.pane-left {
    width: 250px;
    min-width: 200px;
    border-right: 1px solid var(--md-default-fg-color--lightest);
    overflow-y: auto;
    padding: 10px;
    background: var(--md-default-bg-color);
}
.tree-nav {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    line-height: 1.2;
}
.tree-nav ul {
    list-style-type: none;
    padding-left: 12px;
    margin: 0;
}
.tree-nav > ul { padding-left: 0; }
.tree-nav li {
    margin: 0;
    position: relative;
    white-space: nowrap;
}
.node-wrapper {
    display: inline-flex;
    align-items: center;
    padding: 1px 2px;
    border-radius: 3px;
    cursor: pointer;
}
.node-wrapper:hover { background: var(--md-default-fg-color--lightest); }
.tree-nav li.selected > .node-wrapper {
    background: #e3f2fd;
    outline: 1px solid #90caf9;
}
.node-icon {
    display: inline-block;
    width: 14px;
    height: 14px;
    line-height: 14px;
    text-align: center;
    border-radius: 2px;
    font-size: 9px;
    font-weight: bold;
    margin-right: 4px;
    color: #1565c0;
    background: #e3f2fd;
    border: 1px solid #90caf9;
}
.node-icon.attr {
    color: #ef6c00;
    background: #fff3e0;
    border-color: #ffcc80;
}
.node-icon.ct {
    color: #6a1b9a;
    background: #f3e5f5;
    border-color: #ce93d8;
}
.node-name { 
    color: var(--md-typeset-color);
    max-width: 130px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    display: inline-block;
    vertical-align: bottom;
}
.node-card {
    background: #fff9c4;
    border: 1px solid #fff59d;
    border-radius: 3px;
    padding: 0 4px;
    font-size: 9px;
    margin: 0 4px;
    color: #f57f17;
    font-weight: bold;
}
.node-type { 
    color: #757575; 
    font-size: 11px;
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    display: inline-block;
    vertical-align: bottom;
}
.expander {
    cursor: pointer;
    display: inline-block;
    width: 10px;
    text-align: center;
    margin-left: -10px;
    margin-right: 2px;
    position: relative;
    z-index: 2;
    background: transparent;
    color: #9e9e9e;
    font-size: 9px;
}

/* Center Pane: D3 Graph */
.pane-center {
    flex-grow: 1;
    position: relative;
    overflow: hidden;
    background: var(--md-code-bg-color); /* Light gray for contrast */
}

/* Right Pane: Details */
.pane-right {
    width: 350px;
    min-width: 250px;
    border-left: 1px solid var(--md-default-fg-color--lightest);
    overflow-y: auto;
    padding: 20px;
    background: var(--md-default-bg-color);
}

/* Custom JS Resizer Handles */
.resizer {
    width: 6px;
    background: var(--md-default-fg-color--lightest);
    cursor: col-resize;
    z-index: 10;
    transition: background 0.2s;
}
.resizer:hover, .resizer.dragging {
    background: var(--md-primary-fg-color);
}

.details-title {
    font-size: 1.5em;
    font-weight: bold;
    color: var(--md-primary-fg-color);
    margin-top: 0;
    margin-bottom: 10px;
    border-bottom: 2px solid var(--md-primary-fg-color);
    padding-bottom: 5px;
}
.badges {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
    flex-wrap: wrap;
}
.badge {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: bold;
}
.badge-type { background: #e3f2fd; color: #1565c0; }
.badge-cardinality { background: #fbe9e7; color: #d84315; }
.details-desc {
    font-size: 0.95em;
    line-height: 1.5;
    margin-bottom: 20px;
}

/* D3 Graph Styles */
.node rect {
    fill: var(--md-default-bg-color);
    stroke: var(--md-primary-fg-color);
    stroke-width: 1.5px;
    rx: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
}
.node.selected rect {
    fill: #e3f2fd;
    stroke: #1565c0;
    stroke-width: 2.5px;
    box-shadow: 0 0 10px rgba(21,101,192,0.3);
}
.node text {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
}
.node .name { font-weight: bold; fill: var(--md-typeset-color); }
.node .type { fill: #1565c0; font-size: 10px; }
.node .cardinality { fill: #d84315; font-size: 10px; text-anchor: end; }
.node .expand-btn { fill: #fff; stroke: var(--md-primary-fg-color); stroke-width: 1px; cursor: pointer; }
.node .expand-text { fill: var(--md-primary-fg-color); font-size: 10px; text-anchor: middle; cursor: pointer; font-family: monospace; }
.link {
    fill: none;
    stroke: #ccc;
    stroke-width: 1.5px;
}

.rule-card {
    background: #fff3e0;
    border-left: 4px solid #ff9800;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 0 4px 4px 0;
    font-size: 0.85em;
}
.rule-error { background: #ffebee; border-left-color: #f44336; }
.badge-choice { background: #ede7f6; color: #4527a0; }
.badge-abstract { background: #eceff1; color: #37474f; }
.abstract-note {
    background: #e3f2fd;
    border-left: 4px solid #1565c0;
    padding: 10px 12px;
    margin: 10px 0 0 0;
    border-radius: 0 4px 4px 0;
    font-size: 0.85em;
    line-height: 1.5;
}
.subs-list {
    background: #e3f2fd;
    margin: 0 0 14px 0;
    padding: 0 12px 10px 30px;
    border-left: 4px solid #1565c0;
    border-radius: 0 0 4px 0;
    font-size: 0.85em;
}
.subs-list code { background: rgba(0,0,0,0.06); padding: 0 4px; border-radius: 3px; font-weight: 700; }
.subs-type { color: #1565c0; font-family: 'Consolas', monospace; font-size: 0.9em; margin-left: 6px; }
.subs-desc { color: var(--md-default-fg-color--light); margin: 2px 0 6px 0; }
.choice-note {
    background: #ede7f6;
    border-left: 4px solid #673ab7;
    padding: 10px 12px;
    margin: 10px 0 14px 0;
    border-radius: 0 4px 4px 0;
    font-size: 0.85em;
    line-height: 1.5;
}
.choice-note code { background: rgba(0,0,0,0.06); padding: 0 4px; border-radius: 3px; }
.rule-conditional { background: #fff3e0; border-left-color: #ff9800; }
.rule-warning { background: #e8f5e9; border-left-color: #4caf50; }
.rule-severity {
    display: inline-block;
    font-size: 0.75em;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    padding: 1px 6px;
    border-radius: 3px;
    margin-right: 6px;
    vertical-align: 2px;
    color: #fff;
}
.sev-error { background: #c62828; }
.sev-conditional { background: #ef6c00; }
.sev-warning { background: #2e7d32; }

.bp-link {
    display: inline-block;
    margin: 10px 0 15px 0;
    padding: 8px 16px;
    background: linear-gradient(135deg, #3f51b5, #5c6bc0);
    color: #fff !important;
    text-decoration: none;
    border-radius: 6px;
    font-size: 0.85em;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(63,81,181,0.3);
}
.bp-link:hover {
    background: linear-gradient(135deg, #303f9f, #3f51b5);
    box-shadow: 0 4px 8px rgba(63,81,181,0.4);
    transform: translateY(-1px);
}
</style>

<div class="schema-explorer">
    <div class="pane-left" id="tree-nav">
        <!-- Vertical tree list -->
    </div>
    <div class="resizer" id="resizer-left"></div>
    <div class="pane-center" id="d3-graph">
        <!-- SVG Canvas -->
    </div>
    <div class="resizer" id="resizer-right"></div>
    <div class="pane-right" id="details-panel">
        <div class="details-title">Select an element</div>
        <div class="details-desc">Click on any node in the center graph or left tree to view its details, description, and validation rules.</div>
    </div>
</div>

<!-- Load D3.js -->
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
function initResizers() {
    const resizerLeft = document.getElementById('resizer-left');
    const resizerRight = document.getElementById('resizer-right');
    const paneLeft = document.getElementById('tree-nav');
    const paneRight = document.getElementById('details-panel');
    const container = document.querySelector('.schema-explorer');

    let isResizingLeft = false;
    let isResizingRight = false;
    let startX;
    let startWidthLeft;
    let startWidthRight;

    resizerLeft.addEventListener('mousedown', function(e) {
        isResizingLeft = true;
        startX = e.clientX;
        startWidthLeft = paneLeft.getBoundingClientRect().width;
        resizerLeft.classList.add('dragging');
        document.body.style.cursor = 'col-resize';
        e.preventDefault();
    });

    resizerRight.addEventListener('mousedown', function(e) {
        isResizingRight = true;
        startX = e.clientX;
        startWidthRight = paneRight.getBoundingClientRect().width;
        resizerRight.classList.add('dragging');
        document.body.style.cursor = 'col-resize';
        e.preventDefault();
    });

    document.addEventListener('mousemove', function(e) {
        if (!isResizingLeft && !isResizingRight) return;
        
        if (isResizingLeft) {
            const newWidth = startWidthLeft + (e.clientX - startX);
            if (newWidth > 150 && newWidth < (container.getBoundingClientRect().width - 300)) {
                paneLeft.style.width = `${newWidth}px`;
                paneLeft.style.flex = `0 0 ${newWidth}px`;
            }
        }
        
        if (isResizingRight) {
            const newWidth = startWidthRight - (e.clientX - startX);
            if (newWidth > 200 && newWidth < (container.getBoundingClientRect().width - 300)) {
                paneRight.style.width = `${newWidth}px`;
                paneRight.style.flex = `0 0 ${newWidth}px`;
            }
        }
    });

    document.addEventListener('mouseup', function(e) {
        if (isResizingLeft) {
            isResizingLeft = false;
            resizerLeft.classList.remove('dragging');
        }
        if (isResizingRight) {
            isResizingRight = false;
            resizerRight.classList.remove('dragging');
        }
        document.body.style.cursor = '';
    });
}

function initSchemaTree() {
    const treeNav = document.querySelector("#tree-nav");
    if (!treeNav) return; // Not on the schema tree page
    // Prevent double initialization if navigating back or if async fetch is already in progress
    if (treeNav.children.length > 0 || treeNav.dataset.loading === "true") return;
    treeNav.dataset.loading = "true";

    let globalData = null;
    let selectedNode = null;
    let resizeTimer = null;

    // Fetch data
    fetch("../schema_data/schema.json")
        .then(response => {
            if (!response.ok) throw new Error("HTTP error " + response.status);
            return response.json();
        })
        .then(data => {
            globalData = data;
            initNavTree(data);
            initD3Graph(data);
            initResizers(); // Hook up custom drag handlers
            selectNode(data, null); // select root by default
            
            // Set up debounced ResizeObserver to redraw graph on container resize
            const d3Container = document.getElementById("d3-graph");
            const ro = new ResizeObserver(() => {
                if (resizeTimer) clearTimeout(resizeTimer);
                resizeTimer = setTimeout(() => {
                    if (globalData) {
                        initD3Graph(globalData);
                        if (selectedNode) selectNode(selectedNode);
                    }
                }, 150); // Debounce to prevent duplicate render calls
            });
            ro.observe(d3Container);
        })
        .catch(err => {
            console.error("Error loading schema:", err);
            document.getElementById("d3-graph").innerHTML = `<div style="color:red; padding:20px;">Failed to load schema data. Check console.</div>`;
        });

    // Best Practice deep-link mapping (element name → anchor on admin page)
    const bestPracticeLinks = {
        'administrativeData': 'administrative_data/#structure-at-a-glance',
        'coreData': 'administrative_data/#31-core-data-coredata',
        'titleOfTheDocument': 'administrative_data/#311-title-of-the-document-titleofthedocument',
        'uniqueIdentifier': 'administrative_data/#312-unique-identifier-uniqueidentifier',
        'documentVersion': 'administrative_data/#313-document-version-documentversion',
        'documentIdentifiers': 'administrative_data/#314-document-identifiers-documentidentifiers',
        'documentIdentifier': 'administrative_data/#314-document-identifiers-documentidentifiers',
        'scheme': 'administrative_data/#314-document-identifiers-documentidentifiers',
        'value': 'administrative_data/#314-document-identifiers-documentidentifiers',
        'validity': 'administrative_data/#315-validity-validity',
        'untilRevoked': 'administrative_data/#315-validity-validity',
        'timeAfterDispatch': 'administrative_data/#315-validity-validity',
        'specificTime': 'administrative_data/#315-validity-validity',
        'dispatchDate': 'administrative_data/#315-validity-validity',
        'period': 'administrative_data/#315-validity-validity',
        'referenceMaterialProducer': 'administrative_data/#32-reference-material-producer-referencematerialproducer',
        'name': 'administrative_data/#321-name',
        'contact': 'administrative_data/#322-contact',
        'descriptionData': 'administrative_data/#323-descriptiondata-optional-attachment',
        'cryptElectronicSeal': 'administrative_data/#324-cryptographic-capability-flags-optional-booleans',
        'cryptElectronicSignature': 'administrative_data/#324-cryptographic-capability-flags-optional-booleans',
        'cryptElectronicTimeStamp': 'administrative_data/#324-cryptographic-capability-flags-optional-booleans',
        'organizationIdentifiers': 'administrative_data/#325-organization-identifiers-optional-list',
        'organizationIdentifier': 'administrative_data/#325-organization-identifiers-optional-list',
        'respPersons': 'administrative_data/#33-responsible-persons-resppersons',
        'respPerson': 'administrative_data/#331-responsible-person-entry-respperson',
        'person': 'administrative_data/#332-person-details-dccperson',
        'mainSigner': 'administrative_data/#331-responsible-person-entry-respperson',
        'role': 'administrative_data/#331-responsible-person-entry-respperson',
        'comment': 'comments_documents/#72-comment-comment',
        'document': 'comments_documents/#73-document-document',
        'materials': 'materials/#42-materials-list',
        'material': 'materials/#43-material-entry-material',
        'description': 'materials/#432-description-description',
        'materialClass': 'materials/#44-material-classification-materialclass',
        'minimumSampleSize': 'materials/#451-minimum-sample-size-minimumsamplesize',
        'itemQuantities': 'materials/#452-item-quantities-itemquantities',
        'real': 'materials/#461-option-a-sireal',
        'noQuantity': 'materials/#462-option-b-dccnoquantity',
        'realListXMLList': 'materials/#463-option-c-sireallistxmllist',
        'charsXMLList': 'materials/#464-option-d-dcccharsxmllist',
        'textType': 'parsing_guide/#1321-multilingual-text-fallback-dcctexttype',
        'propertiesList': 'properties/#52-properties-list-propertieslist',
        'properties': 'properties/#53-properties-block-properties',
        'results': 'properties/#54-results-list-results',
        'result': 'properties/#55-result-type-result',
        'data': 'properties/#56-data-type-data',
        'list': 'properties/#57-list-type-list',
        'quantity': 'properties/#58-quantity-type-quantity',
        'propertyIdentifiers': 'properties/#59-property-identifiers-propertyidentifiers',
        'procedures': 'properties/#5101-procedures-procedures',
        'measurementMetaData': 'properties/#5102-measurement-metadata-measurementmetadata',
        'statements': 'statements/#63-standard-statements',
        'richContentType': 'statements/#62-common-content-model-dccrichcontenttype',
        'intendedUse': 'statements/#631-intended-use-intendeduse',
        'commutability': 'statements/#632-commutability-commutability',
        'storageInformation': 'statements/#633-storage-information-storageinformation',
        'instructionsForHandlingAndUse': 'statements/#634-instructions-for-handling-and-use-instructionsforhandlinganduse',
        'metrologicalTraceability': 'statements/#635-metrological-traceability-metrologicaltraceability',
        'healthAndSafetyInformation': 'statements/#636-health-and-safety-information-healthandsafetyinformation',
        'subcontractors': 'statements/#637-subcontractors-subcontractors',
        'legalNotice': 'statements/#638-legal-notice-legalnotice',
        'referenceToCertificationReport': 'statements/#639-reference-to-certification-report-referencetocertificationreport',
        'statement': 'statements/#6310-statement-catch-all-statement',
        'unit': 'units_quantities/#111-unit-strings-siunit',
        'Signature': 'signatures/#71-signature-element-signature',
    };

    let selectedParent = null;

    // Walk from the root to find the parent of a node, so the details panel can list the
    // other options of a choice. The D3 hierarchy carries a parent link, but the left-hand
    // nav passes raw data objects, which do not.
    function findParent(node, target) {
        if (!node || !node.children) return null;
        for (const child of node.children) {
            if (child === target) return node;
            const hit = findParent(child, target);
            if (hit) return hit;
        }
        return null;
    }

    function selectNode(d, parent) {
        const data = d.data || d;
        selectedNode = data;
        selectedParent = parent || (d.parent && d.parent.data) || findParent(globalData, data) || null;
        
        const panel = document.getElementById("details-panel");
        let html = `<div class="details-title">${data.name || 'Unnamed Element'}</div>`;
        html += `<div class="badges">`;
        if (data.type) html += `<span class="badge badge-type">Type: ${data.type}</span>`;
        if (data.cardinality) html += `<span class="badge badge-cardinality">Cardinality: ${data.cardinality}</span>`;
        if (data.base) html += `<span class="badge" style="background:#e8f5e9; color:#2e7d32;">Base: ${data.base}</span>`;
        if (data.compositor === "choice") html += `<span class="badge badge-choice">One of a choice</span>`;
        if (data.abstract) html += `<span class="badge badge-abstract">Abstract</span>`;
        html += `</div>`;

        // A choice must never be read as "all of these are required". The cardinality on each
        // option is its cardinality *if that option is the one used*, not a requirement to
        // include it alongside the others.
        if (data.compositor === "choice") {
            const siblings = (selectedParent && selectedParent.children || [])
                .filter(c => c.compositor === "choice" && c.name !== data.name)
                .map(c => `<code>${c.name}</code>`);
            html += `<div class="choice-note"><strong>This element is one option of a choice.</strong> `
                  + `Exactly one option may appear here`
                  + (siblings.length ? `. The alternatives are ${siblings.join(", ")}.` : `.`)
                  + ` Its cardinality applies only when this option is the one used. It does not mean the element is required alongside the others.</div>`;
        }

        // An abstract element is never written in an instance document. Say so, and name what
        // is written instead. Otherwise the tree shows a placeholder with no way out of it.
        if (data.abstract) {
            html += `<div class="abstract-note"><strong>This element is abstract and is never written in a document.</strong> `;
            if (data.substitutions && data.substitutions.length) {
                html += `Use one of its substitutes in its place:</div><ul class="subs-list">`;
                data.substitutions.forEach(sub => {
                    html += `<li><code>${sub.name}</code>`
                          + (sub.type ? ` <span class="subs-type">${sub.type}</span>` : ``)
                          + (sub.description ? `<div class="subs-desc">${sub.description}</div>` : ``)
                          + `</li>`;
                });
                html += `</ul>`;
            } else {
                html += `No substitute is defined in the schemas bundled here.</div>`;
            }
        }

        html += `<div class="details-desc">${data.description || '<i>No description available.</i>'}</div>`;

        // Best Practice link
        const bpLink = bestPracticeLinks[data.name];
        if (bpLink) {
            html += `<a href="../${bpLink}" class="bp-link" target="_blank">See Best Practice &rarr;</a>`;
        }
        
        if (data.enumerations && data.enumerations.length > 0) {
            html += `<h3>Enumerations</h3><ul>`;
            data.enumerations.forEach(en => {
                html += `<li><code>${en}</code></li>`;
            });
            html += `</ul>`;
        }
        
        if (data.attributes && data.attributes.length > 0) {
            html += `<h3>Attributes</h3><ul>`;
            data.attributes.forEach(attr => {
                html += `<li><strong>@${attr.name}</strong>: ${attr.type} (${attr.use})<br><i>${attr.description}</i></li>`;
            });
            html += `</ul>`;
        }

        if (data.rules && data.rules.length > 0) {
            html += `<h3>Business Rules</h3>`;
            const SEVERITY = {
                "error":             { card: "rule-error",       chip: "sev-error",       label: "Error" },
                "conditional-error": { card: "rule-conditional", chip: "sev-conditional", label: "Conditional" },
                "warning":           { card: "rule-warning",     chip: "sev-warning",     label: "Warning" }
            };
            data.rules.forEach(rule => {
                const sev = SEVERITY[rule.role] || SEVERITY["error"];
                html += `<div class="rule-card ${sev.card}">
                    <span class="rule-severity ${sev.chip}">${sev.label}</span>
                    <strong>[${rule.id}]</strong> ${rule.description}
                </div>`;
            });
        }
        
        panel.innerHTML = html;
        
        document.querySelectorAll('.tree-nav li').forEach(li => li.classList.remove('selected'));
        const navEl = document.getElementById(`nav-${data.name}`);
        if(navEl) navEl.classList.add('selected');

        // Highlight D3 node
        if (typeof d3 !== 'undefined') {
            d3.selectAll("g.node").classed("selected", false);
            d3.selectAll("g.node").filter(n => (n.data || n) === data).classed("selected", true);
        }
    }

    // ==========================================
    // LEFT PANE: NAV TREE
    // ==========================================
    function initNavTree(data) {
        const container = document.getElementById("tree-nav");
        container.innerHTML = ""; // Clear existing navigation tree to prevent duplication from async fetch race condition
        const nav = document.createElement('div');
        nav.className = "tree-nav";
        
        function buildUL(nodeData, depth = 0) {
            const ul = document.createElement('ul');
            
            const li = document.createElement('li');
            li.id = `nav-${nodeData.name}`;
            
            const hasChildren = (nodeData.children && nodeData.children.length > 0) || (nodeData.attributes && nodeData.attributes.length > 0);
            const isOpenByDefault = depth <= 1;
            
            // Expander
            const exp = document.createElement('span');
            exp.className = 'expander';
            if (hasChildren) {
                exp.innerText = isOpenByDefault ? '▼' : '▶'; // Open if depth <= 1
                exp.onclick = (e) => {
                    e.stopPropagation();
                    const childUl = li.querySelector('ul');
                    if (childUl.style.display === 'none') {
                        childUl.style.display = 'block';
                        exp.innerText = '▼';
                    } else {
                        childUl.style.display = 'none';
                        exp.innerText = '▶';
                    }
                };
            } else {
                exp.innerText = ' ';
            }
            li.appendChild(exp);
            
            const wrapper = document.createElement('div');
            wrapper.className = 'node-wrapper';
            wrapper.onclick = (e) => {
                e.stopPropagation();
                selectNode(nodeData);
            };
            
            wrapper.innerHTML = `
                <span class="node-icon">E</span>
                <span class="node-name">${nodeData.name}</span>
                ${nodeData.cardinality ? `<span class="node-card">${nodeData.cardinality}</span>` : ''}
                <span class="node-type">: ${nodeData.type || 'complexType'}</span>
            `;
            li.appendChild(wrapper);
            
            if (hasChildren) {
                const childUl = document.createElement('ul');
                childUl.style.display = isOpenByDefault ? 'block' : 'none';
                
                // Add attributes first
                if (nodeData.attributes) {
                    nodeData.attributes.forEach(attr => {
                        const attrLi = document.createElement('li');
                        // Add empty expander for alignment
                        const attrExp = document.createElement('span');
                        attrExp.className = 'expander';
                        attrExp.innerText = ' ';
                        attrLi.appendChild(attrExp);
                        
                        const attrWrapper = document.createElement('div');
                        attrWrapper.className = 'node-wrapper';
                        attrWrapper.onclick = (e) => { e.stopPropagation(); selectNode(nodeData); };
                        attrWrapper.innerHTML = `
                            <span class="node-icon attr">A</span>
                            <span class="node-name">@${attr.name}</span>
                            <span class="node-type">: ${attr.type}</span>
                        `;
                        attrLi.appendChild(attrWrapper);
                        childUl.appendChild(attrLi);
                    });
                }
                
                // Add children
                if (nodeData.children) {
                    nodeData.children.forEach(child => {
                        childUl.appendChild(buildUL(child, depth + 1).firstChild); // append the li
                    });
                }
                li.appendChild(childUl);
            }
            ul.appendChild(li);
            return ul;
        }
        
        nav.appendChild(buildUL(data, 0));
        container.appendChild(nav);
    }

    // ==========================================
    // CENTER PANE: D3 GRAPH
    // ==========================================
    function initD3Graph(data) {
        const container = document.getElementById("d3-graph");
        
        // Clear previous SVG/DOM elements to prevent duplication
        container.innerHTML = "";
        
        const width = container.clientWidth;
        const height = container.clientHeight;
        
        const margin = {top: 20, right: 90, bottom: 30, left: 90};
        const dx = 50; // vertical spacing
        const dy = 250; // horizontal spacing
        const nodeWidth = 220;
        const nodeHeight = 60;
        
        const svg = d3.select("#d3-graph").append("svg")
            .attr("width", width)
            .attr("height", height)
            .style("cursor", "grab");
            
        const g = svg.append("g");
        
        // Zoom behavior
        const zoom = d3.zoom()
            .scaleExtent([0.1, 3])
            .on("zoom", (event) => {
                g.attr("transform", event.transform);
            });
        svg.call(zoom).on("dblclick.zoom", null);
        
        // Center the root node
        const initialTransform = d3.zoomIdentity.translate(50, height/2).scale(0.8);
        svg.call(zoom.transform, initialTransform);
        
        const tree = d3.tree().nodeSize([dx + nodeHeight, dy]);
        
        const root = d3.hierarchy(data);
        root.x0 = 0;
        root.y0 = 0;
        
        // Collapse all children of root by default to keep it tidy
        if (root.children) {
            root.children.forEach(collapse);
        }
        
        function collapse(d) {
            if (d.children) {
                d._children = d.children;
                d._children.forEach(collapse);
                d.children = null;
            }
        }
        
        update(root);
        
        function update(source) {
            const treeData = tree(root);
            const nodes = treeData.descendants();
            const links = treeData.links();
            
            // Normalize for fixed-depth
            nodes.forEach(d => { d.y = d.depth * dy; });
            
            let i = 0;
            const node = g.selectAll("g.node")
                .data(nodes, d => d.id || (d.id = ++i));
                
            // Enter any new nodes at the parent's previous position.
            const nodeEnter = node.enter().append("g")
                .attr("class", "node")
                .attr("transform", d => `translate(${source.y0},${source.x0})`)
                .on("click", (event, d) => {
                    selectNode(d, d.parent ? d.parent.data : null);
                });
                
            // Draw Box
            nodeEnter.append("rect")
                .attr("width", nodeWidth)
                .attr("height", nodeHeight)
                .attr("y", -nodeHeight/2)
                .attr("x", 0);
                
            // Text: Name
            nodeEnter.append("text")
                .attr("class", "name")
                .attr("x", 10)
                .attr("y", -10)
                .text(d => d.data.name.length > 25 ? d.data.name.substring(0, 22) + '...' : d.data.name);
                
            // Text: Type
            nodeEnter.append("text")
                .attr("class", "type")
                .attr("x", 10)
                .attr("y", 10)
                .text(d => d.data.type);
                
            // Text: Cardinality
            nodeEnter.append("text")
                .attr("class", "cardinality")
                .attr("x", nodeWidth - 10)
                .attr("y", -10)
                .text(d => d.data.cardinality);
                
            // Expand Button (only if has children)
            const btnGroup = nodeEnter.append("g")
                .attr("transform", `translate(${nodeWidth}, 0)`)
                .style("display", d => (d.children || d._children) ? "block" : "none")
                .on("click", (event, d) => {
                    event.stopPropagation();
                    if (d.children) {
                        d._children = d.children;
                        d.children = null;
                    } else {
                        d.children = d._children;
                        d._children = null;
                    }
                    update(d);
                });
                
            btnGroup.append("rect")
                .attr("class", "expand-btn")
                .attr("width", 16)
                .attr("height", 16)
                .attr("y", -8)
                .attr("x", -8)
                .attr("rx", 3);
                
            btnGroup.append("text")
                .attr("class", "expand-text")
                .attr("y", 3)
                .text(d => d._children ? "+" : "-");
            
            // Transition nodes to their new position.
            const nodeUpdate = nodeEnter.merge(node);
            
            nodeUpdate.transition()
                .duration(300)
                .attr("transform", d => `translate(${d.y},${d.x})`);
                
            // Update the button symbol
            nodeUpdate.select(".expand-text")
                .text(d => d._children ? "+" : "-");
            
            // Transition exiting nodes to the parent's new position.
            const nodeExit = node.exit().transition()
                .duration(300)
                .attr("transform", d => `translate(${source.y},${source.x})`)
                .remove();
                
            // Links
            const link = g.selectAll("path.link")
                .data(links, d => d.target.id);
                
            const linkEnter = link.enter().insert("path", "g")
                .attr("class", "link")
                .attr("d", d => {
                    const o = {x: source.x0, y: source.y0};
                    return diagonal(o, o);
                });
                
            const linkUpdate = linkEnter.merge(link);
            
            linkUpdate.transition()
                .duration(300)
                .attr("d", d => diagonal(d.source, d.target));
                
            link.exit().transition()
                .duration(300)
                .attr("d", d => {
                    const o = {x: source.x, y: source.y};
                    return diagonal(o, o);
                })
                .remove();
                
            nodes.forEach(d => {
                d.x0 = d.x;
                d.y0 = d.y;
            });
        }
        
        function diagonal(s, d) {
            return `M ${s.y + nodeWidth} ${s.x}
                    C ${(s.y + nodeWidth + d.y) / 2} ${s.x},
                      ${(s.y + nodeWidth + d.y) / 2} ${d.x},
                      ${d.y} ${d.x}`;
        }
    }
}

// Hook into MkDocs Material instant loading, or use DOMContentLoaded as fallback
if (typeof document$ !== "undefined") {
    document$.subscribe(function() {
        initSchemaTree();
    });
} else {
    document.addEventListener("DOMContentLoaded", initSchemaTree);
}
</script>
