from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import sys

if len(sys.argv) != 3:
    print("Usage: spark-submit predict_emr.py <test_data_path> <model_path>")
    sys.exit(1)

test_path = sys.argv[1]
model_path = sys.argv[2]

spark = SparkSession.builder.appName("WineQualityPredictionEMR").getOrCreate()
df = spark.read.csv(test_path, header=True, inferSchema=True)

feature_cols = [col for col in df.columns if col != "quality"]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
df = assembler.transform(df)

model = LogisticRegressionModel.load(model_path)
predictions = model.transform(df)

evaluator = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction", metricName="f1")
f1_score = evaluator.evaluate(predictions)
print(f"🔹 Prediction Completed. F1 Score: {f1_score:.4f}")

spark.stop()
