from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, length
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

# Initialize Spark Session for Spam Detection
spark = SparkSession.builder \
    .appName("Ecommerce_Review_Spam_Detection") \
    .getOrCreate()

print("==========================================================")
print("E-COMMERCE REVIEW SPAM DETECTION USING BIG DATA (SPARK MLLIB)")
print("==========================================================")

# 1. Load Parquet Dataset from HDFS
raw_df = spark.read.parquet("hdfs://namenode:9000/project/input/All_Amazon_Review.parquet")

# Clean rows with missing values
df_clean = raw_df.dropna(subset=["verified", "reviewText", "overall"]).limit(50000)

# 2. Define Spam vs Non-Spam Ground Truth Label:
# A review is flagged as SPAM (1.0) if it is an UNVERIFIED purchase (verified == False)
# Otherwise it is classified as AUTHENTIC / NOT SPAM (0.0)
df = df_clean.withColumn(
    "label",
    when(col("verified") == False, 1.0).otherwise(0.0)
)

print(f"Training Spam Detection Model on {df.count()} Amazon reviews...")

# 3. NLP Feature Extraction Pipeline
tokenizer = Tokenizer(inputCol="reviewText", outputCol="words")
remover = StopWordsRemover(inputCol="words", outputCol="filtered")
hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=10000)
idf = IDF(inputCol="rawFeatures", outputCol="features")

# 4. Classification Algorithm: Logistic Regression for Spam vs Non-Spam
lr = LogisticRegression(maxIter=10, regParam=0.01)

pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, lr])

# Split into Training (80%) and Test (20%) sets
(trainData, testData) = df.randomSplit([0.8, 0.2], seed=42)

print("Training the Spam Classifier Model...")
model = pipeline.fit(trainData)
print("Training Complete!")

# 5. Evaluate on Test Data
predictions = model.transform(testData)

print("==========================================================")
print("Sample Spam vs Not Spam Predictions:")
print("label: 1.0 = SPAM (Fake/Unverified) | 0.0 = NOT SPAM (Authentic)")
print("==========================================================")
predictions.select("reviewText", "verified", "label", "prediction").show(15, truncate=55)

# Calculate Accuracy
correct = predictions.filter(col("label") == col("prediction")).count()
total = predictions.count()
accuracy = (correct / total) * 100
print(f"Spam Detection Model Accuracy: {accuracy:.2f}%")
print("==========================================================")

spark.stop()
