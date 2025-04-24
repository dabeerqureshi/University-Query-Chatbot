import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class SimpleVectorStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.document_vectors = None
        self.chunks = []  # Each chunk is a dict with 'content' and 'metadata'

    def add_documents(self, chunks):
        """
        Add a list of chunks where each chunk is:
        {
            'content': 'text of the chunk',
            'metadata': {
                'page': 3,
                'length': 420
            }
        }
        """
        self.chunks = chunks
        texts = [chunk['content'] for chunk in chunks]
        self.document_vectors = self.vectorizer.fit_transform(texts)

    def search(self, query, top_k=3):
        """Return top_k most relevant chunks to the query."""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [
            {
                'content': self.chunks[i]['content'],
                'metadata': self.chunks[i]['metadata'],
                'score': similarities[i]
            }
            for i in top_indices
        ]

    def save(self, path):
        """Save the vector store to a file."""
        with open(path, 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'vectorizer': self.vectorizer,
                'document_vectors': self.document_vectors
            }, f)

    @classmethod
    def load(cls, path):
        """Load the vector store from a file."""
        if not os.path.exists(path):
            return None
        with open(path, 'rb') as f:
            data = pickle.load(f)
        store = cls()
        store.chunks = data['chunks']
        store.vectorizer = data['vectorizer']
        store.document_vectors = data['document_vectors']
        return store
