from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, desc, count, avg, round, expr, length, min, max

# Initialize Spark Session for the massive analytics job
spark = SparkSession.builder \
    .appName("FullDatasetAnalytics") \
    .config("spark.driver.memory", "6g") \
    .getOrCreate()

print("Loading 50GB Parquet Dataset from HDFS...")
raw_df = spark.read.parquet("hdfs://namenode:9000/project/input/All_Amazon_Review.parquet")

# 1. Data Cleaning & Sentiment Labelling
print("Cleaning data and applying Sentiment Analysis...")
cleaned_df = raw_df.dropna(subset=["overall", "reviewText", "asin"])

# Apply sentiment logic based on star rating
df = cleaned_df.withColumn(
    "sentiment",
    when(col("overall") > 3, "Positive")
    .when(col("overall") == 3, "Neutral")
    .otherwise("Negative")
)

# NO .cache()! The dataset is way too big for memory (150GB uncompressed). 
# Spark will read directly from the compressed Parquet file for each query.

print("Starting Aggregations...")

# 1. Rating distribution
print("Calculating Rating Distribution...")
ratingDist = df.groupBy("overall").count().orderBy(desc("count"))
ratingDist.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_rating_distribution")

# 2. Sentiment distribution
print("Calculating Sentiment Distribution...")
sentimentDist = df.groupBy("sentiment").count().orderBy(desc("count"))
sentimentDist.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_sentiment_distribution")

# 3. Top products by review count
print("Calculating Top Products...")
topProducts = df.groupBy("asin").count().orderBy(desc("count")).limit(20)
topProducts.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_top_products")

# 4. Product average rating (with count)
print("Calculating Product Ratings...")
productRatings = df.groupBy("asin").agg(count("*").alias("reviews"), round(avg("overall"), 2).alias("avg_rating")).orderBy(desc("reviews")).limit(20)
productRatings.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_product_ratings")

# 5. Yearly reviews
print("Calculating Yearly Review Trends...")
yearlyReviews = df.withColumn("year", expr("right(reviewTime, 4)")).groupBy("year").count().orderBy("year")
yearlyReviews.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_yearly_reviews")

# 6. Review length analysis
print("Calculating Review Lengths...")
reviewLength = df.withColumn("review_len", length(col("reviewText"))).agg(
    round(avg("review_len"), 2).alias("avg_length"), 
    min("review_len").alias("min_length"), 
    max("review_len").alias("max_length")
)
reviewLength.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_review_length")

# 7. Sentiment vs Average Rating
print("Calculating Sentiment vs Rating correlation...")
sentimentRating = df.groupBy("sentiment").agg(count("*").alias("reviews"), round(avg("overall"), 2).alias("avg_rating")).orderBy(desc("reviews"))
sentimentRating.repartition(1).write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/full_sentiment_rating")

print("SUCCESS: All Big Data Analytics completed and saved to HDFS!")
spark.stop()
