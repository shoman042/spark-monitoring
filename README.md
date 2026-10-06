Spark Job Monitoring with Prometheus & Grafana

An end-to-end observability project for an Apache Spark application, combining PySpark data processing with Prometheus metrics collection and Grafana visualization.

Overview

This project demonstrates how to monitor a Spark application while it is processing real datasets.

The application reads customer and order data, applies filtering and transformation logic, joins the datasets, calculates revenue, and produces total revenue by country.

At the same time, Spark exposes runtime metrics through its Prometheus-compatible metrics endpoints. Prometheus collects these metrics, while Grafana provides a dashboard for monitoring job execution and application performance.

Architecture

                         ┌──────────────────────┐
                         │     customers.csv    │
                         └──────────┬───────────┘
                                    │
                                    │
                         ┌──────────▼───────────┐
                         │                      │
                         │   PySpark Application│
                         │      spark_job.py    │
                         │                      │
                         └──────────┬───────────┘
                                    │
                         Spark Metrics / HTTP :4040
                                    │
                         ┌──────────▼───────────┐
                         │      Prometheus      │
                         │       :9090          │
                         └──────────┬───────────┘
                                    │
                               PromQL queries
                                    │
                         ┌──────────▼───────────┐
                         │       Grafana        │
                         │        :3000         │
                         └──────────────────────┘

                         ┌──────────────────────┐
                         │      orders.csv      │
                         └──────────────────────┘

Prometheus and Grafana run as Docker containers, while the Spark application runs locally on the Windows host. The containers communicate with the host Spark application through host.docker.internal.

Project Objectives

The project was designed to demonstrate the complete monitoring workflow for a Spark application:

Build a PySpark data-processing application.

Execute the application using spark-submit.

Configure Spark to expose Prometheus-compatible metrics.

Configure Prometheus to scrape Spark metrics.

Connect Prometheus to Grafana.

Build a Grafana dashboard for Spark execution and performance monitoring.

Verify the collected metrics and resulting dashboard values.

Technology Stack

Component

Version / Technology

Apache Spark

4.2.0

PySpark

4.2.0

Python

3.13.12

Java

OpenJDK 17.0.20.1 (Temurin)

Prometheus

Docker image

Grafana

Docker image

Docker

29.2.1

Docker Compose

Used for monitoring services

Operating System

Windows

Development Environment

Visual Studio Code

Repository Structure

spark-monitoring/
│
├── spark_job.py
├── metrics.properties
├── prometheus.yml
├── docker-compose.yml
├── .gitignore
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
└── screenshots/
    ├── WhatsApp Image 2026-10-06 at 4.03.11 PM.jpeg
    ├── WhatsApp Image 2026-10-06 at 4.03.41 PM.jpeg
    ├── WhatsApp Image 2026-10-06 at 4.04.03 PM.jpeg
    └── WhatsApp Image 2026-10-06 at 4.06.51 PM.jpeg

Key Components

spark_job.py
PySpark application responsible for reading, filtering, joining, transforming, and aggregating the datasets.

metrics.properties
Configures Spark's PrometheusServlet metrics sink and the HTTP paths used to expose Spark metrics.

prometheus.yml
Defines Prometheus scrape configuration for the Spark driver and executor endpoints.

docker-compose.yml
Runs Prometheus and Grafana as Docker services.

monitoring/
Contains the exported Grafana dashboard configuration.

docs/
Contains the detailed project documentation in PDF and DOCX formats.

Data Processing

The Spark application processes two CSV datasets.

Customers

The customer dataset contains:

customer_id

name

country

age

Orders

The orders dataset contains:

order_id

customer_id

product

category

quantity

price

status

Transformation Flow

The application performs the following processing sequence:

Customers + Orders
        │
        ▼
Filter customers: age >= 18
        │
        ▼
Filter orders: status = Completed
        │
        ▼
Filter orders: quantity >= 2
        │
        ▼
Join on customer_id
        │
        ▼
Calculate revenue
        │
        ▼
Group by country
        │
        ▼
SUM(total revenue)
        │
        ▼
Sort descending

Revenue is calculated as:

revenue = quantity × price

The application then remains active for 300 seconds, keeping the Spark UI and metrics endpoints available for monitoring.

Running the Project

1. Start the Monitoring Stack

From the project root:

docker compose up -d

This starts:

Prometheus on port 9090

Grafana on port 3000

2. Start the Spark Application

Run:

spark-submit --conf spark.ui.prometheus.enabled=true --conf spark.metrics.conf=metrics.properties --conf spark.metrics.namespace=spark spark_job.py

The Spark application exposes its metrics through the Spark UI on port 4040.

3. Access the Services

Service

URL

Spark UI

http://localhost:4040

Prometheus

http://localhost:9090

Grafana

http://localhost:3000

Monitoring Configuration

Spark Metrics

The project enables the Prometheus metrics endpoint through Spark configuration.

The configured metrics paths include:

/metrics/driver/prometheus
/metrics/executors/prometheus
/metrics/master/prometheus
/metrics/applications/prometheus

These endpoints are served by the Spark UI while the application is running.

Prometheus

Prometheus is configured with a 5-second global scrape interval and collects metrics from:

host.docker.internal:4040

The configured scrape paths include:

/metrics/driver/prometheus/
/metrics/executors/prometheus/

Grafana

Prometheus is configured as the Grafana data source using:

http://prometheus:9090

The Grafana dashboard is provided as an exported JSON file under:

monitoring/

Grafana Dashboard

Spark Job Monitoring Dashboard

The dashboard contains six panels covering job execution, failures, executor information, CPU-related activity, and JVM memory.

Panel

Purpose

PromQL

Running Jobs

Current active Spark jobs

metrics_spark_driver_DAGScheduler_job_activeJobs_Number

Completed Jobs

Completed jobs derived from total and active jobs

metrics_spark_driver_DAGScheduler_job_allJobs_Number - metrics_spark_driver_DAGScheduler_job_activeJobs_Number

Failed Jobs

Failed stages used as the available failure indicator

metrics_spark_driver_DAGScheduler_stage_failedStages_Number

CPU Usage

Estimated CPU-related activity from executor task duration

rate(metrics_executor_totalDuration_seconds_total[1m])

Executors

Number of reported Spark executors

count(metrics_executor_totalCores)

JVM Heap Memory

Executor JVM heap memory usage

metrics_executor_JVMHeapMemory_bytes

The dashboard uses the metrics exposed by the configured Spark endpoints. "Completed Jobs" is derived because a dedicated completed-jobs metric was not available, while "Failed Jobs" uses failed stages as the closest available failure indicator.

Verified Results

Data Processing Output

The Spark application produced the following total revenue by country:

Country

Total Revenue

Egypt

122,485

France

52,786

USA

38,068

Canada

30,753

Germany

20,084

UAE

18,115

India

11,559

UK

11,164

Saudi Arabia

9,545

Monitoring Verification

Prometheus successfully reported both configured Spark scrape targets as UP.

The dashboard displayed the following values during execution:

Metric

Observed Value

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

Because Spark is running in local mode, the single reported executor is the driver process itself.

Implementation Notes

Spark Submit

On Windows, the spark-submit.cmd executable was located inside the installed PySpark package. The required Scripts/bin directory was added to the terminal PATH so the application could be launched with spark-submit.cmd.

Prometheus 404 Issue

The Spark driver target initially returned HTTP 404 Not Found because the configured scrape path did not match the driver metrics endpoint.

The configuration was corrected to:

/metrics/driver/prometheus/

After the correction, the Spark driver target reported UP.

Multiple Application Series

Running the Spark application multiple times produced different application_id values. This caused CPU and JVM heap queries to expose more than one series.

The documentation identified aggregation with sum() as a way to obtain a single aggregated value when required.

Limitations

This project intentionally runs Spark in local mode. As a result:

There are no separate worker executors.

The executor count remains one.

Spark metrics are available only while the application and Spark UI are running.

The application pauses for 300 seconds to keep the metrics endpoints available.

The Failed Jobs panel represents failed stages rather than a direct failed-jobs metric.

The CPU Usage panel is an estimate based on executor task execution time rather than a direct operating-system CPU measurement.

Project Documentation

For the complete implementation details, configuration explanations, verification results, challenges, and limitations, see:

docs/Spark_Monitoring_Project_Documentation.pdf

docs/Spark_Monitoring_Project_Documentation.docx

The repository also includes the exported Grafana dashboard and project screenshots.

Project Context

Samsung Innovation Campus

This project demonstrates the integration of:

Apache Spark
      +
Prometheus
      +
Grafana
      +
Docker

to create a practical monitoring workflow around a Spark data-processing application.

Author

Yusuf Ahmed Shoman

Computer Engineering Student | Data Engineering Track

GitHub: @shoman042
