# parsewise

> *Smart PDF text extraction for RAG: agreement-tested wrappers, tuned configs, and an open benchmark.*

`parsewise` is two things in one repository:

1. **A small Python library** that wraps the popular PDF text-layer parsers (PyMuPDF, pdfplumber, pypdf, pdfminer.six) behind a single `extract()` interface, ships the **tuned configurations** identified in our research, and (in upcoming versions) routes documents to the best parser based on a layout-complexity score.
2. **An open benchmark + reproducible paper** measuring how those parsers actually agree on real public-domain PDFs. The first paper — *Reading-Order Divergence Across PDF Text Parsers* — is in [`papers/2026-06-pdf-parsers/`](papers/2026-06-pdf-parsers/PAPER.md).

The library and the benchmark live in one repo because the research findings **directly drive** the library's recommended defaults. The relationship is intentional.

---

## Why this exists

When you build a RAG pipeline you need a PDF parser. The community ships several. Their text extraction silently disagrees by up to 37 % CER on real layouts (multi-column publications, forms, legal opinions all behave differently), and no one has published a measurement large enough to act on. `parsewise` measures the disagreement, identifies the configuration that collapses it, and ships those defaults.

If your downstream RAG pipeline answers questions differently depending on which parser you happened to install, this library is the smallest change that fixes that.

---

## Quick start (library use)

```bash
pip install parsewise
```

```python
from parsewise import extract, recommended_config

# default: PyMuPDF (fastest parser in Cluster A — see the paper)
text = extract("doc.pdf")

# or explicitly pick a parser, with the *recommended* config:
text = extract("doc.pdf", parser="pdfplumber", config=recommended_config("pdfplumber"))
```

The `recommended_config("pdfplumber")` returns `{"x_tolerance": 2, "y_tolerance": 2, "use_text_flow": True}` — the configuration our benchmark shows collapses pdfplumber's default-config CER divergence from 0.37 to 0.006 vs PyMuPDF.

Future versions will ship a `route(path)` function that picks the optimal parser per document from a layout-complexity score.

---

## Repository layout

```
parsewise/
├── src/parsewise/           # the pip-installable library
│   ├── parsers/             # wrappers around PyMuPDF, pdfplumber, pypdf, pdfminer
│   ├── configs.py           # recommended configs (tuned-pdfplumber etc.)
│   ├── layout_complexity.py # per-doc geometric complexity scorer
│   ├── router.py            # (planned) layout-aware parser router
│   └── stats.py             # bootstrap CI + paired bootstrap helpers
├── benchmarks/              # all measurement code
│   ├── corpus/real/         # 30 public-domain US-govt PDFs + metadata
│   ├── scripts/             # reproducible eval pipeline
│   └── results/             # raw JSONL + summary Markdown + figures
├── papers/
│   └── 2026-06-pdf-parsers/ # the first paper
│       ├── PAPER.md
│       ├── PAPER.pdf        # built artifact (post arXiv)
│       └── figures/
├── docs/                    # usage guides + benchmark methodology
├── LICENSE                  # Apache-2.0 (code)
├── corpus/LICENSE.md        # CC-BY-4.0 (data)
└── pyproject.toml
```

---

## Reproducing the benchmark

```bash
git clone https://github.com/lavishgoeldev/parsewise
cd parsewise
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# re-download corpus (idempotent, sha-verified):
python -m benchmarks.scripts.download_real_pdfs

# re-run Step 1.A (synthetic PDFs):
python -m benchmarks.scripts.synth_pdfs
python -m benchmarks.scripts.eval_parsers

# re-run Step 1.B (real PDFs, n=30, 5 parsers, bootstrap CIs):
python -m benchmarks.scripts.eval_parsers_real

# regenerate the headline figure:
python -m benchmarks.scripts.plot_complexity_vs_cer
```

Raw records land in `benchmarks/results/*.jsonl`. Markdown summaries land alongside.

---

## Findings (TL;DR — full numbers in `papers/2026-06-pdf-parsers/PAPER.md`)

On 30 public-domain US-government PDFs across tax, immigration, medical, housing, and legal categories:

* **Three reading-order clusters** emerge among 5 Python parser configurations:
  - **Cluster A** = {PyMuPDF, pypdf, *tuned* pdfplumber} — agree within 1 % CER.
  - **Cluster B** = {pdfminer.six} — disagrees with Cluster A at ~20 % CER.
  - **Cluster C** = {pdfplumber at default settings} — disagrees with everything at ~37 % CER.
* **The divergence is layout-driven** (Pearson r = 0.80 between a layout-complexity score and pdfplumber-vs-PyMuPDF CER).
* **The disagreement is reading-order, not character recognition** — token-set Jaccard stays near 1.00 while 5-gram sequence Jaccard drops with CER.
* **Tuning pdfplumber's `x_tolerance / y_tolerance / use_text_flow` collapses the divergence** at zero latency cost. The library ships this config as `recommended_config("pdfplumber")`.
* **Latency spread: 22×.** PyMuPDF dominates the Pareto frontier on a consumer-hardware Apple Silicon tier.

---

## What's planned

Roadmap (see also the `papers/` directory):

| Phase | Artifact |
|---|---|
| v0.1 | This paper + the basic library wrappers + recommended configs. |
| v0.2 | OCR engine agreement paper (image-only PDFs); EasyOCR + Tesseract + macOS Vision. |
| v0.3 | Layout-aware parser **router** — `route(path)` picks the best parser per document on a complexity score; benchmark shows it beats every individual parser. |
| v0.4 | A new geometric reading-order reconstructor that takes PyMuPDF's character extraction and emits a smarter sequence. |
| v0.5 | DOCX, HTML, EPUB parser agreement studies. |

Each phase ships a paper + a library upgrade together.

---

## Licensing

* **Code:** Apache-2.0 (see `LICENSE`).
* **Corpus:** every document is a US federal government work in the public domain by 17 USC § 105. The aggregate composition is released under CC-BY-4.0 (see `corpus/LICENSE.md`).

---

## Citation

If you use the library or the benchmark, please cite the paper (citation block to be filled in after arXiv assignment):

```bibtex
@misc{goel2026parsewise,
  title  = {Reading-Order Divergence Across PDF Text Parsers: Quantifying Layout-Driven Disagreement and Latency Trade-offs on Consumer Hardware},
  author = {Goel, Lavish},
  year   = {2026},
  eprint = {[arXiv ID pending]},
  archivePrefix = {arXiv},
  primaryClass = {cs.IR}
}
```

---

## Contributing

Issues and PRs welcome. The benchmark is designed so new parsers can be added by registering them in `src/parsewise/parsers/registry.py` and re-running `eval_parsers_real.py`. See `docs/CONTRIBUTING.md`.
