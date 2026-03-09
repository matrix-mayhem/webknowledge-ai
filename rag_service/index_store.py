import faiss
import pickle
import os


def save_index(index, docs):

    faiss.write_index(index, "rag_service/faiss_index.bin")

    with open("rag_service/docs.pkl", "wb") as f:
        pickle.dump(docs, f)


def load_index():

    if not os.path.exists("rag_service/faiss_index.bin"):
        return None, None

    if not os.path.exists("rag_service/docs.pkl"):
        return None, None

    index = faiss.read_index("rag_service/faiss_index.bin")

    with open("rag_service/docs.pkl", "rb") as f:
        docs = pickle.load(f)

    return index, docs