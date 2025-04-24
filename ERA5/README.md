# ERA5 Climate Data Processor for Illinois

This tool downloads, processes, and exports ERA5 climate data specifically for the state of Illinois. It provides a simple command-line interface for researchers and analysts to retrieve climate data for specific time periods and variables.

## Key Features

- Filter by date range (YYYY-MM-DD format)
- Select specific climate variables or include all available variables
- Optional county-level attribution for each grid cell
- Export to multiple formats (Parquet, CSV, NetCDF)
- Consistent interpolation to a regular grid
- Calculation of derived variables (vapor pressure, wind magnitude/direction, relative humidity)

## Getting Started

### Prerequisites

- Python 3.9+
- Required packages (see `pyproject.toml`)
- Access to Google Cloud Storage (for ERA5 data access)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

The main command-line interface is through the `era5il.py` script. Here's a basic example:

```bash
python -m climate_map.ERA5.era5il process \
  --start-date 2022-01-01 \
  --end-date 2022-01-31 \
  --variables 2t 2d vapor_pressure \
  --format parquet \
  --output-path ./output
```

### Command-line Arguments

- `--start-date`: Start date in YYYY-MM-DD format
- `--end-date`: End date in YYYY-MM-DD format
- `--variables` or `-v`: List of variables to include (use 'all' for all variables)
- `--format` or `-f`: Output format (parquet, csv, netcdf)
- `--output-path` or `-o`: Directory to save the output file
- `--include-counties/--no-counties`: Whether to add county information to each grid cell
- `--county-file`: Path to GeoJSON file with county boundaries

### Available Variables

The tool supports all ERA5 surface variables, plus the following derived variables:

- `vapor_pressure`: Calculated from dewpoint temperature (hPa/mb)
- `surface_wind`: Magnitude and direction calculated from U and V wind components (m/s, degrees)
- `relative_humidity`: Calculated from temperature and dewpoint (0-1)

## Understanding the Code

The code is organized into three main components:

1. **era5il.py** - Main CLI entry point
2. **era5il_models.py** - Data models and enums
3. **era5il_utils.py** - Utility functions for processing

### Key Processing Steps

1. Data retrieval from Google Cloud Storage
2. Filtering by date range and geographic boundaries
3. Triangulation and interpolation to a regular grid
4. Calculation of derived variables
5. County-level attribution (optional)
6. Export to the specified format

## For Grad Students

This tool is designed to make it easy to acquire climate data for county-level analysis in Illinois. When using the data:

1. Data is provided on a regular grid (approximately 4 points per degree of lat/long)
2. When county attribution is enabled, each grid cell is assigned to a county
3. You can aggregate grid cells by county for county-level analysis
4. All derived variables are calculated using standard meteorological formulas

## Delaunay Triangulation and Interpolation

The tool uses Delaunay triangulation for spatial interpolation. This method is particularly well-suited for climate data because:

1. It handles irregularly spaced input data (common in climate datasets)
2. It preserves the original values at data points
3. It creates a continuous surface without artifacts
4. It's computationally efficient for large datasets

### Technical Details

The interpolation process:
1. Constructs a triangular mesh from the original points
2. For each target point in the regular grid, identifies which triangle contains it
3. Calculates barycentric coordinates within that triangle
4. Uses those coordinates as weights to interpolate the data value

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the ARCO-ERA5 project: https://github.com/google-research/arco-era5
- Developed for the Illinois Department of Public Health climate data processing project
