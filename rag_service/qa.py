import os
import numpy as np
import pandas as pd
import faiss
import pickle
from google import genai
from dotenv import load_dotenv

load_dotenv()


class RAGEngine:

    def __init__(self, filename):

        # Initialize Gemini client
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        # Load dataset (CSV)
        df = pd.read_csv(filename)

        df = df.dropna()

        docs = df["text"].astype(str).tolist()

        self.docs = docs

        # Check if FAISS index exists
        if os.path.exists("rag_service/faiss_index.bin"):

            print("Loading existing FAISS index...")

            self.index = faiss.read_index("rag_service/faiss_index.bin")

            with open("rag_service/docs.pkl", "rb") as f:
                self.docs = pickle.load(f)

        else:

            print("Creating embeddings with Gemini...")

            embeddings = []

            for doc in self.docs:

                res = self.client.models.embed_content(
                    model="gemini-embedding-001",
                    contents=doc,
                    config={"task_type": "RETRIEVAL_DOCUMENT"}
                )

                embeddings.append(res.embeddings[0].values)

            embeddings_array = np.array(embeddings, dtype="float32")

            dimension = embeddings_array.shape[1]

            self.index = faiss.IndexFlatL2(dimension)

            self.index.add(embeddings_array)

            # Save index
            faiss.write_index(self.index, "rag_service/faiss_index.bin")

            with open("rag_service/docs.pkl", "wb") as f:
                pickle.dump(self.docs, f)


    def retrieve(self, query, k=3):

        res = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=query,
            config={"task_type": "RETRIEVAL_QUERY"}
        )

        q_emb = np.array([res.embeddings[0].values], dtype="float32")

        distances, indices = self.index.search(q_emb, k)

        results = [self.docs[i] for i in indices[0]]

        return "\n".join(results)


    def ask_llm(self, question, context):

        prompt = f"""
You are a helpful assistant.

Use ONLY the provided context to answer the question.

If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text


    def ask(self, question):

        context = self.retrieve(question)

        answer = self.ask_llm(question, context)

        return answer