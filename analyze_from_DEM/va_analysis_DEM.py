import arcpy
import os
import os.path

# User Inputs 
input_points = "C:\\your_path\\here"
buffersize = "XXX Units"
output_directory = "C:\\your_path\\here"
offseta = 0
offsetb = 0
startloop = 0
endloop = 1

# Set local functions
def table_prep(tablefile):
	prepwrite = open(tablefile, 'w')
	prepwrite.write("FID,vispix,nvispix,percent_visibility\n")
	prepwrite.close() 

def create_folder(foldername):
	global output_directory
	if os.path.exists(os.path.join(output_directory, foldername)):
		pass
	elsC:
		os.mkdir(os.path.join(output_directory, foldername))

def file_path(subdirectory, filename):
	create_folder(subdirectory)
	return os.path.join(output_directory, subdirectory, filename)

def output_message(message):
	print message
	arcpy.AddMessage(message)

# Set global variables, variables for produced files
recordnumber = startloop
vispix = 0
nvispix = 0
subset_dem = file_path('va_demfiles', 'subset_dem.tif')
csv_output_file = file_path('va_output_files', 'visibility_analysis.csv')
loop_range = xrange(startloop,endloop)

# Set the workspace for Arc and Python
arcpy.env.workspace = output_directory
os.chdir(output_directory)

# Loops through all records in specified loop range
for recordnumber in loop_rangC:

	output_message("Analyzing record number %d..." % recordnumber)

	# Select a record and create a new feature
	arcpy.MakeFeatureLayer_management(input_points, "va_r%r" % recordnumber) 
	arcpy.SelectLayerByAttribute_management("va_r%d" % recordnumber, "NEW_SELECTION", ' "FID" = %d ' % recordnumber)
	arcpy.CopyFeatures_management("va_r%r" % recordnumber, file_path('va_points', 'va_r%r' % recordnumber))

	# Adds a field named OffsetA and a field named OffsetB
	arcpy.AddField_management(file_path('va_points', 'va_r%r.shp' % recordnumber), "OffsetA", "FLOAT")
	arcpy.AddField_management(file_path('va_points', 'va_r%r.shp' % recordnumber), "OffsetB", "FLOAT")

	# Loops through attribute table, assigns defined values to OffsetA and OffsetB
	cursor = arcpy.UpdateCursor(file_path('va_points', 'va_r%r.shp' % recordnumber)) 
	for row in cursor:
		global offseta, offsetb
		row.setValue('OffsetA', offseta)
		cursor.updateRow(row)
		row.setValue('OffsetB', offsetb)
		cursor.updateRow(row)
	# Delete cursor and row objects to remove data locks
	del row
	del cursor

	# Create a user-defined buffer around current record
	arcpy.Buffer_analysis(file_path('va_points','va_r%r.shp' % recordnumber), file_path('va_buffer', 'va_r%rbuf' % recordnumber), buffersize)

	# Clip the subset DEM to the individual buffer
	arcpy.Clip_management(subset_dem, "#", file_path('va_clip', 'va_r%rclip' % recordnumber), file_path('va_buffer', 'va_r%rbuf.shp' % recordnumber), "0", "ClippingGeometry")

	# Retrieves 3D analyst license, then creates a viewshed within individual DEM, then returns license to license manager
	arcpy.CheckOutExtension("3D")
	arcpy.Viewshed_3d(file_path('va_clip', 'va_r%rclip' % recordnumber), file_path('va_points', 'va_r%r.shp' % recordnumber), file_path('va_viewshed', 'va_r%rvshd' % recordnumber))
	arcpy.CheckInExtension("3D")

	# Pulls number of visible and not-visible pixels out of the table. Stores in variables vispix and nvispix, respectively.
	with arcpy.da.SearchCursor(file_path('va_viewshed', 'va_r%rvshd' % recordnumber), ("COUNT"), ' "Rowid" = 0') as cursor:
		for row in cursor:
			nvispix = row[0]
		
	with arcpy.da.SearchCursor(file_path('va_viewshed', 'va_r%rvshd' % recordnumber), ("COUNT"), ' "Rowid" = 1') as cursor:
		for row in cursor:
			vispix = row[0]

	# Calculates percent visibility at this record location, converts the quotient to a float, and writes results to a csv file.
	percent_visibility = float(vispix) / (nvispix + vispix)
	append_to_csv = open(csv_output_file, 'a')
	append_to_csv.write("%d,%f,%f,%f\n" % (recordnumber, vispix, nvispix, percent_visibility)) 
	append_to_csv.close()

	# Resets variables vispix and nvispix
	vispix = 0
	nvispix = 0

	# Add a percent visibility field and populate it with the calculated value 
	arcpy.AddField_management(file_path('va_points', 'va_r%r.shp' % recordnumber), "percentvis", "FLOAT")
	cursor = arcpy.UpdateCursor(file_path('va_points', 'va_r%r.shp' % recordnumber)) 
	for row in cursor:
		global percent_visibility
		row.setValue('percentvis', percent_visibility)
		cursor.updateRow(row)
	# Delete curor and row objects to remove data locks
	del row
	del cursor

	output_message("Complete")

output_message("Visibility Analysis Complete")