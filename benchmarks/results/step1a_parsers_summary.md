# Step 1.A — PDF parser eval (synthetic PDFs)

Records: 45

## Layout: `simple`

| Parser | mean CER | mean WER | p50 latency (ms) |
|---|---|---|---|
| pdfplumber | 0.0488 | 0.0330 | 6.6 |
| pymupdf | 0.0488 | 0.0330 | 1.1 |
| pypdf | 0.0488 | 0.0330 | 0.6 |

## Layout: `two_column`

| Parser | mean CER | mean WER | p50 latency (ms) |
|---|---|---|---|
| pdfplumber | 0.0488 | 0.0330 | 6.2 |
| pymupdf | 0.0488 | 0.0330 | 1.0 |
| pypdf | 0.0488 | 0.0330 | 0.6 |

## Layout: `with_table`

| Parser | mean CER | mean WER | p50 latency (ms) |
|---|---|---|---|
| pdfplumber | 0.0413 | 0.0285 | 7.7 |
| pymupdf | 0.0413 | 0.0285 | 1.1 |
| pypdf | 0.0413 | 0.0285 | 0.9 |
