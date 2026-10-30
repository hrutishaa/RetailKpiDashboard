import json, pathlib, sqlite3
ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_kpis_match_db():
    from scripts.build_dashboard import compute
    k = compute(sqlite3.connect(ROOT / "data/retail.db"))
    saved = json.loads((ROOT / "docs/kpis.json").read_text())
    assert k["gross_sales"] == saved["gross_sales"]
    assert 0 < k["return_rate_pct"] < 100
    assert k["customers"] > 4000

def test_no_cancellations_in_sales():
    con = sqlite3.connect(ROOT / "data/retail.db")
    assert con.execute("SELECT COUNT(*) FROM fact_sales WHERE InvoiceNo LIKE 'C%'").fetchone()[0] == 0
