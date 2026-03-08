from rag_engine import RAGEngine

engine = RAGEngine(filename="data/site_data.json")

def answer_question(question):
    context = engine.search(question)
    answer = " ".join(context)
    return answer
