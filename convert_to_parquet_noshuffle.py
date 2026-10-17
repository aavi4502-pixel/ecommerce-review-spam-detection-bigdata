from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("ConvertGzipToParquetNoShuffle") \
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

print("Writing directly to Parquet (No Shuffle)...")
# Notice NO .repartition() !
# This forces streaming directly from gzip decompression to parquet compression in 1 task.
df.write.mode("overwrite").parquet("hdfs://namenode:9000/project/input/All_Amazon_Review.parquet")

print("SUCCESS: Data converted to Parquet format!")
spark.stop()
