# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 11:43:22 2024

@author: mailes2
"""

import urllib
from bs4 import BeautifulSoup
import requests
import fnmatch
from pathlib import Path

def file_downloader(variable):
    models_dict = \
        { "ACCESS-CM2": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}, "ssp245": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}, 
                         "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}, "ssp585": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}},
         "ACCESS-ESM1-5": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, "ssp245": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"},
                   "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, "ssp585": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}}, 
 "AWI-CM-1-1-MR": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, "ssp245": {"r1i1p1f1"}, "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, 
                   "ssp585": {"r1i1p1f1"}}, 
         "BCC-CSM2-MR": {"historical": {"r1i1p1f1"}, "ssp245": {"r1i1p1f1"}, "ssp370": {"r1i1p1f1"}, "ssp585": {"r1i1p1f1"}}, 
 "CESM2-LENS": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1","r8i1p1f1","r9i1p1f1","r10i1p1f1"}, 
                "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1","r8i1p1f1","r9i1p1f1","r10i1p1f1"}}, 
 "CNRM-CM6-1": {"historical": {"r1i1p1f2"}, "ssp245": {"r1i1p1f2"}, "ssp370": {"r1i1p1f2"}, "ssp585": {"r1i1p1f2"}},
 "CNRM-CM6-1-HR": {"historical": {"r1i1p1f2"}, "ssp585": {"r1i1p1f2"}}, 
 "CNRM-ESM2-1": {"historical": {"r1i1p1f2"}, "ssp245": {"r1i1p1f2"}, "ssp370": {"r1i1p1f2"}, "ssp585": {"r1i1p1f2"}},
 "CanESM5": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1"}, "ssp245": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1"},
             "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1"},  "ssp585": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1"}}, 
 "EC-Earth3": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1"},  "ssp245": {"r1i1p1f1","r2i1p1f1","r4i1p1f1"},  "ssp370": {"r1i1p1f1","r4i1p1f1"},
               "ssp585": {"r1i1p1f1","r3i1p1f1","r4i1p1f1"}}, 
 "EC-Earth3-Veg": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, "ssp245": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"},
                   "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1"}, "ssp585": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1"}}, 
 "FGOALS-g3": {"historical": {"r1i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, "ssp245": {"r1i1p1f1","r3i1p1f1","r4i1p1f1"}, "ssp370": {"r1i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"},  
               "ssp585": {"r1i1p1f1","r3i1p1f1","r4i1p1f1"}}, 
 "GFDL-CM4": {"historical": {"r1i1p1f1"},  "ssp245": {"r1i1p1f1"}, "ssp585": {"r1i1p1f1"}},  
 "GFDL-ESM4": {"historical": {"r1i1p1f1"}, "ssp245": {"r1i1p1f1"},  "ssp370": {"r1i1p1f1"},  "ssp585": {"r1i1p1f1"}}, 
 "HadGEM3-GC31-LL": {"historical": {"r1i1p1f3","r2i1p1f3","r3i1p1f3"}, "ssp245": {"r1i1p1f3"}, "ssp585": {"r1i1p1f3","r2i1p1f3","r3i1p1f3"}}, 
 "HadGEM3-GC31-MM": {"historical": {"r1i1p1f3","r2i1p1f3"},  "ssp585": {"r1i1p1f3","r2i1p1f3"}},  
 "INM-CM4-8": {"historical": {"r1i1p1f1"}, "ssp245": {"r1i1p1f1"}, "ssp370": {"r1i1p1f1"}, "ssp585": {"r1i1p1f1"}},  
 "INM-CM5-0": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, "ssp245": {"r1i1p1f1"}, "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"},  
               "ssp585": {"r1i1p1f1"}},  
 "IPSL-CM6A-LR": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1","r8i1p1f1","r9i1p1f1","r10i1p1f1"}, 
                  "ssp245": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"},  
                  "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1","r8i1p1f1","r9i1p1f1","r10i1p1f1"}, 
                  "ssp585": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1"}}, 
 "KACE-1-0-G": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}, "ssp245": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}, "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"},  
                "ssp585": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}}, 
 "MIROC6": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, "ssp245": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}, "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"},
            "ssp585": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}},
 "MPI-ESM1-2-HR": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1","r8i1p1f1","r9i1p1f1","r10i1p1f1"}, "ssp245": {"r1i1p1f1","r2i1p1f1"}, 
                   "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1","r8i1p1f1","r9i1p1f1","r10i1p1f1"}, "ssp585": {"r1i1p1f1","r2i1p1f1"}}, 
 "MPI-ESM1-2-LR": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1","r8i1p1f1","r10i1p1f1"}, 
                   "ssp245": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1","r8i1p1f1","r10i1p1f1"}, 
                   "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r7i1p1f1","r8i1p1f1","r10i1p1f1"}, 
                   "ssp585": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1","r6i1p1f1","r7i1p1f1","r8i1p1f1","r10i1p1f1"}}, 
 "MRI-ESM2-0": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, "ssp245": {"r1i1p1f1"}, "ssp370": {"r1i1p1f1","r2i1p1f1","r3i1p1f1","r4i1p1f1","r5i1p1f1"}, 
                "ssp585": {"r1i1p1f1"}}, 
 "NorESM2-LM": {"historical": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}, "ssp245": {"r1i1p1f1","r2i1p1f1","r3i1p1f1"}, "ssp370": {"r1i1p1f1"}, "ssp585": {"r1i1p1f1"}}, 
 "NorESM2-MM": {"historical": {"r1i1p1f1","r2i1p1f1"}, "ssp245": {"r1i1p1f1","r2i1p1f1"}, "ssp370": {"r1i1p1f1"}, "ssp585": {"r1i1p1f1"}}, 
 "TaiESM1": {"historical": {"r1i1p1f1"}, "ssp245": {"r1i1p1f1"}, "ssp370": {"r1i1p1f1"}} }
    
    #full_dataset_list = []
    for model in models_dict_test:
        for scenario in models_dict_test[model]:
            for memberid in models_dict_test[model][scenario]:
                path_string = ("https://cirrus.ucsd.edu/~pierce/LOCA2/CONUS_regions_split/" + model + "/cent/0p0625deg/" + memberid + "/" + 
                               scenario + "/" + variable + "/")
                path_soup = BeautifulSoup(urllib.request.urlopen(path_string), 'html.parser')
                file_list = []
                for file in path_soup.find_all('a'):
                    file_list.append(file.get('href'))
                file_string = (variable + "." + model + "." + scenario + "." + memberid + ".*.LOCA_16thdeg_*.cent.nc")
                filtered = fnmatch.filter(file_list, file_string)
                directory = (model + "/" + scenario + "/")
                print(directory)
                for filefiltered in filtered:
                  full_string = path_string + filefiltered
                  print(full_string)
                
                  opener = urllib.request.URLopener()
                  if not Path(directory+filefiltered).is_file():
                    opener.retrieve(full_string, (directory+filefiltered))
                    print("Downloaded!")
                #full_dataset_list.append(full_string)
    #return full_dataset_list
    
datasets = file_downloader("pr")

#with open("LOCA2_filenames.txt", 'w') as f:
#    for file in datasets:
#        f.write(f"{file}\n")
