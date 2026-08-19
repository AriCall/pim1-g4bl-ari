import uproot
import os
import subprocess
import numpy as np

#Earlier material and length sweeping.  It is probably better to use all_scan or all_scan with momentumscale, but I've included this as well.

material_dict = {
    #'Al':np.linspace(0.01,8,50),
    #'Be':np.linspace(0.01,1,50),
    'POLYOXYMETHYLENE':np.linspace(0.01,10,50),
    #'Au':np.linspace(0.001,1,50),
}

results = np.empty((0,6))

branch_name = 'NTuple/Z12140;1'

for key, items in material_dict.items():
    os.environ['DEGMATERIAL'] = key
    for length in items:
        os.environ['DEGLENGTH'] = str(length)

        #100 MeV
        os.environ['BEAMMOMENTUM']='100'
        os.environ['SOURCEFILE']='musource_100.txt'
        os.environ['BEAMPART'] = 'mu+'

        subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)

        with uproot.open('piM1_plastic_decay_bend_air_mu+_100_1_300_12351.root') as file:
            mu_end_momenta_100 = np.mean(file[branch_name]['Pz'].array(library="np"))

        os.environ['SOURCEFILE']='esource_100.txt'
        os.environ['BEAMPART'] = 'e+'

        subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)

        with uproot.open('piM1_plastic_decay_bend_air_e+_100_1_300_12351.root') as file:
                pos_end_momenta_100 = np.mean(file[branch_name]['Pz'].array(library="np"))

        #155 MeV
        os.environ['BEAMMOMENTUM']='155'
        os.environ['SOURCEFILE']='musource.txt'
        os.environ['BEAMPART'] = 'mu+'

        subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)

        with uproot.open('piM1_plastic_decay_bend_air_mu+_155_1_300_12351.root') as file:
            mu_end_momenta_155 = np.mean(file[branch_name]['Pz'].array(library="np"))

        os.environ['SOURCEFILE']='musource_but_positron.txt'
        os.environ['BEAMPART'] = 'e+'

        subprocess.run("g4bl $PIM1/piM1_mu.g4bl", shell=True, check=False)

        with uproot.open('piM1_plastic_decay_bend_air_e+_155_1_300_12351.root') as file:
                pos_end_momenta_155 = np.mean(file[branch_name]['Pz'].array(library="np"))

        result = np.array([list(material_dict).index(key),length,mu_end_momenta_100,pos_end_momenta_100,mu_end_momenta_155,pos_end_momenta_155])
                                              
        results = np.vstack((result,results))

np.savetxt('all_materials_testing.csv',results,delimiter=',')