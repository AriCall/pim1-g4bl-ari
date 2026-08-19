import numpy as np
import uproot
import os
import subprocess

'''
A smaller scan that specifically sweeps length of a degrader.
'''

lengths = np.linspace(0.01,15,100)

result = np.empty((0,8))

for length in lengths:
    os.environ['DEGLENGTH']=str(length)
    os.environ['MOMENTUMSCALE']=str(1)
    #run the thing and look at the muon momentum post degrader
    os.environ['NUMEVENTS']='5000'
    os.environ['BEAMPART']='mu+'
    os.environ['SOURCEFILE']='musource_100.txt'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_300_12351.root') as file:
        muon_momentum_start = np.median(file['NTuple/Z10620;1']['Pz'].array(library="np"))
        muon_momentum_end = np.median(file['NTuple/Z12140;1']['Pz'].array(library="np"))
        momentum_scale = muon_momentum_end/100
    #rerun with momentumscale set
    os.environ['NUMEVENTS']='10000'
    os.environ['MOMENTUMSCALE']=str(momentum_scale)
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    os.environ['BEAMPART']='e+'
    os.environ['SOURCEFILE']='esource_100.txt'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    #find the muon momentum change, positron momentum change
    with uproot.open('piM1_plastic_decay_bend_air_e+_100_1_300_12351.root') as file:
        pos_momentum_start = np.median(file['NTuple/Z10620;1']['Pz'].array(library="np"))
        pos_momentum_end = np.median(file['NTuple/Z12140;1']['Pz'].array(library="np"))
        pos_count = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
    with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_300_12351.root') as file:
        mu_count = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
    #find the number of muons at the end, number of positrons at the end
    #return
    results = np.array([length,muon_momentum_start,muon_momentum_end,pos_momentum_start,pos_momentum_end,mu_count,pos_count,momentum_scale])
    result = np.vstack((result,results))
    print(results)

np.savetxt('degrader_plastic_100.csv',result,delimiter=',')