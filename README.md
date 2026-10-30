# Retail KPI Dashboard

A KPI dashboard for a UK online gift retailer, built the way I'd build one for a business team: clean the raw data, model it in SQL, write down exactly what each metric means, and publish one page people can actually open.

**Live dashboard:** https://hrutishaa.github.io/RetailKpiDashboard/

**Data:** [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) — 541,909 invoice lines from a UK-based online retailer, 1 Dec 2010 to 9 Dec 2011 (Chen, D. 2015, UCI Machine Learning Repository, CC BY 4.0).

## How it works

1. `scripts/clean.py` downloads the data, cleans it with pandas (541,909 → 531,380 lines) and loads it into SQLite.
2. `sql/model.sql` builds the model: `fact_sales`, `fact_returns`, `dim_customer` and a `kpi_monthly` view.
3. `scripts/build_dashboard.py` queries the model and writes `docs/index.html` and `docs/kpis.json`.
4. [docs/metrics.md](docs/metrics.md) defines every metric and cleaning rule.

## What the numbers say

- **£10.25M** gross sales across **19,776 orders**, an average order of **£518.56**.
- **4,334** identified customers; **65.3%** ordered more than once.
- Returns/cancellations are worth **4.6%** of gross sales.
- The UK is **85.1%** of sales.
- November 2011 was the peak month, with sales up **116.7%** on January 2011, so the business is heavily seasonal around Q4 gifting.

## Run it

```bash
pip install -r requirements.txt
python scripts/clean.py
python scripts/build_dashboard.py
python -m pytest -q
```
