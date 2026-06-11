"""Retrieval metrics used across all step evaluations.

Implementations are deliberately self-contained (no external metric lib) so
the methodology can be inspected and audited in the paper.

All metrics take:
    qrels    : {query_id: {doc_id: relevance_score (int)}}
    results  : {query_id: {doc_id: score (float)}}
where 'results' is the retriever's ranked output (higher score = more relevant).
"""
from __future__ import annotations

import math
from collections.abc import Iterable


def _rank_docs(results_for_q: dict[str, float]) -> list[str]:
    """Sort doc_ids by descending score; tie-broken by lexicographic doc_id for determinism."""
    return [d for d, _ in sorted(results_for_q.items(), key=lambda kv: (-kv[1], kv[0]))]


def recall_at_k(qrels: dict, results: dict, k: int) -> float:
    scores = []
    for qid, rels in qrels.items():
        if qid not in results:
            scores.append(0.0)
            continue
        positives = {d for d, r in rels.items() if r > 0}
        if not positives:
            continue
        ranked = _rank_docs(results[qid])[:k]
        hits = sum(1 for d in ranked if d in positives)
        scores.append(hits / len(positives))
    return _mean(scores)


def mrr(qrels: dict, results: dict, k: int | None = None) -> float:
    scores = []
    for qid, rels in qrels.items():
        if qid not in results:
            scores.append(0.0)
            continue
        positives = {d for d, r in rels.items() if r > 0}
        ranked = _rank_docs(results[qid])
        if k is not None:
            ranked = ranked[:k]
        rr = 0.0
        for i, d in enumerate(ranked, start=1):
            if d in positives:
                rr = 1.0 / i
                break
        scores.append(rr)
    return _mean(scores)


def ndcg_at_k(qrels: dict, results: dict, k: int) -> float:
    scores = []
    for qid, rels in qrels.items():
        if qid not in results:
            scores.append(0.0)
            continue
        ranked = _rank_docs(results[qid])[:k]
        gains = [rels.get(d, 0) for d in ranked]
        dcg = sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(gains))
        ideal_gains = sorted(rels.values(), reverse=True)[:k]
        idcg = sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(ideal_gains))
        scores.append(dcg / idcg if idcg > 0 else 0.0)
    return _mean(scores)


def hit_rate_at_k(qrels: dict, results: dict, k: int) -> float:
    scores = []
    for qid, rels in qrels.items():
        positives = {d for d, r in rels.items() if r > 0}
        if not positives:
            continue
        if qid not in results:
            scores.append(0.0)
            continue
        ranked = _rank_docs(results[qid])[:k]
        scores.append(1.0 if any(d in positives for d in ranked) else 0.0)
    return _mean(scores)


def all_metrics(qrels: dict, results: dict, ks: Iterable[int] = (1, 5, 10, 20)) -> dict[str, float]:
    out: dict[str, float] = {}
    for k in ks:
        out[f"recall@{k}"] = recall_at_k(qrels, results, k)
        out[f"ndcg@{k}"] = ndcg_at_k(qrels, results, k)
        out[f"hit@{k}"] = hit_rate_at_k(qrels, results, k)
    out["mrr"] = mrr(qrels, results)
    return out


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


# ─────────────────────────── self-test ───────────────────────────
if __name__ == "__main__":
    qrels = {"q1": {"d1": 2, "d2": 0, "d3": 1}, "q2": {"d4": 1}}
    results = {
        "q1": {"d3": 0.9, "d1": 0.8, "d2": 0.7},  # d3(rel=1) at 1, d1(rel=2) at 2
        "q2": {"d4": 0.5, "d5": 0.4},
    }
    print(all_metrics(qrels, results))
