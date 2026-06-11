"""Degrade synth PDFs into image-only PDFs at controlled difficulty tiers.

For each PDF in cache/synth_pdfs/, render each page to PNG at a target DPI,
add controlled gaussian noise + rotation + JPEG re-encode, then assemble as
an image-only PDF (no text layer). The original PDF's `.txt` file is used
as the ground truth for OCR evaluation.

Output:
    cache/scanned_synth_pdfs/<sample_id>__<layout>__<tier>.pdf
    cache/scanned_synth_pdfs/<sample_id>__<layout>__<tier>.txt   ← ground truth (copied from parent)

Tiers parallel scripts/synthesize_scans.py:
    high : DPI 220, ±0.5°, σ=4,  q=90   (clean scan baseline)
    low  : DPI 110, ±1.5°, σ=12, q=55   (degraded scan stressor)
"""
from __future__ import annotations

import argparse
import hashlib
import io
import random
import sys
from pathlib import Path

import fitz
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SYNTH_DIR = ROOT / "cache" / "synth_pdfs"
OUT_DIR = ROOT / "cache" / "scanned_synth_pdfs"

TIERS = {
    "high": {"dpi": 220, "rot_max_deg": 0.5, "noise_sigma": 4.0,  "jpeg_quality": 90, "offset": 1},
    "low":  {"dpi": 110, "rot_max_deg": 1.5, "noise_sigma": 12.0, "jpeg_quality": 55, "offset": 2},
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--tiers", default="high,low", help="comma-separated tier names")
    args = p.parse_args()

    if not SYNTH_DIR.exists():
        print(f"No synth_pdfs/ at {SYNTH_DIR}. Run scripts.synth_pdfs first.", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tiers = [t.strip() for t in args.tiers.split(",") if t.strip()]
    n_done = 0
    for src_pdf in sorted(SYNTH_DIR.glob("*.pdf")):
        src_txt = src_pdf.with_suffix(".txt")
        if not src_txt.exists():
            print(f"  ! missing ground truth for {src_pdf.name}, skipping", file=sys.stderr)
            continue
        for tier_name in tiers:
            tier = TIERS[tier_name]
            out_pdf = OUT_DIR / f"{src_pdf.stem}__{tier_name}.pdf"
            out_txt = out_pdf.with_suffix(".txt")
            seed = _seed_for(src_pdf.stem, tier["offset"])
            _render_degraded(src_pdf, out_pdf, tier=tier, seed=seed)
            out_txt.write_text(src_txt.read_text())
            print(f"  wrote {out_pdf.name} (seed={seed})")
            n_done += 1
    print(f"\nGenerated {n_done} scanned-synth PDFs in {OUT_DIR.relative_to(ROOT)}")
    return 0


def _seed_for(stem: str, offset: int) -> int:
    h = hashlib.sha256(stem.encode()).digest()
    return (int.from_bytes(h[:4], "big") + offset) & 0xFFFFFFFF


def _render_degraded(src: Path, dst: Path, *, tier: dict, seed: int) -> None:
    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)
    out = fitz.open()
    with fitz.open(src) as doc:
        for page in doc:
            pix = page.get_pixmap(dpi=tier["dpi"])
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            img = img.rotate(
                rng.uniform(-tier["rot_max_deg"], tier["rot_max_deg"]),
                resample=Image.BILINEAR, fillcolor=(255, 255, 255),
            )
            arr = np.asarray(img, dtype=np.int16)
            arr = np.clip(arr + np_rng.normal(0, tier["noise_sigma"], arr.shape).astype(np.int16),
                          0, 255).astype(np.uint8)
            img = Image.fromarray(arr, mode="RGB")
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=tier["jpeg_quality"])
            new_page = out.new_page(width=img.width, height=img.height)
            new_page.insert_image(fitz.Rect(0, 0, img.width, img.height), stream=buf.getvalue())
    out.save(dst, deflate=True)
    out.close()


if __name__ == "__main__":
    sys.exit(main())
