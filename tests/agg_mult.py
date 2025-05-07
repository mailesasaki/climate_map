def weighted_aggregation(path_tif, band, shapefile, crs, time_str):
    """
    Function to do weighted aggregation over counties

    Inputs:
        shapes - (list) Polygons
        band - (int) Band you want (usually time step)
        shapefile - (Geodataframe) Shapefile to fit dataset to 
    Outputs:
        geoframe - (GeoDataFrame) gdf of the original data and geometries
        shapefile - (GeoDataFrame) Data aggregated to shapefile

    """
    dataset_tif = rasterio.open(path_tif)
    shapes = rasterio.features.shapes(rasterio.band(dataset_tif, (band+1)))
            
    pol = list(shapes)
    geom = [shapely.geometry.shape(i[0]) for i in pol]
    # Convert to a GeoSeries
    geom = gpd.GeoSeries(geom, crs=crs)

    if crs != 'NAD83':
        # Convert coordinate reference system
        geom = geom.to_crs('NAD83')
    
    # Extract values as well
    values = [i[1] for i in pol]
    values = pd.Series(values)

    # Create geodataframe
    geoframe = gpd.GeoDataFrame({'value': values, 'geometry': geom})
    
    geoframe['area'] = geoframe.area # Area of each square
    shape_grid = geoframe.overlay(shapefile) # Overlaying the shapefile and the data

    # Creating weighted averages
    shape_grid['area_sub'] = shape_grid.area # Getting area of each square in each shape
    shape_grid['area_prop'] = shape_grid['area_sub'] / shape_grid['area'] # Getting proportional area of each square in each shape
    shape_grid['value_weight'] = shape_grid['value'] * shape_grid['area_prop'] # Getting proportional value based on area

    var_sum_county = shape_grid.groupby('NAME')['value_weight'].sum().reset_index() # Summing data over counties
    area_prop_county = shape_grid.groupby('NAME')['area_prop'].sum().reset_index() # Summing area proportions over counties
    area_prop_county['weight_vals'] = var_sum_county['value_weight'] / area_prop_county['area_prop'] # Dividing total weighted data over weights
    
    shapefile = pd.merge(shapefile, area_prop_county[['NAME', 'weight_vals']], on='NAME', how='left') # Putting the GDF back together
    shapefile = shapefile[['NAME', 'weight_vals', 'geometry']]
    shapefile = shapefile.assign(time=str(time_str[band]))
    
    if band%10 == 0:
        print(band)
    
    return shapefile

#def polygons(path_tif, band, crs):

#    return geom

def agg_call(dataset_io, path_tif, shapefile_path, crs):

    dataset_io = dataset_io.rename({'lon':'x', 'lat':'y'})
    # Open as raster
    dataset_io = dataset_io.rio.write_crs(crs, inplace=True)
    # Save as raster (tiff)
    print(dataset_io.shape)
    if not os.path.exists(path_tif):
        dataset_io.rio.to_raster(path_tif)
    # Opening shapefile
    shapefile = gpd.read_file(shapefile_path)
    
    # List of years
    time_str = [str(i) for i in dataset_io['time'].values]
    
    #pool = multiprocessing.Pool(8)
   # geom_gs = pool.starmap(polygons, zip(, list(range(0,len(time_str))), repeat(crs)))
    
    re = list(zip(repeat(path_tif), list(range(0,len(time_str))), repeat(shapefile), repeat(crs), repeat(time_str)))
    # Iterate over every timestep
    pool = multiprocessing.Pool(8)
    shp_tot = pool.starmap(weighted_aggregation, re)
    #for band in range(0, len(time_str)):
    #    gf, shp = weighted_aggregation(shapes, band, shapefile, crs)
    #    shp = shp.rename({'weight_vals':time_str[band]}, axis='columns')
    #    gf_tot[time_str[band]] = gf
    #    shp_tot[time_str[band]] = shp

    
    # https://www.statology.org/pandas-merge-multiple-dataframes/
    # Merging the geodataframes together so they all have the same geometry
    shp_fuse = pd.concat(shp_tot,ignore_index=True)
    return shp_fuse