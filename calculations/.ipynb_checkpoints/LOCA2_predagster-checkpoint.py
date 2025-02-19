import os
import xarray as xr
import intake
from dotenv import load_dotenv
import numpy as np
import geopandas
import pandas as pd



class OpenLocaCat:
    def __init__(self):
        load_dotenv()

        url = "s3://ees240146/loca2_zarr_monthly_esm_catalog.json"
        catalog = intake.open_esm_datastore(url,
                                            storage_options={
                                            "anon": True,
                                            "endpoint_url": os.environ['S3_ENDPOINT_URL']
                                            })
        
        self.catalog = catalog
        print('Initialized')
        print(catalog)
    
    def load(self, query):
        catalog_subset = self.catalog.search(**query)
        
        dsets = catalog_subset.to_dataset_dict(
                                    xarray_open_kwargs={"use_cftime": True, "engine": 'zarr'},
                                    storage_options={"anon": True, "endpoint_url": os.environ['S3_ENDPOINT_URL']}
                                    )
        
        # Nested list to contain datasets. Nested by scheme, variable, model, and member ID
        dataset_list = [[[[[np.nan, np.nan, np.nan] for _ in catalog_subset.unique()['experiment_id']
                          ] for _ in catalog_subset.unique()['model']
                         ] for _ in catalog_subset.unique()['variable']
                        ] for _ in catalog_subset.unique()['scheme']]

        # Iterates through all datasets and labels them accordingly
        for dataset in dsets:
            dataset_contents = dsets[dataset]
            dataset_contents.coords['member_id'] = dsets[dataset].attrs['intake_esm_attrs:experiment_id']
            dataset_contents.coords['scheme'] = dsets[dataset].attrs['intake_esm_attrs:scheme']
            #dataset_contents.coords['variable'] = dsets[dataset].attrs['intake_esm_attrs:variable']
            dataset_contents.coords['model'] = dsets[dataset].attrs['intake_esm_attrs:model']

        # Estimates amount of time series needed for empty datasets (needed to fill gaps)
        sum_time = 0
        if 'historical' in catalog_subset.unique()['scheme']:
            sum_time += 780
        if any(map(lambda i: i in ['ssp245','ssp370','ssp585'], catalog_subset.unique()['scheme'])):
            sum_time += 1032



        scheme_index = 0
        for scheme in catalog_subset.unique()['scheme']: # Iterate over schemes
            list_scheme = []
            for dataset_key in dsets: # Iterates over all datasets chosen to find the ones to pull
                dataset = dsets[dataset_key]
                if dataset['scheme'] == scheme:
                    list_scheme.append(dataset)
            var_index = 0
            for variable in catalog_subset.unique()['variable']: # Iterate over variables
                list_var = []
                for dataset in list_scheme:
                    if dataset.attrs['intake_esm_attrs:variable'] == variable:
                        list_var.append(dataset)
                model_index = 0
                for model in catalog_subset.unique()['model']: # Iterate over models
                    list_model = []
                    for dataset in list_var:
                        if dataset['model'] == model:
                            list_model.append(dataset)
                    member_index = 0
                    for member_id in catalog_subset.unique()['experiment_id']: # Iterate over member IDs
                        list_id = []
                        for dataset in list_model: # Pick out all datasets along the time series
                            if dataset['member_id'] == member_id:
                                list_id.append(dataset)
                        # Sort dataset so it's in chronological order
                        list_id = sorted(list_id, key=lambda x:x.attrs['intake_esm_attrs:time_range']) 
                        if list_id: #If datasets exist
                            dataset_complete = xr.concat(list_id,'time', coords='minimal', compat='equals') # Concatenate
                            dataset_list[scheme_index][var_index][model_index][member_index] = dataset_complete 
                        else: # If no datasets for this set of parameters
                            # Create an empty dataset with the correct dimensions and labeled accordingly
                            empty_dataset = xr.DataArray(
                                                    np.empty((sum_time,474,944)),
                                                    dims=['time','lat','lon']).to_dataset(name=variable + '_tavg')
                            empty_dataset.coords['member_id'] = member_id
                            empty_dataset.coords['scheme'] = scheme
                            empty_dataset.coords['model'] = model
                            print('Empty!') # Informs the user that there's an empty dataset present
                            dataset_list[scheme_index][var_index][model_index][member_index] = empty_dataset
                        member_index += 1
                    model_index += 1
                var_index += 1
            scheme_index += 1

        dataset_full = xr.combine_nested(dataset_list, concat_dim=['scheme',None,'model','member_id'], fill_value=np.nan, 
                                      compat='no_conflicts', data_vars='different')
        datetimeindex = dataset_full.indexes['time'].to_datetimeindex()
        dataset_full['time'] = datetimeindex
        
        return dataset_full
        
    def stats(self, dataset):
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
    
    def illinois(self, dataset):
        dataset_ill = dataset.sel(lat=slice(36,43.5)).sel(lon=slice(267.2,274))
        
        return dataset_ill

    def parquet(self, dataset, filename):
        
        dataframe = dataset.to_dataframe()
        dataframe_reset = dataframe.reset_index()
        gdf = geopandas.GeoDataFrame(
                dataframe_reset, 
                geometry=geopandas.points_from_xy(dataframe_reset.lon, dataframe_reset.lat), 
                crs="NAD83",
                )

        gdf.to_parquet(filename)


    