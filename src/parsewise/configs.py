"""Recommended parser configurations identified by the parsewise benchmark.

These are the keyword arguments to pass to each parser's extraction call to
keep its output in **Cluster A** (the source-order traversal cluster — see
`papers/2026-06-pdf-parsers/PAPER.md`, §6.2 and §6.5).

For pdfplumber specifically, the default configuration produces text that
disagrees with PyMuPDF and pypdf at mean CER 0.37 on real PDFs. Switching to
the recommended config below collapses the disagreement to CER 0.006 — i.e.
within the normalization floor — at zero latency cost.

API:

    >>> from parsewise import recommended_config
    >>> recommended_config("pdfplumber")
    {'x_tolerance': 2, 'y_tolerance': 2, 'use_text_flow': True, 'layout': False}
"""
from __future__ import annotations

_RECOMMENDED: dict[str, dict] = {
    # pdfplumber: collapse Cluster C → Cluster A.
    "pdfplumber": {
        "x_tolerance": 2,
        "y_tolerance": 2,
        "use_text_flow": True,
        "layout": False,
    },
    # The remaining parsers are already in Cluster A or use their own
    # defaults; we record empty recommendations explicitly so callers can
    # treat the function as total.
    "pymupdf": {},
    "pypdf": {},
    "pdfminer": {},
    "pdfplumber_tuned": {
        "x_tolerance": 2,
        "y_tolerance": 2,
        "use_text_flow": True,
        "layout": False,
    },
}


def recommended_config(parser_name: str) -> dict:
    """Return the recommended keyword arguments for a parser.

    Returns an empty dict for parsers that have no specific recommendation
    beyond their default behaviour. Raises :class:`KeyError` for an unknown
    parser name.
    """
    if parser_name not in _RECOMMENDED:
        raise KeyError(
            f"Unknown parser {parser_name!r}. "
            f"Known: {sorted(_RECOMMENDED)}"
        )
    return dict(_RECOMMENDED[parser_name])
