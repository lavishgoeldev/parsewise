"""Download the small set of real public-domain PDFs for Step 1.B.

Idempotent: skips already-downloaded files. Records sha256, page count,
and a per-doc metadata sidecar consistent with the schema.

Usage:
    python -m scripts.download_real_pdfs
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "corpus" / "real"

try:
    from .real_pdfs import REAL_PDFS, RealPDF
except ImportError:
    sys.path.insert(0, str(ROOT))
    from scripts.real_pdfs import REAL_PDFS, RealPDF  # type: ignore


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).date().isoformat()
    n_done = n_skip = n_fail = 0
    for d in REAL_PDFS:
        out_pdf = OUT_DIR / f"{d.id}.pdf"
        out_meta = OUT_DIR / f"{d.id}.metadata.json"
        if out_pdf.exists() and out_meta.exists():
            print(f"[SKIP] {d.id}: already present")
            n_skip += 1
            continue
        try:
            print(f"  Downloading {d.id} ({d.title}) …")
            with httpx.Client(follow_redirects=True, timeout=90.0,
                              headers={"User-Agent": "PrivateVault-Benchmark/0.1"}) as client:
                r = client.get(d.url)
                r.raise_for_status()
                out_pdf.write_bytes(r.content)
            sha = hashlib.sha256(r.content).hexdigest()
            page_count = _count_pages(out_pdf)
            meta = {
                "id": d.id,
                "category": d.category,
                "doc_type": d.id.rstrip("0123456789").lower() or "doc",
                "source_url": d.url,
                "source_organization": d.publisher,
                "license": "public-domain",
                "license_verified_at": today,
                "format": "digital_pdf",
                "page_count": page_count,
                "language": "en",
                "added_at": today,
                "notes": f"US federal govt work, public domain by 17 USC §105. {d.title}",
                "sha256": sha,
            }
            out_meta.write_text(json.dumps(meta, indent=2))
            print(f"  saved {len(r.content):,} bytes — {page_count} pages — sha256 {sha[:12]}…")
            n_done += 1
        except Exception as exc:
            print(f"  ! failed {d.id}: {exc}", file=sys.stderr)
            n_fail += 1
    print(f"\nSummary: {n_done} downloaded, {n_skip} skipped, {n_fail} failed.")
    return 0 if n_fail == 0 else 1


def _count_pages(pdf: Path) -> int:
    try:
        import fitz
        with fitz.open(pdf) as doc:
            return doc.page_count
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
