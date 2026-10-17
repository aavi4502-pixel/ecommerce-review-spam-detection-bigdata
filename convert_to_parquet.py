from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("ConvertGzipToParquet") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

# Explicit schema to avoid the expensive schema inference pass
schema = StructType([
  StructField("reviewerID", StringType(), True),
  StructField("asin", StringType(), True),
  StructField("reviewerName", StringType(), True),
  StructField("helpful", ArrayType(IntegerType()), True),
  StructField("reviewText", StringType(), True),
  StructField("overall", DoubleType(), True),
  StructField("summary", StringType(), True),
  StructField("unixReviewTime", LongType(), True),
  StructField("reviewTime", StringType(), True),
  StructField("verified", BooleanType(), True)
])

print("Reading GZIP file...")
df = spark.read.schema(schema).json("hdfs://namenode:9000/project/input/All_Amazon_Review.json.gz")

print("Repartitioning and writing to Parquet...")
df.repartition(200).write.mode("overwrite").parquet("hdfs://namenode:9000/project/input/All_Amazon_Review.parquet")

print("SUCCESS: Data converted to partitioned Parquet format!")
spark.stop()
