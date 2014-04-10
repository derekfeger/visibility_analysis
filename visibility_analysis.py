import arcpy
import os.path

# Set the workspace
arcpy.env.workspace = "E:\\independent_study\\visibility_analysis"

# User Inputs (Ideally would be definable parameters instead of having to code in themselves)
	# Should include prepare_table, a buffer size, input point features, dem file, csv output location
csv_output_file = "E:\\independent_study\\visibility_analysis\\visibility_analysis.csv"

# Set global variables
recordnumber = 0
prepare_table = True
vispix = 0
nvispix = 0

# Set local functions
def table_prep(tablefile):
	prepwrite = open(tablefile, 'w')
	prepwrite.write("FID,vispix,nvispix,percent_visibility\n")
	prepwrite.close() 


# Conducts a test to see if user wants to prepare a table file. If so, runs table_prep. Else, continues on to loop.
if prepare_table == True:
	table_prep(csv_output_file)
else:
	pass

# Loops through all records from Record 0 through Record 1008 (should be formatted range(0,1009))
for recordnumber in range(0,1):

	# Select a record and create a new feature for just that billboard
	arcpy.MakeFeatureLayer_management(os.path.join('E:\\', 'independent_study', 'Billboardsdata_pghcityplanning', 'LamarSigns.shp'), "bb_r%r" % recordnumber) 
	arcpy.SelectLayerByAttribute_management("bb_r%d" % recordnumber, "NEW_SELECTION", ' "FID" = %d ' % recordnumber)
	arcpy.CopyFeatures_management("bb_r%r" % recordnumber, "E:\\independent_study\\visibility_analysis\\bboard_points\\bb_r%r" % recordnumber)

	# Create a 1000ft buffer around current billboard
	arcpy.Buffer_analysis("E:\\independent_study\\visibility_analysis\\bboard_points\\bb_r%r.shp" % recordnumber, "E:\\independent_study\\visibility_analysis\\bboard_buffer\\bb_r%rbuf" % recordnumber, "1000 Feet")

	# Clip the full DEM to the individual billboard buffer
	arcpy.Clip_management("E:\\independent_study\\visibility_analysis\\fullclip_test", "#", "E:\\independent_study\\visibility_analysis\\bboard_clip\\bb_r%rclip" % recordnumber, "E:\\independent_study\\visibility_analysis\\bboard_buffer\\bb_r%rbuf.shp" % recordnumber, "#", "ClippingGeometry")

	# Retrieves 3D analyst license, then creates a viewshed within individual DEM, then returns license to license manager
	arcpy.CheckOutExtension("3D")
	arcpy.Viewshed_3d("E:\\independent_study\\visibility_analysis\\bboard_clip\\bb_r%rclip" % recordnumber, "E:\\independent_study\\visibility_analysis\\bboard_points\\bb_r%r.shp" % recordnumber, "E:\\independent_study\\visibility_analysis\\bboard_viewshed\\bb_r%rvshd" % recordnumber)
	arcpy.CheckInExtension("3D")

	# Pulls number of visible and not-visible pixels out of the table. Stores in variables vispix and nvispix, respectively.
	with arcpy.da.SearchCursor("E:\\independent_study\\visibility_analysis\\bboard_viewshed\\bb_r%rvshd" % recordnumber, ("COUNT"), ' "Rowid" = 0') as cursor:
		for row in cursor:
			nvispix = row[0]
		
	with arcpy.da.SearchCursor("E:\\independent_study\\visibility_analysis\\bboard_viewshed\\bb_r%rvshd" % recordnumber, ("COUNT"), ' "Rowid" = 1') as cursor:
		for row in cursor:
			vispix = row[0]

	# Calculates percent visibility at this record location, converts the quotient to a float, and writes results to a csv file.
	percent_visibility = float(vispix) / (nvispix + vispix)
	append_to_csv = open(csv_output_file, 'a')
	append_to_csv.write("%d,%f,%f,%f\n" % (recordnumber, vispix, nvispix, visibility_analysis)) 
	append_to_csv.close()

	# Resets variables vispix and nvispix
	vispix = 0
	nvispix = 0

