import arcpy
import os
import os.path

# User Inputs 
input_points = "E:\\independent_study\\Billboardsdata_pghcityplanning\\LamarSigns.shp"
full_dem = "E:\\independent_study\\visibility_analysis\\fullcity_outputmosaic.tif"
buffersize = "1000 Feet"
output_directory = "E:\\independent_study\\visibility_analysis"
offseta = 30
offsetb = 5.5
startloop = 0
endloop = 5

# Set global variables, variables for produced files
recordnumber = startloop
vispix = 0
nvispix = 0
subset_dem = os.path.join(output_directory, 'va_demfiles', 'subset_dem.tif')
full_buffer = os.path.join(output_directory, 'va_output_files', 'va_rALL_buf.shp')
csv_output_file = os.path.join(output_directory, 'va_output_files', 'visibility_analysis.csv')
point_files = []
loop_range = xrange(startloop,endloop)

# Set local functions
def table_prep(tablefile):
	prepwrite = open(tablefile, 'w')
	prepwrite.write("FID,vispix,nvispix,percent_visibility\n")
	prepwrite.close() 

def create_folder(foldername):
	global output_directory
	if os.path.exists(os.path.join(output_directory, foldername)):
		pass
	else:
		os.mkdir(os.path.join(output_directory, foldername))

def file_path(subdirectory, filename):
	create_folder(subdirectory)
	return os.path.join(output_directory, subdirectory, filename)

def output_message(message):
	print message
	arcpy.AddMessage(message)

# Set the workspace for Arc and Python
arcpy.env.workspace = output_directory
os.chdir(output_directory)

# Create a list containing every individual point file and Merge individual points for each record into a new feature class
output_message("Merging point features...")

for recordnumber in loop_range:
	record_name = file_path('va_points', 'va_r%r.shp' % recordnumber)
	point_files.append(record_name)

arcpy.Merge_management(point_files, file_path('va_output_files', 'va_rALLpoints.shp'))

output_message("Complete")

