#!/usr/bin/env bash
# Build PAPER.pdf from PAPER.md.
#
# Requires:
#   - pandoc (brew install pandoc)
#   - weasyprint (pip install weasyprint) — Python HTML-to-PDF engine; no LaTeX needed.
#
# Usage:
#   ./build.sh
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

INPUT="PAPER.md"
HTML="PAPER.html"
OUTPUT="PAPER.pdf"
CSS="style.css"

if ! command -v pandoc >/dev/null 2>&1; then
    echo "error: pandoc not installed. Run: brew install pandoc" >&2
    exit 1
fi

# Find weasyprint — prefer the local benchmark venv, fall back to PATH.
WEASYPRINT="$(command -v weasyprint || true)"
for cand in \
    "/Users/lavishgoel/private-workspace/privatevault/benchmark/.venv/bin/weasyprint" \
    "$HERE/../../.venv/bin/weasyprint"
do
    if [ -x "$cand" ]; then WEASYPRINT="$cand"; break; fi
done
if [ -z "$WEASYPRINT" ]; then
    echo "error: weasyprint not installed. Run: pip install weasyprint" >&2
    exit 1
fi

echo "==> Markdown → HTML"
pandoc "$INPUT" \
    --from markdown+pipe_tables+fenced_code_blocks+autolink_bare_uris \
    --to html5 \
    --standalone \
    --metadata pagetitle="parsewise — PDF Parser Paper" \
    --css "$CSS" \
    --output "$HTML"

echo "==> HTML → PDF"
"$WEASYPRINT" "$HTML" "$OUTPUT"

echo "==> Wrote $OUTPUT"
ls -lh "$OUTPUT"
