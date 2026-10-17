from pyspark.sql import SparkSession
import time

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("AmazonReviews_Presentation_Live") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

print("==================================================")
print("SPARK WEB UI IS NOW LIVE AT http://localhost:4040")
print("==================================================")
print("Keeping Spark alive for your presentation...")

# Keep the script running so the UI stays up
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Shutting down Spark...")
    spark.stop()
