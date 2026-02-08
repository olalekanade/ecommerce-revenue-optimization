import sqlite3
import pandas as pd

conn = sqlite3.connect("olist.db")

tables = ["fact_order_items", "fact_orders", "dim_customers_agg"]
for t in tables:
    n = pd.read_sql(f"SELECT COUNT(*) AS n FROM {t}", conn)["n"].iloc[0]
    print(f"{t}: {n:,} rows")

print("\nSample fact_orders:")
print(pd.read_sql("SELECT * FROM fact_orders LIMIT 5", conn))

conn.close()
