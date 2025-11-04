
This folder stores all datasets and knowledge sources required by the project.

## 1. MedQuAD Dataset (Required)

Please **manually download** the [MedQuAD](https://github.com/abachaa/MedQuAD) dataset and place it under:

```
data/MedQuAD/
```

Make sure the folder name is exactly **`MedQuAD`** (case-sensitive).

Example structure:
```
data/
├─ MedQuAD/
│   ├─ 1_CancerGov_QA
│   ├─ 2_GARD_QA
│   └─ ...
└─ emergency_terms.json
```

---

## 2. Convert XML → JSON

After placing MedQuAD, run the conversion script to build the unified QA dataset:

```bash
python scripts/convert_medquad_xml_to_json.py
```

This will:
- Recursively parse all `.xml` files under `data/MedQuAD/`
- Extract all Question–Answer pairs
- Save the merged result as:

```
data/medquad_subset.json
```

> The script will automatically create or overwrite it when finished.

---

## 3. Notes

- The resulting `medquad_subset.json` will be automatically used by the retrieval (RAG) component.
- The conversion script skips invalid or empty QA pairs automatically.
- If you modify or update MedQuAD data, rerun the script to refresh the JSON.
