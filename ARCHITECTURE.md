# Credit Portfolio Analytics Pipeline Architecture

This repository contains a full-stack, local data engineering pipeline simulating a fintech credit portfolio monitoring system. It ingests synthetic transactional data, applies data transformations and modeling via `dbt`, and presents business indicators through a interactive Streamlit dashboard.

---

## Architecture Diagram

```mermaid
graph TD
    subgraph Data Generator Layer
        A[Faker & Pandas] --> |Synthetic Operations Data| B[database/init_db.py]
    end

    subgraph Storage Layer
        B --> |pandas.to_sql()| C[(SQLite: ume_finops.db)]
    end

    subgraph Transformation Layer dbt
        C -->|raw schemas| D[staging models]
        D --> E[core models]
        E --> F[marts models]
        F -->|analytics tables| C
    end

    subgraph Presentation Layer
        C -->|read marts| G[Streamlit Dashboard]
    end
```

---

## Component Details

### 1. Data Generator Layer (`data_generator/`)
This module simulates a live, operational fintech database.
*   **Merchants (`merchants.py`)**: Generates randomized Brazilian retail merchants (e.g., electronics, furniture segments) using `Faker("pt_BR")`.
*   **Transactions (`transactions.py`)**: Simulates credit purchases. Ticket values are sampled from a lognormal distribution to reflect realistic purchasing behavior.
*   **Installments (`installments.py`)**: Splits transactions into equal monthly payments, calculating principal and interest, and mapping statuses (`paid`, `late`, `default`, `pending`).
*   **Payments & Settlements (`payments.py`, `settlements.py`)**: Simulates actual money collection, generating late payment delays, partial payment scenarios, and bank reconciliation gaps (missed settlements).

### 2. Storage Layer (`database/`)
*   **Database (`ume_finops.db`)**: A lightweight SQLite database used for simplicity and zero-configuration local deployments. 
*   **Initialization script (`init_db.py`)**: Acts as the ingestion engine. It replaces old generic raw tables with fresh DataFrames directly streamed via Pandas.

### 3. Transformation Layer (`dbt_project/`)
Built with `dbt-core` and `dbt-sqlite`, this layer implements a classic 3-tier medallion-style modeling structure within the warehouse:

#### A. Staging (`models/staging/`)
Lightweight, 1-to-1 views over the raw loaded tables (`stg_transactions`, `stg_installments`, `stg_payments`, `stg_settlements`, `stg_merchants`). Responsible for renaming and type casting.

#### B. Core (`models/core/`)
Intermediate tables where business logic and enrichments are applied.
*   `fct_credit_transactions`: Enriches transaction rows with geographical/segment data from merchants, and calculates the origination month (vintage).
*   `fct_installments`: Computes `days_past_due` logic and categorizes debts into delinquency buckets (e.g., `0-30`, `31-60`, `90+`).
*   `fct_payments`: Calculates payment differences and identifies partial payment behavior.

#### C. Marts (`models/marts/`)
The consumption layer tables optimized for the BI/dashboard tool. These heavily aggregate state logic to present high-level KPIs.
*   `portfolio_metrics`: Total financed value, outstanding principal, PAR30/PAR90, and average ticket.
*   `reconciliation_metrics`: Analysis of received cash vs settled banking cash.
*   `collection_metrics`: Analysis of expected vs collected payments.
*   `vintage_default_metrics`: Tracks default rates over different origination cohorts.

All schemas are fortified with column-level descriptions and **data integrity tests** (e.g., primary key constraints, `not_null` constraints, referential relationships mappings checking for orphans, and predefined accepted values for enumerations).

### 4. Presentation Layer (`dashboard/app.py`)
A fast, strictly-read-only analytical interface built with Streamlit. Features:
*   **Portfolio Health**: Core metric cards (Overall Portfolio, PAR30/PAR90, Average ticket). Contains **threshold alerting logic** to automatically render high-risk notifications if `PAR90` exceeds 8%.
*   **Portfolio Evolution**: A timeline of volume-origination using Plotly lines.
*   **Vintage Default Curve**: A classic credit risk visualization demonstrating lifetime default behavior per cohort.
*   **Collections + Reconciliation Monitoring**: Validating operational cashflow with expected vs. settled cash.

### 5. Orchestration (`run_pipeline.py`)
A master controller script that sequentially unifies the end-to-end flow:
1.  Fires Python scripts to generate the SQL data.
2.  Invokes `dbt run` locally through a subprocess, running all transformations synchronously.
3.  Prepares the final DB for dashboard analysis.
