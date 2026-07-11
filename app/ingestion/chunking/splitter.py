from typing import List
import logfire
from app.config import settings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings  

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

semantic_chunker = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=90,
)

def chunk_text(text: str) -> List[str]:
    """
    Performs semantic chunking using LangChain's SemanticChunker.

    Returns:
        List[str]: A list of semantically coherent text chunks.
    """
    with logfire.span("✂️ Semantic Chunking", text_length=len(text)):
        if not text.strip():
            logfire.warning("⚠️ Empty text received for chunking.")
            return []

        try:
            documents = semantic_chunker.create_documents([text])
            chunks = [doc.page_content.strip() for doc in documents if doc.page_content.strip()]

            logfire.info(
                f"✅ Generated {len(chunks)} semantic chunks "
                f"(avg_size={sum(len(c) for c in chunks) / max(len(chunks), 1):.0f} chars)"
            )

            return chunks

        except Exception as e:
            logfire.error(f"❌ Semantic Chunking Failed: {e}")
            raise