"""Parser wrappers — one ``extract(path)`` method per backend.

See ``papers/2026-06-pdf-parsers/PAPER.md`` for the agreement-cluster
findings that justify the configuration choices in :mod:`parsewise.configs`.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class Parser(ABC):
    name: str
    install: str

    @abstractmethod
    def extract(self, pdf_path: Path, *, config: dict | None = None) -> str:
        """Return concatenated page text with form-feed page separators."""


class PyMuPDFParser(Parser):
    name = "pymupdf"
    install = "pip install pymupdf"

    def extract(self, pdf_path: Path, *, config: dict | None = None) -> str:
        import fitz
        out = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                out.append(page.get_text("text"))
        return "\f".join(out)


class PdfPlumberParser(Parser):
    """pdfplumber at default settings.

    Without an explicit config, this produces Cluster-C text — diverging from
    every other parser on layout-complex documents. Pass
    :func:`parsewise.recommended_config("pdfplumber")` to get Cluster-A text.
    """
    name = "pdfplumber"
    install = "pip install pdfplumber"

    def extract(self, pdf_path: Path, *, config: dict | None = None) -> str:
        import pdfplumber
        kwargs = dict(config) if config else {}
        out = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                out.append(page.extract_text(**kwargs) or "")
        return "\f".join(out)


class PdfPlumberTunedParser(Parser):
    """pdfplumber preconfigured with the recommended config baked in.

    Same engine as :class:`PdfPlumberParser`. Provided as a convenience so
    callers can write ``extract(path, parser="pdfplumber_tuned")`` without
    passing a config kwarg.
    """
    name = "pdfplumber_tuned"
    install = "pip install pdfplumber"

    def extract(self, pdf_path: Path, *, config: dict | None = None) -> str:
        import pdfplumber
        kwargs = {
            "x_tolerance": 2,
            "y_tolerance": 2,
            "use_text_flow": True,
            "layout": False,
        }
        if config:
            kwargs.update(config)
        out = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                out.append(page.extract_text(**kwargs) or "")
        return "\f".join(out)


class PypdfParser(Parser):
    name = "pypdf"
    install = "pip install pypdf"

    def extract(self, pdf_path: Path, *, config: dict | None = None) -> str:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        return "\f".join(page.extract_text() or "" for page in reader.pages)


class PdfMinerParser(Parser):
    name = "pdfminer"
    install = "pip install pdfminer.six"

    def extract(self, pdf_path: Path, *, config: dict | None = None) -> str:
        from pdfminer.high_level import extract_text
        return extract_text(str(pdf_path)) or ""


REGISTRY: dict[str, Parser] = {
    p.name: p
    for p in (
        PyMuPDFParser(),
        PdfPlumberParser(),
        PdfPlumberTunedParser(),
        PypdfParser(),
        PdfMinerParser(),
    )
}


def get(name: str) -> Parser:
    if name not in REGISTRY:
        raise KeyError(f"Unknown parser {name!r}. Known: {sorted(REGISTRY)}")
    return REGISTRY[name]


__all__ = [
    "Parser",
    "PyMuPDFParser",
    "PdfPlumberParser",
    "PdfPlumberTunedParser",
    "PypdfParser",
    "PdfMinerParser",
    "REGISTRY",
    "get",
]
