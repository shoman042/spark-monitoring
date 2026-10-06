from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import time

spark = SparkSession.builder.appName("SparkJobMonitoring").getOrCreate()

customers = spark.read.csv("customers.csv", header=True, inferSchema=True)
orders = spark.read.csv("orders.csv", header=True, inferSchema=True)

customers_clean = customers.filter(F.col("age") >= 18)

orders_clean = (orders
                .filter(F.trim(F.col("status")) == "Completed")
                .filter(F.col("quantity") >= 2))

result = (orders_clean
          .join(customers_clean, "customer_id")
          .withColumn("revenue", F.col("quantity") * F.col("price"))
          .groupBy("country")
          .agg(F.sum("revenue").alias("total_revenue"))
          .orderBy(F.col("total_revenue").desc()))

result.show()


time.sleep(300)

spark.stop()