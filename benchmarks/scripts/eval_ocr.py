"""Step 2 — OCR engine bake-off on degraded synthetic PDFs.

For each (engine × scanned PDF × run): time the OCR, compute CER/WER vs the
parent PDF's ground-truth text, measure peak RSS delta. Results land in
benchmark/results/step2_ocr_*.

Usage:
    python -m scripts.eval_ocr                   # all available engines
    python -m scripts.eval_ocr --engines tesseract
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
SCAN_DIR = ROOT / "cache" / "scanned_synth_pdfs"
RESULTS_DIR = ROOT / "results"

try:
    from . import ocr_engines
    from .text_metrics import cer, wer
except ImportError:
    sys.path.insert(0, str(ROOT))
    from scripts import ocr_engines  # type: ignore
    from scripts.text_metrics import cer, wer  # type: ignore


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--engines", default=None, help="comma-separated engine names")
    p.add_argument("--runs", type=int, default=2)
    args = p.parse_args()

    avail = ocr_engines.available()
    if not avail:
        print("No OCR engines available. Install Tesseract (`brew install tesseract && "
              "pip install pytesseract`) or EasyOCR (`pip install easyocr`).", file=sys.stderr)
        return 2

    chosen_names = [n.strip() for n in args.engines.split(",")] if args.engines else list(avail)
    engines = [avail[n] for n in chosen_names if n in avail]
    if not engines:
        print(f"No engines match {chosen_names}. Available: {list(avail)}", file=sys.stderr)
        return 2

    if not SCAN_DIR.exists() or not list(SCAN_DIR.glob("*.pdf")):
        print(f"No scanned PDFs in {SCAN_DIR.relative_to(ROOT)}. "
              "Run: python -m scripts.degrade_synth_pdfs", file=sys.stderr)
        return 1

    pdfs = sorted(SCAN_DIR.glob("*.pdf"))
    records: list[dict] = []
    print(f"Evaluating {len(engines)} engines on {len(pdfs)} scanned PDFs, {args.runs} runs each.")

    for pdf in pdfs:
        ref_path = pdf.with_suffix(".txt")
        if not ref_path.exists():
            print(f"  ! missing reference for {pdf.name}", file=sys.stderr)
            continue
        reference = ref_path.read_text()
        # filename parses as e.g. S001__simple__high.pdf
        parts = pdf.stem.split("__")
        sample_id, layout, tier = parts[0], parts[1], parts[-1]

        for engine in engines:
            latencies = []
            text = ""
            for _ in range(args.runs):
                t0 = time.perf_counter()
                try:
                    text = engine.ocr(pdf)
                except Exception as exc:
                    print(f"  ! {engine.name} crashed on {pdf.name}: {exc}", file=sys.stderr)
                    text = ""
                    latencies.append(float("nan"))
                    break
                latencies.append(time.perf_counter() - t0)
            c = cer(text, reference) if text else 1.0
            w = wer(text, reference) if text else 1.0
            records.append({
                "engine": engine.name,
                "sample_id": sample_id,
                "layout": layout,
                "tier": tier,
                "cer": c,
                "wer": w,
                "latency_p50_s": statistics.median(latencies) if latencies else None,
                "latency_max_s": max(latencies) if latencies else None,
                "runs": args.runs,
            })
            p50 = statistics.median(latencies) * 1000 if latencies else float("nan")
            print(f"  {engine.name:10s} {pdf.name:36s} CER={c:.4f}  WER={w:.4f}  p50={p50:.0f}ms")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RESULTS_DIR / "step2_ocr_raw.jsonl"
    raw_path.write_text("\n".join(json.dumps(r) for r in records) + "\n")
    md = _summary_md(records)
    md_path = RESULTS_DIR / "step2_ocr_summary.md"
    md_path.write_text(md)
    print(f"\nWrote {raw_path.relative_to(ROOT)} and {md_path.relative_to(ROOT)}.")
    print("\n" + md)
    return 0


def _summary_md(records: list[dict]) -> str:
    # group by (engine, layout, tier)
    groups: dict[tuple[str, str, str], list[dict]] = {}
    for r in records:
        groups.setdefault((r["engine"], r["layout"], r["tier"]), []).append(r)
    engines = sorted({k[0] for k in groups})
    layouts = sorted({k[1] for k in groups})
    tiers = sorted({k[2] for k in groups})
    lines = [f"# Step 2 — OCR eval (synthetic scans)", "",
             f"Records: {len(records)}", ""]
    for tier in tiers:
        lines.append(f"## Tier: `{tier}`\n")
        lines.append("| Engine | Layout | mean CER | mean WER | p50 latency (ms) |")
        lines.append("|---|---|---|---|---|")
        for engine in engines:
            for layout in layouts:
                recs = groups.get((engine, layout, tier), [])
                if not recs:
                    continue
                mc = statistics.mean(r["cer"] for r in recs)
                mw = statistics.mean(r["wer"] for r in recs)
                ml = statistics.mean(r["latency_p50_s"] for r in recs if r["latency_p50_s"]) * 1000
                lines.append(f"| {engine} | {layout} | {mc:.4f} | {mw:.4f} | {ml:.1f} |")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
