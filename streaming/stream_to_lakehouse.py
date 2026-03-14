# streaming/stream_to_lakehouse.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

def stream_to_lakehouse():
    spark = SparkSession.builder \
        .appName("KafkaToLakehouse") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .getOrCreate()

    schema = StructType() \
        .add("id", IntegerType()) \
        .add("name", StringType()) \
        .add("stars", IntegerType())

    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "github_repos") \
        .load()

    df_parsed = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    # Write to Hudi
    df_parsed.writeStream \
        .format("hudi") \
        .option("hoodie.table.name", "github_repos") \
        .option("hoodie.datasource.write.recordkey.field", "id") \
        .option("hoodie.datasource.write.precombine.field", "stars") \
        .option("checkpointLocation", "/tmp/hudi_checkpoint") \
        .start() \
        .awaitTermination()