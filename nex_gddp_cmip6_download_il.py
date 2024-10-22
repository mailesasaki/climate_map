#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
# Set the working directory
os.chdir('/data/keeling/a/ad87/cmip6')
# Verify the change
print("Current Working Directory:", os.getcwd())


# ## Select file of interest form index
# 
# Data available here https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/index.html and filtered with the nex_gddp_cmip6_inventory_files.ipynb; highest version of the file was selected. 
# 
# The file inventory is available here: "latest_inventory.csv".

# In[4]:


import pandas as pd

# List of models to check
# models = [ 
#    "CNRM-ESM2-1","EC-Earth3-Veg-LR", "IPSL-CM6A-LR", "MIROC6", 
#     "MPI-ESM1-2-HR", "MPI-ESM1-2-LR"
# ]

models = [ 
    "CNRM-ESM2-1", "EC-Earth3-Veg-LR", "IPSL-CM6A-LR", 
    "MIROC6", "MPI-ESM1-2-HR", "MPI-ESM1-2-LR", 
    "NorESM2-LM", "UKESM1-0-LL"
]


# List of variables to check
variables = ["tas", "tasmin", "tasmax", "pr"]

# Create a combined regex pattern for models and variables
model_pattern = '|'.join(models)
variable_pattern = '|'.join(variables)
df_latest_inventory = pd.read_csv("tabs/latest_inventory.csv")
# Filter rows where file_path contains any of the models and variables
df = df_latest_inventory[df_latest_inventory['file_path'].str.contains(model_pattern) & 
                                  df_latest_inventory['file_path'].str.contains(variable_pattern)]

# Display the filtered DataFrame
df


# In[7]:


s3_base_path = "s3://nex-gddp-cmip6"
input_path = s3_base_path.join(df[2:2])
# Construct the full S3 path
df['S3_Path'] = s3_base_path + '/' + df['file_path']
# Extract the output directory from the file path
df['Out_Dirs'] = df['file_path'].apply(lambda x: 'ncs/IL_' + '/'.join(x.split('/')[:-1]))
# Create the output file name by replacing the .nc extension with _illinois.nc
df['Out_Files'] = df['file_path'].apply(lambda x: x.split('/')[-1].replace('.nc', '_illinois.nc'))

# Display the DataFrame with the new S3 Path column
print(df)


# Verify data frame

# In[8]:


# Print the first row of the Out_File column
print(df['S3_Path'].iloc[0])

# Extract scenarios using string splitting
scenarios = [fname.split('_')[3] for fname in df['Out_Files']]

# Find unique scenarios
unique_scenarios = set(scenarios)
# Print the unique scenarios
print(unique_scenarios)

unique_out_dirs = set(df['Out_Dirs'])
print(unique_out_dirs)




# Create directories if they don't exist

# In[9]:


for directory in unique_out_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")


# Subset data and write cropped data

# In[6]:


import s3fs
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import io  # Import the io module

# Define latitude and longitude limits for subsetting
min_lat = 36
max_lat = 43.5
min_lon = 267.2
max_lon = 274

# Function to process each file
def process_file(file_path, out_dir, out_file, min_lat = min_lat, max_lat = max_lat, min_lon = min_lon, max_lon = max_lon):

    # Define the output path
    out_path = os.path.join(out_dir, out_file)
     # Check if the output file already exists, and skip if it does
    if os.path.exists(out_path):
        print(f"File {out_path} already exists. Skipping.")
        # Use s3fs to open the file and read its contents into memory
    else:
        fs = s3fs.S3FileSystem(anon=True)
        with fs.open(file_path, 'rb') as f:
            file_content = f.read()  # Read the entire file into memory

        # Create a file-like object from the byte string
        file_like_object = io.BytesIO(file_content)

        # Open the dataset using xarray with engine='h5netcdf'
        ds = xr.open_dataset(file_like_object, engine='h5netcdf')

        # Crop the dataset to the specified lat/lon bounds
        cropped_hurs = ds.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))
 
   
        # Save the cropped dataset to a new NetCDF file
        cropped_hurs.to_netcdf(out_path)
        print(f"Saved cropped file to: {out_path}")




# In[22]:


# # test function
# file_path = df['S3_Path'].iloc[0]
# print(file_path)
# out_dir = df['Out_Dirs'].iloc[0]
# print(out_dir)
# out_file = df['Out_Files'].iloc[0]
# print(out_file)
# process_file(file_path, out_dir, out_file)


# Iterate through the DataFrame and process each file

# In[7]:


for index, row in df.iterrows():
    file_path = row['S3_Path']
    out_dir = row['Out_Dirs']
    out_file = row['Out_Files']
    print(file_path + out_dir+ out_file)
    process_file(file_path, out_dir, out_file)

