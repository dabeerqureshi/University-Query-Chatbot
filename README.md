# 📚 University Query Chatbot

A smart, efficient chatbot designed to answer university-related questions using a local PDF knowledge base with a web search fallback. Built using **Streamlit**, **LangChain**, and **SentenceTransformers**, this application provides fast, accurate responses while operating entirely offline—no reliance on Hugging Face pipelines.

---

## 🚀 Features

- 📘 **PDF-Based Knowledge Base**: Accepts university books or prospectuses as input.
- 🔍 **Robust Information Retrieval**: Leverages vector similarity search for relevant answers.
- 🧠 **Local Embeddings**: Utilizes SentenceTransformers for fast, on-device query matching.
- 🌐 **Web Search Fallback**: Optionally retrieves information from the web when local answers are insufficient.
- 💻 **Interactive UI**: Simple, elegant Streamlit-based web interface for user queries.

---

## 🛠️ Functionality Overview

1. **PDF Upload**  
   - Users upload a university book or prospectus as input.

2. **Text Extraction & Preprocessing**  
   - Extracts raw text from the PDF.
   - Cleans the text by:
     - Removing non-ASCII characters
     - Collapsing extra whitespace
     - Removing special characters and formatting noise

3. **Text Chunking**  
   - Splits the cleaned text into manageable chunks for embedding and retrieval.

4. **Vector Store Creation**  
   - Converts text chunks into vector embeddings using SentenceTransformers.
   - Saves the vectors into a **FAISS** database for fast similarity search.

5. **Streamlit Interface**  
   - User enters a question via a sleek UI.
   - The app retrieves the most relevant chunk(s) from the vector store and displays the answer.
   - If no relevant match is found, the system performs a web search fallback.

---

## 📦 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python, LangChain  
- **Embeddings**: SentenceTransformers  
- **Vector Database**: FAISS  
- **PDF Parsing**: PyMuPDF or PDFMiner (configurable)


## 🧪 How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/dabeerqureshi/University-Query-Chatbot.git
   cd University-Query-Chatbot
