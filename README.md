# E-commerce Revenue Optimization (Olist)

## Exploratory Analysis, Customer Segmentation, and Revenue Forecasting

This project analyzes the **Olist Brazilian e-commerce dataset** to understand revenue dynamics, customer behavior, and churn risk.  
It demonstrates an end-to-end analytics workflow using **SQL, Python, and BI-ready outputs**, with a focus on **business decision-making** and reproducibility.

Status: Analytics pipeline complete  
Power BI dashboard: In progress (to be added under /dashboards)

---

## Project Objectives

- Analyze how revenue and order volume evolved over time
- Identify high-value and at-risk customer segments
- Quantify revenue concentration and churn risk
- Provide a realistic short-term revenue outlook
- Generate clean, reproducible datasets for BI consumption

---

## Key Insights

- Revenue grew rapidly throughout **2017** and plateaued in **2018**, indicating a transition from growth to maturity
- The customer base is dominated by **one-time buyers**, while repeat customers generate significantly higher average revenue
- RFM segmentation shows that a substantial share of revenue comes from **At Risk** and **Hibernating** customers
- Due to limited historical depth, complex seasonal models were not appropriate; a **naive forecasting baseline** achieved the lowest holdout error and was selected

---

## Repository Structure

```
ecommerce-revenue-optimization/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── scripts/
├── sql/
├── dashboards/
├── build_db.py
├── run_sql_models.py
├── check_db.py
└── README.md
```

---

## Methodology

### 1. Data Modeling (SQL / SQLite)

- Built a local SQLite database from raw transactional CSV files
- Defined analytical tables using a fact/dimension approach:
  - `fact_orders`
  - `fact_order_items`
  - `dim_customers_agg`
- Applied explicit business rules (delivered orders only)

---

### 2. Exploratory Data Analysis (EDA)

- Validated schema, missing values, and data integrity
- Analyzed:
  - Monthly revenue and order volume trends
  - Average order value (AOV)
  - Category and geographic revenue concentration
  - Repeat vs one-time customer behavior

Notebook:
- `notebooks/01_eda.ipynb`

---

### 3. Customer Segmentation (RFM)

- Engineered customer-level features:
  - **Recency:** Days since last purchase
  - **Frequency:** Number of completed orders
  - **Monetary:** Total customer spend
- Used quantile-based scoring (1–5)
- Grouped customers into actionable segments:
  - Champions
  - Loyal Customers
  - Potential Loyalists
  - At Risk
  - Hibernating

Notebook:
- `notebooks/02_rfm_segmentation.ipynb`

---

### 4. Revenue Forecasting

- Constructed a monthly revenue time series from delivered orders
- Used a holdout window to avoid leakage
- Compared naive and ETS models
- Selected the naive model due to limited historical depth

Notebook:
- `notebooks/03_revenue_forecasting.ipynb`

---

## BI-Ready Outputs

- `monthly_revenue_actual.csv`
- `rfm_segments.csv`
- `rfm_segment_summary.csv`
- `revenue_forecast_total.csv`
- `forecast_model_comparison.csv`

---

## How to Run Locally

### Environment Setup

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Build Database

```
python build_db.py
python run_sql_models.py
python check_db.py
```

### Run Analysis Notebooks

1. `01_eda.ipynb`
2. `02_rfm_segmentation.ipynb`
3. `03_revenue_forecasting.ipynb`

### Build Power BI Inputs

```
python scripts/build_monthly_revenue_actual.py
```

---

## Tech Stack

- Python
- SQL (SQLite)
- Power BI
- Git and GitHub

---

## Data Source

Public **Olist Brazilian E-commerce Dataset**.  
Raw data files and the SQLite database are excluded due to size and licensing considerations.

---

## Notes and Limitations

- Forecasting is intentionally short-term and baseline-focused
- Segmentation is optimized for business actionability
- Power BI dashboard will be added in a future update

---
