import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object AmazonPreprocessing {

  def main(args: Array[String]): Unit = {

    // --------------------------------------------------
    // 1. Create Spark Session
    // --------------------------------------------------
    val spark = SparkSession.builder()
      .appName("Amazon Review Preprocessing")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._

    // --------------------------------------------------
    // 2. Input and Output HDFS paths
    // --------------------------------------------------
    val inputPath =
      "hdfs://namenode:9000/project/test/reviews_sample.json"

    val outputPath =
      "hdfs://namenode:9000/project/cleaned/reviews_scala"

    // --------------------------------------------------
    // 3. Read raw Amazon review data from HDFS
    // --------------------------------------------------
    println("==============================================")
    println("AMAZON REVIEW PREPROCESSING")
    println("==============================================")
    println("Reading raw data from HDFS...")

    val reviews = spark.read
      .json(inputPath)

    val originalCount = reviews.count()

    println("Original record count = " + originalCount)

    // --------------------------------------------------
    // 4. Remove duplicate records
    // --------------------------------------------------
    val noDuplicates = reviews
      .dropDuplicates()

    val duplicateRemovedCount = noDuplicates.count()

    println(
      "After duplicate removal = " + duplicateRemovedCount
    )

    // --------------------------------------------------
    // 5. Remove invalid ratings and missing review text
    // --------------------------------------------------
    val cleanedReviews = noDuplicates
      .filter(col("overall").between(1.0, 5.0))
      .filter(col("reviewText").isNotNull)
      .filter(length(trim(col("reviewText"))) > 0)

    val cleanedCount = cleanedReviews.count()

    println(
      "After cleaning = " + cleanedCount
    )

    println(
      "Records removed = " + (originalCount - cleanedCount)
    )

    // --------------------------------------------------
    // 6. Create sentiment labels
    //
    // 1-2 stars = Negative
    // 3 stars   = Neutral
    // 4-5 stars = Positive
    // --------------------------------------------------
    val labeledReviews = cleanedReviews
      .withColumn(
        "sentiment",
        when(col("overall") <= 2.0, "Negative")
          .when(col("overall") === 3.0, "Neutral")
          .when(col("overall") >= 4.0, "Positive")
          .otherwise("Unknown")
      )

    // --------------------------------------------------
    // 7. Select useful columns
    // --------------------------------------------------
    val finalReviews = labeledReviews.select(
      col("asin"),
      col("reviewerID"),
      col("overall"),
      col("reviewText"),
      col("summary"),
      col("reviewTime"),
      col("verified"),
      col("sentiment")
    )

    // --------------------------------------------------
    // 8. Display preprocessing results
    // --------------------------------------------------
    println("==============================================")
    println("SENTIMENT DISTRIBUTION")
    println("==============================================")

    finalReviews
      .groupBy("sentiment")
      .count()
      .orderBy("sentiment")
      .show()

    println("==============================================")
    println("FINAL SCHEMA")
    println("==============================================")

    finalReviews.printSchema()

    println("==============================================")
    println("SAMPLE PROCESSED DATA")
    println("==============================================")

    finalReviews.show(5, truncate = false)

    // --------------------------------------------------
    // 9. Write processed data to HDFS as Parquet
    // --------------------------------------------------
    println("Writing processed data to HDFS...")

    finalReviews
      .write
      .mode("overwrite")
      .parquet(outputPath)

    println("==============================================")
    println("PREPROCESSING COMPLETED")
    println("==============================================")
    println("Output path:")
    println(outputPath)

    // --------------------------------------------------
    // 10. Stop Spark
    // --------------------------------------------------
    spark.stop()
  }
}