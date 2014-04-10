import arcpy
import os.path

# Set the workspace
arcpy.env.workspace = "E:\\independent_study\\visibility_analysis"

# User Inputs (Ideally would be definable parameters instead of having to code in themselves)
	# Should include input point features, full_dem, buffer size
input_points = os.path.join('E:\\', 'independent_study', 'Billboardsdata_pghcityplanning', 'LamarSigns.shp')
full_dem = "E:\\independent_study\\visibility_analysis\\fullcity_outputmosaic.tif"
buffersize = "1000 Feet"

# Buffers input point features to specified buffer size
arcpy.Buffer_analysis(input_points, "E:\\independent_study\\visibility_analysis\\output_files\\va_rALL_buf.shp", buffersize)

# Clips full DEM to extent of buffer output_file
arcpy.Clip_management(full_dem, "#", "E:\\independent_study\\visibility_analysis\\dem_files\\clipped_dem.tif", "E:\\independent_study\\visibility_analysis\\output_files\\va_rALL_buf.shp", "#", "ClippingGeometry")
