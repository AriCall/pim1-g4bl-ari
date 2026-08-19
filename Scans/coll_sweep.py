import numpy as np
import uproot
import os
import subprocess

'''
Sweep through collimator openings (directly before degrader).  Returns a csv with the quantity of muons and positrons at the end.
'''

coll_opens = np.linspace(5,105,50)
all_tested = np.empty((0,3)) #open, x std, y std, count, pz mean, pz start std, pz end std


for coll_open in coll_opens:
    os.environ['COLLOPEN']=str(coll_open)
    os.environ['SOURCEFILE']='musource_upsampled_pcut_100.txt'
    os.environ['BEAMPART']='mu+'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    with uproot.open(f'piM1_plastic_decay_bend_air_mu+_100_1_{coll_open}_12351.root') as file:
        #x_std = np.std(file['NTuple/Z22159;1']['x'].array(library="np"))
        #y_std = np.std(file['NTuple/Z22159;1']['y'].array(library="np"))
        mucount = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
        #pz_mean = np.mean(file['NTuple/Z22159;1']['Pz'].array(library="np"))
        #pz_std_start = np.std(file['NTuple/Z11873;1']['Pz'].array(library="np"))
        #pz_std = np.std(file['NTuple/Z22159;1']['Pz'].array(library="np"))
    os.environ['SOURCEFILE']='esource_upsampled_pcut_100.txt'
    os.environ['BEAMPART']='e+'

    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    with uproot.open(f'piM1_plastic_decay_bend_air_e+_100_1_{coll_open}_12351.root') as file:
        #x_std = np.std(file['NTuple/Z22159;1']['x'].array(library="np"))
        #y_std = np.std(file['NTuple/Z22159;1']['y'].array(library="np"))
        ecount = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
        #pz_mean = np.mean(file['NTuple/Z22159;1']['Pz'].array(library="np"))
        #pz_std_start = np.std(file['NTuple/Z11873;1']['Pz'].array(library="np"))
        #pz_std = np.std(file['NTuple/Z22159;1']['Pz'].array(library="np"))

    result = np.array([coll_open,mucount,ecount])
    os.remove(f'piM1_plastic_decay_bend_air_mu+_100_1_{coll_open}_12351.root')
    os.remove(f'piM1_plastic_decay_bend_air_e+_100_1_{coll_open}_12351.root')
    all_tested = np.vstack((all_tested,result))

np.savetxt('coll_ranges_gold.csv',all_tested,delimiter=',')
