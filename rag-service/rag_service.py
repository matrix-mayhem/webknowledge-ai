from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-miniLM-L6-V2")

index = None
documents = []

def build_index(text_chunks):

    global index
    global documents

    documents = text_chunks
    embeddings = model.encode(text_chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

def search(query):
    query_vector = model.encode(["query"])
    distances, indices = index.search(np.array(query_vector),3)
    results = [documents[i] for i in indices[0]]
    return results
