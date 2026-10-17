from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, length, coalesce, lit, element_at
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
import json

print("======================================================================")
print("UNIT IV: ADVANCED MULTI-FEATURE SPAM CLASSIFIER WITH SPARK MLLIB")
print("======================================================================")

# 1. Initialize Spark Session
spark = SparkSession.builder \
    .appName("Advanced_Ecommerce_Spam_Detection") \
    .getOrCreate()

# 2. Ingest Parquet Dataset from HDFS
print("Loading reviews from HDFS...")
raw_df = spark.read.parquet("hdfs://namenode:9000/project/input/All_Amazon_Review.parquet")

# Filter null values and sample 60,000 records for fast, reliable training
df_clean = raw_df.dropna(subset=["verified", "reviewText", "overall"]).limit(60000)

# Extract helpful upvotes safely (helpful is array<int> [upvotes, total_votes])
df_features = df_clean.withColumn("helpful_votes", coalesce(element_at(col("helpful"), 1).cast("double"), lit(0.0))) \
                      .withColumn("review_len", length(col("reviewText")).cast("double")) \
                      .withColumn("rating", col("overall").cast("double"))

# 3. Enhanced Ground-Truth Spam Labeling (Composite Heuristic)
# Academic Standard: Unverified purchase + extreme rating (5 or 1 star) + short length or 0 helpful votes
df_labeled = df_features.withColumn(
    "label",
    when(
        (col("verified") == False) & 
        ((col("rating") == 5.0) | (col("rating") == 1.0)) & 
        ((col("review_len") < 150.0) | (col("helpful_votes") == 0.0)),
        1.0 # SPAM
    ).otherwise(0.0) # AUTHENTIC
)

print(f"Total dataset for modeling: {df_labeled.count()} records")
spam_count = df_labeled.filter(col("label") == 1.0).count()
auth_count = df_labeled.filter(col("label") == 0.0).count()
print(f"Spam instances: {spam_count} | Authentic instances: {auth_count}")

# 4. Multi-Feature Pipeline:
# A. Text Processing Stages
tokenizer = Tokenizer(inputCol="reviewText", outputCol="words")
remover = StopWordsRemover(inputCol="words", outputCol="filtered")
hashingTF = HashingTF(inputCol="filtered", outputCol="raw_text_features", numFeatures=5000)
idf = IDF(inputCol="raw_text_features", outputCol="text_features")

# B. Vector Assembler: Combines NLP Text Vector + Numerical Metadata Features!
assembler = VectorAssembler(
    inputCols=["text_features", "rating", "review_len", "helpful_votes"],
    outputCol="features"
)

# C. Machine Learning Classifier: Logistic Regression
lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=15, regParam=0.01)

# Assemble Pipeline
pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, assembler, lr])

# Split Train (80%) vs Test (20%)
(trainData, testData) = df_labeled.randomSplit([0.8, 0.2], seed=42)

print("\nTraining the Multi-Feature Logistic Regression Spam Model...")
model = pipeline.fit(trainData)
print("Training Completed Successfully!")

# 5. Model Evaluation on Unseen Test Partition
predictions = model.transform(testData)

# Calculate Confusion Matrix
tp = predictions.filter((col("label") == 1.0) & (col("prediction") == 1.0)).count()
fp = predictions.filter((col("label") == 0.0) & (col("prediction") == 1.0)).count()
tn = predictions.filter((col("label") == 0.0) & (col("prediction") == 0.0)).count()
fn = predictions.filter((col("label") == 1.0) & (col("prediction") == 0.0)).count()
total = predictions.count()

accuracy = (tp + tn) / total if total > 0 else 0.0
precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

# Multiclass Evaluators from Spark MLlib
evaluator_acc = MulticlassClassificationEvaluator(metricName="accuracy")
evaluator_f1 = MulticlassClassificationEvaluator(metricName="f1")
spark_acc = evaluator_acc.evaluate(predictions)
spark_f1 = evaluator_f1.evaluate(predictions)

print("\n" + "=" * 60)
print("               MODEL EVALUATION METRICS")
print("=" * 60)
print(f"Total Test Set Records Evaluated: {total}")
print(f"Accuracy:  {accuracy * 100:.2f}% (Spark Evaluator: {spark_acc * 100:.2f}%)")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall:    {recall * 100:.2f}%")
print(f"F1-Score:  {f1_score * 100:.2f}% (Spark Evaluator: {spark_f1 * 100:.2f}%)")

print("\n---------------- CONFUSION MATRIX ----------------")
print(f"True Positives  (TP - Correctly identified Spam):      {tp}")
print(f"True Negatives  (TN - Correctly identified Authentic): {tn}")
print(f"False Positives (FP - Authentic flagged as Spam):      {fp}")
print(f"False Negatives (FN - Spam missed as Authentic):       {fn}")
print("--------------------------------------------------")

print("\nSample Predictions (1.0 = SPAM, 0.0 = AUTHENTIC):")
predictions.select("reviewText", "rating", "review_len", "helpful_votes", "label", "prediction") \
           .show(10, truncate=40)

# Save metrics to JSON for the Web Dashboard
metrics_dict = {
    "total_test": total,
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1_score * 100, 2),
    "confusion_matrix": {
        "tp": tp, "tn": tn, "fp": fp, "fn": fn
    }
}

with open("/tmp/spam_metrics.json", "w") as f:
    json.dump(metrics_dict, f, indent=4)

print("Metrics saved to /tmp/spam_metrics.json successfully!")
print("======================================================================")

spark.stop()
