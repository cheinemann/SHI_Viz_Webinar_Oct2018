################################################################################
# Sample script that shows how to
# Restore VisIt session with different sources
#
# Amit Chourasia, SDSC, UC San Diego
# Jan Jun, 2015
# CC-BY-SA
################################################################################
import sys, os
import random
from time import clock, time, sleep

#nodes = os.environ['SLURM_NNODES']
#cores = os.environ['SLURM_NTASKS']
tasks = os.environ['SLURM_NTASKS']
home = os.environ['HOME']


# Change the following as needed
################################################################################
# VisIt session file location
# script_dir = os.path.dirname(os.path.realpath(__file__))
script_dir = '/oasis/scratch/comet/jsale/temp_project/viz/batch'
print 'script dir', script_dir
sessionfile = script_dir + '/noise3d_example.session'

# Data we wish to swap from original data in session file with one on stampede
# Note: do not use wildcards
datafile = ('/oasis/scratch/comet/jsale/temp_project/viz/batch/noise.silo')


# Image save information
myOutputDir = script_dir  # Location of output images
myOutFilename = 'noise3d_img_' # Name prefix for output image files
width = 1024  # Image resolution width in pixels
height = 512 # Image resolution width in pixels
################################################################################


# Open parallel compute engine and run on tasks as requested
# This line will be different for other clusters
#OpenComputeEngine("localhost", ("-nn", "1", "-np", str( tasks ), "-l", "ibrun") )
OpenComputeEngine("localhost", ("-nn", "1", "-np", str( tasks )) )

# Run in serial this may be needed sometimes
# OpenComputeEngine("localhost"))

# Restore session will usually not work, unless the session file was
# created on same machine
# RestoreSession(sessionfile, 0)

# We need to restore session from different source
# this way we can create session on our desktop and batch things on cluster
RestoreSessionWithDifferentSources(sessionfile, 0, datafile )


# VisIt does not restore temporal data and time slider correctly
# so reload data in all windows
ga = GetGlobalAttributes()
all_windows = ga.windows # number of windows is a tuple e.g. (1,2,3)
for w in all_windows:
	SetActiveWindow(w) #activate window
	ReOpenDatabase(datafile) #reopen datafile
   	#ToggleLockTime() #lock time slider if not set in session file


#
# file: script_3.py
# example: Animating an Isosurface Operator.
#
 
# Make sure the noise.silo database is open.
 
# Clean up any existing plots.
DeleteAllPlots()
# Create a pseudocolor plot
AddPlot("Pseudocolor", "hardyglobal")
 
# Add an isosurface operator
AddOperator("Isosurface")
 
# Fetch the default Isosurface Operator Attributes
iso_atts = IsosurfaceAttributes()
iso_atts.contourMethod = iso_atts.Value
iso_atts.variable = "hardyglobal"
iso_atts.contourValue = 1.9
 
# Render the plot
DrawPlots()
 
# Animate 30 steps, updating the Isosurface Operator Attributes.
for i in range(30):
   # Set new Isosurface Contour Value
   iso_atts.contourValue = (2 + 0.1*i)
   # Set the attributes of our Isosurface Operator.
   SetOperatorOptions(iso_atts)
   s = SaveWindowAttributes()
   s.outputToCurrentDirectory = 0   # do not write to current dir
   s.outputDirectory = '/oasis/scratch/comet/jsale/temp_project/viz/batch/png/'  # write images to this location
   s.family = 0                     # disable appending 0000 0001 to filename
   s.fileName = "noise3d" + "_%04d" % (i) # setup output image filename
   s.saveTiled = 1                  # if tiling is used
   s.format = s.PNG                 # Use PNG as they are compressed and lossless
   s.width = 1024
   s.height = 1024
   SetSaveWindowAttributes(s)
   SaveWindow()

# Animate time slider. This example does not have one, but lets do it anyways
# for i in range(TimeSliderGetNStates()):

        # Set the save window attributes
#         s = SaveWindowAttributes()
#         s.outputToCurrentDirectory = 0   # do not write to current dir
#         s.outputDirectory = myOutputDir  # write images to this location
#         s.family = 0                     # disable appending 0000 0001 to filename
#         s.fileName = myOutFilename + "_%04d" % (i) # setup output image filename
#         s.saveTiled = 1                  # if tiling is used
#         s.format = s.PNG                 # Use PNG as they are compressed and lossless
#         s.width = width
#         s.height = height
#         SetSaveWindowAttributes(s)

# 	SetTimeSliderState(i)
	# VisIt does not redraw automatically with time change, so make it
# 	DrawPlots()
	# Save the plot window
# 	SaveWindow()


'''
# If needed: clean up everything before closing
for w in all_windows:
	SetActiveWindow(w) #activate window
	DeleteAllPlots()
'''


CloseDatabase(datafile) # close the database

CloseComputeEngine()
sleep(30) # wait for engines to terminate

sys.exit() # required by VisIt
