# CLAUDE.md

## Project Overview

This project simulates the data platform of a fintech that finances retail purchases and manages a credit portfolio.

The goal is to demonstrate:

- data engineering practices
- fintech credit portfolio analytics
- financial reconciliation
- dbt-based modeling
- operational dashboards

The stack is intentionally simple and fully local.

### Technology Stack

- Python
- Faker (synthetic data generation)
- SQLite (data warehouse)
- dbt + dbt-sqlite
- Streamlit (analytics dashboard)

The system simulates the lifecycle of financed transactions, installment payments, and financial reconciliation.

---

# Core Architectural Principles

## 1. Clear Data Layers

The project follows a simplified **ELT architecture**.

Raw data must never be overwritten.

Data flows through the following layers:

Data Generator (Python)  
↓  
RAW tables (SQLite)  
↓  
STAGING models (dbt)  
↓  
CORE models (dbt)  
↓  
ANALYTICS MARTS  
↓  
Streamlit dashboards

### Layer Responsibilities

#### RAW

Exact representation of source systems.

Tables:

- raw_merchants
- raw_transactions
- raw_installments
- raw_payments
- raw_settlements

These tables must contain **no transformations**.

---

#### STAGING

Purpose:

- clean data
- rename fields
- standardize types
- apply light transformations

Naming convention:

stg_<table_name>

Examples:

- stg_transactions
- stg_installments
- stg_payments

---

#### CORE

Purpose:

- business logic
- normalized models
- derived metrics such as delinquency

Naming convention:

fct_<entity>

Examples:

- fct_credit_transactions
- fct_installments
- fct_payments

---

#### MARTS

Purpose:

Business-ready aggregated models used by dashboards.

Naming convention:

<domain>_metrics

Examples:

- portfolio_metrics
- reconciliation_metrics
- collection_metrics
- vintage_default_metrics

---

# Data Modeling Guidelines

## Use Fact-Based Modeling

Core tables should represent **business events**.

Examples:

| Table | Description |
|------|-------------|
| transactions | financed purchase |
| installments | scheduled repayment |
| payments | customer payments |
| settlements | bank settlement |

Avoid overly complex star schemas.

The goal is clarity.

---

## Key Derived Fields

The following fields must be computed in dbt models.

### days_past_due

days_past_due = current_date - due_date

Used to determine delinquency.

---

### delinquency_bucket

Buckets must be:

- 0-30
- 31-60
- 61-90
- 90+

This is standard in credit analytics.

---

# Synthetic Data Generation Guidelines

All synthetic data must be generated with **Faker**.

Goals:

- realism
- reproducibility
- configurable parameters

### Required Behavior

The generator must simulate:

- on-time payments
- late payments
- defaults
- partial payments
- missing settlements

This ensures reconciliation metrics are meaningful.

---

### Configurable Parameters

The generator should allow tuning:

- number_of_merchants
- number_of_transactions
- default_rate
- late_payment_rate
- average_ticket

---

### Data Relationships

The generator must enforce the following hierarchy:

transaction  
↓  
installments  
↓  
payments  
↓  
bank settlements

---

# dbt Best Practices

## Naming Conventions

Use clear model names.

Examples:

- stg_transactions.sql
- fct_installments.sql
- portfolio_metrics.sql

Avoid generic names like:

- data_model.sql
- table1.sql

---

## Keep SQL Readable

Follow these rules:

- lowercase SQL
- explicit joins
- avoid nested queries when possible

Example:

select  
    transaction_id,  
    purchase_value  
from {{ ref('stg_transactions') }}

---

## Always Use ref()

Never reference tables directly.

Correct:

{{ ref('stg_transactions') }}

Incorrect:

select * from raw_transactions

---

## One Transformation Per Model

Each dbt model should have a **clear responsibility**.

Example (good):

fct_installments → compute delinquency

Example (bad):

single huge SQL model doing everything

---

# Financial Metrics Guidelines

The project must compute key fintech credit indicators.

## Portfolio Metrics

Must include:

- total_financed_value
- outstanding_principal
- average_ticket
- PAR30
- PAR90

Definitions:

PAR30 = % of portfolio overdue > 30 days  
PAR90 = % of portfolio overdue > 90 days

---

## Collection Metrics

Must compute:

- expected_collection
- actual_collection
- collection_rate

Formula:

collection_rate = collected_amount / expected_amount

---

## Reconciliation Metrics

Must compute:

- expected_cash
- settled_cash
- difference
- reconciliation_rate
- unmatched_payments

Formula:

reconciliation_rate = reconciled_payments / total_payments

---

## Vintage Default Metrics

Compute cohort-based credit performance.

Group by:

origination_month

Metrics:

- total_financed
- defaulted_amount
- default_rate

This simulates **Vintage Default Curves** used by credit risk teams.

---

# Streamlit Dashboard Guidelines

The dashboard should focus on **clarity and monitoring**.

Avoid overly complex UI.

### Dashboard Sections

#### Portfolio Health

Show metric cards:

- Outstanding Portfolio
- PAR30
- PAR90
- Average Ticket

---

#### Portfolio Evolution

Line chart showing:

portfolio size over time

---

#### Vintage Default Curve

Line chart showing:

default_rate by origination_month

---

#### Collections

Comparison chart:

expected vs actual collections

---

#### Reconciliation Monitoring

Show:

- reconciliation_rate
- unmatched_payments

---

# Operational Alerts

Add simple monitoring rules.

Example:

if PAR90 > 8% → show warning in dashboard

This simulates risk monitoring.

---

# Code Quality Guidelines

## Keep Code Modular

Avoid large scripts.

Example structure:

data_generator/
- merchants.py
- transactions.py
- installments.py
- payments.py
- settlements.py

---

## Separate Logic and Execution

Prefer functions like:

generate_transactions()

instead of executing logic directly in scripts.

---

## Reproducibility

All data generation should support a fixed random seed.

Example:

random.seed(42)

This ensures consistent datasets.

---

# Performance Guidelines

Although the dataset is small, follow scalable patterns.

- avoid unnecessary loops
- prefer pandas operations
- write clean SQL transformations

---

# Simplicity Rule

This project is **a demonstration project**, not a production system.

Prioritize:

- readability
- clarity
- educational value

Avoid:

- overengineering
- unnecessary abstractions
- excessive frameworks

---

# Final Goal

The final system should demonstrate a realistic fintech data pipeline capable of:

1. simulating credit portfolio data
2. modeling financial transactions
3. computing credit risk indicators
4. reconciling payments with bank settlements
5. presenting results in an operational dashboard