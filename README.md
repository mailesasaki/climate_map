# Introduction 

This is a repository containing various scripts for downloading and processing data from various downscaled datasets. 

# Table of Contents 

1. [LOCA2](#LOCA2)
2. [NEX-GDDP-CMIP6](#NEX-GDDP-CMIP6)

   
# LOCA2

[LOCA2 Website](https://loca.ucsd.edu/) 

## Details
|          |      |
| :----: | :----: |
| Resolution | 6 x 6 km |
| Extent | [Central Region of US](./docs/images/plot_reg.R.png) |
| Data Location | /data/keeling/a/cristi/a/downscaled_data/LOCA2 |
| Variables | tasmin, tasmax, pr |

| Scenarios | Years |
| :-----: | :-----: |
| historical | 1950-2014 |
| ssp245 | 2015-2100 | 
| ssp370 | 2015-2100 |
| ssp585 | 2015-2100 |

## Models
| Model | Scenario | Experiment ID |
| :----: | :----: | :----: |
| ACCESS-CM2 | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1 |
| ACCESS-CM2 | ssp245 | r1i1p1f1,r2i1p1f1,r3i1p1f1 | 
| ACCESS-CM2 | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1 | 
| ACCESS-CM2 | ssp585 | r1i1p1f1,r2i1p1f1,r3i1p1f1 | 
| ACCESS-ESM1-5 | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 |
| ACCESS-ESM1-5 | ssp245 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 | 
| ACCESS-ESM1-5 | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 | 
| ACCESS-ESM1-5 | ssp585 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 | 
| AWI-CM-1-1-MR | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 |
| AWI-CM-1-1-MR | ssp245 | r1i1p1f1 |
| AWI-CM-1-1-MR | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 |
| AWI-CM-1-1-MR | ssp585 | r1i1p1f1 |
| BCC-CSM2-MR | historical | r1i1p1f1 | 
| BCC-CSM2-MR | ssp245 | r1i1p1f1 |
| BCC-CSM2-MR | ssp370 | r1i1p1f1 |
| BCC-CSM2-MR | ssp585 | r1i1p1f1 |
| CESM2-LENS | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1,r8i1p1f1,r9i1p1f1,r10i1p1f1 | 
| CESM2-LENS | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1,r8i1p1f1,r9i1p1f1,r10i1p1f1 |
| CNRM-CM6-1 | historical | r1i1p1f2 |
| CNRM-CM6-1 | ssp245 | r1i1p1f2 |
| CNRM-CM6-1 | ssp370 | r1i1p1f2 |
| CNRM-CM6-1 | ssp585 | r1i1p1f2 |
| CNRM-CM6-1-HR | historical | r1i1p1f2 | 
| CNRM-CM6-1-HR | ssp585 | r1i1p1f2 |
| CNRM-ESM2-1 | historical | r1i1p1f2 | 
| CNRM-ESM2-1 | ssp245 | r1i1p1f2 |
| CNRM-ESM2-1 | ssp370 | r1i1p1f2 |
| CNRM-ESM2-1 | ssp585 | r1i1p1f2 |
| CanESM5 | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1 | 
| CanESM5 | ssp245 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1 |
| CanESM5 | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1 |
| CanESM5 | ssp585 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1 |
| EC-Earth3 | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1 |
| EC-Earth3 | ssp245 | r1i1p1f1,r2i1p1f1,r4i1p1f1 |
| EC-Earth3 | ssp370 | r1i1p1f1,r4i1p1f1 |
| EC-Earth3 | ssp585 | r1i1p1f1,r3i1p1f1,r4i1p1f1 | 
| EC-Earth3-Veg | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 | 
| EC-Earth3-Veg | ssp245 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 |
| EC-Earth3-Veg | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1 |
| EC-Earth3-Veg | ssp585 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1 |
| FGOALS-g3 | historical | r1i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 |
| FGOALS-g3 | ssp245 | r1i1p1f1,r3i1p1f1,r4i1p1f1 |
| FGOALS-g3 | ssp370 | r1i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 | 
| FGOALS-g3 | ssp585 | r1i1p1f1,r3i1p1f1,r4i1p1f1 |
| GFDL-CM4 | historical | r1i1p1f1 |
| GFDL-CM4 | ssp245 | r1i1p1f1 |
| GFDL-CM4 | ssp585 | r1i1p1f1 |
| GFDL-ESM4 | historical | r1i1p1f1 | 
| GFDL-ESM4 | ssp245 | r1i1p1f1 |
| GFDL-ESM4 | ssp370 | r1i1p1f1 |
| GFDL-ESM4 | ssp585 | r1i1p1f1 |
| HadGEM3-GC31-LL | historical | r1i1p1f3,r2i1p1f3,r3i1p1f3 | 
| HadGEM3-GC31-LL | ssp245 | r1i1p1f3 |
| HadGEM3-GC31-LL | ssp585 | r1i1p1f3,r2i1p1f3,r3i1p1f3 | 
| HadGEM3-GC31-MM | historical | r1i1p1f3,r2i1p1f3 |
| HadGEM3-GC31-MM | ssp585 | r1i1p1f3,r2i1p1f3 |
| INM-CM4-8 | historical | r1i1p1f1 |
| INM-CM4-8 | ssp245 | r1i1p1f1 |
| INM-CM4-8 | ssp370 | r1i1p1f1 |
| INM-CM4-8 | ssp585 | r1i1p1f1 |
| INM-CM5-0 | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 | 
| INM-CM5-0 | ssp245 | r1i1p1f1 |
| INM-CM5-0 | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 | 
| INM-CM5-0 | ssp585 | r1i1p1f1 |
| IPSL-CM6A-LR | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1,r8i1p1f1,r9i1p1f1,r10i1p1f1 | 
| IPSL-CM6A-LR | ssp245 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 |
| IPSL-CM6A-LR | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1,r8i1p1f1,r9i1p1f1,r10i1p1f1 | 
| IPSL-CM6A-LR | ssp585 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1 |
| KACE-1-0-G | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1 |
| KACE-1-0-G | ssp245 | r1i1p1f1,r2i1p1f1,r3i1p1f1 |
| KACE-1-0-G | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1 |
| KACE-1-0-G | ssp585 | r1i1p1f1,r2i1p1f1,r3i1p1f1 |
| MIROC6 | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 | 
| MIROC6 | ssp245 | r1i1p1f1,r2i1p1f1,r3i1p1f1 |
| MIROC6 | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1 |
| MIROC6 | ssp585 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 |
| MPI-ESM1-2-HR | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1,r8i1p1f1,r9i1p1f1,r10i1p1f1 | 
| MPI-ESM1-2-HR | ssp245 | r1i1p1f1,r2i1p1f1 |
| MPI-ESM1-2-HR | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1,r8i1p1f1,r9i1p1f1,r10i1p1f1 | 
| MPI-ESM1-2-HR | ssp585 | r1i1p1f1,r2i1p1f1 |
| MPI-ESM1-2-LR | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1,r8i1p1f1,r10i1p1f1 | 
| MPI-ESM1-2-LR | ssp245 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1,r8i1p1f1,r10i1p1f1 |
| MPI-ESM1-2-LR | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r7i1p1f1,r8i1p1f1,r10i1p1f1 |
| MPI-ESM1-2-LR | ssp585 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1,r6i1p1f1,r7i1p1f1,r8i1p1f1,r10i1p1f1 | 
| MRI-ESM2-0 | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 |
| MRI-ESM2-0 | ssp245 | r1i1p1f1 |
| MRI-ESM2-0 | ssp370 | r1i1p1f1,r2i1p1f1,r3i1p1f1,r4i1p1f1,r5i1p1f1 | 
| MRI-ESM2-0 | ssp585 | r1i1p1f1 |
| NorESM2-LM | historical | r1i1p1f1,r2i1p1f1,r3i1p1f1 |
| NorESM2-LM | ssp245 | r1i1p1f1,r2i1p1f1,r3i1p1f1 |
| NorESM2-LM | ssp370 | r1i1p1f1 |
| NorESM2-LM | ssp585 | r1i1p1f1 |
| NorESM2-MM | historical | r1i1p1f1,r2i1p1f1 | 
| NorESM2-MM | ssp245 | r1i1p1f1,r2i1p1f1 |
| NorESM2-MM | ssp370 | r1i1p1f1 |
| NorESM2-MM | ssp585 | r1i1p1f1 |
| TaiESM1 | historical | r1i1p1f1 |
| TaiESM1 | ssp245 | r1i1p1f1 |
| TaiESM1 | ssp370 | r1i1p1f1 |

## Downloading and Processing

All code is downloaded to /data/keeling/a/cristi/a/downscaled_data/LOCA2.

[Code to download datasets](./LOCA2/file_name_generator.py)

[Code to process datasets](./)

# NEX-GDDP-CMIP6

[NEX-GDDP-CMIP6 Website](https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6) 

## Details

|    |     |
| :----: | :----: |
| Resolution | 25 x 25 km |
| Extent | Worldwide |
| Data Location | Google Earth Engine (data/keeling/a/cristi/a/downscaled_data/cmip6/nex_gddp for ssp370) |
| Variables | hurs, sfcWind |

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

- ## Downloading and Processing

ssp370 data is downloaded to /data/keeling/a/cristi/a/downscaled_data/cmip6/nex_gddp/ncs/IL_NEX-GDDP-CMIP6.
All other data is located on [Google Earth Engine (GEE)](https://developers.google.com/earth-engine/datasets/catalog/NASA_GDDP-CMIP6#description).

[Code to download datasets](./)

[Code to process datasets](./)
