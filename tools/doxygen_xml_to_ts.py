import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

CSharpToTS = {
    "string": "string",
    "int": "number",
    "long": "number",
    "float": "number",
    "double": "number",
    "bool": "boolean",
    "object": "any",
    "object?": "any",
    "void": "void",
}

def map_type(t: str) -> str:
    if not t:
        return "void"

    t = t.replace("params ", "").strip()
    t = t.replace("??", "?")

    is_array = "[]" in t
    is_nullable = t.endswith("?")

    base = t.replace("[]", "").replace("?", "")
    ts = CSharpToTS.get(base, base)

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

    fq = compound.findtext("compoundname")
    parts = fq.split("::")

    namespace = ".".join(parts[:-1])
    class_name = parts[-1]

    methods = defaultdict(list)

    for section in compound.findall("sectiondef"):
        if section.attrib.get("kind") != "public-func":
            continue

        for m in section.findall("memberdef"):
            name = m.findtext("name")

            # skip constructors
            if name == class_name:
                continue

            ret = map_type(m.findtext("type"))
            params = []

            for p in m.findall("param"):
                raw_type = p.findtext("type") or "object"
                name_p = p.findtext("declname") or "arg"

                ts_type = map_type(raw_type)

                if raw_type.startswith("params"):
                    params.append(f"...{name_p}: any[]")
                elif ts_type.endswith("| undefined"):
                    params.append(f"{name_p}?: {ts_type.replace(' | undefined', '')}")
                else:
                    params.append(f"{name_p}: {ts_type}")

            methods[name].append((params, ret))

    return namespace, class_name, methods

def main(xml_dir: Path, out_file: Path):
    namespaces = defaultdict(lambda: defaultdict(dict))

    for xml in xml_dir.glob("class*.xml"):
        parsed = parse_class(xml)
        if not parsed:
            continue

        namespace, class_name, methods = parsed
        namespaces[namespace][class_name] = methods

    lines = []

    for namespace, classes in sorted(namespaces.items()):
        lines.append(f"declare namespace {namespace} {{")

        for class_name, methods in classes.items():
            lines.append(f"  interface {class_name} {{")

            for name, overloads in methods.items():
                for params, ret in overloads:
                    sig = ", ".join(params)
                    lines.append(f"    {name}({sig}): {ret};")

            lines.append("  }")

        lines.append("}")
        lines.append("")

    out_file.write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python doxygen_xml_to_ts.py <xml_dir> <out.d.ts>")
        sys.exit(1)

    main(Path(sys.argv[1]), Path(sys.argv[2]))
