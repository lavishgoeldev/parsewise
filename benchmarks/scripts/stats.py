"""Statistical helpers for the parser-paper analyses.

We deliberately keep this small and dependency-free:
  - bootstrap CI on a univariate mean (resample with replacement)
  - paired bootstrap test for the difference of two paired means
  - mean + bootstrap CI summary for a list of per-doc metrics

These are the only inferential machinery the parser paper needs at v0.1.
McNemar / chi-square style tests aren't used because the headline claims are
about continuous metrics (CER), not binary outcomes.
"""
from __future__ import annotations

import math
import random
import statistics
from dataclasses import dataclass


@dataclass
class CI:
    mean: float
    lo: float
    hi: float
    n: int

    def fmt(self, digits: int = 4) -> str:
        return f"{self.mean:.{digits}f}  [{self.lo:.{digits}f}, {self.hi:.{digits}f}]"


def bootstrap_mean_ci(
    values: list[float],
    *,
    n_resamples: int = 10_000,
    alpha: float = 0.05,
    seed: int = 0xBE_EF,
) -> CI:
    """Return mean + (alpha/2, 1-alpha/2) percentile bootstrap CI.

    NaN values are filtered out. With <2 non-NaN values, returns a degenerate
    CI with lo==hi==mean.
    """
    clean = [v for v in values if v == v]  # NaN-filter
    n = len(clean)
    if n == 0:
        return CI(mean=float("nan"), lo=float("nan"), hi=float("nan"), n=0)
    mean = statistics.fmean(clean)
    if n < 2:
        return CI(mean=mean, lo=mean, hi=mean, n=n)
    rng = random.Random(seed)
    means: list[float] = []
    for _ in range(n_resamples):
        s = 0.0
        for _ in range(n):
            s += clean[rng.randrange(n)]
        means.append(s / n)
    means.sort()
    lo = means[int(alpha / 2 * n_resamples)]
    hi = means[int((1 - alpha / 2) * n_resamples)]
    return CI(mean=mean, lo=lo, hi=hi, n=n)


def paired_bootstrap_diff(
    a: list[float],
    b: list[float],
    *,
    n_resamples: int = 10_000,
    alpha: float = 0.05,
    seed: int = 0xBE_EF,
) -> tuple[CI, float]:
    """Paired bootstrap test: estimate mean(a - b), 95% CI, and a two-sided p-value.

    Inputs must be the same length and paired (a[i] and b[i] come from the same doc).
    NaN-handling: any pair with either side NaN is dropped before resampling.

    Returns (CI of mean difference, two-sided p-value for H0: mean diff = 0).
    The p-value is the proportion of bootstrap diffs whose sign is opposite the
    observed mean diff, times 2 (two-sided), bounded by [1/n_resamples, 1.0].
    """
    if len(a) != len(b):
        raise ValueError(f"a and b must be same length: {len(a)} vs {len(b)}")
    pairs = [(x, y) for x, y in zip(a, b) if x == x and y == y]
    n = len(pairs)
    if n == 0:
        return CI(mean=float("nan"), lo=float("nan"), hi=float("nan"), n=0), float("nan")
    diffs = [x - y for x, y in pairs]
    mean = statistics.fmean(diffs)
    if n < 2:
        return CI(mean=mean, lo=mean, hi=mean, n=n), float("nan")
    rng = random.Random(seed)
    boot_diffs: list[float] = []
    for _ in range(n_resamples):
        s = 0.0
        for _ in range(n):
            s += diffs[rng.randrange(n)]
        boot_diffs.append(s / n)
    boot_diffs.sort()
    lo = boot_diffs[int(alpha / 2 * n_resamples)]
    hi = boot_diffs[int((1 - alpha / 2) * n_resamples)]
    # Two-sided p-value: proportion of resampled means on the "wrong" side of 0,
    # clamped to [1/n_resamples, 1.0]. This is a simple percentile-based p-value;
    # it is not the most powerful test in the literature but it is rigorous
    # enough for our claim-shape and easy to interpret.
    if mean >= 0:
        wrong_side = sum(1 for d in boot_diffs if d <= 0)
    else:
        wrong_side = sum(1 for d in boot_diffs if d >= 0)
    p_two_sided = min(1.0, max(1.0 / n_resamples, 2 * wrong_side / n_resamples))
    return CI(mean=mean, lo=lo, hi=hi, n=n), p_two_sided


def summarize_grouped_metric(
    records: list[dict],
    *,
    group_keys: tuple[str, ...],
    metric_key: str,
    n_resamples: int = 10_000,
) -> dict[tuple, CI]:
    """For each unique combination of group_keys, compute bootstrap mean CI of metric_key."""
    groups: dict[tuple, list[float]] = {}
    for r in records:
        key = tuple(r[k] for k in group_keys)
        v = r.get(metric_key)
        if v is None or (isinstance(v, float) and math.isnan(v)):
            continue
        groups.setdefault(key, []).append(float(v))
    return {k: bootstrap_mean_ci(vs, n_resamples=n_resamples) for k, vs in groups.items()}
