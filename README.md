# Credit FinOps Mini Case

This project simulates the financial operations reconciliation process
of a credit fintech that finances purchases from retail partners.

Stack:
- Python
- Faker
- SQLite
- dbt
- Streamlit

Goal:
Demonstrate how a FinOps / Credit Ops team consolidates transaction
data from multiple sources and produces reconciliation and credit
portfolio health metrics.

## How to run

1. **Install dependencies:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   # source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Pipeline (Data Generation & Modeling):**
   ```bash
   # This will create database tables using Faker, then run dbt
   python run_pipeline.py
   ```

3. **Run the Dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```