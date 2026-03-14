# api/main.py
from fastapi import FastAPI
from vector_search.vector_search import vector_search
from vector_search.semantic_search import semantic_search
from vector_search.hybrid_search import hybrid_search

app = FastAPI()

@app.get("/vector_search")
def vector(q: str, k: int = 5):
    return vector_search(q, k)

@app.get("/semantic_search")
def semantic(q: str, k: int = 5):
    return semantic_search(q, k)

@app.get("/hybrid_search")
def hybrid(q: str, k: int = 5, alpha: float = 0.7):
    return hybrid_search(q, k, alpha)