# airflow/dags/ml_pipeline_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from ingestion.github_ingest import ingest_github
from ingestion.news_ingest import ingest_news
from ingestion.yelp_ingest import ingest_yelp
from streaming.stream_to_lakehouse import stream_to_lakehouse
from features.feature_views import compute_features
from embeddings.build_faiss_index import build_faiss_index
from ml.train_model import train_recommendation_model
from ml.evaluate_model import evaluate_model

dag = DAG('ml_lakehouse_pipeline', start_date=datetime(2026,3,11), schedule_interval='@daily', catchup=False)

ingest_github_task = PythonOperator(task_id='ingest_github', python_callable=ingest_github, dag=dag)
ingest_news_task = PythonOperator(task_id='ingest_news', python_callable=ingest_news, dag=dag)
ingest_yelp_task = PythonOperator(task_id='ingest_yelp', python_callable=ingest_yelp, dag=dag)
stream_task = PythonOperator(task_id='stream_to_lakehouse', python_callable=stream_to_lakehouse, dag=dag)
feature_task = PythonOperator(task_id='compute_features', python_callable=compute_features, dag=dag)
index_task = PythonOperator(task_id='build_faiss_index', python_callable=build_faiss_index, dag=dag)
train_task = PythonOperator(task_id='train_model', python_callable=train_recommendation_model, dag=dag)
evaluate_task = PythonOperator(task_id='evaluate_model', python_callable=evaluate_model, dag=dag)

ingest_github_task >> ingest_news_task >> ingest_yelp_task >> stream_task >> feature_task >> index_task >> train_task >> evaluate_task