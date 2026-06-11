"""Pluggable OCR-engine backends for Step 2.

Each engine has `name`, `install` (how to install it), and
`ocr(pdf_path) -> str` returning concatenated text across pages.

The engine receives an image-only PDF (no text layer); it renders each page
to an image and runs the OCR.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class OCREngine(ABC):
    name: str
    install: str

    @abstractmethod
    def ocr(self, pdf_path: Path) -> str:
        """Return concatenated OCR text across all pages, page-break separated."""


class TesseractEngine(OCREngine):
    name = "tesseract"
    install = "brew install tesseract && pip install pytesseract"

    def __init__(self, lang: str = "eng", dpi: int = 220):
        self.lang = lang
        self.dpi = dpi

    def ocr(self, pdf_path: Path) -> str:
        import io
        import fitz
        import pytesseract
        from PIL import Image
        out = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                pix = page.get_pixmap(dpi=self.dpi)
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                out.append(pytesseract.image_to_string(img, lang=self.lang))
        return "\f".join(out)


class EasyOCREngine(OCREngine):
    name = "easyocr"
    install = "pip install easyocr  # heavy: pulls PyTorch"

    def __init__(self, langs: list[str] | None = None, dpi: int = 220):
        self.langs = langs or ["en"]
        self.dpi = dpi
        self._reader = None

    def _get_reader(self):
        if self._reader is None:
            import easyocr
            self._reader = easyocr.Reader(self.langs, gpu=False, verbose=False)
        return self._reader

    def ocr(self, pdf_path: Path) -> str:
        import fitz
        import numpy as np
        reader = self._get_reader()
        out = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                pix = page.get_pixmap(dpi=self.dpi)
                arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
                result = reader.readtext(arr, detail=0, paragraph=True)
                out.append("\n".join(result))
        return "\f".join(out)


def available() -> dict[str, OCREngine]:
    """Return engines whose dependencies are importable right now."""
    out: dict[str, OCREngine] = {}
    try:
        import pytesseract  # noqa: F401
        import shutil
        if shutil.which("tesseract"):
            out["tesseract"] = TesseractEngine()
    except ImportError:
        pass
    try:
        import easyocr  # noqa: F401
        out["easyocr"] = EasyOCREngine()
    except ImportError:
        pass
    return out


def get(name: str) -> OCREngine:
    engines = {"tesseract": TesseractEngine, "easyocr": EasyOCREngine}
    if name not in engines:
        raise KeyError(f"Unknown engine '{name}'. Known: {list(engines)}")
    return engines[name]()
