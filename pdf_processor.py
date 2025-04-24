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

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")

    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    return text.strip()

def clean_text(text):
    """Clean the extracted text."""
    # Normalize unicode characters
    text = text.encode('ascii', errors='ignore').decode()
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove unwanted special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,?!:;()\[\]{}"-]', '', text)
    return text.strip()

def split_into_chunks(text, chunk_size=1000, overlap=200):
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
            # Save current chunk
            chunks.append(" ".join(current_chunk))

            # Create overlap
            if overlap > 0:
                overlap_text = " ".join(current_chunk)[-overlap:]
                current_chunk = [overlap_text.strip()]
                total_tokens = len(overlap_text)
            else:
                current_chunk = []
                total_tokens = 0

            # Add current sentence to next chunk
            current_chunk.append(sentence)
            total_tokens += sentence_len

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def process_pdf(pdf_path, chunk_size=1000, overlap=200):
    """Process PDF and return clean, chunked text."""
    raw_text = extract_text_from_pdf(pdf_path)
    clean_content = clean_text(raw_text)
    chunks = split_into_chunks(clean_content, chunk_size, overlap)
    return chunks
