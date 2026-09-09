#!/usr/bin/env python3
"""
build_schema_tree.py: generate docs/schema_data/schema.json for the interactive schema tree.

The "Schema Interactive Tree" page renders a D3 explorer from a single JSON file describing the
expanded DRMD element tree: every element, its type, cardinality, annotation, attributes,
enumerated values, and the Schematron rules that apply to it.

This script builds that file directly from the schema sources, so the page can never drift from
the schema it claims to document. Re-run it after any change to drmd.xsd or
drmd-business-rules.sch.

Usage
    python tools/build_schema_tree.py --schema-dir ../schema
    python tools/build_schema_tree.py --schema-dir /path/to/schema --max-depth 12

Requirements
    lxml only. It reads the XSD files as XML rather than through a schema processor, so no
    XSD-aware library and no network access are needed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lxml import etree

XS = "http://www.w3.org/2001/XMLSchema"
SCH_NS = "http://purl.oclc.org/dsdl/schematron"

# Namespace URI -> conventional prefix, used to render type names as people write them.
PREFIX_FOR = {
    "urn:drmd:schema": "drmd",
    "https://ptb.de/dcc": "dcc",
    "https://ptb.de/si": "si",
    "http://www.w3.org/2000/09/xmldsig#": "ds",
    "http://qudt.org/vocab/": "qudt",
    XS: "xs",
}


class SchemaSet:
    """The four schemas loaded together, indexed by qualified name."""

    def __init__(self, files):
        self.complex_types = {}
        self.simple_types = {}
        self.elements = {}
        self.attribute_groups = {}
        # head element -> the concrete elements that may appear in its place
        self.substitutions = {}
        for path in files:
            if not path.is_file():
                continue
            root = etree.parse(str(path)).getroot()
            target = root.get("targetNamespace", "")
            for node in root:
                name = node.get("name") if hasattr(node, "get") else None
                if not name:
                    continue
                key = (target, name)
                tag = etree.QName(node).localname if node.tag is not etree.Comment else ""
                if tag == "complexType":
                    self.complex_types[key] = node
                elif tag == "simpleType":
                    self.simple_types[key] = node
                elif tag == "element":
                    self.elements[key] = node
                elif tag == "attributeGroup":
                    self.attribute_groups[key] = node
                if tag == "element" and node.get("substitutionGroup"):
                    head = self.split_qname(node, node.get("substitutionGroup"))
                    if head:
                        self.substitutions.setdefault(head, []).append((target, name, node))

    @staticmethod
    def split_qname(node, qname):
        """Resolve a prefixed name such as 'dcc:textType' using the node's own namespace map."""
        if not qname:
            return None
        if ":" in qname:
            prefix, local = qname.split(":", 1)
            return node.nsmap.get(prefix), local
        return node.nsmap.get(None), qname

    def complex_type(self, node, qname):
        key = self.split_qname(node, qname)
        return self.complex_types.get(key) if key else None

    def simple_type(self, node, qname):
        key = self.split_qname(node, qname)
        return self.simple_types.get(key) if key else None

    def element(self, node, qname):
        key = self.split_qname(node, qname)
        return self.elements.get(key) if key else None


def documentation(node) -> str:
    """Collapse every xs:documentation directly under a node's annotation into one line."""
    if node is None:
        return ""
    texts = []
    for annotation in node.findall(f"{{{XS}}}annotation"):
        for doc in annotation.findall(f"{{{XS}}}documentation"):
            texts.append(" ".join("".join(doc.itertext()).split()))
    return " ".join(t for t in texts if t)


def pretty_qname(node, qname: str) -> str:
    """Render a type name with its conventional prefix rather than whatever the file used."""
    if not qname:
        return ""
    resolved = SchemaSet.split_qname(node, qname)
    if not resolved or not resolved[0]:
        return qname
    uri, local = resolved
    return f"{PREFIX_FOR.get(uri, uri)}:{local}"


def cardinality(node) -> str:
    lo = node.get("minOccurs", "1")
    hi = node.get("maxOccurs", "1")
    return f"[{lo}..{'*' if hi == 'unbounded' else hi}]"


def simple_type_facets(schemas: SchemaSet, node, type_qname: str):
    """Return (base type, enumerated values) for a simple type, following one level of naming."""
    st = schemas.simple_type(node, type_qname) if type_qname else None
    if st is None:
        return "", None
    restriction = st.find(f"{{{XS}}}restriction")
    if restriction is None:
        return "", None
    base = pretty_qname(restriction, restriction.get("base", ""))
    values = [e.get("value") for e in restriction.findall(f"{{{XS}}}enumeration")]
    return base, (values or None)


def collect_attributes(schemas: SchemaSet, type_node):
    """Attributes declared on a complex type, following one level of extension."""
    if type_node is None:
        return []
    out = []
    scopes = [type_node]
    content = type_node.find(f"{{{XS}}}complexContent")
    if content is not None:
        for kind in ("extension", "restriction"):
            derived = content.find(f"{{{XS}}}{kind}")
            if derived is not None:
                scopes.append(derived)
                base = schemas.complex_type(derived, derived.get("base", ""))
                if base is not None:
                    out.extend(collect_attributes(schemas, base))
    for scope in scopes:
        for attr in scope.findall(f"{{{XS}}}attribute"):
            name = attr.get("name")
            if not name:
                continue
            out.append(
                {
                    "name": name,
                    "type": pretty_qname(attr, attr.get("type", "")),
                    "use": attr.get("use", "optional"),
                    "description": documentation(attr),
                    "rules": [],
                }
            )
    seen, unique = set(), []
    for attr in out:
        if attr["name"] not in seen:
            seen.add(attr["name"])
            unique.append(attr)
    return unique


def child_elements(schemas: SchemaSet, type_node, _depth=0):
    """Every element particle inside a complex type, in document order, following extensions.

    Returns (element, compositor) pairs. The compositor is the model group the element sits
    in ("sequence", "choice" or "all"), which the tree needs in order to say whether siblings
    appear together or as alternatives. Without it a choice of eight payload types renders as
    eight required siblings, which is the opposite of what the schema means.
    """
    if type_node is None or _depth > 6:
        return []
    found = []
    content = type_node.find(f"{{{XS}}}complexContent")
    if content is not None:
        for kind in ("extension", "restriction"):
            derived = content.find(f"{{{XS}}}{kind}")
            if derived is not None:
                base = schemas.complex_type(derived, derived.get("base", ""))
                found.extend(child_elements(schemas, base, _depth + 1))
                found.extend(_particles(schemas, derived, "sequence"))
        return found
    return _particles(schemas, type_node, "sequence")


def _particles(schemas: SchemaSet, node, compositor):
    out = []
    for child in node:
        if child.tag is etree.Comment:
            continue
        tag = etree.QName(child).localname
        if tag == "element":
            out.append((child, compositor))
        elif tag in ("sequence", "choice", "all"):
            out.extend(_particles(schemas, child, tag))
        elif tag == "group":
            pass  # no named model groups are used in this schema set
    return out


def _steps(expression: str):
    """Turn an XPath-ish expression into a list of element steps.

    "//" becomes the marker "**", meaning "any number of steps here". Predicates, attribute
    steps and function calls are dropped: only the element path matters for locating a rule.
    """
    expression = " ".join((expression or "").split())
    # Drop predicates, which may themselves contain paths we must not mistake for steps.
    out, depth = [], 0
    for char in expression:
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        elif depth == 0:
            out.append(char)
    expression = "".join(out)

    steps = []
    for raw in expression.replace("//", "/**/").split("/"):
        raw = raw.strip()
        if not raw:
            continue
        if raw == "**":
            steps.append("**")
            continue
        if raw.startswith("@") or "(" in raw or "=" in raw:
            continue
        steps.append(raw.split(":")[-1])
    return steps


def _matches(node_steps, pattern):
    """True when node_steps ends with pattern, where "**" absorbs any number of steps."""
    if not pattern:
        return False
    # Walk both from the end.
    n, p = len(node_steps) - 1, len(pattern) - 1
    while p >= 0:
        step = pattern[p]
        if step == "**":
            # Absorb greedily: the remaining pattern must match somewhere further left.
            remaining = pattern[:p]
            if not remaining:
                return True
            for cut in range(n, -1, -1):
                if _matches(node_steps[:cut + 1], remaining):
                    return True
            return False
        if n < 0 or node_steps[n] != step:
            return False
        n -= 1
        p -= 1
    return True


def load_rules(sch_path: Path):
    """Read the Schematron assertions and the element paths each one speaks about.

    A rule is attached to two kinds of node: the node its rule context selects, and the node its
    test names. Matching is done on the element PATH, not on the bare element name. Otherwise a
    rule about materials/material/name would also be shown on document/name, which is a different
    element governed by nothing.
    """
    if not sch_path.is_file():
        return []
    root = etree.parse(str(sch_path)).getroot()
    entries = []
    for rule in root.iter(f"{{{SCH_NS}}}rule"):
        context_steps = _steps(rule.get("context", ""))
        for assertion in rule.findall(f"{{{SCH_NS}}}assert"):
            test = assertion.get("test") or ""
            patterns = [context_steps] if context_steps else []
            for branch in test.replace(" or ", "|").replace(" and ", "|").split("|"):
                branch_steps = _steps(branch)
                if branch_steps:
                    patterns.append(context_steps + branch_steps)
            entries.append(
                {
                    "entry": {
                        "id": assertion.get("id", ""),
                        "role": assertion.get("role", "error"),
                        "test": " ".join(test.split()),
                        "description": " ".join("".join(assertion.itertext()).split()),
                    },
                    "patterns": patterns,
                }
            )
    return entries


def rules_for(rules, node_path: str):
    node_steps = [step for step in node_path.split("/") if step]
    out = []
    for rule in rules:
        if any(_matches(node_steps, pattern) for pattern in rule["patterns"]):
            if rule["entry"] not in out:
                out.append(rule["entry"])
    return out


def build(schemas: SchemaSet, rules, element, path, max_depth, seen_types, depth=0,
          compositor="sequence"):
    name = element.get("name") or (element.get("ref") or "").split(":")[-1]
    referenced = None
    if element.get("ref"):
        referenced = schemas.element(element, element.get("ref"))
        type_qname = referenced.get("type", "") if referenced is not None else ""
        doc_node = referenced if referenced is not None else element
    else:
        type_qname = element.get("type", "")
        doc_node = element

    inline_type = element.find(f"{{{XS}}}complexType")
    type_node = inline_type if inline_type is not None else schemas.complex_type(doc_node, type_qname)

    base, enumerations = simple_type_facets(schemas, doc_node, type_qname)
    inline_simple = element.find(f"{{{XS}}}simpleType")
    if inline_simple is not None:
        restriction = inline_simple.find(f"{{{XS}}}restriction")
        if restriction is not None:
            base = pretty_qname(restriction, restriction.get("base", ""))
            enumerations = [e.get("value") for e in restriction.findall(f"{{{XS}}}enumeration")] or None

    node_path = f"{path}/{name}" if path else name
    description = documentation(element) or documentation(type_node)

    # An abstract element never appears in an instance: an element from its substitution group
    # takes its place. si:quantityType is the case that matters here: nobody writes
    # <si:quantityType>, they write <si:quantityTypeQUDT>. Listing the substitutes is the only
    # way a reader of the tree can discover them.
    declared = referenced if element.get("ref") and referenced is not None else element
    is_abstract = declared.get("abstract") == "true"
    substitutes = []
    if is_abstract and declared.get("name"):
        head_key = (declared.getroottree().getroot().get("targetNamespace", ""), declared.get("name"))
        for ns, sub_name, sub_node in schemas.substitutions.get(head_key, []):
            substitutes.append(
                {
                    "name": sub_name,
                    "type": pretty_qname(sub_node, sub_node.get("type", "")),
                    "description": documentation(sub_node),
                }
            )

    node = {
        "name": name,
        "type": pretty_qname(doc_node, type_qname) if type_qname else "complexType",
        "base": base,
        "enumerations": enumerations,
        "cardinality": cardinality(element),
        "compositor": compositor,
        "abstract": is_abstract,
        "substitutions": substitutes,
        "description": description,
        "path": node_path,
        "attributes": collect_attributes(schemas, type_node),
        "rules": rules_for(rules, node_path),
        "children": [],
    }

    # Guard against unbounded recursion through recursive types such as ds:Object.
    type_key = pretty_qname(doc_node, type_qname) if type_qname else id(type_node)
    if depth >= max_depth or (type_key and type_key in seen_types):
        return node

    for child, child_compositor in child_elements(schemas, type_node):
        node["children"].append(
            build(schemas, rules, child, node_path, max_depth,
                  seen_types | ({type_key} if type_key else set()), depth + 1,
                  child_compositor)
        )
    return node


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--schema-dir", default="../schema",
                        help="path to the schema repository (default: ../schema)")
    parser.add_argument("--out", default="docs/schema_data/schema.json",
                        help="output file (default: docs/schema_data/schema.json)")
    parser.add_argument("--max-depth", type=int, default=9,
                        help="how deep to expand the tree (default: 9)")
    args = parser.parse_args(argv)

    schema_dir = Path(args.schema_dir).resolve()
    xsd = schema_dir / "drmd.xsd"
    if not xsd.is_file():
        print(f"build_schema_tree.py: {xsd} not found. Pass --schema-dir.", file=sys.stderr)
        return 2

    supporting = schema_dir / "supporting"
    schemas = SchemaSet([
        xsd,
        supporting / "dcc.xsd",
        supporting / "SI_Format.xsd",
        supporting / "xmldsig-core-schema.xsd",
        supporting / "quantitykind.xsd",
    ])
    rules = load_rules(schema_dir / "drmd-business-rules.sch")

    root_element = schemas.elements.get(("urn:drmd:schema", "digitalReferenceMaterialDocument"))
    if root_element is None:
        print("build_schema_tree.py: root element not found in drmd.xsd", file=sys.stderr)
        return 2

    tree = build(schemas, rules, root_element, "", args.max_depth, frozenset())

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(tree, indent=2), encoding="utf-8")

    def count(node):
        return 1 + sum(count(c) for c in node["children"])

    def rule_count(node):
        return len(node["rules"]) + sum(rule_count(c) for c in node["children"])

    print(f"Wrote {out}: {count(tree)} nodes, {rule_count(tree)} rule annotations, "
          f"{out.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
