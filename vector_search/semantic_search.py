# vector_search/semantic_search.py
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

df = pd.read_parquet("lakehouse/github_repos.parquet")
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['name'].tolist(), convert_to_numpy=True)

def semantic_search(query, k=5):
    query_vec = model.encode([query])
    dists = np.linalg.norm(embeddings - query_vec, axis=1)
    return df.iloc[np.argsort(dists)[:k]].to_dict(orient='records')