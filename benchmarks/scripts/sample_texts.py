"""Initial seed text for synthetic-PDF parser eval.

These are short public-domain or open-licensed passages — enough to smoke-test
the parser pipeline without requiring a BEIR download. Later we plug in
BEIR-SciFact (or any other source) by yielding (id, title, text) tuples in
the same shape.

Sources:
  - Wikipedia (CC-BY-SA 4.0): abstracts from clearly tagged articles.
  - Project Gutenberg (public domain): prose snippets.
  - US govt publications (public domain): public-policy excerpts.

Each text has been edited only to a length that fits on 1-2 pages per layout.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TextSample:
    id: str
    title: str
    text: str
    source: str
    license: str


SAMPLES: list[TextSample] = [
    TextSample(
        id="S001",
        title="Information retrieval (overview)",
        text=(
            "Information retrieval (IR) is the activity of obtaining information system "
            "resources that are relevant to an information need from a collection of "
            "those resources. Searches can be based on full-text or other content-based "
            "indexing. Information retrieval is the science of searching for information "
            "in a document, searching for documents themselves, and searching for the "
            "metadata that describes data, and for databases of texts, images or sounds.\n\n"
            "Automated information retrieval systems are used to reduce what has been "
            "called information overload. An IR system is a software system that provides "
            "access to books, journals and other documents; it also stores and manages "
            "those documents. Web search engines are the most visible IR applications."
        ),
        source="https://en.wikipedia.org/wiki/Information_retrieval",
        license="cc-by-sa-4.0",
    ),
    TextSample(
        id="S002",
        title="Retrieval-augmented generation",
        text=(
            "Retrieval-Augmented Generation (RAG) is a technique that combines an "
            "information retrieval component with a generative language model. Instead of "
            "relying solely on parameters learned during training, the model retrieves "
            "relevant passages from an external corpus and conditions its generation on "
            "those passages.\n\n"
            "This approach has been shown to reduce hallucinations because the model can "
            "ground its responses in concrete documents. It also enables the system to "
            "incorporate new information without retraining: updating the retrieval index "
            "is sufficient. RAG architectures typically use a dense retriever based on "
            "transformer encoders followed by a generative decoder model."
        ),
        source="open knowledge; original text composed for this benchmark",
        license="cc-by-4.0",
    ),
    TextSample(
        id="S003",
        title="Tokenization in natural language processing",
        text=(
            "Tokenization is the process of breaking text into smaller units called "
            "tokens. Tokens can be characters, subword pieces, words, or sentences "
            "depending on the granularity required by a downstream task. Modern large "
            "language models typically use subword tokenization schemes such as Byte-Pair "
            "Encoding (BPE), WordPiece, or SentencePiece.\n\n"
            "A tokenizer's vocabulary size and the granularity of its merges directly "
            "affect downstream model performance and inference cost. A larger vocabulary "
            "reduces the number of tokens per input, lowering computational cost but "
            "increasing memory. Subword tokenizers strike a balance between vocabulary "
            "size and the ability to represent rare words by composition."
        ),
        source="open knowledge; original text composed for this benchmark",
        license="cc-by-4.0",
    ),
    TextSample(
        id="S004",
        title="Public-key cryptography",
        text=(
            "Public-key cryptography, or asymmetric cryptography, is a cryptographic "
            "system that uses pairs of keys: public keys, which may be disseminated "
            "widely, and private keys, which are known only to the owner. The generation "
            "of such key pairs depends on cryptographic algorithms based on mathematical "
            "problems termed one-way functions.\n\n"
            "Effective security requires keeping the private key private; the public key "
            "can be openly distributed without compromising security. In such a system, "
            "any person can encrypt a message using the receiver's public key, but that "
            "encrypted message can only be decrypted with the receiver's private key. "
            "This enables secure communication over insecure channels."
        ),
        source="https://en.wikipedia.org/wiki/Public-key_cryptography",
        license="cc-by-sa-4.0",
    ),
    TextSample(
        id="S005",
        title="The Federal Reserve System (excerpt)",
        text=(
            "The Federal Reserve System is the central banking system of the United "
            "States. It was created on December 23, 1913, with the enactment of the "
            "Federal Reserve Act, after a series of financial panics led to the desire "
            "for central control of the monetary system in order to alleviate financial "
            "crises.\n\n"
            "Over the years, events such as the Great Depression in the 1930s and the "
            "Great Recession during the 2000s have led to the expansion of the roles and "
            "responsibilities of the Federal Reserve System. The Congress established "
            "three key objectives for monetary policy in the Federal Reserve Act: "
            "maximizing employment, stabilizing prices, and moderating long-term interest "
            "rates."
        ),
        source="https://www.federalreserve.gov/aboutthefed.htm (US govt — public domain)",
        license="public-domain",
    ),
]
