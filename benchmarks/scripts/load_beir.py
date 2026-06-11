"""Loader for BEIR subsets used as the headline benchmark.

We use four BEIR datasets relevant to personal-doc RAG:
  - FiQA-2018  : financial QA — closest to personal-finance use case
  - SciFact    : fact verification with citations — relevant to citation-quality study
  - HotpotQA   : multi-hop QA — multi-chunk synthesis
  - NFCorpus   : nutrition / medical retrieval — medical category

Datasets are downloaded on first use into benchmark/cache/beir/, then
returned as in-memory dicts of {corpus, queries, qrels}.

Usage:
    from scripts.load_beir import load_dataset
    corpus, queries, qrels = load_dataset("fiqa")
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache" / "beir"

# BEIR dataset name -> default URL on the BEIR HuggingFace mirror
DATASETS = {
    "fiqa": "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/fiqa.zip",
    "scifact": "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scifact.zip",
    "hotpotqa": "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/hotpotqa.zip",
    "nfcorpus": "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nfcorpus.zip",
}


def load_dataset(name: str, split: str = "test") -> tuple[dict, dict, dict]:
    """Return (corpus, queries, qrels) for a BEIR dataset.

    corpus  : {doc_id: {"title": ..., "text": ...}}
    queries : {query_id: query_text}
    qrels   : {query_id: {doc_id: relevance_score}}
    """
    try:
        from beir import util
        from beir.datasets.data_loader import GenericDataLoader
    except ImportError as exc:
        raise ImportError(
            "BEIR not installed. Install with: pip install beir"
        ) from exc

    if name not in DATASETS:
        raise ValueError(f"Unknown BEIR dataset '{name}'. Choices: {list(DATASETS)}")

    CACHE.mkdir(parents=True, exist_ok=True)
    out_dir = util.download_and_unzip(DATASETS[name], str(CACHE))
    corpus, queries, qrels = GenericDataLoader(data_folder=out_dir).load(split=split)
    return corpus, queries, qrels


def small_split(corpus: dict, queries: dict, qrels: dict, *, n_queries: int = 50) -> tuple[dict, dict, dict]:
    """Subset to ~n_queries for fast smoke-tests.

    Keeps only the docs that are in the qrels of the kept queries so the
    corpus stays small but coherent.
    """
    sub_q_ids = list(queries.keys())[:n_queries]
    sub_queries = {qid: queries[qid] for qid in sub_q_ids}
    sub_qrels = {qid: qrels[qid] for qid in sub_q_ids if qid in qrels}
    keep_docs: set[str] = set()
    for rels in sub_qrels.values():
        keep_docs.update(rels.keys())
    sub_corpus = {did: corpus[did] for did in keep_docs if did in corpus}
    return sub_corpus, sub_queries, sub_qrels


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("dataset", choices=list(DATASETS.keys()))
    p.add_argument("--small", action="store_true", help="load a ~50-query subset for smoke-test")
    args = p.parse_args()
    print(f"Loading BEIR {args.dataset} …")
    corpus, queries, qrels = load_dataset(args.dataset)
    if args.small:
        corpus, queries, qrels = small_split(corpus, queries, qrels)
    print(f"  corpus:  {len(corpus):,} docs")
    print(f"  queries: {len(queries):,}")
    print(f"  qrels:   {sum(len(v) for v in qrels.values()):,} relevance judgments")
