from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import time

print("Starting Spark Presentation Session...")

spark = SparkSession.builder \
    .appName("Ecommerce_Review_Spam_Detection_UI") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

print("Executing Query 1: Reading HDFS Parquet dataset and counting...")
df = spark.read.parquet("hdfs://namenode:9000/project/input/All_Amazon_Review.parquet")

# Action 1: Triggers Job 0 (Shows in Spark UI)
sample_count = df.limit(10000).count()
print(f"Sample count: {sample_count}")

# Action 2: Triggers Job 1 with groupBy / shuffle (Shows 2 Stages and full DAG!)
print("Executing Query 2: Rating distribution with DAG shuffle...")
rating_summary = df.limit(50000).groupBy("overall").count().collect()
print("Rating summary calculated!")

# Action 3: Triggers Job 2: Spam Detection distribution (verified vs unverified)
print("Executing Query 3: Spam verification breakdown...")
spam_summary = df.limit(50000).groupBy("verified").count().collect()
print("Spam summary calculated!")

print("==================================================================")
print("SUCCESS: 3 JOBS & STAGES ARE NOW FULLY POPULATED IN SPARK UI!")
print("OPEN http://localhost:4040/jobs/ TO SEE THE COMPLETED JOBS & DAG!")
print("==================================================================")

# Keep the script alive so the UI stays populated and clickable
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    spark.stop()
