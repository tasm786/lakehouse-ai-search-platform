# ml/evaluate_model.py
import pandas as pd
import joblib
from sklearn.metrics import ndcg_score

def evaluate_model():
    df = pd.read_parquet("lakehouse/github_repos.parquet")
    X = df[['stars','forks']]
    y = df['stars']
    model = joblib.load("ml/recommendation_model.joblib")
    preds = model.predict(X)
    score = ndcg_score([y], [preds])
    print(f"✅ NDCG Score: {score}")