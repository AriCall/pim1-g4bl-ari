import numpy as np
import uproot
import subprocess
import os

'''
Sweeps specifically one material, but includes a failcheck for if the momentum scale finding fails; this is unlikely, but can help remove bad material combinations 
'''

lengths = np.linspace(0.001,1,100)
result = np.empty((0,9))

for length in lengths:
    print(f'length: {length}')
    os.environ['DEGLENGTH']=str(length)
    os.environ['MOMENTUMSCALE']=str(1)
    #run the thing and look at the muon momentum post degrader
    os.environ['NUMEVENTS']='5000'
    os.environ['BEAMPART']='mu+'
    os.environ['SOURCEFILE']='musource_upsampled_pcut_100.txt'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    with uproot.open(f'piM1_plastic_decay_bend_air_mu+_100_1_5_12351.root') as file:
        muon_momentum_start = np.median(file['NTuple/Z10620;1']['Pz'].array(library="np"))
        muon_momentum_end = np.median(file['NTuple/Z12140;1']['Pz'].array(library="np"))
        momentum_scale = muon_momentum_end/155
        failcheck=0
        if len(file['NTuple/Z12140;1']['Pz'].array(library="np")) == 0:
            momentum_scale = 1
            failcheck=1

    #rerun with momentumscale set
    os.environ['NUMEVENTS']='50000'
    os.environ['MOMENTUMSCALE']=str(momentum_scale)
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    os.environ['BEAMPART']='e+'
    os.environ['SOURCEFILE']='esource_upsampled_pcut_100.txt'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    #find the muon momentum change, positron momentum change
    with uproot.open(f'piM1_plastic_decay_bend_air_e+_100_1_5_12351.root') as file:
        pos_momentum_start = np.median(file['NTuple/Z10620;1']['Pz'].array(library="np"))
        pos_momentum_end = np.median(file['NTuple/Z12140;1']['Pz'].array(library="np"))
        pos_count = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
    with uproot.open(f'piM1_plastic_decay_bend_air_mu+_100_1_5_12351.root') as file:
        mu_count = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
    #find the number of muons at the end, number of positrons at the end
    #return
    results = np.array([length,muon_momentum_start,muon_momentum_end,pos_momentum_start,pos_momentum_end,mu_count,pos_count,momentum_scale,failcheck])
    result = np.vstack((result,results))

np.savetxt('plastic_sweep.csv',result,delimiter=',')