"""Build benchmark/corpus/manifest.json from all sidecar metadata files."""
from __future__ import annotations

import argparse
import collections
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
SCHEMAS = ROOT / "schemas"

VERSION = "0.1.0"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--validate", action="store_true", help="validate against schemas before writing")
    args = p.parse_args()

    docs = []
    by_cat: dict[str, int] = collections.Counter()
    by_fmt: dict[str, int] = collections.Counter()
    license_summary: dict[str, int] = collections.Counter()

    for meta_path in sorted(CORPUS.rglob("*.metadata.json")):
        meta = json.loads(meta_path.read_text())
        pdf_path = meta_path.with_name(meta_path.stem.replace(".metadata", "") + ".pdf")
        if not pdf_path.exists():
            print(f"[WARN] metadata without pdf: {meta_path.relative_to(ROOT)}", file=sys.stderr)
            continue

        docs.append({
            "id": meta["id"],
            "category": meta["category"],
            "relative_path": str(pdf_path.relative_to(ROOT)),
            "license": meta["license"],
            "format": meta["format"],
            "sha256": meta.get("sha256", ""),
            "size_bytes": pdf_path.stat().st_size,
        })
        by_cat[meta["category"]] += 1
        by_fmt[meta["format"]] += 1
        license_summary[meta["license"]] += 1

    manifest = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_documents": len(docs),
        "by_category": dict(by_cat),
        "by_format": dict(by_fmt),
        "license_summary": dict(license_summary),
        "documents": docs,
    }

    if args.validate:
        try:
            import jsonschema
            schema = json.loads((SCHEMAS / "manifest.schema.json").read_text())
            jsonschema.validate(manifest, schema)
            print("  manifest validates against schema.")
        except Exception as exc:
            print(f"[FAIL] manifest schema validation: {exc}", file=sys.stderr)
            return 2

    out_path = CORPUS / "manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"  Wrote {out_path.relative_to(ROOT)} — {len(docs)} docs.")
    print(f"  by_category: {dict(by_cat)}")
    print(f"  by_format:   {dict(by_fmt)}")
    print(f"  licenses:    {dict(license_summary)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
