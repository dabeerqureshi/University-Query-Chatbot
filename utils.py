import wikipedia

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return f"According to Wikipedia:\n\n{summary}"
    except Exception as e:
        return "Sorry, I couldn't find anything on Wikipedia either."
