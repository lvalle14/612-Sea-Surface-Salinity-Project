# This cell sets up the necessary Python libraries and environment.

import arcpy
import os
from arcpy.sa import *  # Import Spatial Analyst tools for CellStatistics
import matplotlib.pyplot as plt

# Check out the Spatial Analyst extension (for CellStatistics)
arcpy.CheckOutExtension("Spatial")

# Set workspace and overwrite output settings
arcpy.env.overwriteOutput = True
project_workspace = r"C:\Users\Liliana\Documents\ArcGIS\Projects\SalinityDrafting"  
arcpy.env.workspace = project_workspace

# This cell creates a Geodatabase for the project and sets the workspace to the geodatabase.
# Create a File Geodatabase to store processed data
gdb_name = "Salinity_Analysis.gdb"
gdb_path = os.path.join(project_workspace, gdb_name)

if not arcpy.Exists(gdb_path):
    arcpy.management.CreateFileGDB(project_workspace, gdb_name)
    print(f"Created geodatabase: {gdb_path}")
else:
    print(f"Geodatabase already exists: {gdb_path}")

# Set the current workspace to the geodatabase for all outputs
arcpy.env.workspace = gdb_path
print("Environment setup complete.")

# This cell uses a for loop to processes all NETCDF files in a folder, converts them to raster layers, and saves them to the geodatabase.
import glob

netcdf_folder = r"C:\Users\Liliana\Desktop\Monthly Salinity"
netcdf_files = glob.glob(os.path.join(netcdf_folder, "*.nc"))

print(f"Found {len(netcdf_files)} NetCDF files to process")

variable = "sss"
x_dim = "longitude"
y_dim = "latitude"

all_saved_rasters = []

for i, netcdf_file in enumerate(netcdf_files):
    try:
        print(f"Processing {i+1}/{len(netcdf_files)}: {os.path.basename(netcdf_file)}")
        
        base_name = os.path.splitext(os.path.basename(netcdf_file))[0]
        # Extract just the date part (2011-09) and clean it
        base_name = os.path.splitext(os.path.basename(netcdf_file))[0]
        # Extract the date part assuming the format: ..._2011-09.nc
        date_part = base_name.split('_')[-1]  # Gets '2011-09'
        clean_name = date_part.replace('-', '')  # Becomes '201109'

        output_name = f"SSS_{clean_name}"  # e.g., "SSS_201109"
        
        # Create raster layer directly from NetCDF
        arcpy.md.MakeNetCDFRasterLayer(netcdf_file, variable, x_dim, y_dim, "temp_raster")
        
        # Save the full global raster directly to geodatabase 
        arcpy.management.CopyRaster("temp_raster", os.path.join(gdb_path, output_name))
        
        all_saved_rasters.append(output_name)
        arcpy.management.Delete("temp_raster")
        
        print(f"  ✓ Saved full global raster as: {output_name}")
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        continue

print(f"\n=== BATCH PROCESSING COMPLETE ===")
print(f"Processed {len(all_saved_rasters)} full global rasters successfully")
print(f"All rasters saved to: {gdb_path}")

# Save the list of processed rasters for use in later sections
processed_rasters_list = all_saved_rasters
print(f"Raster list saved as 'processed_rasters_list' variable")

# This cell displays a screenshot of the layout including title, legend, scale bar, etc.

# Path to screenshot
screenshot_path = r"C:\Users\Liliana\Desktop\612 photos\lab1_layout_09_11.png" 

if os.path.exists(screenshot_path):
    display(Image(filename=screenshot_path))


