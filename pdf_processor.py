import os
import re
import nltk
import PyPDF2
from nltk.tokenize import sent_tokenize

# Ensure NLTK tokenizer is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def extract_text_per_page(pdf_path):
    """Extract text per page from PDF."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")
    
    page_texts = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for i, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                page_texts.append({
                    "page": i + 1,
                    "text": page_text.strip()
                })
    return page_texts

def clean_text(text):
    """Clean the extracted text."""
    text = text.encode('ascii', errors='ignore').decode()  # Remove non-ascii
    text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
    text = re.sub(r'[^\w\s.,?!:;()\[\]{}"-]', '', text)  # Remove unwanted chars
    return text.strip()

def split_text_to_chunks(text, page, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks using sentence boundaries."""
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    total_tokens = 0

    for sentence in sentences:
        sentence_len = len(sentence)

        if total_tokens + sentence_len <= chunk_size:
            current_chunk.append(sentence)
            total_tokens += sentence_len
        else:
            # Create chunk with metadata
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "content": chunk_text,
                "metadata": {
                    "page": page,
                    "length": len(chunk_text)
                }
            })

            # Overlap tokens
            if overlap > 0:
                overlap_text = chunk_text[-overlap:]
                current_chunk = [overlap_text.strip()]
                total_tokens = len(overlap_text)
            else:
                current_chunk = []
                total_tokens = 0

            current_chunk.append(sentence)
            total_tokens += sentence_len

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append({
            "content": chunk_text,
            "metadata": {
                "page": page,
                "length": len(chunk_text)
            }
        })

    return chunks

def process_pdf(pdf_path, chunk_size=1000, overlap=200):
    """Process entire PDF into clean, contextual chunks with metadata."""
    pages = extract_text_per_page(pdf_path)
    all_chunks = []

    for page_info in pages:
        page_text = clean_text(page_info["text"])
        chunks = split_text_to_chunks(page_text, page=page_info["page"], chunk_size=chunk_size, overlap=overlap)
        all_chunks.extend(chunks)

    return all_chunks
