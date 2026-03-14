# embeddings/build_faiss_index.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

def build_faiss_index():
    df = pd.read_parquet("lakehouse/github_repos.parquet")
    texts = df['name'].tolist()

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "embeddings/faiss_index.bin")
    print("✅ FAISS index built")