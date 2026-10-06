Spark Job Monitoring with Prometheus and Grafana

A simple end-to-end Apache Spark monitoring project that demonstrates how to process customer and order data with PySpark and monitor Spark execution and performance using Prometheus and Grafana.

📌 Project Overview

The project consists of a PySpark application that processes two CSV datasets:

customers.csv

orders.csv

The Spark application filters and joins the data, calculates revenue by country, and displays the results.

At the same time, Spark exposes monitoring metrics that are collected by Prometheus and visualized through a Grafana dashboard.

The monitoring pipeline is:

PySpark Application
        │
        │ Spark Metrics
        ▼
    Prometheus
        │
        │ PromQL
        ▼
      Grafana

🎯 Objectives

Develop a PySpark application for processing customer and order data.

Execute the application using spark-submit.

Configure Spark to expose Prometheus-compatible metrics.

Collect Spark metrics using Prometheus.

Connect Prometheus to Grafana.

Build a Grafana dashboard with six monitoring panels.

🛠️ Technologies

Apache Spark 4.2.0

PySpark 4.2.0

Python 3.13.12

OpenJDK 17.0.20.1

Prometheus

Grafana

Docker 29.2.1

Docker Compose

Windows

Visual Studio Code

📁 Project Structure

spark-monitoring/
│
├── spark_job.py
├── docker-compose.yml
├── prometheus.yml
├── metrics.properties
│
├── data/
│   ├── customers.csv
│   └── orders.csv
│
├── monitoring/
│   └── Spark Job Monitoring Dashboard-1791292196622.json
│
├── docs/
│   ├── Spark_Monitoring_Project_Documentation.pdf
│   └── Spark_Monitoring_Project_Documentation.docx
│
├── screenshots/
│   ├── WhatsApp Image 2026-10-06 at 4.03.11 PM.jpeg
│   ├── WhatsApp Image 2026-10-06 at 4.03.41 PM.jpeg
│   ├── WhatsApp Image 2026-10-06 at 4.04.03 PM.jpeg
│   └── WhatsApp Image 2026-10-06 at 4.06.51 PM.jpeg
│
└── .gitignore

⚙️ Spark Data Processing

The PySpark application performs the following steps:

Reads the customer and order CSV files.

Filters customers whose age is greater than or equal to 18.

Filters orders with status Completed.

Trims whitespace from the order status before filtering.

Keeps orders with quantity greater than or equal to 2.

Joins orders with customers using customer_id.

Calculates order revenue:

revenue = quantity × price

Groups the results by country.

Calculates total revenue for each country.

Sorts the results from highest to lowest revenue.

The application then remains active for 300 seconds so that Spark metrics remain available for Prometheus and Grafana.

🚀 Running the Spark Application

spark-submit --conf spark.ui.prometheus.enabled=true --conf spark.metrics.conf=metrics.properties --conf spark.metrics.namespace=spark spark_job.py

Spark exposes the metrics through its Spark UI on port 4040.

📊 Prometheus Configuration

Prometheus scrapes the Spark metrics every 5 seconds.

The configured Spark endpoints include:

/metrics/driver/prometheus/
/metrics/executors/prometheus/

Prometheus runs on:

http://localhost:9090

The Spark application runs on the host machine while Prometheus runs inside Docker.

Docker containers access the host through:

host.docker.internal

📈 Grafana Dashboard

The project includes a Grafana dashboard named:

Spark Job Monitoring Dashboard

The dashboard contains six panels:

Panel

PromQL Query

Running Jobs

metrics_spark_driver_DAGScheduler_job_activeJobs_Number

Completed Jobs

metrics_spark_driver_DAGScheduler_job_allJobs_Number - metrics_spark_driver_DAGScheduler_job_activeJobs_Number

Failed Jobs

metrics_spark_driver_DAGScheduler_stage_failedStages_Number

CPU Usage

rate(metrics_executor_totalDuration_seconds_total[1m])

Executors

count(metrics_executor_totalCores)

JVM Heap Memory

metrics_executor_JVMHeapMemory_bytes

The dashboard JSON is available in:

monitoring/

🐳 Running Prometheus and Grafana

Start the monitoring stack with:

docker compose up -d

Prometheus:

http://localhost:9090

Grafana:

http://localhost:3000

Prometheus is configured as the Grafana data source using:

http://prometheus:9090

📊 Results

The Spark application produced the following total revenue by country:

Country

Total Revenue

Egypt

122485

France

52786

USA

38068

Canada

30753

Germany

20084

UAE

18115

India

11559

UK

11164

Saudi Arabia

9545

Prometheus successfully reported both Spark scrape targets as UP.

During execution, the Grafana dashboard displayed:

Metric

Value

Running Jobs

0

Completed Jobs

7

Failed Jobs

0

CPU Usage

43.5%

Executors

1

JVM Heap Memory

164 MiB

Because the application runs in local mode, the single reported executor is the driver process itself.

🔧 Challenges and Solutions

1. spark-submit was not recognized

The spark-submit.cmd executable was located inside the installed PySpark package.

The required Scripts/bin directory was added to the terminal PATH and spark-submit.cmd was used.

2. Prometheus returned HTTP 404

The initial Spark driver metrics path was incorrect.

The configuration was changed to:

/metrics/driver/prometheus/

After the correction, the Spark driver target became UP.

3. No direct completed-jobs metric

Spark did not expose a dedicated completed-jobs metric.

Therefore, completed jobs were calculated as:

Total Jobs - Active Jobs

4. No direct failed-jobs metric

The available Spark metrics did not provide a ready-made failed-jobs metric.

The dashboard therefore uses the failed stages metric as the closest available indicator.

⚠️ Limitations

The Spark application runs in local mode.

The executor count is therefore always one.

Spark metrics are available only while the Spark application and Spark UI are running.

The application pauses for 300 seconds to keep the metrics endpoints available.

The Failed Jobs panel represents failed stages rather than failed jobs.

CPU Usage is an estimate based on executor task execution time rather than a direct CPU measurement.

📚 Documentation

Detailed project documentation is available in the docs/ directory in both PDF and DOCX formats.

👨‍💻 Project

Spark Job Monitoring using Prometheus and Grafana

Built as part of Samsung Innovation Campus.
