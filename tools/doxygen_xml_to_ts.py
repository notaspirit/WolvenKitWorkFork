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

def clean_text(elem):
    if elem is None:
        return ""
    return " ".join(elem.itertext()).strip()

def map_type(t: str) -> str:
    if not t:
        return "void"

    t = t.replace("params ", "").strip()
    t = t.replace("??", "?")

    is_array = "[]" in t
    is_nullable = t.endswith("?")

    base = t.replace("[]", "").replace("?", "")
    ts = CSHARP_TO_TS.get(base, base)

    if is_array:
        ts += "[]"
    if is_nullable:
        ts += " | undefined"

    return ts

def parse_class(xml_path: Path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    compound = root.find("compounddef")

    if compound is None or compound.attrib.get("kind") != "class":
        return None

    class_name = compound.findtext("compoundname").split("::")[-1]

    methods = defaultdict(list)

    for section in compound.findall("sectiondef"):
        if section.attrib.get("kind") != "public-func":
            continue

        for m in section.findall("memberdef"):
            name = m.findtext("name")

            if name == class_name:
                continue  # constructor

            ret = map_type(m.findtext("type"))

            # docs
            summary = clean_text(m.find("briefdescription")) or clean_text(m.find("detaileddescription"))
            param_docs = {}
            returns_doc = ""

            deta = m.find("detaileddescription")
            if deta is not None:
                for p in deta.findall(".//parameteritem"):
                    pname = clean_text(p.find(".//parametername"))
                    pdesc = clean_text(p.find(".//parameterdescription"))
                    if pname:
                        param_docs[pname] = pdesc

                r = deta.find(".//simplesect[@kind='return']")
                if r is not None:
                    returns_doc = clean_text(r)

            params = []
            jsdoc_params = []

            for p in m.findall("param"):
                raw_type = p.findtext("type") or "object"
                pname = p.findtext("declname") or "arg"
                ts_type = map_type(raw_type)

                if raw_type.startswith("params"):
                    params.append(f"...{pname}: any[]")
                elif ts_type.endswith("| undefined"):
                    params.append(f"{pname}?: {ts_type.replace(' | undefined', '')}")
                else:
                    params.append(f"{pname}: {ts_type}")

                if pname in param_docs and param_docs[pname]:
                    jsdoc_params.append(f" * @param {pname} {param_docs[pname]}")

            methods[name].append({
                "params": params,
                "return": ret,
                "summary": summary,
                "jsdoc_params": jsdoc_params,
                "returns_doc": returns_doc,
            })

    return class_name, methods

def main(xml_dir: Path, out_file: Path):
    classes = {}

    for xml in xml_dir.glob("class*.xml"):
        parsed = parse_class(xml)
        if not parsed:
            continue
        class_name, methods = parsed
        classes[class_name] = methods

    lines = []
    lines.append("declare namespace wkit {")

    for class_name, methods in sorted(classes.items()):
        lines.append(f"  interface {class_name} {{")

        for name, overloads in methods.items():
            for o in overloads:
                if o["summary"] or o["jsdoc_params"] or o["returns_doc"]:
                    lines.append("    /**")
                    if o["summary"]:
                        lines.append(f"     * {o['summary']}")
                    for p in o["jsdoc_params"]:
                        lines.append(f"     {p}")
                    if o["returns_doc"]:
                        lines.append(f"     * @returns {o['returns_doc']}")
                    lines.append("     */")

                sig = ", ".join(o["params"])
                lines.append(f"    {name}({sig}): {o['return']};")

        lines.append("  }")

    lines.append("}")

    out_file.write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python doxygen_xml_to_ts.py <xml_dir> <out.d.ts>")
        sys.exit(1)

    main(Path(sys.argv[1]), Path(sys.argv[2]))
