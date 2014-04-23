Visibility Analysis
===================

Contents:
---------

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Known Issues/Limitations](#known issues/limitations)
- [Licence and Contribution](#licence and contribution)
- [Contact](#contact)

Overview:
---------

This repository contains a collection of scripts that allow the user to 
test the visibility of a series of points. The user inputs a shapefile 
containing the points of interest, a digital elevation model (DEM), and 
a radius defining the area of analysis around each point. This process 
will then sequentially calculate the percentage of visible pixels within the 
analysis area and output the results to a table. Additonal outputs include
a shapefile representing the areas of analysis, a viewshed raster for each 
point, and an optional shapefile of all the input points with an updated
attribute table reflecting the results of the analysis. 

Installation:
-------------

Dependencies: ArcGIS 10.1, ArcGIS 3D Analyst Extension, arcpy, Python 2.7

- Note: These scripts may run on previous versions of ArcGIS and arcpy, but
they have not been tested.

### Installation Instructions:

Download and extract this repository to a local directory on your computer.

These scripts can be utilized in two ways:

1. As tools

	- The scripts may be packaged as tools within ArcCatalog and stored inside
	a toolbox. This has already been done for you, with the toolbox included in
	this repository.

	- To import the tools, open ArcMap and click on 'Arc Toolbox' either in the
	Geoprocessing drop-down menu or on the standard toolbar. 

	- Within the ArcToolbox window, right click on ArcToolbox and click 
	'Add Toolbox'

	- Navigate to this repository and click on the toolbox.

	- Click open.

	- You're done.

2. As stand-alone scripts:

	- Open your preferred command-line shell, such a PowerShell.

	- Navigate to this repository.

	- Execute scripts using the command `python scriptname.py`


Usage:
------

The intended workflow for this set of tools is as follows:

1. Use va_prep.py to define your area of analysis, clip your input DEM to 
the extent of that defined area of analysis, and create containers for later
outputs of the analysis process. 

	- This script should only be run once. 

	- Viewshedding is one of the most computationally intensive tasks ArcGIS 
	can	perform. This step is intended to reduce the amount of information 
	that must be processed to just the areas that need to be calculated.

	- The outputs of this script are:
		- A series of folders created within your specified output folder

		- A blank .csv file (found in output_folder\\va_output_files)

		- A shapefile displaying your entire analysis extent (found in 
		output_folder\\va_output_files)

		- A raster file containing your clipped DEM (found in output_folder\\
		va_demfiles)

	- The script is configured by opening your favorite text editor and 
	adjusting the values in the User Inputs section. You will have to designate
	a shapefile for the input_points, a raster for the DEM, a buffer distance 
	for the radius of your analysis, and an already existing folder in which 
	you would like process outputs to be stored. Your script should look 
	something like this:

	```````````````````````````````````````````````````````````````````````````
	# User Inputs 
	input_points = "C:\\your_path\\point_data\\input_points.shp"
	full_dem = "C:\\your_path\\DEM_data\\full_dem.tif"
	buffersize = "XXX Units"
	output_directory = "C:\\your_path\\visibility_analysis"
	```````````````````````````````````````````````````````````````````````````

	- Important: Your file paths must contain the double back slash (`\\`)
	separators, not a single back slash (`\`), a forward slash (`\`), or any
	other separator. Also, your filepath must sit between the double quotes.

	- You may specify units for buffersize if you wish. Arc is very specific 
	about how units should be written out (e.g. Feet, Meters, DecimalDegrees).
	Consult Arc documentation for other units if you are having problems. 

	- If you do not specify a unit for buffersize and are running this tool 
	through an .mxd, Arc will automatically use the unit of measure for that 
	map document. 

	- If you are running this as a tool, click on the script in ArcToolbox. 
	You will see a window that says something like "This tool has no 
	parameters." You should have already set those parameters within your
	text editor, so hit 'OK' to run the tool.


2. Use va_analysis.py to calculate the visibility for each pixel within your 
defined buffer radius and export the results to a table that can be opened in 
any text editor and most spreadsheet applications, including Microsoft Excel.

	- This tool may be run on your entire dataset or any number of
	non-overlapping subsets of your data. This is done by setting the 
	startloop and endloop variables in the user inputs section of the script.
	Startloop should be set to the first record you want to include in the 
	analysis, and endloop should be set to the number of the last record you
	want to include in the analysis plus one. 

	- For example, assume we are trying to run an analysis of a point dataset 
	which contains records ranging from 0 to 200. If I wanted to run the 
	analysis in two parts, I would do so by first specifying the loop variables
	to have values like this:

	```````````````````````````````````````````````````````````````````````````
	startloop = 0
	endloop = 100
	```````````````````````````````````````````````````````````````````````````

	This would yield an analysis of records 0 through 99. I could then run 
	another analysis after resetting the values to:

	```````````````````````````````````````````````````````````````````````````
	startloop = 100
	endloop = 201
	```````````````````````````````````````````````````````````````````````````

	This would complete the analysis by analyzing records 100 through 200 and 
	writing the results of the analysis to the same table as the first 
	analysis. Or, you could run it all at once, setting the values to:

	```````````````````````````````````````````````````````````````````````````
	startloop = 0
	endloop = 201
	```````````````````````````````````````````````````````````````````````````

	- In addition to writing the values of the analysis to a .csv table, number
	of visible pixels, number of non-visible pixels, and percentage of visible
	pixels are all written to the attribute table of each individual point file 
	produced by the process.

	- Other outputs of this script are:

		- A buffer for each record.

		- A clipped DEM raster within the buffer radius for each record.

		- A viewshed raster for each record analyzed.

	- Important: The input_points, buffersize, and output_folder variables must
	be set to the same filepaths you set them to in va_prep.py, or this tool 
	won't work.

	- The variables offseta and offsetb are used to account for the fact that 
	you rarely want your point features to sit directly on top of your DEM.
	Offseta represents the height of your point feature above the ground, and 
	offsetb represents the height of your observer. As an example, you may be 
	analyzing the visibility of 30 foot tall features to a person of average 
	height (with 5.5 feet representing average eye level). You would do so by 
	setting the variables like this:

	```````````````````````````````````````````````````````````````````````````
	offseta = "30 Feet"
	offsetb = "5.5 Feet"
	```````````````````````````````````````````````````````````````````````````

	Similar to above, you can specify units for your offset heights (in which 
	case you must wrap the value in double quotes as in the example above), or 
	you can	just set them equal to a number and let Arc use default units for
	the map (if you are using the script as a tool). 

	- If you are running this as a tool, click on the script in ArcToolbox. 
	You will see a window that says something like "This tool has no 
	parameters." You should have already set those parameters within your
	text editor, so hit 'OK' to run the tool.

3. (Optional): Use va_mergeoutputs.py to merge all of the single point features
created at the analysis stage into a new shapefile that reflects the results of
the analysis within its attribute table.

	- If you choose to merge the points created in the last step, only run this 
	script once over the entire range of the data. This script does not
	currently work on a series of non-overlapping subsets of the data.

	- Important: You must specify the same filepath for output_folder in this 
	step as you did in the previous two.

Known Issues/Limitations
------------------------

1. This set of tools will crash if specified filepaths don't exist. This is
remedied by always setting output_folder to the same filepath for the same
project and by never running the analyis script over an overlapping set of 
ranges. If you do run into a crash, take comfort in the fact that the script
is designed such that files are saved at each point in the process. You should
not lose any files due to a crash. The script will either fail to run at the 
outset or will just stop mid-way, leaving you with everything you have already
produced.

2. If any points in your dataset have attributes but no location, va_analysis
will crash at the viewshedding stage when it reaches the first of those points. 
It will still output a point file, buffer file, and clipped DEM, but it will
not perform a visibility calculation and update that result to the .csv output
table. This can be remedied by either running the analysis in steps and skipping
the files that will not work, or by deleting those files from the original 
dataset.

3. Va_mergeoutputs will fail to run in a situation similar to Issue #2. This
can be remedied by either running va_analysis for each offending point in order
to produce a point for va_mergeoutputs to use, or by deleting the offending 
points from the original dataset before performing the analysis.

4. Va_analyis slows down as it analyzes more files. This cannot be corrected by
running the analysis in small steps. The rate that it slows down is roughly 
equal to one extra second of analysis time per record, per hundred records (i.e.
the first 100 records are analyzed in roughly one second, the second 100 in two
seconds, etc.). The only workaround for this is to do the analysis in steps by 
returning to va_prep in each step and specifying a new output folder for use in 
the next analysis. You are probably better off just accepting the speed hit
until this bug can be fixed, given the need to manually merge the .csv outputs
and the need to migrate points to one folder in order to use va_mergeoutputs.

5. Va_mergeoutputs is incredibly slow. It would probably be much faster to use
the .csv output table and perform a join on it and the original input_points
shapefile. Until this can be optimized for better speed, don't use this tool 
unless you need some functionality that you can only get by producing a 
shapefile with the visibility calculations baked into the attribute table. 

6. The accuracy of this analysis is limited by the resolution and accuracy of 
your input DEM. An inaccurate DEM will result in inaccurate visibility
calculations. For example, if you are analyzing over an area containing 
buildings, trees, or some other obstruction, your DEM must reflect those
obstructions, or they will be invisible to the program. Attempting to correct
for this by clipping areas covered by obstructions will not solve this issue,
as the visibility "shadow" cast by an obsturction will not be calculated
in areas blocked from view by that obstruction.

Licence and Contribution
------------------------

Copyright (c) 2014 Derek Feger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


###Contribution

Feel free to contribute to this project by:

1. Forking this repo

2. Creating a new branch for your proposed feature

3. Committing your changes, and

4. Sending a Pull Request

Contact
-------

This project is maintained by Derek Feger and will remain hosted at 
github.com/derekfeger/visibility_analysis. Feel free to report any issues
through the Github issue tracker. Direct any questions to my email at 
<derek.feger@gmail.com> with the subject header "Github Repo Question: 
visibility_analysis"