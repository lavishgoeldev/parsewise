# §6.4 Reading-order analysis — token set vs sequence overlap

**Claim:** parser disagreement on real PDFs is concentrated in sequence
order, not token identity. We measure:

- `jaccard_tokens`: Jaccard similarity over the set of unique word tokens.
- `jaccard_5gram`: Jaccard over the set of token 5-grams (sequence-sensitive).

If the hypothesis holds, even high-CER pairs should show `jaccard_tokens` near 1
(parsers extract the same words) while `jaccard_5gram` drops (different order).

## Per-pair summary (mean over 30 docs, 95% bootstrap CI)

| Parser pair | mean CER [95% CI] | mean Jaccard-tokens [95% CI] | mean Jaccard-5gram [95% CI] |
|---|---|---|---|
| pdfplumber vs pdfminer | 0.353  [0.257, 0.446] | 0.986  [0.978, 0.993] | 0.571  [0.482, 0.666] |
| pdfplumber vs pdfplumber_tuned | 0.371  [0.277, 0.460] | 0.991  [0.983, 0.997] | 0.601  [0.522, 0.686] |
| pdfplumber vs pypdf | 0.371  [0.277, 0.461] | 0.971  [0.962, 0.979] | 0.587  [0.511, 0.669] |
| pdfplumber_tuned vs pdfminer | 0.197  [0.140, 0.258] | 0.995  [0.992, 0.997] | 0.716  [0.647, 0.784] |
| pdfplumber_tuned vs pypdf | 0.002  [0.002, 0.003] | 0.977  [0.970, 0.984] | 0.949  [0.932, 0.965] |
| pymupdf vs pdfminer | 0.200  [0.143, 0.260] | 0.993  [0.989, 0.996] | 0.716  [0.647, 0.783] |
| pymupdf vs pdfplumber | 0.373  [0.278, 0.463] | 0.991  [0.982, 0.997] | 0.601  [0.522, 0.686] |
| pymupdf vs pdfplumber_tuned | 0.006  [0.002, 0.011] | 0.997  [0.996, 0.999] | 0.994  [0.990, 0.997] |
| pymupdf vs pypdf | 0.008  [0.004, 0.013] | 0.977  [0.970, 0.984] | 0.948  [0.931, 0.964] |
| pypdf vs pdfminer | 0.198  [0.141, 0.258] | 0.974  [0.967, 0.981] | 0.695  [0.632, 0.759] |

## Per-doc detail for headline pair `pymupdf vs pdfplumber`

If reading-order is the issue, columns 3 (`jaccard_tokens`) should remain near 1
regardless of layout, while column 4 (`jaccard_5gram`) tracks the CER.

| Doc | CER | jaccard_tokens | jaccard_5gram |
|---|---|---|---|
| L002 | 0.001 | 0.997 | 0.995 |
| L004 | 0.007 | 1.000 | 0.977 |
| L001 | 0.007 | 0.999 | 0.977 |
| L003 | 0.012 | 0.993 | 0.960 |
| IM008 | 0.012 | 0.887 | 0.880 |
| H003 | 0.027 | 1.000 | 0.954 |
| H002 | 0.041 | 0.996 | 0.947 |
| H001 | 0.048 | 0.986 | 0.885 |
| T002 | 0.151 | 1.000 | 0.705 |
| T004 | 0.163 | 1.000 | 0.580 |
| T001 | 0.202 | 0.991 | 0.569 |
| T006 | 0.293 | 0.998 | 0.700 |
| IM003 | 0.327 | 0.999 | 0.554 |
| IM005 | 0.363 | 0.999 | 0.565 |
| IM002 | 0.438 | 0.998 | 0.523 |
| IM007 | 0.505 | 1.000 | 0.409 |
| M005 | 0.519 | 0.989 | 0.427 |
| M002 | 0.537 | 0.995 | 0.555 |
| M001 | 0.569 | 1.000 | 0.483 |
| M003 | 0.581 | 0.996 | 0.488 |
| IM006 | 0.593 | 1.000 | 0.371 |
| IM004 | 0.595 | 1.000 | 0.349 |
| T008 | 0.604 | 0.993 | 0.389 |
| IM001 | 0.615 | 0.999 | 0.274 |
| T007 | 0.638 | 0.988 | 0.438 |
| M004 | 0.643 | 0.994 | 0.447 |
| M006 | 0.648 | 0.979 | 0.455 |
| T005 | 0.660 | 0.992 | 0.478 |
| H004 | 0.684 | 1.000 | 0.393 |
| T003 | 0.694 | 0.953 | 0.304 |
