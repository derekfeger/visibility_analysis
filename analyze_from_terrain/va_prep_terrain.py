import arcpy
import os
import os.path

# User Inputs 
input_points = "E:\\independent_study\\Billboardsdata_pghcityplanning\\LamarSigns.shp"
buffersize = "1000 Feet"
output_directory = "E:\\independent_study\\visibility_analysis_fromterrain"

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

# Set global variables, variables for produced files
full_buffer = file_path('va_output_files', 'va_rALL_buf.shp')
csv_output_file = file_path('va_output_files', 'visibility_analysis.csv')

# Set the workspace for Arc and Python
arcpy.env.workspace = output_directory
os.chdir(output_directory)

# Creates folders to store output files for later processes
output_message("Creating folders to store outputs...")

create_folder('va_buffer')
create_folder('va_clip')
create_folder('va_demfiles')
create_folder('va_output_files')
create_folder('va_points')
create_folder('va_viewshed')

output_message("Complete")

# Prepare a table file for output of visibility results
output_message("Preparing output table...")

table_prep(csv_output_file)

output_message("Complete")

