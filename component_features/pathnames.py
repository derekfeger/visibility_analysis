import os
import os.path

# User Inputs (Ideally would be definable parameters instead of having to code in themselves)
	# Should include prepare_table
output_directory = "C:\\Users\\derek\\Documents\\Programs"

# Set local functions
# tested - works
def create_folder(foldername):
	global output_directory
	if os.path.exists(os.path.join(output_directory, foldername)):
		print "Path exists."
	else:
		os.mkdir(os.path.join(output_directory, foldername))

# untested
def new_file(subdirectory, filename):
	create_folder(subdirectory)
	return os.path.join(output_directory, subdirectory, filename)


# Set the workspace for Arc and Python
os.chdir(output_directory)

print "Beginning process."

print new_file('test_folder', 'test1.txt')
print new_file('test_folder', 'test2.txt')
print new_file('test_folder', 'test3.txt')

print "Process complete."