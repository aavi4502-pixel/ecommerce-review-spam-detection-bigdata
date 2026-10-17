# 🛒 E-Commerce Review Spam Detection Using Big Data Frameworks

[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.1.1-orange.svg)](https://spark.apache.org/)
[![Hadoop HDFS](https://img.shields.io/badge/Hadoop%20HDFS-3.2.1-yellow.svg)](https://hadoop.apache.org/)
[![Scala](https://img.shields.io/badge/Scala-2.12-red.svg)](https://www.scala-lang.org/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end Big Data engineering and machine learning system for detecting fake reviews and opinion spam across **232.8 Million Amazon Customer Reviews (140+ GB)** using a multi-node **Hadoop HDFS** storage cluster, **Scala** preprocessing, in-memory **Apache Spark DAG** execution, and **Spark MLlib** distributed classifiers.

---

## 📌 Deliverables Included in this Repository

| Deliverable | File Link | Description |
|---|---|---|
| 📊 **Final Review Presentation** | [`Amazon_Reviews_BigData_Presentation.pptx`](./Amazon_Reviews_BigData_Presentation.pptx) | Complete 10-slide widescreen review presentation deck. |
| 📄 **Full Technical Report** | [`Ecommerce_Review_Spam_Detection_Project_Report.docx`](./Ecommerce_Review_Spam_Detection_Project_Report.docx) | Formal 11-chapter academic project report. |
| 📘 **Project Explanation Guide** | [`PROJECT_EXPLANATION.md`](./PROJECT_EXPLANATION.md) | Comprehensive technical walkthrough & viva question bank. |
| 💻 **Scala ETL Pipeline** | [`scala/AmazonPreprocessing.scala`](./scala/AmazonPreprocessing.scala) | Native JVM data cleansing and sentiment labeling. |
| ⚙️ **Hadoop MapReduce Job** | [`mapreduce/`](./mapreduce/) | Java Mapper, Reducer, and Driver for rating distribution. |
| 🤖 **Spark MLlib Classifier** | [`mllib_advanced_spam.py`](./mllib_advanced_spam.py) | Multi-feature NLP & behavioral Logistic Regression pipeline. |
| 🌐 **Interactive Web Dashboard** | [`dashboard/`](./dashboard/) | Flask & Chart.js live spam prediction web interface. |

---

## 🏗️ System Architecture Pipeline

```
               [ RAW DATA SOURCE ]
       Amazon Customer Reviews (140+ GB JSON)
                         │
                         ▼
             [ DISTRIBUTED STORAGE ]
           Hadoop HDFS 3.2.1 Cluster
    NameNode (:9870)  ───►  DataNode 1 & DataNode 2
   (Metadata & Namespace)    (161 GB Replicated Parquet)
                         │
                         ▼
            [ PROCESSING & ANALYTICS ]
      Apache Spark 3.1.1 + Scala 2.12 + MapReduce
     ├── MapReduce: Initial Token Distribution
     ├── Scala: Functional Cleaning & Type-Safe ETL
     └── Spark DAG Engine: Columnar Filtering (Snappy)
                         │
                         ▼
             [ MACHINE LEARNING PIPELINE ]
                     Spark MLlib
   Tokenizer ──► StopWords ──► HashingTF (5000) ──► IDF ──┐
   Rating + Length + Helpful Votes (Metadata) ────────────┴──► VectorAssembler ──► LogisticRegression
                         │
                         ▼
             [ PRESENTATION & OUTPUTS ]
     ├── 7 HDFS CSV Analytics Reports
     ├── Spark Master & App UI (Ports 8080 & 4040)
     └── Interactive Web Dashboard (Flask / Port 5000)
```

---

## 📊 The 5 V's of Big Data Addressed

1. **VOLUME**: 232.8 Million rows of text and metadata (140+ GB uncompressed text; 161 GB replicated HDFS storage).
2. **VARIETY**: Unstructured text (`reviewText`), semi-structured JSON lines, columnar Parquet, and tabular CSV reports.
3. **VELOCITY**: Zero-shuffle streaming into Parquet without intermediate disk spilling; high-throughput in-memory DAG analytics.
4. **VERACITY**: Directly filtering fake reviews, bot repetitions, unverified buyers, and rating manipulation.
5. **VALUE**: Restoring consumer trust in online shopping, protecting honest sellers, and preventing financial fraud.

---

## 📈 Model Performance & Evaluation

Evaluated across an unseen 20% holdout test partition (**12,000 records**):

| Metric | Baseline Model (Text-Only) | Multi-Feature Model (Text + Metadata) | Improvement |
|---|---|---|---|
| **Accuracy** | 81.03% | **88.64%** | **+7.61%** |
| **Precision (Spam)** | 78.20% | **86.72%** | **+8.52%** |
| **Recall (Spam)** | 74.50% | **84.35%** | **+9.85%** |
| **F1-Score** | 76.30% | **85.52%** | **+9.22%** |
| **ROC AUC** | 0.8640 | **0.9312** | **+0.0672** |

### Exact Confusion Matrix (12,000 Test Records)

| Actual Class | Predicted AUTHENTIC (0.0) | Predicted SPAM (1.0) | Total Actual |
|---|---|---|---|
| **Actual AUTHENTIC (0.0)** | **6,612 (TN)** *(True Negatives)* | **616 (FP)** *(False Positives)* | 7,228 |
| **Actual SPAM (1.0)** | **747 (FN)** *(False Negatives)* | **4,025 (TP)** *(True Positives)* | 4,772 |
| **Total** | 7,359 | 4,641 | **12,000 Total** |

---

## 🚀 Quickstart & Reproduction

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Linux Containers)
* Python 3.9+

### 2. Start Cluster & Services
Double-click `start_for_presentation.bat` or run:
```bash
# 1. Start Docker Containers
docker start namenode datanode1 datanode2 spark-master spark-worker

# 2. Disable HDFS Safe Mode
docker exec namenode hdfs dfsadmin -safemode leave

# 3. Launch Spark Showcase
docker cp presentation_showcase.py spark-master:/tmp/presentation_showcase.py
docker exec -d spark-master bash -c "/spark/bin/spark-submit /tmp/presentation_showcase.py > /tmp/showcase.log 2>&1"

# 4. Launch Web Dashboard
python dashboard/run_dashboard.py
```

### 3. Access Live Web Interfaces
* **Interactive Dashboard**: `http://localhost:5000/index.html`
* **Spark Master Web UI**: `http://localhost:8080`
* **Spark Jobs & DAG UI**: `http://localhost:4040/jobs/`
* **Hadoop HDFS NameNode**: `http://localhost:9870/dfshealth.html`

---

## 👥 Authors & Acknowledgments

* **Student / Team**: Mathangi Avinash (`aavi4502-pixel`)
* **Course**: Big Data Analytics (23AID302)
* **Dataset**: Julian McAuley, UCSD (*Justifying Recommendations using Distantly-Labeled Reviews and Fine-Grained Aspects*, EMNLP 2019)
