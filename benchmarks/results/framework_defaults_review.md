# Framework Defaults Review

**Reviewed:** 2026-06-11. We read the `main`-branch source of each framework's PDF document loader to determine which underlying text-extraction library is invoked when a user calls the most-documented ingestion API without specifying a backend.

## LangChain (langchain-community)

- **Conventional API:** `PyPDFLoader`
- **Underlying parser:** `pypdf` (via `PyPDFParser`)
- **Cluster (this paper):** A
- **Source location:** `libs/community/langchain_community/document_loaders/pdf.py` → `PyPDFLoader` → `PyPDFParser` in `libs/community/langchain_community/document_loaders/parsers/pdf.py`
- **Alternatives in tree:** `PyMuPDFLoader` (PyMuPDF → A), `PDFPlumberLoader` (pdfplumber default → C), `PDFMinerLoader` (pdfminer → B), `PyPDFium2Loader`, `UnstructuredPDFLoader`

## LlamaIndex (llama-index-readers-file)

- **Conventional API:** `SimpleDirectoryReader` → consults `default_file_reader_cls` dict
- **Default for `.pdf`:** `PDFReader` (from `llama_index.readers.file`)
- **Underlying parser inside PDFReader:** `pypdf` — verified by reading `llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/docs/base.py`, which imports `pypdf` and instantiates `pypdf.PdfReader`
- **Cluster (this paper):** A
- **Source location of mapping:** `llama-index-core/llama_index/core/readers/file/base.py`
- **Alternatives in tree:** `PyMuPDFReader` (PyMuPDF → A); user must instantiate it explicitly

## Haystack (deepset-ai/haystack)

- **Conventional API:** `PDFMinerToDocument`
- **Underlying parser:** `pdfminer.six` — verified in `haystack/components/converters/pdfminer.py`, which imports `pdfminer.high_level.extract_pages` and `pdfminer.layout`
- **Cluster (this paper):** B
- **Note:** the prior `PDFToTextConverter` from Haystack 1.x was deprecated and replaced by `PDFMinerToDocument` in Haystack 2.x. No other in-tree PDF text converter ships in the components/converters tree at time of writing.

## Cluster summary

| Framework | Default parser | Cluster | Implication |
|---|---|---|---|
| LangChain `PyPDFLoader` | pypdf | A | Agrees with PyMuPDF / tuned pdfplumber |
| LlamaIndex `PDFReader` | pypdf | A | Same |
| Haystack `PDFMinerToDocument` | pdfminer.six | B | Disagrees with Cluster A at CER ≈ 0.20 |

**No framework defaults to pdfplumber.** Cluster C divergence is opt-in: practitioners hit it when they explicitly select `PDFPlumberLoader` (LangChain) or wrap pdfplumber for its table-extraction capabilities.

## Limitations of this review

- We did not exhaustively review every plugin/integration in each ecosystem. Third-party readers (e.g., LlamaHub plugins, Haystack community connectors) may select different parsers.
- Frameworks evolve rapidly; the cluster assignment is stable as long as each framework's default does not change. Commit hashes are not pinned because each framework's tutorial-recommended loader has been stable for multiple minor releases.
- We treat the *default* invocation only. Power users routinely swap in PyMuPDF, pdfplumber, or pdfminer regardless of the framework default.
