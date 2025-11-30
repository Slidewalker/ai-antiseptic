# antiseptic/rag.py
import os
from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings, HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# Default directories
DEFAULT_SOURCES_DIR = Path("sources")
DEFAULT_DB_DIR = Path(".chroma")

def load_documents(sources_dir: str | Path = DEFAULT_SOURCES_DIR) -> List:
    """Load all supported documents from the sources directory."""
    sources_dir = Path(sources_dir)
    docs = []
    for file_path in sources_dir.iterdir():
        if not file_path.is_file():
            continue
        try:
            if file_path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_path.suffix.lower() in {".txt", ".md", ".markdown"}:
                if file_path.suffix.lower() in {".md", ".markdown"}:
                    loader = UnstructuredMarkdownLoader(str(file_path))
                else:
                    loader = TextLoader(str(file_path), encoding="utf-8")
            else:
                continue  # skip unsupported files
            docs.extend(loader.load())
            print(f"Loaded: {file_path.name}")
        except Exception as e:
            print(f"Failed to load {file_path.name}: {e}")
    return docs

def create_vectorstore(
    documents,
    embedding_model: Optional[str] = None,
    persist_directory: str | Path = DEFAULT_DB_DIR,
):
    """Create (or update) Chroma vector store with smart embedding choice."""
    persist_directory = Path(persist_directory)
    persist_directory.mkdir(parents=True, exist_ok=True)

    # Choose embeddings (offline first)
    if os.getenv("LLM_PROVIDER") in {"ollama", None} or not os.getenv("OPENAI_API_KEY"):
        embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
        print("Using Ollama embeddings (fully offline)")
    elif embedding_model and "openai" in embedding_model.lower():
        embeddings = OpenAIEmbeddings()
        print("Using OpenAI embeddings")
    else:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        print("Using local HuggingFace embeddings")

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    splits = text_splitter.split_documents(documents)

    # Build / update vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(persist_directory),
    )
    print(f"Vector store created/updated with {len(splits)} chunks → {persist_directory}")
    return vectorstore

def get_retriever(k: int = 6):
    """Return a ready-to-use retriever from the persisted Chroma DB."""
    if not DEFAULT_DB_DIR.exists():
        raise FileNotFoundError("No vector database found. Run build_rag() first.")

    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest") \
        if os.getenv("LLM_PROVIDER") in {"ollama", None} else OpenAIEmbeddings()

    vectorstore = Chroma(persist_directory=str(DEFAULT_DB_DIR), embedding_function=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": k})

def build_rag(sources_dir: str | Path = DEFAULT_SOURCES_DIR):
    """One-call function to build the full RAG index from sources."""
    docs = load_documents(sources_dir)
    if not docs:
        raise ValueError("No documents loaded. Check your sources/ folder.")
    vectorstore = create_vectorstore(docs)
    return vectorstore.as_retriever(search_kwargs={"k": 6})
