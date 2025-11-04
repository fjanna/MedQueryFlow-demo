import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_xml_file(xml_path: Path):
    """Parse a MedQuAD XML file and extract question-answer pairs."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        items = []
        for qa in root.findall(".//QAPair"):
            q = qa.findtext("Question") or ""
            a = qa.findtext("Answer") or ""
            qid = qa.findtext("QID") or xml_path.stem
            if q.strip() and a.strip():
                items.append({
                    "id": qid.strip(),
                    "question": q.strip(),
                    "answer": a.strip()
                })
        return items
    except Exception as e:
        print(f"[WARN] Failed to parse {xml_path}: {e}")
        return []

def convert_all_medquad(root_dir="data/MedQuAD", output_file="data/medquad_subset.json"):
    """Convert all XML files under MedQuAD directory into one JSON file."""
    root_path = Path(root_dir)
    if not root_path.exists():
        raise FileNotFoundError(f"MedQuAD directory not found: {root_dir}")

    all_items = []
    xml_files = list(root_path.rglob("*.xml"))
    print(f"Found {len(xml_files)} XML files under {root_dir}")

    for xml_file in xml_files:
        items = parse_xml_file(xml_file)
        all_items.extend(items)

    print(f"Parsed {len(all_items)} QA pairs total.")
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved merged JSON → {output_path.resolve()}")
    return output_path

if __name__ == "__main__":
    convert_all_medquad()
