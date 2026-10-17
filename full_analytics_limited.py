from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, desc, count, avg, round, expr, length, min, max

# Limit cores to 4 so it doesn't run out of memory reading 20 blocks at once
spark = SparkSession.builder \
    .master("local[4]") \
    .appName("FullDatasetAnalytics") \
    .config("spark.driver.memory", "6g") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

print("Loading 50GB Parquet Dataset from HDFS...")
raw_df = spark.read.parquet("hdfs://namenode:9000/project/input/All_Amazon_Review.parquet")

print("Cleaning data and applying Sentiment Analysis...")
cleaned_df = raw_df.dropna(subset=["overall", "reviewText", "asin"])

df = cleaned_df.withColumn(
    "sentiment",
    when(col("overall") > 3, "Positive")
    .when(col("overall") == 3, "Neutral")
    .otherwise("Negative")
)

print("Starting Aggregations...")

print("Calculating Rating Distribution...")
ratingDist = df.groupBy("overall").count().orderBy(desc("count"))
ratingDist.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_rating_distribution")

print("Calculating Sentiment Distribution...")
sentimentDist = df.groupBy("sentiment").count().orderBy(desc("count"))
sentimentDist.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_sentiment_distribution")

print("Calculating Top Products...")
topProducts = df.groupBy("asin").count().orderBy(desc("count")).limit(20)
topProducts.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_top_products")

print("Calculating Product Ratings...")
productRatings = df.groupBy("asin").agg(count("*").alias("reviews"), round(avg("overall"), 2).alias("avg_rating")).orderBy(desc("reviews")).limit(20)
productRatings.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_product_ratings")

print("Calculating Yearly Review Trends...")
yearlyReviews = df.withColumn("year", expr("right(reviewTime, 4)")).groupBy("year").count().orderBy("year")
yearlyReviews.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_yearly_reviews")

print("Calculating Review Lengths...")
reviewLength = df.withColumn("review_len", length(col("reviewText"))).agg(
    round(avg("review_len"), 2).alias("avg_length"), 
    min("review_len").alias("min_length"), 
    max("review_len").alias("max_length")
)
reviewLength.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_review_length")

print("Calculating Sentiment vs Rating correlation...")
sentimentRating = df.groupBy("sentiment").agg(count("*").alias("reviews"), round(avg("overall"), 2).alias("avg_rating")).orderBy(desc("reviews"))
sentimentRating.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_sentiment_rating")

print("SUCCESS: All Big Data Analytics completed and saved to HDFS!")
spark.stop()
