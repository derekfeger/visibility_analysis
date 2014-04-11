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

# Set local functions
def extract_subsetdem():
	outmask = arcpy.sa.ExtractByMask(full_dem, full_buffer)
	outmask.save(subset_dem)

# Buffers input point features to specified buffer size
arcpy.Buffer_analysis(input_points, full_buffer, buffersize)

# Retrieves Spatial Analyst licence, extracts portions of the full_dem covered by full_buffer, then returns Spatial Analyst licence to licence manager
arcpy.CheckOutExtension("Spatial")
extract_subsetdem()
arcpy.CheckInExtension("Spatial")