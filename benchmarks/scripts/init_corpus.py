"""End-to-end orchestrator for Step 0a.

Sequentially runs:
  1. download_corpus.py   — pull digital + real-scan sources
  2. synthesize_scans.py  — generate synthetic-scan variants
  3. build_manifest.py    — assemble corpus manifest
  4. validate_corpus.py   — smoke-test everything

Pauses for license-verification prompts during step 1 unless --yes.

Usage:
    python -m scripts.init_corpus
    python -m scripts.init_corpus --dry-run
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--yes", action="store_true", help="skip license-verification prompts (only for re-runs)")
    p.add_argument("--archive-wayback", action="store_true", help="archive each URL to web.archive.org")
    args = p.parse_args()

    steps = [
        ("Step 0a.3 — Downloading digital and real-scan sources",
         ["download_corpus"] + (["--dry-run"] if args.dry_run else [])
         + (["--yes"] if args.yes else [])
         + (["--archive-wayback"] if args.archive_wayback else [])),

        ("Step 0a.5 — Synthesizing scan variants",
         ["synthesize_scans"] + (["--dry-run"] if args.dry_run else [])),

        ("Step 0a.6 — Building manifest",
         ["build_manifest", "--validate"]),

        ("Step 0a.7 — Validating corpus",
         ["validate_corpus"]),
    ]

    for header, args_list in steps:
        print(f"\n{'='*70}\n{header}\n{'='*70}")
        cmd = [sys.executable, "-m", "scripts." + args_list[0], *args_list[1:]]
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            print(f"\n  ! {header} failed (exit {result.returncode}). Aborting.", file=sys.stderr)
            return result.returncode

    print("\nCorpus initialization complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
