# Appendix A — Per-document data

All 30 corpus documents with: license metadata, layout-complexity score,
per-parser extraction length, and per-pair Character Error Rate.
License for every doc: public-domain (US federal government work, 17 USC §105).

## A.1 Document metadata

| ID | Category | Publisher | Pages | sha256 (truncated) |
|---|---|---|---|---|
| H001 | housing | U.S. Department of Housing and Urban Development | 15 | `ae735de3c9619a2b…` |
| H002 | housing | U.S. Department of Housing and Urban Development | 10 | `4199df227db0987b…` |
| H003 | housing | U.S. Department of Housing and Urban Development | 3 | `d084a477cd491b36…` |
| H004 | housing | U.S. Department of Housing and Urban Development | 5 | `22606c9b869126a3…` |
| IM001 | immigration | U.S. Citizenship and Immigration Services | 12 | `7fc733d4639995d6…` |
| IM002 | immigration | U.S. Citizenship and Immigration Services | 14 | `8b33868ba071e261…` |
| IM003 | immigration | U.S. Citizenship and Immigration Services | 24 | `7c8e1c5242d680b2…` |
| IM004 | immigration | U.S. Citizenship and Immigration Services | 7 | `9ac0eae287749d4c…` |
| IM005 | immigration | U.S. Citizenship and Immigration Services | 12 | `f231f39684ba4dd3…` |
| IM006 | immigration | U.S. Citizenship and Immigration Services | 7 | `fd436062284fd572…` |
| IM007 | immigration | U.S. Citizenship and Immigration Services | 4 | `d73cd620d241b0f8…` |
| IM008 | immigration | U.S. Citizenship and Immigration Services | 42 | `6630a6a2dc732b84…` |
| L001 | legal | Supreme Court of the United States | 118 | `85fb5ba49289e9d7…` |
| L002 | legal | Supreme Court of the United States | 82 | `93c73e3cb1ce0048…` |
| L003 | legal | Supreme Court of the United States | 20 | `f3015ab4890996a0…` |
| L004 | legal | Supreme Court of the United States | 119 | `4cbb9bd0c0f023cd…` |
| M001 | medical | U.S. Centers for Disease Control and Prevention | 26 | `7e9c6b33b3d9c33a…` |
| M002 | medical | U.S. Centers for Disease Control and Prevention | 28 | `543de06af3035445…` |
| M003 | medical | U.S. Centers for Disease Control and Prevention | 36 | `be45c0c188c5b25c…` |
| M004 | medical | U.S. Centers for Disease Control and Prevention | 27 | `441667795d311dce…` |
| M005 | medical | U.S. Centers for Disease Control and Prevention | 29 | `e75dd4c555cebaf5…` |
| M006 | medical | U.S. Centers for Disease Control and Prevention | 16 | `3e7af919c2f5d330…` |
| T001 | tax | U.S. Internal Revenue Service | 2 | `3d31c226df0d189c…` |
| T002 | tax | U.S. Internal Revenue Service | 2 | `ddf401dbe060467d…` |
| T003 | tax | U.S. Internal Revenue Service | 142 | `2d2381d62c7c77ed…` |
| T004 | tax | U.S. Internal Revenue Service | 1 | `c14acf3478f4c33f…` |
| T005 | tax | U.S. Internal Revenue Service | 6 | `2d420cbb4123dcf1…` |
| T006 | tax | U.S. Internal Revenue Service | 5 | `92444d8856ce55d9…` |
| T007 | tax | U.S. Internal Revenue Service | 62 | `ddc3bb15e437bd65…` |
| T008 | tax | U.S. Internal Revenue Service | 126 | `482e9c487c608f1b…` |

## A.2 Layout-complexity scores

| ID | Pages | Column count (mean per page) | Form-page fraction | n_blocks (mean) | Complexity |
|---|---|---|---|---|---|
| H001 | 15 | 2.60 | 0.00 | 12.7 | 2.600 |
| H002 | 10 | 2.20 | 0.00 | 6.4 | 2.200 |
| H003 | 3 | 2.00 | 0.00 | 10.7 | 2.000 |
| H004 | 5 | 3.60 | 0.20 | 16.4 | 3.800 |
| IM001 | 12 | 2.67 | 0.92 | 52.5 | 3.583 |
| IM002 | 14 | 3.14 | 0.86 | 29.4 | 4.000 |
| IM003 | 24 | 3.25 | 0.92 | 30.9 | 4.167 |
| IM004 | 7 | 2.71 | 0.86 | 34.3 | 3.571 |
| IM005 | 12 | 2.83 | 0.83 | 28.4 | 3.667 |
| IM006 | 7 | 2.86 | 0.71 | 37.1 | 3.571 |
| IM007 | 4 | 3.00 | 0.75 | 30.2 | 3.750 |
| IM008 | 42 | 2.02 | 0.43 | 19.8 | 2.452 |
| L001 | 118 | 1.31 | 0.00 | 16.7 | 1.305 |
| L002 | 82 | 1.21 | 0.00 | 3.4 | 1.207 |
| L003 | 20 | 1.20 | 0.00 | 17.8 | 1.200 |
| L004 | 119 | 1.19 | 0.00 | 17.3 | 1.193 |
| M001 | 26 | 3.31 | 0.35 | 20.8 | 3.654 |
| M002 | 28 | 3.54 | 0.39 | 22.7 | 3.929 |
| M003 | 36 | 3.28 | 0.56 | 23.5 | 3.833 |
| M004 | 27 | 3.11 | 0.44 | 23.1 | 3.556 |
| M005 | 29 | 3.07 | 0.72 | 47.6 | 3.793 |
| M006 | 16 | 3.56 | 0.50 | 26.1 | 4.062 |
| T001 | 2 | 1.50 | 1.00 | 50.5 | 2.500 |
| T002 | 2 | 3.50 | 0.50 | 27.5 | 4.000 |
| T003 | 142 | 3.31 | 0.52 | 46.9 | 3.831 |
| T004 | 1 | 3.00 | 1.00 | 27.0 | 4.000 |
| T005 | 6 | 3.67 | 0.83 | 29.3 | 4.500 |
| T006 | 5 | 2.80 | 0.60 | 30.2 | 3.400 |
| T007 | 62 | 3.66 | 0.35 | 26.1 | 4.016 |
| T008 | 126 | 3.48 | 0.54 | 33.3 | 4.024 |

## A.3 Per-parser extraction length and latency

| ID | Pages | pdfminer (chars) | pdfplumber (chars) | pdfplumber_tuned (chars) | pymupdf (chars) | pypdf (chars) |
|---|---|---|---|---|---|---|
| H001 | 15 | 32,489 | 32,483 | 32,495 | 32,495 | 32,482 |
| H002 | 10 | 31,346 | 31,347 | 31,347 | 31,324 | 31,334 |
| H003 | 3 | 11,711 | 11,711 | 11,711 | 11,711 | 11,711 |
| H004 | 5 | 28,407 | 28,406 | 28,406 | 28,406 | 28,408 |
| IM001 | 12 | 22,845 | 22,844 | 22,845 | 22,858 | 22,751 |
| IM002 | 14 | 34,446 | 34,446 | 34,446 | 34,444 | 34,299 |
| IM003 | 24 | 53,978 | 53,960 | 53,976 | 53,953 | 53,790 |
| IM004 | 7 | 13,210 | 13,207 | 13,209 | 13,207 | 13,150 |
| IM005 | 12 | 23,599 | 23,592 | 23,598 | 23,598 | 23,540 |
| IM006 | 7 | 13,965 | 13,964 | 13,965 | 13,965 | 13,934 |
| IM007 | 4 | 7,777 | 7,777 | 7,777 | 7,776 | 7,758 |
| IM008 | 42 | 149,835 | 149,777 | 149,840 | 148,373 | 149,865 |
| L001 | 118 | 240,199 | 240,062 | 240,059 | 240,059 | 240,565 |
| L002 | 82 | 167,900 | 167,821 | 167,900 | 167,900 | 168,254 |
| L003 | 20 | 38,212 | 38,214 | 38,189 | 38,189 | 38,255 |
| L004 | 119 | 244,415 | 244,324 | 244,321 | 244,321 | 244,844 |
| M001 | 26 | 121,475 | 121,454 | 121,501 | 121,492 | 121,643 |
| M002 | 28 | 124,965 | 124,851 | 124,990 | 124,897 | 125,113 |
| M003 | 36 | 172,915 | 172,743 | 172,841 | 172,744 | 172,985 |
| M004 | 27 | 114,075 | 113,897 | 114,011 | 113,946 | 114,198 |
| M005 | 29 | 133,780 | 133,744 | 133,839 | 132,882 | 133,940 |
| M006 | 16 | 61,194 | 61,018 | 61,224 | 59,932 | 61,221 |
| T001 | 2 | 10,158 | 10,152 | 10,158 | 10,156 | 10,150 |
| T002 | 2 | 6,848 | 6,844 | 6,847 | 6,848 | 6,848 |
| T003 | 142 | 989,330 | 995,746 | 989,505 | 960,116 | 989,029 |
| T004 | 1 | 3,951 | 3,951 | 3,951 | 3,951 | 3,951 |
| T005 | 6 | 37,723 | 37,689 | 37,724 | 37,690 | 37,689 |
| T006 | 5 | 25,712 | 25,718 | 25,713 | 25,713 | 25,712 |
| T007 | 62 | 291,840 | 291,956 | 291,962 | 279,093 | 292,540 |
| T008 | 126 | 633,178 | 630,533 | 633,784 | 607,529 | 630,287 |

## A.4 Per-doc pairwise CER (all parser pairs)

| ID | pdfplumber↔pdfminer | pdfplumber↔pdfplumber_tuned | pdfplumber↔pypdf | pdfplumber_tuned↔pdfminer | pdfplumber_tuned↔pypdf | pymupdf↔pdfminer | pymupdf↔pdfplumber | pymupdf↔pdfplumber_tuned | pymupdf↔pypdf | pypdf↔pdfminer |
|---|---|---|---|---|---|---|---|---|---|---|
| H001 | 0.026 | 0.048 | 0.048 | 0.068 | 0.000 | 0.068 | 0.048 | 0.000 | 0.000 | 0.068 |
| H002 | 0.013 | 0.040 | 0.041 | 0.039 | 0.001 | 0.040 | 0.041 | 0.001 | 0.000 | 0.040 |
| H003 | 0.033 | 0.027 | 0.027 | 0.027 | 0.000 | 0.027 | 0.027 | 0.000 | 0.000 | 0.027 |
| H004 | 0.670 | 0.684 | 0.684 | 0.052 | 0.000 | 0.052 | 0.684 | 0.000 | 0.000 | 0.052 |
| IM001 | 0.481 | 0.615 | 0.616 | 0.471 | 0.004 | 0.472 | 0.615 | 0.001 | 0.005 | 0.471 |
| IM002 | 0.068 | 0.438 | 0.439 | 0.429 | 0.004 | 0.429 | 0.438 | 0.000 | 0.004 | 0.428 |
| IM003 | 0.048 | 0.328 | 0.327 | 0.328 | 0.004 | 0.327 | 0.327 | 0.001 | 0.004 | 0.326 |
| IM004 | 0.468 | 0.595 | 0.597 | 0.524 | 0.004 | 0.524 | 0.595 | 0.000 | 0.005 | 0.523 |
| IM005 | 0.057 | 0.363 | 0.363 | 0.363 | 0.003 | 0.363 | 0.363 | 0.000 | 0.003 | 0.363 |
| IM006 | 0.441 | 0.593 | 0.593 | 0.537 | 0.002 | 0.537 | 0.593 | 0.000 | 0.002 | 0.537 |
| IM007 | 0.361 | 0.505 | 0.505 | 0.451 | 0.002 | 0.451 | 0.505 | 0.000 | 0.003 | 0.451 |
| IM008 | 0.097 | 0.021 | 0.022 | 0.099 | 0.000 | 0.090 | 0.012 | 0.011 | 0.011 | 0.099 |
| L001 | 0.003 | 0.003 | 0.005 | 0.006 | 0.002 | 0.010 | 0.007 | 0.004 | 0.006 | 0.007 |
| L002 | 0.001 | 0.001 | 0.003 | 0.001 | 0.002 | 0.001 | 0.001 | 0.000 | 0.002 | 0.003 |
| L003 | 0.002 | 0.008 | 0.009 | 0.008 | 0.002 | 0.013 | 0.012 | 0.004 | 0.006 | 0.010 |
| L004 | 0.000 | 0.003 | 0.005 | 0.003 | 0.002 | 0.007 | 0.007 | 0.004 | 0.006 | 0.005 |
| M001 | 0.613 | 0.569 | 0.569 | 0.117 | 0.001 | 0.118 | 0.569 | 0.001 | 0.002 | 0.118 |
| M002 | 0.606 | 0.537 | 0.537 | 0.164 | 0.003 | 0.165 | 0.537 | 0.002 | 0.003 | 0.166 |
| M003 | 0.601 | 0.580 | 0.581 | 0.121 | 0.002 | 0.122 | 0.581 | 0.001 | 0.002 | 0.123 |
| M004 | 0.637 | 0.642 | 0.643 | 0.158 | 0.004 | 0.158 | 0.643 | 0.002 | 0.004 | 0.160 |
| M005 | 0.568 | 0.514 | 0.515 | 0.177 | 0.002 | 0.178 | 0.519 | 0.009 | 0.010 | 0.178 |
| M006 | 0.625 | 0.632 | 0.635 | 0.127 | 0.006 | 0.138 | 0.648 | 0.022 | 0.022 | 0.130 |
| T001 | 0.472 | 0.202 | 0.201 | 0.407 | 0.001 | 0.407 | 0.202 | 0.000 | 0.001 | 0.407 |
| T002 | 0.328 | 0.151 | 0.151 | 0.257 | 0.000 | 0.256 | 0.151 | 0.000 | 0.000 | 0.256 |
| T003 | 0.687 | 0.691 | 0.691 | 0.165 | 0.006 | 0.179 | 0.694 | 0.030 | 0.036 | 0.169 |
| T004 | 0.342 | 0.163 | 0.163 | 0.293 | 0.000 | 0.293 | 0.163 | 0.000 | 0.000 | 0.293 |
| T005 | 0.663 | 0.660 | 0.660 | 0.033 | 0.001 | 0.032 | 0.660 | 0.001 | 0.000 | 0.032 |
| T006 | 0.435 | 0.293 | 0.293 | 0.159 | 0.000 | 0.159 | 0.293 | 0.000 | 0.000 | 0.159 |
| T007 | 0.635 | 0.625 | 0.626 | 0.090 | 0.005 | 0.129 | 0.638 | 0.044 | 0.048 | 0.093 |
| T008 | 0.614 | 0.586 | 0.585 | 0.225 | 0.008 | 0.257 | 0.604 | 0.041 | 0.049 | 0.231 |

## A.5 Source URLs (for reproducibility)

| ID | Source URL |
|---|---|
| H001 | https://www.hud.gov/sites/dfiles/OCHCO/documents/90105a.pdf |
| H002 | https://www.hud.gov/sites/dfiles/OCHCO/documents/90105b.pdf |
| H003 | https://www.hud.gov/sites/dfiles/OCHCO/documents/52646.pdf |
| H004 | https://www.hud.gov/sites/dfiles/OCHCO/documents/52641A.pdf |
| IM001 | https://www.uscis.gov/sites/default/files/document/forms/i-130.pdf |
| IM002 | https://www.uscis.gov/sites/default/files/document/forms/n-400.pdf |
| IM003 | https://www.uscis.gov/sites/default/files/document/forms/i-485.pdf |
| IM004 | https://www.uscis.gov/sites/default/files/document/forms/i-765.pdf |
| IM005 | https://www.uscis.gov/sites/default/files/document/forms/i-864.pdf |
| IM006 | https://www.uscis.gov/sites/default/files/document/forms/i-90.pdf |
| IM007 | https://www.uscis.gov/sites/default/files/document/forms/g-28.pdf |
| IM008 | https://www.uscis.gov/sites/default/files/document/forms/i-485instr.pdf |
| L001 | https://www.supremecourt.gov/opinions/24pdf/23-477_2cp3.pdf |
| L002 | https://www.supremecourt.gov/opinions/24pdf/22-7466_5h25.pdf |
| L003 | https://www.supremecourt.gov/opinions/23pdf/23-719_19m2.pdf |
| L004 | https://www.supremecourt.gov/opinions/23pdf/23-939_e2pg.pdf |
| M001 | https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7301-H.pdf |
| M002 | https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7309-H.pdf |
| M003 | https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7315-H.pdf |
| M004 | https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7316-H.pdf |
| M005 | https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7341-H.pdf |
| M006 | https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7350-H.pdf |
| T001 | https://www.irs.gov/pub/irs-pdf/f1040.pdf |
| T002 | https://www.irs.gov/pub/irs-pdf/f1040sc.pdf |
| T003 | https://www.irs.gov/pub/irs-pdf/p17.pdf |
| T004 | https://www.irs.gov/pub/irs-pdf/f1040sa.pdf |
| T005 | https://www.irs.gov/pub/irs-pdf/fw9.pdf |
| T006 | https://www.irs.gov/pub/irs-pdf/fw4.pdf |
| T007 | https://www.irs.gov/pub/irs-pdf/p463.pdf |
| T008 | https://www.irs.gov/pub/irs-pdf/i1040gi.pdf |
