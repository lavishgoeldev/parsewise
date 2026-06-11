"""parsewise — smart PDF text extraction for RAG.

Two public APIs at v0.1:

    >>> from parsewise import extract, recommended_config
    >>> text = extract("doc.pdf")                                 # PyMuPDF default
    >>> text = extract("doc.pdf", parser="pdfplumber",
    ...                config=recommended_config("pdfplumber"))  # tuned pdfplumber

Both are deliberately thin. The point of v0.1 is to:
  1. Provide a single `extract()` entrypoint that works across the 4 popular
     pure-Python PDF text-layer parsers.
  2. Ship the *recommended configurations* identified in the parsewise
     benchmark — see `papers/2026-06-pdf-parsers/PAPER.md` — so that
     practitioners do not silently inherit divergent default-config behaviour.

Future versions add `router.route(path)` which picks the best parser per
document on a layout-complexity score.
"""
from __future__ import annotations

from pathlib import Path

from .configs import recommended_config
from .parsers import REGISTRY

__version__ = "0.1.0"

__all__ = ["extract", "recommended_config", "REGISTRY", "__version__"]


def extract(
    pdf_path: str | Path,
    *,
    parser: str = "pymupdf",
    config: dict | None = None,
) -> str:
    """Extract text from a PDF.

    Parameters
    ----------
    pdf_path : str | pathlib.Path
        Path to a PDF file.
    parser : str
        One of: ``"pymupdf"`` (default — fastest, Cluster A),
        ``"pypdf"`` (Cluster A), ``"pdfplumber"`` (Cluster C unless tuned),
        ``"pdfplumber_tuned"`` (pdfplumber with the recommended config baked
        in — Cluster A), ``"pdfminer"`` (Cluster B).
    config : dict | None
        Optional keyword arguments passed to the underlying parser's
        extraction call. For pdfplumber, use
        :func:`recommended_config("pdfplumber")` to get the configuration
        that moves it from Cluster C to Cluster A. Most other parsers ignore
        this argument at v0.1.

    Returns
    -------
    str
        Concatenated page text, with form-feed (``\\f``) page separators.
    """
    if parser not in REGISTRY:
        raise KeyError(
            f"Unknown parser {parser!r}. Available: {sorted(REGISTRY)}"
        )
    p = REGISTRY[parser]
    return p.extract(Path(pdf_path), config=config) if hasattr(p, "extract") and "config" in p.extract.__code__.co_varnames else p.extract(Path(pdf_path))
