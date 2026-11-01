from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "p2p.db"
DB.parent.mkdir(exist_ok=True)

with sqlite3.connect(DB) as con:
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript((ROOT / "database" / "schema.sql").read_text(encoding="utf-8"))
    count = con.execute("SELECT COUNT(*) FROM suppliers").fetchone()[0]
    if count == 0:
        con.executescript((ROOT / "database" / "seed.sql").read_text(encoding="utf-8"))

print(f"Database ready: {DB}")
