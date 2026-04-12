# Banking Digital Sales Analytics Pipeline

## 📌 Project Overview
This project implements an end-to-end data engineering pipeline for a banking sales funnel. It automates the flow of data from raw capture to executive-level insights, utilizing Python for ingestion and dbt (data build tool) for robust, tested transformations within Snowflake.

## 🏗️ Architecture
The project follows the **Medallion Architecture** to ensure data quality and separation of concerns:
- **Bronze (Staging):** Schema enforcement and cleaning of raw landing data.
- **Silver (Intermediate):** High-level business logic and behavioral filtering.
- **Gold (Marts):** Production-ready tables optimized for BI tools and ROI analysis.



## 🚀 Components

### 1. Ingestion (`/ingest_to_snowflake.py`)
A standalone Python script that acts as the pipeline's entry point. It:
- Establishes a secure connection to Snowflake using `snowflake-connector-python`.
- Initializes the `RAW_ZONE` and landing tables.
- Ingests synthetic web events and CRM conversion data, simulating a real-world data stream for processing.

### 2. Transformation (`/models`)
The dbt transformation suite is organized into three distinct layers to maintain a clean Directed Acyclic Graph (DAG):

* **Staging (`/models/staging`):** * Renames and casts raw fields (e.g., standardizing `TS` to `event_at`).
    * Enforces **Core Integrity Tests** (Unique, Not_Null) to ensure the foundation of the pipeline is solid.
* **Intermediate (`/models/intermediate`):**
    * **Model:** `int_lost_opportunities.sql`
    * **Logic:** Utilizes a **Left Anti-Join** between web traffic and converted leads. This isolates high-intent users who exited the funnel, providing a direct "re-targeting" list for the marketing team.
* **Marts (`/models/marts`):**
    * **Model:** `mart_marketing_roi.sql`
    * **Logic:** Aggregates conversion data by channel to calculate real-time ROI and efficiency metrics. Final tables are materialized as tables for optimized BI performance.

## 🛠️ How to Run
1.  **Environment Setup:** Ensure `requirements.txt` is installed and Snowflake credentials are configured in `profiles.yml`.
2.  **Data Ingestion:** Run `python ingest_to_snowflake.py` to populate the `RAW_ZONE`.
3.  **Pipeline Execution:** Run `dbt build` to execute all models, run data quality tests, and materialize the final analytics tables in a single command.

## 📊 Key Insights & Value
- **Operational Efficiency:** The `int_lost_opportunities` model provides the Marketing team with actionable re-targeting lists, moving beyond static reporting.
- **Channel Performance:** The pipeline identifies `Referral` as the highest-converting channel (40%), enabling data-driven budget allocation.
- **Data Observability:** Automated testing guarantees that only validated, non-duplicate data reaches the final executive dashboards, preventing "garbage-in, garbage-out" scenarios.