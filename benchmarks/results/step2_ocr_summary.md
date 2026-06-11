# Step 2 — OCR eval (synthetic scans)

Records: 30

## Tier: `high`

| Engine | Layout | mean CER | mean WER | p50 latency (ms) |
|---|---|---|---|---|
| tesseract | simple | 0.0491 | 0.0349 | 1570.8 |
| tesseract | two_column | 0.0497 | 0.0405 | 1545.1 |
| tesseract | with_table | 0.2559 | 0.2787 | 1676.1 |

## Tier: `low`

| Engine | Layout | mean CER | mean WER | p50 latency (ms) |
|---|---|---|---|---|
| tesseract | simple | 0.0508 | 0.0467 | 531.1 |
| tesseract | two_column | 0.0491 | 0.0350 | 534.3 |
| tesseract | with_table | 0.2596 | 0.2796 | 592.0 |
