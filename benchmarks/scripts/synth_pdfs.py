"""Generate synthetic PDFs from input text in several controlled layouts.

For each (id, title, text) sample we produce N layout variants. Each variant
is a real PDF (with a text layer) that can be parsed by any PDF library; the
*ground truth* text for CER/WER computation is the original input string,
which we wrote into the PDF.

Layouts:
  - simple      : single column, plain paragraphs
  - two_column  : academic-paper-style two-column
  - with_table  : single column + an inserted table (stress-tests parsers)

Output:
  benchmark/cache/synth_pdfs/<id>__<layout>.pdf
  benchmark/cache/synth_pdfs/<id>__<layout>.txt   ← ground-truth text
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "cache" / "synth_pdfs"

try:
    from .sample_texts import SAMPLES, TextSample
except ImportError:
    sys.path.insert(0, str(ROOT))
    from scripts.sample_texts import SAMPLES, TextSample  # type: ignore


LAYOUTS = ("simple", "two_column", "with_table")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--layouts", default=",".join(LAYOUTS),
                   help="comma-separated subset of layouts to generate")
    p.add_argument("--only", default=None, help="comma-separated sample ids")
    args = p.parse_args()

    layouts = [l.strip() for l in args.layouts.split(",") if l.strip()]
    samples = SAMPLES
    if args.only:
        wanted = set(s.strip() for s in args.only.split(","))
        samples = [s for s in SAMPLES if s.id in wanted]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n_done = 0
    for sample in samples:
        for layout in layouts:
            pdf_path = OUT_DIR / f"{sample.id}__{layout}.pdf"
            txt_path = OUT_DIR / f"{sample.id}__{layout}.txt"
            try:
                _render(sample, layout, pdf_path)
                txt_path.write_text(_reference_text(sample, layout))
                n_done += 1
                print(f"  wrote {pdf_path.name}")
            except Exception as exc:
                print(f"  ! failed {sample.id}/{layout}: {exc}", file=sys.stderr)
    print(f"\nGenerated {n_done} synthetic PDFs in {OUT_DIR.relative_to(ROOT)}")
    return 0


def _table_data(sample: TextSample) -> list[list[str]]:
    return [
        ["Field", "Value"],
        ["Sample ID", sample.id],
        ["Source", sample.source[:60]],
        ["License", sample.license],
        ["Word count", str(len(sample.text.split()))],
    ]


def _reference_text(sample: TextSample, layout: str) -> str:
    if layout != "with_table":
        return sample.text
    # The with_table layout renders the body, then a 2-column table after it.
    # The reference must include the table content so parsers can match it;
    # without this, every parser shows a ~0.23 CER that reflects the missing
    # reference, not parser quality.
    table_text = "\n".join(" ".join(row) for row in _table_data(sample))
    return sample.text + "\n\n" + table_text


def _render(sample: TextSample, layout: str, out_path: Path) -> None:
    """Render `sample` as a PDF using ReportLab Platypus."""
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    )
    from reportlab.lib import colors

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", parent=styles["Heading1"], spaceAfter=12)
    body_style = ParagraphStyle("body", parent=styles["BodyText"], leading=14)

    width, height = LETTER
    margin = 0.75 * inch

    if layout == "two_column":
        col_gap = 0.25 * inch
        col_w = (width - 2 * margin - col_gap) / 2
        frames = [
            Frame(margin, margin, col_w, height - 2 * margin, id="L"),
            Frame(margin + col_w + col_gap, margin, col_w, height - 2 * margin, id="R"),
        ]
    else:
        frames = [Frame(margin, margin, width - 2 * margin, height - 2 * margin, id="main")]

    doc = BaseDocTemplate(str(out_path), pagesize=LETTER,
                          leftMargin=margin, rightMargin=margin,
                          topMargin=margin, bottomMargin=margin)
    doc.addPageTemplates([PageTemplate(id=layout, frames=frames)])

    story = [Paragraph(sample.title, title_style)]
    for para in sample.text.split("\n\n"):
        story.append(Paragraph(para.replace("\n", " "), body_style))
        story.append(Spacer(1, 6))

    if layout == "with_table":
        data = _table_data(sample)
        t = Table(data, colWidths=[1.5 * inch, 4.5 * inch])
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))
        story.append(Spacer(1, 12))
        story.append(t)

    doc.build(story)


if __name__ == "__main__":
    sys.exit(main())
