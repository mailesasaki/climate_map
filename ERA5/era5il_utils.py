import re
from datetime import datetime
from pathlib import Path

import geopandas as gpd
import numpy as np
import regionmask
import scipy.spatial
import typer
import xarray as xr
from climate_map.ERA5.era5il_models import GeographicBoundaries


def validate_date_format(value: str) -> str:
    """Validate that date is in YYYY-MM-DD format

    Args:
        value: Date string to validate

    Returns:
        The validated date string

    Raises:
        typer.BadParameter: If the date format is invalid
    """
    DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    if not DATE_PATTERN.match(value):
        raise typer.BadParameter("Date must be in YYYY-MM-DD format")

    # Additional validation to ensure it's a valid date
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise typer.BadParameter(f"Invalid date: {value}")

    return value


def build_triangulation(x: np.ndarray, y: np.ndarray) -> scipy.spatial.Delaunay:
    """
    Creates a Delaunay triangulation from longitude and latitude coordinates.

    Delaunay triangulation connects a set of points to form a triangular mesh where no point is
    inside the circumcircle of any triangle. This is useful for interpolation because it creates
    a mesh that works well with irregularly spaced data points, which is common in climate data.

    Args:
        x: Array of x-coordinates (longitudes)
        y: Array of y-coordinates (latitudes)

    Returns:
        A Delaunay triangulation object containing information about the triangular mesh
    """

    # Stack the coordinates to create a 2D array where each row is a coordinate pair [lon, lat]
    grid = np.column_stack((x, y))

    # Create and return the Delaunay triangulation
    return scipy.spatial.Delaunay(grid)


def interpolate(
    data: np.ndarray, tri: scipy.spatial.Delaunay, mesh: np.ndarray
) -> np.ndarray:
    """
    Interpolates climate data values from irregular grid points to a regular grid using barycentric interpolation.

    Args:
        data: Array of data values at the original grid points
        tri: Delaunay triangulation object created from the original grid points
        mesh: Regular grid of points where we want to interpolate values

    Returns:
        Array of interpolated data values at each point in the mesh
    """
    # Find which triangle (simplex) each mesh point falls into
    indices = tri.find_simplex(mesh)

    # Get the number of dimensions
    ndim = tri.transform.shape[-1]

    # Extract transformation matrices for each point's containing triangle
    T_inv = tri.transform[indices, :ndim, :]

    # Extract offset vectors for each point's triangle
    r = tri.transform[indices, ndim, :]

    # Calculate the first two barycentric coordinates for each point
    # using Einstein summation for efficient matrix multiplication
    c = np.einsum("...ij,...j", T_inv, mesh - r)

    # Calculate the third barycentric coordinate and combine all three
    # (barycentric coordinates sum to 1)
    c = np.concatenate([c, 1 - c.sum(axis=-1, keepdims=True)], axis=-1)

    # For 1D data arrays, reshape the simplices for proper indexing
    # Instead of data[:, tri.simplices[indices]] which assumes data is 2D
    data_at_vertices = data[tri.simplices[indices]]

    # Use the barycentric coordinates to interpolate the data values
    # This is a weighted average of the values at the three vertices of each triangle
    result = np.einsum("...i,...i", data_at_vertices, c)

    # Replace results for points outside all triangles with NaN
    return np.where(indices == -1, np.nan, result)


def vapor_pressure(dewpoint: xr.DataArray) -> xr.DataArray:
    """
    Calculates vapor pressure from dewpoint temperature using the Magnus-Tetens formula.

    Args:
        dewpoint: DataArray of 2m dewpoint temperature in Kelvin

    Returns:
        DataArray of vapor pressure in hPa/mb
    """
    # Convert from Kelvin to Celsius
    dewpoint_C = dewpoint - 273.15

    # Calculate vapor pressure using Magnus-Tetens formula
    e = 6.11 * 10 ** ((7.5 * dewpoint_C) / (237.3 + dewpoint_C))

    return e


def relative_humidity(
    temperature: xr.DataArray, dewpoint: xr.DataArray
) -> xr.DataArray:
    """
    Calculates relative humidity from temperature and dewpoint temperature.

    Args:
        temperature: DataArray of temperature in Kelvin
        dewpoint: DataArray of dewpoint temperature in Kelvin

    Returns:
        DataArray of relative humidity as a decimal (0-1)
    """
    # Calculate actual vapor pressure from dewpoint
    e = vapor_pressure(dewpoint)

    # Convert temperature from Kelvin to Celsius
    temperature_C = temperature - 273.15

    # Calculate saturation vapor pressure using the same formula
    es = 6.11 * 10 ** ((7.5 * temperature_C) / (237.3 + temperature_C))

    # Calculate relative humidity as a ratio (0-1)
    rh = e / es

    return rh


def wind_tot(
    uwind: xr.DataArray, vwind: xr.DataArray
) -> tuple[xr.DataArray, xr.DataArray]:
    """
    Calculates wind magnitude and direction from wind vector components.

    Args:
        uwind: DataArray of east-west wind component in m/s (positive = eastward)
        vwind: DataArray of north-south wind component in m/s (positive = northward)

    Returns:
        Tuple containing:
            - wind_mag: DataArray of wind magnitude (speed) in m/s
            - wind_dir: DataArray of wind direction in degrees (meteorological convention)
    """
    # Calculate wind magnitude (speed) using the Pythagorean theorem
    wind_mag = np.sqrt(vwind**2 + uwind**2)

    # Calculate wind direction using arctan2
    # Note: division by wind_mag only where wind_mag is non-zero to avoid division by zero
    # We're creating a mask where wind_mag is zero
    zero_wind_mask = wind_mag == 0

    # Calculate the direction where wind is non-zero
    temp_u = uwind.copy()
    temp_v = vwind.copy()

    # Avoid division by zero by temporarily setting wind_mag to 1 where it's zero
    # This won't affect the result since we'll mask these points later
    temp_mag = wind_mag.copy()
    temp_mag = xr.where(zero_wind_mask, 1.0, temp_mag)

    # Calculate direction
    wind_dir = np.arctan2(temp_v / temp_mag, temp_u / temp_mag)

    # Convert from radians to degrees
    wind_dir = wind_dir * 180 / np.pi

    # Set direction to NaN where wind magnitude is zero
    wind_dir = xr.where(zero_wind_mask, np.nan, wind_dir)

    return wind_mag, wind_dir


def assign_counties_to_grid(data: xr.Dataset, county_file: Path) -> xr.Dataset:
    """
    Assigns Illinois county names to each grid cell in the dataset.

    Args:
        data: xarray Dataset with climate data on a regular grid
        county_file: Path to GeoJSON file with county boundaries

    Returns:
        Dataset with an additional 'county' coordinate
    """
    # Load county boundaries
    counties = gpd.read_file(county_file)

    # Create a mask for each county using the DataFrame index instead of looking for an 'index' column
    # The default behavior (numbers=None) will use the position in the DataFrame
    masks = regionmask.mask_geopandas(counties, data.lon, data.lat)

    # Convert the mask to a DataArray with county names
    county_names = counties["NAME"].values
    county_indices = masks.values

    # Create a county name array with the same shape as the mask
    county_array = np.full(county_indices.shape, "", dtype="object")

    # Assign county names based on indices
    for i, name in enumerate(county_names):
        county_array[county_indices == i] = name

    # Set cells outside any county to NaN
    county_array[county_indices == -1] = np.nan

    # Add as a coordinate to the dataset
    county_da = xr.DataArray(
        county_array, dims=["lat", "lon"], coords={"lat": data.lat, "lon": data.lon}
    )
    data = data.assign_coords(county=county_da)

    return data


def prepare_climate_grid(
    start_date: str, end_date: str, variables: list, IL_boundaries: GeographicBoundaries
) -> xr.Dataset:
    """
    Prepares a regular grid of climate data for the given time period and variables.

    This function retrieves ERA5 data from Google Cloud Storage, filters it to the specified
    region and time period, and creates a regular grid through interpolation.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        variables: List of climate variables to retrieve
        IL_boundaries: min/max latitude and longitude from IL_boundaries basemodel.

    Returns:
        xarray Dataset with interpolated climate data on a regular grid

    """
    # Open the ERA5 dataset
    climate_data = xr.open_zarr(
        "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3",
        chunks={"time": 48},
        consolidated=True,
        decode_timedelta=True,  # Explicitly set decode_timedelta
    )

    # Subset by time first - this is straightforward as time is a dimension
    data_subset_time = climate_data.sel(time=slice(start_date, end_date))

    # Create a spatial mask using the original approach
    # This is necessary because longitude and latitude might be variables, not coordinates
    print(f"\n=== Retrieving ERA5 data for time period {start_date} to {end_date} ===")
    print(
        f"Geographic area: Longitude {IL_boundaries.lon_min}-{IL_boundaries.lon_max}, Latitude {IL_boundaries.lat_min}-{IL_boundaries.lat_max}"
    )

    # Create mask
    mask = (
        (data_subset_time.longitude >= IL_boundaries.lon_min)
        & (data_subset_time.longitude <= IL_boundaries.lon_max)
        & (data_subset_time.latitude >= IL_boundaries.lat_min)
        & (data_subset_time.latitude <= IL_boundaries.lat_max)
    ).compute()

    # Apply the mask - we'll compute only when needed in later operations
    data_subset_il = data_subset_time.where(mask, drop=True)

    # Handle derived variables - build the base variables list efficiently
    base_variables = []
    derived_variables = set()
    print("\n=== Processing the following variables ===\nRequested:")

    for var in variables:
        if var == "vapor_pressure":
            derived_variables.add(var)
            if "d2m" not in base_variables:
                base_variables.append("d2m")
            print(f"  - {var} (derived from d2m)")
        elif var == "surface_wind":
            derived_variables.add(var)
            if "u10" not in base_variables:
                base_variables.append("u10")
            if "v10" not in base_variables:
                base_variables.append("v10")
            print(f"  - {var} (derived from u10 and v10)")
        elif var == "relative_humidity":
            derived_variables.add(var)
            if "t2m" not in base_variables:
                base_variables.append("t2m")
            if "d2m" not in base_variables:
                base_variables.append("d2m")
            print(f"  - {var} (derived from t2m and d2m)")
        else:
            base_variables.append(var)
            print(f"  - {var} (direct)")

    print("\nBase variables being retrieved from ERA5:")
    for var in base_variables:
        print(f"  - {var}")

    # Now project only the variables requested
    # This further reduces the data loaded into memory
    data_subset_projection = data_subset_il[base_variables]

    longitudes = data_subset_projection["longitude"].compute().values
    latitudes = data_subset_projection["latitude"].compute().values

    # Create a triangulation
    tri = build_triangulation(longitudes, latitudes)

    # Create regular arrays of longitudes and latitudes (4 points per degree)
    longitude = np.linspace(
        IL_boundaries.lon_min,
        IL_boundaries.lon_max,
        num=round((IL_boundaries.lon_max - IL_boundaries.lon_min) * 4) + 1,
    )
    latitude = np.linspace(
        IL_boundaries.lat_min,
        IL_boundaries.lat_max,
        num=round((IL_boundaries.lat_max - IL_boundaries.lat_min) * 4) + 1,
    )

    # Create a grid of all coordinate pairs
    mesh = np.stack(np.meshgrid(longitude, latitude, indexing="ij"), axis=-1)

    # Initialize the output dataset
    ds_out = xr.Dataset(
        coords={"time": data_subset_projection.time, "lon": longitude, "lat": latitude}
    )

    # Process each variable
    print("\n=== Processing variables ===")
    for var in base_variables:
        print(f"Processing variable: {var}")
        # Interpolate each time step
        result = np.zeros(
            (data_subset_projection.time.size, longitude.size, latitude.size)
        )

        for t in range(data_subset_projection.time.size):
            # Get data for this time step - compute to convert from dask to numpy
            var_data = data_subset_projection[var].isel(time=t).compute().values

            # Apply interpolation
            result[t] = interpolate(var_data, tri, mesh)

        # Add to the output dataset
        ds_out[var] = xr.DataArray(result, dims=["time", "lon", "lat"])

    # Now calculate derived variables
    print("\n=== Calculating derived variables ===")

    # Only calculate the derived variables that were actually requested
    if "vapor_pressure" in derived_variables and "d2m" in base_variables:
        print("Calculating vapor pressure")
        ds_out["vapor_pressure"] = vapor_pressure(ds_out["d2m"])

    if (
        "surface_wind" in derived_variables
        and "u10" in base_variables
        and "v10" in base_variables
    ):
        print("Calculating wind components")
        wind_mag, wind_dir = wind_tot(ds_out["u10"], ds_out["v10"])
        ds_out["wind_speed"] = wind_mag
        ds_out["wind_direction"] = wind_dir

    if (
        "relative_humidity" in derived_variables
        and "t2m" in base_variables
        and "d2m" in base_variables
    ):
        print("Calculating relative humidity")
        ds_out["relative_humidity"] = relative_humidity(ds_out["t2m"], ds_out["d2m"])

    print("\n=== Processing complete ===")
    return ds_out


def save_dataset(data: xr.Dataset, filename: Path, format: str) -> str:
    """
    Saves an xarray Dataset to disk in the specified format.

    Args:
        data: xarray Dataset to save
        filename: Base filename (without extension) as a Path object
        format: Output format ('csv', 'parquet', or 'netcdf')

    Returns:
        Path to the saved file
    """
    # Create directory if it doesn't exist
    output_dir = filename.parent
    if output_dir.name and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    if format.lower() == "netcdf":
        # Save as NetCDF
        out_file = filename.with_suffix(".nc")
        data.to_netcdf(str(out_file))
    elif format.lower() == "csv":
        # Convert to DataFrame and save as CSV
        out_file = filename.with_suffix(".csv")
        df = data.to_dataframe()
        df.to_csv(str(out_file))
    elif format.lower() == "parquet":
        # Convert to DataFrame and save as Parquet
        out_file = filename.with_suffix(".parquet")
        df = data.to_dataframe()
        df.to_parquet(str(out_file))
    else:
        raise ValueError(f"Unsupported format: {format}")

    return str(out_file)
