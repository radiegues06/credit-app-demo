import sqlite3

conn = sqlite3.connect('database/ume_finops.db')

# Check raw transaction_date format
rows = conn.execute("SELECT transaction_date FROM raw_transactions LIMIT 5").fetchall()
print("raw_transactions.transaction_date samples:")
for r in rows:
    print(f"  {r[0]!r}")

# Check what strftime produces
rows2 = conn.execute("SELECT transaction_date, strftime('%Y-%m', transaction_date) FROM raw_transactions LIMIT 5").fetchall()
print("\nstrftime('%Y-%m', transaction_date) results:")
for r in rows2:
    print(f"  {r[0]!r} -> {r[1]!r}")

# Check installment due_date format
rows3 = conn.execute("SELECT due_date FROM raw_installments LIMIT 5").fetchall()
print("\nraw_installments.due_date samples:")
for r in rows3:
    print(f"  {r[0]!r}")

# Check fct_installments days_past_due
rows4 = conn.execute("SELECT due_date, days_past_due, delinquency_bucket, status FROM fct_installments LIMIT 10").fetchall()
print("\nfct_installments samples:")
for r in rows4:
    print(f"  due_date={r[0]!r}, dpd={r[1]}, bucket={r[2]!r}, status={r[3]!r}")

conn.close()
