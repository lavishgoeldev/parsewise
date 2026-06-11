"""Generate synthetic-scan variants from the digital source documents.

For each eligible digital source we render two image-only PDFs:
  - _v1_high : DPI 220, rotation ±0.5°, gaussian noise σ=4, JPEG q=90  (clean-scan baseline)
  - _v2_low  : DPI 110, rotation ±1.5°, gaussian noise σ=12, JPEG q=55 (degraded-scan stressor)

Each variant is fully deterministic given the seed in its metadata, so we can
recreate the exact corpus from scratch.

Key correctness property: the variant's `ground_truth_text` is the digital
parent's PyMuPDF text extraction, locked at synthesis time. That lets us
compute per-doc character-error-rate for any OCR engine in Step 2.

Usage:
    python -m scripts.synthesize_scans
    python -m scripts.synthesize_scans --only L001
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

import fitz
import numpy as np
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"

try:
    from .sources import SOURCES, Source
except ImportError:
    sys.path.insert(0, str(ROOT))
    from scripts.sources import SOURCES, Source  # type: ignore


TIERS = {
    "v1_high": {"dpi": 220, "rot_max_deg": 0.5, "noise_sigma": 4.0,  "jpeg_quality": 90, "seed_offset": 1},
    "v2_low":  {"dpi": 110, "rot_max_deg": 1.5, "noise_sigma": 12.0, "jpeg_quality": 55, "seed_offset": 2},
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--only", type=str, default=None, help="comma-separated parent source ids")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    parents = [s for s in SOURCES if s.synthesize]
    if args.only:
        wanted = set(s.strip() for s in args.only.split(","))
        parents = [s for s in parents if s.id in wanted]

    n_done = n_skipped = 0
    for parent in parents:
        parent_pdf = CORPUS / parent.category / f"{parent.id}.pdf"
        if not parent_pdf.exists():
            print(f"[SKIP] parent {parent.id} not downloaded yet ({parent_pdf.name})")
            n_skipped += 1
            continue

        with fitz.open(parent_pdf) as doc:
            ground_truth_text = "\n\f\n".join(page.get_text("text") for page in doc)

        for tier_name, tier in TIERS.items():
            variant_id = f"{parent.id}_{tier_name}"
            variant_pdf = CORPUS / parent.category / f"{variant_id}.pdf"
            variant_meta = CORPUS / parent.category / f"{variant_id}.metadata.json"

            if args.dry_run:
                print(f"[DRY-RUN] {variant_id}  parent={parent.id}  tier={tier_name}")
                continue
            if variant_pdf.exists() and variant_meta.exists():
                print(f"[SKIP] {variant_id}: already synthesized")
                n_skipped += 1
                continue

            seed = _seed_for(parent.id, tier["seed_offset"])
            print(f"  Synthesizing {variant_id} (seed={seed}) …")
            _render_variant(parent_pdf, variant_pdf, tier=tier, seed=seed)

            sha = hashlib.sha256(variant_pdf.read_bytes()).hexdigest()
            page_count = _count_pages(variant_pdf)
            metadata = _build_metadata(parent, variant_id, tier_name, tier, seed,
                                       ground_truth_text, sha, page_count)
            variant_meta.write_text(json.dumps(metadata, indent=2))
            n_done += 1

    print(f"\nSynthesis summary: {n_done} variants created, {n_skipped} skipped.")
    return 0


def _seed_for(parent_id: str, offset: int) -> int:
    h = hashlib.sha256(parent_id.encode()).digest()
    return (int.from_bytes(h[:4], "big") + offset) & 0xFFFFFFFF


def _render_variant(src_pdf: Path, dst_pdf: Path, *, tier: dict, seed: int) -> None:
    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)
    out = fitz.open()
    with fitz.open(src_pdf) as doc:
        for page in doc:
            pix = page.get_pixmap(dpi=tier["dpi"])
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            img = _degrade(img, tier=tier, rng=rng, np_rng=np_rng)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=tier["jpeg_quality"])
            buf.seek(0)
            page_rect = fitz.Rect(0, 0, img.width, img.height)
            new_page = out.new_page(width=img.width, height=img.height)
            new_page.insert_image(page_rect, stream=buf.getvalue())
    out.save(dst_pdf, deflate=True)
    out.close()


def _degrade(img: Image.Image, *, tier: dict, rng: random.Random, np_rng) -> Image.Image:
    # 1. small rotation (with white fill)
    angle = rng.uniform(-tier["rot_max_deg"], tier["rot_max_deg"])
    img = img.rotate(angle, resample=Image.BILINEAR, fillcolor=(255, 255, 255))

    # 2. additive gaussian noise
    arr = np.asarray(img, dtype=np.int16)
    noise = np_rng.normal(0, tier["noise_sigma"], arr.shape).astype(np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, mode="RGB")

    # 3. JPEG round-trip happens during save downstream
    return img


def _count_pages(pdf: Path) -> int:
    with fitz.open(pdf) as doc:
        return doc.page_count


def _build_metadata(parent: Source, variant_id: str, tier_name: str, tier: dict, seed: int,
                    ground_truth_text: str, sha256: str, page_count: int) -> dict:
    today = datetime.now(timezone.utc).date().isoformat()
    return {
        "id": variant_id,
        "category": parent.category,
        "doc_type": f"{parent.doc_type}__synthetic_scan_{tier_name}",
        "source_url": f"derived://{parent.id}",
        "source_organization": parent.publisher,
        "license": parent.license,
        "license_verified_at": today,
        "format": "synthetic_scan",
        "synthetic_scan_params": {
            "source_doc_id": parent.id,
            "dpi": tier["dpi"],
            "rotation_degrees": tier["rot_max_deg"],
            "gaussian_noise_sigma": tier["noise_sigma"],
            "jpeg_quality": tier["jpeg_quality"],
            "seed": seed,
        },
        "page_count": page_count,
        "language": "en",
        "ground_truth_text": ground_truth_text,
        "added_at": today,
        "notes": f"Synthetic-scan variant of {parent.id} at tier {tier_name}. "
                 f"Generated deterministically; ground_truth_text taken from parent's PyMuPDF extraction.",
        "sha256": sha256,
    }


if __name__ == "__main__":
    sys.exit(main())
