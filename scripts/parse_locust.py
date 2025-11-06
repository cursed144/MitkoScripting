import csv
import sys
from pathlib import Path

csv_path = Path("report_stats.csv")
if not csv_path.exists():
    print("report_stats.csv not found", file=sys.stderr)
    sys.exit(1)

rows = []
with csv_path.open(newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

def to_int(x):
    try:
        return int(x)
    except:
        return 0

rows_sorted = sorted(rows, key=lambda r: to_int(r.get("Request Count", "0")), reverse=True)
total = next((r for r in rows if r.get("Name", "").strip().lower() == "total"), None)

if total:
    print(f"TOTAL requests: {total.get('Request Count')}  failures: {total.get('Failure Count')}  avg_ms: {total.get('Average Response Time')}")
else:
    print("No 'Total' row in CSV")

print("\nTop endpoints:")
for r in rows_sorted[:10]:
    print(f"{r.get('Name','')}: requests={r.get('Request Count','')}, failures={r.get('Failure Count','')}, avg_ms={r.get('Average Response Time','')}")
