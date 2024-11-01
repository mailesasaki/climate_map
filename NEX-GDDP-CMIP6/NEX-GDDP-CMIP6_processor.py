import ee
import pandas as pd
import xee
import xarray as xr
import glob
import argparse

def nexgddpcmip6_processing(year_start, year_end, variable, scenario, out_path, project=None):
    model_list = ['ACCESS-CM2', 'ACCESS-ESM1-5', 'BCC-CSM2-MR', 'CESM2', 'CESM2-WACCM', 'CMCC-CM2-SR5', 'CMCC-ESM2',
                  'CNRM-CM6-1', 'CNRM-ESM2-1', 'CanESM5', 'EC-Earth3', 'EC-Earth3-Veg-LR', 'FGOALS-g3', 'GFDL-CM4',
                  'GFDL-ESM4', 'GISS-E2-1-G', 'HadGEM3-GC31-LL', 'HadGEM3-GC31-MM', 'IITM-ESM', 'INM-CM4-8', 'INM-CM5-0',
                  'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC-ES2L', 'MIROC6', 'MPI-ESM1-2-HR', 'MPI-ESM1-2-LR',
                  'MRI-ESM2-0', 'NESM3', 'NorESM2-LM', 'NorESM2-MM', 'TaiESM1', 'UKESM1-0-LL']
    scenario_list = ['historical', 'ssp245', 'ssp585']

    # Dates
    i_date = str(year_start) + '-01-01'
    f_date = str(year_end)   + '-12-31'
    
    dataset_list = []
    if scenario == 'ssp370':
        base_directory = '/data/keeling/a/cristi/a/downscaled_data/cmip6/nex_gddp/ncs/IL_NEX-GDDP-CMIP6/'
        
        for model in model_list:
            nexgddp_filtered = glob.glob(base_directory + model + '/ssp370/*/' + variable + '/' + variable + '_day_' + model + 
                                        '_ssp370_*')
            if len(nexgddp_filtered) > 0: 
                filtered_dataset = xr.open_mfdataset(nexgddp_filtered,combine="by_coords", use_cftime=True) # Opening datasets
                filtered_dataset = filtered_dataset.assign(time=pd.date_range(start=
                                                                              (str(filtered_dataset.time[0].values).split(' ')[0]),
                                            freq='D',
                                            periods=len(filtered_dataset.time))).sel(time=slice(str(year_start), str(year_end)))
                filtered_dataset['model'] = model
                print(model)
                filtered_dataset.load()
                dataset_list.append(filtered_dataset)
    else:
        # Trigger the authentication flow.
        ee.Authenticate()

        # Initialize the library.
        ee.Initialize(project=project)
    
        # Import NEX-GDDP-CMIP6
        nexgddp = ee.ImageCollection("NASA/GDDP-CMIP6")
        
        # Picking out the Illinois region
        illinois = ee.Geometry.Rectangle([267.2,36,274,43.5])

        
        for model in model_list:
            if model == 'GFDL-CM4':
                nexgddp_filtered = (nexgddp.select(variable).filterDate(i_date, f_date)
                         .filter(ee.Filter.eq('model',model)).filter(ee.Filter.eq('scenario',scenario))
                                    .filter(ee.Filter.eq('grid_label','gr1')))
            else:
                # Filtering out the dataset we want
                nexgddp_filtered = (nexgddp.select(variable).filterDate(i_date, f_date)
                             .filter(ee.Filter.eq('model',model)).filter(ee.Filter.eq('scenario',scenario)))
            if nexgddp_filtered.size().getInfo() > 0:
                filtered_dataset = xr.open_dataset(nexgddp_filtered, engine='ee', scale=0.25, geometry=illinois,
                                                     projection=nexgddp_filtered.first().select(0).projection(),
                                                     use_cftime=True, fast_time_slicing=True)
                filtered_dataset['model'] = model
                print(model)
                filtered_dataset.load()
                dataset_list.append(filtered_dataset)
    
    dataset = xr.concat(dataset_list, dim='model', coords='minimal', compat='override')
    
    # Changing from -180-180 to 0-360 longitude scale
    dataset = dataset.assign_coords({"lon":dataset.lon%360})
    
    # Saving the dataset
    output_file = out_path + '/NEX-GDDP-CMIP6_IL_' + variable + '_' + scenario + '_' + str(year_start) + '-' + str(year_end) + '.nc'
    dataset.to_netcdf(output_file)
    print('Dataset saved to ' + output_file)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year_start", required=True, type=int)
    parser.add_argument("--year_end", required=True, type=int)
    parser.add_argument("--variable", required=True, type=str)
    parser.add_argument("--scenario", required=True, type=str)
    parser.add_argument("--project", required=False, type=str)
    parser.add_argument("--out_path", required=True, type=str)
    args = parser.parse_args()
    
    year_start = args.year_start
    year_end = args.year_end
    variable = args.variable
    scenario = args.scenario
    project = args.project
    out_path = args.out_path
    
    if not project:
        nexgddpcmip6_processing(year_start, year_end, variable, scenario, out_path)
    else:
        nexgddpcmip6_processing(year_start, year_end, variable, scenario, out_path, project)