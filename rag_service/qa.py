from rag_engine import search

def answer_question(question):
    context = search(question)
    answer = " ".join(context)
    return answer
