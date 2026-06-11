# Parser Paper — Outline & Claim List

**Working title:** "Reading-Order Divergence Across PDF Text Parsers: Quantifying Layout-Driven Disagreement and Latency Trade-offs for Consumer-Hardware RAG"

**Target venue:** arXiv preprint → ACL / EMNLP / SIGIR workshop on RAG, IR, or document understanding.

**Length target:** 6–10 pages including refs.

**License:** Code Apache-2.0, dataset CC-BY 4.0 (where compositionally copyrightable), per-doc licenses retained.

**Reproducibility:** all scripts in `benchmark/scripts/`, all raw records in `benchmark/results/*.jsonl`, all corpus files in `benchmark/corpus/` with per-doc `metadata.json`.

---

## 0. House rules (per memory)

- **Honesty over results.** Lead each finding with what we *measured*; then what we can *conclude*; then explicitly what we *cannot conclude yet*. Methodology limits go in the body, not the appendix.
- **No product mentions.** This paper must not name, promote, or hint at the PrivateVault box. Consumer-hardware tiers are framed as neutral hardware classes (M-series Mac, 16 GB x86, low-power 8 GB) for community generalizability.
- **No paper-over.** Where the Step 1.A `with_table` reference bug existed, we either fix it before re-running or explicitly retract that data point.

---

## 1. Claim list (must be backed by data before paper ships)

| # | Claim | Evidence required | Current status |
|---|---|---|---|
| C1 | On clean text-layer PDFs, PyMuPDF, pdfplumber, and pypdf produce statistically indistinguishable text (CER < normalization floor). | Step 1.A, multi-layout, n≥3 runs, paired bootstrap 95% CI on CER. Fix `with_table` reference bug. | Data collected (n=45); methodology bug pending fix. |
| C2 | On real public-domain PDFs, **pdfplumber's extracted text systematically diverges from PyMuPDF and pypdf** at mean CER ≈ 0.44, while PyMuPDF ↔ pypdf agree at CER < 0.01. | Step 1.B, n≥30 real PDFs spanning 5 categories. Paired bootstrap 95% CI on pairwise CER. McNemar on per-page binary agreement. | n=6 currently; need n≈30+. |
| C3 | **Divergence scales monotonically with layout complexity** (multi-column publications and dense forms diverge most; short single-column forms diverge least). | Step 1.B with a layout-complexity score per doc (computed from PyMuPDF's block structure: column count, table presence, text-density-per-block variance). Regression of pairwise CER on the score. | Per-doc CER known; complexity score not yet computed. |
| C4 | The divergence is driven by **reading-order reconstruction**, not character-level errors: pdfplumber rebuilds reading order from text-span bounding boxes, while PyMuPDF/pypdf walk the document object in source order. | Qualitative analysis of disagreement loci on 5–10 specimen pages. n-gram order analysis: pdfplumber's *bag of tokens* often matches PyMuPDF's, but the *sequence* differs. | Hypothesis only; no diagnostic yet. |
| C5 | Tuning pdfplumber's reading-order parameters (`x_tolerance`, `y_tolerance`, `layout=True`) reduces but does not eliminate the divergence; tuned pdfplumber still differs from PyMuPDF/pypdf by ≥X% CER on layouts above a complexity threshold. | Step 1.B re-run with default vs tuned pdfplumber configs. | Not yet run. |
| C6 | A **fourth parser (Docling)** agrees with PyMuPDF/pypdf on simple text but produces a *third* reading order on complex layouts, suggesting the field has at least two non-degenerate reading-order conventions, not one "correct" one. | Step 1.B with Docling added; three-way agreement matrix. | Not yet run. |
| C7 | **Latency varies by ≥25× across parsers** on long publications; PyMuPDF is fastest, pdfplumber slowest. Latency × extraction-agreement defines a Pareto frontier with PyMuPDF dominating on long docs. | Step 1.B latency p50/p95 per parser per doc; per-page latency for fairness. Re-run on at least two hardware classes. | Single hardware class (M-series Mac) currently. |
| C8 | **Peak resident-set memory** differs by ≥10× between parsers on long docs, with pdfplumber the worst offender. | RSS-delta measurement per parser per doc. | Single-class data collected; needs verification on a 16 GB x86 baseline. |
| C9 | The choice of parser **defaults** in popular RAG frameworks (LangChain → pypdf, LlamaIndex → PyMuPDF, Haystack → tika/pdfplumber) is consequential: pypdf and PyMuPDF agree, so users of those frameworks land on equivalent text, but Haystack's pdfplumber default delivers materially different text from the same input. | Cite framework defaults with version pins. Map to claim C2. | Documentation review pending. |

**Claims we will NOT make** (and will say so):
- We will **not** claim any parser produces the "correct" text. No canonical ground truth exists for real PDFs.
- We will **not** generalize divergence findings beyond public-domain US-government PDFs in v0.1. Other domains (academic LaTeX-exports, scanned-then-OCR'd PDFs, born-digital legal contracts) are explicit out-of-scope until v0.2.
- We will **not** assert downstream RAG-quality impact in this paper. That goes in a future end-to-end paper. This paper is about text extraction alone.
- We will **not** report results from documents we haven't license-cleared.

---

## 2. Sections

### 2.1 Abstract (1 paragraph)

PDF text extraction is the first step of nearly every document-RAG pipeline, yet the choice between popular parsers is usually made on convenience rather than evidence. We benchmark three widely-used Python parsers (PyMuPDF, pdfplumber, pypdf), plus one document-structure parser (Docling), on (a) controlled synthetic PDFs where ground truth is exact, and (b) a corpus of N public-domain US-government PDFs spanning leases, invoices, medical literature, immigration forms, and tax publications. We find: clean PDFs produce statistically equivalent text across parsers; real PDFs produce mean pairwise CER ≈ 0.44 between pdfplumber and the other two, while PyMuPDF and pypdf agree at CER < 0.01; the divergence scales with layout complexity and is concentrated in reading-order reconstruction, not character recognition; latency varies by 25× on long documents; and tuning pdfplumber's reading-order parameters reduces but does not eliminate the gap. We release the corpus, the harness, and a layout-complexity scorer under permissive licenses. The findings are immediately consequential for the default parser choices baked into LangChain, LlamaIndex, and Haystack.

### 2.2 Introduction (~1 page)

- One paragraph framing: RAG quality is bounded above by what the document parser surfaces. Garbage in, citations out.
- One paragraph on the state of practice: parser choice is usually made by framework default, with little empirical guidance.
- One paragraph on the contributions list (see §1 claims).
- One paragraph on what this paper deliberately does NOT cover (scanned-PDF OCR — separate paper; downstream RAG quality — separate paper; non-English text — out of scope in v0.1).

### 2.3 Related Work (~0.5 page)

- BEIR (Thakur 2021), FiQA, NQ, HotpotQA — established RAG benchmarks; assume clean text input.
- DocVQA (Mathew 2021), VisualMRC — visual document question answering; assume rendered images, different problem.
- Marker (vikparuchuri), Docling (IBM) — document-structure tools; we include Docling.
- PaperFigures / pdfplumber / PyMuPDF developer docs — we cite published behavior notes.
- Position: no published paper we know of has quantified inter-parser disagreement on real-world long-form PDFs.

### 2.4 Corpus (~1 page)

- 30+ public-domain US-government PDFs across leases, invoices, medical, immigration, tax (per `benchmark/SOURCING_PLAN.md`).
- Per-doc metadata: source URL, Wayback archival, license verification, page count, layout-complexity score.
- Composition table (corpus/manifest.json — to be generated post-download).
- Synthetic-PDF corpus: 5 source texts × 3 layouts (simple, two_column, with_table), generated with ReportLab. Methodology bug in `with_table` flagged and fixed.

### 2.5 Methodology (~1.5 pages)

- Parser implementations: see `scripts/parsers.py`, exact versions pinned in `requirements.txt`.
- Extraction protocol: 3 runs per (parser, doc); record extracted text, latency, peak RSS delta. Take run-1 text as canonical for the parser; runs 2–3 for latency stats.
- Metrics: CER (Levenshtein distance over normalized text / length of reference); WER (token-level). Normalization defined in `scripts/text_metrics.py` — Unicode NFKC + collapse whitespace + lowercase. Normalization floor reported (~5% CER) and any claims below the floor are treated as noise.
- Pairwise comparison: for each doc, compute (CER, WER, length-ratio) for every parser pair. Mean over docs with bootstrap 95% CI (10 000 resamples). Paired bootstrap test for pairwise CER differences; McNemar's test for per-page binary agreement.
- Layout-complexity score: derived from PyMuPDF's block structure — number of detected columns × (1 + table-presence) × text-density variance across blocks. Defined in `scripts/layout_complexity.py` (to be written).
- Hardware: M-series MacBook (specify exact model + RAM). Latency cross-validation on 16 GB x86 baseline (to be added).
- Reproducibility: full reproducer documented in `benchmark/RUN.md`.

### 2.6 Results (~2.5 pages)

#### 2.6.1 Clean synthetic PDFs (Step 1.A)
- Table: per-layout CER/WER per parser with bootstrap CIs.
- Headline: parsers are statistically indistinguishable on clean PDFs once the `with_table` reference bug is fixed. Latency ordering is stable (pypdf < pymupdf < pdfplumber).

#### 2.6.2 Real PDFs — pairwise agreement (Step 1.B)
- Pairwise CER matrix with bootstrap CIs. **C2 lives here.**
- Per-category breakdown.

#### 2.6.3 Layout complexity vs divergence
- Scatter: layout-complexity score vs (pymupdf vs pdfplumber) CER per doc. Regression line, R². **C3 lives here.**

#### 2.6.4 Reading-order analysis
- n-gram overlap analysis: token-set overlap is high but sequence-order overlap is low. **C4 lives here.**
- 1–2 specimen pages with side-by-side extracted text showing the disagreement.

#### 2.6.5 pdfplumber tuned vs default
- pdfplumber with `x_tolerance / y_tolerance / layout=True` re-run on the same corpus. **C5 lives here.**

#### 2.6.6 Docling as a third parser cohort
- Three-way agreement matrix (PyMuPDF, pypdf, Docling). **C6 lives here.**

#### 2.6.7 Latency + memory
- Per-parser p50/p95 latency per page-count bucket.
- Pareto plot: latency × CER-disagreement-from-majority. **C7, C8 live here.**

#### 2.6.8 Framework default mapping
- Table of {Framework, default parser, claim-C2-relevant impact}. **C9 lives here.**

### 2.7 Limitations (~0.5 page) — MANDATORY, NOT BOILERPLATE

- We **cannot claim correctness**: no canonical ground truth on real PDFs. PyMuPDF/pypdf convergence is *suggestive* of correctness, not proof.
- n ≈ 30 is small. We chose 30+ as the minimum where bootstrap CIs are informative; a follow-up at n ≈ 100 would tighten estimates.
- Corpus is English-only and US-government-only. Multilingual and non-government PDFs are out of scope.
- We measure text extraction, not downstream RAG quality. A robust downstream pipeline might wash out the divergence.
- pypdf emits "padding error" warnings on some docs; we report these explicitly and discuss whether they signal partial extraction failure.

### 2.8 Conclusion (~0.5 page)

The state of practice in PDF text extraction for RAG pipelines rests on parser defaults that have not been quantitatively justified. We show those defaults are consequential: on real-world layouts the most popular parsers disagree at CER ≈ 0.44, almost entirely due to reading-order reconstruction. We make no normative claim about which parser is "correct," but we release the data needed for future work to make that case empirically.

### 2.9 Ethics, broader-impact, dataset-license appendix
- Per-document license matrix.
- Wayback-Machine archival policy.
- PII redaction policy (relevant for invoices; none retained in v0.1 corpus).

---

## 3. Figures / tables (target)

| # | Type | Section | Notes |
|---|---|---|---|
| F1 | Table | Corpus | Composition: category × format × source × license. |
| F2 | Table | Results 2.6.1 | Synthetic-PDF CER/WER with bootstrap CIs. |
| F3 | Heatmap | Results 2.6.2 | Pairwise CER per doc per pair. |
| F4 | Scatter+regression | Results 2.6.3 | Layout-complexity vs pairwise CER. **Headline figure candidate.** |
| F5 | Side-by-side | Results 2.6.4 | Two specimen pages, three parsers' extracted text. |
| F6 | Bar | Results 2.6.5 | pdfplumber default vs tuned divergence per doc. |
| F7 | Heatmap | Results 2.6.6 | Three-way agreement matrix incl. Docling. |
| F8 | Pareto | Results 2.6.7 | Latency × disagreement; per-hardware-class. **Headline figure candidate.** |
| F9 | Table | Results 2.6.8 | Framework default → parser → downstream impact. |

---

## 4. Pre-paper data-collection checklist

Ordered by blocking dependency:

1. **[ ] Fix Step 1.A `with_table` reference bug** (1–2 hr work). Either drop layout or include table text. Re-run 1.A.
2. **[ ] Expand real-PDF corpus from n=6 → n≥30** across 5 categories. License-clear each. (~1 day)
3. **[ ] Define and implement `layout_complexity.py` score.** Validate on the existing 6 docs (does it explain current CER spread?). (~3 hr)
4. **[ ] Add Docling to `parsers.py`.** Confirm install fits the venv (Docling ships heavy deps; quantify install footprint for paper.) (~2 hr)
5. **[ ] Add pdfplumber tuned config** as a separate REGISTRY entry. (~30 min)
6. **[ ] Refactor `eval_parsers_real.py`** to emit per-run records (so paired bootstrap is possible) and to compute bootstrap CIs + McNemar inline. (~3 hr)
7. **[ ] Re-run Step 1.B on full corpus, all parsers, all configs.** (~30 min runtime once n=30)
8. **[ ] Reading-order diagnostic:** n-gram sequence overlap vs n-gram set overlap, with specimen pages. (~half day)
9. **[ ] Latency cross-validation on a second hardware class** (e.g., a 16 GB x86 box or a t2/c5 EC2 instance). (~half day)
10. **[ ] Framework-default review:** read LangChain, LlamaIndex, Haystack source to confirm current default PDF parsers and pin versions. (~2 hr)

Once 1–10 are done the paper draft (`PAPER.md` → LaTeX) is mostly a writing exercise.

---

## 5. Risks / open questions

- **Risk: pdfplumber tuning closes the gap entirely.** Then C5 + headline weaken. Mitigation: if so, reframe paper around the *defaults* problem rather than the parser-quality problem. Still publishable.
- **Risk: ground truth for synthetic PDFs has the normalization floor problem.** Mitigation: report the floor explicitly; all CER below the floor is treated as noise; framing is "indistinguishable" not "perfect."
- **Risk: a fourth parser produces yet another reading order.** That's actually the desired finding for C6.
- **Open question: which exact x/y tolerance values to use for tuned pdfplumber?** Decision: grid-search over the existing 6 docs, pick the best, lock those parameters for the full re-run. Report the grid in appendix.
- **Open question: should we include `marker` and `unstructured.io` as further parser candidates?** They're heavier (PyTorch deps). Decision: deferred to v2 unless a reviewer asks. Document the deferral in limitations.

---

## 6. What goes in the repo before submission

- `benchmark/corpus/manifest.json` — generated corpus index with license summary.
- `benchmark/corpus/<category>/` — all PDFs with `metadata.json` sidecars.
- `benchmark/scripts/` — all scripts pinned by `requirements.txt`.
- `benchmark/results/` — raw `.jsonl` records (gitignored by default but linked to a dataset release).
- `benchmark/paper/PAPER.md` (and eventual `paper.tex`) — the paper itself.
- `benchmark/paper/figures/` — generated PDFs/PNGs for each figure, regenerable from raw records.
- `benchmark/RUN.md` — reproducer instructions.

Open dataset release: HuggingFace Datasets card under `privatevault/pv-parser-bench-v0.1` (subject to name decision per [[open-decisions]]).
