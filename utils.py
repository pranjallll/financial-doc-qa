import pdfplumber
import pandas as pd
import io
import ollama
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import streamlit as st

# Load embeddings model once
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# PDF / Excel extraction
# ----------------------------
def extract_text_from_pdf(bytes_io: io.BytesIO) -> str:
    """Extract text from all pages of a PDF"""
    text_parts = []
    with pdfplumber.open(bytes_io) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            text_parts.append(t)
    return "\n".join(text_parts).strip()

def extract_from_excel(bytes_io: io.BytesIO) -> dict:
    """Extract all sheets from an Excel file as DataFrames"""
    xls = pd.ExcelFile(bytes_io)
    dfs = {}
    for sheet in xls.sheet_names:
        df = xls.parse(sheet_name=sheet)
        dfs[sheet] = df
    return dfs

# ----------------------------
# Chunking + FAISS with caching
# ----------------------------
@st.cache_data(show_spinner=False)
def cached_chunks_and_index(text_or_context: str, chunk_size=500, overlap=50):
    """Split text into chunks, embed them, and build FAISS index (cached)."""
    # Chunking
    words = text_or_context.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    
    # Embedding
    embeddings = embedder.encode(chunks, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    
    return chunks, index, embeddings

def retrieve_relevant_chunks(question, chunks, index, embeddings, top_k=3):
    """Return top-k most relevant chunks for a question."""
    q_emb = embedder.encode([question], convert_to_numpy=True)
    D, I = index.search(q_emb, top_k)
    return [chunks[i] for i in I[0]]

# ----------------------------
# Ollama Q&A
# ----------------------------
def ask_ollama(question: str, context: str, model: str = "mistral") -> str:
    """Send a financial Q&A prompt to Ollama with the given context"""
    prompt = f"""
    You are a financial analyst assistant.
    Use the following document text to answer the question.

    Context:
    {context}

    Question: {question}

    Answer in clear, concise financial terms.
    """
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]
