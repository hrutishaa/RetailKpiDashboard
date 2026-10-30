"""Download (if needed) and clean the UCI Online Retail dataset, then load it into SQLite."""
import pathlib, sqlite3, urllib.request, zipfile, io
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
XLSX = ROOT / "data/Online Retail.xlsx"
DB = ROOT / "data/retail.db"

def fetch():
    if not XLSX.exists():
        XLSX.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(SRC).read())) as z:
            z.extract("Online Retail.xlsx", XLSX.parent)

def clean(df):
    log = {"raw_rows": len(df)}
    df = df.dropna(subset=["Description"])
    df = df.drop_duplicates()
    log["after_dedupe"] = len(df)
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["is_cancel"] = df["InvoiceNo"].str.startswith("C")
    # keep cancellations (needed for return rate) but drop non-product rows and bad prices
    df = df[~df["StockCode"].astype(str).isin(["POST", "D", "M", "BANK CHARGES", "AMAZONFEE", "DOT", "CRUK", "S", "PADS", "B"])]
    df = df[df["UnitPrice"] > 0]
    log["clean_rows"] = len(df)
    df["revenue"] = df["Quantity"] * df["UnitPrice"]
    df["month"] = df["InvoiceDate"].dt.strftime("%Y-%m")
    df["CustomerID"] = df["CustomerID"].astype("Int64")
    return df, log

def main():
    fetch()
    df, log = clean(pd.read_excel(XLSX))
    con = sqlite3.connect(DB)
    con.executescript("DROP TABLE IF EXISTS order_lines;")
    df[["InvoiceNo","StockCode","Description","Quantity","InvoiceDate","UnitPrice","CustomerID","Country","is_cancel","revenue","month"]] \
        .assign(InvoiceDate=lambda d: d.InvoiceDate.astype(str)) \
        .to_sql("order_lines", con, index=False)
    con.executescript((ROOT / "sql/model.sql").read_text())
    con.commit()
    print(log)
    return log

if __name__ == "__main__":
    main()
