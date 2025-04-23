from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field


class ERA5OutputFormat(Enum):
    NETCDF = "netcdf"
    PARQUET = "parquet"
    CSV = "csv"


class GeographicBoundaries(BaseModel):
    lon_min: float = Field(..., description="Minimum longitude boundary")
    lon_max: float = Field(..., description="Maximum longitude boundary")
    lat_min: float = Field(..., description="Minimum latitude boundary")
    lat_max: float = Field(..., description="Maximum latitude boundary")

    class Config:
        validate_assignment = True


# Create an instance with Illinois boundaries
IL_boundaries = GeographicBoundaries(
    lon_min=267.2, lon_max=274.0, lat_min=36.0, lat_max=43.5
)


class WeatherVariable(str, Enum):
    # Surface parameters
    cape = "cape"  # convective available potential energy
    tciw = "tciw"  # total column cloud ice water
    sst = "sst"  # sea surface temperature
    skt = "skt"  # skin temperature

    # Soil and ice parameters
    stl1 = "stl1"  # soil temperature level 1
    stl2 = "stl2"  # soil temperature level 2
    stl3 = "stl3"  # soil temperature level 3
    stl4 = "stl4"  # soil temperature level 4
    tsn = "tsn"  # temperature of snow layer
    swvl1 = "swvl1"  # volumetric soil water layer 1
    swvl2 = "swvl2"  # volumetric soil water layer 2
    swvl3 = "swvl3"  # volumetric soil water layer 3
    swvl4 = "swvl4"  # volumetric soil water layer 4
    istl1 = "istl1"  # ice temperature layer 1
    istl2 = "istl2"  # ice temperature layer 2
    istl3 = "istl3"  # ice temperature layer 3
    istl4 = "istl4"  # ice temperature layer 4

    # Total column parameters
    tclw = "tclw"  # total column cloud liquid water
    tcrw = "tcrw"  # total column rain water
    tcsw = "tcsw"  # total column snow water
    tcw = "tcw"  # total column water
    tcwv = "tcwv"  # total column vertically-integrated water vapour

    # General surface parameters
    z = "z"  # Geopotential
    sp = "sp"  # Surface pressure
    msl = "msl"  # Mean sea level pressure
    tcc = "tcc"  # Total cloud cover
    lcc = "lcc"  # Low cloud cover
    mcc = "mcc"  # Medium cloud cover
    hcc = "hcc"  # High cloud cover

    # Wind components
    u10 = "u10"  # 10 metre U wind component
    v10 = "v10"  # 10 metre V wind component
    u100 = "u100"  # 100 metre U wind component
    v100 = "v100"  # 100 metre V wind component

    # Temperature parameters
    t2m = "t2m"  # 2 metre temperature
    d2m = "d2m"  # 2 metre dewpoint temperature

    # Derived parameters
    vapor_pressure = "vapor-pressure"
    surface_wind = "surface-wind"
    relative_humidity = "relative-humidity"


class WeatherVariableInfo(BaseModel):
    name: str = Field(..., description="Full variable name")
    units: str = Field(..., description="Units of measurement")
    docs: str = Field(..., description="Documentation URL")
    config: str = Field(..., description="Configuration file")


# Dictionary of WeatherVariableInfo instances with WeatherVariable enum values as keys
weather_variable_info: Dict[WeatherVariable, WeatherVariableInfo] = {
    WeatherVariable.cape: WeatherVariableInfo(
        name="convective available potential energy",
        units="J kg^-1",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=59",
        config="era5_sfc_cape.cfg",
    ),
    WeatherVariable.tciw: WeatherVariableInfo(
        name="total column cloud ice water",
        units="kg m^-2",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=79",
        config="era5_sfc_cape.cfg",
    ),
    WeatherVariable.u100: WeatherVariableInfo(
        name="100 metre U wind component",
        units="m s^-1",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=228246",
        config="era5_sfc_cape.cfg",
    ),
    WeatherVariable.v100: WeatherVariableInfo(
        name="100 metre V wind component",
        units="m s^-1",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=228247",
        config="era5_sfc_cape.cfg",
    ),
    WeatherVariable.sst: WeatherVariableInfo(
        name="sea surface temperature",
        units="Pa",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=34",
        config="era5_sfc_cisst.cfg",
    ),
    WeatherVariable.skt: WeatherVariableInfo(
        name="skin temperature",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=235",
        config="era5_sfc_cisst.cfg",
    ),
    WeatherVariable.stl1: WeatherVariableInfo(
        name="soil temperature level 1",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=139",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.stl2: WeatherVariableInfo(
        name="soil temperature level 2",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=170",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.stl3: WeatherVariableInfo(
        name="soil temperature level 3",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=183",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.stl4: WeatherVariableInfo(
        name="soil temperature level 4",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=236",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.tsn: WeatherVariableInfo(
        name="temperature of snow layer",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=238",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.swvl1: WeatherVariableInfo(
        name="volumetric soil water layer 1",
        units="m^3 m^-3",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=39",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.swvl2: WeatherVariableInfo(
        name="volumetric soil water layer 2",
        units="m^3 m^-3",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=40",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.swvl3: WeatherVariableInfo(
        name="volumetric soil water layer 3",
        units="m^3 m^-3",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=41",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.swvl4: WeatherVariableInfo(
        name="volumetric soil water layer 4",
        units="m^3 m^-3",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=42",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.istl1: WeatherVariableInfo(
        name="ice temperature layer 1",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=35",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.istl2: WeatherVariableInfo(
        name="ice temperature layer 2",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=36",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.istl3: WeatherVariableInfo(
        name="ice temperature layer 3",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=37",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.istl4: WeatherVariableInfo(
        name="ice temperature layer 4",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=38",
        config="era5_sfc_soil.cfg",
    ),
    WeatherVariable.tclw: WeatherVariableInfo(
        name="total column cloud liquid water",
        units="kg m^-2",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=78",
        config="era5_sfc_tcol.cfg",
    ),
    WeatherVariable.tcrw: WeatherVariableInfo(
        name="total column rain water",
        units="kg m^-2",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=228089",
        config="era5_sfc_tcol.cfg",
    ),
    WeatherVariable.tcsw: WeatherVariableInfo(
        name="total column snow water",
        units="kg m^-2",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=228090",
        config="era5_sfc_tcol.cfg",
    ),
    WeatherVariable.tcw: WeatherVariableInfo(
        name="total column water",
        units="kg m^-2",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=136",
        config="era5_sfc_tcol.cfg",
    ),
    WeatherVariable.tcwv: WeatherVariableInfo(
        name="total column vertically-integrated water vapour",
        units="kg m^-2",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=137",
        config="era5_sfc_tcol.cfg",
    ),
    WeatherVariable.z: WeatherVariableInfo(
        name="Geopotential",
        units="m^2 s^-2",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=129",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.sp: WeatherVariableInfo(
        name="Surface pressure",
        units="Pa",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=134",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.msl: WeatherVariableInfo(
        name="Mean sea level pressure",
        units="Pa",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=151",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.tcc: WeatherVariableInfo(
        name="Total cloud cover",
        units="(0 - 1)",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=164",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.u10: WeatherVariableInfo(
        name="10 metre U wind component",
        units="m s^-1",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=165",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.v10: WeatherVariableInfo(
        name="10 metre V wind component",
        units="m s^-1",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=166",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.t2m: WeatherVariableInfo(
        name="2 metre temperature",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=167",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.d2m: WeatherVariableInfo(
        name="2 metre dewpoint temperature",
        units="K",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=168",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.lcc: WeatherVariableInfo(
        name="Low cloud cover",
        units="(0 - 1)",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=186",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.mcc: WeatherVariableInfo(
        name="Medium cloud cover",
        units="(0 - 1)",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=187",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.hcc: WeatherVariableInfo(
        name="High cloud cover",
        units="(0 - 1)",
        docs="https://apps.ecmwf.int/codes/grib/param-db?id=188",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.vapor_pressure: WeatherVariableInfo(
        name="Vapor pressure",
        units="mb",
        docs="Calculated from dew_point_temperature variable",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.surface_wind: WeatherVariableInfo(
        name="Surface wind",
        units="m/s (magnitude) and deg (direction)",
        docs="Calculated from u_component_of_wind and v_component_of_wind variables",
        config="era5_sfc.cfg",
    ),
    WeatherVariable.relative_humidity: WeatherVariableInfo(
        name="Relative humidity",
        units="(0 - 1)",
        docs="Calculated from temperature and dew_point_temperature variables",
        config="era5_sfc.cfg",
    ),
}
