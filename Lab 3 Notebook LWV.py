import arcpy
import os
from arcpy.sa import *

# Setup
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\Users\Liliana\Documents\ArcGIS\Projects\SalinityDrafting\Salinity_Analysis.gdb"

# Get all processed rasters
all_rasters = arcpy.ListRasters("SSS_20*")
print(f"Found {len(all_rasters)} monthly salinity rasters")


# Calculate global mean
print("Calculating global mean across all months...")
global_mean = CellStatistics(all_rasters, "MEAN", "DATA")

# Save the result
output_name = "Global_Mean_Salinity_2011_2024"
global_mean.save(output_name)
print(f"✓ Global mean saved as: {output_name}")

metadata = """
<title>Global Mean Sea Surface Salinity (2011-2024)</title>
<abstract>Average sea surface salinity calculated from NASA Multi-Mission 
Optimally Interpolated monthly data spanning 2011 to 2024. This represents 
the baseline salinity conditions of the world's oceans over a 14 year period.</abstract>
<tags>salinity, oceanography, NASA, climate</tags>
"""

# Reclassifying to reduce file size for web display and creating a simplified version with fewer classes
simplified_output = "Global_Mean_Salinity_Web"
reclass_ranges = arcpy.sa.RemapRange([
    [0, 20, 1],    # Very low salinity
    [20, 30, 2],   # Low salinity  
    [30, 33, 3],   # Moderate salinity
    [33, 35, 4],   # Normal ocean salinity
    [35, 38, 5],   # High salinity
    [38, 50, 6]    # Very high salinity
])
simplified_raster = arcpy.sa.Reclassify(global_mean, "Value", reclass_ranges)
simplified_raster.save(simplified_output)
print(f"✓ Simplified raster created: {simplified_output}")

# Export to Cloud Optimized GeoTIFF
print("Exporting to Cloud Optimized GeoTIFF...")
output_tiff = r"C:\Users\Liliana\Documents\ArcGIS\Projects\SalinityDrafting\Global_Mean_Salinity.tif"
arcpy.management.CopyRaster(
    simplified_output,
    output_tiff,
    config_keyword="CloudOptimized=YES"
)
print(f"✓ Cloud Optimized GeoTIFF created: {output_tiff}")

from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
    
# Connect to AGOL
print("Connecting to ArcGIS Online...")
gis = GIS("https://www.arcgis.com", "lvalle14", "Basalt00!")
print(f"✓ Connected as: {gis.properties.user.username}")
    

# Using new Folder.add() method 

from arcgis.gis import GIS
import os

# file path
output_tiff = r"C:\Users\Liliana\Documents\ArcGIS\Projects\SalinityDrafting\Global_Mean_Salinity.tif"

# Check file exists
if not os.path.exists(output_tiff):
    print(f"File not found: {output_tiff}")
else:
    print(f"File ready: {os.path.basename(output_tiff)}")
  

# Get user folder
user = gis.users.get(gis.properties.user.username)
folder_name = "SalinityDrafting" 

# add item to the folder
print("\nUploading file...")
item = gis.content.add(
    item_properties={
        "title": "Global Mean Salinity 2011-2024",
        "tags": "salinity, NASA, ocean"
    },
    data=output_tiff,
    folder=folder_name 
)

    print(f"Uploaded! Item: {item.id}")
    
    # Publish
    print("Publishing...")
    published = item.publish()
    
    # Share
    published.share(everyone=True)
    print("Shared publicly!")
    
    print(f"View at: {published.homepage}")
