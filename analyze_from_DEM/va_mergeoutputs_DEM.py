import arcpy
import os
import os.path

# User Inputs 
output_directory = "E:\\independent_study\\visibility_analysis_fromdem"
startloop = 0
endloop = 1009

# Set global variables, variables for produced files
recordnumber = startloop
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

