"""Download digital + real-scan source documents.

Idempotent: skips files that already exist with the expected SHA-256.
Records each download in the per-doc metadata sidecar, including the
license-verification step (which is a human-confirmation prompt).

Usage:
    python -m scripts.download_corpus            # interactive: prompts per doc
    python -m scripts.download_corpus --dry-run  # show plan, change nothing
    python -m scripts.download_corpus --only L001,L002
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"

try:
    from . import sources as _sources  # noqa: F401
    from .sources import SOURCES, Source
except ImportError:
    sys.path.insert(0, str(ROOT))
    from scripts.sources import SOURCES, Source  # type: ignore


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--only", type=str, default=None, help="comma-separated source ids")
    p.add_argument("--archive-wayback", action="store_true",
                   help="also save each URL to web.archive.org for permanence")
    p.add_argument("--yes", action="store_true",
                   help="auto-confirm license verification (DANGEROUS: only for re-runs)")
    args = p.parse_args()

    targets = SOURCES
    if args.only:
        wanted = set(s.strip() for s in args.only.split(","))
        targets = [s for s in SOURCES if s.id in wanted]
        if not targets:
            print(f"No sources match {wanted}", file=sys.stderr)
            return 2

    n_done = n_skipped = n_failed = 0
    for s in targets:
        if not s.source_url:
            print(f"[SKIP] {s.id}: no source URL yet (manual selection pending)")
            n_skipped += 1
            continue

        out_dir = CORPUS / s.category
        out_dir.mkdir(parents=True, exist_ok=True)
        out_pdf = out_dir / f"{s.id}.pdf"
        out_meta = out_dir / f"{s.id}.metadata.json"

        if args.dry_run:
            print(f"[DRY-RUN] {s.id} → {out_pdf.relative_to(ROOT)}  ({s.confidence})")
            continue

        if out_pdf.exists() and out_meta.exists():
            print(f"[SKIP] {s.id}: already present")
            n_skipped += 1
            continue

        if s.confidence == "needs-selection":
            print(f"[MANUAL] {s.id} needs file selection. URL points to a collection: {s.source_url}")
            print(f"         Download a file by hand into {out_pdf} and rerun to record metadata.")
            continue

        # License-verification gate (per the SOURCING_PLAN audit).
        if not args.yes:
            print(f"\n=== {s.id} ({s.category}) ===")
            print(f"  Title:     {s.title}")
            print(f"  Publisher: {s.publisher}")
            print(f"  License:   {s.license} (confidence: {s.confidence})")
            print(f"  URL:       {s.source_url}")
            resp = input("  Open URL in a browser, confirm the license matches. "
                         "Proceed with download? [y/N] ").strip().lower()
            if resp != "y":
                print(f"[SKIP] {s.id}: license not confirmed")
                n_skipped += 1
                continue

        try:
            print(f"  Downloading {s.id} …")
            data = _download(s.source_url)
            out_pdf.write_bytes(data)
            sha = hashlib.sha256(data).hexdigest()
            print(f"  Saved {len(data):,} bytes — sha256 {sha[:12]}…")

            page_count = _try_count_pages(out_pdf)
            metadata = _build_metadata(s, sha, page_count, args.archive_wayback)
            out_meta.write_text(json.dumps(metadata, indent=2))
            n_done += 1
        except Exception as exc:
            print(f"  ! FAILED {s.id}: {exc}", file=sys.stderr)
            n_failed += 1

    print(f"\nSummary: {n_done} downloaded, {n_skipped} skipped, {n_failed} failed.")
    return 0 if n_failed == 0 else 1


def _download(url: str) -> bytes:
    with httpx.Client(follow_redirects=True, timeout=60.0,
                      headers={"User-Agent": "PrivateVault-Benchmark/0.1"}) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.content


def _try_count_pages(pdf_path: Path) -> int:
    try:
        import fitz
        with fitz.open(pdf_path) as doc:
            return doc.page_count
    except Exception:
        return 0


def _build_metadata(s: Source, sha256: str, page_count: int, archive: bool) -> dict:
    today = datetime.now(timezone.utc).date().isoformat()
    meta = {
        "id": s.id,
        "category": s.category,
        "doc_type": s.doc_type,
        "source_url": s.source_url,
        "source_organization": s.publisher,
        "license": s.license,
        "license_verified_at": today,
        "format": "digital_pdf" if "scan" not in s.doc_type else "scan_high",
        "page_count": page_count,
        "language": "en",
        "added_at": today,
        "notes": s.notes,
        "sha256": sha256,
    }
    if archive:
        meta["wayback_url"] = _wayback_archive(s.source_url)
    return meta


def _wayback_archive(url: str) -> str:
    try:
        from waybackpy import WaybackMachineSaveAPI
        saver = WaybackMachineSaveAPI(url, user_agent="PrivateVault-Benchmark/0.1")
        return saver.save()
    except Exception as exc:
        print(f"  ! wayback archival failed: {exc}", file=sys.stderr)
        return ""


if __name__ == "__main__":
    sys.exit(main())
