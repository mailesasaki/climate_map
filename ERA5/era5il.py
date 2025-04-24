#!/usr/bin/env python
"""
ERA5 Climate Data Processor for Illinois

This script downloads, processes, and exports ERA5 climate data for the state of Illinois.
It can filter by date range, select specific variables, and output in various formats.

Created for the Illinois Department of Public Health climate data processing project.
"""

import warnings
from pathlib import Path
from typing import List

import typer
from climate_map.ERA5.era5il_models import (
    IL_boundaries,
    WeatherVariable,
    weather_variable_info,
)
from climate_map.ERA5.era5il_utils import (
    assign_counties_to_grid,
    prepare_climate_grid,
    save_dataset,
    validate_date_format,
)
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

# Suppress the Google Cloud SDK credentials warning
warnings.filterwarnings(
    "ignore",
    message="Your application has authenticated using end user credentials from Google Cloud SDK without a quota project.*",
    category=UserWarning,
    module="google.auth._default",
)

app = typer.Typer(help="Process ERA5 climate data for Illinois")
console = Console()


@app.command(name="list-variables")
def list_variables():
    """List all available weather variables with their details."""
    console.print(
        "[bold green]Available Weather Variables for ERA5 Climate Data[/bold green]\n"
    )

    # Group variables by category for better organization
    categories = {
        "Surface Parameters": ["cape", "tciw", "sst", "skt"],
        "Soil and Ice Parameters": [
            "stl1",
            "stl2",
            "stl3",
            "stl4",
            "tsn",
            "swvl1",
            "swvl2",
            "swvl3",
            "swvl4",
            "istl1",
            "istl2",
            "istl3",
            "istl4",
        ],
        "Total Column Parameters": ["tclw", "tcrw", "tcsw", "tcw", "tcwv"],
        "General Surface Parameters": ["z", "sp", "msl", "tcc", "lcc", "mcc", "hcc"],
        "Wind Components": ["u10", "v10", "u100", "v100"],
        "Temperature Parameters": ["t2m", "d2m"],
        "Derived Parameters": ["vapor_pressure", "surface_wind", "relative_humidity"],
    }

    for category, var_codes in categories.items():
        console.print(f"[bold cyan]{category}[/bold cyan]")

        for var_code in var_codes:
            # Find the matching WeatherVariable enum
            var_enum = None
            for weather_var in WeatherVariable:
                if weather_var.value == var_code:
                    var_enum = weather_var
                    break

            if var_enum and var_enum in weather_variable_info:
                var_info = weather_variable_info[var_enum]
                console.print(
                    f"  [bold]{var_code}[/bold]: {var_info.name} ({var_info.units})"
                )
                # Print documentation URL if available and not empty
                if var_info.docs and var_info.docs != "":
                    console.print(f"    [dim]Documentation: {var_info.docs}[/dim]")
            else:
                # Fallback for variables not in the weather_variable_info dict
                console.print(
                    f"  [bold]{var_code}[/bold]: No detailed information available"
                )

        console.print("")

    console.print(
        "[italic]Note: Use these variable codes with the --variables option when processing data.[/italic]"
    )


@app.command()
def process(
    start_date: str = typer.Option(
        ...,
        "--start-date",
        help="Start date in YYYY-MM-DD format",
        callback=validate_date_format,
    ),
    end_date: str = typer.Option(
        ...,
        "--end-date",
        help="End date in YYYY-MM-DD format",
        callback=validate_date_format,
    ),
    variables: List[str] = typer.Option(
        [
            "t2m",  # 2 metre temperature
            "d2m",  # 2 metre dewpoint temperature
            "u10",  # 10 metre U wind component
            "v10",  # 10 metre V wind component
            "vapor_pressure",  # Calculated from dewpoint
            "surface_wind",    # Wind speed and direction
            "relative_humidity"  # Calculated from temperature and dewpoint
        ],
        "--variables",
        "-v",
        help="List of variables to include. Default is common meteorological variables. Use 'list-variables' command to see all options, or 'all' for all variables.",
    ),
    output_format: str = typer.Option(
        "parquet",
        "--format",
        "-f",
        help="Output file format (parquet, csv, netcdf)",
    ),
    output_path: Path = typer.Option(
        "./output",
        "--output-path",
        "-o",
        help="Directory to save the output file",
    ),
    include_counties: bool = typer.Option(
        True,
        "--include-counties/--no-counties",
        help="Whether to add county information to each grid cell",
    ),
    county_file: Path = typer.Option(
        "../county_boundaries/illinois_counties.geojson",
        "--county-file",
        help="Path to GeoJSON file with county boundaries",
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
    ),
):
    """Process ERA5 climate data for Illinois and save to the specified format.

    To see a list of all available weather variables, run the 'list-variables' command.
    """
    # Create output directory if it doesn't exist
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    # Process 'all' variables option
    if variables and "all" in variables:
        # Use all available variables except derived ones
        available_vars = [v.value for v in WeatherVariable]
        # Add derived variables specifically
        derived_vars = ["vapor_pressure", "surface_wind", "relative_humidity"]
        variables = available_vars + derived_vars

    # Generate output filename
    output_file_name = (
        f"ERA5_IL_{start_date.replace('-', '')}_to_{end_date.replace('-', '')}"
    )
    output_file_path = output_path / output_file_name

    # Show processing information
    console.print("[bold green]Processing ERA5 climate data for Illinois[/bold green]")
    console.print(f"Time period: {start_date} to {end_date}")
    console.print(f"Variables: {', '.join(variables)}")
    console.print(f"Output format: {output_format}")
    console.print(f"Output file: {output_file_path}.{output_format}")

    # Process the data with a progress display
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}[/bold green]"),
        TimeElapsedColumn(),
    ) as progress:
        # Start tasks
        task1 = progress.add_task("Preparing climate grid...", total=None)

        data = prepare_climate_grid(
            start_date=start_date,
            end_date=end_date,
            variables=variables,
            IL_boundaries=IL_boundaries,
        )
        progress.update(task1, completed=True, description="Climate grid prepared")

        # Add county information if requested
        if include_counties:
            task2 = progress.add_task("Adding county information...", total=None)
            data = assign_counties_to_grid(data, county_file)
            progress.update(
                task2, completed=True, description="County information added"
            )

        # Save the data
        task3 = progress.add_task("Saving data...", total=None)
        saved_file_path = save_dataset(data, output_file_path, output_format)
        progress.update(task3, completed=True, description="Data saved")

    # Show completion message
    console.print("\n[bold green]Processing complete![/bold green]")
    console.print(f"Data saved to: {saved_file_path}")
    console.print("\nIncluded variables:")
    for var in variables:
        # Get nice variable name if available
        var_info = None
        for weather_var in WeatherVariable:
            if weather_var.value == var:
                var_info = weather_variable_info.get(weather_var)
                break

        if var_info:
            console.print(f"  - {var}: {var_info.name} ({var_info.units})")
        else:
            if var == "vapor_pressure":
                console.print(f"  - {var}: Vapor pressure (hPa/mb)")
            elif var == "surface_wind":
                console.print(
                    f"  - {var}: Surface wind speed (m/s) and direction (degrees)"
                )
            elif var == "relative_humidity":
                console.print(f"  - {var}: Relative humidity (0-1)")
            else:
                console.print(f"  - {var}")


if __name__ == "__main__":
    app()
