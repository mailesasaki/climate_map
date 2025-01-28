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