"""
Build monthly revenue fact table for Power BI dashboards.

Source:
- olist.db (fact_orders)

Output:
- data/processed/monthly_revenue_actual.csv

Business rules:
- Only delivered orders
- Revenue = sum(total_payment_value)
- Orders = count(distinct order_id)
- Grain = month
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("../olist.db")
OUTPUT_PATH = Path("../data/processed/monthly_revenue_actual.csv")

def main():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            """
            SELECT
                strftime('%Y-%m-01', order_purchase_date) AS month,
                SUM(total_payment_value) AS revenue,
                COUNT(DISTINCT order_id) AS orders
            FROM fact_orders
            WHERE order_status = 'delivered'
            GROUP BY 1
            ORDER BY 1
            """,
            conn,
            parse_dates=["month"],
        )

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
