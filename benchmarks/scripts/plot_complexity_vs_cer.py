"""Headline figure for the parser paper: layout complexity × pairwise CER.

Reads:
  results/step1b_parsers_real_raw.jsonl  (pairwise CER per (doc, parser-pair))
  results/layout_complexity.jsonl        (per-doc complexity score)

Outputs:
  results/fig_complexity_vs_cer.png
  results/correlations.json   (pearson + spearman for each parser-pair)
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

CATEGORY_COLOR = {
    "tax": "#1f77b4",
    "immigration": "#ff7f0e",
    "medical": "#2ca02c",
    "housing": "#d62728",
    "legal": "#9467bd",
}


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return float("nan")
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else float("nan")


def spearman(xs: list[float], ys: list[float]) -> float:
    def rank(vs: list[float]) -> list[float]:
        order = sorted(range(len(vs)), key=lambda i: vs[i])
        ranks = [0.0] * len(vs)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and vs[order[j + 1]] == vs[order[i]]:
                j += 1
            r = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[order[k]] = r
            i = j + 1
        return ranks
    return pearson(rank(xs), rank(ys))


def main() -> int:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    raw_path = RESULTS / "step1b_parsers_real_raw.jsonl"
    cx_path = RESULTS / "layout_complexity.jsonl"
    if not raw_path.exists() or not cx_path.exists():
        print(f"Missing inputs. Need {raw_path} and {cx_path}.", file=sys.stderr)
        return 1

    # Step 1.B raw is a single JSON object with per_parser + pairs lists.
    raw = json.loads(raw_path.read_text())
    pairs = raw.get("pairs", [])
    cx_rows = [json.loads(line) for line in cx_path.read_text().splitlines() if line.strip()]
    cx_by_doc = {r["doc_id"]: r for r in cx_rows}
    cat_by_doc = {r["doc_id"]: r.get("category", "?") for r in cx_rows}

    # Group pair_records by (parser_a, parser_b)
    pair_groups: dict[tuple[str, str], list[dict]] = {}
    for p in pairs:
        key = (p["parser_a"], p["parser_b"])
        pair_groups.setdefault(key, []).append(p)

    # Headline figure: pick four pairs that tell the cluster story.
    # If those pairs aren't present (e.g. old 3-parser data), fall back to
    # whatever is available.
    headline_pairs = [
        ("pymupdf", "pdfplumber"),         # A ↔ C — the bad case
        ("pymupdf", "pdfplumber_tuned"),   # within A — tuning fixed it
        ("pymupdf", "pdfminer"),           # A ↔ B — third cluster
        ("pymupdf", "pypdf"),              # within A — baseline
    ]
    headline_pairs = [k for k in headline_pairs if k in pair_groups]
    if not headline_pairs:
        headline_pairs = sorted(pair_groups.keys())
    pair_groups = {k: pair_groups[k] for k in headline_pairs}

    n = len(pair_groups)
    cols = 2 if n >= 2 else 1
    rows = (n + cols - 1) // cols
    fig, axes_arr = plt.subplots(rows, cols, figsize=(6 * cols, 4.5 * rows),
                                  sharex=True, sharey=True)
    if rows == 1 and cols == 1:
        axes = [axes_arr]
    else:
        axes = axes_arr.flatten() if hasattr(axes_arr, "flatten") else list(axes_arr)

    correlations = {}
    for ax, (pair_key, recs) in zip(axes, sorted(pair_groups.items())):
        a, b = pair_key
        xs, ys, cats = [], [], []
        for r in recs:
            doc_id = r["doc_id"]
            if doc_id not in cx_by_doc:
                continue
            x = cx_by_doc[doc_id]["complexity"]
            y = r["cer_ab"]
            if y != y:  # NaN
                continue
            xs.append(x)
            ys.append(y)
            cats.append(cat_by_doc.get(doc_id, "?"))

        for cat in sorted(set(cats)):
            cat_xs = [x for x, c in zip(xs, cats) if c == cat]
            cat_ys = [y for y, c in zip(ys, cats) if c == cat]
            ax.scatter(cat_xs, cat_ys, label=cat, s=70,
                       color=CATEGORY_COLOR.get(cat, "#777"),
                       edgecolor="black", linewidth=0.5, alpha=0.85)

        pr = pearson(xs, ys)
        sr = spearman(xs, ys)
        correlations[f"{a} vs {b}"] = {"pearson": pr, "spearman": sr, "n": len(xs)}
        ax.set_title(f"{a}  vs  {b}\nPearson r = {pr:.3f}   Spearman ρ = {sr:.3f}   n = {len(xs)}")
        ax.set_xlabel("Layout complexity score")
        ax.set_ylabel("Pairwise CER")
        ax.set_ylim(-0.02, 0.8)
        ax.grid(True, alpha=0.3)

    # Hide any unused subplots
    for ax in axes[len(pair_groups):]:
        ax.set_visible(False)
    axes[0].legend(loc="upper left", framealpha=0.9, fontsize=9)
    fig.suptitle("Pairwise CER scales with layout complexity — three reading-order clusters\n"
                 "(US public-domain PDFs, n = 30, 5 categories)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out_png = RESULTS / "fig_complexity_vs_cer.png"
    fig.savefig(out_png, dpi=150)
    print(f"Wrote {out_png.relative_to(ROOT)}")

    out_json = RESULTS / "correlations.json"
    out_json.write_text(json.dumps(correlations, indent=2))
    print(f"Wrote {out_json.relative_to(ROOT)}")
    for k, v in correlations.items():
        print(f"  {k:35s}  Pearson r = {v['pearson']:.3f}   Spearman ρ = {v['spearman']:.3f}   n = {v['n']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
