import os
import os.path

# User Inputs (Ideally would be definable parameters instead of having to code in themselves)
	# Should include prepare_table
output_directory = "C:\\Users\\derek\\Documents\\Programs\\testfolders"

# Set local functions
def create_folder(foldername):
	global output_directory
	if os.path.exists(os.path.join(output_directory, foldername)):
		print "Path exists."
	else:
		os.mkdir(os.path.join(output_directory, foldername))

# Set the workspace for Arc and Python
os.chdir(output_directory)

print "Creating folders..."

create_folder('test3')
create_folder('test4')

print "Process complete."