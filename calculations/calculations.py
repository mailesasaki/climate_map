from LOCA2.LOCA2_processor import loca2_processing
import xarray as xr
import numpy as np


def complete_loca2(scenario, year_start, year_end):
    """
    Code to create a LOCA2 dataset that contains all three variables (tasmax [maximum daily temperature],
        tasmin [minimum daily temperature], and pr [precipitation]) within the desired time range and in
        the desired scenario
        
    Inputs:
        - scenario (str) - historical, ssp245, ssp370, ssp585
        - year_start (int) - First year you'd like to request
        - year_end (int) - Last year you'd like to request (inclusive)
        
    Output:
        - data_full (Dataset) - Contains tasmax, tasmin, precip from year_start to year_end in scenario
        
    """
    
    data_tasmax = loca2_processing(scenario, 'tasmax', year_start, year_end)
    data_tasmin = loca2_processing(scenario, 'tasmin', year_start, year_end)
    data_precip = loca2_processing(scenario, 'pr', year_start, year_end)
    
    data_full = xr.merge([data_tasmax, data_tasmin, data_precip], fill_value=np.nan)
    return data_full

def stats(dataset):
    """    
    Calculates statistics across the models for all variables
    
    Input:
        - dataset (Dataset or Dataarray) - Needs a dimension called "model"
        
    Output:
        - data_stats (Dataset) - Contains calculations of the mean, standard deviation, and variance
            of the dataset. All statistics stored in a coordinate called "stats"
            
    """
    
    mean = dataset.mean('model')
    mean['stats'] = 'mean'
    
    stdev = dataset.std('model')
    stdev['stats'] = 'stdev'
    
    variance = dataset.var('model')
    variance['stats'] = 'variance'
    
    data_stats = xr.concat([mean, stdev, variance], 'stats')
    return data_stats

def heat_index(RH, T):
    """
    https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml

    Calculates heat index for an array
    
    Inputs:
        RH (DataArray) - Should be in decimal format
        T  (DataArray) - Should be in Kelvins
        
    Outputs:
        hi_alone (DataArray) - Heat index array (in F)
    """
    # Convert to Fahrenheit
    T_F = ((T - 273.15) * 1.8) + 32

    # Convert to relative humidity
    RH_p = RH * 100
    RH_p = RH_p.rename('relative_humidity')
    
    # Standard heat index
    heat_index = 0.5 * (T_F + 61.0 + ((T_F-68.0)*1.2) + (RH_p*0.094))
    heat_index = heat_index.rename('heat_index')

    # Combining temperature, relative humidity, and heat index into a dataset
    hi_set = xr.combine_by_coords((heat_index,T_F,RH_p))
        
    # Heat index for heat index above 80
    heat_index_80 = (-42.379 + 2.04901523*T_F + 10.14333127*RH_p - 0.22475541*T_F*RH_p 
          - 6.83783e-3*T_F**2 - 5.481717e-2*RH_p**2 + 1.22874e-3*T_F**2*RH_p 
          + 8.5282e-4*T_F*RH_p**2 - 1.99e-6*T_F**2*RH_p**2)
    hi_set['heat_index>80'] = heat_index_80
    
    # Replacing heat indices above 80 with the new equation
    hi_set['heat_index'] = xr.where(hi_set['heat_index']>80,
                                    hi_set['heat_index>80'],
                                    hi_set['heat_index']
                                    )
    
    # Heat index for relative humidity under 13% and temps between 80 and 112 F
    heat_index_13 = heat_index_80 - ((13-RH_p)/4) * np.sqrt((17 - abs(T_F - 95))/17)
    hi_set['heat_index_RH<13'] = heat_index_13
    
    hi_set['heat_index'] = xr.where(((hi_set['relative_humidity']<13) & 
                                         (hi_set['2m_temperature']>80) & 
                                         (hi_set['2m_temperature']<112)),
                                    hi_set['heat_index_RH<13'],
                                    hi_set['heat_index'])
    
    # Heat index for relative humidity over 85% and temps between 80 and 87 F
    heat_index_85 = heat_index_80 + ((RH_p-85)/10) * ((87-T_F)/5)
    hi_set['heat_index_RH>85'] = heat_index_85
    hi_set['heat_index'] = xr.where(((hi_set['relative_humidity']>85) & 
                                         (hi_set['2m_temperature']>80) & 
                                         (hi_set['2m_temperature']<87)),
                                    hi_set['heat_index_RH>85'],
                                    hi_set['heat_index'])
    
    # Picking out the heat index dataarray alone
    hi_alone = hi_set['heat_index']

    return hi_alone

def wind_tot(uwind, vwind):
    wind_mag = np.sqrt(vwind**2 + uwind**2)
    wind_dir = np.arctan2(vwind/wind_mag, uwind/wind_mag)
    wind_dir = wind_dir * 180/np.pi
    
    return wind_mag, wind_dir

def wind_chill(T, sfcWind):
    """
    https://www.weather.gov/safety/cold-wind-chill-chart
    
    Calculates wind chill in array format
    
    Inputs:
        T (DataArray) - Temperature in Kelvin format
        sfcWInd (DataArray) - Surface Wind in m/s
    Output:
        wind_chill_alone (DataArray) - Wind Chill array (In F) 
    """
    T_F = T * 9/5 - 459.67 # Convert to Fahrenheit
    sfcWind_mph = 0.44704 * sfcWind # Convert to mph
    sfcWind_mph = sfcWind_mph.rename('surface_wind')
    
    # Calculate wind chill
    wind_chill = 35.74 + 0.6215*T_F - 35.75*(sfcWind_mph**0.16) + 0.4275*T_F*(sfcWind_mph**0.16)
    wind_chill = wind_chill.rename('wind_chill')
    
    # Combining into one dataset
    wind_chill_set = xr.combine_by_coords((wind_chill,T_F,sfcWind_mph))
    
   # Note: The Wind Chill Temperature is defined only for temperatures at or below 50°F and wind speeds above 3 mph.
    wind_chill_set['wind_chill'] = xr.where(((wind_chill_set['2m_temperature']<50) & 
                                                  (wind_chill_set['surface_wind']>3)),
                                              wind_chill_set['wind_chill'],
                                              np.nan)    

    wind_chill_alone = wind_chill_set['wind_chill']
    
    return wind_chill_alone

def apparent_temperature(t2m, wind, vp):
    """
    https://confluence.ecmwf.int/display/FCST/New+parameters%3A+heat+and+cold+indices%2C+mean+radiant+temperature+and+globe+temperature
    
    Inputs:
        t2m - (DataArray) 2m temperature (C)
        wind - (DataArray) 10 m wind speed (m/s)
        vp - (DataArray) 2m vapor pressure (hPa)
    Outputs: 
        apparent_temperature - (DataArray) Apparent temperature (in C)
    """
    
    apparent_temperature = t2m + 0.33*vp - 0.7*wind - 4.0
    
    return apparent_temperature

def vapor_pressure(dewpoint):
    """
    https://www.weather.gov/epz/wxcalc_vaporpressure
    
    Returns vapor pressure in units of hPa/mb
    """
    e = 6.11 * 10**((7.5*dewpoint)/(237.3+dewpoint))
    return e

def normal_effective_temperature(t2m, RH, wind_speed):
    """
    Calculates normal effective temperature for a DataArray
    
    Inputs:
        t2m - (DataArray) 2m air temperature (C)
        RH - (DataArray) 2m relative humidity (%)
        wind_speed - (DataArray) wind speed at 1.2 m above the ground (m/s)
    Output:
        net - (DataArray) normal effective temperature (C)
    """
    
    net = (37 - 
           ((37-t2m)/(0.68-(0.0014*RH)+(1/(1.76+(1.4*wind_speed**0.75)))))
           - (0.29*t2m*(1-(0.01*RH))))
    
    return net

def humidex(t2m, vp):
    """
    Calculate humidex for a DataArray
    
    Inputs:
        t2m (DataArray) - 2m air temperature in C
        vp (DataArray) - vapor pressure in hPa
        
    Output:
        humidex (DataArray) - Humidex in C
    """
    
    humidex = t2m + 0.5555*(vp - 10)
    
    return humidex