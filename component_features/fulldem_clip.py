import arcpy
import os.path

# Set the workspace
arcpy.env.workspace = "F:\\independent_study\\visibility_analysis"

# User Inputs (Ideally would be definable parameters instead of having to code in themselves)
	# Should include input point features, full_dem, buffersize
input_points = "F:\\independent_study\\Billboardsdata_pghcityplanning\\LamarSigns.shp"
full_dem = "F:\\independent_study\\visibility_analysis\\fullcity_outputmosaic.tif"
buffersize = "1000 Feet"
csv_output_file = "F:\\independent_study\\visibility_analysis\\visibility_analysis.csv"

# Set global variables, variables for produced files
recordnumber = 0
prepare_table = True
vispix = 0
nvispix = 0
subset_dem = "F:\\independent_study\\visibility_analysis\\dem_files\\clipped_dem.tif"
full_buffer = "F:\\independent_study\\visibility_analysis\\output_files\\va_rALL_buf.shp"

# Buffers input point features to specified buffer size
arcpy.Buffer_analysis(input_points, full_buffer, buffersize)

# Clips full DEM to extent of buffer output_file
#arcpy.Clip_management(full_dem, "#", subset_dem, full_buffer, "#", "ClippingGeometry")

# Retrieves Spatial Analyst licence, extracts by mask to clip dem to full_buffer, returns Spatial Analyst licence to Licence Manager
arcpy.CheckOutExtension("Spatial")
outExtractByMask = arcpy.sa.ExtractByMask(full_dem, full_buffer)
outExtractByMask.save(subset_dem)
arcpy.CheckInExtension("Spatial")