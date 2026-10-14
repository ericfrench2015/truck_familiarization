"""Check data/procedures.json against data/truck_inventory.csv.

Every item a step lists must match an inventory Item name exactly.

Usage: python tools/check_procedures.py
"""
import csv
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

with open(DATA / "truck_inventory.csv", encoding="utf-8") as f:
    names = {row["Item"] for row in csv.DictReader(f)}

procedures = json.loads((DATA / "procedures.json").read_text(encoding="utf-8"))["procedures"]
problems = 0
ids = set()
for proc in procedures:
    if proc["id"] in ids:
        print(f"duplicate procedure id '{proc['id']}'")
        problems += 1
    ids.add(proc["id"])
    for n, step in enumerate(proc["steps"], 1):
        for item in step["items"]:
            if item not in names:
                print(f"'{proc['name']}' step {n}: '{item}' is not an inventory item")
                problems += 1

print(f"\n{problems} problem(s) found." if problems else f"All {len(procedures)} procedures match the inventory.")
