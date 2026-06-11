"""Step 1.A — PDF parser bake-off on synthetic PDFs.

For every synth PDF and every parser:
  - extract text
  - compute CER and WER against the source text we rendered the PDF from
  - record latency (wall-clock seconds) and delta peak RSS (bytes)

Results are emitted as both a JSONL of raw records and a Markdown summary
table grouped by (parser, layout).

Usage:
    python -m scripts.eval_parsers
    python -m scripts.eval_parsers --parsers pymupdf,pdfplumber
"""
from __future__ import annotations

import argparse
import json
import resource
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYNTH_DIR = ROOT / "cache" / "synth_pdfs"
RESULTS_DIR = ROOT / "results"

try:
    from .parsers import REGISTRY
    from .text_metrics import cer, wer
except ImportError:
    sys.path.insert(0, str(ROOT))
    from scripts.parsers import REGISTRY  # type: ignore
    from scripts.text_metrics import cer, wer  # type: ignore


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--parsers", default=",".join(REGISTRY.keys()),
                   help=f"comma-separated subset of {list(REGISTRY)}")
    p.add_argument("--runs", type=int, default=3, help="n runs per (parser, pdf) for latency stats")
    args = p.parse_args()

    parser_names = [n.strip() for n in args.parsers.split(",")]
    parsers = [REGISTRY[n] for n in parser_names if n in REGISTRY]
    if not parsers:
        print(f"No parsers match {parser_names}", file=sys.stderr)
        return 2

    if not SYNTH_DIR.exists() or not list(SYNTH_DIR.glob("*.pdf")):
        print(f"No synth PDFs in {SYNTH_DIR.relative_to(ROOT)}.")
        print("Run: python -m scripts.synth_pdfs")
        return 1

    pdfs = sorted(SYNTH_DIR.glob("*.pdf"))
    records: list[dict] = []
    print(f"Evaluating {len(parsers)} parsers on {len(pdfs)} PDFs, {args.runs} runs each.")

    for pdf in pdfs:
        ref_path = pdf.with_suffix(".txt")
        if not ref_path.exists():
            print(f"  ! missing reference for {pdf.name}, skipping")
            continue
        reference = ref_path.read_text()
        sample_id, layout = pdf.stem.split("__", 1)

        for parser in parsers:
            latencies = []
            rss_deltas = []
            text = ""
            for _ in range(args.runs):
                pre = _peak_rss()
                t0 = time.perf_counter()
                try:
                    text = parser.extract(pdf)
                except Exception as exc:
                    print(f"  ! {parser.name} crashed on {pdf.name}: {exc}", file=sys.stderr)
                    text = ""
                    latencies.append(float("nan"))
                    break
                latencies.append(time.perf_counter() - t0)
                rss_deltas.append(_peak_rss() - pre)
            c = cer(text, reference) if text else 1.0
            w = wer(text, reference) if text else 1.0
            records.append({
                "parser": parser.name,
                "sample_id": sample_id,
                "layout": layout,
                "cer": c,
                "wer": w,
                "latency_p50_s": statistics.median(latencies) if latencies else None,
                "latency_max_s": max(latencies) if latencies else None,
                "peak_rss_delta_bytes_p50": statistics.median(rss_deltas) if rss_deltas else None,
                "runs": args.runs,
            })
            print(f"  {parser.name:12s} {pdf.name:34s} "
                  f"CER={c:.4f}  WER={w:.4f}  p50={statistics.median(latencies)*1000:.1f}ms")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RESULTS_DIR / "step1a_parsers_raw.jsonl"
    raw_path.write_text("\n".join(json.dumps(r) for r in records) + "\n")
    print(f"\nWrote raw records: {raw_path.relative_to(ROOT)}")

    md = _summary_md(records)
    md_path = RESULTS_DIR / "step1a_parsers_summary.md"
    md_path.write_text(md)
    print(f"Wrote summary:     {md_path.relative_to(ROOT)}")
    print("\n" + md)
    return 0


def _peak_rss() -> int:
    """Process peak RSS in bytes. ru_maxrss is in kB on Linux, bytes on macOS."""
    ru = resource.getrusage(resource.RUSAGE_SELF)
    if sys.platform == "darwin":
        return int(ru.ru_maxrss)
    return int(ru.ru_maxrss) * 1024


def _summary_md(records: list[dict]) -> str:
    # group by (parser, layout)
    groups: dict[tuple[str, str], list[dict]] = {}
    for r in records:
        groups.setdefault((r["parser"], r["layout"]), []).append(r)
    parsers = sorted({p for p, _ in groups})
    layouts = sorted({l for _, l in groups})
    lines = ["# Step 1.A — PDF parser eval (synthetic PDFs)", "",
             f"Records: {len(records)}", ""]
    for layout in layouts:
        lines.append(f"## Layout: `{layout}`\n")
        lines.append("| Parser | mean CER | mean WER | p50 latency (ms) |")
        lines.append("|---|---|---|---|")
        for parser in parsers:
            recs = groups.get((parser, layout), [])
            if not recs:
                continue
            mean_cer = statistics.mean(r["cer"] for r in recs)
            mean_wer = statistics.mean(r["wer"] for r in recs)
            mean_lat = statistics.mean(r["latency_p50_s"] for r in recs) * 1000
            lines.append(f"| {parser} | {mean_cer:.4f} | {mean_wer:.4f} | {mean_lat:.1f} |")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
