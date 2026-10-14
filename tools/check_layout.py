"""Check data/layout.json against data/truck_inventory.csv.

Reports layout areas/sub-locations that don't match the inventory, inventory
sub-locations missing from the layout, and boxes outside their bounds.

Usage: python tools/check_layout.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

inventory = defaultdict(list)
with open(DATA / "truck_inventory.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        subs = inventory[row["Main Location"]]
        if row["Sub Location"] not in subs:
            subs.append(row["Sub Location"])

layout = json.loads((DATA / "layout.json").read_text(encoding="utf-8"))
problems = 0


def report(msg):
    global problems
    problems += 1
    print(msg)


def check_box(label, box, limit):
    x, y, w, h = (box.get(k) for k in ("x", "y", "w", "h"))
    if None in (x, y, w, h):
        report(f"{label}: missing x/y/w/h")
    elif x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > limit or y + h > limit:
        report(f"{label}: box ({x}, {y}, {w}, {h}) is outside 0-{limit}")


placed = set()
for area in layout["areas"]:
    loc = area["location"]
    check_box(f"area '{area['id']}'", area, 100)
    if area["group"] not in layout["groups"]:
        report(f"area '{area['id']}': unknown group '{area['group']}'")
    if area.get("scope") not in layout["scopes"]:
        report(f"area '{area['id']}': unknown scope '{area.get('scope')}'")
    if loc not in inventory:
        report(f"area '{area['id']}': location '{loc}' not in inventory")
        continue
    placed.add(loc)
    for sub in area["subLocations"]:
        check_box(f"'{loc}' / '{sub['name']}'", sub, 1)
        if sub["name"] not in inventory[loc]:
            report(f"'{loc}' / '{sub['name']}': sub-location not in inventory")
    missing = [s for s in inventory[loc] if s not in {x["name"] for x in area["subLocations"]}]
    for s in missing:
        report(f"'{loc}' / '{s}': in inventory but not in layout")

unplaced = [loc for loc in inventory if loc not in placed]
if unplaced:
    print("\nInventory locations with no layout area (not shown on the page):")
    for loc in unplaced:
        print(f"  - {loc}")

print(f"\n{problems} problem(s) found." if problems else "\nLayout matches inventory.")
