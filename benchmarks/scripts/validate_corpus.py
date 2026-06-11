"""Smoke-test the corpus.

For every document on disk:
  1. Sidecar metadata exists and validates against document_metadata.schema.json.
  2. PDF opens with PyMuPDF and reports the page count claimed in metadata.
  3. SHA-256 in metadata matches the actual file.
  4. License is in the allowed set.

Exits non-zero if any check fails.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
SCHEMAS = ROOT / "schemas"

ALLOWED_LICENSES = {
    "public-domain", "us-government-work", "cc0",
    "cc-by-4.0", "cc-by-sa-4.0", "open-government-license",
    "cc-by-nc-4.0", "cc-by-nc-sa-4.0", "other-open",
}


def main() -> int:
    errors: list[str] = []
    try:
        import jsonschema
        schema = json.loads((SCHEMAS / "document_metadata.schema.json").read_text())
    except Exception as exc:
        print(f"[FAIL] cannot load schema: {exc}", file=sys.stderr)
        return 2

    try:
        import fitz
    except ImportError:
        print("[FAIL] PyMuPDF not installed; install with: pip install -r benchmark/requirements.txt",
              file=sys.stderr)
        return 2

    pdfs = sorted(p for p in CORPUS.rglob("*.pdf") if p.name != "manifest.json")
    if not pdfs:
        print("[INFO] no PDFs yet; nothing to validate. Run download_corpus.py first.")
        return 0

    for pdf in pdfs:
        meta_path = pdf.with_suffix("").with_suffix(".metadata.json")
        if not meta_path.exists():
            errors.append(f"{pdf.name}: missing sidecar {meta_path.name}")
            continue
        meta = json.loads(meta_path.read_text())

        # 1. schema
        try:
            jsonschema.validate(meta, schema)
        except Exception as exc:
            errors.append(f"{pdf.name}: schema error — {exc.message if hasattr(exc, 'message') else exc}")
            continue

        # 2. PDF opens, page count matches
        try:
            with fitz.open(pdf) as doc:
                if doc.page_count != meta["page_count"]:
                    errors.append(f"{pdf.name}: page_count mismatch "
                                  f"(metadata={meta['page_count']}, actual={doc.page_count})")
        except Exception as exc:
            errors.append(f"{pdf.name}: cannot open PDF — {exc}")

        # 3. sha matches
        if "sha256" in meta and meta["sha256"]:
            actual = hashlib.sha256(pdf.read_bytes()).hexdigest()
            if actual != meta["sha256"]:
                errors.append(f"{pdf.name}: sha256 mismatch")

        # 4. license allowed
        if meta["license"] not in ALLOWED_LICENSES:
            errors.append(f"{pdf.name}: license '{meta['license']}' not in allowed set")

    print(f"Validated {len(pdfs)} docs.")
    if errors:
        print(f"\n{len(errors)} validation errors:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("  All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
