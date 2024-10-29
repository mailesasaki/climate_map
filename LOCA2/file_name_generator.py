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
import argparse

def file_downloader(variable, path_out):
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
    
    for model in models_dict:
        for scenario in models_dict[model]:
            for memberid in models_dict[model][scenario]:
                # Putting together the URL of the data location
                path_string = ("https://cirrus.ucsd.edu/~pierce/LOCA2/CONUS_regions_split/" + model + "/cent/0p0625deg/" + memberid + "/" + 
                               scenario + "/" + variable + "/")
                path_soup = BeautifulSoup(urllib.request.urlopen(path_string), 'html.parser') # Parsing the website to look for the download
                file_list = []
                for file in path_soup.find_all('a'): # Pulling the links
                    file_list.append(file.get('href'))
                file_string = (variable + "." + model + "." + scenario + "." + memberid + ".*.LOCA_16thdeg_*.cent.nc")
                filtered = fnmatch.filter(file_list, file_string) # Looking for specifically the full daily dataset
                directory = (path_out + "/" + model + "/" + scenario + "/") # Pulling out the directory to download into
                print(directory)
                for filefiltered in filtered:
                  full_string = path_string + filefiltered # Putting together the full URL
                  print(full_string)
                
                  opener = urllib.request.URLopener()
                  if not Path(directory+filefiltered).is_file():
                    opener.retrieve(full_string, (directory+filefiltered)) # Downloading
                    print("Downloaded!")
                  else:
                    print("Already downloaded. Skipping")
    
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--variable", required=True, type=str)
  parser.add_argument("--path_out", required=True, type=str)
  args = parser.parse_args()

  variable = args.variable
  path_out = args.path_out
  file_downloader(variable, path_out)
