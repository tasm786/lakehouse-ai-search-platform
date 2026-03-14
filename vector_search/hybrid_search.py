# vector_search/hybrid_search.py
from vector_search.vector_search import vector_search
from features.feature_views import compute_features
import pandas as pd

def hybrid_search(query, k=5, alpha=0.7):
    vec_results = vector_search(query, k=10)
    df = pd.read_parquet("lakehouse/github_repos.parquet").iloc[vec_results]
    df['score'] = alpha*df['stars'] + (1-alpha)*df['forks']
    return df.sort_values('score', ascending=False).head(k).to_dict(orient='records')