import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class SimpleVectorStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.document_vectors = None
        self.documents = []
        
    def add_documents(self, documents):
        """Add documents and store their vector representations."""
        self.documents = documents
        self.document_vectors = self.vectorizer.fit_transform(documents)
        
    def search(self, query, top_k=3):
        """Return top_k most similar documents to the query."""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [{'text': self.documents[idx], 'score': similarities[idx]} for idx in top_indices]
    
    def save(self, path):
        """Save the vector store to a file."""
        with open(path, 'wb') as f:
            pickle.dump({'documents': self.documents, 'vectorizer': self.vectorizer, 'document_vectors': self.document_vectors}, f)
    
    @classmethod
    def load(cls, path):
        """Load the vector store from a file."""
        if not os.path.exists(path): return None
        with open(path, 'rb') as f:
            data = pickle.load(f)
        store = cls()
        store.documents = data['documents']
        store.vectorizer = data['vectorizer']
        store.document_vectors = data['document_vectors']
        return store
