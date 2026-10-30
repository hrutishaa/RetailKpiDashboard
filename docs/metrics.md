# Metric definitions

All metrics come from `data/retail.db`, built by `scripts/clean.py` and `sql/model.sql`.

| Metric | Definition | Source |
|---|---|---|
| Gross sales | Sum of `Quantity × UnitPrice` on non-cancelled invoices with positive quantity | `fact_sales` |
| Orders | Distinct `InvoiceNo` in `fact_sales` | `fact_sales` |
| Average order value (AOV) | Gross sales ÷ orders | `fact_sales` |
| Customers | Distinct non-null `CustomerID` with at least one sale | `dim_customer` |
| Repeat customer rate | Customers with 2+ distinct orders ÷ customers | `fact_sales` |
| Return rate (value) | Value of cancelled lines (`InvoiceNo` starting with C) ÷ gross sales | `fact_returns` |
| Active customers (monthly) | Distinct customers with a sale in the month | `kpi_monthly` |
| New customers (monthly) | Customers whose first purchase month is that month | `kpi_monthly` |
| UK share | UK gross sales ÷ gross sales | `fact_sales` |

## Cleaning rules
1. Drop rows with no product description.
2. Drop exact duplicate rows. Steps 1–2 remove 1,454 + 5,268 rows (541,909 → 535,187).
3. Drop non-product stock codes (postage, manual adjustments, bank/Amazon fees, discounts, samples, etc.).
4. Drop lines with a unit price of 0 or less. Result: 531,380 clean lines.
5. Keep cancellations, but only in `fact_returns`.

## Caveats
- About a quarter of lines have no `CustomerID`, so customer metrics cover identified customers only; sales metrics include everyone.
- December 2011 only runs to the 9th, so it is left out of the monthly charts.
