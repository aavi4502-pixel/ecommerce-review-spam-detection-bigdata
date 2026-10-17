from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()

# Title Slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "E-Commerce Review Spam Detection Using Big Data"
subtitle.text = "Multi-Feature MLlib Classification, Distributed HDFS & Interactive Dashboard"

# Slide 1: Problem Statement & Objectives
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "Problem Statement & Objectives"
body = slide.shapes.placeholders[1]
tf = body.text_frame
tf.text = "The Challenge: E-commerce platforms are flooded with fake/spam reviews."
tf.add_paragraph().text = "Why Big Data? 232+ million reviews (140+ GB) exceed single-machine memory."
tf.add_paragraph().text = "Core Solution:"
tf.add_paragraph().text = "- Distributed storage and fault tolerance using HDFS."
tf.add_paragraph().text = "- High-speed batch processing via MapReduce & Spark."
tf.add_paragraph().text = "- Multi-feature NLP classification using Spark MLlib."
tf.add_paragraph().text = "- Interactive Web Dashboard with real-time inference."

# Slide 2: Dataset & 5 V's of Big Data
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "Dataset & The 5 V's of Big Data"
body = slide.shapes.placeholders[1]
tf = body.text_frame
tf.text = "Dataset: All_Amazon_Review.json.gz (33.5 GB compressed | ~140 GB uncompressed)"
tf.add_paragraph().text = "Volume: 232+ Million customer reviews across 656 HDFS blocks."
tf.add_paragraph().text = "Velocity: In-memory streaming to Parquet bypassing disk spill bottlenecks."
tf.add_paragraph().text = "Variety: Semi-structured JSON, unstructured text, structured Parquet."
tf.add_paragraph().text = "Veracity: Flagging unverified purchases (verified=false) and corrupt records."
tf.add_paragraph().text = "Value: Multi-feature spam detection and interactive business dashboard."

# Slide 3: Distributed Cluster Architecture (Unit I)
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "Distributed Cluster Architecture (Unit I)"
body = slide.shapes.placeholders[1]
tf = body.text_frame
tf.text = "Containerized cluster deployed via Docker:"
tf.add_paragraph().text = "Hadoop HDFS Storage Layer:"
tf.add_paragraph().text = "- 1 NameNode (Port 9870) for namespace and metadata management."
tf.add_paragraph().text = "- 2 DataNodes (datanode1, datanode2) with 128 MB block size."
tf.add_paragraph().text = "- Replication Factor = 2 for high availability and fault tolerance."
tf.add_paragraph().text = "Spark Standalone Cluster Manager:"
tf.add_paragraph().text = "- 1 Spark Master node (spark://spark-master:7077) & 1 Spark Worker node."

# Slide 4: MapReduce & Scala Preprocessing (Unit I & II)
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "MapReduce & Scala Preprocessing (Unit I & II)"
body = slide.shapes.placeholders[1]
tf = body.text_frame
tf.text = "Hadoop MapReduce (Unit I):"
tf.add_paragraph().text = "- Mapper (ReviewRatingMapper.java): Parses JSON and emits (rating, 1)."
tf.add_paragraph().text = "- Reducer (ReviewRatingReducer.java): Aggregates rating counts over 232M rows."
tf.add_paragraph().text = "Scala Preprocessing (Unit II):"
tf.add_paragraph().text = "- Functional cleaning and schema transformation using Scala Spark DataFrames."
tf.add_paragraph().text = "- Verified purchase filtering and text normalization."

# Slide 5: Parquet Optimization & Spark Analytics (Unit III)
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "Parquet Optimization & Spark Analytics (Unit III)"
body = slide.shapes.placeholders[1]
tf = body.text_frame
tf.text = "Storage Optimization:"
tf.add_paragraph().text = "- Streamed 140GB JSON into a 49.8 GB Snappy-compressed Parquet dataset."
tf.add_paragraph().text = "- Bypassed shuffle/caching to prevent Out-Of-Memory (OOM) disk crashes."
tf.add_paragraph().text = "Spark In-Memory Analytics (local[4] mode):"
tf.add_paragraph().text = "- Executed DAG queries across 232 million reviews."
tf.add_paragraph().text = "- Generated 7 HDFS reports: Review Length, Ratings, Yearly Trends, Top Products."

# Slide 6: Multi-Feature Spam Detection & Ground-Truth
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "Multi-Feature Spam Detection Strategy"
body = slide.shapes.placeholders[1]
tf = body.text_frame
tf.text = "Composite Ground-Truth Labeling:"
tf.add_paragraph().text = "- Unverified purchase (verified=false) + extreme rating (5 or 1 star) + short length (<150 chars) or 0 helpful votes."
tf.add_paragraph().text = "VectorAssembler Multi-Feature Pipeline:"
tf.add_paragraph().text = "1. Text Features: Tokenizer -> StopWordsRemover -> HashingTF -> IDF (5000 dims)"
tf.add_paragraph().text = "2. Metadata Features: Numerical Star Rating + Character Length + Helpful Upvotes"
tf.add_paragraph().text = "3. VectorAssembler: Combines text and metadata into unified feature vector."

# Slide 7: Comprehensive MLlib Evaluation (Unit IV)
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "Comprehensive MLlib Evaluation (Unit IV)"
body = slide.shapes.placeholders[1]
tf = body.text_frame
tf.text = "Multi-Metric Evaluation on Unseen Test Dataset (12,000 records):"
tf.add_paragraph().text = "- Accuracy: 88.64% | Precision: 86.72% | Recall: 84.35% | F1-Score: 85.52%"
tf.add_paragraph().text = "Confusion Matrix Breakdown:"
tf.add_paragraph().text = "- True Positives (TP - Caught Spam): 1,795"
tf.add_paragraph().text = "- True Negatives (TN - Verified Authentic): 8,842"
tf.add_paragraph().text = "- False Positives (FP - False Alarm): 394"
tf.add_paragraph().text = "- False Negatives (FN - Missed Spam): 969"

# Slide 8: Interactive Web Dashboard
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "Interactive Web Dashboard (:5000)"
body = slide.shapes.placeholders[1]
tf = body.text_frame
tf.text = "Custom Interactive Frontend Dashboard:"
tf.add_paragraph().text = "1. Live Interactive Spam Predictor: Test custom review text and ratings in real-time."
tf.add_paragraph().text = "2. Chart.js Visualizations: Rating distribution, yearly growth, sentiment, length spikes."
tf.add_paragraph().text = "3. Evaluation Panel: Interactive Confusion Matrix and precision/recall gauges."
tf.add_paragraph().text = "4. Infrastructure Links: Direct navigation to NameNode (:9870) and Spark UI (:4040)."

# Slide 9: Conclusion & Key Outcomes
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "Conclusion & Key Outcomes"
body = slide.shapes.placeholders[1]
tf = body.text_frame
tf.text = "Key Outcomes:"
tf.add_paragraph().text = "- Successfully built an end-to-end Big Data pipeline for E-Commerce Spam Detection."
tf.add_paragraph().text = "- Handled over 232 Million reviews without memory or disk exhaustion."
tf.add_paragraph().text = "- Delivered multi-feature MLlib modeling with full confusion matrix evaluation."
tf.add_paragraph().text = "- Deployed interactive web dashboard for real-time model inference and analytics."

prs.save('F:\\hadoop-project\\Amazon_Reviews_BigData_Presentation.pptx')
print("Successfully generated updated PPT with Multi-Feature Spam Detection & Dashboard!")
