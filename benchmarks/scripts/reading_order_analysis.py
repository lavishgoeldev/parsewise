"""Reading-order proof for §6.4 of the parser paper.

Hypothesis: when two parsers disagree at high CER on a real PDF, the
disagreement is dominated by **sequence order**, not by **token identity**.
We expect:
  - token-set Jaccard ≈ 1   (parsers extract the same set of words)
  - 5-gram sequence Jaccard ≪ 1 (parsers emit them in different orders)

Re-extracts each PDF with each parser (deterministic, run 1 only), tokenises
the output the same way, then for every parser pair on every doc reports:
  jaccard_tokens   = |A ∩ B| / |A ∪ B| over the bag of unique tokens
  jaccard_5gram    = |A ∩ B| / |A ∪ B| over the set of 5-grams of tokens
  cer (recomputed) = char error rate on normalized strings, for reference

Outputs:
  results/reading_order_analysis.jsonl   (per-doc per-pair rows)
  results/reading_order_analysis_summary.md
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus" / "real"
RESULTS = ROOT / "results"

try:
    from .parsers import REGISTRY
    from .text_metrics import cer, normalize
    from .stats import bootstrap_mean_ci
except ImportError:
    sys.path.insert(0, str(ROOT))
    from scripts.parsers import REGISTRY  # type: ignore
    from scripts.text_metrics import cer, normalize  # type: ignore
    from scripts.stats import bootstrap_mean_ci  # type: ignore


TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(normalize(text))


def ngrams(toks: list[str], n: int) -> set[tuple[str, ...]]:
    if len(toks) < n:
        return set()
    return {tuple(toks[i : i + n]) for i in range(len(toks) - n + 1)}


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def main() -> int:
    pdfs = sorted(CORPUS_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs in {CORPUS_DIR}", file=sys.stderr)
        return 1

    # Extract once per (parser, doc) — single run, as we're only computing
    # text-derived metrics that don't depend on latency.
    parser_names = list(REGISTRY.keys())
    print(f"Extracting {len(parser_names)} parsers × {len(pdfs)} docs (run 1 only)...")
    extracts: dict[tuple[str, str], str] = {}
    for pdf in pdfs:
        for name in parser_names:
            try:
                extracts[(name, pdf.stem)] = REGISTRY[name].extract(pdf)
            except Exception as exc:
                print(f"  ! {name} crashed on {pdf.name}: {exc}", file=sys.stderr)
                extracts[(name, pdf.stem)] = ""
        print(f"  {pdf.stem} extracted by {len(parser_names)} parsers")

    rows: list[dict] = []
    docs = [pdf.stem for pdf in pdfs]
    cats = {pdf.stem: json.loads(pdf.with_suffix(".metadata.json").read_text())
            .get("category", "?") if pdf.with_suffix(".metadata.json").exists() else "?"
            for pdf in pdfs}
    for i, a in enumerate(parser_names):
        for b in parser_names[i + 1:]:
            for doc in docs:
                ta = tokens(extracts[(a, doc)])
                tb = tokens(extracts[(b, doc)])
                jt = jaccard(set(ta), set(tb))
                jg5 = jaccard(ngrams(ta, 5), ngrams(tb, 5))
                c = cer(extracts[(a, doc)], extracts[(b, doc)]) if extracts[(a, doc)] and extracts[(b, doc)] else float("nan")
                rows.append({
                    "doc_id": doc,
                    "category": cats[doc],
                    "parser_a": a,
                    "parser_b": b,
                    "jaccard_tokens": jt,
                    "jaccard_5gram": jg5,
                    "cer": c,
                    "n_tokens_a": len(ta),
                    "n_tokens_b": len(tb),
                })

    out = RESULTS / "reading_order_analysis.jsonl"
    out.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    print(f"\nWrote {out.relative_to(ROOT)} ({len(rows)} rows)\n")

    # Summary
    md = ["# §6.4 Reading-order analysis — token set vs sequence overlap", ""]
    md.append("**Claim:** parser disagreement on real PDFs is concentrated in sequence")
    md.append("order, not token identity. We measure:")
    md.append("")
    md.append("- `jaccard_tokens`: Jaccard similarity over the set of unique word tokens.")
    md.append("- `jaccard_5gram`: Jaccard over the set of token 5-grams (sequence-sensitive).")
    md.append("")
    md.append("If the hypothesis holds, even high-CER pairs should show `jaccard_tokens` near 1")
    md.append("(parsers extract the same words) while `jaccard_5gram` drops (different order).")
    md.append("")
    md.append("## Per-pair summary (mean over 30 docs, 95% bootstrap CI)")
    md.append("")
    md.append("| Parser pair | mean CER [95% CI] | mean Jaccard-tokens [95% CI] | mean Jaccard-5gram [95% CI] |")
    md.append("|---|---|---|---|")
    pair_keys = sorted({(r["parser_a"], r["parser_b"]) for r in rows})
    for a, b in pair_keys:
        recs = [r for r in rows if r["parser_a"] == a and r["parser_b"] == b]
        cers = [r["cer"] for r in recs if r["cer"] == r["cer"]]
        jts = [r["jaccard_tokens"] for r in recs]
        jgs = [r["jaccard_5gram"] for r in recs]
        cer_ci = bootstrap_mean_ci(cers)
        jt_ci = bootstrap_mean_ci(jts)
        jg_ci = bootstrap_mean_ci(jgs)
        md.append(f"| {a} vs {b} | {cer_ci.fmt(3)} | {jt_ci.fmt(3)} | {jg_ci.fmt(3)} |")
    md.append("")

    # The clearest single statement: for the headline A↔C pair on each doc,
    # tokens stay similar while 5-grams diverge.
    a_c_pair = ("pymupdf", "pdfplumber")
    if a_c_pair in pair_keys:
        md.append(f"## Per-doc detail for headline pair `{a_c_pair[0]} vs {a_c_pair[1]}`")
        md.append("")
        md.append("If reading-order is the issue, columns 3 (`jaccard_tokens`) should remain near 1")
        md.append("regardless of layout, while column 4 (`jaccard_5gram`) tracks the CER.")
        md.append("")
        md.append("| Doc | CER | jaccard_tokens | jaccard_5gram |")
        md.append("|---|---|---|---|")
        recs_ac = [r for r in rows if r["parser_a"] == a_c_pair[0] and r["parser_b"] == a_c_pair[1]]
        for r in sorted(recs_ac, key=lambda r: r["cer"]):
            md.append(f"| {r['doc_id']} | {r['cer']:.3f} | {r['jaccard_tokens']:.3f} | {r['jaccard_5gram']:.3f} |")
        md.append("")

    summary = RESULTS / "reading_order_analysis_summary.md"
    summary.write_text("\n".join(md))
    print(f"Wrote {summary.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
