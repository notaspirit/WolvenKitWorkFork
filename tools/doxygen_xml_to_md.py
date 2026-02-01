"""
generate_docs.py

Scans a directory for Doxygen-generated XML files whose names start with "class",
parses every method (memberdef kind="function") out of them, and writes a single
flat GitBook-style Markdown file listing each method with its signature and any
<para> documentation found in briefdescription / detaileddescription.

Usage:
    python generate_docs.py <input_directory> [output_file.md]

    input_directory  – folder containing the doxygen XML files
    output_file.md   – (optional) path to write; defaults to "docs.md" in CWD
"""

import sys
import os
import xml.etree.ElementTree as ET
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def collect_text(element: ET.Element | None) -> str:
    """Recursively collect all text content from an XML element, stripping
    surrounding whitespace.  Returns an empty string if the element is None."""
    if element is None:
        return ""
    # itertext() yields every text fragment in document-order (including tails)
    return " ".join(element.itertext()).strip()


def extract_docs(memberdef: ET.Element) -> str:
    """Pull meaningful doc text from briefdescription and detaileddescription,
    skipping empty <para> tags and the auto-generated parameter / return
    sections that Doxygen adds (they are redundant with the signature)."""
    lines: list[str] = []

    for section_tag in ("briefdescription", "detaileddescription"):
        section = memberdef.find(section_tag)
        if section is None:
            continue
        for para in section.iter("para"):
            # Skip <para> that only contain a <parameterlist> or <simplesect kind="return">
            # with no actual written text.
            text_parts: list[str] = []
            # Direct text of the <para>
            if para.text and para.text.strip():
                text_parts.append(para.text.strip())
            for child in para:
                # Skip auto-generated sections
                if child.tag in ("parameterlist", "simplesect"):
                    continue
                text_parts.append(collect_text(child))
                # Include any tail text after this child
                if child.tail and child.tail.strip():
                    text_parts.append(child.tail.strip())

            combined = " ".join(text_parts).strip()
            if combined:
                lines.append(combined)

    return "\n".join(lines)


def build_signature(memberdef: ET.Element) -> str:
    """Build a clean, presentable signature using only the short method name.

    Format:
        MethodName(param1: Type1, param2: Type2 = default) → ReturnType
    """
    ret_type = collect_text(memberdef.find("type")).strip()
    method_name = (memberdef.findtext("name") or "").strip()

    # Parameters in "name: Type" style, which reads more naturally
    params: list[str] = []
    for param in memberdef.findall("param"):
        p_type = collect_text(param.find("type")).strip()
        p_name = (param.findtext("declname") or "").strip()
        p_default = (param.findtext("defval") or "").strip()

        if p_name:
            token = f"{p_name}: {p_type}"
        else:
            token = p_type

        if p_default:
            token += f" = {p_default}"
        params.append(token)

    params_str = ", ".join(params)
    signature = f"{method_name}({params_str})"

    # Append return type with an arrow, skip for constructors (no return type)
    if ret_type:
        signature += f" → {ret_type}"

    return signature


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def parse_class_xml(xml_path: Path) -> list[dict]:
    """Parse a single doxygen class XML file and return a list of method dicts,
    each with keys: signature (str), docs (str)."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    methods: list[dict] = []
    for memberdef in root.iter("memberdef"):
        if memberdef.get("kind") != "function":
            continue

        signature = build_signature(memberdef)
        docs = extract_docs(memberdef)
        methods.append({"signature": signature, "docs": docs})

    return methods


def generate_markdown(all_methods: list[dict], title: str = "API Reference") -> str:
    """Turn the flat list of method dicts into a GitBook Markdown string."""
    md_lines: list[str] = [f"# {title}", ""]

    for method in all_methods:
        # Doc comment block (/// style, rendered as a blockquote in GitBook)
        if method["docs"]:
            for doc_line in method["docs"].splitlines():
                md_lines.append(f"> {doc_line}")
            md_lines.append("")

        # Fenced code block with the signature
        md_lines.append("```csharp")
        md_lines.append(method["signature"])
        md_lines.append("```")
        md_lines.append("")  # blank line between entries

    return "\n".join(md_lines)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_dir = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("docs.md").resolve()

    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' is not a directory.")
        sys.exit(1)

    # Collect all XML files whose *stem* starts with "class"
    xml_files = sorted(
        f for f in input_dir.iterdir()
        if f.suffix.lower() == ".xml" and f.stem.startswith("class")
    )

    if not xml_files:
        print(f"No XML files starting with 'class' found in '{input_dir}'.")
        sys.exit(0)

    all_methods: list[dict] = []
    for xml_file in xml_files:
        print(f"  Parsing {xml_file.name} …")
        all_methods.extend(parse_class_xml(xml_file))

    if not all_methods:
        print("No methods found in any of the parsed files.")
        sys.exit(0)

    markdown = generate_markdown(all_methods)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"\nDone — {len(all_methods)} method(s) written to {output_path}")


if __name__ == "__main__":
    main()
