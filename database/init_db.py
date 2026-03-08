import sqlite3
import os
import sys

# Ensure data_generator can be found when script is run from inside its directory or via subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_generator.merchants import generate_merchants
from data_generator.transactions import generate_transactions
from data_generator.installments import generate_installments
from data_generator.payments import generate_payments
from data_generator.settlements import generate_settlements

def init_db():
    print("Generating synthetic data...")
    merchants_df = generate_merchants()
    merchant_ids = merchants_df["merchant_id"].tolist()
    
    transactions_df = generate_transactions(merchant_ids=merchant_ids)
    installments_df = generate_installments(transactions_df)
    payments_df = generate_payments(installments_df)
    settlements_df = generate_settlements(payments_df)
    
    db_path = "database/ume_finops.db"
    
    # Ensure dir exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    print(f"Connecting to SQLite at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    # Save raw tables
    print("Loading data into raw SQLite tables...")
    merchants_df.to_sql("raw_merchants", conn, if_exists="replace", index=False)
    transactions_df.to_sql("raw_transactions", conn, if_exists="replace", index=False)
    installments_df.to_sql("raw_installments", conn, if_exists="replace", index=False)
    payments_df.to_sql("raw_payments", conn, if_exists="replace", index=False)
    settlements_df.to_sql("raw_settlements", conn, if_exists="replace", index=False)
    
    conn.close()
    
    print(f"Database setup complete.")
    print(f"Merchants: {len(merchants_df)}")
    print(f"Transactions: {len(transactions_df)}")
    print(f"Installments: {len(installments_df)}")
    print(f"Payments: {len(payments_df)}")
    print(f"Settlements: {len(settlements_df)}")

if __name__ == "__main__":
    init_db()
