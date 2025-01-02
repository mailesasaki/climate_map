import xarray as xr
import glob
import pandas as pd
import os
import argparse
from datetime import date


def loca2_processing(scenario, variable, year_start, year_end):
    """
    
    Code to process LOCA2 Datasets for use over Illinois 
    
    
    Inputs:
     - scenario (str) - historical, ssp245, ssp370, ssp585
     - variable (str) - pr (Precipitation), tasmax (Maximum surface air temp.), tasmin (Minimum surface air temp.)
     - year_start (int) - First year you'd like to request
     - year_end (int) - Last year you'd like to request (inclusive)
    Outputs:
     - dataset (Dataset) - Contains data of given variable in Illinois within the designated 
    
    """
    # Locating the catalog
    catalog = pd.read_csv('/data/keeling/a/cristi/a/downscaled_data/LOCA2/LOCA2_catalog.csv')

    list_dataset_model = []
    for model in catalog.model.unique(): 
        print(model)
        # Looking to see if file exists for specified requirements
        cat_pull = catalog.loc[(catalog['variable']==variable) & (catalog['model']==model) & (catalog['scheme']==scenario)]
        # For each ensemble member (i.e. r1i1p1f1, r2i1p1f1, etc.)
        list_dataset_mem = []
        for mem in cat_pull.experiment_id.unique(): 
            mem_data = cat_pull.loc[(cat_pull['experiment_id']==mem)]['path'].to_list()
            if model=='CanESM5' and mem=='r3i1p1f1' and scenario=='ssp585' and variable=='pr':
                continue
            dataset_mem = xr.open_mfdataset(mem_data, combine="by_coords", use_cftime=True) # Opening datasets
            if variable not in dataset_mem.variables:
                continue
            # Assigning new time coordinates so that datasets from different models cooperate
            dataset_mem = dataset_mem.assign(time=pd.date_range(start=(str(dataset_mem.time[0].values).split(' ')[0]),
                                            freq='D',
                                            periods=len(dataset_mem.time))).sel(time=slice(str(year_start), str(year_end)))
            # Assigning ensemble member name
            dataset_mem['ens_mem'] = mem 
            list_dataset_mem.append(dataset_mem)
        if len(list_dataset_mem) == 0:
            continue
        # If only one dataset, assign model to that dataset
        elif len(list_dataset_mem) == 1: 
            dataset_model = list_dataset_mem[0]
        # If multiple, concatenate then assign    
        else: 
            dataset_model = xr.concat(list_dataset_mem, dim='ens_mem', coords='minimal', compat='override')
            dataset_model = dataset_model.mean('ens_mem') # Take mean over ensemble
        # Assign model name
        dataset_model['model'] = model
        # Picking out the Illinois region
        dataset_model = dataset_model.sel(lat=slice(36,43.5)).sel(lon=slice(267.2,274))
        list_dataset_model.append(dataset_model)
    # Appending all the datasets for each model together
    dataset = xr.concat(list_dataset_model, dim='model', coords='minimal', compat='override')
    return dataset

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, type=str)
    parser.add_argument("--variable", required=True, type=str)
    parser.add_argument("--year_start", required=True, type=int)
    parser.add_argument("--year_end", required=True, type=int)
    parser.add_argument("--out_path", required=True, type=str)
    args = parser.parse_args()
    
    scenario = args.scenario
    variable = args.variable
    year_start = args.year_start
    year_end = args.year_end
    out_path = args.out_path
    dataset = loca2_processing(scenario, variable, year_start, year_end)
          
    # Saving the dataset
    output_file = (out_path + '/LOCA2_IL_' + variable + '_' + scenario + '_' + str(year_start) + '-' + str(year_end) + '_' + 
                   str(date.today()) + '.nc')
    dataset.to_netcdf(output_file)
    print('Dataset saved to ' + output_file)

