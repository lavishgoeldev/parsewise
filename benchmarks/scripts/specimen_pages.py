"""Generate Appendix B specimen pages — visible side-by-side extracts.

We pick two contrast cases:
  - M005 (CDC MMWR multi-column publication), page 1 — high A↔C divergence.
  - L001 (SCOTUS opinion, single-column prose), page 1 — all parsers agree.

For each specimen, we re-extract page-1 text via each of the 5 parsers and
write a Markdown file that shows the first ~50 lines of each parser's output.
That lets a reader of the paper see, with their own eyes, that pdfplumber-default
threads the same words in a noticeably different order on the multi-column page
and that all parsers agree on the prose page.

Output:
  results/appendix_b_specimen_pages.md
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus" / "real"
RESULTS = ROOT / "results"

try:
    from .parsers import REGISTRY
except ImportError:
    sys.path.insert(0, str(ROOT))
    from scripts.parsers import REGISTRY  # type: ignore


PARSERS_ORDER = ["pymupdf", "pypdf", "pdfplumber_tuned", "pdfminer", "pdfplumber"]


SPECIMENS = [
    ("M005", 1, "CDC MMWR Vol 73 No 41 — multi-column publication (page 1)"),
    ("L001", 1, "SCOTUS Slip Opinion 23-477 — single-column prose (page 1)"),
]

PREVIEW_LINES = 30
PREVIEW_CHARS = 1600


def extract_page(parser_name: str, pdf_path: Path, page_idx: int) -> str:
    """Extract a single page's text. We extract the whole doc and slice on '\f'
    page separators, because not every parser exposes per-page extraction
    uniformly. Page numbering is 1-based; page_idx=1 returns the first page."""
    full = REGISTRY[parser_name].extract(pdf_path)
    pages = full.split("\f")
    if page_idx - 1 >= len(pages):
        return f"<no page {page_idx}>"
    return pages[page_idx - 1]


def preview(text: str) -> str:
    text = text[:PREVIEW_CHARS]
    lines = text.splitlines()
    if len(lines) > PREVIEW_LINES:
        lines = lines[:PREVIEW_LINES] + [f"... [truncated, {len(text)} chars total]"]
    return "\n".join(lines)


def main() -> int:
    md = [
        "# Appendix B — Specimen pages",
        "",
        "Same page, five parsers. We show the first ~30 lines of extracted text",
        "per parser to let the reader see *qualitatively* what the cluster CER",
        "numbers in §6.2 are measuring. Full extracts are in `results/specimen_pages/`.",
        "",
    ]
    out_dir = RESULTS / "specimen_pages"
    out_dir.mkdir(parents=True, exist_ok=True)

    for doc_id, page_idx, label in SPECIMENS:
        pdf = CORPUS / f"{doc_id}.pdf"
        if not pdf.exists():
            print(f"  ! missing {pdf}", file=sys.stderr)
            continue
        md.append(f"## B.{SPECIMENS.index((doc_id, page_idx, label)) + 1} {doc_id} — {label}")
        md.append("")
        for parser_name in PARSERS_ORDER:
            try:
                text = extract_page(parser_name, pdf, page_idx)
            except Exception as exc:
                text = f"<{parser_name} crashed: {exc}>"
            full_path = out_dir / f"{doc_id}_page{page_idx}_{parser_name}.txt"
            full_path.write_text(text)
            md.append(f"### {parser_name}")
            md.append("")
            md.append("```")
            md.append(preview(text))
            md.append("```")
            md.append("")
            print(f"  {parser_name:18s} {doc_id} p{page_idx}: {len(text):>6,} chars → {full_path.name}")
        md.append("---")
        md.append("")

    out = RESULTS / "appendix_b_specimen_pages.md"
    out.write_text("\n".join(md))
    print(f"\nWrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
