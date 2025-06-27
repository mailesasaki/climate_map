# NEX-GDDP-CMIP6 Climate Data Processor for Illinois

This tool helps download and process data from NEX-GDDP-CMIP6. 

[NEX-GDDP-CMIP6 Website](https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6) 

[Usage guide for the code](./NEX-GDDP-CMIP6_Guide.ipynb)

## Table of Contents
1. [Dataset details](##Dataset%20details)
2. [Models](##Models)
3. [Downloading and Processing](##Downloading%20and%20Processing)
## Dataset details

|    |     |
| :----: | :----: |
| Resolution | 25 x 25 km |
| Extent (historical, ssp245, ssp585) | Worldwide |
| Extent (ssp370, downloaded) | Illinois |
| Data Location | Google Earth Engine (data/keeling/a/cristi/a/downscaled_data/cmip6/nex_gddp for ssp370) |
| Complete Variables | huss (Near-surface specific humidity) [Mass fraction], sfcWind (Near-surface wind speed) [m/s]|
| Variables w/o ssp375 | hurs (Near surface relative humidity) [%], pr (Precipitation) [kg/m^2/s], rlds (Surface downwelling longwave) [W/m^2], rsds (Surface downwelling shortwave) [W/m^2], tas (Daily near-surface air temp) [K], tasmin (Daily min tas) [K], tasmax (Daily max tas) [K] |
| Derived variables | vp (Vapor pressure) [mb] |  

| Scenario | Years | Data Source |
| :----: | :---: | :---: 
| historical | 1950-2014 | [GEE](https://developers.google.com/earth-engine/datasets/catalog/NASA_GDDP-CMIP6#description) |
| ssp245 | 2015-2100 | GEE |
| ssp370 | 2015-2100 | [Amazon S3](https://aws.amazon.com/marketplace/pp/prodview-k6adk576fiwmm) |
| ssp585 | 2015-2100 | GEE |

## Models
- ACCESS-CM2
- ACCESS-ESM1-5
- BCC-CSM2-MR
- CESM2
- CESM2-WACCM
- CMCC-CM2-SR5
- CMCC-ESM2
- CNRM-CM6-1
- CNRM-ESM2-1
- CanESM5
- EC-Earth3
- EC-Earth3-Veg-LR
- FGOALS-g3
- GFDL-CM4 (grid_label=gr1)
- GFDL-ESM4
- GISS-E2-1-G
- HadGEM3-GC31-LL
- HadGEM3-GC31-MM
- IITM-ESM
- INM-CM4-8
- INM-CM5-0
- IPSL-CM6A-LR
- KACE-1-0-G
- KIOST-ESM
- MIROC-ES2L
- MIROC6
- MPI-ESM1-2-HR
- MPI-ESM1-2-LR
- MRI-ESM2-0
- NESM3
- NorESM2-LM
- NorESM2-MM
- TaiESM1
- UKESM1-0-LL

## Downloading and Processing

ssp370 data is downloaded to /data/keeling/a/cristi/a/downscaled_data/cmip6/nex_gddp/ncs/IL_NEX-GDDP-CMIP6.
All other data is located on [Google Earth Engine (GEE)](https://developers.google.com/earth-engine/datasets/catalog/NASA_GDDP-CMIP6#description).

[Code to download datasets](./nex_gddp_cmip6_download_il.py)

[Code to process datasets](./NEX_GDDP_CMIP6_processor.py)

