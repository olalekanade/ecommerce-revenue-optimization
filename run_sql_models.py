import sqlite3
from pathlib import Path

db_path = "olist.db"
sql_path = Path("sql/cleaning_queries.sql")

conn = sqlite3.connect(db_path)
conn.executescript(sql_path.read_text(encoding="utf-8"))
conn.commit()
conn.close()

print("✅ Created analytical tables: fact_order_items, fact_orders, dim_customers_agg")
