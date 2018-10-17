#!/bin/bash
#----------------------------------------------------
# Amit Chourasia, SDSC
# Example SLURM job script to run 
# VisIt on SDSC's Comet system
#----------------------------------------------------

#SBATCH -J BatchVis                # Job name
#SBATCH -o BatchVis.%j.out         # Name of stdout output file (%j expands to jobId)
#SBATCH -p compute                # Queue name
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=24
#SBATCH -t 00:30:00           # Run time (hh:mm:ss) - 0.5 hours
#SBATCH --mail-type=ALL
#SBATCH --mail-user=esale@ucsd.edu
#SBATCH -A crl155       # <-- Allocation name to charge job against

module unload mvapich2_ib
module unload intel
module load gnu
module load openmpi_ib
module li

# set memory limits to 95% of total memory to prevent node death
#NODE_MEMORY=`free -k | grep ^Mem: | awk '{ print $2; }'`
#NODE_MEMORY_LIMIT=`echo "0.95 * $NODE_MEMORY / 1" | bc`
#ulimit -v $NODE_MEMORY_LIMIT -m $NODE_MEMORY_LIMIT
# echo "memory limit set to $NODE_MEMORY_LIMIT kilobytes"

ulimit -v unlimited -s unlimited 

# set wayness, used for ibrun
#WAYNESS=`echo $PE | perl -pe 's/([0-9]+)way/\1/;'`
#echo "set wayness to $WAYNESS"

#Change to current working dir
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
echo $DIR

# Location of this file i.e. batch_render.sh
echo $SLURM_SUBMIT_DIR

# Set location of render.py, use absolute path
render_script="$SLURM_SUBMIT_DIR/render_noise3d.py"
echo $render_script

# launch visit to run our script render.py as batch process 
/opt/visit/bin/visit -nowin -cli -s $render_script -assume_format 'SILO'

#ibrun  -v  -n 48  -o  0  /opt/visit/bin/visit -nowin -cli -s $render_script -assume_format 'SILO'
# ibrun /oasis/scratch/comet/amit/temp_project/VISIT/bin/visit -nowin -cli -s $render_script -assume_format 'SILO'

# Notes 
# -assume_format 'SILO' needed sometimes so visit can identify correct data reader 
# In this example -assume_format is not needed because 'SILO' is default in VisIt
# but this hidden gem is needed when things are not obvious
