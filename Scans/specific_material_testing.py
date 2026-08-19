import numpy as np
import uproot
import subprocess
import os

material_dict = {
    'Au':np.linspace(0.001,0.05,30),
    'Ag':np.linspace(0.001,0.2,30),
    'Cu':np.linspace(0.001,0.3,30),
    'W':np.linspace(0.001,0.05,30)
}

#Tests a lot of materials, but also shows the separation of distributions in the resultant csv.

results = np.empty((0,12))

for material,length_list in material_dict.items():
    os.environ['DEGMATERIAL'] = material
    for length in length_list:
        os.environ['SOURCEFILE']='musource_100.txt'
        os.environ['BEAMPART']='mu+'
        os.environ['DEGLENGTH'] = str(length)
        subprocess.run('g4bl $PIM1/piM1_mu.g4bl',shell=True,check=False)
        with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_300_12351.root') as file:
            mu_start_momentum_mean = np.mean(file['NTuple/Z10615;1']['Pz'].array(library="np"))
            mu_end_momentum_mean = np.mean(file['NTuple/Z12140;1']['Pz'].array(library="np"))
            mu_start_momentum_median = np.median(file['NTuple/Z10615;1']['Pz'].array(library="np"))
            mu_end_momentum_median = np.median(file['NTuple/Z12140;1']['Pz'].array(library="np"))
            mu_loss_mean = mu_end_momentum_mean/mu_start_momentum_mean
            mu_loss_median = mu_end_momentum_median/mu_start_momentum_median
        os.environ['SOURCEFILE']='esource_100.txt'
        os.environ['BEAMPART']='e+'
        subprocess.run('g4bl $PIM1/piM1_mu.g4bl',shell=True,check=False)
        with uproot.open('piM1_plastic_decay_bend_air_e+_100_1_300_12351.root') as file:
            e_start_momentum_mean = np.mean(file['NTuple/Z10615;1']['Pz'].array(library="np"))
            e_end_momentum_mean = np.mean(file['NTuple/Z12140;1']['Pz'].array(library="np"))
            e_start_momentum_median = np.median(file['NTuple/Z10615;1']['Pz'].array(library="np"))
            e_end_momentum_median = np.median(file['NTuple/Z12140;1']['Pz'].array(library="np"))
            e_loss_mean = e_end_momentum_mean/e_start_momentum_mean
            e_loss_median = e_end_momentum_median/e_start_momentum_median
        result = ([list(material_dict).index(material),length,mu_loss_mean,mu_loss_median,e_loss_mean,e_loss_median,mu_start_momentum_mean,mu_start_momentum_median,e_start_momentum_mean,e_start_momentum_median,e_loss_mean-mu_loss_mean,e_loss_median-mu_loss_median])
        print(result)
        results = np.vstack((results,result))

np.savetxt('au_ag_cu_momentum_loss_new.csv',results,delimiter=',')
'''
results = np.empty((0,5))
for material,length_list in material_dict.items():
    os.environ['DEGMATERIAL'] = material
    for length in length_list:
        os.environ["SOURCEFILE"]='musource_100.txt'
        os.environ['BEAMPART']='mu+'
        os.environ['DEGLENGTH'] = str(length)
        subprocess.run('g4bl $PIM1/piM1_mu.g4bl',shell=True,check=False)
        with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_300_12351.root') as file:
            mu_start_momentum = np.median(file['NTuple/Z10615;1']['Pz'].array(library="np"))
            mu_end_momentum = np.median(file['NTuple/Z12140;1']['Pz'].array(library="np"))
        momentum_loss = mu_end_momentum/mu_start_momentum
        os.environ["MOMENTUMSCALE"]=momentum_loss
        subprocess.run('g4bl $PIM1/piM1_mu.g4bl',shell=True,check=False)
        with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_300_12351.root') as file:
            mu_count = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
        os.environ["SOURCEFILE"]='esource_100.txt'
        os.environ['BEAMPART']='e+'
        subprocess.run('g4bl $PIM1/piM1_mu.g4bl',shell=True,check=False)
        with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_300_12351.root') as file:
            e_count = len(file['NTuple/Z22159;1']['Pz'].array(library="np"))
        result = ([list(material_dict).index(material),length,momentum_loss,mu_count,e_count])
        print(result)
        results = np.vstack((results,result))

np.savetxt('au_ag_cu_momentum_loss_again.csv',results,delimiter=',')
'''