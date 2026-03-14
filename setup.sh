#!/bin/bash
set -e

echo "Creating Python virtual environments..."
python3.12 -m venv env-data
python3.12 -m venv env-features
python3.12 -m venv env-api
python3.12 -m venv env-orchestration

echo "Installing dependencies..."
source env-data/bin/activate
pip install --upgrade pip
pip install pyspark==3.5.0 hudi-spark3.5-bundle pyarrow requests pandas great_expectations openlineage-python
deactivate

source env-features/bin/activate
pip install --upgrade pip
pip install feast==0.60.0 redis numpy<2.0.0
deactivate

source env-api/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn sentence-transformers faiss-cpu redis
deactivate

source env-orchestration/bin/activate
pip install --upgrade pip
pip install apache-airflow
deactivate

echo "Starting Podman services..."
podman-compose -f infra/podman-compose.yml up -d

echo "Waiting for Zookeeper & Kafka to be healthy..."
until podman exec -it $(podman ps -q --filter name=zookeeper) sh -c 'echo ruok | nc localhost 2181 | grep imok'; do
  echo "Waiting for Zookeeper..."
  sleep 5
done

until podman exec -it $(podman ps -q --filter name=kafka) sh -c 'kafka-broker-api-versions --bootstrap-server localhost:9092'; do
  echo "Waiting for Kafka..."
  sleep 5
done

echo "Producing sample Kafka data..."
source env-data/bin/activate
python ingestion/kafka_produce.py
deactivate

echo "Starting Spark streaming ingestion (Hudi)..."
source env-data/bin/activate
nohup python streaming/stream_to_hudi.py &
STREAM_PID=$!
deactivate
sleep 10

echo "Converting Hudi → Iceberg..."
source env-data/bin/activate
python lakehouse/hudi_to_iceberg.py
deactivate

echo "Validating Hudi using Great Expectations..."
source env-data/bin/activate
python lakehouse/validate_hudi.py
deactivate

echo "Building FAISS embeddings..."
source env-api/bin/activate
python embeddings/build_index.py
deactivate

echo "Starting FastAPI server..."
source env-api/bin/activate
nohup uvicorn api.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!
deactivate

echo "Setup complete!"
echo "Spark streaming PID: $STREAM_PID, FastAPI PID: $API_PID"
echo "Access API at http://localhost:8000"