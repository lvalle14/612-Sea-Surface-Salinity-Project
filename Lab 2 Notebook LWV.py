import arcpy
from arcpy.stats import *
import os
import matplotlib.pyplot as plt

# Set up environment
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\Users\Liliana\Documents\ArcGIS\Projects\SalinityDrafting\SalinityDrafting.gdb"  
print("✓ Environment setup complete")

# Processed raster from Lab 1
sample_salinity_raster = "SSS_201109" 
# Verify that the raster exists
if arcpy.Exists(sample_salinity_raster):
    print(f"✓ Sample raster found: {sample_salinity_raster}")
    
    # Get basic properties
    desc = arcpy.Describe(sample_salinity_raster)
    print(f"  Extent: {desc.extent}")
    print(f"  Cell size: {desc.meanCellWidth} x {desc.meanCellHeight}")
    print(f"  Spatial reference: {desc.spatialReference.name}")
else:
    print("✗ Sample raster not found. Using first available raster...")
    # Fallback: list available rasters and use the first one
    rasters = arcpy.ListRasters("SSS_Full_*")
    if rasters:
        sample_salinity_raster = rasters[0]
        print(f"✓ Using raster: {sample_salinity_raster}")
    else:
        print("✗ No suitable rasters found. Please check your geodatabase.")

print("✓ Data preparation complete")

# Create output feature class for the points
output_points = "Salinity_Sample_Points"

# Convert raster to points - using systematic sampling for efficiency
print("Converting raster to sample points...")
arcpy.conversion.RasterToPoint(
    "SSS_201109", 
    output_points, 
    "Value"  # This carries the salinity values
)

# Count the points created
point_count = arcpy.management.GetCount(output_points)
print(f"✓ Created {point_count[0]} sample points")

analysis_points = "Salinity_Sample_Points"
salinity_field = "grid_code"

print("Running Global Moran's I...")
moran_result = arcpy.stats.SpatialAutocorrelation(analysis_points, salinity_field, "GENERATE_REPORT")
print("✓ Analysis complete!")

print("="*50)
print("GLOBAL MORAN'S I RESULTS")
print("="*50)
print(f"Moran's I: {morans_i}")
print(f"Z-score: {z_score}")
print(f"P-value: {p_value}")

print("\n" + "="*50)
print("INTERPRETATION")
print("="*50)
print("✓ NULL HYPOTHESIS REJECTED")
print("✓ Salinity is NOT spatially random")
print(f"✓ Moran's I = {morans_i:.4f} indicates very strong clustering")
print("✓ P-value of 0.0 means this result is virtually certain")
print("✓ Z-score of 2884 means this is 2884 standard deviations from random")

# Create visualization of the results
import matplotlib.pyplot as plt
import numpy as np

# Create figure with two side by side subplots (1 row, 2 columns)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Moran's I value interpretation
categories = ['Perfect Dispersion', 'Random', 'Perfect Clustering']
values = [-1, 0, 1]
current_pos = morans_i

# Create horizontal reference line at zero
ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)

# Draw vertical line at our observed Moran's I value
ax1.axvline(x=current_pos, color='red', linestyle='--', alpha=0.7, label=f'Observed I = {morans_i:.4f}')

# Add dot at Moran's I coordinate
ax1.scatter([current_pos], [0], color='red', s=100, zorder=5)

# Set x-axis limits from perfect dispersion to perfect clustering
ax1.set_xlim(-1.1, 1.1)
ax1.set_xlabel("Moran's I Value")
ax1.set_title("Global Moran's I Interpretation")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Statistical significance using p-value
significance_levels = ['90%', '95%', '99%']
p_thresholds = [0.10, 0.05, 0.01]
colors = ['yellow', 'orange', 'red']

# Draw confidence threshold lines with color coding
for i, (level, threshold) in enumerate(zip(significance_levels, p_thresholds)):
    ax2.axhline(y=threshold, color=colors[i], linestyle='-', label=f'{level} confidence')

# Draw line at observed p-value
ax2.axhline(y=p_value, color='blue', linestyle='--', linewidth=2, label=f'Observed p = {p_value:.6f}')

# Highlight p-value position with a dot
ax2.scatter([0], [p_value], color='blue', s=100, zorder=5)

# Use log scale to make p-value visible
ax2.set_yscale('log')
ax2.set_ylabel('P-value (log scale)')
ax2.set_title('Statistical Significance')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-0.5, 0.5)

# Adjust layout and display the figure
plt.tight_layout()
plt.show()



