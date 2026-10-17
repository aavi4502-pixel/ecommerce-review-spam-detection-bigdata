import org.apache.spark.sql.functions._

val df = spark.read.parquet("hdfs://namenode:9000/project/cleaned/reviews_scala")
df.cache()

// 1. Rating distribution
val ratingDist = df.groupBy("overall").count().orderBy(desc("count"))
ratingDist.write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/rating_distribution")

// 2. Sentiment distribution
val sentimentDist = df.groupBy("sentiment").count().orderBy(desc("count"))
sentimentDist.write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/sentiment_distribution")

// 3. Top products by review count
val topProducts = df.groupBy("asin").count().orderBy(desc("count")).limit(10)
topProducts.write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/top_products")

// 4. Product average rating (with count)
val productRatings = df.groupBy("asin").agg(count("*").alias("reviews"), round(avg("overall"), 2).alias("avg_rating")).orderBy(desc("reviews")).limit(10)
productRatings.write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/product_ratings")

// 5. Yearly reviews
val yearlyReviews = df.withColumn("year", expr("right(reviewTime, 4)")).groupBy("year").count().orderBy("year")
yearlyReviews.write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/yearly_reviews")

// 6. Review length analysis
val reviewLength = df.withColumn("review_len", length(col("reviewText"))).agg(round(avg("review_len"), 2).alias("avg_length"), min("review_len").alias("min_length"), max("review_len").alias("max_length"))
reviewLength.write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/review_length")

// 7. Sentiment vs average rating
val sentimentRating = df.groupBy("sentiment").agg(count("*").alias("reviews"), round(avg("overall"), 2).alias("avg_rating")).orderBy(desc("reviews"))
sentimentRating.write.mode("overwrite").option("header", "true").csv("hdfs://namenode:9000/project/analytics/sentiment_rating")

println("SUCCESS: Saved all analytics to HDFS.")
sys.exit(0)
