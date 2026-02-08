E-commerce Revenue Optimization (Olist)

Exploratory Analysis, Customer Segmentation, and Revenue Forecasting



This project analyzes the Olist Brazilian e-commerce dataset to understand revenue dynamics, customer behavior, and churn risk.

It demonstrates an end-to-end analytics workflow using SQL, Python, and BI-ready outputs, with a focus on business decision-making and reproducibility.



Status: Analytics pipeline complete

Power BI dashboard: In progress (to be added under /dashboards)



🎯 Project Objectives



Analyze how revenue and order volume evolved over time



Identify high-value and at-risk customer segments



Quantify revenue concentration and churn risk



Provide a realistic short-term revenue outlook



Generate clean, reproducible datasets for BI consumption



📌 Key Insights



Revenue grew rapidly throughout 2017 and plateaued in 2018, indicating a transition from growth to maturity



The customer base is dominated by one-time buyers, while repeat customers generate significantly higher average revenue



RFM segmentation reveals that a substantial share of revenue comes from At Risk and Hibernating customers, making retention a high-impact opportunity



Due to limited historical depth, complex seasonal models were not appropriate; a naive forecasting baseline achieved the lowest holdout error and was selected



🧱 Repository Structure

ecommerce-revenue-optimization/

├── data/

│   ├── raw/                # Raw CSVs (local only, ignored by git)

│   └── processed/          # Cleaned outputs for analysis and BI

├── notebooks/              # Analysis notebooks (EDA, RFM, forecasting)

├── scripts/                # Reproducible dataset builders for BI

├── sql/                    # SQL transformation logic

├── dashboards/             # Power BI assets (PBIX to be added)

├── build\_db.py             # Builds SQLite database from raw CSVs

├── run\_sql\_models.py       # Creates analytical tables

├── check\_db.py             # Sanity checks and validation

└── README.md



🧠 Methodology

1\. Data Modeling (SQL / SQLite)



Built a local SQLite database from raw transactional CSV files



Defined analytical tables using a fact/dimension mindset:



fact\_orders — order-level metrics



fact\_order\_items — item-level details



dim\_customers\_agg — customer-level aggregates



Applied explicit business rules (e.g., delivered orders only)



2\. Exploratory Data Analysis (EDA)



Validated schema, missing values, and data integrity



Analyzed:



Monthly revenue and order volume trends



Average order value (AOV)



Category and geographic revenue concentration



Repeat vs one-time customer behavior



Identified structural patterns that informed downstream modeling decisions



Notebook



notebooks/01\_eda.ipynb



3\. Customer Segmentation (RFM)



Engineered customer-level features:



Recency: Days since last purchase



Frequency: Number of completed orders



Monetary: Total customer spend



Used quantile-based scoring (1–5) to handle skewed e-commerce distributions



Mapped RFM scores into business-oriented segments:



Champions



Loyal Customers



Potential Loyalists



At Risk



Hibernating



Produced BI-ready outputs:



data/processed/rfm\_segments.csv



data/processed/rfm\_segment\_summary.csv



Notebook



notebooks/02\_rfm\_segmentation.ipynb



4\. Revenue Forecasting



Constructed a monthly revenue time series from delivered orders



Excluded low-volume platform launch months to reduce noise



Used a holdout window to evaluate forecasting approaches without leakage



Compared:



Naive baseline



Seasonal naive (when valid)



ETS (Holt–Winters) variants



ETS models failed to converge due to limited history; the naive baseline achieved the lowest holdout error and was selected



Saved transparent forecasting artifacts:



data/processed/revenue\_forecast\_total.csv



data/processed/forecast\_model\_comparison.csv



Notebook



notebooks/03\_revenue\_forecasting.ipynb



📊 BI-Ready Outputs



All analytical outputs are generated reproducibly and stored in data/processed/:



monthly\_revenue\_actual.csv — Monthly revenue and order counts



rfm\_segment\_summary.csv — Segment-level customer and revenue metrics



revenue\_forecast\_total.csv — Short-term revenue forecast



forecast\_model\_comparison.csv — Model evaluation and transparency table



These datasets are designed to be consumed directly by Power BI.



▶️ How to Run Locally

1\. Environment Setup

python -m venv .venv

\# Windows (PowerShell)

.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt



2\. Build the Database



Place the raw Olist CSV files into data/raw/, then run:



python build\_db.py

python run\_sql\_models.py

python check\_db.py



3\. Run Analysis Notebooks



Execute notebooks in order:



01\_eda.ipynb



02\_rfm\_segmentation.ipynb



03\_revenue\_forecasting.ipynb



4\. Build Power BI Inputs

python scripts/build\_monthly\_revenue\_actual.py



🛠 Tech Stack



Python: pandas, numpy, matplotlib, statsmodels



SQL: SQLite



Business Intelligence: Power BI (PL-300 aligned)



Version Control: Git, GitHub



📁 Data Source



This project uses the public Olist Brazilian E-commerce Dataset.

Raw CSV files and the SQLite database are intentionally not committed due to size and licensing considerations.

All results can be reproduced using the provided SQL and Python scripts.



⚠️ Notes \& Limitations



Forecasting is intentionally short-term and baseline-focused due to limited historical depth



Segment definitions prioritize business actionability over academic clustering



The Power BI dashboard is under active development and will be added in a future update

