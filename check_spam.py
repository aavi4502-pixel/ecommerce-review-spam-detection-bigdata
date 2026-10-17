from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('CheckSpam').getOrCreate()
df = spark.read.parquet('hdfs://namenode:9000/project/input/All_Amazon_Review.parquet').limit(5000)
df.groupBy('verified').count().show()
spark.stop()
