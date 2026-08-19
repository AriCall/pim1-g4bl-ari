import numpy as np
import uproot
from scipy import optimize
import subprocess
import os

'''
An optimizer for a specific material, at a specific energy.  The loss function prefers high muon counts and low contamination.
Uses the scipy optimizer.
'''

def loss(length):
    #input should be a float or numeric
    os.environ['DEGLENGTH']=str(length)
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=True)

    os.environ['SOURCEFILE']='musource_upsampled_pcut_100.txt'
    os.environ['BEAMPART'] = 'mu+'
    os.environ['NUMEVENTS'] = '5000'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_5_12351.root') as file:
        branch_name = 'NTuple/Z12140;1'
        mu_end_momenta = np.mean(file[branch_name]['Pz'].array(library="np"))
        branch_name = 'NTuple/Z10620;1'
        mu_start_momenta = np.mean(file[branch_name]['Pz'].array(library="np"))

    #There may be a case where no particles make it through the degrader; this should be discouraged.
    if np.isnan(mu_end_momenta):
        mu_end_momenta = 100

    os.environ['MOMENTMUMSCALE'] = str(mu_end_momenta/mu_start_momenta)
    os.environ['NUMEVENTS'] = '50000'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_5_12351.root') as file:
        branch_name = 'NTuple/Z22159'
        mu_x = file[branch_name]['x'].array(library="np")
        mu_y = file[branch_name]['y'].array(library="np")
        #mucount_limitless = len(mu_x)
        mucount = ((mu_x < 10) & (mu_y < 10)).sum()

    os.environ['BEAMPART']='e+'
    os.environ['SOURCEFILE']='esource_upsampled_pcut_100.txt'
    subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)
    with uproot.open('piM1_plastic_decay_bend_air_e+_100_1_5_12351.root') as file:
        branch_name = 'NTuple/Z22159'
        pos_x = file[branch_name]['x'].array(library="np")
        pos_y = file[branch_name]['y'].array(library="np")
        #poscount_limitless = len(mu_x)
        poscount = ((pos_x < 10) & (pos_y < 10)).sum()

    if mucount == 0:
        poscount = (poscount+1)*100
        mucount = 1

    contamination = poscount/mucount

    result = contamination/mucount - mucount/contamination

    return result

bound = [(1,12)]

results=dict()

results['DE']=optimize.differential_evolution(loss,bound,workers=1,maxiter=500) #Add maxiter = n if this takes too long
print(results['DE'])
