"""Generate Appendix A — per-document raw data dump for the parser paper.

Combines:
  - corpus metadata (id, category, publisher, page_count, sha256)
  - layout-complexity score
  - per-doc pairwise CER for every parser pair
  - per-parser per-doc extraction length

Output:
  results/appendix_a_per_doc.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus" / "real"
RESULTS = ROOT / "results"


def main() -> int:
    # Load raw step1b records
    raw = json.loads((RESULTS / "step1b_parsers_real_raw.jsonl").read_text())
    per_parser = raw.get("per_parser", [])
    pairs = raw.get("pairs", [])

    # Load layout complexity
    cx_rows = [json.loads(line) for line in
               (RESULTS / "layout_complexity.jsonl").read_text().splitlines() if line.strip()]
    cx_by_doc = {r["doc_id"]: r for r in cx_rows}

    # Doc metadata
    docs: list[dict] = []
    for pdf in sorted(CORPUS.glob("*.pdf")):
        meta_path = pdf.with_suffix(".metadata.json")
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        docs.append({
            "id": pdf.stem,
            "category": meta.get("category", "?"),
            "publisher": meta.get("source_organization", "?"),
            "page_count": meta.get("page_count", 0),
            "sha256": meta.get("sha256", "?")[:16] + "…",
            "source_url": meta.get("source_url", "?"),
        })

    md = [
        "# Appendix A — Per-document data",
        "",
        "All 30 corpus documents with: license metadata, layout-complexity score,",
        "per-parser extraction length, and per-pair Character Error Rate.",
        "License for every doc: public-domain (US federal government work, 17 USC §105).",
        "",
        "## A.1 Document metadata",
        "",
        "| ID | Category | Publisher | Pages | sha256 (truncated) |",
        "|---|---|---|---|---|",
    ]
    for d in docs:
        md.append(f"| {d['id']} | {d['category']} | {d['publisher']} | {d['page_count']} | `{d['sha256']}` |")
    md.append("")

    md.append("## A.2 Layout-complexity scores")
    md.append("")
    md.append("| ID | Pages | Column count (mean per page) | Form-page fraction | n_blocks (mean) | Complexity |")
    md.append("|---|---|---|---|---|---|")
    for d in docs:
        cx = cx_by_doc.get(d["id"], {})
        md.append(f"| {d['id']} | {d['page_count']} | "
                  f"{cx.get('column_count_mean', 0):.2f} | "
                  f"{cx.get('form_pages_frac', 0):.2f} | "
                  f"{cx.get('n_blocks_mean', 0):.1f} | "
                  f"{cx.get('complexity', 0):.3f} |")
    md.append("")

    md.append("## A.3 Per-parser extraction length and latency")
    md.append("")
    parsers = sorted({r["parser"] for r in per_parser})
    md.append("| ID | Pages | " + " | ".join(f"{p} (chars)" for p in parsers) + " |")
    md.append("|---|---|" + "---|" * len(parsers))
    for d in docs:
        cells = []
        for p in parsers:
            recs = [r for r in per_parser if r["doc_id"] == d["id"] and r["parser"] == p]
            cells.append(f"{recs[0]['extracted_text_chars']:,}" if recs else "—")
        md.append(f"| {d['id']} | {d['page_count']} | " + " | ".join(cells) + " |")
    md.append("")

    md.append("## A.4 Per-doc pairwise CER (all parser pairs)")
    md.append("")
    pair_keys = sorted({(p["parser_a"], p["parser_b"]) for p in pairs})
    md.append("| ID | " + " | ".join(f"{a}↔{b}" for a, b in pair_keys) + " |")
    md.append("|---|" + "---|" * len(pair_keys))
    for d in docs:
        cells = []
        for a, b in pair_keys:
            recs = [p for p in pairs if p["doc_id"] == d["id"]
                    and p["parser_a"] == a and p["parser_b"] == b]
            if recs and recs[0]["cer_ab"] == recs[0]["cer_ab"]:
                cells.append(f"{recs[0]['cer_ab']:.3f}")
            else:
                cells.append("—")
        md.append(f"| {d['id']} | " + " | ".join(cells) + " |")
    md.append("")

    md.append("## A.5 Source URLs (for reproducibility)")
    md.append("")
    md.append("| ID | Source URL |")
    md.append("|---|---|")
    for d in docs:
        md.append(f"| {d['id']} | {d['source_url']} |")
    md.append("")

    out = RESULTS / "appendix_a_per_doc.md"
    out.write_text("\n".join(md))
    print(f"Wrote {out.relative_to(ROOT)} ({len(docs)} docs, {len(pair_keys)} pair columns)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
