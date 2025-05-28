import ee
import xarray as xr

def era5_heat_load(variable, section, i_date, f_date):
    """
    https://gee-community-catalog.org/projects/era5_heat/ 

    Loading data from ERA5-Heat

    Inputs:
        variable - (list or str) Variables to call
            UTCI - utci_mean, utci_max, utci_min, utci_median
            MRT - mrt_mean, mrt_max, mrt_min, mrt_median
        section - (list) Geometrical cross section
        i_date (str) - First date you want (YYYY-MM-DD)
        f_date (str) - Last date you want (YYYY-MM-DD)  
    Outputs:
        era5_dataset - (Dataset) Processed dataset with data from ERA5-HEAT
        
    """
    # Trigger the authentication flow.
    ee.Authenticate()
    
    # Initialize the library.
    ee.Initialize(project=None)

    # Import ERA5-Heat
    era5_heat = ee.ImageCollection('projects/climate-engine-pro/assets/ce-era5-heat')

    # Picking out the designated region
    area = ee.Geometry.Rectangle(section)

    if type(variable) == str:
        variable = [variable]

    era5_filtered = era5_heat.select(variable).filterDate(i_date, f_date)

    era5_dataset = xr.open_dataset(era5_filtered, engine='ee', scale=0.25, geometry=area,
                                     projection=era5_filtered.first().select(0).projection(),
                                     use_cftime=True, fast_time_slicing=True)
    era5_dataset.load()

    return era5_dataset