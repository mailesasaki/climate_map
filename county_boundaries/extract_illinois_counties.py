#!/usr/bin/env python3
"""
Extract Illinois counties from a U.S. county shapefile and save as GeoJSON.
"""
import geopandas as gpd
import os

def extract_illinois_counties():
    # Input shapefile path
    shapefile_path = 'tl_2024_us_county.shp'
    
    # Output GeoJSON path
    output_path = 'illinois_counties.geojson'
    
    print(f"Reading shapefile from {shapefile_path}...")
    
    # Read the shapefile
    counties = gpd.read_file(shapefile_path)
    
    # Filter for Illinois counties (FIPS state code 17)
    illinois_counties = counties[counties['STATEFP'] == '17']
    
    print(f"Found {len(illinois_counties)} counties in Illinois")
    
    # Save to GeoJSON format
    illinois_counties.to_file(output_path, driver='GeoJSON')
    
    print(f"Illinois counties saved to {output_path}")
    
    return illinois_counties

if __name__ == "__main__":
    extract_illinois_counties()