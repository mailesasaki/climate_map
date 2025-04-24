# County Boundaries

This directory contains county boundary data for the United States and tools to process this data.

## Contents

- `tl_2024_us_county.shp` and related files: TIGER/Line Shapefiles from the U.S. Census Bureau
- `extract_illinois_counties.py`: Python script to extract Illinois counties and save as GeoJSON
- `illinois_counties.geojson`: Extracted Illinois county boundaries in GeoJSON format

## Understanding Shapefiles

Shapefiles (`.shp`) are a common geospatial vector data format that stores location, shape, and attribute information for geographic features. A shapefile is actually comprised of multiple files:

- `.shp`: Contains the geometry data
- `.dbf`: Attributes for each shape (like county names, FIPS codes)
- `.prj`: Projection information (coordinate system)
- `.shx`: Shape index file
- `.cpg`: Character encoding for attribute data
- `.xml` files: Metadata

## Usage

### Prerequisites

To work with these geospatial files, you'll need:

- Python 3.x
- GeoPandas library (`pip install geopandas`)
  - GeoPandas depends on other libraries like Fiona, Shapely, and pyproj

### Extracting Illinois Counties

Run the provided script:

```bash
python extract_illinois_counties.py
```

This script reads the U.S. county shapefile, filters for Illinois counties (FIPS state code 17), and saves them to `illinois_counties.geojson`.

### Working with GeoJSON

GeoJSON is a more web-friendly format for geospatial data:

- JSON-based and human-readable
- Easily consumed by web mapping libraries like Leaflet, MapBox, and OpenLayers
- Can be directly loaded into visualization tools or web applications

## Common Operations

### Viewing Shapefiles

You can view shapefiles with:

- QGIS (free, open-source)
- ArcGIS (commercial)
- GeoPandas in a Jupyter notebook:
  ```python
  import geopandas as gpd
  counties = gpd.read_file("tl_2024_us_county.shp")
  counties.plot()
  ```

### Filtering Data

Filter by attributes in Python:

```python
# Get counties for a specific state
state_counties = counties[counties['STATEFP'] == '17']  # Illinois

# Get a specific county by name
cook_county = counties[counties['NAME'] == 'Cook']
```

### Common Attributes in County Shapefiles

- `STATEFP`: State FIPS code (e.g., '17' for Illinois)
- `COUNTYFP`: County FIPS code
- `GEOID`: Combined state and county FIPS
- `NAME`: County name
- `geometry`: The actual spatial data

## Data Source

The TIGER/Line Shapefiles are provided by the U.S. Census Bureau and were downloaded from https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2024&layergroup=Counties+%28and+equivalent%29. They are updated annually and are in the public domain.

## Further Resources

- [GeoPandas Documentation](https://geopandas.org/)
- [U.S. Census Bureau TIGER/Line Shapefiles](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
- [Introduction to GIS with Python](https://automating-gis-processes.github.io/site/)