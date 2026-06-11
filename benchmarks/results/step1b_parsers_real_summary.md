# Step 1.B — PDF parser eval on real public-domain US-govt PDFs

## Per-parser totals (across all docs)

| Parser | Total chars | Mean chars/page | p50 latency (ms) | p95 latency (ms) |
|---|---|---|---|---|
| pymupdf | 3,769,568 | 3,577 | 91.1 | 97.0 |
| pdfplumber | 3,844,231 | 3,602 | 2010.5 | 2039.0 |
| pdfplumber_tuned | 3,842,134 | 3,603 | 1984.5 | 2004.8 |
| pypdf | 3,840,246 | 3,602 | 424.6 | 504.9 |
| pdfminer | 3,841,478 | 3,603 | 1304.7 | 1336.6 |

## Per-doc extraction length (chars)

| Doc | Pages | pymupdf | pdfplumber | pdfplumber_tuned | pypdf | pdfminer | min/max ratio |
|---|---|---|---|---|---|---|---|
| H001 | 15 | 32,495 | 32,483 | 32,495 | 32,482 | 32,489 | 1.000 |
| H002 | 10 | 31,324 | 31,347 | 31,347 | 31,334 | 31,346 | 0.999 |
| H003 | 3 | 11,711 | 11,711 | 11,711 | 11,711 | 11,711 | 1.000 |
| H004 | 5 | 28,406 | 28,406 | 28,406 | 28,408 | 28,407 | 1.000 |
| IM001 | 12 | 22,858 | 22,844 | 22,845 | 22,751 | 22,845 | 0.995 |
| IM002 | 14 | 34,444 | 34,446 | 34,446 | 34,299 | 34,446 | 0.996 |
| IM003 | 24 | 53,953 | 53,960 | 53,976 | 53,790 | 53,978 | 0.997 |
| IM004 | 7 | 13,207 | 13,207 | 13,209 | 13,150 | 13,210 | 0.995 |
| IM005 | 12 | 23,598 | 23,592 | 23,598 | 23,540 | 23,599 | 0.997 |
| IM006 | 7 | 13,965 | 13,964 | 13,965 | 13,934 | 13,965 | 0.998 |
| IM007 | 4 | 7,776 | 7,777 | 7,777 | 7,758 | 7,777 | 0.998 |
| IM008 | 42 | 148,373 | 149,777 | 149,840 | 149,865 | 149,835 | 0.990 |
| L001 | 118 | 240,059 | 240,062 | 240,059 | 240,565 | 240,199 | 0.998 |
| L002 | 82 | 167,900 | 167,821 | 167,900 | 168,254 | 167,900 | 0.997 |
| L003 | 20 | 38,189 | 38,214 | 38,189 | 38,255 | 38,212 | 0.998 |
| L004 | 119 | 244,321 | 244,324 | 244,321 | 244,844 | 244,415 | 0.998 |
| M001 | 26 | 121,492 | 121,454 | 121,501 | 121,643 | 121,475 | 0.998 |
| M002 | 28 | 124,897 | 124,851 | 124,990 | 125,113 | 124,965 | 0.998 |
| M003 | 36 | 172,744 | 172,743 | 172,841 | 172,985 | 172,915 | 0.999 |
| M004 | 27 | 113,946 | 113,897 | 114,011 | 114,198 | 114,075 | 0.997 |
| M005 | 29 | 132,882 | 133,744 | 133,839 | 133,940 | 133,780 | 0.992 |
| M006 | 16 | 59,932 | 61,018 | 61,224 | 61,221 | 61,194 | 0.979 |
| T001 | 2 | 10,156 | 10,152 | 10,158 | 10,150 | 10,158 | 0.999 |
| T002 | 2 | 6,848 | 6,844 | 6,847 | 6,848 | 6,848 | 0.999 |
| T003 | 142 | 960,116 | 995,746 | 989,505 | 989,029 | 989,330 | 0.964 |
| T004 | 1 | 3,951 | 3,951 | 3,951 | 3,951 | 3,951 | 1.000 |
| T005 | 6 | 37,690 | 37,689 | 37,724 | 37,689 | 37,723 | 0.999 |
| T006 | 5 | 25,713 | 25,718 | 25,713 | 25,712 | 25,712 | 1.000 |
| T007 | 62 | 279,093 | 291,956 | 291,962 | 292,540 | 291,840 | 0.954 |
| T008 | 126 | 607,529 | 630,533 | 633,784 | 630,287 | 633,178 | 0.959 |

## Pairwise inter-parser agreement (mean over docs, 95% bootstrap CI)

Bootstrap: 10,000 resamples of doc-level metrics, percentile method.

| Pair | mean CER [95% CI] | mean WER [95% CI] | mean length ratio | docs |
|---|---|---|---|---|
| pdfplumber vs pdfminer | 0.3532  [0.2575, 0.4458] | 0.4304  [0.3147, 0.5431] | 0.999 | 30 |
| pdfplumber vs pdfplumber_tuned | 0.3705  [0.2767, 0.4599] | 0.4390  [0.3229, 0.5519] | 0.999 | 30 |
| pdfplumber vs pypdf | 0.3712  [0.2774, 0.4606] | 0.4464  [0.3305, 0.5584] | 0.998 | 30 |
| pdfplumber_tuned vs pdfminer | 0.1966  [0.1395, 0.2576] | 0.2472  [0.1768, 0.3209] | 1.000 | 30 |
| pdfplumber_tuned vs pypdf | 0.0024  [0.0017, 0.0032] | 0.0255  [0.0186, 0.0325] | 0.998 | 30 |
| pymupdf vs pdfminer | 0.2001  [0.1433, 0.2605] | 0.2529  [0.1841, 0.3256] | 0.995 | 30 |
| pymupdf vs pdfplumber | 0.3726  [0.2783, 0.4630] | 0.4434  [0.3278, 0.5555] | 0.995 | 30 |
| pymupdf vs pdfplumber_tuned | 0.0060  [0.0022, 0.0106] | 0.0109  [0.0065, 0.0158] | 0.995 | 30 |
| pymupdf vs pypdf | 0.0078  [0.0037, 0.0129] | 0.0309  [0.0220, 0.0401] | 0.994 | 30 |
| pypdf vs pdfminer | 0.1975  [0.1408, 0.2583] | 0.2570  [0.1890, 0.3281] | 0.998 | 30 |

## Paired bootstrap: per-pair CER differences (10,000 resamples)

Same doc set, paired by doc_id. p two-sided.

| Pair X | Pair Y | mean(X − Y) [95% CI] | p |
|---|---|---|---|
| pdfplumber vs pdfminer | pdfplumber vs pdfplumber_tuned | -0.0173  [-0.0676, 0.0294] | 0.4944 |
| pdfplumber vs pdfminer | pdfplumber vs pypdf | -0.0180  [-0.0684, 0.0288] | 0.4800 |
| pdfplumber vs pdfminer | pdfplumber_tuned vs pdfminer | 0.1566  [0.0545, 0.2604] | 0.0034 |
| pdfplumber vs pdfminer | pdfplumber_tuned vs pypdf | 0.3507  [0.2551, 0.4432] | 0.0001 |
| pdfplumber vs pdfminer | pymupdf vs pdfminer | 0.1531  [0.0526, 0.2554] | 0.0038 |
| pdfplumber vs pdfminer | pymupdf vs pdfplumber | -0.0194  [-0.0694, 0.0277] | 0.4460 |
| pdfplumber vs pdfminer | pymupdf vs pdfplumber_tuned | 0.3472  [0.2529, 0.4378] | 0.0001 |
| pdfplumber vs pdfminer | pymupdf vs pypdf | 0.3454  [0.2510, 0.4359] | 0.0001 |
| pdfplumber vs pdfminer | pypdf vs pdfminer | 0.1557  [0.0539, 0.2590] | 0.0034 |
| pdfplumber vs pdfplumber_tuned | pdfplumber vs pypdf | -0.0007  [-0.0010, -0.0004] | 0.0001 |
| pdfplumber vs pdfplumber_tuned | pdfplumber_tuned vs pdfminer | 0.1739  [0.0873, 0.2647] | 0.0001 |
| pdfplumber vs pdfplumber_tuned | pdfplumber_tuned vs pypdf | 0.3681  [0.2745, 0.4570] | 0.0001 |
| pdfplumber vs pdfplumber_tuned | pymupdf vs pdfminer | 0.1705  [0.0850, 0.2598] | 0.0001 |
| pdfplumber vs pdfplumber_tuned | pymupdf vs pdfplumber | -0.0020  [-0.0040, -0.0003] | 0.0146 |
| pdfplumber vs pdfplumber_tuned | pymupdf vs pdfplumber_tuned | 0.3645  [0.2719, 0.4524] | 0.0001 |
| pdfplumber vs pdfplumber_tuned | pymupdf vs pypdf | 0.3627  [0.2705, 0.4504] | 0.0001 |
| pdfplumber vs pdfplumber_tuned | pypdf vs pdfminer | 0.1730  [0.0866, 0.2634] | 0.0001 |
| pdfplumber vs pypdf | pdfplumber_tuned vs pdfminer | 0.1746  [0.0879, 0.2653] | 0.0001 |
| pdfplumber vs pypdf | pdfplumber_tuned vs pypdf | 0.3688  [0.2752, 0.4578] | 0.0001 |
| pdfplumber vs pypdf | pymupdf vs pdfminer | 0.1711  [0.0857, 0.2604] | 0.0001 |
| pdfplumber vs pypdf | pymupdf vs pdfplumber | -0.0014  [-0.0033, 0.0003] | 0.1202 |
| pdfplumber vs pypdf | pymupdf vs pdfplumber_tuned | 0.3652  [0.2727, 0.4531] | 0.0001 |
| pdfplumber vs pypdf | pymupdf vs pypdf | 0.3634  [0.2713, 0.4510] | 0.0001 |
| pdfplumber vs pypdf | pypdf vs pdfminer | 0.1737  [0.0873, 0.2641] | 0.0001 |
| pdfplumber_tuned vs pdfminer | pdfplumber_tuned vs pypdf | 0.1942  [0.1374, 0.2550] | 0.0001 |
| pdfplumber_tuned vs pdfminer | pymupdf vs pdfminer | -0.0035  [-0.0072, -0.0006] | 0.0094 |
| pdfplumber_tuned vs pdfminer | pymupdf vs pdfplumber | -0.1760  [-0.2674, -0.0883] | 0.0001 |
| pdfplumber_tuned vs pdfminer | pymupdf vs pdfplumber_tuned | 0.1906  [0.1326, 0.2524] | 0.0001 |
| pdfplumber_tuned vs pdfminer | pymupdf vs pypdf | 0.1888  [0.1311, 0.2502] | 0.0001 |
| pdfplumber_tuned vs pdfminer | pypdf vs pdfminer | -0.0009  [-0.0015, -0.0004] | 0.0006 |
| pdfplumber_tuned vs pypdf | pymupdf vs pdfminer | -0.1976  [-0.2577, -0.1410] | 0.0001 |
| pdfplumber_tuned vs pypdf | pymupdf vs pdfplumber | -0.3701  [-0.4600, -0.2763] | 0.0001 |
| pdfplumber_tuned vs pypdf | pymupdf vs pdfplumber_tuned | -0.0035  [-0.0077, -0.0001] | 0.0380 |
| pdfplumber_tuned vs pypdf | pymupdf vs pypdf | -0.0054  [-0.0100, -0.0017] | 0.0001 |
| pdfplumber_tuned vs pypdf | pypdf vs pdfminer | -0.1951  [-0.2557, -0.1384] | 0.0001 |
| pymupdf vs pdfminer | pymupdf vs pdfplumber | -0.1725  [-0.2622, -0.0860] | 0.0001 |
| pymupdf vs pdfminer | pymupdf vs pdfplumber_tuned | 0.1941  [0.1366, 0.2555] | 0.0001 |
| pymupdf vs pdfminer | pymupdf vs pypdf | 0.1923  [0.1350, 0.2533] | 0.0001 |
| pymupdf vs pdfminer | pypdf vs pdfminer | 0.0025  [0.0000, 0.0058] | 0.0446 |
| pymupdf vs pdfplumber | pymupdf vs pdfplumber_tuned | 0.3666  [0.2734, 0.4549] | 0.0001 |
| pymupdf vs pdfplumber | pymupdf vs pypdf | 0.3648  [0.2718, 0.4528] | 0.0001 |
| pymupdf vs pdfplumber | pypdf vs pdfminer | 0.1751  [0.0877, 0.2663] | 0.0001 |
| pymupdf vs pdfplumber_tuned | pymupdf vs pypdf | -0.0018  [-0.0026, -0.0011] | 0.0001 |
| pymupdf vs pdfplumber_tuned | pypdf vs pdfminer | -0.1915  [-0.2529, -0.1337] | 0.0001 |
| pymupdf vs pypdf | pypdf vs pdfminer | -0.1897  [-0.2510, -0.1322] | 0.0001 |

## Per-category pairwise CER (mean, 95% bootstrap CI)

| Category | n | pdfplumber vs pdfminer | pdfplumber vs pdfplumber_tuned | pdfplumber vs pypdf | pdfplumber_tuned vs pdfminer | pdfplumber_tuned vs pypdf | pymupdf vs pdfminer | pymupdf vs pdfplumber | pymupdf vs pdfplumber_tuned | pymupdf vs pypdf | pypdf vs pdfminer |
|---|---|---|---|---|---|---|---|---|---|---|---|
| housing | 4 | 0.186  [0.018, 0.509] | 0.200  [0.032, 0.523] | 0.200  [0.032, 0.523] | 0.047  [0.033, 0.061] | 0.000  [0.000, 0.001] | 0.047  [0.033, 0.061] | 0.200  [0.032, 0.523] | 0.000  [0.000, 0.001] | 0.000  [0.000, 0.000] | 0.047  [0.033, 0.061] |
| immigration | 8 | 0.253  [0.116, 0.383] | 0.432  [0.289, 0.548] | 0.433  [0.289, 0.548] | 0.400  [0.295, 0.481] | 0.003  [0.002, 0.004] | 0.399  [0.292, 0.481] | 0.431  [0.285, 0.548] | 0.002  [0.000, 0.004] | 0.005  [0.003, 0.007] | 0.400  [0.295, 0.481] |
| legal | 4 | 0.002  [0.001, 0.003] | 0.004  [0.001, 0.006] | 0.006  [0.003, 0.008] | 0.005  [0.002, 0.007] | 0.002  [0.002, 0.002] | 0.008  [0.003, 0.011] | 0.007  [0.002, 0.011] | 0.003  [0.001, 0.004] | 0.005  [0.003, 0.006] | 0.006  [0.004, 0.009] |
| medical | 6 | 0.608  [0.590, 0.625] | 0.579  [0.544, 0.616] | 0.580  [0.544, 0.618] | 0.144  [0.127, 0.163] | 0.003  [0.002, 0.005] | 0.146  [0.129, 0.164] | 0.583  [0.546, 0.622] | 0.006  [0.001, 0.013] | 0.007  [0.003, 0.013] | 0.146  [0.128, 0.164] |
| tax | 8 | 0.522  [0.424, 0.615] | 0.421  [0.262, 0.584] | 0.421  [0.262, 0.584] | 0.203  [0.127, 0.285] | 0.003  [0.001, 0.005] | 0.214  [0.140, 0.289] | 0.426  [0.262, 0.591] | 0.015  [0.004, 0.029] | 0.017  [0.004, 0.033] | 0.205  [0.130, 0.285] |

## Per-doc pairwise CER (where do parsers disagree most?)

| Doc | pdfplumber vs pdfminer | pdfplumber vs pdfplumber_tuned | pdfplumber vs pypdf | pdfplumber_tuned vs pdfminer | pdfplumber_tuned vs pypdf | pymupdf vs pdfminer | pymupdf vs pdfplumber | pymupdf vs pdfplumber_tuned | pymupdf vs pypdf | pypdf vs pdfminer |
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