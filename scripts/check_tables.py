import sqlite3

conn = sqlite3.connect('database/ume_finops.db')
tables = sorted([r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])
print('Tables:', tables)
print(f'Total: {len(tables)}')

# Quick check on marts
for t in ['portfolio_metrics', 'reconciliation_metrics', 'collection_metrics', 'vintage_default_metrics']:
    if t in tables:
        rows = conn.execute(f"SELECT * FROM {t}").fetchall()
        cols = [d[0] for d in conn.execute(f"SELECT * FROM {t}").description]
        print(f"\n--- {t} ---")
        print(f"Columns: {cols}")
        for row in rows[:3]:
            print(row)
    else:
        print(f"\nMISSING: {t}")

conn.close()
