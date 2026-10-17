from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

# Initialize Spark Session for Standalone Cluster
spark = SparkSession.builder \
    .appName("AmazonReviews_MLlib_Sentiment") \
    .getOrCreate()

print("==================================================")
print("UNIT IV: SPARK MLLIB - NLP SENTIMENT ANALYSIS")
print("==================================================")

# 1. Load a sample of the Parquet Dataset to train the model quickly
print("Loading data from HDFS...")
raw_df = spark.read.parquet("hdfs://namenode:9000/project/input/All_Amazon_Review.parquet")

# Clean and sample 50,000 rows to prevent OOM in the Docker worker
df_clean = raw_df.dropna(subset=["overall", "reviewText"]).limit(50000)

# Create the numeric label (1 = Positive, 0 = Negative)
# MLlib requires labels to be numeric (Doubles or Integers)
df = df_clean.withColumn("label", when(col("overall") > 3, 1.0).otherwise(0.0))

print(f"Training ML model on {df.count()} reviews...")

# 2. NLP Pipeline (Natural Language Processing)
# Break text into words
tokenizer = Tokenizer(inputCol="reviewText", outputCol="words")
# Remove common words like 'the', 'is', 'and'
remover = StopWordsRemover(inputCol="words", outputCol="filtered")
# Convert words to numerical term frequencies
hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=10000)
# Down-weight words that appear in every single review
idf = IDF(inputCol="rawFeatures", outputCol="features")

# 3. Machine Learning Algorithm
# Logistic Regression will learn which words correlate to Positive (1.0) or Negative (0.0)
lr = LogisticRegression(maxIter=10, regParam=0.01)

# Assemble the Pipeline
pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, lr])

# Split into Training and Testing datasets
(trainingData, testData) = df.randomSplit([0.8, 0.2], seed=42)

# 4. Train the Model!
print("Training the Logistic Regression Model... (This takes a moment)")
model = pipeline.fit(trainingData)
print("Training Complete!")

# 5. Test the Model
print("Predicting sentiment on the test dataset...")
predictions = model.transform(testData)

# Show the results (Original Text vs Actual Label vs ML Prediction)
print("==================================================")
print("MLlib Predictions (1.0 = Positive, 0.0 = Negative)")
print("==================================================")
predictions.select("reviewText", "label", "prediction").show(20, truncate=50)

# Evaluate accuracy
correct = predictions.filter(col("label") == col("prediction")).count()
total = predictions.count()
accuracy = correct / total
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")
print("==================================================")

spark.stop()
