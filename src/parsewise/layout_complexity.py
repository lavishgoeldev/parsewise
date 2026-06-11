"""Per-doc layout complexity score derived from PyMuPDF text-block geometry.

Hypothesis for the parser paper: parser disagreement on real PDFs is driven by
reading-order reconstruction, which is hardest when the page has multiple
visual columns or many non-aligned text blocks. So a simple geometric proxy
should correlate with the pdfplumber-vs-pymupdf CER.

The score is intentionally simple so reviewers can understand and reproduce it:

  complexity(doc) = mean over pages of (column_count_score + form_block_score)

where for a single page:

  column_count_score = number of distinct horizontal text-band centers,
                       clustered with a tolerance equal to 1/12 of page width.
                       A pure single-column page scores 1; a true two-column
                       publication scores 2; a 3-column table can score 3+.

  form_block_score   = a 0-or-1 indicator that the page has many small,
                       non-aligned blocks (heuristic: >20 text blocks AND
                       median block height < 5% of page height).
                       Captures form-page layouts (checkbox grids etc.)
                       that are not "columns" but still confuse readers.

Output: per-doc {column_count_mean, form_pages_frac, complexity}.

This is deliberately a coarse score; the paper's claim is monotonic, not
linear-precise. We also report the per-doc raw block count so readers can
sanity-check.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus" / "real"
RESULTS_DIR = ROOT / "results"


def page_column_count(blocks: list[tuple], page_width: float) -> int:
    """Estimate distinct horizontal text-band count on a single page.

    `blocks` is the list of (x0, y0, x1, y1, text, block_no, type) tuples that
    `fitz.Page.get_text("blocks")` returns. We:
      1. Filter to text-typed blocks with non-empty text.
      2. Take each block's x-center.
      3. Cluster x-centers with a tolerance of page_width / 12 (i.e. ~0.6 in
         on letter paper).
    """
    text_blocks = [b for b in blocks if b[6] == 0 and (b[4] or "").strip()]
    if not text_blocks:
        return 0
    centers = sorted((b[0] + b[2]) / 2 for b in text_blocks)
    tol = page_width / 12.0
    clusters: list[list[float]] = []
    for c in centers:
        if clusters and c - clusters[-1][-1] < tol:
            clusters[-1].append(c)
        else:
            clusters.append([c])
    return len(clusters)


def page_form_indicator(blocks: list[tuple], page_height: float) -> int:
    text_blocks = [b for b in blocks if b[6] == 0 and (b[4] or "").strip()]
    if len(text_blocks) <= 20:
        return 0
    heights = sorted((b[3] - b[1]) for b in text_blocks)
    median_h = heights[len(heights) // 2]
    return 1 if median_h < 0.05 * page_height else 0


def score_doc(pdf_path: Path) -> dict:
    import fitz
    per_page = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            blocks = page.get_text("blocks")
            cols = page_column_count(blocks, page.rect.width)
            form = page_form_indicator(blocks, page.rect.height)
            per_page.append({
                "page_no": page.number + 1,
                "n_blocks": sum(1 for b in blocks if b[6] == 0),
                "col_count": cols,
                "form_indicator": form,
            })
    if not per_page:
        return {"doc_id": pdf_path.stem, "complexity": 0.0,
                "column_count_mean": 0.0, "form_pages_frac": 0.0, "n_pages": 0,
                "n_blocks_mean": 0.0}
    col_mean = statistics.fmean(p["col_count"] for p in per_page)
    form_frac = statistics.fmean(p["form_indicator"] for p in per_page)
    block_mean = statistics.fmean(p["n_blocks"] for p in per_page)
    complexity = col_mean + form_frac
    return {
        "doc_id": pdf_path.stem,
        "n_pages": len(per_page),
        "column_count_mean": col_mean,
        "form_pages_frac": form_frac,
        "n_blocks_mean": block_mean,
        "complexity": complexity,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", default=str(CORPUS_DIR), help="dir with PDFs")
    p.add_argument("--out", default=str(RESULTS_DIR / "layout_complexity.jsonl"))
    args = p.parse_args()

    corpus = Path(args.corpus)
    pdfs = sorted(corpus.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs in {corpus}", file=sys.stderr)
        return 1

    rows: list[dict] = []
    for pdf in pdfs:
        meta_path = pdf.with_suffix(".metadata.json")
        category = "?"
        if meta_path.exists():
            category = json.loads(meta_path.read_text()).get("category", "?")
        row = score_doc(pdf)
        row["category"] = category
        rows.append(row)
        print(f"  {pdf.stem:6s} cat={category:12s} cols≈{row['column_count_mean']:.2f}  "
              f"form_frac={row['form_pages_frac']:.2f}  blocks≈{row['n_blocks_mean']:5.1f}  "
              f"complexity={row['complexity']:.3f}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    print(f"\nWrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
