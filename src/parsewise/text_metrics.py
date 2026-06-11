"""Text-quality metrics for PDF parser evaluation (Step 1) and OCR (Step 2).

CER (Character Error Rate) = Levenshtein(predicted, reference) / len(reference)
WER (Word Error Rate)      = Levenshtein on tokens, divided by reference token count

We normalize both texts before scoring so that benign formatting differences
(extra whitespace, page-break characters, fancy quotes) don't dominate the
error rate.
"""
from __future__ import annotations

import re
import unicodedata

try:
    from Levenshtein import distance as lev_distance  # python-Levenshtein
except ImportError:  # pragma: no cover
    lev_distance = None


_WHITESPACE_RE = re.compile(r"\s+")
_FANCY_QUOTES = {
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "\xa0": " ",
}


def normalize(text: str) -> str:
    """Light normalization shared by CER and WER computation."""
    text = unicodedata.normalize("NFKC", text)
    for src, dst in _FANCY_QUOTES.items():
        text = text.replace(src, dst)
    text = text.replace("\f", " ")
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def cer(predicted: str, reference: str) -> float:
    if lev_distance is None:
        raise RuntimeError("python-Levenshtein not installed; pip install python-Levenshtein")
    p, r = normalize(predicted), normalize(reference)
    if not r:
        return 0.0 if not p else float("inf")
    return lev_distance(p, r) / len(r)


def wer(predicted: str, reference: str) -> float:
    if lev_distance is None:
        raise RuntimeError("python-Levenshtein not installed")
    p_tokens = normalize(predicted).split()
    r_tokens = normalize(reference).split()
    if not r_tokens:
        return 0.0 if not p_tokens else float("inf")
    # Levenshtein on token sequences via temporary unicode mapping
    vocab: dict[str, str] = {}
    def encode(toks: list[str]) -> str:
        out = []
        for t in toks:
            if t not in vocab:
                vocab[t] = chr(0xE000 + len(vocab))  # private use area
            out.append(vocab[t])
        return "".join(out)
    return lev_distance(encode(p_tokens), encode(r_tokens)) / len(r_tokens)


if __name__ == "__main__":
    ref = "The quick brown fox jumps over the lazy dog."
    pred = "the  quick brown fox jumped over the lazy dog"
    print(f"CER: {cer(pred, ref):.4f}")
    print(f"WER: {wer(pred, ref):.4f}")
