# ml/train_model.py
import pandas as pd
import xgboost as xgb
import joblib

def train_recommendation_model():
    df = pd.read_parquet("lakehouse/github_repos.parquet")
    X = df[['stars','forks']]
    y = df['stars']  # example target
    model = xgb.XGBRanker(objective='rank:pairwise', n_estimators=50)
    model.fit(X, y)
    joblib.dump(model, "ml/recommendation_model.joblib")