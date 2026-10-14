# Truck Familiarization

This project is being set up to help new EMTs get familiar with the locations of items in the trucks.

**For demonstration purposes only.** The layout and procedures are a work in progress and have not been
reviewed for clinical use.

Live page: https://ericfrench2015.github.io/truck_familiarization/

The main interface is a webpage with a representation of a few key areas of the truck:
1) the left-side cabinetry (including a placeholder for the pediatric bag)
2) the stretcher (the LIFEPAK is laid out in the data but hidden on the page until its layout is ready)
3) the First-In (Red) Bag
4) the trauma bag
5) the medicine refrigerator

Not every inventory location is drawn yet. The bench seat, pocket ventilator, cleaning supply cabinet,
main oxygen compartment, stair chair, back board, and cervical collar compartments are in the inventory
but not on the page, so their items don't come up in search. `tools/check_layout.py` lists them.

There are three ways you can interact with this.
1) pick an item or do a substring search and the locations where matching items are will change color
2) pick a procedure and the locations where items necessary to perform that procedure will change color and show up numbered
3) click a pocket to see what's in it

Additionally, you can change the scope of what's available to simulate different conditions. The
checkboxes are Truck, First-In Bag, and Pediatric Bag. For example, untick everything except First-In Bag
to see what you have if you walk in with just the red bag. (The stretcher and trauma bag are currently
part of the Truck scope, so they can't be selected on their own.)

### Links

The page reads these URL parameters, so a search or procedure can be shared as a link:

- `?q=flush` – start with a search filled in.
- `?p=io-setup` – start with a procedure selected (ignored if `q` is also given).
- `?exclude=truck,pediatric-bag` – start with those scopes unticked.

### Running locally

The page loads its data with `fetch`, so opening `index.html` straight from disk won't work. Serve the
folder instead, e.g. `python -m http.server`, then open http://localhost:8000/.

## Data files

- `data/truck_inventory.csv` / `.xlsx` – every item: Main Location, Sub Location, Item, Count, Notes.
  The CSV is the source of truth: the page and the check scripts read only the CSV, so make edits there.
  The xlsx is a copy for convenient viewing.
- `data/layout.json` – where each location is drawn on the page.
- `data/procedures.json` – procedures and the items each step needs (see below).

### layout.json

- `canvas` – the design size of the page in pixels (positions scale with it).
- `groups` – the section headings areas are grouped under (Left-Side Cabinetry, Stretcher and LIFEPAK, etc.).
- `scopes` – the include/exclude checkboxes on the page (e.g. Truck, First-In Bag, Pediatric Bag).
- `areas` – one box per inventory Main Location:
  - `location` must match a Main Location in the inventory exactly.
  - `label` is the text shown on the page.
  - `scope` is which checkbox includes or excludes the area.
  - `kind` (optional): `bag` draws the area with a heavy border so it reads as separate from the wall.
  - `x`, `y`, `w`, `h` are percentages (0–100) of the canvas.
  - `status` is a note for editing: `from-prototype` (box and pockets copied from Tableau),
    `area-from-prototype` (box from Tableau, pockets are placeholders), `draft` (pockets laid out
    from photos, needs review), `placeholder` (all placeholder).
  - `subLocations` – one box per Sub Location; `name` must match the inventory, and
    `x`, `y`, `w`, `h` are fractions (0–1) of the parent area.
  - `subLocations` may also have `label` (short text shown on the box; full name shows on hover)
    and `color` (accent color, e.g. for the blue IV pod).

Run `python tools/check_layout.py` after editing to catch name mismatches and out-of-bounds boxes.

### procedures.json

Each procedure has an `id` (used in links: `?p=io-setup`), a `name`, a `source` (the REMSA protocol
section it came from), optional `notes`, and `steps`. Each step has `text` and `items` – a list of inventory
Item names, matched exactly. The page numbers every pocket holding an item by the step(s) that need it.

Run `python tools/check_procedures.py` after editing to catch item names that don't match the inventory.
