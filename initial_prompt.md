You are helping design and implement a realistic data engineering mini-project that simulates the credit portfolio analytics pipeline of a fintech like UME.

The objective is to build a **complete but simple local data stack** demonstrating:

- fintech credit portfolio analytics
- financial reconciliation processes
- modern data stack practices
- data modeling with dbt
- dashboard visualization

The project must run locally and be easy to execute.

TECH STACK (MANDATORY)

Python
Faker (synthetic data generation)
SQLite (data warehouse)
dbt + dbt-sqlite
Streamlit (dashboard)

No cloud infrastructure should be required.

The final result should simulate a **credit portfolio management system** that ingests transactional data, models the portfolio, and produces business indicators and dashboards.

--------------------------------

PROJECT OVERVIEW

The system represents a fintech that finances retail purchases.

Business flow:

1. A customer buys a product in a partner store.
2. The fintech approves the credit.
3. The purchase is split into installments.
4. The customer pays installments via payment channels.
5. Payments are settled through the bank.
6. The fintech reconciles payments against bank settlements.
7. The company monitors the health of its credit portfolio.

The project should simulate the data pipeline needed to support this.

--------------------------------

ARCHITECTURE

Python (data generator using Faker)
        ↓
SQLite database
        ↓
dbt transformations
        ↓
analytics tables
        ↓
Streamlit dashboard

--------------------------------

DATA GENERATION (PYTHON + FAKER)

Create a Python module responsible for generating realistic synthetic fintech data.

Use Faker to simulate merchants, customers, transactions, and payments.

The generator should create the following datasets:

MERCHANTS

merchant_id
merchant_name
segment
city

TRANSACTIONS

transaction_id
merchant_id
customer_id
purchase_value
installments
transaction_date

INSTALLMENTS

installment_id
transaction_id
installment_number
due_date
principal
interest
status

Possible status values:

pending
paid
late
default

PAYMENTS

payment_id
installment_id
payment_date
amount
payment_channel

Channels:

pix
boleto
credit_card

BANK_SETTLEMENTS

settlement_id
payment_id
settlement_date
amount
bank_reference

--------------------------------

REALISTIC FINTECH BEHAVIOR

The generator must simulate realistic credit dynamics:

- some late payments
- some defaults
- partial payments
- payments received after due date
- some payments without settlements (to simulate reconciliation failures)

Parameters should be configurable:

number_of_merchants
number_of_transactions
default_rate
late_payment_rate
average_ticket

--------------------------------

SQLITE DATABASE

Create a SQLite database file:

ume_finops.db

Tables should be created under a "raw" layer conceptually:

raw_merchants
raw_transactions
raw_installments
raw_payments
raw_settlements

--------------------------------

DBT TRANSFORMATION LAYERS

Use dbt with dbt-sqlite.

Organize models into three layers.

STAGING

Standardize raw tables:

stg_merchants
stg_transactions
stg_installments
stg_payments
stg_settlements

CORE MODELS

Create normalized fact tables:

fct_credit_transactions
fct_installments
fct_payments

Include derived fields such as:

days_past_due

delinquency_bucket

Buckets must be:

0-30
31-60
61-90
90+

--------------------------------

ANALYTICS MARTS

Create analytical tables that compute key fintech metrics.

MART 1 — portfolio_metrics

Compute:

total_financed_value
outstanding_principal
average_ticket
PAR30
PAR90

Definitions:

PAR30 = % of portfolio with installments > 30 days overdue  
PAR90 = % of portfolio with installments > 90 days overdue

--------------------------------

MART 2 — reconciliation_metrics

Join payments with bank settlements.

Compute:

expected_cash
settled_cash
difference
reconciliation_rate
unmatched_payments

Definition:

reconciliation_rate = reconciled_payments / total_payments

--------------------------------

MART 3 — collection_metrics

Compute:

expected_collection
actual_collection
collection_rate

Definition:

collection_rate = collected_amount / expected_amount

--------------------------------

MART 4 — vintage_default_metrics

Compute credit performance by origination cohort.

Fields:

origination_month
total_financed
defaulted_amount
default_rate

This simulates the "Vintage Default Curve" used in fintech risk monitoring.

--------------------------------

STREAMLIT DASHBOARD

Create a Streamlit application that reads the analytics tables from SQLite and displays business metrics.

The dashboard should contain:

SECTION 1 — Portfolio Health

Show metric cards:

Outstanding Portfolio  
PAR30  
PAR90  
Average Ticket  

--------------------------------

SECTION 2 — Portfolio Evolution

Line chart:

portfolio size over time

--------------------------------

SECTION 3 — Vintage Default Curve

Line chart:

default_rate by origination_month

--------------------------------

SECTION 4 — Collections

Chart comparing:

expected collection vs actual collection

--------------------------------

SECTION 5 — Reconciliation Monitoring

Show:

reconciliation_rate
number of unmatched payments

--------------------------------

ALERT SYSTEM

Implement a simple operational alert.

Example:

If PAR90 > 8%  
Display warning in Streamlit dashboard.

--------------------------------

PROJECT STRUCTURE

Design a clean repository structure.

Example:

project_root/

data_generator/
    generate_merchants.py
    generate_transactions.py
    generate_installments.py
    generate_payments.py
    generate_settlements.py

database/
    ume_finops.db

dbt_project/
    models/
        staging/
        core/
        marts/

dashboard/
    app.py

scripts/
    generate_data.py

--------------------------------

DELIVERABLES

Provide:

1. Full project architecture
2. Python data generation code structure
3. SQLite schema definitions
4. dbt model structure
5. Example SQL logic for key transformations
6. Streamlit dashboard implementation
7. Instructions for running the entire pipeline locally

The project must remain simple enough to implement in a few hours but realistic enough to demonstrate fintech data modeling and credit portfolio analytics.

Generate the repository structure and start implementing the Python data generator first.