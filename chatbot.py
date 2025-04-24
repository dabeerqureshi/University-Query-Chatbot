from vector_store import SimpleVectorStore
import os
import re

class AdmissionChatbot:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def get_answer(self, question):
        """Generate an answer for the user's question."""
        results = self.vector_store.search(question, top_k=3)

        if not results or results[0]['score'] < 0.1:
            return ("I'm sorry, I don't have enough information to answer that question about admissions. "
                    "Could you try rephrasing or ask something else?")

        # Use the best matching text chunk
        best_match = results[0]['content']
        relevant_sentences = []

        # Extract keywords from the question
        keywords = [k for k in re.findall(r'\b\w+\b', question.lower()) if len(k) > 3]

        # Search for relevant sentences
        for sentence in best_match.split('.'):
            sentence = sentence.strip()
            if not sentence:
                continue
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in keywords):
                relevant_sentences.append(sentence)

        # Compose answer
        if relevant_sentences:
            answer = '. '.join(relevant_sentences) + '.'
        else:
            answer = best_match.strip()

        # Optionally add context from the second-best result
        if len(results) > 1 and results[1]['score'] > 0.4:
            second_match = results[1]['content']
            extra_sentences = second_match.split('.')[:2]
            additional_context = '. '.join(s.strip() for s in extra_sentences if s.strip()) + '.'
            answer += f"\n\nAdditionally: {additional_context}"

        return answer

def create_chatbot_from_pdf(pdf_path, vector_store_path='vector_store.pkl'):
    """Create and return an AdmissionChatbot instance."""
    from pdf_processor import process_pdf

    # Load vector store if it exists
    vector_store = SimpleVectorStore.load(vector_store_path)

    if vector_store is None:
        print("Processing PDF and creating new vector store...")
        chunks = process_pdf(pdf_path)
        vector_store = SimpleVectorStore()
        vector_store.add_documents(chunks)
        vector_store.save(vector_store_path)

    return AdmissionChatbot(vector_store)
