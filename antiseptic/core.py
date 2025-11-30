from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings, HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

load_dotenv()

def build_antiseptic_chain(sources_dir="sources"):
    # Load all documents
    docs = []
    for file in os.listdir(sources_dir):
        path = os.path.join(sources_dir, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif file.endswith(".txt"):
            loader = TextLoader(path, encoding="utf-8")
        elif file.endswith(".md"):
            loader = UnstructuredMarkdownLoader(path)
        else:
            continue
        docs.extend(loader.load())

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Embeddings (offline-first)
    if os.getenv("LLM_PROVIDER") == "ollama" or not os.getenv("OPENAI_API_KEY"):
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
    else:
        embeddings = OpenAIEmbeddings()

    # Vectorstore
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=".chroma")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    # Prompt
    template = """You are AI Antiseptic. Answer ONLY using the context below.
    If the answer is not in the context, say "Not found in sources."

    Context:
    {context}

    Question: {question}
    Answer with citations (Source: page X or filename)."""
    prompt = ChatPromptTemplate.from_template(template)

    # LLM selection
    from langchain_openai import ChatOpenAI
    from langchain_ollama import ChatOllama
    from langchain_anthropic import ChatAnthropic
    from langchain_google_genai import ChatGoogleGenerativeAI

    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    model = os.getenv("MODEL_NAME", "llama3.2:8b")

    if provider == "openai":
        llm = ChatOpenAI(model=model, temperature=0)
    elif provider == "groq":
        from langchain_groq import ChatGroq
        llm = ChatGroq(model=model, temperature=0)
    elif provider == "anthropic":
        llm = ChatAnthropic(model=model, temperature=0)
    elif provider == "gemini":
        llm = ChatGoogleGenerativeAI(model=model, temperature=0)
    else:
        llm = ChatOllama(model=model, temperature=0)

    # Chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
