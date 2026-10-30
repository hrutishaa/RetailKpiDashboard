-- Star-ish model on top of the cleaned order lines
DROP VIEW IF EXISTS fact_sales;
CREATE VIEW fact_sales AS SELECT * FROM order_lines WHERE is_cancel = 0 AND Quantity > 0;

DROP VIEW IF EXISTS fact_returns;
CREATE VIEW fact_returns AS SELECT * FROM order_lines WHERE is_cancel = 1;

DROP VIEW IF EXISTS dim_customer;
CREATE VIEW dim_customer AS
SELECT CustomerID, MIN(month) AS first_month, MAX(Country) AS country
FROM fact_sales WHERE CustomerID IS NOT NULL GROUP BY CustomerID;

-- Monthly KPIs
DROP VIEW IF EXISTS kpi_monthly;
CREATE VIEW kpi_monthly AS
SELECT s.month,
       ROUND(SUM(s.revenue), 2)                         AS net_sales,
       COUNT(DISTINCT s.InvoiceNo)                      AS orders,
       ROUND(SUM(s.revenue) / COUNT(DISTINCT s.InvoiceNo), 2) AS aov,
       COUNT(DISTINCT s.CustomerID)                     AS active_customers,
       COUNT(DISTINCT CASE WHEN c.first_month = s.month THEN s.CustomerID END) AS new_customers
FROM fact_sales s LEFT JOIN dim_customer c USING (CustomerID)
GROUP BY s.month;
