"""Pluggable PDF-parser backends for Step 1.

Each parser is a small class with a single `extract(path) -> str` method, plus
metadata for the results table (name, install footprint, etc.). Add a new
parser by writing a class and adding it to the REGISTRY at the bottom.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class Parser(ABC):
    name: str
    version_note: str = ""
    install: str

    @abstractmethod
    def extract(self, pdf_path: Path) -> str:
        """Return concatenated text across all pages, page-break-separated."""


class PyMuPDFParser(Parser):
    name = "pymupdf"
    install = "pip install pymupdf"

    def extract(self, pdf_path: Path) -> str:
        import fitz
        out = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                out.append(page.get_text("text"))
        return "\f".join(out)


class PdfPlumberParser(Parser):
    name = "pdfplumber"
    install = "pip install pdfplumber"

    def extract(self, pdf_path: Path) -> str:
        import pdfplumber
        out = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                out.append(page.extract_text() or "")
        return "\f".join(out)


class PdfPlumberTunedParser(Parser):
    """pdfplumber with tuned reading-order params.

    Hypothesis: relaxing x_tolerance and y_tolerance widens pdfplumber's word-
    grouping window, which may bring its reading order closer to the source-
    order traversal used by pymupdf and pypdf. Reported separately so the paper
    can show both default-config and tuned-config divergence.
    """
    name = "pdfplumber_tuned"
    install = "pip install pdfplumber"

    def extract(self, pdf_path: Path) -> str:
        import pdfplumber
        out = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                out.append(page.extract_text(x_tolerance=2, y_tolerance=2,
                                              layout=False, use_text_flow=True) or "")
        return "\f".join(out)


class PypdfParser(Parser):
    name = "pypdf"
    install = "pip install pypdf"

    def extract(self, pdf_path: Path) -> str:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        return "\f".join(page.extract_text() or "" for page in reader.pages)


class PdfMinerParser(Parser):
    """Light-weight pure-Python parser; the historical reference implementation."""
    name = "pdfminer"
    install = "pip install pdfminer.six"

    def extract(self, pdf_path: Path) -> str:
        from pdfminer.high_level import extract_text
        return extract_text(str(pdf_path)) or ""


REGISTRY: dict[str, Parser] = {
    p.name: p
    for p in (PyMuPDFParser(), PdfPlumberParser(), PdfPlumberTunedParser(),
              PypdfParser(), PdfMinerParser())
}


def get(name: str) -> Parser:
    if name not in REGISTRY:
        raise KeyError(f"Unknown parser '{name}'. Known: {list(REGISTRY)}")
    return REGISTRY[name]
