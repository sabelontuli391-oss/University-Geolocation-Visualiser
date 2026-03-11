# University Geolocation Visualiser

A lightweight ETL pipeline that fetches, caches, and visualises the geographic 
locations of universities and institutions worldwide on an interactive map.

## How it works

1. **`geoload.py`** — reads a list of institutions, queries the OpenStreetMap 
   geocoding API, and caches the raw JSON responses in a local SQLite database
2. **`geodump.py`** — parses the cached geodata and exports coordinates + place 
   names into a `where.js` file
3. **`index.html`** — loads `where.js` and renders all locations as pins on an 
   interactive map

## Stack
- Python 3
- SQLite
- OpenStreetMap / Nominatim API
- Leaflet.js

## Usage
```bash
python geoload.py   # populate the database
python geodump.py   # export to where.js
# then open index.html in your browser
```
