

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import xarray as xr
    from climate_map.ERA5 import era5il, era5il_models, era5il_utils
    from climate_map.ERA5.era5il import IL_boundaries
    import rich
    import numpy as np
    return IL_boundaries, era5il_utils, np, rich, xr


@app.cell
def _():
    start_date = "2022-01-01"
    end_date = "2022-01-02"
    variables = ["t2m"]
    return end_date, start_date, variables


@app.cell
def _(IL_boundaries, end_date, start_date, xr):
    climate_data = xr.open_zarr(
        "gs://gcp-public-data-arco-era5/co/single-level-reanalysis.zarr",
        chunks={"time": 48},
        consolidated=True,
        decode_timedelta=True,  # Explicitly set decode_timedelta
    )

    data_subset_time = climate_data.sel(time=slice(start_date, end_date))

    # Create mask
    mask = (
        (data_subset_time.longitude >= IL_boundaries.lon_min)
        & (data_subset_time.longitude <= IL_boundaries.lon_max)
        & (data_subset_time.latitude >= IL_boundaries.lat_min)
        & (data_subset_time.latitude <= IL_boundaries.lat_max)
    ).compute()

    # Apply the mask - we'll compute only when needed in later operations
    data_subset_il = data_subset_time.where(mask, drop=True)
    return (data_subset_il,)


@app.cell
def _(data_subset_il):
    data_subset_il
    return


@app.cell
def _(data_subset_il, variables):
    data_subset_projection = data_subset_il[variables]

    longitudes = data_subset_projection["longitude"].compute().values
    latitudes = data_subset_projection["latitude"].compute().values
    return data_subset_projection, latitudes, longitudes


@app.cell
def _(data_subset_projection):
    data_subset_projection
    return


@app.cell
def _(latitudes):
    latitudes
    return


@app.cell
def _(longitudes):
    longitudes
    return


@app.cell
def _(era5il_utils, latitudes, longitudes):
    # Create a triangulation
    tri = era5il_utils.build_triangulation(longitudes, latitudes)

    tri
    return


@app.cell
def _(IL_boundaries, np, rich):
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

    rich.print(f"Longitude: {longitude}, Latitude: {latitude}")
    return latitude, longitude


@app.cell
def _(latitude, longitude, np):
    # Create a grid of all coordinate pairs
    mesh = np.stack(np.meshgrid(longitude, latitude, indexing="ij"), axis=-1)

    mesh
    return


@app.cell
def _(data_subset_projection, latitude, longitude, xr):
    # Initialize the output dataset
    ds_out = xr.Dataset(
        coords={
            "time": data_subset_projection.time,
            "lon": longitude,
            "lat": latitude,
        }
    )

    ds_out
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
