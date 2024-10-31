import xarray as xr
import glob
import pandas as pd
import os
import argparse

def loca2_processing(scenario, variable, year_start, year_end, out_path):
    """
    
    Code to process LOCA2 Datasets for use over Illinois 
    
    
    Inputs:
     - scenario (str) - historical, ssp245, ssp370, ssp585
     - variable (str) - pr (Precipitation), tasmax (Maximum surface air temp.), tasmin (Minimum surface air temp.)
     - year_start (int) - First year you'd like to request
     - year_end (int) - Last year you'd like to request (exclusive)
     - out_path (str) - Directory you'd like to save the dataset in
    Outputs:
     - None, saves Netcdf file to location directed to
    
    """
    # Locating where data is kept
    base_directory = "/data/keeling/a/cristi/a/downscaled_data/LOCA2/"
    models = next(os.walk(base_directory))[1]

    list_dataset_model = []
    # Iterate over models and retrieve files
    for model in models: 
        print(model)
        directory = base_directory +  model + '/' + scenario + '/'
        all_files = glob.glob(directory + '/*')
        
        ens_mem = []
        # Looking to see if file exists for specified requirements
        for file in all_files: 
            ens_mem.append(file.split('.')[3])
        if not ens_mem:
            continue
        list_dataset_mem = []
        # For each ensemble member (i.e. r1i1p1f1, r2i1p1f1, etc.)
        for mem in list(set(ens_mem)): 
            if scenario == 'historical': # Pulling historical files
                files_mem = glob.glob(directory + '/' + variable + '.' + model + '.' + scenario + '.' + mem + '.' 
                                       + '*')
            # Pulling appropriate files for ssp scenarios
            else: 
                files_mem = []
                if year_start < 2045:
                    files_mem.append(glob.glob(directory + '/' + variable + '.' + model + '.' + scenario + '.' + mem +
                                               '.2015-2044.*')[0])
                if year_end > 2075:
                    files_mem.append(glob.glob(directory + '/' + variable + '.' + model + '.' + scenario + '.' + mem + 
                                              '.2075-2100.*')[0])
                if year_end > 2045 and year_start < 2075: 
                    files_mem.append(glob.glob(directory + '/' + variable + '.' + model + '.' + scenario + '.' + mem + 
                                              '.2045-2074.*')[0])
            dataset_mem = xr.open_mfdataset(files_mem,combine="by_coords", use_cftime=True) # Opening datasets
            # Assigning new time coordinates so that datasets from different models cooperate
            dataset_mem = dataset_mem.assign(time=pd.date_range(start=(str(dataset_mem.time[0].values).split(' ')[0]),
                                            freq='D',
                                            periods=len(dataset_mem.time))).sel(time=slice(str(year_start), str(year_end)))
            # Assigning ensemble member name
            dataset_mem['ens_mem'] = mem 
            list_dataset_mem.append(dataset_mem)
        # If only one dataset, assign model to that dataset
        if len(list_dataset_mem) == 1: 
            dataset_model = list_dataset_mem[0]
        # If multiple, concatenate then assign    
        else: 
            dataset_model = xr.concat(list_dataset_mem, dim='ens_mem', coords='minimal', compat='override')
            dataset_model = dataset_model.mean('ens_mem') # Take mean over ensemble
        # Assign model name
        dataset_model['name'] = model
        # Picking out the Illinois region
        dataset_model = dataset_model.sel(lat=slice(36,43.5)).sel(lon=slice(267.2,274))
        list_dataset_model.append(dataset_model)
    # Appending all the datasets for each model together
    dataset = xr.concat(list_dataset_model, dim='name', coords='minimal', compat='override')
    
    # Saving the dataset
    output_file = out_path + '/LOCA2_IL_' + variable + '_' + scenario + '_' + str(year_start) + '-' + str(year_end) + '.nc'
    dataset.to_netcdf(output_file)
    print('Dataset saved to ' + output_file)
    
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
    loca2_processing(scenario, variable, year_start, year_end, out_path)

