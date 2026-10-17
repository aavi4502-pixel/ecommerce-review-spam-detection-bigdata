from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, length
import time

print("==========================================================")
print("LAUNCHING LIVE SPARK SHOWCASE FOR PRESENTATION...")
print("==========================================================")

spark = SparkSession.builder \
    .appName("Ecommerce_Review_Spam_Detection_Live_UI") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "2g") \
    .config("spark.cores.max", "4") \
    .config("spark.ui.port", "4040") \
    .getOrCreate()

print("Connected to Spark! Ingesting Parquet from HDFS...")
df = spark.read.parquet("hdfs://namenode:9000/project/input/All_Amazon_Review.parquet")

# Job 0: Sample Read & Count
print("Running Job 0: Reading dataset sample...")
c = df.limit(5000).count()
print(f"Job 0 complete! Sample count: {c}")

# Job 1: Rating Distribution (Triggers DAG Shuffle with 2 Stages)
print("Running Job 1: Star Rating Distribution across partitions...")
ratings = df.limit(20000).groupBy("overall").count().collect()
print("Job 1 complete! Rating distribution computed.")

# Job 2: Spam Verification Analysis (Triggers 2 Stages & DAG)
print("Running Job 2: Verified purchase breakdown (Spam vs Authentic)...")
spam_check = df.limit(20000).groupBy("verified").count().collect()
print("Job 2 complete! Verified breakdown computed.")

# Job 3: Review Length Character Analytics
print("Running Job 3: Review Length Aggregation...")
len_check = df.limit(20000).withColumn("len", length(col("reviewText"))).groupBy("overall").avg("len").collect()
print("Job 3 complete! Length analytics computed.")

print("==========================================================")
print("ALL 4 JOBS & DAG STAGES ARE FULLY COMPLETED AND LIVE!")
print("OPEN http://localhost:4040/jobs/ TO SEE ALL SUCCEEDED JOBS!")
print("==========================================================")

# Keep the Spark UI alive for the presentation
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    spark.stop()
