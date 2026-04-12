# Banking Digital Sales Analytics Pipeline

## 📌 Project Overview
This project implements an end-to-end data engineering pipeline for a banking sales funnel. It automates the flow of data from raw capture to executive-level insights, utilizing Python for ingestion and dbt (data build tool) for robust, tested transformations within Snowflake.

## 🏗️ Architecture & Orchestration
The project follows the **Medallion Architecture** to ensure data quality and separation of concerns, orchestrated entirely via **Dockerized Airflow**:

- **Orchestration Layer:** Managed by **Apache Airflow** using the **Astronomer Cosmos** provider to dynamically render dbt models as an Airflow DAG.
- **Bronze (Staging):** Schema enforcement and cleaning of raw landing data.
- **Silver (Intermediate):** High-level business logic and behavioral filtering.
- **Gold (Marts):** Production-ready tables optimized for BI tools and ROI analysis.

![Airflow DAG Lineage Proof](snapshots\airflow_dag_lineage.png)
*Figure 1: Airflow DAG Lineage rendered by Cosmos, showing task groups and execution dependencies.*

## 🚀 Components

### 1. Containerization & Environment
- **Docker:** The entire stack—Airflow Webserver, Scheduler, and dbt environment—is containerized to ensure consistent execution across different environments.
- **Virtual Environment:** Python dependencies are managed within a `venv` and injected into Docker containers to support the `apache-airflow-providers-snowflake` and `astronomer-cosmos` packages.

### 2. Ingestion (`/ingest_to_snowflake.py`)
- Establishes a secure connection to Snowflake.
- Initializes the `RAW_ZONE` and landing tables.
- Ingests synthetic web events and CRM conversion data to simulate a real-world stream.

### 3. Transformation (`/models`)
The pipeline structure is managed as a Directed Acyclic Graph (DAG). While the UI simplifies the view into task groups, the project contains **13 total nodes** (5 models, 6 tests, and 2 sources) identified during parsing.

![dbt Model Lineage Graph](snapshots\conversion_stream_pipeline_lineage_graph.png)
*Figure 2: Grid view showing successful state across the pipeline stages.*

- **Staging:** Renames fields and enforces **Core Integrity Tests** (Unique, Not_Null).
- **Intermediate (`int_lost_opportunities.sql`):** Uses a **Left Anti-Join** to isolate high-intent users who exited the funnel—creating a "re-targeting" list.
- **Marts (`mart_marketing_roi.sql`):** Aggregates data by channel for real-time ROI metrics, materialized for BI performance.

## 🛠️ Challenges Encountered & Solutions

| Challenge | Impact | Solution |
| :--- | :--- | :--- |
| **Missing Airflow Providers** | DAGs failed to parse because the Snowflake provider was missing from the container image. | Performed a `docker exec` to manually install `apache-airflow-providers-snowflake`. |
| **dbt Account Authentication** | dbt reported that `'account' is a required property`, even when defined in the Airflow UI fields. | Modified the Airflow Connection **Extra Fields JSON** to explicitly pass the account locator. |
| **Role Permissions** | Tasks failed because no Snowflake Role was assigned. | Updated connection configuration to explicitly use the `ACCOUNTADMIN` role. |
| **DAG Reserialization** | Changes to the dbt project weren't immediately reflecting in the Airflow UI. | Used `airflow dags reserialize` via Docker CLI to force a cache refresh. |

## 🧪 Data Contracts & Quality
- **Automated Testing:** The pipeline executes **6 data tests** during every run, checking for nulls and duplicates on keys like `USER_ID` and `CONV_ID`.
- **Asset Lineage:** Cosmos provides a visual lineage in the Airflow UI, ensuring that if a staging test fails, downstream Marts are blocked.
- **Observability:** Successful runs generate **Asset Events** that map data lineage directly in the Airflow UI.


## ⚙️ Setup & Execution

### 1. Prerequisites
- **Docker Desktop:** Required for running the Airflow stack.
- **Snowflake Account:** You will need a database named `RAW_ZONE` and appropriate credentials.
- **Python 3.9+:** For local ingestion and environment management.

### 2. Environment Setup
Clone the repository and create a virtual environment to manage dependencies:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
```

### 3. Database Ingestion
Run the ingestion script to seed Snowflake with the raw banking data:
```bash
python ingest_to_snowflake.py
```

### 4. Orchestration with Docker & Airflow
This project uses the Astronomer CLI/Docker to manage Airflow.
```bash
# Start the Airflow environment
astro dev start

# Access the Airflow UI
# Navigate to http://localhost:8080 (Username/Password: admin/admin)
# Install dependencies
pip install -r requirements.txt
```

### 5. Running the Pipeline
- In the Airflow UI, ensure the ```snowflake_default``` connection is configured.

- If dbt providers are missing in the container, run:

```bash
docker ps  # Get the scheduler container ID
docker exec -it <container_id> pip install apache-airflow-providers-snowflake
```
- Trigger the ```banking_transformation_pipeline``` DAG.

## 📊 Key Insights & Value
- **Operational Efficiency:** Actionable re-targeting lists generated via `int_lost_opportunities`.
- **Data Observability:** Automated testing guarantees that only validated data reaches executive dashboards.
- **Modern Stack Mastery:** Demonstrates an integrated workflow using **Docker, Airflow, dbt, and Snowflake**.

## 🖼️ Infrastructure Proofs

### Execution Success
Full proof of a successful run. Note the 5 "Created Asset Events" representing the physical creation of staging, intermediate, and mart datasets in Snowflake.
![Successful Run](snapshots\successful_run.png)

### Snowflake Infrastructure Configuration
 Documented configuration of the Snowflake connection used to bridge Airflow and the Data Warehouse (Account ID redacted for security).
![Snowflake Connection Configuration](snapshots\snowflake_connection_configuration.png)