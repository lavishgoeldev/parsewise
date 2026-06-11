"""Step 1.B — PDF parser eval on real US-govt PDFs.

For real-world PDFs no canonical ground-truth text exists. So we measure
*inter-parser agreement* using pairwise CER, plus per-parser extraction length,
latency, and memory. Divergences between parsers are themselves the finding.

Pipeline per PDF:
  - Run each parser N times → take run 1 as the parser's output, runs 2..N for latency stats.
  - Compute pairwise CER/WER between every parser pair.
  - Record per-parser: text length, latency p50, peak-RSS delta.

Outputs:
  results/step1b_parsers_real_raw.jsonl
  results/step1b_parsers_real_summary.md
"""
from __future__ import annotations

import argparse
import itertools
import json
import resource
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus" / "real"
RESULTS_DIR = ROOT / "results"

try:
    from .parsers import REGISTRY
    from .stats import bootstrap_mean_ci, paired_bootstrap_diff
    from .text_metrics import cer, wer, normalize
except ImportError:
    sys.path.insert(0, str(ROOT))
    from scripts.parsers import REGISTRY  # type: ignore
    from scripts.stats import bootstrap_mean_ci, paired_bootstrap_diff  # type: ignore
    from scripts.text_metrics import cer, wer, normalize  # type: ignore


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--parsers", default=",".join(REGISTRY.keys()))
    p.add_argument("--runs", type=int, default=3)
    args = p.parse_args()

    parser_names = [n.strip() for n in args.parsers.split(",")]
    parsers = [REGISTRY[n] for n in parser_names if n in REGISTRY]
    pdfs = sorted(CORPUS_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No real PDFs in {CORPUS_DIR.relative_to(ROOT)}.", file=sys.stderr)
        return 1

    print(f"Evaluating {len(parsers)} parsers on {len(pdfs)} real PDFs, {args.runs} runs each.\n")

    per_parser_records: list[dict] = []
    pair_records: list[dict] = []

    for pdf in pdfs:
        meta_path = pdf.with_suffix(".metadata.json")
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        page_count = meta.get("page_count", 0)
        category = meta.get("category", "?")
        outputs: dict[str, str] = {}

        for parser in parsers:
            latencies = []
            rss_deltas = []
            text = ""
            for run_i in range(args.runs):
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
            outputs[parser.name] = text
            text_len = len(normalize(text))
            per_parser_records.append({
                "parser": parser.name,
                "doc_id": pdf.stem,
                "category": category,
                "page_count": page_count,
                "extracted_text_chars": text_len,
                "chars_per_page": text_len / page_count if page_count else 0,
                "latency_p50_s": statistics.median(latencies) if latencies else None,
                "latency_p95_s": _pct(latencies, 95) if len(latencies) > 1 else max(latencies, default=None),
                "peak_rss_delta_bytes_p50": statistics.median(rss_deltas) if rss_deltas else None,
                "runs": args.runs,
            })
            p50 = statistics.median(latencies) * 1000 if latencies else float("nan")
            print(f"  {parser.name:11s} {pdf.name:18s} {text_len:>9,} chars  {p50:>6.0f}ms  ({page_count}pp)")

        # pairwise agreement
        for a, b in itertools.combinations(outputs.keys(), 2):
            ca = cer(outputs[a], outputs[b]) if outputs[a] and outputs[b] else float("nan")
            wa = wer(outputs[a], outputs[b]) if outputs[a] and outputs[b] else float("nan")
            la = len(normalize(outputs[a]))
            lb = len(normalize(outputs[b]))
            ratio = (min(la, lb) / max(la, lb)) if max(la, lb) else 0.0
            pair_records.append({
                "doc_id": pdf.stem,
                "category": category,
                "parser_a": a,
                "parser_b": b,
                "cer_ab": ca,
                "wer_ab": wa,
                "length_a": la,
                "length_b": lb,
                "length_ratio_min_over_max": ratio,
            })
        print()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    raw = {"per_parser": per_parser_records, "pairs": pair_records}
    raw_path = RESULTS_DIR / "step1b_parsers_real_raw.jsonl"
    raw_path.write_text(json.dumps(raw, indent=2))
    md = _summary_md(per_parser_records, pair_records, parsers)
    md_path = RESULTS_DIR / "step1b_parsers_real_summary.md"
    md_path.write_text(md)
    print(f"Wrote {raw_path.relative_to(ROOT)} and {md_path.relative_to(ROOT)}.\n")
    print(md)
    return 0


def _peak_rss() -> int:
    ru = resource.getrusage(resource.RUSAGE_SELF)
    if sys.platform == "darwin":
        return int(ru.ru_maxrss)
    return int(ru.ru_maxrss) * 1024


def _pct(vals: list[float], pct: int) -> float:
    if not vals:
        return float("nan")
    s = sorted(vals)
    k = max(0, min(len(s) - 1, int(round(pct / 100 * (len(s) - 1)))))
    return s[k]


def _summary_md(per_parser, pairs, parsers) -> str:
    parser_names = [p.name for p in parsers]
    lines = ["# Step 1.B — PDF parser eval on real public-domain US-govt PDFs", ""]

    # Per-parser summary
    lines.append("## Per-parser totals (across all docs)\n")
    lines.append("| Parser | Total chars | Mean chars/page | p50 latency (ms) | p95 latency (ms) |")
    lines.append("|---|---|---|---|---|")
    for name in parser_names:
        recs = [r for r in per_parser if r["parser"] == name]
        total_chars = sum(r["extracted_text_chars"] for r in recs)
        mean_cpp = statistics.mean(r["chars_per_page"] for r in recs if r["page_count"])
        p50 = statistics.mean(r["latency_p50_s"] for r in recs if r["latency_p50_s"]) * 1000
        p95 = statistics.mean(r["latency_p95_s"] for r in recs if r["latency_p95_s"]) * 1000
        lines.append(f"| {name} | {total_chars:,} | {mean_cpp:,.0f} | {p50:.1f} | {p95:.1f} |")
    lines.append("")

    # Per-doc per-parser detail
    lines.append("## Per-doc extraction length (chars)\n")
    lines.append("| Doc | Pages | " + " | ".join(parser_names) + " | min/max ratio |")
    lines.append("|---|---|" + "---|" * len(parser_names) + "---|")
    docs = sorted({r["doc_id"] for r in per_parser})
    for doc in docs:
        recs = {r["parser"]: r for r in per_parser if r["doc_id"] == doc}
        pc = recs[parser_names[0]]["page_count"]
        lens = [recs[n]["extracted_text_chars"] for n in parser_names]
        ratio = min(lens) / max(lens) if max(lens) else 0.0
        cells = " | ".join(f"{l:,}" for l in lens)
        lines.append(f"| {doc} | {pc} | {cells} | {ratio:.3f} |")
    lines.append("")

    # Pairwise agreement (with bootstrap 95% CI on mean CER and WER)
    lines.append("## Pairwise inter-parser agreement (mean over docs, 95% bootstrap CI)\n")
    lines.append("Bootstrap: 10,000 resamples of doc-level metrics, percentile method.\n")
    lines.append("| Pair | mean CER [95% CI] | mean WER [95% CI] | mean length ratio | docs |")
    lines.append("|---|---|---|---|---|")
    pair_keys = sorted({(p["parser_a"], p["parser_b"]) for p in pairs})
    pair_cer_by_doc: dict[tuple[str, str], dict[str, float]] = {}
    for a, b in pair_keys:
        recs = [p for p in pairs if p["parser_a"] == a and p["parser_b"] == b]
        if not recs:
            continue
        cer_vals = [p["cer_ab"] for p in recs if p["cer_ab"] == p["cer_ab"]]
        wer_vals = [p["wer_ab"] for p in recs if p["wer_ab"] == p["wer_ab"]]
        cer_ci = bootstrap_mean_ci(cer_vals)
        wer_ci = bootstrap_mean_ci(wer_vals)
        mr = statistics.mean(p["length_ratio_min_over_max"] for p in recs)
        lines.append(f"| {a} vs {b} | {cer_ci.fmt()} | {wer_ci.fmt()} | {mr:.3f} | {len(recs)} |")
        pair_cer_by_doc[(a, b)] = {p["doc_id"]: p["cer_ab"] for p in recs}
    lines.append("")

    # Paired bootstrap comparisons: is the divergence to pdfplumber significantly
    # different from the agreement between pymupdf and pypdf?
    lines.append("## Paired bootstrap: per-pair CER differences (10,000 resamples)\n")
    lines.append("Same doc set, paired by doc_id. p two-sided.\n")
    lines.append("| Pair X | Pair Y | mean(X − Y) [95% CI] | p |")
    lines.append("|---|---|---|---|")
    docs_in_all = sorted(set.intersection(*(set(d.keys()) for d in pair_cer_by_doc.values()))) \
        if pair_cer_by_doc else []
    pairs_list = list(pair_keys)
    for i, px in enumerate(pairs_list):
        for py in pairs_list[i + 1:]:
            if px not in pair_cer_by_doc or py not in pair_cer_by_doc:
                continue
            xs = [pair_cer_by_doc[px][d] for d in docs_in_all]
            ys = [pair_cer_by_doc[py][d] for d in docs_in_all]
            diff_ci, p = paired_bootstrap_diff(xs, ys)
            lines.append(f"| {px[0]} vs {px[1]} | {py[0]} vs {py[1]} | {diff_ci.fmt()} | {p:.4f} |")
    lines.append("")

    # Per-category breakdown of pairwise CER — supports the layout-complexity story
    lines.append("## Per-category pairwise CER (mean, 95% bootstrap CI)\n")
    cats = sorted({p["category"] for p in pairs if p.get("category")})
    lines.append("| Category | n | " + " | ".join(f"{a} vs {b}" for a, b in pair_keys) + " |")
    lines.append("|---|---|" + "---|" * len(pair_keys))
    for cat in cats:
        cells = []
        n_docs_cat = len({p["doc_id"] for p in pairs if p["category"] == cat})
        for a, b in pair_keys:
            vals = [p["cer_ab"] for p in pairs
                    if p["category"] == cat and p["parser_a"] == a and p["parser_b"] == b
                    and p["cer_ab"] == p["cer_ab"]]
            if vals:
                ci = bootstrap_mean_ci(vals, n_resamples=2000)
                cells.append(ci.fmt(3))
            else:
                cells.append("—")
        lines.append(f"| {cat} | {n_docs_cat} | " + " | ".join(cells) + " |")
    lines.append("")

    # Per-doc pairwise CER (where do parsers disagree most?)
    lines.append("## Per-doc pairwise CER (where do parsers disagree most?)\n")
    lines.append("| Doc | " + " | ".join(f"{a} vs {b}" for a, b in pair_keys) + " |")
    lines.append("|---|" + "---|" * len(pair_keys))
    for doc in docs:
        cells = []
        for a, b in pair_keys:
            recs = [p for p in pairs if p["doc_id"] == doc and p["parser_a"] == a and p["parser_b"] == b]
            if recs:
                c = recs[0]["cer_ab"]
                cells.append(f"{c:.3f}" if c == c else "—")
            else:
                cells.append("—")
        lines.append(f"| {doc} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
