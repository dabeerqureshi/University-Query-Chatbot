from vector_store import SimpleVectorStore
import os
import re

class AdmissionChatbot:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        
    def get_answer(self, question):
        """Generate an answer for the user's question."""
        # Search for relevant documents
        results = self.vector_store.search(question, top_k=3)
        
        if not results or results[0]['score'] < 0.1:
            return "I'm sorry, I don't have enough information to answer that question about admissions. Could you try rephrasing or ask something else?"
        
        # Use the best matching text to form an answer
        best_match = results[0]['text']
        
        # Extract the most relevant sentences
        sentences = best_match.split('.')
        relevant_sentences = []
        
        # Keywords from the question
        keywords = re.findall(r'\b\w+\b', question.lower())
        keywords = [k for k in keywords if len(k) > 3]  # Filter out short words
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in keywords):
                relevant_sentences.append(sentence)
        
        # If we found relevant sentences, use them
        if relevant_sentences:
            answer = '. '.join(relevant_sentences) + '.'
        else:
            # Fall back to the best match
            answer = best_match
        
        # Add additional context from other results if helpful
        if len(results) > 1 and results[1]['score'] > 0.5:
            additional_info = results[1]['text']
            # Extract only the most relevant part
            additional_sentences = additional_info.split('.')[:2]
            additional_context = '. '.join(additional_sentences) + '.'
            answer += f"\n\nAdditionally: {additional_context}"
            
        return answer

def create_chatbot_from_pdf(pdf_path, vector_store_path='vector_store.pkl'):
    """Create a chatbot from a PDF document."""
    from pdf_processor import process_pdf
    
    # Try to load existing vector store
    vector_store = SimpleVectorStore.load(vector_store_path)
    
    if vector_store is None or not os.path.exists(vector_store_path):
        print("Processing PDF and creating new vector store...")
        # Process the PDF
        chunks = process_pdf(pdf_path)
        
        # Create and save vector store
        vector_store = SimpleVectorStore()
        vector_store.add_documents(chunks)
        vector_store.save(vector_store_path)
    
    return AdmissionChatbot(vector_store)