import sqlite3
import pandas as pd
from pathlib import Path

data_dir = Path("data/raw")
db_path = "olist.db"

conn = sqlite3.connect(db_path)

tables = {
    "olist_orders_dataset": "olist_orders_dataset.csv",
    "olist_order_items_dataset": "olist_order_items_dataset.csv",
    "olist_products_dataset": "olist_products_dataset.csv",
    "olist_customers_dataset": "olist_customers_dataset.csv",
    "olist_order_payments_dataset": "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset": "olist_order_reviews_dataset.csv",
    "olist_sellers_dataset": "olist_sellers_dataset.csv",
    "olist_geolocation_dataset": "olist_geolocation_dataset.csv",
    "product_category_name_translation": "product_category_name_translation.csv",
}

for table_name, filename in tables.items():
    csv_path = data_dir / filename
    print(f"Loading {csv_path} -> {table_name}")
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.close()
print("✅ Done! Database created:", db_path)
