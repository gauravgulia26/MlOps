# 🛠️ ETL Pipeline with Airflow, API Handling & Dockerized PostgreSQL 🚀

This project demonstrates an **ETL pipeline** using **Apache Airflow**, which fetches data from an **API**, transforms the data, and loads it into a **PostgreSQL database** running inside a **Docker container**. Additionally, the pipeline includes **API health check handling** to ensure smooth operation.

## 📦 Requirements

Before running the pipeline, make sure you have the following tools installed:
- **Docker** 🐳
- **Apache Airflow** ✈️
- **PostgreSQL** (within Docker) 🍇
- Python Libraries:
  - `requests` 🌐
  - `psycopg2` 📚
  - `airflow` 🧑‍💻

## 🚀 Features

- **ETL Pipeline**:
  - Extracts data from an external **API** 🖥️.
  - Transforms the data as per your business logic 🔄.
  - Loads the data into a **PostgreSQL** database running inside a **Docker container** 🗄️.

- **API Health Check** 🩺:
  - Implements an API handling feature to check if the API is **up or down**.
  - Sends a notification if the API is not reachable 🚫.

- **Dockerized PostgreSQL** 🍷:
  - PostgreSQL database is containerized using Docker for easy deployment and scalability.
