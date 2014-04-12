import arcpy
import os
import os.path

# User Inputs (Ideally would be definable parameters instead of having to code in themselves)
	# Should include prepare_table
input_points = "F:\\independent_study\\Billboardsdata_pghcityplanning\\LamarSigns.shp"
output_directory = "F:\\independent_study\\visibility_analysis"

# Set global variables, variables for produced files
recordnumber = 0

# Set local functions
def create_folder(foldername):
	global output_directory
	if os.path.exists(os.path.join(output_directory, foldername)):
		pass
	else:
		os.mkdir(os.path.join(output_directory, foldername))

def new_file(subdirectory, filename):
	create_folder(subdirectory)
	return os.path.join(output_directory, subdirectory, filename)

# Set the workspace for Arc and Python
arcpy.env.workspace = output_directory
os.chdir(output_directory)

for recordnumber in range(0,1):

	# Select a record and create a new feature for just that billboard
	arcpy.MakeFeatureLayer_management(input_points, "va_r%r" % recordnumber) 
	arcpy.SelectLayerByAttribute_management("va_r%d" % recordnumber, "NEW_SELECTION", ' "FID" = %d ' % recordnumber)
	arcpy.CopyFeatures_management("va_r%r" % recordnumber, new_file('va_points', 'va_r%r' % recordnumber))
	
	# Adds a field named OffsetA and a field named OffsetB
	arcpy.AddField_management(new_file('va_points', 'va_r%r' % recordnumber), "OffsetA", "TEXT")
	arcpy.AddField_management(new_file('va_points', 'va_r%r' % recordnumber), "OffsetB", "TEXT")