"""Compute KPIs from SQLite and render docs/index.html (static, Chart.js from CDN)."""
import json, pathlib, sqlite3
ROOT = pathlib.Path(__file__).resolve().parents[1]

def q(con, sql):
    cur = con.execute(sql); cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]

def compute(con):
    # Dec 2011 only covers up to the 9th, so it's excluded from trend KPIs
    monthly = q(con, "SELECT * FROM kpi_monthly WHERE month < '2011-12' ORDER BY month")
    one = lambda s: con.execute(s).fetchone()[0]
    gross = one("SELECT SUM(revenue) FROM fact_sales")
    returned = -one("SELECT SUM(revenue) FROM fact_returns")
    cust = one("SELECT COUNT(*) FROM dim_customer")
    repeat = one("""SELECT COUNT(*) FROM (SELECT CustomerID FROM fact_sales WHERE CustomerID IS NOT NULL
                   GROUP BY CustomerID HAVING COUNT(DISTINCT InvoiceNo) > 1)""")
    top_country = q(con, """SELECT Country, ROUND(SUM(revenue)) AS sales FROM fact_sales
                    GROUP BY Country ORDER BY sales DESC LIMIT 6""")
    top_products = q(con, """SELECT Description, ROUND(SUM(revenue)) AS sales FROM fact_sales
                     GROUP BY Description ORDER BY sales DESC LIMIT 8""")
    uk = con.execute("SELECT SUM(revenue) FROM fact_sales WHERE Country='United Kingdom'").fetchone()[0]
    jan, nov = monthly[1], monthly[-1]  # 2011-01 vs 2011-11
    return {
        "period": f"{monthly[0]['month']} to {monthly[-1]['month']}",
        "gross_sales": round(gross), "returns_value": round(returned),
        "return_rate_pct": round(100 * returned / gross, 1),
        "orders": one("SELECT COUNT(DISTINCT InvoiceNo) FROM fact_sales"),
        "aov": round(gross / one("SELECT COUNT(DISTINCT InvoiceNo) FROM fact_sales"), 2),
        "customers": cust, "repeat_rate_pct": round(100 * repeat / cust, 1),
        "uk_share_pct": round(100 * uk / gross, 1),
        "nov_vs_jan_sales_growth_pct": round(100 * (nov["net_sales"] / jan["net_sales"] - 1), 1),
        "peak_month": max(monthly, key=lambda m: m["net_sales"])["month"],
        "monthly": monthly, "top_country": top_country, "top_products": top_products,
    }

TEMPLATE = (ROOT / "scripts/template.html").read_text

def main():
    con = sqlite3.connect(ROOT / "data/retail.db")
    k = compute(con)
    (ROOT / "docs/kpis.json").write_text(json.dumps(k, indent=2))
    (ROOT / "docs/index.html").write_text(TEMPLATE().replace("__DATA__", json.dumps(k)))
    print({x: v for x, v in k.items() if not isinstance(v, list)})

if __name__ == "__main__":
    main()
