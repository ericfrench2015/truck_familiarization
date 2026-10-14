This project is being set up to help new EMTs get familiar with the locations of items in the trucks.

The main interface is a webpage with a represention of a few key areas of the truck:
1) the left-side cabinetry
2) the stretcher and lifepack
3) the red/first in bag
4) the trauma bag
5) the medicine refrigerator

There are two ways you can interact with this.
1) pick an item or do a substring search and the locations where matching items are will change color
2) pick a procedure and the locations where items necessary to perform that procedure will change color and show up numbered.

Additionally, you can change the scope of what's available to simulate different conditions. For example,
if you're in an apartment with just the stretcher and the red bag.

## Data files

- `data/truck_inventory.csv` / `.xlsx` – every item: Main Location, Sub Location, Item, Count, Notes.
  The CSV is the source of truth; the xlsx is a copy for convenient editing/viewing.
- `data/layout.json` – where each location is drawn on the page.

### layout.json

- `canvas` – the design size of the page in pixels (positions scale with it).
- `groups` – the five areas from the top of this README. Scope filters work on groups.
- `areas` – one box per inventory Main Location:
  - `location` must match a Main Location in the inventory exactly.
  - `label` is the text shown on the page.
  - `kind` (optional): `bag` draws the area with a heavy border so it reads as separate from the wall.
  - `x`, `y`, `w`, `h` are percentages (0–100) of the canvas.
  - `status` is a note for editing: `from-prototype` (box and pockets copied from Tableau),
    `area-from-prototype` (box from Tableau, pockets are placeholders), `draft` (pockets laid out
    from photos, needs review), `placeholder` (all placeholder).
  - `subLocations` may also have `label` (short text shown on the box; full name shows on hover)
    and `color` (accent color, e.g. for the blue IV pod).
  - `subLocations` – one box per Sub Location; `name` must match the inventory, and
    `x`, `y`, `w`, `h` are fractions (0–1) of the parent area.

Run `python tools/check_layout.py` after editing to catch name mismatches and out-of-bounds boxes.
