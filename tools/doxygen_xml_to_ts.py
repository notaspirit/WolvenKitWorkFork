import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

CSHARP_TO_TS = {
    "void": "void",
    "bool": "boolean",
    "byte": "number",
    "sbyte": "number",
    "short": "number",
    "ushort": "number",
    "int": "number",
    "uint": "number",
    "long": "number",
    "ulong": "number",
    "float": "number",
    "double": "number",
    "decimal": "number",
    "string": "string",
    "object": "any",
    "dynamic": "any",
    "ScriptObject": "any",
    "ScriptFunctionWrapper": "any",
}

GENERIC_COLLECTIONS = {
    "IList": "array",
    "IEnumerable": "array",
    "IReadOnlyList": "array",
    "List": "array",
}

def text(elem):
    if elem is None:
        return ""
    return "".join(elem.itertext()).strip()

def normalize_type(raw: str) -> str:
    raw = raw.replace("params ", "").strip()
    raw = raw.replace("??", "?")

    # Nullable
    nullable = raw.endswith("?")
    raw = raw.rstrip("?")

    # Generic collections
    if "<" in raw and ">" in raw:
        base, inner = raw.split("<", 1)
        inner = inner.rstrip(">")

        if base in GENERIC_COLLECTIONS:
            ts_inner = map_type(inner)
            return f"{ts_inner}[]{' | undefined' if nullable else ''}"

        if base == "Dictionary":
            parts = [p.strip() for p in inner.split(",")]
            val = map_type(parts[1]) if len(parts) == 2 else "any"
            return f"Record<string, {val}>"

    ts = CSHARP_TO_TS.get(raw, raw)
    return f"{ts}{' | undefined' if nullable else ''}"

def map_type(raw: str) -> str:
    if not raw:
        return "void"
    return normalize_type(raw)

def parse_xml_dir(xml_dir: Path):
    functions = defaultdict(list)

    for xml in xml_dir.glob("class*.xml"):
        tree = ET.parse(xml)
        root = tree.getroot()
        compound = root.find("compounddef")

        if compound is None:
            continue

        for section in compound.findall("sectiondef"):
            if section.attrib.get("kind") != "public-func":
                continue

            for m in section.findall("memberdef"):
                name = m.findtext("name")
                if name == compound.findtext("compoundname").split("::")[-1]:
                    continue  # constructor

                ret = map_type(text(m.find("type")))

                summary = text(m.find("briefdescription"))
                if not summary:
                    summary = text(m.find("detaileddescription"))

                param_docs = {}
                returns_doc = ""

                deta = m.find("detaileddescription")
                if deta is not None:
                    for p in deta.findall(".//parameteritem"):
                        pname = text(p.find(".//parametername"))
                        pdesc = text(p.find(".//parameterdescription"))
                        if pname and pdesc:
                            param_docs[pname] = pdesc

                    r = deta.find(".//simplesect[@kind='return']")
                    if r is not None:
                        returns_doc = text(r)

                params = []
                jsdoc = []

                for p in m.findall("param"):
                    pname = p.findtext("declname") or "arg"
                    ptype = map_type(text(p.find("type")))

                    if ptype.endswith("[]") and text(p.find("type")).startswith("params"):
                        params.append(f"...{pname}: {ptype}")
                    elif ptype.endswith("| undefined"):
                        params.append(f"{pname}?: {ptype.replace(' | undefined', '')}")
                    else:
                        params.append(f"{pname}: {ptype}")

                    if pname in param_docs:
                        jsdoc.append(f" * @param {pname} {param_docs[pname]}")

                functions[name].append({
                    "params": params,
                    "return": ret,
                    "summary": summary,
                    "param_docs": jsdoc,
                    "returns_doc": returns_doc,
                })

    return functions

def emit_ts(functions, out_file: Path):
    lines = []
    lines.append("declare namespace wkit {")

    for name, overloads in sorted(functions.items()):
        for o in overloads:
            has_docs = o["summary"] or o["param_docs"] or o["returns_doc"]

            if has_docs:
                lines.append("  /**")
                if o["summary"]:
                    lines.append(f"   * {o['summary']}")
                for p in o["param_docs"]:
                    lines.append(f"   {p}")
                if o["returns_doc"]:
                    lines.append(f"   * @returns {o['returns_doc']}")
                lines.append("   */")

            sig = ", ".join(o["params"])
            lines.append(f"  function {name}({sig}): {o['return']};")

    lines.append("}")
    out_file.write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python doxygen_xml_to_ts.py <xml_dir> <out.d.ts>")
        sys.exit(1)

    functions = parse_xml_dir(Path(sys.argv[1]))
    emit_ts(functions, Path(sys.argv[2]))
