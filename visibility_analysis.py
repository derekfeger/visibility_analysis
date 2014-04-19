import arcpy
import os
import os.path

# User Inputs (Ideally would be definable parameters instead of having to code in themselves)
	# Should include prepare_table
input_points = "E:\\independent_study\\Billboardsdata_pghcityplanning\\LamarSigns.shp"
full_dem = "E:\\independent_study\\visibility_analysis\\fullcity_outputmosaic.tif"
buffersize = "1000 Feet"
csv_output_file = "E:\\independent_study\\visibility_analysis\\visibility_analysis.csv"
output_directory = "E:\\independent_study\\visibility_analysis"
offseta = 30
offsetb = 5.5
startloop = 0
endloop = 5

# Set global variables, variables for produced files
recordnumber = 0
prepare_table = True
vispix = 0
nvispix = 0
subset_dem = os.path.join(output_directory, 'va_demfiles', 'subset_dem.tif')
full_buffer = os.path.join(output_directory, 'va_output_files', 'va_rALL_buf.shp')
loop_range = range(startloop,endloop)

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

def new_file(subdirectory, filename):
	create_folder(subdirectory)
	return os.path.join(output_directory, subdirectory, filename)

# Set the workspace for Arc and Python
arcpy.env.workspace = output_directory
os.chdir(output_directory)

# Creates folders to store output files for later processes
create_folder('va_buffer')
create_folder('va_clip')
create_folder('va_demfiles')
create_folder('va_output_files')
create_folder('va_points')
create_folder('va_viewshed')

# Conducts a test to see if user wants to prepare a table file. If so, runs table_prep. Else, continues on to loop.
if prepare_table == True:
	table_prep(csv_output_file)
else:
	pass

# Clips full DEM to extent of user-defined buffer around input points for faster processing in the loop
arcpy.Buffer_analysis(input_points, full_buffer, buffersize)
arcpy.Clip_management(full_dem, "#", subset_dem, full_buffer, "0", "ClippingGeometry")

# Loops through all records from Record 0 through Record 1008 (should be formatted range(0,1009))
for recordnumber in loop_range:

	# Select a record and create a new feature
	arcpy.MakeFeatureLayer_management(input_points, "va_r%r" % recordnumber) 
	arcpy.SelectLayerByAttribute_management("va_r%d" % recordnumber, "NEW_SELECTION", ' "FID" = %d ' % recordnumber)
	arcpy.CopyFeatures_management("va_r%r" % recordnumber, new_file('va_points', 'va_r%r' % recordnumber))

	# Adds a field named OffsetA and a field named OffsetB
	arcpy.AddField_management(new_file('va_points', 'va_r%r.shp' % recordnumber), "OffsetA", "FLOAT")
	arcpy.AddField_management(new_file('va_points', 'va_r%r.shp' % recordnumber), "OffsetB", "FLOAT")

	# Loops through attribute table, assigns an estimated value to OffsetA, assigns average eye level value to OffsetB
	# Change individual record to input_points when test is complete
	cursor = arcpy.UpdateCursor(new_file('va_points', 'va_r%r.shp' % recordnumber)) 
	for row in cursor:
		global offseta, offsetb
		row.setValue('OffsetA', offseta)
		cursor.updateRow(row)
		row.setValue('OffsetB', offsetb)
		cursor.updateRow(row)
	# Delete curor and row objects to remove data locks
	del row
	del cursor

	# Create a user-defined buffer around current record
	arcpy.Buffer_analysis(new_file('va_points','va_r%r.shp' % recordnumber), new_file('va_buffer', 'va_r%rbuf' % recordnumber), buffersize)

	# Clip the subset DEM to the individual buffer
	arcpy.Clip_management(subset_dem, "#", new_file('va_clip', 'va_r%rclip' % recordnumber), new_file('va_buffer', 'va_r%rbuf.shp' % recordnumber), "0", "ClippingGeometry")

	# Retrieves 3D analyst license, then creates a viewshed within individual DEM, then returns license to license manager
	arcpy.CheckOutExtension("3D")
	arcpy.Viewshed_3d(new_file('va_clip', 'va_r%rclip' % recordnumber), new_file('va_points', 'va_r%r.shp' % recordnumber), new_file('va_viewshed', 'va_r%rvshd' % recordnumber))
	arcpy.CheckInExtension("3D")

	# Pulls number of visible and not-visible pixels out of the table. Stores in variables vispix and nvispix, respectively.
	with arcpy.da.SearchCursor(new_file('va_viewshed', 'va_r%rvshd' % recordnumber), ("COUNT"), ' "Rowid" = 0') as cursor:
		for row in cursor:
			nvispix = row[0]
		
	with arcpy.da.SearchCursor(new_file('va_viewshed', 'va_r%rvshd' % recordnumber), ("COUNT"), ' "Rowid" = 1') as cursor:
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
	for recordnumber in loop_range:
		arcpy.AddField_management(new_file('va_points', 'va_r%r.shp' % recordnumber), "%_visible", "FLOAT")
		cursor = arcpy.UpdateCursor(new_file('va_points', 'va_r%r.shp' % recordnumber)) 
		for row in cursor:
			global percent_visibility
			row.setValue('%_visible', percent_visibility)
			cursor.updateRow(row)
		# Delete curor and row objects to remove data locks
		del row
		del cursor
