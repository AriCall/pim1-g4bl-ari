
Running
  - g4bl $PIM1/piM1_mu.g4bl
    
Parallel
  - ./run_g4bl_parallel.sh 155
    
Visual
  - g4bl $PIM1/piM1_mu.g4bl viewer=best vcut=0

Before running, the piM1_mu.g4bl file has a few variables that need to be set in the environment.  Baselines for them are in the setup text file, which can be run with:
set -a
. ./setup.txt
set +a

The PIM1 variable is not in that file by base, and needs to be set to the path to the directory that piM1_mu.g4bl is in.

Important variables:
  SOURCEFILE:sets the sourcefile, which can be generated from source_generation from musource.txt.  It should match BEAMMOMENTUM and BEAMPART.
  DEGLENGTH refers to the thickness of the degrader. 
  DEGMATERIAL refers to the material of the degrader. 
  COLLOPEN refers to 1/2 of the size of the opening of FS12, the collimator before the degrader.  It is included in the file name.
  COLLOFFSET can be used to slide the collimator along the x axis.
  NUMEVENTS alters the number of events run.
  SCALE 1 - 18 refer to a linear scale of magnets, listed in increasing order down the beamline.  The last four are tuned, but can be improved.
  MOMENTUMSCALE will scale down all magnets downstream of the degrader by its value.
