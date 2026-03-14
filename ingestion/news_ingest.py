# ingestion/github_ingest.py
import json
from kafka import KafkaProducer
import requests
import os

KAFKA_TOPIC = "github_repos"
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def ingest_github():
    url = "https://api.github.com/search/repositories?q=stars:>10000&sort=stars&order=desc"
    response = requests.get(url)
    repos = response.json().get("items", [])
    for repo in repos:
        producer.send(KAFKA_TOPIC, repo)
    producer.flush()
    print(f"✅ Ingested {len(repos)} GitHub repos to Kafka")