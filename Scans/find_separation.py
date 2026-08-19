
'''
Lets you search through degrader lengths until you hit a specific separation of distributions.
'''

import uproot
import hist
import numpy as np
import pandas as pd
import os 
import subprocess
from pimutils import *

separation = 0
deglength = 0

while abs(separation) < 0.0105:
    deglength += 0.005
    os.environ['DEGLENGTH']=str(deglength)
    #do the momentumscale at the second turn
    os.environ['BEAMPART']='mu+'
    os.environ['SOURCEFILE']='musource_100.txt'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    muon_dfs = make_dfs(f'piM1_plastic_decay_bend_air_mu+_100_1_300_12351.root',1)
    after_muons = muon_dfs['NTuple/Z12140;1']
    mu_pz_mean = after_muons['Pz'].mean()
    os.environ['BEAMPART']='e+'
    os.environ['SOURCEFILE']='esource_100.txt'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    pos_dfs = make_dfs(f'piM1_plastic_decay_bend_air_mu+_100_1_300_12351.root',1)
    after_pos = pos_dfs['NTuple/Z12140;1']
    pos_pz_mean = after_pos['Pz'].mean()
    print(separation)
    print(deglength)
    separation = 2*(mu_pz_mean-pos_pz_mean)/(mu_pz_mean+pos_pz_mean)

print('DONE')

    