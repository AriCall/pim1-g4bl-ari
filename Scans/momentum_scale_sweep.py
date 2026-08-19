import numpy as np
import uproot
import os
import subprocess

#Specifically sweeps the momentumscale of a degrader setup.  

scales = np.linspace(0.85,1.0,40)
results = np.empty((0,3))

for scale in scales:
    os.environ['MOMENTUMSCALE']=str(scale)
    os.environ['SOURCEFILE']='musource_upsampled_pcut_100.txt'
    os.environ['BEAMPART']='mu+'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    os.environ['SOURCEFILE']='esource_upsampled_pcut_100.txt'
    os.environ['BEAMPART']='e+'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_5_12351.root') as file:
        mu_count = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
    with uproot.open('piM1_plastic_decay_bend_air_e+_100_1_5_12351.root') as file:
        e_count = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
    result = np.array([scale,mu_count,e_count])
    print(result)
    results = np.vstack((result, results))

np.savetxt('momentum_scale_cuts_plastic10.csv',results,delimiter=',')